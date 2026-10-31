"""Project 20, session 3: the registered count (SESSION3.md). Ring positions between the keys (as count2.py), counted per decade of
the year the sound was last made as far as the record says, in 100 one-cent cells; beats against A = 440; the inside check against
session 2's 1-cent histogram. Usage: count3.py bells.csv towers.csv explore2.json out.json"""
import csv, json, math, re, cmath, sys, statistics, collections as C

bells = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
towers = list(csv.DictReader(open(sys.argv[2], encoding='utf-8-sig')))
s2hist = json.load(open(sys.argv[3]))['hist_1c']

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
    return {'n': n, 'mean_cents': mu, 'R': R}
def beat(o):
    return abs(440 * 2 ** (o / 1200) - 440)

tower_by_ring = {}
for t in towers:
    tower_by_ring.setdefault(t['RingID'], t)
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
    o = pos(f)
    R.append({'o': o, 'cell': int(math.floor(o)) + 50, 'year': tune or cast, 'from_tune': bool(tune)})

def row(rs):
    cells = [0] * 100
    for r in rs:
        cells[r['cell']] += 1
    os = [r['o'] for r in rs]
    c = circ(os)
    n = len(rs)
    return {'n': n, 'cells': cells, 'R': c.get('R'), 'mean_cents': c.get('mean_cents'),
            'at_440': sum(1 for o in os if abs(o) <= 1.5), 'at_435': sum(1 for o in os if abs(o + 19.8) <= 1.5),
            'share_440': (sum(1 for o in os if abs(o) <= 1.5) / n) if n else None,
            'median_beat_hz': statistics.median(beat(o) for o in os) if n else None,
            'from_tuneyr': sum(1 for r in rs if r['from_tune'])}

dec = C.defaultdict(list)
for r in R:
    dec[(r['year'] // 10) * 10 if r['year'] else None].append(r)
out = {'rings': len(R), 'with_year': sum(1 for r in R if r['year']), 'from_tuneyr': sum(1 for r in R if r['from_tune'])}
out['decades'] = {str(d): row(dec[d]) for d in sorted(k for k in dec if k is not None)}
out['no_year'] = row(dec[None])
total = [0] * 100
for v in list(out['decades'].values()) + [out['no_year']]:
    total = [a + b for a, b in zip(total, v['cells'])]
s2 = [s2hist.get(str(i - 50), 0) for i in range(100)]
out['check'] = {'tonight_total_cells': total, 'session2_cells': s2, 'rings_tonight': len(R), 'rings_session2': 6549,
                'summed_abs_difference': sum(abs(a - b) for a, b in zip(total, s2))}
pre = [r for r in R if r['year'] and r['year'] < 1900]
late = [r for r in R if r['year'] and r['year'] >= 1990]
out['median_beat_before_1900'] = statistics.median(beat(r['o']) for r in pre)
out['median_beat_1990_on'] = statistics.median(beat(r['o']) for r in late)
out['n_before_1900'] = len(pre); out['n_1990_on'] = len(late)

D = out['decades']
counting = [(int(k), v) for k, v in D.items() if v['n'] >= 20]
first25 = next((k for k, v in counting if v['share_440'] > 0.25), None)
P = {}
P['P1'] = first25 is not None and 1950 <= first25 <= 1979
P['P2'] = all(v['R'] <= 0.25 for k, v in counting if k < 1900)
P['P3'] = 5.0 <= out['median_beat_before_1900'] <= 7.0
P['P4'] = out['median_beat_1990_on'] <= 2.0
P['P5'] = sum(1 for v in D.values() if v['n'] >= 1) >= 40
most = max(D.items(), key=lambda kv: kv[1]['n'])[0]
P['P6'] = 1850 <= int(most) <= 1919
P['P7'] = abs(len(R) - 6549) <= 10 and out['check']['summed_abs_difference'] <= 20
P['P8'] = 'run after the synthesis is written (sound3.py)'
out['first_decade_over_25pct_at_440'] = first25
out['decade_with_most_rings'] = int(most)
out['decades_with_rings'] = sum(1 for v in D.values() if v['n'] >= 1)
out['predictions'] = P
json.dump(out, open(sys.argv[4], 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('decades', 'check', 'no_year')}, indent=1))
print('check', len(R), out['check']['summed_abs_difference'])
