"""Project 21, session 3: the registered count (SESSION3.md). Run once, after the registration was pushed.

Usage: PYTHONPATH=<lib with numpy, ppigrf> python3 count3.py <runways.csv> <airports.csv> <session3.json> <cells3.json>
       python3 count3.py --synthetic   (checks the agreement rule on hand-made rows; reads no material)
session3.json holds the predictions' numbers; cells3.json holds the page's data: per shown cell (>= 10 runways) its corner, its
runway count and, per year 1900-2030, how many agree. No runway, airport or identifier is written anywhere.
"""
import csv, datetime, json, re, sys
import numpy as np
from count1 import NUM, fnum, hav, midpoint, bearing

YEARS = list(range(1900, 2031))
MIN_CELL = 10


def analysed_set(rw_fn):
    A = []
    for r in csv.DictReader(open(rw_fn, newline='', encoding='utf-8')):
        if r['closed'] == '1':
            continue
        m = NUM.match(r['le_ident'].strip().upper())
        if not m:
            continue
        c = [fnum(r[k]) for k in ('le_latitude_deg', 'le_longitude_deg', 'he_latitude_deg', 'he_longitude_deg')]
        if None in c:
            continue
        L = hav(*c)
        if L < 900:
            continue
        lf = fnum(r['length_ft'])
        if lf and lf > 0 and not (0.5 * lf * 0.3048 <= L <= 1.5 * lf * 0.3048):
            continue
        mlat, mlon = midpoint(*c)
        A.append((mlat, mlon, bearing(mlat, mlon, c[2], c[3]), int(m.group(1))))
    return A


def agree_matrix(theta, n, D):
    """D: (years, runways) declination. True where n is the nearest ten of (theta - D) mod 360 (0 read as 36)."""
    nn = np.round(((theta[None, :] - D) % 360) / 10) % 36
    nn[nn == 0] = 36
    return nn == n[None, :]


def synthetic():
    # a runway with true bearing 096 deg; field 6 deg E -> magnetic 090 -> '09' agrees; field 0 -> 096 -> '10'
    th = np.array([96.0, 96.0, 4.0, 4.0]); n = np.array([9, 10, 36, 1])
    D = np.array([[6.0, 6.0, 4.0, 4.0], [0.0, 0.0, -3.0, -3.0]])
    got = agree_matrix(th, n, D).tolist()
    want = [[True, False, True, False], [False, True, False, True]]
    print('synthetic', got, 'ok' if got == want else 'WRONG')
    return got == want


def best_year(s):
    mx = s.max()
    yrs = [y for y, v in zip(YEARS, s) if v >= mx - 0.02]
    return float(np.median(yrs)), max(yrs) - min(yrs)


def main(rw_fn, ap_fn, out_fn, cells_fn):
    import ppigrf
    A = analysed_set(rw_fn)
    lat = np.array([a[0] for a in A]); lon = np.array([a[1] for a in A])
    th = np.array([a[2] for a in A]); n = np.array([a[3] for a in A])
    Be, Bn, _ = ppigrf.igrf(lon, lat, np.zeros_like(lat), [datetime.datetime(y, 1, 1) for y in YEARS])
    D = np.degrees(np.arctan2(Be, Bn))
    ag = agree_matrix(th, n, D)
    S = ag.mean(1)
    out = {'A': len(A), 'years': [YEARS[0], YEARS[-1]], 'field_model': 'IGRF-14 via ppigrf 2.1.0, h=0 km, 1 January'}
    i26 = YEARS.index(2026)
    upto = S[:i26 + 1]
    out['world_best_year_1900_2026'] = YEARS[int(np.argmax(upto))]
    out['world_share_at_best'] = float(upto.max())
    out['world_share'] = {str(y): round(float(S[YEARS.index(y)]), 4) for y in (1900, 1925, 1950, 1975, 2000, 2002, 2026, 2030)}
    out['world_best_year_1900_2030'] = YEARS[int(np.argmax(S))]
    ci = np.floor(lat / 5).astype(int); cj = np.floor(lon / 5).astype(int)
    cells = {}
    for k in range(len(A)):
        cells.setdefault((int(ci[k]), int(cj[k])), []).append(k)
    shown, dated = [], []
    for (i, j), idx in sorted(cells.items()):
        if len(idx) < MIN_CELL:
            continue
        idx = np.array(idx)
        s = ag[:, idx].mean(1)
        by, span = best_year(s)
        rng = float(s.max() - s.min())
        isd = rng >= 0.20 and span <= 30
        c = {'lat': i * 5, 'lon': j * 5, 'n': int(len(idx)), 'agree': [int(x) for x in ag[:, idx].sum(1)],
             'best': by if isd else None, 'range': round(rng, 3), 'span': int(span)}
        shown.append(c)
        if isd:
            dated.append(by)
    out['cells_total'] = len(cells)
    out['cells_shown'] = len(shown)
    out['runways_in_shown_cells'] = int(sum(c['n'] for c in shown))
    out['cells_dated'] = len(dated)
    out['dated_share'] = len(dated) / len(shown) if shown else None
    d = np.array(dated)
    if len(d):
        out['dated_median_best'] = float(np.median(d))
        out['dated_share_le_2025'] = float((d <= 2025).mean())
        out['dated_share_le_1985'] = float((d <= 1985).mean())
        out['dated_best_quantiles'] = {q: float(np.quantile(d, q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9)}
        out['dated_by_decade'] = {str(y): int(((d >= y) & (d < y + 10)).sum()) for y in range(1900, 2031, 10)}
    p = {}
    p['P1'] = abs(len(A) - 12178) <= 150 and 2000 <= out['world_best_year_1900_2026'] <= 2004 and abs(out['world_share_at_best'] - 0.806) <= 0.015
    p['P2'] = 120 <= len(shown) <= 300
    p['P3'] = out['dated_share'] is not None and out['dated_share'] >= 0.5
    p['P4'] = len(d) > 0 and 1990 <= out['dated_median_best'] <= 2010
    p['P5'] = len(d) > 0 and out['dated_share_le_2025'] >= 0.85
    p['P6'] = len(d) > 0 and out['dated_share_le_1985'] >= 0.10
    p['P7'] = S[YEARS.index(1950)] <= 0.55 and S[YEARS.index(2030)] <= 0.70
    out['predictions'] = {k: bool(v) for k, v in p.items()}
    json.dump(out, open(out_fn, 'w'), indent=1)
    json.dump({'years': [YEARS[0], YEARS[-1]], 'world_n': len(A), 'world_agree': [int(x) for x in ag.sum(1)],
               'cell_deg': 5, 'min_cell': MIN_CELL, 'cells': shown}, open(cells_fn, 'w'), separators=(',', ':'))
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    if sys.argv[1] == '--synthetic':
        sys.exit(0 if synthetic() else 1)
    main(*sys.argv[1:5])
