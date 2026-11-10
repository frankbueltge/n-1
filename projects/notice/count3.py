#!/usr/bin/env python3
"""Project 23 session 3: the registered count (SESSION3.md). Reads session2.json only: for each episode, when it was set right
(the correcting release's date); lag weighted by hours; distinct correcting releases; regions by kinds; and the hidden curve --
at each date T, the region-hours already lived, wrong, and not yet set right by any release dated on or before T.
usage: python3 -I count3.py session2.json OUT.json"""
import calendar, collections, json, sys
r = json.load(open(sys.argv[1]))
D = r["release_dates"]; E = r["episodes_rows"]
ts = lambda s: calendar.timegm(tuple(map(int, s.split("-"))) + (0, 0, 0))
for e in E:
    e["fixed"] = ts(D[e["corr"]])
total = sum(e["hours"] for e in E)
by_corr = collections.Counter()
for e in E:
    by_corr[e["corr"]] += e["hours"]
top = by_corr.most_common(1)[0]
# hours-weighted median lag
w = sorted((e["lag_days"], e["hours"]) for e in E); acc = 0; med = None
for lag, h in w:
    acc += h
    if acc >= total / 2:
        med = lag; break
within90 = sum(e["hours"] for e in E if e["lag_days"] <= 90)
kinds = collections.defaultdict(set)
for e in E:
    kinds[e["zone"]].add(e["kind"])
multi = sum(1 for z in kinds if len(kinds[z]) >= 2)
def hidden(T):
    return sum(max(0, min(e["t1"], T) - e["t0"]) / 3600 for e in E if e["fixed"] > T)
days = []
T = ts("1997-01-01"); end = ts("2026-11-07")
while T <= end:
    days.append((T, hidden(T))); T += 86400 * 7
days.append((end, hidden(end)))
mx = max(days, key=lambda x: x[1])
h2016, h2026, hend = hidden(ts("2016-01-01")), hidden(ts("2026-01-01")), hidden(end)
by_fixed_year = collections.Counter()
for e in E:
    by_fixed_year[D[e["corr"]][:4]] += e["hours"]
out = {
    "episodes": len(E), "hours": round(total, 1), "distinct_corr": len(by_corr),
    "top_corr": {"release": top[0], "date": D[top[0]], "hours": top[1]},
    "by_corr": dict(by_corr.most_common()), "by_fixed_year": dict(sorted(by_fixed_year.items())),
    "median_lag_days_weighted": med, "share_within_90d": within90 / total,
    "regions": len(kinds), "regions_multi_kind": multi,
    "hidden_max": {"date": mx[0], "hours": mx[1]},
    "hidden_2016": h2016, "hidden_2026": h2026, "hidden_end": hend,
    "hidden_weekly": [[t, round(h, 1)] for t, h in days],
}
out["predictions"] = {
    "P1": len(E) == 505 and abs(total - r["zone_hours_wrong"]) <= 0.1,
    "P2": 60 <= len(by_corr) <= 160,
    "P3": int(D[top[0]][:4]) >= 2014,
    "P4": med is not None and med > 5 * 365,
    "P5": within90 / total < 0.15,
    "P6": multi >= 25,
    "P7": mx[0] < ts("2010-01-01"),
    "P8": h2016 > 300000,
    "P9": hend == 0 and h2026 < 1000,
}
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("by_corr", "hidden_weekly")}, indent=1))
