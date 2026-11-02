"""Project 21, session 2: exploration after the registered count (exploratory, not registered).
Usage: python3 explore2.py <scratch_rows.json> <out.json>"""
import collections, datetime, json, sys
import numpy as np
import ppigrf
M, V, Y = (lambda d: (d['M'], d['V'], d['Y']))(json.load(open(sys.argv[1])))
wrap = lambda a: (a + 180) % 360 - 180
out = {}
# E1: the declared years, exactly
yc = collections.Counter(Y[s] for s in set(m['site'] for m in M) if s in Y)
out['declared_years_after_2026'] = {str(k): v for k, v in sorted(yc.items()) if k > 2026}
out['declared_year_top12'] = {str(k): v for k, v in yc.most_common(12)}
# E2: out-of-step share (FAA numbers, field 2026) by the airport's declared-variation year
bands = [(1960, 1985), (1985, 1986), (1986, 2000), (2000, 2010), (2010, 2020), (2020, 2027), (2027, 2100)]
eb = {}
for lo, hi in bands:
    g = [m for m in M if m['site'] in Y and lo <= Y[m['site']] < hi]
    if g:
        eb[f'{lo}-{hi - 1}'] = {'n': len(g), 'oos_faa_share': round(sum(abs(m['dev_faa']) > 5 for m in g) / len(g), 3),
                               'in_step_vs_declared_share': round(sum(abs(m['dev_decl']) <= 5 for m in g) / len(g), 3)}
out['by_declared_year'] = eb
# E3: runways out of step against their own airport's declared field: which way do they stand?
od = [m for m in M if 'dev_decl' in m and abs(m['dev_decl']) > 5]
out['out_vs_declared'] = {'n': len(od),
    'also_out_vs_2026': sum(abs(m['dev_faa']) > 5 for m in od),
    'trailing_2026_share': None}
# trailing: deviation against 2026 has the sign of the field's move since the declared year
lat = np.array([m['lat'] for m in M]); lon = np.array([m['lon'] for m in M])
years = list(range(1960, 2027))
Be, Bn, Bu = ppigrf.igrf(lon, lat, np.zeros_like(lat), [datetime.datetime(y, 1, 1) for y in years])
D = np.degrees(np.arctan2(Be, Bn))  # (years, runways)
th = np.array([m['theta'] for m in M])
for key, nk in (('faa', 'n_faa'), ('oa', 'n')):
    n10 = np.array([10.0 * m[nk] for m in M])
    dev = (th[None, :] - D - n10[None, :] + 180) % 360 - 180
    share = (np.abs(dev) <= 5).mean(axis=1)
    out[f'best_fit_year_{key}'] = {'year': years[int(np.argmax(share))], 'in_step_share': round(float(share.max()), 4),
                                   'in_step_share_2026': round(float(share[-1]), 4)}
    out[f'fit_curve_{key}'] = {str(y): round(float(s), 4) for y, s in zip(years, share)}
# E4: the field's move since each airport's declared year, against whether its numbers are in step today
idx = {y: i for i, y in enumerate(years)}
rows = []
for j, m in enumerate(M):
    y = Y.get(m['site'])
    if y is None or y < 1960 or y > 2026:
        continue
    mv = wrap(D[-1, j] - D[idx[y], j])
    rows.append((abs(mv), abs(m['dev_faa']) > 5, abs(m['dev_decl']) > 5))
for lo, hi in ((0, 0.5), (0.5, 1.5), (1.5, 3), (3, 99)):
    g = [r for r in rows if lo <= r[0] < hi]
    out.setdefault('by_move_since_declared', {})[f'{lo}-{hi}'] = {'n': len(g),
        'oos_2026_share': round(sum(r[1] for r in g) / len(g), 3) if g else None,
        'oos_vs_declared_share': round(sum(r[2] for r in g) / len(g), 3) if g else None}
tr = [wrap(D[-1, j] - D[idx[Y[m['site']]], j]) * m['dev_decl'] for j, m in enumerate(M)
      if m['site'] in Y and 1960 <= Y[m['site']] <= 2026 and abs(m['dev_decl']) > 5]
out['out_vs_declared']['sign_note'] = 'dev_decl > 0 means the number reads lower than the declared field gives'
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if not k.startswith('fit_curve')}, indent=1))
