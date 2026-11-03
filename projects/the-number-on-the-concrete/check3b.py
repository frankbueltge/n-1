"""Project 21, session 3: EXPLORATORY, not registered. The registered field check (check3.py) drew four cells where the field is weak
(|D| <= 1.8 deg). This adds the two shown cells with the largest |D| in 2026, same years and service, to test the field where it is
strong. Usage: PYTHONPATH=<lib> python3 check3b.py <cells3.json> <check3b.json>"""
import datetime, json, sys, time, urllib.request
import numpy as np, ppigrf
cells = json.load(open(sys.argv[1]))['cells']
def dec(lat, lon, y):
    Be, Bn, _ = ppigrf.igrf(lon, lat, 0, datetime.datetime(y, 1, 1)); return float(np.degrees(np.arctan2(Be, Bn)).ravel()[0])
top = sorted(cells, key=lambda c: -abs(dec(c['lat'] + 2.5, c['lon'] + 2.5, 2026)))[:2]
out = []
for c in top:
    lat, lon = c['lat'] + 2.5, c['lon'] + 2.5
    for y in (1925, 1975, 2029):
        u = ('https://geomag.bgs.ac.uk/web_service/GMModels/igrf/14/?latitude=%.2f&longitude=%.2f&altitude=0&date=%d-01-01'
             '&format=json' % (lat, lon, y))
        d = json.load(urllib.request.urlopen(u, timeout=30))['geomagnetic-field-model-result']['field-value']['declination']['value']
        m = dec(lat, lon, y)
        out.append({'cell_lat': lat, 'cell_lon': lon, 'year': y, 'mine': round(m, 3), 'bgs': d, 'diff': round(m - d, 3)})
        time.sleep(3)
res = {'exploratory': True, 'values': out, 'max_absdiff': max(abs(o['diff']) for o in out)}
json.dump(res, open(sys.argv[2], 'w'), indent=1); print(res)
