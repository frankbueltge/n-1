"""Exploratory, after the registered count: the 95 anachronisms read by eye and sorted into what they name. -> anach1.json
No reason text is written out; the sort is by rule on the text, checked by reading all 95 (session 1, LOG.md)."""
import json, re, sys
from lib import load
R = load(sys.argv[1])
A = sorted([r for r in R if r["why"] and r["stop"] and r["flag"] and r["stop"] < "2020-01"], key=lambda r: r["stop"])
items = []
for r in A:
    w = r["why"]
    if re.search(r"covidien", w, re.I) and not re.search(r"covid(?!ien)", w, re.I):
        kind = "not the pandemic (a company's name)"
    elif re.search(r"covid|sars-?cov|corona", w, re.I) or (r["stop"] >= "2019-01" and re.search(r"pandemi|lockdown|epidemi", w, re.I)):
        kind = "COVID-19"
    elif re.search(r"h1n1|influenza|flu|pandemic vaccine", w, re.I):
        kind = "an influenza pandemic"
    else:
        kind = "unsorted"
    items.append({"nct": r["nct"], "stop": r["stop"], "last_update": r["lastupd"], "status": r["status"], "names": kind})
from collections import Counter
json.dump({"items": items, "by_kind": Counter(i["names"] for i in items)}, open("anach1.json", "w"), indent=1)
print(Counter(i["names"] for i in items))
gap = sorted((int(i["last_update"][:4]) * 12 + int(i["last_update"][5:]) - int(i["stop"][:4]) * 12 - int(i["stop"][5:])) for i in items if i["names"] == "COVID-19")
print("months stop->lastupd median", gap[len(gap)//2], "min", gap[0], "max", gap[-1])
