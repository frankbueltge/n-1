#!/usr/bin/env python3
"""Project 24 session 2 check (registered in SESSION2.md): grep -c -F on the decompressed file, no hashes, no code shared with
the count. Usage: python3 -I check2.py SESSION2-PER.json STRIPPED.txt OUT.json"""
import json, random, subprocess, sys
per = json.load(open(sys.argv[1])); txt = sys.argv[2]
terms = {}
with open(txt) as f:
    for line in f:
        if line.startswith('A'):
            a, _, body = line.rstrip('\n').partition(' ,'); terms[a] = body.rstrip(',').split(',')
rng = random.Random(20261113)
alone = sorted(r for r in per if r[3] > 0); never = sorted(r for r in per if r[3] == 0)
sample = rng.sample(alone, 12) + rng.sample(never, 6)
def lines(run):
    p = subprocess.run(['grep', '-c', '-F', ',' + ','.join(run) + ',', txt], capture_output=True, text=True)
    return int(p.stdout.strip() or 0)
rows = []; held = 0
for r in sample:
    a, n, L, B, M, Mpos = r[:6]
    t = terms[a]
    if B > 0:
        gB = lines(t[:B]); gB1 = lines(t[:B - 1]) if B > 1 else None
        gM = lines(t[Mpos:Mpos + M])
        shorter = [lines(t[i:i + M - 1]) for i in range(0, n - M + 2)] if M > 1 else []
        ok = gB == 1 and (B == 1 or gB1 > 1) and gM == 1 and all(c >= 2 for c in shorter)
        rows.append({'a': a, 'n': n, 'B': B, 'grep_B': gB, 'grep_B_minus_1': gB1, 'M': M, 'M_pos': Mpos, 'grep_M': gM,
                     'runs_of_M_minus_1': len(shorter), 'min_grep_M_minus_1': min(shorter) if shorter else None, 'holds': ok})
    else:
        g = lines(t)
        ok = g >= 2
        rows.append({'a': a, 'n': n, 'kind': r[7], 'grep_full': g, 'holds': ok})
    held += ok
json.dump({'seed': 20261113, 'held': held, 'of': len(rows), 'rows': rows}, open(sys.argv[3], 'w'), indent=1)
print(held, 'of', len(rows)); [print(x) for x in rows]
