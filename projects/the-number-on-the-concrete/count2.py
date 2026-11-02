"""Project 21, session 2: the registered count (SESSION2.md). Run once, after the registration and this script were pushed.

Usage: python3 count2.py <runways.csv> <airports.csv> <faa_dir> <out.json> <scratch_rows.json>
<faa_dir> holds APT_BASE.csv, APT_RWY.csv, APT_RWY_END.csv of the NASR cycle effective 2026-10-29.
Per-runway rows go to scratch only; session2.json holds counts and distributions.
"""
import csv, datetime, json, math, os, re, sys
import numpy as np
import ppigrf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from count1 import NUM, fnum, bearing, hav, midpoint, wrap, median  # session 1's own functions

FAA_RWY = re.compile(r'^(0?[1-9]|[12][0-9]|3[0-6])([LCR]?)/(0?[1-9]|[12][0-9]|3[0-6])([LCR]?)$')


def decl(lats, lons, years):
    """IGRF-14 declination (east +), one value per (lat, lon, year) triple, 1 January of the year."""
    out = np.full(len(lats), np.nan)
    by = {}
    for i, y in enumerate(years):
        by.setdefault(int(y), []).append(i)
    for y, idx in by.items():
        la = np.array([lats[i] for i in idx]); lo = np.array([lons[i] for i in idx])
        Be, Bn, Bu = ppigrf.igrf(lo, la, np.zeros_like(la), datetime.datetime(y, 1, 1))
        out[idx] = np.degrees(np.arctan2(np.ravel(Be), np.ravel(Bn)))
    return out


def a_us(rw_fn, ap_fn):
    """Session 1's analysed set A (SELECTION.md), restricted to iso_country US. Filter logic as in count1.main."""
    aps = {}
    for r in csv.DictReader(open(ap_fn, newline='', encoding='utf-8')):
        aps[r['id']] = r
    A = []
    for r in csv.DictReader(open(rw_fn, newline='', encoding='utf-8')):
        if r['closed'] == '1':
            continue
        le = r['le_ident'].strip().upper(); m = NUM.match(le)
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
        ap = aps.get(r['airport_ref'], {})
        if ap.get('iso_country') != 'US':
            continue
        mlat, mlon = midpoint(*c)
        A.append({'id': r['id'], 'ident': ap.get('ident', ''), 'local_code': ap.get('local_code', ''),
                  'le': le, 'n': int(m.group(1)), 'lat': mlat, 'lon': mlon,
                  'theta': bearing(mlat, mlon, c[2], c[3]), 'theta_le': bearing(*c)})
    return A


def load_faa(d):
    base = {}
    for r in csv.DictReader(open(os.path.join(d, 'APT_BASE.csv'), newline='', encoding='latin-1')):
        base[r['SITE_NO']] = r
    by_id = {}
    for s, r in base.items():
        by_id.setdefault(r['ARPT_ID'].strip(), []).append(s)
    ends = {}
    for r in csv.DictReader(open(os.path.join(d, 'APT_RWY_END.csv'), newline='', encoding='latin-1')):
        ends.setdefault((r['SITE_NO'], r['RWY_ID']), {})[r['RWY_END_ID'].strip()] = r
    rwys, kinds = {}, {'numeric': 0, 'other': 0}
    nrwy = 0
    for r in csv.DictReader(open(os.path.join(d, 'APT_RWY.csv'), newline='', encoding='latin-1')):
        nrwy += 1
        rid = r['RWY_ID'].strip(); m = FAA_RWY.match(rid)
        if not m:
            kinds['other'] += 1
            continue
        kinds['numeric'] += 1
        n1, n2 = int(m.group(1)), int(m.group(3))
        e = ends.get((r['SITE_NO'], r['RWY_ID']), {})
        e1 = e.get(m.group(1) + m.group(2)) or e.get(m.group(1).zfill(2) + m.group(2))
        e2 = e.get(m.group(3) + m.group(4)) or e.get(m.group(3).zfill(2) + m.group(4))
        c = None; ax = None; mid = None
        if e1 and e2:
            c = [fnum(e1['LAT_DECIMAL']), fnum(e1['LONG_DECIMAL']), fnum(e2['LAT_DECIMAL']), fnum(e2['LONG_DECIMAL'])]
            if None not in c and hav(*c) > 50:
                mid = midpoint(*c)
                ax = bearing(mid[0], mid[1], c[2], c[3])  # toward end 2
            else:
                c = None
        if ax is None and e1 and fnum(e1['TRUE_ALIGNMENT']) is not None:
            ax = fnum(e1['TRUE_ALIGNMENT'])  # direction of travel from end 1, i.e. toward end 2
        rwys.setdefault(r['SITE_NO'], []).append({'rid': rid, 'n1': n1, 'n2': n2, 'ax': ax, 'mid': mid})
    return base, by_id, rwys, {'base_rows': len(base), 'rwy_rows': nrwy, 'rwy_kinds': kinds}


