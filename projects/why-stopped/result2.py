"""The check of session 2, scored after the key was opened (readings2.json committed 9d82b54 first). -> result2.json"""
import json
K = {k["i"]: k for k in json.load(open("key2.json"))}
R = {r["i"]: r for r in json.load(open("readings2.json"))["readings"]}
told = [i for i in K if R[i]["month"] != "cannot tell"]
dated_agree = sum((K[i]["line_month"] is not None) == (R[i]["month"] != "none") for i in told)
both = [i for i in told if K[i]["line_month"] and R[i]["month"] != "none"]
month_agree = sum(K[i]["line_month"] == R[i]["month"] for i in both)
dis = [{"i": i, "nct": K[i]["nct"], "rule": K[i]["line_month"], "reading": R[i]["month"], "note": R[i].get("note")}
       for i in told if (K[i]["line_month"] or "none") != R[i]["month"]]
out = {"told": len(told), "agree_dated": dated_agree, "both_dated": len(both), "agree_month": month_agree, "disagreements": dis,
       "P6": {"registered": "the dating rule agrees with the reading on dated vs none at >= 36 of those told",
              "value": dated_agree, "held": dated_agree >= 36}}
json.dump(out, open("result2.json", "w"), indent=1)
print(json.dumps(out, indent=1))
