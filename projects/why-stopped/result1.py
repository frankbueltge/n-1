"""The check of session 1, scored after the key was opened (readings.json committed 0e2aebe first). -> result1.json"""
import json
K = {k["i"]: k for k in json.load(open("key.json"))}
R = {r["i"]: r for r in json.load(open("readings.json"))["readings"]}
told = [i for i in K if R[i]["reading"] != "cannot tell"]
words = sum(K[i]["flag"] == (R[i]["reading"] in ("pandemic", "other")) for i in told)
event = sum(K[i]["flag"] == (R[i]["reading"] == "pandemic") for i in told)
dis = [{"i": i, "nct": K[i]["nct"], "rule": K[i]["flag"], "reading": R[i]["reading"], "stop": K[i]["stop"],
        "note": R[i].get("note")} for i in told if K[i]["flag"] != (R[i]["reading"] == "pandemic")]
out = {"told": len(told), "agree_words": words, "agree_event": event, "disagreements_event": dis,
       "P6": {"registered": "rule agrees with the reading for the words at >= 36 of those told", "value": words, "held": words >= 36},
       "found_after_key": "item 24 (NCT02890797): its stop month is 2020-02, yet its reason dates the suspension of inclusions to "
                          "18 March 2020 -- the reason is later than the stop it explains (see session1.json anachronisms)"}
json.dump(out, open("result1.json", "w"), indent=1)
print(words, event, len(told))
