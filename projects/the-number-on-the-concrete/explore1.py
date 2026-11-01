"""Project 21, session 1: exploratory, after the registered count. Does an out-of-step number trail the field's motion?
Usage: PYTHONPATH=<lib> python3 explore1.py <scratch_rows.json> <out.json>"""
import json, sys, datetime
import numpy as np, ppigrf
d = json.load(open(sys.argv[1])); A = d['A']
lat = np.array([a['lat'] for a in A]); lon = np.array([a['lon'] for a in A])
Y = [1976, 1996, 2016, 2026]
Be, Bn, _ = ppigrf.igrf(lon, lat, np.zeros_like(lat), [datetime.datetime(y, 1, 1) for y in Y])
D = np.degrees(np.arctan2(Be, Bn))
dev = np.array([a['dev2026'] for a in A]); last = np.array([a['last_right'] for a in A])
dD = ((D[3] - D[1]) + 180) % 360 - 180          # field's change 1996-2026
oos = np.abs(dev) > 5
# trailing: the magnetic heading moved by -dD; a number left behind shows dev with the sign of -dD
trail = np.sign(dev) == -np.sign(dD)
out = {}
for name, m in (('all', np.ones(len(A), bool)), ('in_step', ~oos), ('out_of_step', oos),
                ('oos_and_drift_ge_1.5deg', oos & (np.abs(dD) >= 1.5)), ('oos_and_drift_lt_0.5deg', oos & (np.abs(dD) < 0.5))):
    out['trailing_share_' + name] = {'n': int(m.sum()), 'trailing': float(trail[m].mean()) if m.sum() else None}
# a null: if numbers were right at a single past epoch E, what share would be out of step today? E = 1996, 2016
for i, y in ((1, 1996), (2, 2016)):
    th = np.array([a['theta'] for a in A])
    mag = (th - D[i]) % 360
    nn = np.round(mag / 10) % 36
    nn[nn == 0] = 36
    dv = ((th - D[3] - 10 * nn) + 180) % 360 - 180
    out['if_all_painted_right_in_%d_oos_share_today' % y] = float((np.abs(dv) > 5).mean())
# never-right: what their deviation looks like
nr = last < 0
out['never_right_absdev_hist'] = {f'{lo}-{lo+5}': int(((np.abs(dev[nr]) >= lo) & (np.abs(dev[nr]) < lo + 5)).sum()) for lo in range(0, 185, 5) if ((np.abs(dev[nr]) >= lo) & (np.abs(dev[nr]) < lo + 5)).sum()}
suf = np.array([a['le'][-1] in 'LCR' for a in A])
out['never_right_with_LCR_suffix'] = int((nr & suf).sum()); out['A_with_LCR_suffix_share'] = float(suf.mean())
out['oos_share_LCR'] = float(oos[suf].mean()); out['oos_share_single'] = float(oos[~suf].mean())
# last right year by country (countries with >= 100 in A)
cc = {}
for a, o in zip(A, oos):
    cc.setdefault(a['country'], []).append(a['last_right'] if o else None)
out['by_country'] = {}
for k, v in cc.items():
    if len(v) >= 100:
        lr = [x for x in v if x is not None and x > 0]
        out['by_country'][k] = {'n': len(v), 'oos_share': round(sum(x is not None for x in v) / len(v), 3),
                                'median_last_right': float(np.median(lr)) if lr else None}
# the oldest numbers: out-of-step with last right year <= 1960, in fast and slow places
old = oos & (last > 0) & (last <= 1960)
out['last_right_le_1960'] = {'n': int(old.sum()), 'median_absdev': float(np.median(np.abs(dev[old]))) if old.sum() else None,
                             'median_drift_since_1996': float(np.median(np.abs(dD[old]))) if old.sum() else None}
# examples for a page: out-of-step runways with the largest |drift| and an exact trailing shift (<= 300 committed)
ix = [i for i in np.argsort(-np.abs(dD)) if oos[i] and trail[i]][:12]
out['examples_fast_trailing'] = [{'airport': A[i]['airport'], 'le': A[i]['le'], 'country': A[i]['country'],
                                  'theta': round(A[i]['theta'], 1), 'D2026': round(A[i]['D2026'], 1),
                                  'dev2026': round(float(dev[i]), 1), 'last_right': int(last[i])} for i in ix]
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps(out, indent=1))
