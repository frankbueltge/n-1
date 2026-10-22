"""The registered count of session 1 (SELECTION.md). Usage: python3 count1.py RAWDIR -> session1.json."""
import json, sys
from collections import Counter
from lib import load

R = load(sys.argv[1])
why = [r for r in R if r["why"]]
tw = [r for r in why if r["stop"]]
flag = [r for r in why if r["flag"]]
mf, mr = Counter(r["stop"] for r in tw if r["flag"]), Counter(r["stop"] for r in tw)
months = sorted(m for m in mr if "2015-01" <= m <= "2026-12")
def share(sel):
    s = [r for r in tw if sel(r["stop"])]
    return {"reasons": len(s), "flagged": sum(r["flag"] for r in s),
            "share": round(sum(r["flag"] for r in s) / len(s), 4) if s else None}
top = mf.most_common(5)
anach = sorted([r for r in tw if r["flag"] and r["stop"] < "2020-01"], key=lambda r: r["stop"])
years = {y: share(lambda m, y=y: m[:4] == y) for y in map(str, range(2015, 2027))}
halves = {}
for y in range(2019, 2027):
    halves["%dH1" % y] = share(lambda m, y=y: m[:4] == str(y) and m[5:] <= "06")
    halves["%dH2" % y] = share(lambda m, y=y: m[:4] == str(y) and m[5:] > "06")
susp = [r for r in why if r["status"] == "SUSPENDED"]
out = {
    "data": "ClinicalTrials.gov API v2, processed 2026-10-22T09:00:04 (see fetch_log.json)",
    "stopped": len(R), "by_status": Counter(r["status"] for r in R),
    "with_reason": len(why), "without_reason": len(R) - len(why),
    "flagged_all": len(flag), "flagged_by_status": Counter(r["status"] for r in flag),
    "terminated_withdrawn_with_reason_and_stop_month": len(tw),
    "with_reason_no_stop_month": Counter(r["status"] for r in why if not r["stop"]),
    "first_flagged_month": min(mf) if mf else None, "top_months": top,
    "half_years": halves, "years": years,
    "anachronisms": {"count": len(anach), "by_stop_year": Counter(r["stop"][:4] for r in anach),
                     "nct": [r["nct"] for r in anach]},
    "suspended": {"with_reason": len(susp), "flagged": sum(r["flag"] for r in susp),
                  "flagged_by_last_update_year": Counter(r["lastupd"][:4] for r in susp if r["flag"])},
    "monthly": [{"m": m, "reasons": mr[m], "flagged": mf[m]} for m in months],
}
P = {
    "P1": {"registered": ">= 4000 flagged stated reasons", "value": len(flag), "held": len(flag) >= 4000},
    "P2": {"registered": "most-flagged stop month is 2020-03 or 2020-04", "value": top[0], "held": top[0][0] in ("2020-03", "2020-04")},
    "P3": {"registered": ">= 30 % flagged in 2020H1 (terminated, withdrawn)", "value": halves["2020H1"], "held": halves["2020H1"]["share"] >= 0.30},
    "P4": {"registered": ">= 1 % flagged in stop year 2025", "value": years["2025"], "held": years["2025"]["share"] >= 0.01},
    "P5": {"registered": ">= 10 anachronisms", "value": len(anach), "held": len(anach) >= 10},
}
out["predictions"] = P
json.dump(out, open("session1.json", "w"), indent=1)
for k, v in P.items(): print(k, v)
print("first", out["first_flagged_month"], "top", top)
for h, v in halves.items(): print(h, v)
print(out["by_status"], out["with_reason"], out["flagged_by_status"], out["suspended"])
print(out["anachronisms"]["by_stop_year"])
