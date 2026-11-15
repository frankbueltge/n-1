#!/usr/bin/env python3
"""Project 24, session 3: what holds what (registered in SESSION3.md).

Usage: python3 -I count3.py STRIPPED.gz NAMES.gz OUT.json PER.json

An edge runs from s to t (t != s) when s's whole shown run stands, consecutively and in order, inside t's shown terms.
Signed terms, compared as strings (each distinct string gets an integer id). For every distinct sequence length n: a
rolling 64-bit polynomial hash of every window of length n inside a sequence, looked up against the whole-run hashes
of the sequences of length n; every hash match is then confirmed by comparing the term ids themselves, so a collision
cannot add an edge. Named(s): distinct other lines of the names file containing s's A-number as a whole word.
"""
import gzip, json, re, sys, statistics, collections
import numpy as np

BASE = np.uint64(0x9E3779B97F4A7C15)
CAP = 200
WORD = re.compile(r'\bA\d{6,}\b')

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

def read_names(path):
    names, named = {}, collections.Counter()
    with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            a, _, name = line.partition(' ')
            names[a] = name
            for x in set(WORD.findall(line)) - {a}:
                named[x] += 1
    return names, named

def edges(seqs):
    ids = {}
    flat, starts = [], []
    for _, terms in seqs:
        starts.append(len(flat))
        for t in terms:
            flat.append(ids.setdefault(t, len(ids) + 1))
    N = len(seqs)
    flat = np.array(flat, dtype=np.uint64)
    starts = np.array(starts, dtype=np.int64)
    lens = np.array([len(t) for _, t in seqs], dtype=np.int64)
    ends = starts + lens
    T = len(flat)
    owner = np.repeat(np.arange(N, dtype=np.int64), lens)
    # prefix hash P[i] = hash of flat[0:i] (Horner, mod 2^64); window [i, i+n) = P[i+n] - P[i] * BASE^n.
    # Vectorised with the inverse of BASE (odd, so invertible mod 2^64): P[i] = BASE^(i-1) * sum_{j<i} flat[j] * BASE^-j.
    inv = 1; b_ = int(BASE)
    for _ in range(7):
        inv = (inv * (2 - b_ * inv)) % (1 << 64)
    assert (inv * b_) % (1 << 64) == 1
    with np.errstate(over='ignore'):
        pw = np.cumprod(np.full(T, BASE, dtype=np.uint64), dtype=np.uint64)          # BASE^(j+1)
        ipw = np.empty(T, dtype=np.uint64); ipw[0] = np.uint64(1)
        if T > 1:
            ipw[1:] = np.cumprod(np.full(T - 1, np.uint64(inv), dtype=np.uint64), dtype=np.uint64)  # BASE^-j
        S = np.cumsum(flat * ipw, dtype=np.uint64)                                       # S[i-1] = sum_{j<i}
        P = np.zeros(T + 1, dtype=np.uint64)
        P[2:] = pw[:-1] * S[1:]
        P[1] = S[0]
    src, dst = [], []
    for n in sorted(set(lens.tolist())):
        targets = np.nonzero(lens == n)[0]
        with np.errstate(over='ignore'):
            pn = np.uint64(1)
            e = BASE; k = n
            while k:
                if k & 1: pn = pn * e
                e = e * e; k >>= 1
            th = P[starts[targets] + n] - P[starts[targets]] * pn
            cand = np.nonzero(lens >= n)[0]
            # all window starts inside sequences of length >= n
            wl = lens[cand] - n + 1
            ws = np.repeat(starts[cand], wl) + (np.arange(wl.sum(), dtype=np.int64) - np.repeat(np.cumsum(wl) - wl, wl))
            wh = P[ws + n] - P[ws] * pn
        order = np.argsort(th, kind='stable'); ths = th[order]; tg = targets[order]
        lo = np.searchsorted(ths, wh, 'left'); hi = np.searchsorted(ths, wh, 'right')
        hit = hi > lo
        if not hit.any():
            continue
        ws = ws[hit]; lo = lo[hit]; hi = hi[hit]
        cnt = hi - lo
        wsr = np.repeat(ws, cnt)
        tix = np.repeat(lo, cnt) + (np.arange(cnt.sum(), dtype=np.int64) - np.repeat(np.cumsum(cnt) - cnt, cnt))
        s = tg[tix]; t = owner[wsr]
        keep = s != t
        s, t, wsr = s[keep], t[keep], wsr[keep]
        # confirm by the term ids themselves, in chunks
        ok = np.ones(len(s), dtype=bool)
        step = max(1, 20_000_000 // n)
        for c0 in range(0, len(s), step):
            a = wsr[c0:c0 + step]; b = starts[s[c0:c0 + step]]
            off = np.arange(n, dtype=np.int64)
            ok[c0:c0 + step] = (flat[a[:, None] + off] == flat[b[:, None] + off]).all(axis=1)
        s, t = s[ok], t[ok]
        pair = np.unique(s * N + t)
        src.append(pair // N); dst.append(pair % N)
    src = np.concatenate(src) if src else np.zeros(0, dtype=np.int64)
    dst = np.concatenate(dst) if dst else np.zeros(0, dtype=np.int64)
    return src, dst, lens

def main():
    sp, np_, outp, perp = sys.argv[1:5]
    seqs = read(sp)
    names, named = read_names(np_)
    N = len(seqs)
    A = [a for a, _ in seqs]
    src, dst, lens = edges(seqs)
    holders = np.bincount(src, minlength=N)
    never = holders > 0
    held = np.bincount(dst, minlength=N)          # never-found-alone sequences each t holds
    twin_e = lens[src] == lens[dst]
    twins = np.bincount(src[twin_e], minlength=N)
    alone_holder = np.bincount(src[~never[dst]], minlength=N) > 0
    # depth: strict containment, by length ascending
    strict = ~twin_e
    ss, dd = src[strict], dst[strict]
    o = np.lexsort((ss, lens[dd])); ss, dd = ss[o], dd[o]   # process edges by holder length ascending
    depth = np.ones(N, dtype=np.int64); prev = np.full(N, -1, dtype=np.int64)
    # holder length strictly exceeds held length, so processing edges in holder-length order is a topological order
    for a, b in zip(ss.tolist(), dd.tolist()):
        if depth[a] + 1 > depth[b]:
            depth[b] = depth[a] + 1; prev[b] = a
    dmax = int(depth.max())
    tops = [i for i in np.argsort(-depth, kind='stable')[:20].tolist() if depth[i] == dmax]
    def chain(i):
        c = [i]
        while prev[c[-1]] >= 0: c.append(int(prev[c[-1]]))
        return [{'a': A[j], 'n': int(lens[j]), 'name': names.get(A[j], '')} for j in c]
    nv = np.nonzero(never)[0]
    av = np.nonzero(~never)[0]
    namedv = np.array([named.get(a, 0) for a in A], dtype=np.int64)
    rank = sorted(range(N), key=lambda i: (-namedv[i], A[i]))
    top100, top1000 = rank[:100], rank[:1000]
    def entry(i):
        return {'a': A[i], 'n': int(lens[i]), 'name': names.get(A[i], ''), 'holders': int(holders[i]), 'holds': int(held[i]),
                'named': int(namedv[i]), 'never_found_alone': bool(never[i])}
    hv = holders[nv]
    most_held = sorted(nv.tolist(), key=lambda i: (-holders[i], A[i]))[:25]
    most_holding = sorted(range(N), key=lambda i: (-held[i], A[i]))[:25]
    share_all = len(nv) / N
    share_1000 = sum(1 for i in top1000 if never[i]) / 1000
    res = {
        'sequences': N, 'edges': int(len(src)), 'twin_edges': int(twin_e.sum()),
        'never_found_alone': int(len(nv)), 'never_share': share_all,
        'holders_median': statistics.median(hv.tolist()), 'holders_mean': float(hv.mean()), 'holders_max': int(hv.max()),
        'holders_distribution': {str(k): v for k, v in sorted(collections.Counter(min(int(x), 101) for x in hv).items())},
        'with_alone_holder': int(alone_holder[nv].sum()), 'with_alone_holder_share': float(alone_holder[nv].mean()),
        'only_twins': int(((twins == holders) & never).sum()),
        'holding_sequences': int((held > 0).sum()), 'holding_and_alone': int(((held > 0) & ~never).sum()),
        'depth_max': dmax, 'depth_distribution_never': {str(k): v for k, v in sorted(collections.Counter(depth[nv].tolist()).items())},
        'deepest_chains': [chain(i) for i in tops[:5]], 'deepest_count': len(tops),
        'most_held': [entry(i) for i in most_held], 'most_holding': [entry(i) for i in most_holding],
        'named_median_never': statistics.median(namedv[nv].tolist()), 'named_median_alone': statistics.median(namedv[av].tolist()),
        'named_mean_never': float(namedv[nv].mean()), 'named_mean_alone': float(namedv[av].mean()),
        'top100_never': sum(1 for i in top100 if never[i]), 'top1000_never_share': share_1000,
        'top1000_ratio': share_1000 / share_all,
        'top100': [entry(i) for i in top100],
        'never_share_by_named': {},
    }
    bands = [(0, 0), (1, 1), (2, 4), (5, 9), (10, 49), (50, 199), (200, 10**9)]
    for lo, hi in bands:
        m = (namedv >= lo) & (namedv <= hi)
        res['never_share_by_named'][f'{lo}-{hi if hi < 10**9 else "max"}'] = {'sequences': int(m.sum()), 'never': int((m & never).sum()),
                                                                             'share': float((m & never).sum() / max(1, m.sum()))}
    P = [
        (1, 401318 <= N <= 401900), (2, 0.018 <= share_all <= 0.022), (3, 1 <= res['holders_median'] <= 3),
        (4, res['with_alone_holder_share'] >= 0.5), (5, dmax >= 6), (6, int(lens[most_held[0]]) <= 3),
        (7, int(held[most_holding[0]]) >= 20), (8, res['top100_never'] >= 30),
        (9, res['named_median_never'] > res['named_median_alone']), (10, res['top1000_ratio'] >= 5),
    ]
    res['predictions'] = {f'P{k}': bool(v) for k, v in P}
    with open(outp, 'w') as f:
        json.dump(res, f, indent=1)
    per = {'never_found_alone': [{'a': A[i], 'n': int(lens[i]), 'holders': int(holders[i]), 'twins': int(twins[i]),
                                  'depth': int(depth[i]), 'named': int(namedv[i]),
                                  'held_by': [A[j] for j in sorted(dst[src == i].tolist())[:CAP]]} for i in nv.tolist()],
           'holding': {A[i]: int(held[i]) for i in np.nonzero(held)[0].tolist()},
           'named_top1000': [[A[i], int(namedv[i]), bool(never[i])] for i in top1000]}
    with open(perp, 'w') as f:
        json.dump(per, f)
    print(json.dumps({k: res[k] for k in ('sequences', 'edges', 'never_found_alone', 'holders_median', 'depth_max',
                                          'top100_never', 'top1000_ratio', 'predictions')}))

if __name__ == '__main__':
    main()
