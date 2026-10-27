"""Project 19, session 1: exploration for the page (not registered). Declared calories counted at every exact value from 0 to 300 kcal
in steps of 0.1, and declared total fat from 0 to 15 g in steps of 0.01; values off those steps are counted apart.
Usage: python3 -I explore1b.py <json> <out.json>"""
import json, sys
from collections import Counter
cal = Counter(); fat = Counter(); cal_other = 0; fat_other = 0
DEC = json.JSONDecoder()
with open(sys.argv[1], encoding='utf-8') as f:
    f.readline()
    for line in f:
        s = line.strip().rstrip(',')
        if not s.startswith('{'):
            continue
        ln = DEC.raw_decode(s)[0].get('labelNutrients') or {}
        c = (ln.get('calories') or {}).get('value')
        if c is not None:
            k = round(float(c) * 10)
            if abs(float(c) * 10 - k) < 1e-6 and 0 <= k <= 3000:
                cal[k] += 1
            else:
                cal_other += 1
        x = (ln.get('fat') or {}).get('value')
        if x is not None:
            k = round(float(x) * 100)
            if abs(float(x) * 100 - k) < 1e-6 and 0 <= k <= 1500:
                fat[k] += 1
            else:
                fat_other += 1
json.dump({'note': 'exploratory, for the page; not registered',
           'calories_by_tenth_kcal_0_300': {str(k): v for k, v in sorted(cal.items())}, 'calories_outside': cal_other,
           'fat_by_hundredth_g_0_15': {str(k): v for k, v in sorted(fat.items())}, 'fat_outside': fat_other},
          open(sys.argv[2], 'w'))
print(cal_other, fat_other, cal.most_common(8), fat.most_common(8))
