"""Project 21, session 2: the registered hand check of the join (SESSION2.md). Ten matched pairs, seed 20261102.
Prints OurAirports' row and the FAA's runway-end rows side by side; the verdicts are written by reading them into check2.json.
Usage: python3 check2.py <runways.csv> <faa_dir> <scratch_rows.json>"""
import csv, json, os, random, sys
rw_fn, faa, rows_fn = sys.argv[1:4]
M = json.load(open(rows_fn))['M']
pick = random.Random(20261102).sample(range(len(M)), 10)
oa = {r['id']: r for r in csv.DictReader(open(rw_fn, newline='', encoding='utf-8'))}
ends = {}
for r in csv.DictReader(open(os.path.join(faa, 'APT_RWY_END.csv'), newline='', encoding='latin-1')):
    ends.setdefault((r['SITE_NO'], r['RWY_ID'].strip()), []).append(r)
base = {r['SITE_NO']: r for r in csv.DictReader(open(os.path.join(faa, 'APT_BASE.csv'), newline='', encoding='latin-1'))}
for i in pick:
    m = M[i]; o = oa[m['id']]
    print('OA ', m['id'], o['airport_ident'], o['le_ident'], o['he_ident'], o['le_latitude_deg'], o['le_longitude_deg'],
          'hdgT', o['le_heading_degT'], 'theta', round(m['theta'], 1))
    b = base[m['site']]
    print('FAA', b['ARPT_ID'], b['STATE_CODE'], m['faa_rid'], 'n_faa', m['n_faa'], 'n_oa', m['n'])
    for e in ends.get((m['site'], m['faa_rid']), []):
        print('    end', e['RWY_END_ID'], 'true', e['TRUE_ALIGNMENT'], e['LAT_DECIMAL'], e['LONG_DECIMAL'])
