"""Project 19, session 2: the registered count (SESSION2.md). Does the serving size alone decide which lawful numbers survive the record?

For every food with a declared calorie value v (labelNutrients), an energy amount a per 100 g (foodNutrients, nutrient 208, kcal) and a
serving size s in g or ml:
  on          v is on the law's grid (count1.py's grid_cal)
  consistent  v equals the record's back-conversion of a: sig3(a * s / 100) == v
  g           the grid number nearest v (v itself if on the grid)
  ghost       g reproduces the stored a: |g * 100 / s - a| <= half a's last decimal unit
  predicted   from g and s only, never v or a: a' = g * 100 / s rounded half up to a whole number, sig3(a' * s / 100) == g
Fat (204) and sodium (307) get on, consistent and ghost. Counts only; FDC IDs only in the check sample and in example lists.
Usage: python3 count2.py <branded_food_json> <out.json>   (imports this repository's own count1.py / explore1.py; reads the archive only as data)
"""
import json, math, random, sys
from collections import Counter, defaultdict
sys.path.insert(0, '.')
from count1 import grid_cal, grid_fat, grid_sodium
from explore1 import grid_points, decimals_unit

DEC = json.JSONDecoder()
UNITS = ('g', 'ml', 'grm', 'mlt')
NUM = {'calories': ('208', grid_cal), 'fat': ('204', grid_fat), 'sodium': ('307', grid_sodium)}

def sig3(x):
    if x == 0:
        return 0.0
    return round(x, 2 - int(math.floor(math.log10(abs(x)))))

def half_up(x):
    return math.floor(x + 0.5)

def predicted_cal(g, s):
    if g == 0:
        return True
    return abs(sig3(half_up(g * 100.0 / s) * s / 100.0) - g) < 1e-9

