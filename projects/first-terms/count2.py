#!/usr/bin/env python3
"""Project 24, session 2: the search box's own rule (registered in SESSION2.md).

Usage: python3 -I count2.py STRIPPED.gz OUT.json

For every sequence: L (a beginning against beginnings, as session 1), B (its first k terms held as a run by no other
sequence), M (the shortest run anywhere held by no other sequence, and where it stands), hits at six (sequences holding
its first six terms anywhere). Primary signed; secondary with every leading '-' dropped. Terms are strings; each distinct
string gets an integer id; runs are hashed one term longer per pass (64-bit polynomial, wrapping). A run whose hash is
held by one sequence only is unique, and so is every extension, so such start positions leave the next pass.
"""
import gzip, json, re, sys, statistics, collections
import numpy as np

BASE = np.uint64(0x9E3779B97F4A7C15)

def read(path):
    seqs = []
    with gzip.open(path, 'rt', encoding='utf-8', errors='strict') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^(A\d{6,}) ,(.*)$', line)
            if not m:
                raise SystemExit('odd line: ' + line[:80])
            body = m.group(2)
            if body.endswith(','):
                body = body[:-1]
            terms = body.split(',') if body else []
            if not terms:
                continue
            for t in terms:
                if not re.fullmatch(r'-?\d+', t):
                    raise SystemExit('odd term: ' + line[:80])
            seqs.append((m.group(1), terms))
    return seqs

def flatten(seqs, strip_sign):
    ids = {}
    flat = []
    owner = []
    starts = []
    for si, (_, terms) in enumerate(seqs):
        starts.append(len(flat))
        for t in terms:
            if strip_sign and t.startswith('-'):
                t = t[1:]
            flat.append(ids.setdefault(t, len(ids) + 1))
            owner.append(si)
    ends_of = np.array([s + len(seqs[i][1]) for i, s in enumerate(starts)], dtype=np.int64)
    flat = np.array(flat, dtype=np.uint64)
    owner = np.array(owner, dtype=np.int64)
    return flat, owner, np.array(starts, dtype=np.int64), ends_of

def runs(seqs, strip_sign):
    """Return per-sequence B, M, M position, hits at six (by hash pass)."""
    flat, owner, starts, ends = flatten(seqs, strip_sign)
    N = len(seqs)
    T = len(flat)
    seq_end = ends[owner]                     # end (exclusive) of the sequence each position belongs to
    alive = np.arange(T, dtype=np.int64)       # start positions whose run is still shared
    h = np.zeros(T, dtype=np.uint64)
    B = np.zeros(N, dtype=np.int64)            # 0 = not yet / never
    M = np.zeros(N, dtype=np.int64)
    Mpos = np.full(N, -1, dtype=np.int64)
    hits6 = np.zeros(N, dtype=np.int64)
    is_start = np.zeros(T, dtype=bool); is_start[starts] = True
    k = 0
    with np.errstate(over='ignore'):
        while alive.size:
            k += 1
            ok = alive + k - 1 < seq_end[alive]   # the run of length k fits inside its sequence
            alive = alive[ok]
            if not alive.size:
                break
            h[alive] = h[alive] * BASE + flat[alive + k - 1]
            hv = h[alive]; ow = owner[alive]
            order = np.lexsort((ow, hv))
            hs = hv[order]; os_ = ow[order]
            newpair = np.ones(len(hs), dtype=bool)
            newpair[1:] = (hs[1:] != hs[:-1]) | (os_[1:] != os_[:-1])
            uh = hs[newpair]                       # one entry per (hash, sequence)
            gstart = np.ones(len(uh), dtype=bool); gstart[1:] = uh[1:] != uh[:-1]
            gid = np.cumsum(gstart) - 1
            nseq = np.bincount(gid)                # sequences holding each distinct hash
            ghash = uh[gstart]
            cnt = nseq[np.searchsorted(ghash, hv)]  # for every alive position: sequences holding its run
            uniq = cnt == 1
            # M: first k at which some position of s is unique; position = smallest such start
            up = alive[uniq]
            if up.size:
                us = owner[up]
                new = M[us] == 0
                us2 = us[new]; up2 = up[new]
                M[us2] = k
                # smallest position per sequence among those new at this k
                rel = up2 - starts[us2]
                o = np.lexsort((rel, us2))
                first = np.ones(len(o), dtype=bool); first[1:] = us2[o][1:] != us2[o][:-1]
                Mpos[us2[o][first]] = rel[o][first]
            # B: the start position of each sequence
            st = is_start[alive]
            sp = alive[st]; sc = cnt[st]
            if k == 6:
                hits6[owner[sp]] = sc
            bnew = owner[sp[(sc == 1)]]
            bnew = bnew[B[bnew] == 0]
            B[bnew] = k
            alive = alive[~uniq]
    # starts that left before pass 6 were unique already: one hit (themselves)
    n = ends - starts
    hits6[(hits6 == 0) & (n >= 6)] = 1
    return B, M, Mpos, hits6

