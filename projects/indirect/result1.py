"""Session 1: the readings against the key, and the six predictions (writes result1.json)."""
import collections, json

s1 = json.load(open("session1.json"))
key = {x["n"]: x for x in json.load(open("key.json"))}
rd = {x["n"]: x for x in json.load(open("readings.json"))["readings"]}
br = json.load(open("bridges.json"))
tab = {k: collections.Counter(rd[n]["reading"] for n in rd if key[n]["kind"] == k) for k in ("indirect", "direct")}
def lossrate(k):
    t = tab[k]; readable = sum(t.values()) - t["cannot read"]
    return (t["shifted"] + t["different"]) / readable, readable
ind, ind_n = lossrate("indirect"); dr, dr_n = lossrate("direct")
eng = sum(1 for n in key if key[n]["kind"] == "indirect" and key[n]["bridge"]["lang"] == "eng") / 150
low = {k: sum(1 for n in rd if key[n]["kind"] == k and rd[n]["confidence"] == "low") for k in tab}
P = [
    ("P1", "indirect pairs at least five times direct", s1["ratio_indirect_to_direct"], s1["ratio_indirect_to_direct"] >= 5),
    ("P2", "bridge English in at least 40 % of chains", round(eng, 3), eng >= 0.40),
    ("P3", "indirect shifted or different at least 15 %", round(ind, 3), ind >= 0.15),
    ("P4", "direct loss at most half the indirect", round(dr, 3), dr <= ind / 2),
    ("P5", "indirect different at most 5 %", round(tab["indirect"]["different"] / ind_n, 3), tab["indirect"]["different"] / ind_n <= 0.05),
    ("P6", "cannot read at most 10 % of 200", (tab["indirect"]["cannot read"] + tab["direct"]["cannot read"]) / 200,
     (tab["indirect"]["cannot read"] + tab["direct"]["cannot read"]) / 200 <= 0.10),
]
out = {"estimate": "readings are a machine's; counts of the graph are exact", "table": tab, "indirect_loss": round(ind, 4), "indirect_readable": ind_n,
       "direct_loss": round(dr, 4), "direct_readable": dr_n, "low_confidence": low, "loci": br["counts"],
       "predictions": [{"id": a, "text": b, "value": c, "held": d} for a, b, c, d in P]}
json.dump(out, open("result1.json", "w"), indent=1)
print(json.dumps(out, indent=1))
