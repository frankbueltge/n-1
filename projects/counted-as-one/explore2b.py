"""Project 26 session 2, exploratory (unregistered): discharge hours per day of 2025 for all overflows, bathing-named ones and U.
Usage: python3 -I explore2b.py <start-stop dir>   (run in projects/counted-as-one/, after count2.py). Writes explore2b.json."""
import glob, gzip, json, os, sys
sys.path.insert(0, '.')
import count1
P = json.load(gzip.open('session2-per.json.gz', 'rt'))
S = json.load(open('session2.json'))
med = S['median_hours_O']
grp = {'all': set(r['uid'] for r in P), 'bathing': set(r['uid'] for r in P if r['bathing']),
       'U': set(r['uid'] for r in P if r['count'] < 30 and r['hours'] > med)}
day = {g: [0.0] * 365 for g in grp}
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.csv')) + glob.glob(os.path.join(sys.argv[1], '*.xlsx'))):
    for uid, _s, a, b in count1.read_startstop(f):
        uid = (str(uid).strip() if uid is not None else '')
        ha, hb = count1.hours_of(a), count1.hours_of(b)
        if not uid or ha is None or hb is None or hb < ha:
            continue
        ha, hb = max(ha, 0.0), min(hb, count1.YEAR_H)
        for g, ids in grp.items():
            if uid in ids:
                t = ha
                while t < hb:
                    d = int(t // 24)
                    e = min(hb, (d + 1) * 24.0)
                    day[g][d] += e - t
                    t = e
out = {g: [round(x, 3) for x in v] for g, v in day.items()}
out['totals'] = {g: sum(v) for g, v in day.items()}
json.dump(out, open('explore2b.json', 'w'))
print(out['totals'], {g: sum(v[134:273]) / sum(v) for g, v in day.items()})
