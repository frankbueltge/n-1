#!/usr/bin/env python3
"""Project 24 session 1 check (registered in SELECTION.md): grep, not the count's code, on the decompressed file.
Usage: python3 -I check1.py SESSION1-PER.json STRIPPED.txt OUT.json"""
import json, random, subprocess, sys
per = json.load(open(sys.argv[1])); txt = sys.argv[2]
terms = {}
with open(txt) as f:
    for line in f:
        if line.startswith('A'):
            a, _, body = line.rstrip('\n').partition(' ,'); terms[a] = body.rstrip(',').split(',')
rng = random.Random(20261111)
fin = sorted(r for r in per if r[2] == 'finite'); nev = sorted(r for r in per if r[2] != 'finite')
sample = rng.sample(fin, 12) + rng.sample(nev, 6)
def count(prefix):
    pat = '^A[0-9]+ ,' + ','.join(prefix) + ','
    p = subprocess.run(['grep', '-c', '-E', pat, txt], capture_output=True, text=True)
    return int(p.stdout.strip() or 0)
rows = []; held = 0
for r in sample:
    a, n, kind, L = r[0], r[1], r[2], r[3]
    t = terms[a]
    if kind == 'finite':
        cL = count(t[:L]); cL1 = count(t[:L-1]) if L > 1 else None
        ok = cL == 1 and (L == 1 or cL1 > 1)
        rows.append({'a': a, 'kind': kind, 'L': L, 'grep_L': cL, 'grep_L_minus_1': cL1, 'holds': ok})
    else:
        c = count(t)
        ok = c >= 2
        rows.append({'a': a, 'kind': kind, 'n': n, 'grep_full': c, 'holds': ok})
    held += ok
json.dump({'seed': 20261111, 'held': held, 'of': len(rows), 'rows': rows}, open(sys.argv[3], 'w'), indent=1)
print(held, 'of', len(rows)); [print(x) for x in rows]
