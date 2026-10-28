"""Project 19, session 2: the live check (SESSION2.md). Twenty LI foods drawn with seed 20261028 (count2.py writes them), asked of
FoodData Central's API with DEMO_KEY, one call per 4 s. Compared with the archive: declared calories, serving size, and the energy
amount per 100 g (nutrient 208). Agreement: all three equal after rounding both sides to one decimal; exact equality reported beside.
Usage: python3 -I check2.py <branded_food_json> <session2.json> <check2.json>
"""
import json, sys, time, urllib.request

def fields(r):
    ln = r.get('labelNutrients') or {}
    e = None
    for fn in r.get('foodNutrients') or []:
        if str((fn.get('nutrient') or {}).get('number')) == '208' and fn.get('amount') is not None:
            e = fn['amount']
    return {'calories': (ln.get('calories') or {}).get('value'), 'servingSize': r.get('servingSize'), 'energy208': e}

def same(a, b, exact):
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) < 1e-9 if exact else round(float(a), 1) == round(float(b), 1)

def main(path, sess, out):
    ids = json.load(open(sess))['check_sample_seed_20261028']
    want = set(ids); dump = {}
    with open(path, encoding='utf-8') as f:
        f.readline()
        for line in f:
            s = line.strip().rstrip(',')
            if not s.startswith('{'):
                continue
            r = json.JSONDecoder().raw_decode(s)[0]
            if r['fdcId'] in want:
                dump[r['fdcId']] = fields(r)
                if len(dump) == len(want):
                    break
    rows = []; agree = 0; exact = 0; answered = 0
    for i in ids:
        url = f'https://api.nal.usda.gov/fdc/v1/food/{i}?api_key=DEMO_KEY'
        row = {'fdcId': i, 'dump': dump.get(i), 'clock_utc': time.strftime('%H:%M:%S', time.gmtime())}
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'n-1 research practice (github.com/frankbueltge/n-1)'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                j = json.load(resp)
            row['live'] = fields(j); row['status'] = 200; answered += 1
            row['agree'] = all(same(row['dump'][k], row['live'][k], False) for k in row['dump'])
            row['exact'] = all(same(row['dump'][k], row['live'][k], True) for k in row['dump'])
            agree += row['agree']; exact += row['exact']
        except Exception as e:
            row['status'] = str(e)[:120]; row['agree'] = None
        rows.append(row); time.sleep(4)
    res = {'drawn': len(ids), 'answered': answered, 'agree': agree, 'exact': exact, 'P8 agree >=19 of 20': agree >= 19, 'rows': rows}
    json.dump(res, open(out, 'w'), indent=1)
    print(answered, agree, exact, res['P8 agree >=19 of 20'])
    for r in rows:
        if not r.get('exact'):
            print(r)

if __name__ == '__main__':
    main(*sys.argv[1:4])
