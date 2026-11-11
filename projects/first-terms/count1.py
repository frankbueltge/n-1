#!/usr/bin/env python3
"""Project 24, session 1: identifying length of every OEIS sequence (registered in SELECTION.md).

Usage: python3 -I count1.py STRIPPED.gz NAMES.gz OUT.json
Reads the stripped file (A-number and shown terms), computes for every sequence the smallest k such that no other
sequence's first k terms equal its first k terms; sequences with no such k are 'never parted' (twin or beginning of
another). Terms are compared as strings; nothing is converted to a number.
"""
import gzip, json, sys, statistics, collections, re

def read_stripped(path):
    seqs = []  # (anum, tuple of term strings)
    header = 0; empty = 0; odd = []
    with gzip.open(path, 'rt', encoding='utf-8', errors='strict') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                header += 1; continue
            m = re.match(r'^(A\d{6,}) ,(.*)$', line)
            if not m:
                odd.append(line[:80]); continue
            body = m.group(2)
            if body.endswith(','): body = body[:-1]
            terms = tuple(t for t in body.split(',')) if body else ()
            if not terms or any(not re.fullmatch(r'-?\d+', t) for t in terms):
                if not terms: empty += 1; continue
                odd.append(line[:80]); continue
            seqs.append((m.group(1), terms))
    return seqs, header, empty, odd

def read_names(path):
    names = {}
    with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('#') or not line.strip(): continue
            a, _, n = line.rstrip('\n').partition(' ')
            names[a] = n
    return names

def identifying_lengths(seqs):
    # sort by terms (tuple of strings compares lexicographically, prefixes first)
    order = sorted(range(len(seqs)), key=lambda i: seqs[i][1])
    def lcp(a, b):
        n = min(len(a), len(b)); k = 0
        while k < n and a[k] == b[k]: k += 1
        return k
    N = len(order)
    res = {}
    for pos, i in enumerate(order):
        t = seqs[i][1]
        best = 0; partner = None
        # the maximal common prefix with any other sequence is attained at a sorted neighbour,
        # but equal-term runs need scanning: neighbours within the sorted order suffice for max lcp.
        for q in (pos - 1, pos + 1):
            if 0 <= q < N:
                j = order[q]
                c = lcp(t, seqs[j][1])
                if c > best or (c == best and partner is None):
                    best, partner = c, j
        n = len(t)
        if best < n:
            res[i] = ('finite', best + 1, partner if best > 0 else None, best)
        else:
            # every term shared: twin if some other sequence has exactly these terms
            twin = None
            for q in (pos - 1, pos + 1):
                if 0 <= q < N and seqs[order[q]][1] == t:
                    twin = order[q]; break
            if twin is not None:
                res[i] = ('twin', None, twin, best)
            else:
                res[i] = ('beginning', None, partner, best)
    return res

def main():
    sp, np_, out = sys.argv[1:4]
    seqs, header, empty, odd = read_stripped(sp)
    names = read_names(np_)
    res = identifying_lengths(seqs)
    N = len(seqs)
    fin = [res[i][1] for i in range(N) if res[i][0] == 'finite']
    nshown = [len(s[1]) for s in seqs]
    twins = [i for i in range(N) if res[i][0] == 'twin']
    begs = [i for i in range(N) if res[i][0] == 'beginning']
    dist = collections.Counter(fin)
    p6 = collections.Counter(s[1][:6] for s in seqs if len(s[1]) >= 6)
    top6 = p6.most_common(10)
    def anum_int(a): return int(a[1:])
    low = [res[i][1] for i in range(N) if res[i][0] == 'finite' and anum_int(seqs[i][0]) < 100000]
    high = [res[i][1] for i in range(N) if res[i][0] == 'finite' and anum_int(seqs[i][0]) >= 300000]
    maxL = max(fin) if fin else None
    maxL_seqs = [seqs[i][0] for i in range(N) if res[i][0] == 'finite' and res[i][1] == maxL]
    deadpat = re.compile(r'^(Duplicate of|Erroneous)|\bdead\b', re.I)
    dead = set(a for a, n in names.items() if deadpat.search(n))
    fin_alive = [res[i][1] for i in range(N) if res[i][0] == 'finite' and seqs[i][0] not in dead]
    per = []
    for i in range(N):
        kind, L, partner, shared = res[i]
        per.append([seqs[i][0], len(seqs[i][1]), kind, L, seqs[partner][0] if partner is not None else None, shared])
    largest = sorted((r for r in per if r[2] == 'finite'), key=lambda r: -r[3])[:25]
    summary = {
        'files': {'stripped.gz': 'd3088c0f00bf14c3a81d94b78671816923b52349d2d106d553433e07b4c290bb',
                  'names.gz': '9d8001c3478be2e0d09d3ba6babf5f79718de518b81ffcb83aa2346e0af6d083'},
        'header_lines': header, 'lines_without_terms': empty, 'odd_lines': len(odd), 'odd_examples': odd[:5],
        'sequences': N, 'names': len(names),
        'shown_terms_median': statistics.median(nshown),
        'finite': len(fin), 'twin': len(twins), 'beginning_of_another': len(begs),
        'never_parted': len(twins) + len(begs),
        'never_parted_share': (len(twins) + len(begs)) / N,
        'L_median': statistics.median(fin), 'L_mean': statistics.mean(fin),
        'L_le3_share': sum(1 for x in fin if x <= 3) / len(fin),
        'L_gt12_share': sum(1 for x in fin if x > 12) / len(fin),
        'L_max': maxL, 'L_max_sequences': maxL_seqs[:10],
        'L_distribution': {str(k): dist[k] for k in sorted(dist)},
        'top_prefix6': [[','.join(k), v] for k, v in top6],
        'L_median_below_A100000': statistics.median(low) if low else None, 'n_below_A100000': len(low),
        'L_median_A300000_up': statistics.median(high) if high else None, 'n_A300000_up': len(high),
        'secondary_dead_pattern': deadpat.pattern, 'secondary_dead_names': len(dead),
        'secondary_L_median_without_dead': statistics.median(fin_alive) if fin_alive else None,
        'largest_L': largest,
    }
    json.dump({'summary': summary}, open(out, 'w'), indent=1)
    json.dump(per, open(out.replace('.json', '-per.json'), 'w'), separators=(',', ':'))
    print(json.dumps({k: v for k, v in summary.items() if k not in ('L_distribution', 'largest_L')}, indent=1))

if __name__ == '__main__':
    main()
