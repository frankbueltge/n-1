"""Project 19, session 1: the live check (SELECTION.md). Twenty foods drawn with seed 20261027 (count1.py writes them),
asked of FoodData Central's API with DEMO_KEY, one call per 2 s; calories, fat, sodium, protein compared with the archive.

Usage: python3 -I check1.py <branded_food_json> <session1.json> <check1.json>
"""
import json, sys, time, urllib.request

KEYS = ('calories', 'fat', 'sodium', 'protein')

def main(path, sess, out):
    ids = json.load(open(sess))['check_sample_seed_20261027']
    want = set(ids); dump = {}
    with open(path, encoding='utf-8') as f:
        f.readline()
        for line in f:
            s = line.strip().rstrip(',')
            if not s.startswith('{'):
                continue
            # cheap prefilter on the id
            r = json.JSONDecoder().raw_decode(s)[0]
            if r['fdcId'] in want:
                ln = r.get('labelNutrients') or {}
                dump[r['fdcId']] = {k: (ln.get(k) or {}).get('value') for k in KEYS}
                if len(dump) == len(want):
                    break
    rows = []; agree = 0; answered = 0
    for i in ids:
        url = f'https://api.nal.usda.gov/fdc/v1/food/{i}?api_key=DEMO_KEY'
        row = {'fdcId': i, 'dump': dump.get(i)}
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'n-1 research practice (github.com/frankbueltge/n-1)'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                j = json.load(resp)
            ln = j.get('labelNutrients') or {}
            row['live'] = {k: (ln.get(k) or {}).get('value') for k in KEYS}
            row['status'] = 200
            answered += 1
            same = all(
                (row['dump'][k] is None and row['live'][k] is None) or
                (row['dump'][k] is not None and row['live'][k] is not None and abs(float(row['dump'][k]) - float(row['live'][k])) < 1e-9)
                for k in KEYS)
            row['agree'] = same; agree += same
        except Exception as e:
            row['status'] = str(e)[:120]; row['agree'] = None
        rows.append(row); time.sleep(2)
    res = {'drawn': len(ids), 'answered': answered, 'agree': agree, 'P8 agree >=19 of 20': agree >= 19, 'rows': rows}
    json.dump(res, open(out, 'w'), indent=1)
    print(answered, agree, res['P8 agree >=19 of 20'])
    for r in rows:
        if not r['agree']:
            print(r)

if __name__ == '__main__':
    main(*sys.argv[1:4])
