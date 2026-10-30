"""Project 20, session 2: exploration after the registered count (not registered; nothing here is a prediction's outcome).
The spike in ring positions near -20 cents: how sharp it is (1-cent bins), how many rings stand within 1.5 cents of each named
standard against the 3 % an even spread gives, and by tenor's cast era, tuning year and foundry. Also: whole-hertz tenors, and the spike at A=440. Writes explore2.json."""
import csv, json, math, re, sys, collections as C
sys.path.insert(0, __file__.rsplit('/', 1)[0])
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
pos = lambda f: ((1200 * math.log2(f / 440) + 50) % 100) - 50
STD = {'A=435 (diapason normal)': pos(435), 'A=439 (new philharmonic)': pos(439), 'A=440': 0.0, 'A=452.4 (old philharmonic)': pos(452.4)}
tw = {}
for t in towers:
    tw.setdefault(t['RingID'], t)
grp = {f['Name']: f['Group'] or f['Name'] for f in founders}
rings = C.defaultdict(list)
for b in bells:
    if b['Collection Type'] == 'full-circle ring':
        rings[b['Ring ID']].append(b)
R = []
for rid, bs in rings.items():
    size = bs[0]['Ring Size'].split()[0] if bs[0]['Ring Size'] else ''
    ten = [x for x in bs if x['Bell Role'] == size]
    if len(ten) != 1 or not num(ten[0]['Nominal (Hz)']):
        continue
    t = ten[0]; f = num(t['Nominal (Hz)']); T = tw.get(rid) or {}
    R.append({'f': f, 'o': pos(f), 'cast': year(t['Cast Date']), 'tune': year(T.get('TuneYr')), 'foundry': grp.get(t['Founder']),
              'country': T.get('Country'), 'fhz': round(f, 1)})
def near(rs, c, w=1.5):
    return sum(1 for r in rs if abs(((r['o'] - c + 50) % 100) - 50) <= w)
def table(rs):
    n = len(rs)
    return {'n': n, **{k: {'within_1.5c': near(rs, c), 'share': near(rs, c) / n if n else None} for k, c in STD.items()}}
out = {'standards_positions': STD, 'expected_share_even': 0.03}
out['all'] = table(R)
out['hist_1c'] = dict(sorted(C.Counter(math.floor(r['o']) for r in R).items()))
dec = lambda y: None if y is None else (y // 25) * 25
out['by_cast_25y'] = {str(k): table([r for r in R if dec(r['cast']) == k]) for k in sorted({dec(r['cast']) for r in R if r['cast']}) if k >= 1700}
out['by_tuneyr_25y'] = {str(k): table([r for r in R if dec(r['tune']) == k]) for k in sorted({dec(r['tune']) for r in R if r['tune']})}
fc = C.Counter(r['foundry'] for r in R)
out['by_foundry'] = {k: table([r for r in R if r['foundry'] == k]) for k, n in fc.most_common() if k and n >= 50}
out['by_country'] = {k: table([r for r in R if r['country'] == k]) for k, n in C.Counter(r['country'] for r in R).most_common() if n >= 50}
# the spike's frequencies: the most frequent tenor nominals (to 0.1 Hz) among rings within 1.5 c of A=435
sp = [r for r in R if abs(r['o'] - STD['A=435 (diapason normal)']) <= 1.5]
out['spike435_top_nominals'] = C.Counter(r['fhz'] for r in sp).most_common(15)
out['spike435_by_foundry'] = C.Counter(r['foundry'] for r in sp).most_common(8)
out['spike435_by_cast_25y'] = dict(sorted(C.Counter(dec(r['cast']) for r in sp if r['cast']).items()))
# whole-hertz tenors: is the spike made of round frequencies, and where do round frequencies fall otherwise?
whole = [r for r in R if abs(r['f'] - round(r['f'])) < 1e-9]
out['whole_hz'] = {'rings': len(whole), 'table': table(whole), 'not_whole_table': table([r for r in R if r not in whole])}
sp440 = [r for r in R if abs(r['o']) <= 1.5]
out['spike440_top_nominals'] = C.Counter(r['fhz'] for r in sp440).most_common(12)
out['spike440_by_foundry'] = C.Counter(r['foundry'] for r in sp440).most_common(6)
out['spike440_by_cast_25y'] = dict(sorted(C.Counter(dec(r['cast']) for r in sp440 if r['cast']).items()))
json.dump(out, open(sys.argv[4], 'w'), indent=1, ensure_ascii=False)
