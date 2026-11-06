"""Project 22, session 3: the registered count (SESSION3.md). Run once, after this file is pushed.

Usage: python3 -I count3.py <dir holding wcvp_v10.zip ... wcvp_v16.zip> <out.json>
Streams the names table of each zip; nothing is unzipped to disk. Output: counts per (step, year, class), totals, predictions, and a
seeded sample of events (ids only, kept in the json for the independent check; ids are not carried onto the page).
"""
import csv, io, json, re, sys, random, zipfile
from collections import Counter, defaultdict

csv.field_size_limit(10**9)
RELEASES = ['v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16']
YEAR = re.compile(r'(?<!\d)(\d{4})(?!\d)')
VOID = {'Illegitimate', 'Invalid', 'Orthographic', 'Misapplied'}
VERDICT = {'moved', 'merged', 'void'}
DRAWN = ['condemned', 'acquitted', 'sent', 'judged', 'withdrawn']
CLASSES = DRAWN + ['re-described', 'other']


def year_of(s):
    for m in YEAR.finditer(s or ''):
        y = int(m.group(1))
        if 1753 <= y <= 2026:
            return y
    return None


def kind(status, homo):
    if status == 'Accepted':
        return 'standing'
    if status == 'Synonym':
        return 'moved' if (homo or '').strip().upper() in ('T', 'TRUE') else 'merged'
    if status in VOID:
        return 'void'
    if status == 'Unplaced':
        return 'unjudged'
    return 'other:' + status


def classify(k1, a1, k2, a2):
    if k1 == 'standing' and k2 in VERDICT:
        return 'condemned'
    if k1 in VERDICT and k2 == 'standing':
        return 'acquitted'
    if k1 in VERDICT and k2 in VERDICT:
        return 're-described' if (a1 and a1 == a2) else 'sent'
    if k1 == 'unjudged' and (k2 in VERDICT or k2 == 'standing'):
        return 'judged'
    if (k1 in VERDICT or k1 == 'standing') and k2 == 'unjudged':
        return 'withdrawn'
    return 'other'


def read_release(path):
    z = zipfile.ZipFile(path)
    members = [n for n in z.namelist() if n.endswith('wcvp_names.csv')]
    assert len(members) == 1, (path, z.namelist())
    sp, years = {}, {}
    with z.open(members[0]) as raw:
        r = csv.DictReader(io.TextIOWrapper(raw, encoding='utf-8', newline=''), delimiter='|', quoting=csv.QUOTE_NONE)
        for d in r:
            if d['taxon_rank'] == 'Species':
                pid = d['plant_name_id']
                sp[pid] = (kind(d['taxon_status'], d.get('homotypic_synonym')), (d.get('accepted_plant_name_id') or '').strip())
                years[pid] = year_of(d['first_published'])
    return sp, years


def main(d, out):
    R, Y = {}, {}
    for v in RELEASES:
        R[v], Y[v] = read_release('%s/wcvp_%s.zip' % (d, v))
        print(v, len(R[v]), file=sys.stderr)
    year = {}
    for v in RELEASES:          # later releases overwrite: year from v16, else the latest release holding the name
        year.update(Y[v])
    v16_names_per_year = Counter(y for y in Y['v16'].values() if y is not None)
    v16_standing_per_year = Counter(Y['v16'][p] for p, (k, _) in R['v16'].items() if k == 'standing' and Y['v16'][p] is not None)
    cells = defaultdict(Counter)     # step -> Counter((year, class))
    totals = Counter()
    per_step = {}
    events = []
    for v, w in zip(RELEASES, RELEASES[1:]):
        s = v + '-' + w
        x, yv = R[v], R[w]
        c = Counter()
        for pid, (k1, a1) in x.items():
            if pid not in yv:
                continue
            k2, a2 = yv[pid]
            if k1 == k2:
                continue
            cl = classify(k1, a1, k2, a2)
            c[cl] += 1
            cells[s][(year.get(pid), cl)] += 1
            events.append((s, pid, cl))
        per_step[s] = {'events': sum(c.values()), 'classes': {k: c[k] for k in CLASSES}}
        totals.update(c)
    all_events = sum(totals.values())
    drawn = sum(totals[k] for k in DRAWN)
    drawn_per_year = Counter()
    for s in cells:
        for (y, cl), n in cells[s].items():
            if cl in DRAWN and y is not None:
                drawn_per_year[y] += n
    top_year = max(drawn_per_year, key=drawn_per_year.get) if drawn_per_year else None
    steps_with_1753 = sum(1 for s in cells if any(n for (y, cl), n in cells[s].items() if y == 1753 and cl in DRAWN))

    def rate(lo, hi):
        e = sum(n for y, n in drawn_per_year.items() if lo <= y <= hi)
        t = sum(n for y, n in v16_names_per_year.items() if lo <= y <= hi)
        return round(1000 * e / t, 3) if t else None, e, t
    rate_new, rate_old = rate(2000, 2026), rate(1753, 1799)
    expected = [11226, 7974, 6300, 8455, 3523, 4436]
    got = [per_step[s]['events'] for s in per_step]
    largest = max(CLASSES, key=lambda k: totals[k])
    P = {
        'P1': got == expected,
        'P2': largest == 're-described' and totals['re-described'] >= 0.30 * all_events,
        'P3': all(per_step[s]['classes']['condemned'] > per_step[s]['classes']['acquitted'] for s in per_step),
        'P4': per_step['v10-v11']['classes']['re-described'] >= 0.5 * per_step['v10-v11']['events'],
        'P5': 20000 <= drawn <= 32000,
        'P6': totals['sent'] >= 5000,
        'P7': top_year == 1891,
        'P8': steps_with_1753 >= 4,
        'P9': rate_new[0] is not None and rate_old[0] is not None and rate_new[0] > rate_old[0],
    }
    rnd = random.Random(20261106)
    drawn_ev = sorted(e for e in events if e[2] in DRAWN)
    redesc_ev = sorted(e for e in events if e[2] == 're-described')
    sample = rnd.sample(drawn_ev, min(12, len(drawn_ev))) + rnd.sample(redesc_ev, min(4, len(redesc_ev)))
    res = {
        'note': 'registered count, SESSION3.md; run once',
        'steps': per_step, 'step_events': got, 'totals': {k: totals[k] for k in CLASSES}, 'all_events': all_events,
        'drawn': drawn, 'largest_class': largest, 'top_year_drawn': [top_year, drawn_per_year.get(top_year)],
        'steps_with_1753_drawn': steps_with_1753, 'rate_2000_2026': rate_new, 'rate_1753_1799': rate_old,
        'events_without_year': sum(n for s in cells for (y, cl), n in cells[s].items() if y is None),
        'cells': {s: [[y, cl, n] for (y, cl), n in sorted(cells[s].items(), key=lambda t: (t[0][0] or 0, t[0][1])) if y is not None]
                  for s in cells},
        'v16_names_per_year': sorted(v16_names_per_year.items()),
        'v16_standing_per_year': sorted(v16_standing_per_year.items()),
        'check_sample': [{'step': s, 'plant_name_id': p, 'class': c} for s, p, c in sample],
        'predictions': P,
    }
    json.dump(res, open(out, 'w'), indent=0)
    print(json.dumps({k: res[k] for k in ('step_events', 'totals', 'all_events', 'drawn', 'largest_class', 'top_year_drawn',
                                          'steps_with_1753_drawn', 'rate_2000_2026', 'rate_1753_1799', 'predictions')}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
