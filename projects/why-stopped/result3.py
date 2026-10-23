"""Session 3: the blind re-reading against the first reading. Usage: python3 result3.py SHEETKEY (scratch sheet3_key.json)."""
import json, sys
key = json.load(open(sys.argv[1]))
first = {r[0]: r[3] for r in json.load(open("readings3.json"))["rows"]}
re = {x["n"]: x["read"] for x in json.load(open("reread3.json"))["reread"]}
grp = lambda c: "came" if c in "ESFU" else "went" if c == "W" else "neither"
items = [{"n": k["n"], "nct": k["nct"], "first": first[k["i"]], "reread": re[k["n"]]} for k in key]
cat = sum(x["first"] == x["reread"] for x in items)
cw = sum(grp(x["first"]) == grp(x["reread"]) for x in items)
out = {"category_agree": cat, "came_went_agree": cw, "of": len(items), "P6_held": cat >= 34,
       "disagreements": [x for x in items if x["first"] != x["reread"]]}
json.dump(out, open("result3.json", "w"), indent=1)
print(json.dumps(out, indent=1))
