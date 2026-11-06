"""Project 22, session 3: P11, the independent parse (SESSION3.md). Shares no code with count3.py: raw lines, plain split on '|',
the class derived by hand. Usage: python3 -I check3.py <dir with the zips> <session3.json> <out.json>"""
import json, sys, zipfile
s3 = json.load(open(sys.argv[2]))
want = {}
for e in s3['check_sample']:
    a, b = e['step'].split('-')
    want.setdefault(a, set()).add(e['plant_name_id']); want.setdefault(b, set()).add(e['plant_name_id'])
rows = {}
for v, ids in want.items():
    p = sys.argv[1] + '/wcvp_%s.zip' % v
    z = zipfile.ZipFile(p)
    m = [n for n in z.namelist() if n.endswith('wcvp_names.csv')][0]
    with z.open(m) as f:
        head = f.readline().decode('utf-8').rstrip('\r\n').split('|')
        ix = {h: i for i, h in enumerate(head)}
        for raw in f:
            parts = raw.decode('utf-8').rstrip('\r\n').split('|')
            if parts[ix['plant_name_id']] in ids:
                rows[(v, parts[ix['plant_name_id']])] = (parts[ix['taxon_rank']], parts[ix['taxon_status']],
                                                         parts[ix['homotypic_synonym']], parts[ix['accepted_plant_name_id']])
def by_hand(st, fl, acc_same_nonempty_unused=None):
    if st == 'Accepted': return 'A'
    if st == 'Synonym': return 'S'
    if st in ('Illegitimate', 'Invalid', 'Orthographic', 'Misapplied'): return 'S'   # a verdict that is not standing
    if st == 'Unplaced': return 'U'
    return 'X'
out = []
for e in s3['check_sample']:
    a, b = e['step'].split('-'); p = e['plant_name_id']
    r1, r2 = rows.get((a, p)), rows.get((b, p))
    c1, c2 = by_hand(r1[1], r1[2]), by_hand(r2[1], r2[2])
    if c1 == 'A' and c2 == 'S': cl = 'condemned'
    elif c1 == 'S' and c2 == 'A': cl = 'acquitted'
    elif c1 == 'S' and c2 == 'S': cl = 're-described' if r1[3].strip() and r1[3].strip() == r2[3].strip() else 'sent'
    elif c1 == 'U' and c2 in 'AS': cl = 'judged'
    elif c1 in 'AS' and c2 == 'U': cl = 'withdrawn'
    else: cl = 'other'
    out.append({'step': e['step'], 'plant_name_id': p, 'count3': e['class'], 'check3': cl, 'agree': cl == e['class'],
                'raw_' + a: list(r1), 'raw_' + b: list(r2)})
res = {'agree': sum(o['agree'] for o in out), 'of': len(out), 'rows': out}
json.dump(res, open(sys.argv[3], 'w'), indent=1)
print(res['agree'], 'of', res['of'])
for o in out: print(o['step'], o['plant_name_id'], o['count3'], o['check3'])
