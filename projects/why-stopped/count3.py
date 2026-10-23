"""Session 3 registered count: the readings of every flagged reason against the register's dates. Usage: python3 count3.py RAWDIR.
Writes session3.json (counts and months only; no reason text)."""
import collections, json, statistics, sys
import lib3

rows = {r["nct"]: r for r in lib3.load(sys.argv[1])}
read = json.load(open("readings3.json"))["rows"]
CAME, WENT = set("ESFU"), {"W"}
grp = lambda c: "came" if c in CAME else "went" if c in WENT else "of" if c == "C" else "neither"
mi = lambda m: int(m[:4]) * 12 + int(m[5:7]) - 1
im = lambda k: "%04d-%02d" % (k // 12, k % 12 + 1)
cat = collections.Counter(r[3] for r in read)
n = len(read)
items = []
for i, nct, sha, c in read:
    s = rows[nct]
    items.append({"nct": nct, "read": c, "group": grp(c), "status": s["status"], "stop": s["stop"], "lastupd": s["lastupd"]})
came = [x for x in items if x["group"] == "came"]
went = [x for x in items if x["group"] == "went"]
med = lambda xs: im(int(statistics.median([mi(x["stop"]) for x in xs if x["stop"]])))
mc, mw = med(came), med(went)
monthly = collections.defaultdict(lambda: collections.Counter())
for x in items:
    if x["stop"]:
        monthly[x["stop"]][x["read"]] += 1
susp = collections.defaultdict(lambda: collections.Counter())
for x in items:
    if x["status"] == "SUSPENDED":
        susp[x["lastupd"][:4]][x["group"]] += 1
pre = [x for x in items if x["stop"] and x["stop"] < "2020-01"]
out = {
    "data": "ClinicalTrials.gov API v2, processed 2026-10-23T09:00:04 (fetch_log3.json)",
    "flagged": n, "flagged_session1": 2642,
    "by_category": dict(cat.most_common()),
    "by_group": dict(collections.Counter(x["group"] for x in items)),
    "came_by_mechanism": {k: cat[k] for k in "ESFU"},
    "median_stop_came": mc, "median_stop_went": mw, "median_gap_months": mi(mw) - mi(mc),
    "with_stop_month": {"came": sum(1 for x in came if x["stop"]), "went": sum(1 for x in went if x["stop"])},
    "pre2020_by_category": dict(collections.Counter(x["read"] for x in pre)),
    "suspended_by_lastupd_year": {y: dict(c) for y, c in sorted(susp.items())},
    "by_status_group": {st: dict(collections.Counter(x["group"] for x in items if x["status"] == st)) for st in ("TERMINATED", "WITHDRAWN", "SUSPENDED")},
    "monthly": [{"m": m, **dict(c)} for m, c in sorted(monthly.items())],
    "marks": [[x["nct"], x["read"], x["status"][0], x["stop"] or "", x["lastupd"]] for x in items],
}
p = [
    {"n": 1, "registered": "at least 70 % of flagged lines are came (E, S, F or U)", "value": round(100 * len(came) / n, 1)},
    {"n": 2, "registered": "among came, E is the most common", "value": max("ESFU", key=lambda k: cat[k])},
    {"n": 3, "registered": "median stop month of went at least 12 months after that of came", "value": [mc, mw, mi(mw) - mi(mc)]},
    {"n": 4, "registered": "N at most 3 % of flagged lines", "value": round(100 * cat["N"] / n, 2)},
    {"n": 5, "registered": "at least 100 lines are went", "value": len(went)},
]
p[0]["held"] = p[0]["value"] >= 70; p[1]["held"] = p[1]["value"] == "E"; p[2]["held"] = p[2]["value"][2] >= 12
p[3]["held"] = p[3]["value"] <= 3; p[4]["held"] = p[4]["value"] >= 100
r3 = json.load(open("result3.json"))
p.append({"n": 6, "registered": "blind re-reading agrees on category in at least 34 of 40", "value": r3["category_agree"], "held": r3["P6_held"]})
out["predictions"] = p
out["cannot_place"] = {"?": cat["?"], "share": round(100 * cat["?"] / n, 2), "put_back_threshold_pct": 10}
json.dump(out, open("session3.json", "w"), indent=1)
for k, v in out.items():
    if k not in ("monthly", "marks"):
        print(k, v)
