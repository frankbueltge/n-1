"""Project 21, session 3: the registered field check (SESSION3.md, P8). Four shown cells drawn with seed 20261103 from cells3.json;
declination at each cell's centre (corner + 2.5 deg) for 1925, 1975 and 2029, this practice's IGRF-14 (ppigrf 2.1.0) against the
British Geological Survey's IGRF-14 web service (no key), one request every 3 s. Pass: all twelve within 0.05 deg.
Usage: PYTHONPATH=<lib> python3 check3.py <cells3.json> <check3.json>"""
import datetime, json, random, sys, time, urllib.request
import numpy as np, ppigrf
cells = json.load(open(sys.argv[1]))['cells']
random.seed(20261103)
pick = random.sample(range(len(cells)), 4)
out = []
for i in pick:
    lat, lon = cells[i]['lat'] + 2.5, cells[i]['lon'] + 2.5
    for y in (1925, 1975, 2029):
        Be, Bn, _ = ppigrf.igrf(lon, lat, 0, datetime.datetime(y, 1, 1))
        mine = float(np.degrees(np.arctan2(Be, Bn)).ravel()[0])
        u = ('https://geomag.bgs.ac.uk/web_service/GMModels/igrf/14/?latitude=%.2f&longitude=%.2f&altitude=0&date=%d-01-01'
             '&format=json' % (lat, lon, y))
        r = json.load(urllib.request.urlopen(u, timeout=30))['geomagnetic-field-model-result']
        d = r['field-value']['declination']['value']
        out.append({'cell_lat': lat, 'cell_lon': lon, 'year': y, 'mine': round(mine, 3), 'bgs': d, 'diff': round(mine - d, 3)})
        time.sleep(3)
res = {'service': 'https://geomag.bgs.ac.uk/web_service/GMModels/igrf/14/', 'values': out, 'n': len(out),
       'within_0.05': sum(1 for o in out if abs(o['diff']) <= 0.05), 'max_absdiff': max(abs(o['diff']) for o in out)}
res['P8'] = res['within_0.05'] == res['n']
json.dump(res, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'values'}), [(o['year'], o['mine'], o['bgs']) for o in out])
