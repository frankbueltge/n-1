"""Project 27 session 2, exploratory (not registered): silent rises per year against rated pairs per year;
the posting after a silent rise from a posted bridge; Poor exits that stay out. Reuses count2.py's reading.
Usage: python3 explore3.py DIR OUT.json"""
import json, sys, gzip
from collections import Counter
import count2

d, out = sys.argv[1:3]
by_bridge = {}
for y in range(1993, 2026):
    recs, _ = count2.read_year(f"{d}/AL{y % 100:02d}.txt")
    for b, r in recs.items():
        by_bridge.setdefault(b, {})[y] = r
pairs_y = Counter(); rises_y = Counter(); falls_y = Counter(); insp_y = Counter()
for b, s in by_bridge.items():
    ins = count2.inspections(s)
    for y, r in ins:
        insp_y[y] += 1
    for (y0, a), (y1, c) in zip(ins, ins[1:]):
        if a["L"] is None or c["L"] is None:
            continue
        pairs_y[y1] += 1
        if c["L"] < a["L"]:
            falls_y[y1] += 1
sil = json.load(gzip.open("session2-rises.json.gz", "rt"))
for x in sil:
    rises_y[x["y1"]] += 1
years = sorted(pairs_y)
posted = [x for x in sil if x["open0"] in ("P", "R")]
pe = [x for x in sil if x["poor_exit"]]
res = {
    "by_year": {str(y): {"inspections_beginning": insp_y[y], "rated_pairs_ending": pairs_y[y], "silent_rises": rises_y[y],
                         "falls": falls_y[y], "silent_rate": round(rises_y[y] / pairs_y[y], 4) if pairs_y[y] else None} for y in years},
    "odd_years": {"pairs": sum(pairs_y[y] for y in years if y % 2), "silent": sum(rises_y[y] for y in years if y % 2)},
    "even_years": {"pairs": sum(pairs_y[y] for y in years if not y % 2), "silent": sum(rises_y[y] for y in years if not y % 2)},
    "posted_before_open_after": dict(Counter(x["open1"] for x in posted)),
    "posted_before_L1_ge5": sum(1 for x in posted if x["L1"] >= 5),
    "posted_before_L1_ge5_still_posted": sum(1 for x in posted if x["L1"] >= 5 and x["open1"] in ("P", "R")),
    "poor_exits": len(pe),
    "poor_exits_with_later": sum(1 for x in pe if x["n_later"] > 0),
    "poor_exits_holds_out_of_poor": sum(1 for x in pe if x["n_later"] > 0 and not x["back_poor"]),
    "silent_rise_steps": dict(Counter(x["L1"] - x["L0"] for x in sil)),
    "bridges_with_silent_rise": len({x["b"] for x in sil}),
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "by_year"}, indent=1))
for y in years:
    r = res["by_year"][str(y)]; print(y, r["inspections_beginning"], r["rated_pairs_ending"], r["silent_rises"], r["falls"], r["silent_rate"])
