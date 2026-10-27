"""Project 19, session 1: count1.py corrected (count1b.py). The registered run skipped the last food, whose line also closes the
array (`}]}`); this copy parses each line with raw_decode, which reads the first object and ignores what follows. Nothing else changed. Registered and corrected outcomes both kept.

Usage: python3 -I count1.py <branded_food_json> <out.json>
Reads FoodData Central's branded-foods JSON (one food per line inside a top-level array) and writes counts only.
"""
import json, math, random, statistics, sys
from collections import Counter, defaultdict

EPS = 1e-9
DEC = json.JSONDecoder()

def is_mult(v, step):
    q = v / step
    return abs(q - round(q)) < EPS

def grid_cal(v):
    return abs(v) < EPS or (v <= 50 + EPS and is_mult(v, 5)) or (v > 50 and is_mult(v, 10))

def grid_fat(v):
    return abs(v) < EPS or (v < 5 - EPS and is_mult(v, 0.5)) or (v >= 5 - EPS and is_mult(v, 1))

def grid_sodium(v):
    return abs(v) < EPS or (5 - EPS <= v <= 140 + EPS and is_mult(v, 5)) or (v > 140 and is_mult(v, 10))

def grid_chol(v):
    return is_mult(v, 5)

def grid_whole(v):
    return is_mult(v, 1)

GRID = {
    'calories': grid_cal, 'fat': grid_fat, 'saturatedFat': grid_fat, 'transFat': grid_fat,
    'sodium': grid_sodium, 'cholesterol': grid_chol,
    'protein': grid_whole, 'carbohydrates': grid_whole, 'fiber': grid_whole, 'sugars': grid_whole,
}

def kind_off(v):
    """How a value is off the grid: 'fraction' if not a multiple of 0.5 (e.g. 9.33), else 'step' (a whole or half number off the step)."""
    return 'step' if is_mult(v, 0.5) else 'fraction'

def main(path, out):
    n = 0; bad_lines = 0
    with_label = 0
    declared = Counter(); on = Counter(); off_kind = defaultdict(Counter)
    off_examples = defaultdict(Counter)  # value -> count, off-grid values per nutrient
    by_source = defaultdict(lambda: [0, 0])  # calories: declared, on grid
    by_cat_off = defaultdict(lambda: [0, 0])  # calories: declared, off grid
    gaps = []; gap_hist = Counter()
    trans_zero = 0
    gtins = Counter()
    cal_ids = []
    with open(path, encoding='utf-8') as f:
        first = f.readline()
        assert first.startswith('{"BrandedFoods"'), first[:40]
        for line in f:
            s = line.strip()
            if s in (']}', ']', ''):
                continue
            if s.endswith(','):
                s = s[:-1]
            try:
                r = DEC.raw_decode(s)[0]
            except Exception:
                bad_lines += 1
                continue
            n += 1
            gtins[r.get('gtinUpc')] += 1
            ln = r.get('labelNutrients') or {}
            if ln:
                with_label += 1
            vals = {}
            for k, fn in GRID.items():
                x = ln.get(k)
                if not isinstance(x, dict) or x.get('value') is None:
                    continue
                try:
                    v = float(x['value'])
                except Exception:
                    continue
                vals[k] = v
                declared[k] += 1
                if fn(v):
                    on[k] += 1
                else:
                    off_kind[k][kind_off(v)] += 1
                    off_examples[k][repr(v)] += 1
            if 'calories' in vals:
                cal_ids.append(r['fdcId'])
                src = r.get('dataSource') or 'none'
                by_source[src][0] += 1
                by_source[src][1] += GRID['calories'](vals['calories'])
                cat = r.get('brandedFoodCategory') or 'none'
                by_cat_off[cat][0] += 1
                by_cat_off[cat][1] += not GRID['calories'](vals['calories'])
            if 'transFat' in vals and abs(vals['transFat']) < EPS:
                trans_zero += 1
            if all(k in vals for k in ('calories', 'protein', 'carbohydrates', 'fat')) and vals['calories'] >= 50:
                d = vals['calories'] - (4 * vals['protein'] + 4 * vals['carbohydrates'] + 9 * vals['fat'])
                gaps.append(d)
                b = max(-200, min(200, int(math.floor(d / 5.0) * 5)))
                gap_hist[b] += 1
    absg = sorted(abs(g) for g in gaps)
    med_abs = statistics.median(absg) if absg else None
    within10pct = None
    rates = {k: on[k] / declared[k] for k in declared}
    dup = sum(1 for g, c in gtins.items() if c > 1)
    rnd = random.Random(20261027)
    sample = rnd.sample(cal_ids, 20) if len(cal_ids) >= 20 else cal_ids
    preds = {
        'P1 >=400000 foods': n >= 400000,
        'P2 >=85% declare calories': declared['calories'] / n >= 0.85,
        'P3 >=90% calories on grid': rates.get('calories', 0) >= 0.90,
        'P4 >=90% total fat on grid': rates.get('fat', 0) >= 0.90,
        'P5 >=90% sodium on grid': rates.get('sodium', 0) >= 0.90,
        'P6 median |d| <=10 kcal': med_abs is not None and med_abs <= 10,
        'P7 >=80% trans fat exactly 0': declared['transFat'] and trans_zero / declared['transFat'] >= 0.80,
    }
    res = {
        'source': 'FoodData Central, Branded Foods JSON, release 2026-04-30 (CC0 1.0)',
        'foods': n, 'unparsed_lines': bad_lines, 'foods_with_labelNutrients': with_label,
        'gtin_distinct': len(gtins), 'gtin_with_more_than_one_record': dup,
        'declared': dict(declared), 'on_grid': dict(on),
        'on_grid_rate': {k: round(v, 5) for k, v in rates.items()},
        'off_grid_kind': {k: dict(v) for k, v in off_kind.items()},
        'off_grid_commonest_values': {k: v.most_common(25) for k, v in off_examples.items()},
        'calories_by_dataSource': {k: {'declared': a, 'on_grid': b, 'rate': round(b / a, 5)} for k, (a, b) in by_source.items()},
        'calories_off_grid_by_category_top': sorted(
            ({'category': c, 'declared': a, 'off_grid': b, 'rate': round(b / a, 4)} for c, (a, b) in by_cat_off.items() if a >= 500),
            key=lambda x: -x['rate'])[:25],
        'trans_fat_declared': declared['transFat'], 'trans_fat_zero': trans_zero,
        'atwater': {
            'n': len(gaps), 'median_abs_d': med_abs,
            'median_d': statistics.median(gaps) if gaps else None,
            'share_abs_d_le_5': round(sum(1 for g in absg if g <= 5) / len(absg), 5) if absg else None,
            'share_abs_d_le_10': round(sum(1 for g in absg if g <= 10) / len(absg), 5) if absg else None,
            'share_d_eq_0': round(sum(1 for g in gaps if abs(g) < EPS) / len(gaps), 5) if gaps else None,
            'hist_5kcal_clipped_200': sorted(gap_hist.items()),
        },
        'check_sample_seed_20261027': sample,
        'predictions_registered': preds,
    }
    json.dump(res, open(out, 'w'), indent=1, default=lambda o: bool(o))
    print(json.dumps({k: res[k] for k in ('foods', 'foods_with_labelNutrients', 'on_grid_rate', 'off_grid_kind', 'atwater')}, indent=1)[:3000])
    print(json.dumps(preds, indent=1, default=bool))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
