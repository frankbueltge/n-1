"""Project 22, session 2: exploratory, after the count (not registered). (a) For changes v10->v16, whether the accepted name a synonym
points to stayed the same (a flag or status repair under the same accepted name) or changed (the name re-placed). (b) Per decade, the
share of v10's standing names no longer standing in v16, and of v10's undone names standing in v16. (c) Per step, net standing.
Usage: python3 -I explore2.py <dir with wcvp_v10.zip, wcvp_v16.zip> <session2.json> <out.json>"""
import csv, io, json, re, sys, zipfile
from collections import Counter, defaultdict
csv.field_size_limit(10**9)
YEAR = re.compile(r'(?<!\d)(\d{4})(?!\d)')
VOID = {'Illegitimate', 'Invalid', 'Orthographic', 'Misapplied'}


def year_of(s):
    for m in YEAR.finditer(s or ''):
        y = int(m.group(1))
        if 1753 <= y <= 2026:
            return y


def kind(st, h):
    if st == 'Accepted': return 'standing'
    if st == 'Synonym': return 'moved' if (h or '').strip().upper() in ('T', 'TRUE') else 'merged'
    if st in VOID: return 'void'
    if st == 'Unplaced': return 'unjudged'
    return 'other:' + st


def load(p):
    z = zipfile.ZipFile(p)
    out = {}
    with z.open([n for n in z.namelist() if n.endswith('wcvp_names.csv')][0]) as raw:
        for d in csv.DictReader(io.TextIOWrapper(raw, encoding='utf-8', newline=''), delimiter='|', quoting=csv.QUOTE_NONE):
            if d['taxon_rank'] == 'Species':
                out[d['plant_name_id']] = (kind(d['taxon_status'], d['homotypic_synonym']), d['accepted_plant_name_id'],
                                           year_of(d['first_published']))
    return out


a = load(sys.argv[1] + '/wcvp_v10.zip')
b = load(sys.argv[1] + '/wcvp_v16.zip')
same_acc = Counter()
for p, (k, acc, _) in a.items():
    if p in b and b[p][0] != k:
        same_acc[(k, b[p][0], 'same accepted' if acc and acc == b[p][1] else 'accepted changed or none')] += 1
dec = defaultdict(Counter)
for p, (k, acc, _) in a.items():
    if p not in b:
        continue
    y = b[p][2]
    if y is None:
        continue
    dd = str(min(y // 10 * 10, 2020))
    if k == 'standing':
        dec[dd]['standing_v10'] += 1
        if b[p][0] in ('moved', 'merged', 'void'):
            dec[dd]['lost'] += 1
    elif k in ('moved', 'merged', 'void'):
        dec[dd]['undone_v10'] += 1
        if b[p][0] == 'standing':
            dec[dd]['raised'] += 1
for dd, c in dec.items():
    c['lost_share'] = round(c['lost'] / c['standing_v10'], 4) if c['standing_v10'] else None
    c['raised_share'] = round(c['raised'] / c['undone_v10'], 4) if c['undone_v10'] else None
s2 = json.load(open(sys.argv[2]))
net = {}
for s, v in s2['steps'].items():
    f = Counter()
    for x, y, n in v['flows_top']:
        f[(x, y)] = n
    net[s] = 'see session2.json flows_top (top 8 only)'
res = {'note': 'exploratory, after the count; not registered',
       'v10_v16_changes_by_accepted_link': [[k[0], k[1], k[2], n] for k, n in same_acc.most_common(30)],
       'decades': {k: dict(v) for k, v in sorted(dec.items())}}
json.dump(res, open(sys.argv[3], 'w'), indent=1)
for r in res['v10_v16_changes_by_accepted_link'][:16]: print(r)
for k, v in res['decades'].items(): print(k, v)
