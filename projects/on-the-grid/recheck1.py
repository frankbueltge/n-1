"""Project 19, session 1: the ten foods check1.py could not ask (429), re-asked once, outside the registration, one call per 8 s."""
import json, time, urllib.request
c = json.load(open('check1.json'))
KEYS = ('calories', 'fat', 'sodium', 'protein')
out = []
for r in c['rows']:
    if r['status'] == 200:
        continue
    url = f"https://api.nal.usda.gov/fdc/v1/food/{r['fdcId']}?api_key=DEMO_KEY"
    row = {'fdcId': r['fdcId'], 'dump': r['dump']}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'n-1 research practice (github.com/frankbueltge/n-1)'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            ln = json.load(resp).get('labelNutrients') or {}
        row['live'] = {k: (ln.get(k) or {}).get('value') for k in KEYS}; row['status'] = 200
        row['agree'] = all((row['dump'][k] is None and row['live'][k] is None) or (row['dump'][k] is not None and row['live'][k] is not None and abs(float(row['dump'][k]) - float(row['live'][k])) < 1e-9) for k in KEYS)
    except Exception as e:
        row['status'] = str(e)[:120]; row['agree'] = None
    out.append(row); print(row); time.sleep(8)
json.dump({'note': 're-asked once by hand, outside the registration; not counted toward P8', 'rows': out}, open('recheck1.json', 'w'), indent=1)