def main(path, out):
    n = 0
    testable = Counter()                 # per nutrient, by source
    cls = defaultdict(Counter)           # (nutrient, source) -> class counts
    agree = Counter()                    # calories: (source, predicted, on)
    band = defaultdict(lambda: [0, 0])   # calories LI: band -> [n, on]
    by_s = defaultdict(lambda: [0, 0])   # calories LI: serving size -> [n, on]
    cells = defaultdict(lambda: [0, 0])  # calories LI: 'g|s' (s whole, <= 400; g <= 900) -> [n, on]
    examples = defaultdict(list)
    sample_pool = []
    with open(path, encoding='utf-8') as f:
        first = f.readline()
        assert first.startswith('{"BrandedFoods"'), first[:40]
        for line in f:
            s_ = line.strip().rstrip(',')
            if not s_.startswith('{'):
                continue
            r = DEC.raw_decode(s_)[0]
            n += 1
            ln = r.get('labelNutrients') or {}
            ss = r.get('servingSize'); unit = (r.get('servingSizeUnit') or '').lower()
            if not ss or ss <= 0 or unit not in UNITS:
                continue
            src = r.get('dataSource') or 'none'
            src = 'LI' if src == 'LI' else 'other'
            amounts = {(fn.get('nutrient') or {}).get('number'): fn['amount'] for fn in r.get('foodNutrients') or [] if fn.get('amount') is not None}
            for name, (num, grid) in NUM.items():
                x = (ln.get(name) or {}).get('value'); a = amounts.get(num)
                if x is None or a is None:
                    continue
                v = float(x); a = float(a)
                testable[(name, src)] += 1
                on = grid(v)
                consistent = abs(sig3(a * ss / 100.0) - v) < 1e-9
                g = v if on else grid_points(name, v)
                ghost = abs(g * 100.0 / ss - a) <= decimals_unit(a) / 2 + 1e-9
                c = ('on' if on else 'off') + ('_consistent' if consistent else '_not_consistent') + ('_ghost' if ghost else '_no_ghost')
                cls[(name, src)][c] += 1
                if name != 'calories':
                    continue
                p = predicted_cal(g, ss)
                agree[(src, p, on)] += 1
                if src == 'LI':
                    sample_pool.append(r['fdcId'])
                    b = ('g>=100' if g >= 100 else ('10<=g<100' if g >= 10 else 'g<10')) + ('|s<=100' if ss <= 100 else '|s>100')
                    band[b][0] += 1; band[b][1] += on
                    key = repr(float(ss)); by_s[key][0] += 1; by_s[key][1] += on
                    if abs(ss - round(ss)) < 1e-9 and ss <= 400 and g <= 900:
                        cell = cells['%d|%d' % (int(g), int(round(ss)))]; cell[0] += 1; cell[1] += on
                    if on and not consistent and len(examples['LI_on_not_consistent']) < 30:
                        examples['LI_on_not_consistent'].append([r['fdcId'], v, a, ss, unit])
                    if (not on) and p and len(examples['LI_off_but_predicted_on']) < 30:
                        examples['LI_off_but_predicted_on'].append([r['fdcId'], v, a, ss, unit])
                    if on and not p and len(examples['LI_on_but_predicted_off']) < 30:
                        examples['LI_on_but_predicted_off'].append([r['fdcId'], v, a, ss, unit])
    def share(c, keys):
        t = sum(c.values()); return round(sum(c[k] for k in keys) / t, 5) if t else None
    li = cls[('calories', 'LI')]
    li_on = sum(v for k, v in li.items() if k.startswith('on_'))
    li_on_cons = sum(v for k, v in li.items() if k.startswith('on_consistent'))
    li_agree = sum(v for (src, p, on), v in agree.items() if src == 'LI' and p == on)
    li_n = sum(v for (src, p, on), v in agree.items() if src == 'LI')
    d_all = Counter({src: sum(v for k, v in cls[('calories', src)].items() if k == 'off_consistent_no_ghost') for src in ('LI', 'other')})
    def on_cons_share(name):
        c = cls[(name, 'LI')]; o = sum(v for k, v in c.items() if k.startswith('on_'))
        return round(sum(v for k, v in c.items() if k.startswith('on_consistent')) / o, 5) if o else None
    b1 = band['g>=100|s<=100']; b2 = [band['10<=g<100|s<=100'][0] + band['10<=g<100|s>100'][0], band['10<=g<100|s<=100'][1] + band['10<=g<100|s>100'][1]]
    other_share_D = round(d_all['other'] / (d_all['LI'] + d_all['other']), 5) if sum(d_all.values()) else None
    preds = {
        'P1 LI calories: predicted (g, s only) agrees with actual on-grid status >= 97%': li_agree / li_n >= 0.97,
        'P2 LI on-grid calories: consistent with back-conversion >= 95%': li_on_cons / li_on >= 0.95,
        'P3 LI calories g>=100, s<=100: on-grid share >= 97%': b1[1] / b1[0] >= 0.97,
        'P4 LI calories 10<=g<100: on-grid share <= 60%': b2[1] / b2[0] <= 0.60,
        'P5 off-grid, consistent, no ghost (class D): non-LI share >= 25%': other_share_D is not None and other_share_D >= 0.25,
        'P6 LI on-grid fat: consistent >= 95%': (on_cons_share('fat') or 0) >= 0.95,
        'P7 LI on-grid sodium: consistent >= 95%': (on_cons_share('sodium') or 0) >= 0.95,
    }
    rnd = random.Random(20261028)
    sample = rnd.sample(sample_pool, 20)
    res = {
        'source': 'FoodData Central, Branded Foods JSON, release 2026-04-30 (CC0 1.0)',
        'foods': n,
        'testable': {'%s|%s' % k: v for k, v in testable.items()},
        'classes': {'%s|%s' % k: dict(v) for k, v in cls.items()},
        'calories_agreement': {'%s|predicted=%s|on=%s' % k: v for k, v in agree.items()},
        'LI_calories': {'n': li_n, 'agree': li_agree, 'agree_rate': round(li_agree / li_n, 5), 'on': li_on, 'on_consistent': li_on_cons,
                        'on_consistent_rate': round(li_on_cons / li_on, 5)},
        'LI_fat_on_consistent_rate': on_cons_share('fat'), 'LI_sodium_on_consistent_rate': on_cons_share('sodium'),
        'LI_calories_bands': {k: {'n': a, 'on': b, 'rate': round(b / a, 5)} for k, (a, b) in band.items()},
        'class_D_by_source': dict(d_all), 'class_D_other_share': other_share_D,
        'LI_calories_by_serving_top40': sorted(({'s': k, 'n': a, 'on': b, 'rate': round(b / a, 4)} for k, (a, b) in by_s.items()), key=lambda x: -x['n'])[:40],
        'examples': dict(examples),
        'check_sample_seed_20261028': sample,
        'predictions_registered': preds,
    }
    json.dump(res, open(out, 'w'), indent=1, default=bool)
    json.dump({'note': 'LI calories, whole serving sizes <= 400 g/ml, grid number g <= 900: [records, on grid]', 'cells': cells},
              open(out.replace('.json', '_cells.json'), 'w'), separators=(',', ':'))
    print(json.dumps({k: res[k] for k in ('foods', 'LI_calories', 'LI_fat_on_consistent_rate', 'LI_sodium_on_consistent_rate',
                                          'LI_calories_bands', 'class_D_by_source', 'class_D_other_share')}, indent=1))
    print(json.dumps(preds, indent=1, default=bool))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
