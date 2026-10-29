"""Project 19, session 3: the check (SESSION3.md). The seeded foods count3.py drew are asked of Open Food Facts, one call per 1.0 s.
Answered = the product exists, nutrition_data_per is 'serving', energy-kcal_serving is a number, and no data_sources tag contains 'usda'.
Compared: r == OFF and v == OFF for given-back foods, v == OFF for kept foods (within 1e-6). Open Food Facts' own values are not written
out (ODbL); only outcomes, the reason a food was not answered, whether OFF's number carries decimals, and its source tags (as counts).
Usage: python3 -I check3.py <session3.json> <check3.json>
"""
import json, sys, time, urllib.request
from collections import Counter

FIELDS = 'code,nutriments,nutrition_data_per,data_sources_tags'
UA = 'n-1 research practice (github.com/frankbueltge/n-1)'

def ask(code):
    url = f'https://world.openfoodfacts.org/api/v2/product/{code}.json?fields={FIELDS}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return 200, json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            try:
                return 404, json.load(e)
            except Exception:
                return 404, {}
        return e.code, None
    except Exception as e:
        return str(e)[:80], None

def main(sess, out):
    d = json.load(open(sess))['draws']
    rows = []; tags = Counter(); reasons = Counter()
    for kind in ('check_given', 'check_kept'):
        for fid, code, v, r in d[kind]:
            st, j = ask(code)
            if j is None:
                time.sleep(5); st, j = ask(code)
            row = {'kind': kind, 'fdcId': fid, 'code': code, 'status': st, 'clock_utc': time.strftime('%H:%M:%S', time.gmtime())}
            p = (j or {}).get('product') if isinstance(j, dict) else None
            if st != 200 or not p:
                row['answered'] = False; row['why'] = 'not found' if st in (200, 404) else 'error %s' % st
            else:
                n = p.get('nutriments') or {}
                kc = n.get('energy-kcal_serving'); t = p.get('data_sources_tags') or []
                if p.get('nutrition_data_per') != 'serving':
                    row['answered'] = False; row['why'] = 'per %s' % p.get('nutrition_data_per')
                elif not isinstance(kc, (int, float)):
                    row['answered'] = False; row['why'] = 'no kcal per serving'
                elif any('usda' in x for x in t):
                    row['answered'] = False; row['why'] = 'usda import'
                else:
                    row['answered'] = True
                    row['off_has_decimals'] = abs(kc - round(kc)) > 1e-6
                    row['v_eq_off'] = abs(v - kc) < 1e-6
                    if kind == 'check_given':
                        row['r_eq_off'] = abs(r - kc) < 1e-6
                    for x in t:
                        tags[x] += 1
            reasons[(kind, row.get('why', 'answered'))] += 1
            rows.append(row); time.sleep(1.0)
    g = [x for x in rows if x['kind'] == 'check_given' and x['answered']]
    k = [x for x in rows if x['kind'] == 'check_kept' and x['answered']]
    rate = lambda a, b: round(a / b, 4) if b else None
    res = {'answered_given': len(g), 'answered_kept': len(k),
           'given_r_eq_off': sum(x['r_eq_off'] for x in g), 'given_v_eq_off': sum(x['v_eq_off'] for x in g),
           'given_neither': sum(not x['r_eq_off'] and not x['v_eq_off'] for x in g),
           'kept_v_eq_off': sum(x['v_eq_off'] for x in k),
           'off_decimals_answered': sum(x['off_has_decimals'] for x in g + k)}
    res['P6 r == OFF >= 70 %'] = [rate(res['given_r_eq_off'], len(g)), len(g) > 0 and res['given_r_eq_off'] / len(g) >= 0.70]
    res['P7 v == OFF <= 10 %'] = [rate(res['given_v_eq_off'], len(g)), len(g) > 0 and res['given_v_eq_off'] / len(g) <= 0.10]
    res['P8 kept v == OFF >= 70 %'] = [rate(res['kept_v_eq_off'], len(k)), len(k) > 0 and res['kept_v_eq_off'] / len(k) >= 0.70]
    res['at least 20 given back answered'] = len(g) >= 20
    res['reasons'] = {'%s|%s' % kk: v for kk, v in reasons.items()}
    res['source_tags_of_answered'] = dict(tags.most_common(25))
    res['rows'] = rows
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({kk: v for kk, v in res.items() if kk != 'rows'}, indent=1))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
