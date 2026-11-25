"""Project 27 session 1, exploratory (not registered): how far does a structure number carry a bridge from year to year?
Usage: python3 explore1.py DIR OUT.json PER.json.gz"""
import gzip, json, os, sys
from count1 import read_year

d, out, perp = sys.argv[1:4]
years = list(range(1992, 2026))
ids = {}
for y in years:
    recs, _ = read_year(os.path.join(d, f"AL{y % 100:02d}.txt"), y, "01")
    ids[y] = set(recs)
res = {"per_year": {}, "consecutive": {}}
for y in years:
    res["per_year"][str(y)] = len(ids[y])
for a, b in zip(years, years[1:]):
    res["consecutive"][f"{a}-{b}"] = {"kept": len(ids[a] & ids[b]), "gone": len(ids[a] - ids[b]), "new": len(ids[b] - ids[a])}
allyrs = set.intersection(*ids.values())
res["in_all_34"] = len(allyrs)
per = json.load(gzip.open(perp))
res["bridge_006850_L"] = per.get("006850", {}).get("L")
res["bridge_006850_spells"] = per.get("006850", {}).get("spells")
# span of presence: first..last year among numbers present in 2025
span = {}
for b in ids[2025]:
    f = min(y for y in years if b in ids[y])
    span[f] = span.get(f, 0) + 1
res["first_year_of_2025_numbers"] = {str(k): v for k, v in sorted(span.items())}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
