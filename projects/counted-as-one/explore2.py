"""Project 26 session 2, exploratory (unregistered): the record's own trigger word for U and O; where in the year the differing recounts lie.
Usage: python3 -I explore2.py <start-stop dir>   (run in projects/counted-as-one/, after count2.py)"""
import collections, gzip, json, sys, os
sys.path.insert(0, '.')
import count1
P = json.load(gzip.open('session2-per.json.gz', 'rt'))
S = json.load(open('session2.json'))
med = S['median_hours_O']
O = [r for r in P if r['count'] >= 30]
U = [r for r in P if r['count'] < 30 and r['hours'] > med]
out = {}
out['hsf_reason_U'] = collections.Counter(r['hsf_reason'] for r in U).most_common()
out['hsf_reason_O'] = collections.Counter(r['hsf_reason'] for r in O).most_common(8)
out['U_season_zero'] = sum(1 for r in U if r['season_h'] == 0)
out['U_bathing_named'] = sorted((r['uid'], r['bathing'], round(r['hours']), r['count'], round(r['season_h'], 1)) for r in U if r['bathing'])
# year edges: does a differing overflow have an activation within 36 h of 1 Jan 00:00 or of 31 Dec 24:00?
import glob
acts = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.csv')) + glob.glob(os.path.join(sys.argv[1], '*.xlsx'))):
    for uid, _s, a, b in count1.read_startstop(f):
        uid = (str(uid).strip() if uid is not None else '')
        ha, hb = count1.hours_of(a), count1.hours_of(b)
        if uid and ha is not None and hb is not None and hb >= ha:
            acts.setdefault(uid, []).append((ha, hb))
edge = lambda u: any(a < 36 or b > count1.YEAR_H - 36 for a, b in acts.get(u, []))
cls = collections.defaultdict(lambda: [0, 0])
for r in P:
    d = r['count'] - r['ar_count']
    k = 'equal' if d == 0 else ('+1' if d == 1 else ('-1' if d == -1 else 'other'))
    cls[k][0] += 1
    cls[k][1] += edge(r['uid'])
out['year_edge_by_difference'] = {k: {'n': v[0], 'with_activation_within_36h_of_year_edge': v[1]} for k, v in cls.items()}
json.dump(out, open('explore2.json', 'w'), indent=1)
print(json.dumps(out, indent=1)[:3000])
