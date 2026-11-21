"""Exploratory (not registered): the shortest and longest counted spill, recomputed with rule.py over the raw files.
Usage: python3 -I explore1b.py <start-stop dir>  -> explore1b.json"""
import sys, glob, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import count1, rule
acts = {}
for f in sorted(glob.glob(sys.argv[1] + '/*')):
    for uid, _s, a, b in count1.read_startstop(f):
        ha, hb = count1.hours_of(a), count1.hours_of(b)
        u = str(uid).strip() if uid is not None else ''
        if not u or ha is None or hb is None or hb < ha or hb < 0 or ha >= count1.YEAR_H:
            continue
        acts.setdefault(u, []).append((max(ha, 0.0), min(hb, count1.YEAR_H)))
sp = [s['hours'] for l in acts.values() for s in rule.count_spills(l)]
out = {"counted_spills": len(sp), "min_hours": min(sp), "max_hours": max(sp), "zero_hours": sum(1 for x in sp if x == 0),
       "under_one_minute": sum(1 for x in sp if x < 1 / 60), "exactly_24h_or_more": sum(1 for x in sp if x >= 24 - 1e-6)}
json.dump(out, open('explore1b.json', 'w'), indent=1); print(out)
