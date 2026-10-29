"""Project 19, session 3: the record's own fields for the work's panels (SESSION3.md, "the work, if declared"). For the 96 given-back
and 24 unrestorable LI foods count3.py drew (seed 20261029): description, serving size and unit, the household serving text, and for
calories, total fat and sodium the declared value and its restoration (count3.preimage). No brand field is read out.
Usage: python3 -I panels3.py <branded_food_json> <session3.json> <panels3.json>
"""
import json, sys
sys.path.insert(0, '.')
from count3 import preimage, NUM

def main(path, sess, out):
    d = json.load(open(sess))['draws']
    order = [(i, 'given_back') for i in d['panel_given']] + [(i, 'unrestorable') for i in d['panel_unrestorable']]
    want = {i for i, _ in order}; got = {}
    dec = json.JSONDecoder()
    with open(path, encoding='utf-8') as f:
        f.readline()
        for line in f:
            s = line.strip().rstrip(',')
            if not s.startswith('{'):
                continue
            r = dec.raw_decode(s)[0]
            if r['fdcId'] not in want:
                continue
            ln = r.get('labelNutrients') or {}
            ss = r['servingSize']
            amounts = {(fn.get('nutrient') or {}).get('number'): fn['amount'] for fn in r.get('foodNutrients') or [] if fn.get('amount') is not None}
            p = {'fdcId': r['fdcId'], 'description': r.get('description'), 'servingSize': ss, 'unit': r.get('servingSizeUnit'),
                 'household': r.get('householdServingFullText'), 'category': r.get('brandedFoodCategory')}
            for name, (num, _) in NUM.items():
                x = (ln.get(name) or {}).get('value'); a = amounts.get(num)
                if x is None:
                    continue
                pre = preimage(name, a, ss) if a is not None else []
                p[name] = {'v': x, 'a': a, 'r': pre[0] if len(pre) == 1 else None, 'n_pre': len(pre)}
            got[r['fdcId']] = p
            if len(got) == len(want):
                break
    rows = [dict(got[i], fate=k) for i, k in order if i in got]
    json.dump({'seed': 20261029, 'panels': rows}, open(out, 'w'), indent=1)
    print(len(rows), 'panels')

if __name__ == '__main__':
    main(*sys.argv[1:4])
