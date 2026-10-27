"""Project 19, session 1: exploration, written after the count (not registered).
Hypothesis from the off-grid values seen: the record's per-serving labelNutrients are per-100 g amounts multiplied back by the serving
size, so a printed on-grid number returns slightly off. For each declared calorie value (kcal) with an energy amount per 100 g
(nutrient number 208, kcal) and a serving size, test:
  back  = amount_per_100g * servingSize / 100, compared with the declared value (to 0.05, one decimal);
  ghost = the grid point g nearest the declared value, and whether g would have produced the stored per-100 g amount
          (|g * 100 / servingSize - amount| <= half the stored amount's last decimal unit).
Classes: on grid; off grid and explained (back matches, and a grid point reproduces the stored amount); off grid, not explained.
Same for total fat (nutrient 204) and sodium (307).
Usage: python3 -I explore1.py <json> <out.json>
"""
import json, sys
from collections import Counter
sys.path.insert(0, '.')
from count1 import grid_cal, grid_fat, grid_sodium

def grid_points(name, v):
    if name == 'calories':
        c = [0.0] + [5.0 * i for i in range(1, 11)] + [10.0 * i for i in range(6, 1000)]
    elif name == 'fat':
        c = [0.0] + [0.5 * i for i in range(1, 10)] + [float(i) for i in range(5, 300)]
    else:
        c = [0.0] + [5.0 * i for i in range(1, 29)] + [10.0 * i for i in range(15, 10000)]
    return min(c, key=lambda g: abs(g - v))

NUM = {'calories': ('208', grid_cal), 'fat': ('204', grid_fat), 'sodium': ('307', grid_sodium)}

def decimals_unit(x):
    s = repr(float(x))
    if 'e' in s:
        return 1e-6
    d = len(s.split('.')[1].rstrip('0')) if '.' in s else 0
    return 10 ** (-d)

def main(path, out):
    cls = {k: Counter() for k in NUM}
    unexplained = {k: Counter() for k in NUM}
    per100_decimals = Counter()
    with open(path, encoding='utf-8') as f:
        f.readline()
        for line in f:
            s = line.strip().rstrip(',')
            if not s.startswith('{'):
                continue
            r = json.JSONDecoder().raw_decode(s)[0]
            ln = r.get('labelNutrients') or {}
            ss = r.get('servingSize'); unit = (r.get('servingSizeUnit') or '').lower()
            amounts = {}
            for fn in r.get('foodNutrients') or []:
                num = (fn.get('nutrient') or {}).get('number')
                if fn.get('amount') is not None:
                    amounts[num] = fn['amount']
            for name, (num, grid) in NUM.items():
                x = (ln.get(name) or {}).get('value')
                if x is None:
                    continue
                v = float(x)
                if grid(v):
                    cls[name]['on_grid'] += 1
                    continue
                a = amounts.get(num)
                if a is None or not ss or ss <= 0 or unit not in ('g', 'ml', 'grm', 'mlt'):
                    cls[name]['off_no_per100_or_serving'] += 1
                    continue
                if name == 'calories':
                    per100_decimals[decimals_unit(a)] += 1
                back = a * ss / 100.0
                g = grid_points(name, v)
                half = decimals_unit(a) / 2 + 1e-9
                back_ok = abs(back - v) <= 0.05 + 1e-9 or abs(round(back, 2) - v) <= 0.005 + 1e-9 or abs(round(back, 3) - v) <= 0.0005 + 1e-9
                ghost_ok = abs(g * 100.0 / ss - a) <= half
                if back_ok and ghost_ok:
                    cls[name]['off_explained_round_trip'] += 1
                elif back_ok:
                    cls[name]['off_back_matches_no_grid_point'] += 1
                    unexplained[name][repr(v)] += 1
                else:
                    cls[name]['off_back_differs'] += 1
                    unexplained[name][repr(v)] += 1
    res = {'note': 'exploratory, written after the count; not registered',
           'classes': {k: dict(v) for k, v in cls.items()},
           'unexplained_commonest': {k: v.most_common(20) for k, v in unexplained.items()},
           'calories_per100g_last_decimal_unit': {repr(k): v for k, v in per100_decimals.items()}}
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps(res['classes'], indent=1)); print(res['calories_per100g_last_decimal_unit'])
    for k in NUM: print(k, res['unexplained_commonest'][k][:12])

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
