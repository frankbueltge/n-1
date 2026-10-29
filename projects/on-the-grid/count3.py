"""Project 19, session 3: the registered count (SESSION3.md). Can the number printed on each label be given back from the record?

For every testable food (declared calorie value v, energy amount a per 100 g (nutrient 208), serving size s > 0 in g or ml):
  P(a, s)       every lawful grid number g with |g * 100 / s - a| <= half a's last decimal unit, in decimal arithmetic
  restored      P has one member r; ambiguous: two or more; unrestorable: none
  kept          restored and r == v; given back: restored and r != v
Fat (204) and sodium (307) the same with their grids. Counts, and the seeded draws for the check and the work (FDC IDs, codes, and for the
work's panels the record's own fields: description, serving, the three numbers and their restorations).
Usage: python3 -I count3.py <branded_food_json> <out.json>   (imports this repository's count1.py / explore1.py; reads the archive as data)
"""
import bisect, json, random, sys
from collections import Counter, defaultdict
from decimal import Decimal
sys.path.insert(0, '.')
from count1 import grid_cal, grid_fat, grid_sodium
from explore1 import decimals_unit

DEC = json.JSONDecoder()
UNITS = ('g', 'ml', 'grm', 'mlt')
GRIDS = {
    'calories': [0.0] + [5.0 * i for i in range(1, 11)] + [10.0 * i for i in range(6, 1000)],
    'fat': [0.0] + [0.5 * i for i in range(1, 10)] + [float(i) for i in range(5, 300)],
    'sodium': [0.0] + [5.0 * i for i in range(1, 29)] + [10.0 * i for i in range(15, 10000)],
}
NUM = {'calories': ('208', grid_cal), 'fat': ('204', grid_fat), 'sodium': ('307', grid_sodium)}
SEED = 20261029

def D(x):
    return Decimal(repr(float(x)))

def preimage(name, a, s):
    a_ = D(a); s_ = D(s); h = D(decimals_unit(a)) / 2
    lo = (a_ - h) * s_ / 100; hi = (a_ + h) * s_ / 100
    grid = GRIDS[name]
    i = bisect.bisect_left(grid, float(lo) - 1e-6)
    out = []
    while i < len(grid) and grid[i] <= float(hi) + 1e-6:
        g = grid[i]
        if abs(D(g) * 100 / s_ - a_) <= h:
            out.append(g)
        i += 1
    return out

def code13(gtin):
    t = (gtin or '').strip()
    if not t.isdigit() or not (8 <= len(t) <= 14):
        return None
    t = t.lstrip('0') or '0'
    return t.zfill(8) if len(t) <= 8 else t.zfill(13)

def main(path, out):
    n = 0
    fate = defaultdict(Counter)           # (nutrient, src) -> testable / restored / kept / given_back / ambiguous / unrestorable
    on_restored = Counter()               # LI calories with v on the grid and restored: n, r == v
    given_by_size = Counter()             # LI calories given back: how far r is from v (rounded to 0.1)
    unrestorable_whole = Counter()        # LI calories unrestorable: v whole or not
    pools = {'check_given': [], 'check_kept': [], 'panel_given': [], 'panel_unrestorable': []}
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
            src = 'LI' if r.get('dataSource') == 'LI' else 'other'
            amounts = {(fn.get('nutrient') or {}).get('number'): fn['amount'] for fn in r.get('foodNutrients') or [] if fn.get('amount') is not None}
            res = {}
            for name, (num, grid) in NUM.items():
                x = (ln.get(name) or {}).get('value'); a = amounts.get(num)
                if x is None or a is None:
                    continue
                v = float(x); a = float(a)
                p = preimage(name, a, ss)
                k = fate[(name, src)]
                k['testable'] += 1
                if len(p) == 1:
                    k['restored'] += 1
                    if abs(p[0] - v) < 1e-9:
                        k['kept'] += 1; st = 'kept'
                    else:
                        k['given_back'] += 1; st = 'given_back'
                elif p:
                    k['ambiguous'] += 1; st = 'ambiguous'
                else:
                    k['unrestorable'] += 1; st = 'unrestorable'
                res[name] = {'v': v, 'r': p[0] if len(p) == 1 else None, 'state': st}
                if name == 'calories' and src == 'LI':
                    if grid(v) and len(p) == 1:
                        on_restored['n'] += 1; on_restored['r_eq_v'] += abs(p[0] - v) < 1e-9
                    if st == 'given_back':
                        given_by_size[str(round(abs(p[0] - v), 1))] += 1
                    if st == 'unrestorable':
                        unrestorable_whole[str(abs(v - round(v)) < 1e-9)] += 1
            c = res.get('calories')
            if src != 'LI' or not c:
                continue
            fid = r['fdcId']
            code = code13(r.get('gtinUpc'))
            if c['state'] == 'given_back':
                pools['panel_given'].append(fid)
                if code:
                    pools['check_given'].append([fid, code, c['v'], c['r']])
            elif c['state'] == 'kept' and code:
                pools['check_kept'].append([fid, code, c['v'], c['r']])
            elif c['state'] == 'unrestorable':
                pools['panel_unrestorable'].append(fid)
    rng = random.Random(SEED)
    draws = {
        'check_given': rng.sample(pools['check_given'], 300),
        'check_kept': rng.sample(pools['check_kept'], 100),
        'panel_given': rng.sample(pools['panel_given'], 96),
        'panel_unrestorable': rng.sample(pools['panel_unrestorable'], 24),
    }
    li = fate[('calories', 'LI')]
    rate = lambda a, b: round(a / b, 5) if b else None
    preds = {
        'P1 restored >= 93 %': [rate(li['restored'], li['testable']), rate(li['restored'], li['testable']) >= 0.93],
        'P2 ambiguous <= 0.5 %': [rate(li['ambiguous'], li['testable']), rate(li['ambiguous'], li['testable']) <= 0.005],
        'P3 given back >= 20 % of restored': [rate(li['given_back'], li['restored']), rate(li['given_back'], li['restored']) >= 0.20],
        'P4 r == v for >= 99 % of restored on-grid': [rate(on_restored['r_eq_v'], on_restored['n']), rate(on_restored['r_eq_v'], on_restored['n']) >= 0.99],
        'P5 sodium restored >= 90 %': [rate(fate[('sodium', 'LI')]['restored'], fate[('sodium', 'LI')]['testable']),
                                       rate(fate[('sodium', 'LI')]['restored'], fate[('sodium', 'LI')]['testable']) >= 0.90],
    }
    out_ = {'foods': n, 'seed': SEED,
            'fate': {'%s|%s' % k: dict(v) for k, v in fate.items()},
            'LI_calories_on_grid_restored': dict(on_restored),
            'LI_calories_given_back_distance': dict(sorted(given_by_size.items(), key=lambda t: -t[1])[:20]),
            'LI_calories_unrestorable_v_whole': dict(unrestorable_whole),
            'pool_sizes': {k: len(v) for k, v in pools.items()},
            'predictions_P1_P5': preds,
            'draws': draws}
    json.dump(out_, open(out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in out_.items() if k != 'draws'}, indent=1))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
