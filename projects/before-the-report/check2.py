"""Project 25 session 2 check (SESSION2.md): 12 events drawn with seed 20261119 (4 per centre, from public and register-first
events) and the 3 longest register-first drug Class I events. For each, jq selects the event's records by event_id from the unzipped
file (notice string, class, two dates); GNU date computes each record's wait; the event holds if the group, the gravest class and the
smallest wait equal the count's. Python only draws, groups the jq strings by the registered rule and compares.
Second count: records whose notice is exactly "Press Release", per centre, by jq alone.
Usage: python3 -I check2.py <raw dir> <per2.json> <out.json>"""
import json, random, subprocess, sys
raw, per_path, out = sys.argv[1:4]
ev = json.load(open(per_path))
s2 = json.load(open("session2.json"))
rng = random.Random(20261119)
draw = []
for c in ["food", "drug", "device"]:
    draw += rng.sample([e for e in ev if e["centre"] == c and e["notice"] in ("public", "consignees") and e["W"] is not None], 4)
draw += [next(e for e in ev if e["centre"] == "drug" and e["event_id"] == l["event_id"]) for l in s2["longest_register_first_drug_class1"]]
def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
def grp(s):
    t = s.strip().lower()
    if t in ("", "n/a"): return "unrecorded"
    if t == "press release": return "public"
    if t == "other" or t.startswith("two or more of the following"): return "ambiguous"
    if "press release" in t: return "listed-with-press"
    return "consignees"
order = ["public", "listed-with-press", "ambiguous", "consignees", "unrecorded"]
rank = {"Class I": 0, "Class II": 1, "Class III": 2}
rows, ok = [], 0
for e in draw:
    q = (f'jq -r \'.results[]|select(.event_id=="{e["event_id"]}")|[(.initial_firm_notification//""),.classification,'
         f'.recall_initiation_date,.report_date]|join("\\t")\' {raw}/{e["centre"]}.json')
    lines = [l.split("\t") for l in sh(q).splitlines()]
    ws = []
    for n, k, i, r in lines:
        dd = sh(f'echo $(( ( $(date -u -d {r} +%s) - $(date -u -d {i} +%s) ) / 86400 ))')
        if dd.lstrip("-").isdigit(): ws.append(int(dd))
    gs = {grp(l[0]) for l in lines}
    g = next((x for x in order if x in gs), None)
    k = min((l[1] for l in lines), key=lambda x: rank.get(x, 3)) if lines else None
    w = min(ws) if ws else None
    holds = bool(lines) and len(lines) == e["records"] and g == e["notice"] and k == e["class"] and w == e["W"]
    ok += holds
    rows.append({"centre": e["centre"], "event_id": e["event_id"], "jq_records": len(lines), "jq_strings": sorted({l[0] for l in lines}),
                 "jq_group": g, "jq_class": k, "date_W": w, "count": [e["records"], e["notice"], e["class"], e["W"]], "holds": holds})
second = {}
for c in ["food", "drug", "device"]:
    n = int(sh(f'jq \'[.results[]|select(.initial_firm_notification=="Press Release")]|length\' {raw}/{c}.json'))
    second[c] = {"jq": n, "count": s2["record_exact_press_release"][c], "holds": n == s2["record_exact_press_release"][c]}
res = {"held": ok, "of": len(rows), "rows": rows, "second_count": second}
json.dump(res, open(out, "w"), indent=1)
print(ok, "of", len(rows)); print(json.dumps(second))
for r in rows:
    print(r["holds"], r["centre"], r["event_id"], r["jq_records"], r["jq_group"], r["jq_class"], r["date_W"], r["count"], r["jq_strings"])
