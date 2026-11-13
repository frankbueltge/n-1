#!/usr/bin/env python3
"""Project 24 session 2, exploratory (not registered): where the shortest unique run stands, the extremes by name, examples.
Usage: python3 -I explore2.py SESSION2.json SESSION2-PER.json STRIPPED.txt NAMES.gz OUT.json"""
import json, sys, gzip, collections, statistics, random
S = json.load(open(sys.argv[1])); per = json.load(open(sys.argv[2]))
terms = {}
for line in open(sys.argv[3]):
    if line.startswith('A'):
        a, _, b = line.rstrip('\n').partition(' ,'); terms[a] = b.rstrip(',').split(',')
names = {}
with gzip.open(sys.argv[4], 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        if line.startswith('A'):
            a, _, n = line.rstrip('\n').partition(' '); names[a] = n
alone = [r for r in per if r[3] > 0]
# where the shortest name stands: last tenth of the shown terms, by fraction of position
frac = [r[5] / max(1, r[1] - r[4]) if r[1] > r[4] else 0.0 for r in alone]
dec = collections.Counter(min(9, int(f * 10)) for f in frac)
ends_at_last = sum(1 for r in alone if r[5] + r[4] == r[1])
def ex(a, k=None, pos=None):
    t = terms[a]
    d = {'a': a, 'name': names.get(a, '')[:160], 'n': len(t)}
    if k is not None:
        d['run'] = t[pos:pos + k]
    return d
out = {
    'M_decile_of_position': {str(k): dec[k] for k in range(10)},
    'M_run_ends_at_last_shown_term': ends_at_last, 'found_alone': len(alone),
    'M_eq_1': sum(1 for r in alone if r[4] == 1), 'M_eq_2': sum(1 for r in alone if r[4] == 2),
    'M_max': [ex(r[0], r[4], r[5]) | {'M': r[4], 'pos': r[5]} for r in alone if r[4] == S['signed']['M_max']],
    'B_max': [ex(r[0]) | {'B': r[3], 'L': r[2], 'M': r[4]} for r in alone if r[3] == S['signed']['B_max']],
    'B_minus_L_max': sorted(([r[3] - r[2], r[0], r[2], r[3]] for r in alone), reverse=True)[:10],
    'inside_examples': [],
}
for k in ('A000045', 'A000040', 'A000027', 'A000108', 'A000290', 'A000142', 'A000012', 'A000004'):
    r = next((x for x in per if x[0] == k), None)
    if r:
        out.setdefault('famous', []).append(ex(k, r[4], r[5]) | {'L': r[2], 'B': r[3], 'M': r[4], 'pos': r[5], 'hits6': r[6], 'kind': r[7]})
rng = random.Random(20261113)
ins = sorted(r[0] for r in per if r[7] == 'inside another')
for a in rng.sample(ins, 5):
    out['inside_examples'].append(ex(a))
json.dump(out, open(sys.argv[5], 'w'), indent=1)
print(json.dumps(out, indent=1)[:6000])
