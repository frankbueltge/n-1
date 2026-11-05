"""Project 22, session 2: the registered count (SESSION2.md). Run once, after this file is pushed.

Usage: python3 -I count2.py <dir holding wcvp_v10.zip ... wcvp_v16.zip> <out.json>
Reads the names table (the member ending in 'wcvp_names.csv') of each zip by streaming; nothing is unzipped to disk.
"""
import csv, io, json, re, sys, random, zipfile
from collections import Counter, defaultdict

csv.field_size_limit(10**9)
RELEASES = ['v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16']
YEAR = re.compile(r'(?<!\d)(\d{4})(?!\d)')
VOID = {'Illegitimate', 'Invalid', 'Orthographic', 'Misapplied'}
FORM = {'standing': 'whole', 'moved': 'passed on', 'merged': 'gone', 'void': 'gone'}


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


def read_release(path):
    z = zipfile.ZipFile(path)
    members = [n for n in z.namelist() if n.endswith('wcvp_names.csv')]
    assert len(members) == 1, (path, z.namelist())
    sp, nonsp, meta = {}, set(), {}
    flags = Counter()
    rows = 0
    with z.open(members[0]) as raw:
        f = io.TextIOWrapper(raw, encoding='utf-8', newline='')
        r = csv.DictReader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        header = r.fieldnames
        for d in r:
            rows += 1
            pid = d['plant_name_id']
            if d['taxon_rank'] == 'Species':
                k = kind(d['taxon_status'], d.get('homotypic_synonym'))
                sp[pid] = k
                meta[pid] = (year_of(d['first_published']), d.get('place_of_publication') or '')
                if d['taxon_status'] == 'Synonym':
                    flags[(d.get('homotypic_synonym') or '').strip()] += 1
            else:
                nonsp.add(pid)
    return {'member': members[0], 'header': header, 'rows': rows, 'sp': sp, 'nonsp': nonsp, 'meta': meta,
            'synonym_flag_values': dict(flags.most_common(10))}


def share_standing(sp, meta):
    c = Counter(k for pid, k in sp.items() if meta[pid][0] is not None)
    t = sum(c.values())
    return round(c['standing'] / t, 5) if t else None, t


