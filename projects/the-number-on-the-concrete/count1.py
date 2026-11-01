"""Project 21, session 1: the registered count (SELECTION.md). Run once, after the selection was pushed.

Usage: PYTHONPATH=<lib with numpy, ppigrf> python3 count1.py <runways.csv> <airports.csv> <out.json> <scratch_rows.json>
The per-runway derived rows go to scratch only; session1.json holds counts and distributions.
"""
import csv, datetime, json, math, re, sys
import numpy as np
import ppigrf

R = 6371.0
YEARS = list(range(1900, 2027))
NUM = re.compile(r'^(0?[1-9]|[12][0-9]|3[0-6])([LCR]?)$')
TRUE = re.compile(r'^(0?[1-9]|[12][0-9]|3[0-6])([LCR]?)T$')


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def bearing(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(x, y)) % 360


def hav(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * R * 1000 * math.asin(math.sqrt(a))


def midpoint(lat1, lon1, lat2, lon2):
    p1, p2, l1 = math.radians(lat1), math.radians(lat2), math.radians(lon1)
    dl = math.radians(lon2 - lon1)
    bx = math.cos(p2) * math.cos(dl)
    by = math.cos(p2) * math.sin(dl)
    pm = math.atan2(math.sin(p1) + math.sin(p2), math.sqrt((math.cos(p1) + bx) ** 2 + by ** 2))
    lm = l1 + math.atan2(by, math.cos(p1) + bx)
    return math.degrees(pm), (math.degrees(lm) + 540) % 360 - 180


def wrap(a):
    return (a + 180) % 360 - 180


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return None
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def main(rw_fn, ap_fn, out_fn, rows_fn):
    country = {}
    with open(ap_fn, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            country[r['id']] = r['iso_country']
    rows = list(csv.DictReader(open(rw_fn, newline='', encoding='utf-8')))
    out = {'rows': len(rows)}
    open_rows = [r for r in rows if r['closed'] != '1']
    out['closed'] = len(rows) - len(open_rows)
    out['open'] = len(open_rows)
    kinds = {'numeric': 0, 'true': 0, 'other': 0}
    A, T = [], []
    pairs = pairs_ok = 0
    drop = {'no_ends': 0, 'short': 0, 'length_mismatch': 0}
    for r in open_rows:
        le = r['le_ident'].strip().upper()
        m, mt = NUM.match(le), TRUE.match(le)
        kinds['numeric' if m else 'true' if mt else 'other'] += 1
        mh = NUM.match(r['he_ident'].strip().upper())
        if m and mh:
            pairs += 1
            n1, n2 = int(m.group(1)), int(mh.group(1))
            if (n1 + 18 - 1) % 36 + 1 == n2:
                pairs_ok += 1
        if not (m or mt):
            continue
        c = [fnum(r[k]) for k in ('le_latitude_deg', 'le_longitude_deg', 'he_latitude_deg', 'he_longitude_deg')]
        if None in c:
            drop['no_ends'] += 1 if m else 0
            continue
        L = hav(*c)
        if L < 900:
            drop['short'] += 1 if m else 0
            continue
        lf = fnum(r['length_ft'])
        if lf and lf > 0 and not (0.5 * lf * 0.3048 <= L <= 1.5 * lf * 0.3048):
            drop['length_mismatch'] += 1 if m else 0
            continue
        mlat, mlon = midpoint(*c)
        th = bearing(mlat, mlon, c[2], c[3])
        rec = {'id': r['id'], 'airport': r['airport_ident'], 'country': country.get(r['airport_ref'], ''),
               'le': le, 'n': int((m or mt).group(1)), 'lat': mlat, 'lon': mlon, 'theta': th, 'L': L,
               'hdg': fnum(r['le_heading_degT']), 'theta_le': bearing(*c)}
        (A if m else T).append(rec)
    out['designators'] = kinds
    out['he_pairs'] = {'pairs': pairs, 'plus18': pairs_ok, 'share': pairs_ok / pairs if pairs else None}
    out['dropped_numeric'] = drop
    out['A'] = len(A)

    lat = np.array([a['lat'] for a in A]); lon = np.array([a['lon'] for a in A])
    dates = [datetime.datetime(y, 1, 1) for y in YEARS]
    Be, Bn, Bu = ppigrf.igrf(lon, lat, np.zeros_like(lat), dates)
    D = np.degrees(np.arctan2(Be, Bn))  # (years, runways)
    th = np.array([a['theta'] for a in A]); n10 = np.array([10.0 * a['n'] for a in A])
    dev = (th[None, :] - D - n10[None, :] + 180) % 360 - 180
    absdev = np.abs(dev)
    now = absdev[-1]
    instep = now <= 5
    right = absdev <= 5
    last = np.full(len(A), -1)
    for i in range(len(A)):
        idx = np.nonzero(right[:, i])[0]
        if len(idx):
            last[i] = YEARS[idx[-1]]
    rate = np.abs(((D[-1] - D[YEARS.index(1996)]) + 180) % 360 - 180) / 30
    out['in_step'] = int(instep.sum()); out['in_step_share'] = float(instep.mean())
    out['median_absdev_2026'] = float(np.median(now))
    out['absdev_2026_quantiles'] = {q: float(np.quantile(now, q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9, 0.99)}
    oos = ~instep
    out['out_of_step'] = int(oos.sum())
    lr = last[oos & (last > 0)]
    out['out_of_step_with_last_right'] = int(len(lr))
    out['median_last_right_year'] = float(np.median(lr)) if len(lr) else None
    out['last_right_by_decade'] = {str(d): int(((lr >= d) & (lr < d + 10)).sum()) for d in range(1900, 2030, 10)}
    out['never_right'] = int((last < 0).sum()); out['never_right_share'] = float((last < 0).mean())
    hi, lo = rate >= 0.2, rate < 0.05
    out['rate_groups'] = {'ge_0.2': {'n': int(hi.sum()), 'oos_share': float(oos[hi].mean()) if hi.sum() else None},
                          'lt_0.05': {'n': int(lo.sum()), 'oos_share': float(oos[lo].mean()) if lo.sum() else None}}
    # signed deviation of out-of-step runways (does the number trail the field in one direction?)
    out['signed_dev_2026_median_all'] = float(np.median(dev[-1]))
    # record's own heading check (P9)
    hd = [abs(wrap(a['hdg'] - a['theta_le'])) for a in A if a['hdg'] is not None]
    out['heading_check'] = {'n': len(hd), 'median_absdiff': median(hd)}
    # true-designated (P7)
    tdev = [abs(wrap(t['theta'] - 10 * t['n'])) for t in T]
    out['true_designated'] = {'n': len(T), 'canada': sum(1 for t in T if t['country'] == 'CA'),
                              'within5': sum(1 for d in tdev if d <= 5), 'median_absdev': median(tdev)}
    # by country, top 15 by count
    cc = {}
    for i, a in enumerate(A):
        cc.setdefault(a['country'], [0, 0])
        cc[a['country']][0] += 1; cc[a['country']][1] += int(oos[i])
    out['by_country_top15'] = {k: {'n': v[0], 'oos': v[1]} for k, v in sorted(cc.items(), key=lambda kv: -kv[1][0])[:15]}
    out['field_model'] = 'IGRF-14 via ppigrf 2.1.0, h=0 km, 1 January of each year'
    json.dump(out, open(out_fn, 'w'), indent=1)
    for i, a in enumerate(A):
        a.update({'D2026': float(D[-1, i]), 'D1960': float(D[YEARS.index(1960), i]), 'dev2026': float(dev[-1, i]),
                  'last_right': int(last[i]), 'rate': float(rate[i])})
    json.dump({'A': A, 'T': T}, open(rows_fn, 'w'))
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:5])
