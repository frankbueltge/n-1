"""Project 20, session 2: the registered count (SESSION2.md). Ring positions between the keys on a circle of 100 cents (A = 440),
their concentration by tuning era and by foundry, the retuning gap, and the inside check against towers.csv's Hz.
Usage: count2.py bells.csv towers.csv founders.csv out.json"""
import csv, json, math, re, cmath, sys, collections as C

bells = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
towers = list(csv.DictReader(open(sys.argv[2], encoding='utf-8-sig')))
founders = list(csv.DictReader(open(sys.argv[3], encoding='utf-8-sig')))

def num(s):
    try:
        v = float(s); return v if v > 0 else None
    except (ValueError, TypeError):
        return None
def year(s):
    m = re.search(r'(\d{4})', s or ''); return int(m.group(1)) if m else None
def pos(f):
    return ((1200 * math.log2(f / 440) + 50) % 100) - 50
def circ(os):
    n = len(os)
    if n == 0:
        return {'n': 0}
    z = sum(cmath.exp(2j * math.pi * o / 100) for o in os) / n
    R = abs(z); mu = cmath.phase(z) * 100 / (2 * math.pi)
    p = math.exp(math.sqrt(1 + 4 * n + 4 * (n * n - (n * R) ** 2)) - (1 + 2 * n))
    return {'n': n, 'mean_cents': mu, 'R': R, 'rayleigh_p': min(p, 1.0)}
def wrapdiff(a, b):
    return ((a - b + 50) % 100) - 50

tower_by_ring = {}
for t in towers:
    tower_by_ring.setdefault(t['RingID'], t)
group = {}
for f in founders:
    group[f['Name']] = f['Group'] or f['Name']

rings = C.defaultdict(list)
for b in bells:
    if b['Collection Type'] == 'full-circle ring':
        rings[b['Ring ID']].append(b)

R = []
for rid, bs in rings.items():
    size = bs[0]['Ring Size'].split()[0] if bs[0]['Ring Size'] else ''
    ten = [x for x in bs if x['Bell Role'] == size]
    if len(ten) != 1:
        continue
    t = ten[0]; f = num(t['Nominal (Hz)'])
    if not f:
        continue
    tw = tower_by_ring.get(rid)
    tune = year(tw['TuneYr']) if tw else None
    cast = year(t['Cast Date'])
    unc = (t.get('Founder Uncertain') or '').strip()
    fd = None
    if t['Founder'] and not unc:
        fd = group.get(t['Founder'])
    R.append({'ring': rid, 'f': f, 'o': pos(f), 'tune': tune, 'cast': cast, 'year': tune or cast,
              'foundry': fd, 'founder_named': bool(t['Founder']), 'uncertain': bool(unc),
              'tower_hz': num(tw['Hz']) if tw else None, 'country': tw['Country'] if tw else None})

out = {'rings': len(R), 'rings_with_tuneyr': sum(1 for r in R if r['tune']),
       'rings_year_from_cast_only': sum(1 for r in R if not r['tune'] and r['cast']),
       'rings_no_year': sum(1 for r in R if not r['year'])}
out['all'] = circ([r['o'] for r in R])
out['hist_5c'] = dict(sorted(C.Counter(int(math.floor(r['o'] / 5)) * 5 for r in R).items()))
eras = [('before 1800', None, 1799), ('1800-1849', 1800, 1849), ('1850-1899', 1850, 1899), ('1900-1949', 1900, 1949),
        ('1950 and later', 1950, None)]
def inera(y, lo, hi):
    return y is not None and (lo is None or y >= lo) and (hi is None or y <= hi)
out['by_era'] = {k: circ([r['o'] for r in R if inera(r['year'], lo, hi)]) for k, lo, hi in eras}
out['by_era_tuneyr_only'] = {k: circ([r['o'] for r in R if inera(r['tune'], lo, hi)]) for k, lo, hi in eras}
out['by_era_hist_10c'] = {k: dict(sorted(C.Counter(int(math.floor(r['o'] / 10)) * 10 for r in R if inera(r['year'], lo, hi)).items()))
                          for k, lo, hi in eras}

out['foundry_join'] = {'tenor_founder_named': sum(1 for r in R if r['founder_named']),
                       'uncertain': sum(1 for r in R if r['uncertain']),
                       'joined': sum(1 for r in R if r['foundry']),
                       'named_not_found': sum(1 for r in R if r['founder_named'] and not r['uncertain'] and not r['foundry'])}
fy = C.defaultdict(list)
for r in R:
    if r['foundry'] and inera(r['year'], 1880, 1949):
        fy[r['foundry']].append(r['o'])
out['foundries_1880_1949'] = {k: circ(v) for k, v in sorted(fy.items(), key=lambda kv: -len(kv[1])) if len(v) >= 30}

big = out['foundries_1880_1949']
P = {}
a = out['all']; P['P1'] = a['rayleigh_p'] < 0.001 and a['R'] <= 0.25
e = out['by_era']['1950 and later']; P['P2'] = e['R'] >= 0.5 and abs(e['mean_cents']) <= 10
e = out['by_era']['1850-1899']; P['P3'] = e['R'] >= 0.2 and abs(wrapdiff(e['mean_cents'], 48.1)) <= 12
P['P4'] = out['by_era']['before 1800']['R'] <= 0.10
P['P5'] = (sum(1 for v in big.values() if v['rayleigh_p'] < 0.01) >= 2 * len(big) / 3) if big else None
if 'Loughborough' in big and 'Gillett' in big:
    P['P6'] = abs(wrapdiff(big['Loughborough']['mean_cents'], big['Gillett']['mean_cents'])) > 10
else:
    P['P6'] = 'not testable'
tu = [r for r in R if r['tune']]
gap = [r for r in tu if r['cast'] and r['tune'] - r['cast'] >= 50]
out['retune'] = {'with_tuneyr': len(tu), 'with_tuneyr_and_cast': sum(1 for r in tu if r['cast']), 'gap_ge_50': len(gap)}
P['P7'] = len(gap) >= 0.3 * len(tu)
chk = [r for r in R if r['tower_hz']]
agree = [r for r in chk if abs(r['tower_hz'] - r['f']) <= 0.5]
out['check'] = {'rings_with_tower_hz': len(chk), 'agree': len(agree),
                'first_disagreeing_ring_ids': [r['ring'] for r in chk if abs(r['tower_hz'] - r['f']) > 0.5][:10]}
P['P8'] = len(agree) >= 0.95 * len(chk)
out['predictions'] = P
json.dump(out, open(sys.argv[4], 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
