"""Project 20, session 3, exploratory (after the registered count): since 1950, rings whose year is a tuning year against rings whose
year is their tenor's casting year; and, among retuned rings, how old the tenor was when tuned. Usage: explore3.py bells.csv towers.csv out.json"""
import csv, json, math, re, sys, statistics, collections as C
bells = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
towers = list(csv.DictReader(open(sys.argv[2], encoding='utf-8-sig')))
def num(s):
    try:
        v = float(s); return v if v > 0 else None
    except (ValueError, TypeError):
        return None
def year(s):
    m = re.search(r'(\d{4})', s or ''); return int(m.group(1)) if m else None
def pos(f):
    return ((1200 * math.log2(f / 440) + 50) % 100) - 50
def beat(o):
    return abs(440 * 2 ** (o / 1200) - 440)
tw = {}
for t in towers:
    tw.setdefault(t['RingID'], t)
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
    f = num(ten[0]['Nominal (Hz)'])
    if not f:
        continue
    t = tw.get(rid); tune = year(t['TuneYr']) if t else None; cast = year(ten[0]['Cast Date'])
    R.append({'o': pos(f), 'tune': tune, 'cast': cast, 'year': tune or cast})
def summ(rs):
    n = len(rs)
    if not n:
        return {'n': 0}
    return {'n': n, 'share_440': sum(1 for r in rs if abs(r['o']) <= 1.5) / n,
            'share_435': sum(1 for r in rs if abs(r['o'] + 19.8) <= 1.5) / n,
            'median_beat_hz': statistics.median(beat(r['o']) for r in rs)}
out = {}
for lo, hi in [(1930, 1959), (1960, 1989), (1990, 2029)]:
    rs = [r for r in R if r['year'] and lo <= r['year'] <= hi]
    new = [r for r in rs if not r['tune'] or (r['cast'] and r['tune'] - r['cast'] < 10)]
    old = [r for r in rs if r['tune'] and r['cast'] and r['tune'] - r['cast'] >= 50]
    out[f'{lo}-{hi}'] = {'all': summ(rs), 'tenor_new_when_sounded': summ(new), 'tenor_50y_older_than_tuning': summ(old),
                         'tuneyr_no_cast': sum(1 for r in rs if r['tune'] and not r['cast'])}
json.dump(out, open(sys.argv[3], 'w'), indent=1)
print(json.dumps(out, indent=1))
