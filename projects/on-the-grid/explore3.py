"""Project 19, session 3: exploration, written after the check answered none (not registered). For the foods check3.py asked that Open
Food Facts holds per 100 g or per 100 ml, ask again and compare its per-serving calories (energy-kcal_serving, whatever their basis) with
the number given back (r) and the database's (v); also its per-100 g calories with the database's amount a. Source tags are counted;
Open Food Facts' values are not written out, only outcomes. One call per 1.0 s.
Usage: python3 -I explore3.py <session3.json> <check3.json> <explore3.json>
"""
import json, sys, time
from collections import Counter
sys.path.insert(0, '.')
from check3 import ask

def main(sess, chk, out):
    d = json.load(open(sess))['draws']; rows0 = {r['fdcId']: r for r in json.load(open(chk))['rows']}
    out_rows = []; tags = Counter(); agg = Counter()
    for kind in ('check_given', 'check_kept'):
        for fid, code, v, r in d[kind]:
            if not str(rows0[fid].get('why', '')).startswith('per 100'):
                continue
            st, j = ask(code)
            p = (j or {}).get('product') if isinstance(j, dict) else None
            row = {'kind': kind, 'fdcId': fid, 'code': code, 'status': st}
            if p:
                n = p.get('nutriments') or {}; t = p.get('data_sources_tags') or []
                usda = any('usda' in x for x in t); row['usda'] = usda
                for x in t:
                    tags[x] += 1
                kc = n.get('energy-kcal_serving')
                if isinstance(kc, (int, float)):
                    row['has_serving'] = True
                    row['v_eq'] = abs(kc - v) < 1e-6; row['r_eq'] = abs(kc - r) < 1e-6
                    row['near_v'] = abs(kc - v) < 0.5; row['near_r'] = abs(kc - r) < 0.5
                    key = (kind, 'usda' if usda else 'not usda')
                    agg[key + ('n',)] += 1; agg[key + ('v_eq',)] += row['v_eq']; agg[key + ('r_eq',)] += row['r_eq']
                    agg[key + ('neither',)] += (not row['v_eq'] and not row['r_eq'])
                else:
                    row['has_serving'] = False
            out_rows.append(row); time.sleep(1.0)
    res = {'note': 'exploratory, after the registered check answered none; not registered',
           'agg': {'|'.join(k): v for k, v in sorted(agg.items())}, 'tags': dict(tags.most_common(30)), 'rows': out_rows}
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: res[k] for k in ('agg', 'tags')}, indent=1))

if __name__ == '__main__':
    main(*sys.argv[1:4])
