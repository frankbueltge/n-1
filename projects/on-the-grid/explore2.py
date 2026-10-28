"""Project 19, session 2: exploration, written after the count (not registered).
(i) Re-run count2.py's tests with the back-conversion in decimal arithmetic, rounding half to even (and half up, beside), instead of
binary floating point: which rounding does the record use? The registered P1-P4, P6, P7 are recomputed under it, marked as a correction
of the definition. (ii) Describe class D (off the grid, consistent, no lawful number behind it): market country, data source, whether v
is a whole number, update year, top categories; and the same for the rest.
Usage: python3 explore2.py <branded_food_json> <out.json>
"""
import json, sys
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
sys.path.insert(0, '.')
from count1 import grid_cal, grid_fat, grid_sodium
from explore1 import grid_points, decimals_unit

DEC = json.JSONDecoder()
UNITS = ('g', 'ml', 'grm', 'mlt')
NUM = {'calories': ('208', grid_cal), 'fat': ('204', grid_fat), 'sodium': ('307', grid_sodium)}

def dsig3(x, mode):
    x = D(x)
    if x == 0:
        return Decimal(0)
    e = x.adjusted()  # exponent of the leading digit
    return x.quantize(Decimal(1).scaleb(e - 2), rounding=mode)

def D(x):
    return x if isinstance(x, Decimal) else Decimal(repr(float(x)))

def back(a, s, mode):
    return dsig3(D(a) * D(s) / Decimal(100), mode)

def predicted(g, s, mode):
    if g == 0:
        return True
    a1 = (D(g) * 100 / D(s)).quantize(Decimal(1), rounding=mode)
    return back(a1, s, mode) == D(g)

def year(d):
    try:
        return d.split('/')[-1]
    except Exception:
        return 'none'

def main(path, out):
    modes = {'half_even': ROUND_HALF_EVEN, 'half_up': ROUND_HALF_UP}
    cons = defaultdict(Counter)        # (nutrient, src, mode) -> on/off x consistent
    agree = defaultdict(Counter)       # (src, mode) -> agree / n
    band = defaultdict(lambda: [0, 0, 0])  # LI calories, half_even: band -> [n, on, on or class D]
    desc = defaultdict(lambda: defaultdict(Counter))  # group -> field -> value
    with open(path, encoding='utf-8') as f:
        f.readline()
        for line in f:
            s_ = line.strip().rstrip(',')
            if not s_.startswith('{'):
                continue
            r = DEC.raw_decode(s_)[0]
            ln = r.get('labelNutrients') or {}
            ss = r.get('servingSize'); unit = (r.get('servingSizeUnit') or '').lower()
            if not ss or ss <= 0 or unit not in UNITS:
                continue
            src = 'LI' if r.get('dataSource') == 'LI' else 'other'
            amounts = {(fn.get('nutrient') or {}).get('number'): fn['amount'] for fn in r.get('foodNutrients') or [] if fn.get('amount') is not None}
            for name, (num, grid) in NUM.items():
                x = (ln.get(name) or {}).get('value'); a = amounts.get(num)
                if x is None or a is None:
                    continue
                v = float(x); a = float(a); on = grid(v)
                g = v if on else grid_points(name, v)
                ghost = abs(g * 100.0 / ss - a) <= decimals_unit(a) / 2 + 1e-9
                c_by = {}
                for mn, m in modes.items():
                    c = back(a, ss, m) == D(v)
                    c_by[mn] = c
                    cons[(name, src, mn)][('on' if on else 'off') + ('_consistent' if c else '_not_consistent')] += 1
                if name != 'calories':
                    continue
                for mn, m in modes.items():
                    p = predicted(g, ss, m)
                    agree[(src, mn)]['n'] += 1; agree[(src, mn)]['agree'] += (p == on)
                he = c_by['half_even']
                grp = 'on' if on else ('D' if (he and not ghost) else ('C' if he else 'E'))
                if src == 'LI':
                    b = ('g>=100' if g >= 100 else ('10<=g<100' if g >= 10 else 'g<10')) + ('|s<=100' if ss <= 100 else '|s>100')
                    band[b][0] += 1; band[b][1] += on; band[b][2] += on or grp == 'D'
                dd = desc[grp]
                dd['source'][r.get('dataSource') or 'none'] += 1
                dd['marketCountry'][r.get('marketCountry') or 'none'] += 1
                dd['v_whole'][str(abs(v - round(v)) < 1e-9)] += 1
                dd['modified_year'][year(r.get('modifiedDate') or 'none')] += 1
                dd['category'][r.get('brandedFoodCategory') or 'none'] += 1
                dd['s_eq_100'][str(abs(ss - 100) < 1e-9)] += 1
    res = {'note': 'exploratory, written after the count; not registered',
           'consistency': {'%s|%s|%s' % k: dict(v) for k, v in cons.items()},
           'calories_predicted_agree': {'%s|%s' % k: {'n': v['n'], 'agree': v['agree'], 'rate': round(v['agree'] / v['n'], 5)} for k, v in agree.items()},
           'LI_calories_bands_half_even': {k: {'n': a, 'on': b, 'on_or_D': c, 'rate_on': round(b / a, 5), 'rate_on_or_D': round(c / a, 5)} for k, (a, b, c) in band.items()},
           'groups': {g: {f: (dict(c.most_common(12)) if f != 'modified_year' else dict(sorted(c.items()))) for f, c in d.items()} for g, d in desc.items()}}
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: res[k] for k in ('calories_predicted_agree', 'LI_calories_bands_half_even')}, indent=1))
    for k, v in sorted(res['consistency'].items()):
        print(k, v)
    for g, d in res['groups'].items():
        print(g, {f: list(c.items())[:6] for f, c in d.items() if f != 'category'})

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
