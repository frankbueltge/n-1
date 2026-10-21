"""Project 14, session 2: the registered predictions (SESSION2.md) and the rule check, from session2.json, check_key.json and
check_readings.json. Writes result2.json."""

import collections
import json

s = json.load(open("session2.json"))
key = {r["n"]: r["rule"] for r in json.load(open("check_key.json"))}
read = {r["n"]: r["reading"] for r in json.load(open("check_readings.json"))["readings"]}
same = {"T": "T", "V": "V", "mixed": "both", "none": "neither"}
tv = [n for n in key if key[n] in ("T", "V")]
agree = sum(same[key[n]] == read[n] for n in tv)
c = s["chains_by_bridge_class"]
both = {k: v["both_classified"] for k, v in c.items()}
P = [
    (7, "direct fra-rus pairs, both classified: disagreement at most 8 %", s["direct"]["disagree_share"], s["direct"]["disagree_share"] <= 0.08),
    (8, "eng-you chains: disagreement at least 35 %", c["eng-you"]["disagree_share"], c["eng-you"]["disagree_share"] >= 0.35),
    (9, "eng-you chains: at least three quarters of the independence baseline", c["eng-you"]["observed_over_baseline"],
     c["eng-you"]["observed_over_baseline"] >= 0.75),
    (10, "other-language bridges: disagreement at most 15 %", c["other"]["disagree_share"], c["other"]["disagree_share"] <= 0.15),
    (11, "epo-vi chains: disagreement at least 30 % (if 100 or more)", c["epo-vi"]["disagree_share"],
     c["epo-vi"]["both_classified"] >= 100 and c["epo-vi"]["disagree_share"] >= 0.30),
    (12, "eng-you is the largest class among chains with both ends classified", both["eng-you"], max(both, key=both.get) == "eng-you"),
]
out = {
    "rule_check": {"T_or_V_by_rule": len(tv), "agreeing_with_reading": agree, "threshold": 36, "rule_failed": agree < 36,
                   "all": {f"{k}->{v}": n for (k, v), n in collections.Counter((key[n], read[n]) for n in key).items()},
                   "estimate": True},
    "predictions": [{"id": f"P{i}", "text": t, "value": v, "held": bool(h)} for i, t, v, h in P],
}
json.dump(out, open("result2.json", "w"), indent=1)
print(json.dumps(out, indent=1))
