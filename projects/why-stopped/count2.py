"""The registered count of session 2 (SESSION2.md). Usage: python3 count2.py RAWDIR -> session2.json"""
import collections, json, sys
from lib import load
from dating import line_month, year_only

rows = load(sys.argv[1])
pop = [r for r in rows if r["flag"] and r["stop"] and r["status"] in ("TERMINATED", "WITHDRAWN")]
for r in pop:
    r["lm"] = line_month(r["why"])
dated = [r for r in pop if r["lm"]]
late = [r for r in dated if r["lm"] > r["stop"]]
forward = [r for r in dated if r["lastupd"] and r["lm"] > r["lastupd"]]
lm_counts = collections.Counter(r["lm"] for r in dated)
anach_ids = {x["nct"] for x in json.load(open("anach1.json"))["items"] if x["names"] == "COVID-19"}
anach = [r for r in rows if r["nct"] in anach_ids]
anach_dated = [r for r in anach if line_month(r["why"])]

def months_between(a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + int(b[5:]) - int(a[5:])

gaps = sorted(months_between(r["stop"], r["lm"]) for r in late)
susp = [r for r in rows if r["flag"] and r["status"] == "SUSPENDED"]
susp_dated = [r for r in susp if line_month(r["why"])]
out = {
    "data": "ClinicalTrials.gov API v2, processed 2026-10-22T09:00:04; 54 pages, hashes equal to session 1's fetch_log.json",
    "population": len(pop), "self_dated": len(dated), "year_only": sum(year_only(r["why"]) for r in pop),
    "late_lines": len(late), "forward_lines": len(forward),
    "late_gap_months": {"median": gaps[len(gaps) // 2] if gaps else None, "max": gaps[-1] if gaps else None,
                        "at_least_12": sum(g >= 12 for g in gaps)},
    "line_month_top": lm_counts.most_common(12),
    "line_month_by_year": sorted(collections.Counter(r["lm"][:4] for r in dated).items()),
    "anachronisms_covid": len(anach), "anachronisms_self_dated": len(anach_dated),
    "anachronisms_self_dated_items": [{"nct": r["nct"], "stop": r["stop"], "line_month": line_month(r["why"]),
                                        "lastupd": r["lastupd"]} for r in anach_dated],
    "suspended_flagged": len(susp), "suspended_self_dated": len(susp_dated),
    "late_items": [{"nct": r["nct"], "stop": r["stop"], "line_month": r["lm"], "lastupd": r["lastupd"]} for r in late],
    "forward_items": [{"nct": r["nct"], "stop": r["stop"], "line_month": r["lm"], "lastupd": r["lastupd"]} for r in forward],
}
pct = lambda a, b: round(100.0 * a / b, 1) if b else None
P = [("between 4 % and 20 % of the population are self-dated", pct(len(dated), len(pop)), 4 <= pct(len(dated), len(pop)) <= 20),
     ("of the self-dated, at least 30 % are late lines", pct(len(late), len(dated)), pct(len(late), len(dated)) >= 30),
     ("of the self-dated, at most 5 % are forward lines", pct(len(forward), len(dated)), pct(len(forward), len(dated)) <= 5),
     ("of the 86 COVID-19 anachronisms, fewer than 20 % are self-dated", pct(len(anach_dated), len(anach)),
      pct(len(anach_dated), len(anach)) < 20),
     ("the month most often named as the line's month is March 2020", lm_counts.most_common(1)[0],
      lm_counts.most_common(1)[0][0] == "2020-03")]
out["predictions"] = [{"n": i + 1, "registered": p, "value": v, "held": h} for i, (p, v, h) in enumerate(P)]
json.dump(out, open("session2.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if not k.endswith("_items")}, indent=1))
