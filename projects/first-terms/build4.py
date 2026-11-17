#!/usr/bin/env python3
"""Project 24, session 4: the data of the work *Never the Only Answer* (registered in SESSION4.md).

Usage: python3 build4.py STRIPPED.gz NAMES.gz OUT_DATA.json OUT_SUMMARY.json

Holdings are found by count3.py's hash method (imported, unchanged); every edge is then confirmed by plain string
search -- ",s1,...,sn," inside ",t1,...,tm," -- and an edge the string search does not confirm is dropped and counted.
For every never-found-alone entry the data carries its A-number, name, shown run, and every holder (no cap) with the
holder's name and up to three shown terms before and after the first place the run stands in it.
"""
import json, sys, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from count3 import read, read_names, edges

CTX = 3

def main():
    stripped, names_path, out_data, out_sum = sys.argv[1:5]
    seqs = read(stripped)
    names, _ = read_names(names_path)
    src, dst, lens = edges(seqs)
    joined = [',' + ','.join(t) + ',' for _, t in seqs]
    holders = collections.defaultdict(list)
    failed = 0
    for s, t in zip(src.tolist(), dst.tolist()):
        needle, hay = joined[s], joined[t]
        p = hay.find(needle)
        if p < 0:
            failed += 1
            continue
        k = hay.count(',', 0, p)          # index of the run's first term in t
        n = len(seqs[s][1]); tt = seqs[t][1]
        assert tt[k:k + n] == seqs[s][1]
        holders[s].append((t, k, tt[max(0, k - CTX):k], tt[k + n:k + n + CTX], len(tt)))
    held = sorted(holders, key=lambda i: seqs[i][0])
    need = set(held)
    for s in held:
        need.update(t for t, *_ in holders[s])
    idx = {i: j for j, i in enumerate(sorted(need, key=lambda i: seqs[i][0]))}
    table = [[seqs[i][0], names.get(seqs[i][0], '')] for i in sorted(need, key=lambda i: seqs[i][0])]
    entries = []
    for s in held:
        hs = sorted(holders[s], key=lambda h: seqs[h[0]][0])
        entries.append([idx[s], ','.join(seqs[s][1]),
                        [[idx[t], k, ','.join(b), ','.join(a), L] for t, k, b, a, L in hs]])
    data = {'source': 'The On-Line Encyclopedia of Integer Sequences, https://oeis.org/ (CC BY-SA 4.0); stripped.gz and names.gz of 2026-11-16',
            'seqs': table, 'entries': entries}
    with open(out_data, 'w') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
    top = sorted(held, key=lambda i: (-len(holders[i]), seqs[i][0]))[:10]
    summary = {'sequences': len(seqs), 'never_found_alone': len(held),
               'holdings': sum(len(v) for v in holders.values()), 'hash_edges': int(len(src)),
               'string_failed': failed, 'data_bytes': os.path.getsize(out_data),
               'involved_sequences': len(table),
               'most_held': [[seqs[i][0], names.get(seqs[i][0], ''), len(holders[i])] for i in top]}
    with open(out_sum, 'w') as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main()
