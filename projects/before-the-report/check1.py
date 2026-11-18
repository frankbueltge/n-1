"""Project 25 session 1 check (SELECTION.md): 12 records drawn with seed 20261118 (4 per centre) and the 3 longest waits;
for each, jq selects the record by recall number from the unzipped file and GNU date computes the wait. Python only draws and
compares. Second count: records per centre and records with W < 0 by jq alone."""
import json, random, subprocess, sys
raw, per_path, out = sys.argv[1:4]
per = json.load(open(per_path))
s1 = json.load(open("session1.json"))
rng = random.Random(20261118)
draw = []
for c in ["food", "drug", "device"]:
    draw += rng.sample([p for p in per if p["centre"] == c and p["W"] is not None], 4)
draw += [next(p for p in per if p["recall_number"] == l["recall_number"] and p["centre"] == l["centre"]) for l in s1["longest"]]
def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
rows, ok = [], 0
for p in draw:
    q = f'jq -r \'.results[]|select(.recall_number=="{p["recall_number"]}")|.recall_initiation_date+" "+.report_date\' {raw}/{p["centre"]}.json'
    got = sh(q).splitlines()
    i, r = got[0].split() if got else ("", "")
    dd = sh(f'echo $(( ( $(date -u -d {r} +%s) - $(date -u -d {i} +%s) ) / 86400 ))')
    w = int(dd) if dd.lstrip("-").isdigit() else None
    holds = len(got) >= 1 and i == p["init"] and r == p["report"] and w == p["W"]
    ok += holds
    rows.append({"centre": p["centre"], "recall_number": p["recall_number"], "jq_lines": len(got), "init": i, "report": r,
                 "date_W": w, "count_W": p["W"], "holds": holds})
second = {}
for c in ["food", "drug", "device"]:
    n = int(sh(f"jq '.results|length' {raw}/{c}.json"))
    neg = int(sh(f"jq '[.results[]|select(.report_date < .recall_initiation_date)]|length' {raw}/{c}.json"))
    second[c] = {"jq_records": n, "count_records": s1["meta"][c]["records"], "jq_neg": neg,
                 "count_neg": s1["by_centre"][c]["neg"], "holds": n == s1["meta"][c]["records"] and neg == s1["by_centre"][c]["neg"]}
res = {"held": ok, "of": len(rows), "rows": rows, "second_count": second}
json.dump(res, open(out, "w"), indent=1)
print(ok, "of", len(rows)); print(json.dumps(second))
for r in rows:
    if not r["holds"]: print("FAIL", r)
