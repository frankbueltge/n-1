"""Project 21, session 1: the registered field check (SELECTION.md), with one logged deviation: NOAA NCEI's calculator asks for a key
this practice does not hold, so the British Geological Survey's IGRF-14 web service (no key) is the outside implementation instead.
Ten midpoints drawn with seed 20261101 from the analysed set; declination at 2026-01-01 and 1960-01-01, one request per 3 s,
against this practice's IGRF-14 values (ppigrf). Usage: python3 check1.py <scratch_rows.json> <out.json>"""
import json, random, sys, time, urllib.request
rows = json.load(open(sys.argv[1]))['A']
random.seed(20261101)
pick = random.sample(range(len(rows)), 10)
out = []
for i in pick:
    a = rows[i]
    for y, mine in ((2026, a['D2026']), (1960, a['D1960'])):
        u = ('https://geomag.bgs.ac.uk/web_service/GMModels/igrf/14/?latitude=%.5f&longitude=%.5f&altitude=0&date=%d-01-01'
             '&format=json' % (a['lat'], a['lon'], y))
        r = json.load(urllib.request.urlopen(u, timeout=30))['geomagnetic-field-model-result']
        d = r['field-value']['declination']['value']
        out.append({'airport': a['airport'], 'le': a['le'], 'lat': round(a['lat'], 4), 'lon': round(a['lon'], 4), 'year': y,
                    'mine': round(mine, 3), 'bgs': d, 'diff': round(mine - d, 3)})
        time.sleep(3)
res = {'service': 'https://geomag.bgs.ac.uk/web_service/GMModels/igrf/14/', 'values': out,
       'within_0.2': sum(1 for o in out if abs(o['diff']) <= 0.2), 'n': len(out), 'max_absdiff': max(abs(o['diff']) for o in out)}
json.dump(res, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'values'}), [o['diff'] for o in out])
