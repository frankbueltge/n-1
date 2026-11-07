#!/usr/bin/env python3
"""Exploratory, after the count (project 23 session 1). Reads explore1.json (count1.py run with the helper).
Splits late transitions into news arriving late (within 365 days after) and the past rewritten (more than 365 days after),
and groups late news into events: same first release, effect dates within 2 days."""
import json, sys, time, collections
r = json.load(open(sys.argv[1]))
core = [x for x in r["rows"] if not x["with_zone"] and not x["censored"]]
Y = lambda x: int(time.strftime("%Y", time.gmtime(x["t"])))
D = lambda x: time.strftime("%Y-%m-%d %H:%M", time.gmtime(x["t"]))
news = [x for x in core if -365 <= x["lead_days"] < 0]
past = [x for x in core if x["lead_days"] < -365]
short = [x for x in core if 0 <= x["lead_days"] < 30]
per_year = {}
for x in core:
    a = per_year.setdefault(Y(x), {"core": 0, "late_news": 0, "past_rewritten": 0, "under_30_days": 0})
    a["core"] += 1
    if -365 <= x["lead_days"] < 0: a["late_news"] += 1
    elif x["lead_days"] < -365: a["past_rewritten"] += 1
    elif x["lead_days"] < 30: a["under_30_days"] += 1
events = []
for x in sorted(news + short, key=lambda x: (x["first"], x["t"])):
    e = events[-1] if events else None
    if e and e["first"] == x["first"] and abs(x["t"] - e["t_max"]) <= 2 * 86400:
        e["zones"].append(x["zone"]); e["t_max"] = max(e["t_max"], x["t"]); e["leads"].append(x["lead_days"])
    else:
        events.append({"first": x["first"], "first_date": x["first_date"], "t": x["t"], "t_max": x["t"], "when": D(x),
                       "zones": [x["zone"]], "leads": [x["lead_days"]]})
for e in events:
    e["lead_days_min"] = min(e["leads"]); e["n"] = len(e["zones"]); del e["leads"], e["t_max"]
out = {
    "core": len(core), "late_news": len(news), "past_rewritten": len(past), "under_30_days": len(short),
    "per_year": per_year,
    "events_late_or_under_30": events,
    "events_late": sum(1 for e in events if e["lead_days_min"] < 0),
    "past_rewritten_by_first_release_year": dict(collections.Counter(x["first"][:4] for x in past).most_common()),
    "late_news_lead_median": sorted(x["lead_days"] for x in news)[len(news)//2] if news else None,
}
json.dump(out, open(sys.argv[2], "w"), indent=0)
print({k: v for k, v in out.items() if k not in ("events_late_or_under_30", "per_year")})
for e in events:
    print(e["first"], e["first_date"], e["when"], e["n"], round(e["lead_days_min"], 1), e["zones"][:3])