def lengths_L(seqs):
    order = sorted(range(len(seqs)), key=lambda i: seqs[i][1])
    N = len(order); L = [0] * len(seqs)
    def lcp(a, b):
        m = min(len(a), len(b)); c = 0
        while c < m and a[c] == b[c]: c += 1
        return c
    for p, i in enumerate(order):
        best = 0
        for q in (p - 1, p + 1):
            if 0 <= q < N:
                best = max(best, lcp(seqs[i][1], seqs[order[q]][1]))
        L[i] = best + 1 if best < len(seqs[i][1]) else 0
    return L

def never_kind(seqs, idx):
    """For never-found-alone sequences: twin, beginning of another, or inside another (by string search)."""
    full = {}
    for i, (_, t) in enumerate(seqs):
        full.setdefault(tuple(t), []).append(i)
    kinds = {}
    blob = None
    for i in idx:
        t = tuple(seqs[i][1])
        if len(full[t]) > 1:
            kinds[i] = 'twin'; continue
        kinds[i] = None
    rest = [i for i in idx if kinds[i] is None]
    if rest:
        lines = [',' + ','.join(t) + ',' for _, t in seqs]
        # beginning of another: some other line starts with this run
        sorted_lines = sorted(range(len(lines)), key=lambda j: lines[j])
        import bisect
        keys = [lines[j] for j in sorted_lines]
        for i in rest:
            s = lines[i]
            p = bisect.bisect_left(keys, s)
            found = False
            while p < len(keys) and keys[p].startswith(s):
                if sorted_lines[p] != i:
                    found = True; break
                p += 1
            kinds[i] = 'beginning of another' if found else 'inside another'
    return kinds

def summarise(seqs, B, M, Mpos, hits6, L, label):
    N = len(seqs)
    alone = [i for i in range(N) if B[i] > 0]
    never = [i for i in range(N) if B[i] == 0]
    assert all(M[i] > 0 for i in alone) and all(M[i] == 0 for i in never)
    assert all(B[i] >= M[i] for i in alone)
    assert all(L[i] > 0 and B[i] >= L[i] for i in alone)
    Bs = [int(B[i]) for i in alone]; Ms = [int(M[i]) for i in alone]
    six = [int(hits6[i]) for i in range(N) if len(seqs[i][1]) >= 6]
    out = {
        'label': label,
        'sequences': N,
        'found_alone': len(alone), 'never_found_alone': len(never),
        'never_share': len(never) / N,
        'B_median': statistics.median(Bs), 'B_mean': statistics.mean(Bs), 'B_max': max(Bs),
        'B_max_sequences': [seqs[i][0] for i in alone if B[i] == max(Bs)][:10],
        'M_median': statistics.median(Ms), 'M_mean': statistics.mean(Ms), 'M_max': max(Ms),
        'M_max_sequences': [seqs[i][0] for i in alone if M[i] == max(Ms)][:10],
        'B_gt_L_share': sum(1 for i in alone if B[i] > L[i]) / len(alone),
        'M_lt_B_share': sum(1 for i in alone if M[i] < B[i]) / len(alone),
        'M_at_beginning_share': sum(1 for i in alone if Mpos[i] == 0) / len(alone),
        'hits6_n': len(six), 'hits6_single_share': sum(1 for x in six if x == 1) / len(six),
        'hits6_median': statistics.median(six), 'hits6_max': max(six),
        'B_distribution': dict(sorted(collections.Counter(Bs).items())),
        'M_distribution': dict(sorted(collections.Counter(Ms).items())),
        'hits6_distribution_to_50': {str(k): v for k, v in sorted(collections.Counter(min(x, 51) for x in six).items())},
    }
    return out, never

def main():
    path, outp = sys.argv[1:3]
    seqs = read(path)
    L = lengths_L(seqs)
    res = {}
    per = None
    for strip, label in ((False, 'signed'), (True, 'signs_ignored')):
        B, M, Mpos, h6 = runs(seqs, strip)
        s, never = summarise(seqs, B, M, Mpos, h6, L, label)
        if not strip:
            kinds = never_kind(seqs, never)
            s['never_kinds'] = dict(collections.Counter(kinds.values()))
            per = [[seqs[i][0], len(seqs[i][1]), int(L[i]), int(B[i]), int(M[i]), int(Mpos[i]), int(h6[i]),
                    kinds.get(i)] for i in range(len(seqs))]
            Msigned = M.copy()
        else:
            s['M_changed_vs_signed_share'] = float(np.mean(M != Msigned))
            for row, b, m in zip(per, B, M):
                row += [int(b), int(m)]
        res[label] = s
    Lf = [x for x in L if x > 0]
    res['L_recomputed'] = {'median': statistics.median(Lf), 'never_parted': sum(1 for x in L if x == 0)}
    res['files'] = {'stripped.gz': '7b290f3affeeba00fea62defefc06abbb8a6088310301b7f676e6695f9e62f34'}
    res['per_columns'] = ['anum', 'n_shown', 'L', 'B', 'M', 'M_pos', 'hits6', 'never_kind', 'B_unsigned', 'M_unsigned']
    json.dump(res, open(outp, 'w'), indent=1)
    json.dump(per, open(outp.replace('.json', '-per.json'), 'w'), separators=(',', ':'))
    for lab in ('signed', 'signs_ignored'):
        print(lab, json.dumps({k: v for k, v in res[lab].items() if not k.endswith('distribution') and not k.endswith('to_50')}, indent=1))
    print(res['L_recomputed'])

if __name__ == '__main__':
    main()
