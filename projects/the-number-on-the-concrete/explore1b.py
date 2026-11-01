"""Project 21, session 1: exploratory, after the count. For which year's field do the runway numbers agree best?
For each year y 1900-2026: share of the analysed set whose number is the nearest ten of theta - D(y). Overall and by country (>= 100).
Also the same for a scrambled null (numbers shuffled within the set) so the curve's peak can be compared with nothing.
Usage: PYTHONPATH=<lib> python3 explore1b.py <scratch_rows.json> <out.json>"""
import json, sys, datetime
import numpy as np, ppigrf
A = json.load(open(sys.argv[1]))['A']
lat = np.array([a['lat'] for a in A]); lon = np.array([a['lon'] for a in A])
th = np.array([a['theta'] for a in A]); n = np.array([a['n'] for a in A])
Y = list(range(1900, 2027))
Be, Bn, _ = ppigrf.igrf(lon, lat, np.zeros_like(lat), [datetime.datetime(y, 1, 1) for y in Y])
D = np.degrees(np.arctan2(Be, Bn))
nn = np.round(((th[None, :] - D) % 360) / 10) % 36
nn[nn == 0] = 36
agree = (nn == n[None, :])
cc = np.array([a['country'] for a in A])
out = {'years': Y, 'agree_all': [round(float(x), 4) for x in agree.mean(1)]}
out['best_year_all'] = Y[int(np.argmax(agree.mean(1)))]
out['agree_at_best'] = float(agree.mean(1).max()); out['agree_2026'] = float(agree[-1].mean())
out['agree_1996'] = float(agree[Y.index(1996)].mean())
out['by_country'] = {}
for k in sorted(set(cc)):
    m = cc == k
    if m.sum() >= 100:
        s = agree[:, m].mean(1)
        out['by_country'][k] = {'n': int(m.sum()), 'best_year': Y[int(np.argmax(s))], 'agree_best': round(float(s.max()), 3),
                                'agree_2026': round(float(s[-1]), 3), 'spread_1900_2026': round(float(s.max() - s.min()), 3)}
        if k in ('US', 'GB', 'DE', 'FR', 'CA', 'AU'):
            out['by_country'][k]['curve'] = [round(float(x), 4) for x in s]
# fast-field runways only (|D2026 - D1996| >= 3 deg): the sharpest dating
dD = np.abs(((D[-1] - D[Y.index(1996)]) + 180) % 360 - 180)
for thr in (3.0, 1.0):
    m = dD >= thr
    s = agree[:, m].mean(1)
    out['fast_ge_%.0fdeg' % thr] = {'n': int(m.sum()), 'best_year': Y[int(np.argmax(s))], 'agree_best': round(float(s.max()), 3),
                                    'agree_2026': round(float(s[-1]), 3), 'agree_1960': round(float(s[Y.index(1960)]), 3)}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('years', 'agree_all')}, indent=1))
print([(y, a) for y, a in zip(Y, out['agree_all'])][::10])
