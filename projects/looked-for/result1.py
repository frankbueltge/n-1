"""Readings (readings.json) against GBIF's interpreted status (key.json)."""
import json
R = {r["item"]: r for r in json.load(open("projects/looked-for/readings.json"))["readings"]}
K = {k["item"]: k for k in json.load(open("projects/looked-for/key.json"))}
rows, agree, tell = [], 0, 0
for i in sorted(K):
    g, m = K[i]["status"], R[i]["reading"]
    ok = None if m == "cannot tell" else (m.upper() == g)
    if ok is not None:
        tell += 1; agree += ok
    rows.append({"item": i, "gbif": g, "reading": m, "agree": ok, "issues": K[i]["issues"]})
out = {"tellable": tell, "agree": agree, "rows": rows,
       "cannot_tell_gbif": [K[i]["status"] for i in K if R[i]["reading"] == "cannot tell"],
       "status_issues": {i: [x for x in K[i]["issues"] if "STATUS" in x] for i in K if any("STATUS" in x for x in K[i]["issues"])}}
json.dump(out, open("projects/looked-for/result1.json", "w"), indent=1)
print(tell, agree, out["cannot_tell_gbif"], out["status_issues"])
for r in rows:
    if r["agree"] is False: print("disagree", r)
