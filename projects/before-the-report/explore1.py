"""Project 25 session 1, EXPLORATORY (not registered): event-level waits per centre and gravest class; drug events by report
year; where the drug Class I wait sits (before or after classification); the largest drug Class I event; implausible dates.
Usage: python3 -I explore1.py <per1.json> <out.json>. No firm or product name is written."""
import json, sys, collections, statistics
per = json.load(open(sys.argv[1]))
rank = {"Class I": 0, "Class II": 1, "Class III": 2, "other": 3}
E = collections.defaultdict(list)
for p in per:
    E[(p["centre"], p["event_id"])].append(p)
ev = []
for (c, e), ps in E.items():
    cs = [p["C"] for p in ps if p["C"] is not None]
    ev.append({"centre": c, "event_id": e, "g": min((p["class"] for p in ps), key=rank.get), "W": min(p["W"] for p in ps),
               "C": min(cs) if cs else None, "year": min(p["report"] for p in ps)[:4], "records": len(ps)})
med = lambda xs: statistics.median(xs) if xs else None
out = {"note": "exploratory; event = records sharing event_id within a centre; W and C of an event = min over its records"}
out["event_median_W"] = {c: {k: {"events": len([x for x in ev if x["centre"] == c and x["g"] == k]),
                                 "median_W": med([x["W"] for x in ev if x["centre"] == c and x["g"] == k]),
                                 "median_C": med([x["C"] for x in ev if x["centre"] == c and x["g"] == k and x["C"] is not None]),
                                 "median_W_minus_C": med([x["W"] - x["C"] for x in ev if x["centre"] == c and x["g"] == k and x["C"] is not None])}
                             for k in ["Class I", "Class II", "Class III"]} for c in ["food", "drug", "device"]}
yrs = sorted({x["year"] for x in ev})
out["event_median_W_by_year"] = {c: {y: {k: [len([x for x in ev if x["centre"] == c and x["year"] == y and x["g"] == k]),
                                             med([x["W"] for x in ev if x["centre"] == c and x["year"] == y and x["g"] == k])]
                                         for k in ["Class I", "Class II"]} for y in yrs} for c in ["food", "drug", "device"]}
big = max((x for x in ev if x["centre"] == "drug" and x["g"] == "Class I"), key=lambda x: x["records"])
out["largest_drug_class1_event"] = big
out["implausible_init_before_1990"] = [{k: p[k] for k in ("centre", "recall_number", "init", "report", "W")} for p in per if p["init"] < "1990"]
out["negative_W"] = [{k: p[k] for k in ("centre", "recall_number", "class", "init", "report", "W")} for p in per if p["W"] < 0]
json.dump(out, open(sys.argv[2], "w"), indent=1)
d = out["event_median_W"]
print(json.dumps(d, indent=0)); print(big); print(out["implausible_init_before_1990"]); print(len(out["negative_W"]))