def axdiff(a, b):
    """Difference between two axes, modulo 180."""
    d = abs(wrap(a - b)) % 180
    return min(d, 180 - d)


def main(rw_fn, ap_fn, faa_dir, out_fn, rows_fn):
    A = a_us(rw_fn, ap_fn)
    base, by_id, rwys, info = load_faa(faa_dir)
    out = dict(info)
    out['A_US'] = len(A)
    join_how = {'local_code': 0, 'ident': 0, 'K_stripped': 0, 'unjoined': 0}
    unmatched = 0
    M = []
    for a in A:
        site = None
        for how, key in (('local_code', a['local_code']), ('ident', a['ident']),
                         ('K_stripped', a['ident'][1:] if len(a['ident']) == 4 and a['ident'].startswith('K') else '')):
            if key and key.strip() in by_id:
                site = by_id[key.strip()][0]; join_how[how] += 1
                break
        if site is None:
            join_how['unjoined'] += 1
            continue
        cands = [(axdiff(a['theta'], f['ax']), f) for f in rwys.get(site, []) if f['ax'] is not None]
        cands = [cf for cf in cands if cf[0] <= 3]
        if not cands:
            unmatched += 1
            continue
        if len(cands) > 1:
            same = [cf for cf in cands if a['n'] in (cf[1]['n1'], cf[1]['n2'])]
            if len(same) == 1:
                cands = same
            else:
                pool = same or cands
                withmid = [cf for cf in pool if cf[1]['mid']]
                if withmid:
                    cands = sorted(withmid, key=lambda cf: hav(a['lat'], a['lon'], *cf[1]['mid']))
                else:
                    cands = sorted(pool, key=lambda cf: cf[0])
        f = cands[0][1]
        # FAA end whose heading lies within 90 deg of OurAirports' low end's direction
        n_faa = f['n1'] if abs(wrap(f['ax'] - a['theta'])) <= 90 else f['n2']
        M.append({**a, 'site': site, 'faa_rid': f['rid'], 'n_faa': n_faa})
    out['join'] = join_how
    out['joined_unmatched'] = unmatched
    out['matched'] = len(M)
    out['matched_share_of_A_US'] = len(M) / len(A) if A else None

    lat = [m['lat'] for m in M]; lon = [m['lon'] for m in M]
    D26 = decl(lat, lon, [2026] * len(M))
    for i, m in enumerate(M):
        m['D2026'] = float(D26[i])
        m['dev_oa'] = wrap(m['theta'] - D26[i] - 10 * m['n'])
        m['dev_faa'] = wrap(m['theta'] - D26[i] - 10 * m['n_faa'])
        m['agree'] = m['n'] == m['n_faa']
    agree = sum(m['agree'] for m in M)
    out['agree'] = agree; out['agree_share'] = agree / len(M) if M else None
    oos_oa = [m for m in M if abs(m['dev_oa']) > 5]
    out['oos_oa'] = len(oos_oa)
    out['oos_oa_share'] = len(oos_oa) / len(M) if M else None
    out['oos_oa_faa_same'] = sum(m['agree'] for m in oos_oa)
    out['oos_oa_faa_same_share'] = out['oos_oa_faa_same'] / len(oos_oa) if oos_oa else None
    out['oos_oa_faa_differs_and_faa_in_step'] = sum(1 for m in oos_oa if not m['agree'] and abs(m['dev_faa']) <= 5)
    oos_faa = [m for m in M if abs(m['dev_faa']) > 5]
    out['oos_faa'] = len(oos_faa); out['oos_faa_share'] = len(oos_faa) / len(M) if M else None
    dis = [m for m in M if not m['agree']]
    out['disagree_kinds'] = {
        'oa_out_faa_in': sum(1 for m in dis if abs(m['dev_oa']) > 5 and abs(m['dev_faa']) <= 5),
        'oa_in_faa_out': sum(1 for m in dis if abs(m['dev_oa']) <= 5 and abs(m['dev_faa']) > 5),
        'both_in': sum(1 for m in dis if abs(m['dev_oa']) <= 5 and abs(m['dev_faa']) <= 5),
        'both_out': sum(1 for m in dis if abs(m['dev_oa']) > 5 and abs(m['dev_faa']) > 5)}

    # (b) the declared field, each joined airport once
    sites = sorted({m['site'] for m in M})
    out['joined_airports_with_matches'] = len(sites)
    V, Y, la, lo, have = {}, {}, [], [], []
    missing = 0
    for s in sites:
        b = base[s]
        v, h, y = fnum(b['MAG_VARN']), b['MAG_HEMIS'].strip().upper(), fnum(b['MAG_VARN_YEAR'])
        plat, plon = fnum(b['LAT_DECIMAL']), fnum(b['LONG_DECIMAL'])
        if v is None or h not in ('E', 'W') or y is None or plat is None or plon is None:
            missing += 1
            continue
        V[s] = v if h == 'E' else -v; Y[s] = int(y)
        have.append(s); la.append(plat); lo.append(plon)
    out['declared'] = {'with_variation_and_year': len(have), 'missing': missing,
                       'share': len(have) / len(sites) if sites else None}
    ys = [Y[s] for s in have]
    out['declared']['year_median'] = median(ys)
    out['declared']['year_quantiles'] = {q: float(np.quantile(ys, q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9)} if ys else None
    out['declared']['year_by_decade'] = {str(d): sum(1 for y in ys if d <= y < d + 10) for d in range(1900, 2030, 10)}
    out['declared']['year_before_1900'] = sum(1 for y in ys if y < 1900)
    ok = [i for i, s in enumerate(have) if 1900 <= Y[have[i]] <= 2026]
    DY = decl([la[i] for i in ok], [lo[i] for i in ok], [Y[have[i]] for i in ok])
    DN = decl([la[i] for i in ok], [lo[i] for i in ok], [2026] * len(ok))
    err = [V[have[i]] - DY[k] for k, i in enumerate(ok)]
    lag = [wrap(DN[k] - V[have[i]]) for k, i in enumerate(ok)]
    out['declared']['n_year_1900_2026'] = len(ok)
    out['declared']['abs_error_at_year_median'] = median([abs(e) for e in err])
    out['declared']['abs_error_at_year_within_1deg_share'] = sum(1 for e in err if abs(e) <= 1) / len(err) if err else None
    out['declared']['abs_lag_today_median'] = median([abs(x) for x in lag])
    out['declared']['abs_lag_today_quantiles'] = {q: float(np.quantile(np.abs(lag), q)) for q in (0.25, 0.5, 0.75, 0.9)} if lag else None
    # in step against the declared field, per matched runway
    ds = [m for m in M if m['site'] in V]
    for m in ds:
        m['dev_decl'] = wrap(m['theta'] - V[m['site']] - 10 * m['n_faa'])
    instep_decl = sum(1 for m in ds if abs(m['dev_decl']) <= 5)
    out['declared']['runways_with_declared'] = len(ds)
    out['declared']['in_step_against_declared'] = instep_decl
    out['declared']['in_step_against_declared_share'] = instep_decl / len(ds) if ds else None
    out['field_model'] = 'IGRF-14 via ppigrf 2.1.0, h=0 km, 1 January of the year'
    json.dump(out, open(out_fn, 'w'), indent=1, default=float)
    json.dump({'M': M, 'V': V, 'Y': Y}, open(rows_fn, 'w'), default=float)
    print(json.dumps(out, indent=1, default=float))


if __name__ == '__main__':
    main(*sys.argv[1:6])
