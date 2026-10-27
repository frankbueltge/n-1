"""Project 19, session 1: exploration (not registered). For every off-grid declared value of calories, total fat and sodium that
explore1.py could not explain, test a second reading: the per-100 g amount multiplied back by the serving size and rounded to three
significant digits equals the declared value, and a grid number reproduces the stored per-100 g amount.
Usage: python3 explore1c.py <json> <out.json>"""
import json, math, sys
from collections import Counter
sys.path.insert(0, '.')
from count1 import grid_cal, grid_fat, grid_sodium
from explore1 import grid_points, decimals_unit, NUM

def sig3(x):
    if x == 0:
        return 0.0
    return round(x, 2 - int(math.floor(math.log10(abs(x)))))

DEC = json.JSONDecoder()
res = {k: Counter() for k in NUM}
with open(sys.argv[1], encoding='utf-8') as f:
    f.readline()
    for line in f:
        s = line.strip().rstrip(',')
        if not s.startswith('{'):
            continue
        r = DEC.raw_decode(s)[0]
        ln = r.get('labelNutrients') or {}
        ss = r.get('servingSize'); unit = (r.get('servingSizeUnit') or '').lower()
        amounts = {(fn.get('nutrient') or {}).get('number'): fn['amount'] for fn in r.get('foodNutrients') or [] if fn.get('amount') is not None}
        for name, (num, grid) in NUM.items():
            x = (ln.get(name) or {}).get('value')
            if x is None:
                continue
            v = float(x)
            if grid(v):
                res[name]['on_grid'] += 1; continue
            a = amounts.get(num)
            if a is None or not ss or ss <= 0 or unit not in ('g', 'ml', 'grm', 'mlt'):
                res[name]['untestable'] += 1; continue
            back = a * ss / 100.0
            g = grid_points(name, v)
            ghost = abs(g * 100.0 / ss - a) <= decimals_unit(a) / 2 + 1e-9
            s3 = abs(sig3(back) - v) < 1e-9
            res[name][('sig3_' if s3 else 'not_sig3_') + ('grid_behind' if ghost else 'no_grid_behind')] += 1
out = {'note': 'exploratory, written after the count; not registered', 'classes': {k: dict(v) for k, v in res.items()}}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps(out['classes'], indent=1))
