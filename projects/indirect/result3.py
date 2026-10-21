"""Project 14, session 3: the key opened against the readings (SESSION3.md, P13-P18). Writes result3.json."""

import collections
import json

import lib2

sheet = {r["n"]: r for r in json.load(open("sheet3.json"))}
read = {r["n"]: r for r in json.load(open("read3.json"))["readings"]}
key = json.load(open("key3.json"))
by_id = {r["id"]: r["n"] for r in key["rows"]}
cls = {r["id"]: read[r["n"]]["reading"] for r in key["rows"]}

pairs = collections.Counter()
both_sides = 0
for g in key["groups"]:
    t = g["translations"]
    links = {tuple(l) for l in g["links"]}
    tv = [x for x in t if cls[x] in ("T", "V")]
    if any(cls[x] == "T" for x in t) and any(cls[x] == "V" for x in t):
        both_sides += 1
    for i, a in enumerate(tv):
        for b in tv[i + 1:]:
            kind = "agree" if cls[a] == cls[b] else "disagree"
            pairs[(kind, (min(a, b), max(a, b)) in links)] += 1


def share(kind):
    n = pairs[(kind, True)] + pairs[(kind, False)]
    return {"pairs": n, "linked": pairs[(kind, True)], "linked_share": round(pairs[(kind, True)] / n, 4) if n else None}


agree, disagree = share("agree"), share("disagree")
counts = collections.Counter(r["reading"] for r in read.values())
readable = len(read) - counts["cannot"]
rule = {"agree": 0, "n": 0, "misses": []}
for n, r in sheet.items():
    if r["lang"] in ("fra", "rus"):
        c = lib2.address(r["lang"], r["text"])
        if c in (lib2.T, lib2.V):
            rule["n"] += 1
            want = "T" if c == lib2.T else "V"
            if read[n]["reading"] == want:
                rule["agree"] += 1
            else:
                rule["misses"].append(n)
langs = len({r["lang"] for r in sheet.values()})
ratio = agree["linked_share"] / disagree["linked_share"] if disagree["linked_share"] else None
P = {
    "P13": {"registered": "agreeing pairs linked at least 5x as often as disagreeing; disagreeing linked at most 5 %",
            "agree": agree, "disagree": disagree, "ratio": round(ratio, 2) if ratio else "disagreeing pairs never linked",
            "held": (ratio is None or ratio >= 5) and disagree["linked_share"] <= 0.05},
    "P14": {"registered": "at least 10 of 30 sentences have a T and a V", "observed": both_sides, "held": both_sides >= 10},
    "P15": {"registered": "at most 10 % cannot read", "observed": counts["cannot"], "of": len(read), "held": counts["cannot"] <= 0.10 * len(read)},
    "P16": {"registered": "reading agrees with the checked French/Russian rule on at least 90 %", "observed": rule,
            "held": rule["n"] >= 20 and rule["agree"] >= 0.9 * rule["n"]},
    "P17": {"registered": "at most 40 % of readable unmarked", "observed": counts["unmarked"], "of": readable,
            "held": counts["unmarked"] <= 0.40 * readable},
    "P18": {"registered": "at least 25 languages", "observed": langs, "held": langs >= 25},
}
out = {"estimate": True, "note": "readings are a machine's (read3.json); links and groups are the export's", "readings": dict(counts),
       "predictions": P}
json.dump(out, open("result3.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