def main(d, out):
    R = {}
    for v in RELEASES:
        R[v] = read_release('%s/wcvp_%s.zip' % (d, v))
        print(v, R[v]['rows'], len(R[v]['sp']), file=sys.stderr)
    # year and publication: from v16, else the latest release holding the name
    meta = {}
    for v in RELEASES:
        meta.update(R[v]['meta'])
    a, b = R['v10']['sp'], R['v16']['sp']
    both = [pid for pid in a if pid in b]
    to_nonsp = sum(1 for pid in a if pid not in b and pid in R['v16']['nonsp'])
    vanished = sum(1 for pid in a if pid not in b and pid not in R['v16']['nonsp'])
    changed = [pid for pid in both if a[pid] != b[pid]]
    flow = Counter((a[pid], b[pid]) for pid in changed)
    form_flow = Counter((FORM.get(a[pid], a[pid]), FORM.get(b[pid], b[pid])) for pid in changed)
    st_out = sum(n for (x, y), n in flow.items() if x == 'standing' and y in ('moved', 'merged', 'void'))
    st_in = sum(n for (x, y), n in flow.items() if y == 'standing' and x in ('moved', 'merged', 'void'))
    moved_vs_merged_only = sum(n for (x, y), n in flow.items() if {x, y} == {'moved', 'merged'})

    def lost_share(lo, hi):
        s = [pid for pid in both if a[pid] == 'standing' and meta[pid][0] is not None and lo <= meta[pid][0] <= hi]
        n = sum(1 for pid in s if b[pid] in ('moved', 'merged', 'void'))
        return (round(n / len(s), 5) if s else None), n, len(s)

    lost_2000, n2000, t2000 = lost_share(2000, 2022)
    lost_1800, n1800, t1800 = lost_share(1800, 1899)
    to_syn = Counter(b[pid] for pid in changed if a[pid] == 'standing' and b[pid] in ('moved', 'merged'))
    unj = [pid for pid in both if a[pid] == 'unjudged']
    unj_judged = sum(1 for pid in unj if b[pid] != 'unjudged')
    s10, t10 = share_standing(a, meta)
    s16, t16 = share_standing(b, meta)
    pubs = Counter(meta[pid][1] for pid in changed)
    top_pub, top_n = pubs.most_common(1)[0] if pubs else ('', 0)

    steps = {}
    for v, w in zip(RELEASES, RELEASES[1:]):
        x, y = R[v]['sp'], R[w]['sp']
        ch = Counter((x[p], y[p]) for p in x if p in y and x[p] != y[p])
        steps[v + '-' + w] = {'changed': sum(ch.values()), 'present_in_both': sum(1 for p in x if p in y),
                              'flows_top': [[k[0], k[1], n] for k, n in ch.most_common(8)]}
    top_step = max(steps, key=lambda s: steps[s]['changed'])

    added_old = sum(1 for pid in b if pid not in a and meta[pid][0] is not None and meta[pid][0] <= 2022)
    added_all = sum(1 for pid in b if pid not in a)

    allseven = [pid for pid in a if all(pid in R[v]['sp'] for v in RELEASES)]
    rev = 0
    multi = 0
    for pid in allseven:
        seq = [R[v]['sp'][pid] for v in RELEASES]
        nch = sum(1 for i in range(6) if seq[i] != seq[i + 1])
        if nch >= 2:
            multi += 1
            last = seq[-1]
            left = [seq[i] for i in range(6) if seq[i] != seq[i + 1]]
            if last in left:
                rev += 1

    by_dec = defaultdict(Counter)
    for pid in both:
        y = meta[pid][0]
        if y is None:
            continue
        dd = str(min(y // 10 * 10, 2020))
        by_dec[dd]['n'] += 1
        if a[pid] != b[pid]:
            by_dec[dd]['changed'] += 1
            if a[pid] == 'standing' and b[pid] in ('moved', 'merged', 'void'):
                by_dec[dd]['standing_out'] += 1
            if b[pid] == 'standing' and a[pid] in ('moved', 'merged', 'void'):
                by_dec[dd]['standing_in'] += 1

    rnd = random.Random(20261105)
    sample = rnd.sample(sorted(changed), min(12, len(changed)))

    share_changed = len(changed) / len(both)
    P = {
        'P1': len(both) / len(a) >= 0.98,
        'P2': 0.01 <= share_changed <= 0.05,
        'P3': st_out > st_in,
        'P4': (lost_2000 or 0) > (lost_1800 or 0),
        'P5': to_syn['moved'] > to_syn['merged'],
        'P6': (unj_judged / len(unj) if unj else 0) >= 0.10,
        'P7': abs(s16 - s10) < 0.01,
        'P8': (top_n / len(changed) if changed else 0) < 0.05,
        'P9': top_step == 'v12-v13',
        'P10': added_old >= 5000,
        'P11': (rev / len(allseven) if allseven else 1) < 0.001,
    }
    res = {
        'releases': {v: {'member': R[v]['member'], 'header': R[v]['header'], 'rows': R[v]['rows'],
                         'species_names': len(R[v]['sp']), 'synonym_flag_values': R[v]['synonym_flag_values'],
                         'kinds': dict(Counter(R[v]['sp'].values()))} for v in RELEASES},
        'v10_species': len(a), 'v16_species': len(b), 'present_in_both': len(both),
        'share_v10_present_in_v16': round(len(both) / len(a), 5),
        'v10_species_now_other_rank': to_nonsp, 'v10_species_vanished': vanished,
        'changed': len(changed), 'share_changed': round(share_changed, 5),
        'flow_kinds': [[x, y, n] for (x, y), n in flow.most_common()],
        'flow_forms': [[x, y, n] for (x, y), n in form_flow.most_common()],
        'standing_out': st_out, 'standing_in': st_in, 'moved_merged_only': moved_vs_merged_only,
        'lost_share_2000_2022': [lost_2000, n2000, t2000], 'lost_share_1800_1899': [lost_1800, n1800, t1800],
        'standing_to_synonym': dict(to_syn),
        'unjudged_v10_in_both': len(unj), 'unjudged_judged_v16': unj_judged,
        'share_standing_v10': [s10, t10], 'share_standing_v16': [s16, t16],
        'top_publication': [top_pub, top_n], 'publications_top10': pubs.most_common(10),
        'steps': steps, 'top_step': top_step,
        'added_v16_year_le_2022': added_old, 'added_v16_all': added_all,
        'present_all_seven': len(allseven), 'changed_twice_or_more': multi, 'reversals': rev,
        'decades': {k: dict(v) for k, v in sorted(by_dec.items())},
        'check_sample': [{'plant_name_id': p, 'v10': a[p], 'v16': b[p], 'year': meta[p][0]} for p in sample],
        'predictions': P,
    }
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: res[k] for k in ('changed', 'share_changed', 'standing_out', 'standing_in', 'top_step', 'predictions')},
                     indent=1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
