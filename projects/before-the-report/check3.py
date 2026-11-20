"""Project 25 session 3: the registered check (SESSION3.md). A second tool: jq extracts every record's event_id and dates, awk takes
each event's minimum dates and counts, for drawn days, the events begun and not yet listed; GNU date turns the work's day numbers
into calendar dates. Compared with the work's data file.

Usage: python3 -I check3.py <dir with food.json drug.json device.json and work-data.json> <out.json>
"""
import json, sys, random, subprocess, datetime

CENTRES = ["food", "drug", "device"]


def sh(cmd):
    return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True).stdout


def main(src, out):
    data = json.load(open(f"{src}/work-data.json"))
    rnd = random.Random(20261120)
    res = {"events": [], "days": []}
    # one TSV per centre: event_id, initiation, report (jq), then awk minimum per event
    for c in CENTRES:
        sh(f"jq -r '.results[] | [.event_id, .recall_initiation_date, .report_date] | @tsv' {src}/{c}.json > {src}/{c}.tsv")
        sh(f"awk -F'\\t' '{{ if (!($1 in s) || $2 < s[$1]) s[$1]=$2; if (!($1 in l) || $3 < l[$1]) l[$1]=$3 }} "
           f"END {{ for (e in s) print e\"\\t\"s[e]\"\\t\"l[e] }}' {src}/{c}.tsv > {src}/{c}.ev.tsv")
    for ci, c in enumerate(CENTRES):
        rows = [r for r in data["rows"] if r[2] == ci]
        for r in rnd.sample(rows, 4):
            S = sh(f"date -d '{data['epoch']} +{r[0]} days' +%Y%m%d").strip()
            L = sh(f"date -d '{data['epoch']} +{r[1]} days' +%Y%m%d").strip()
            line = sh(f"awk -F'\\t' '$1==\"{r[5]}\"' {src}/{c}.ev.tsv").strip().split("\t")
            res["events"].append({"centre": c, "event_id": r[5], "work": [S, L], "jq_awk": line[1:], "ok": line[1:] == [S, L]})
    # three days in 2025 (as registered) and three in 2024 (a year the work shows; added, not registered)
    for y in (2025, 2024):
        start = datetime.date(y, 1, 1)
        for k in sorted(rnd.sample(range(365), 3)):
            t = (start + datetime.timedelta(days=k)).strftime("%Y%m%d")
            n = int(sh(f"cat {src}/food.ev.tsv {src}/drug.ev.tsv {src}/device.ev.tsv | "
                       f"awk -F'\\t' '$2 > \"20000000\" && $3 >= $2 && $2 <= \"{t}\" && $3 > \"{t}\" {{n++}} END {{print n+0}}'").strip())
            tn = (start + datetime.timedelta(days=k) - datetime.date.fromisoformat(data["epoch"])).days
            py = sum(1 for r in data["rows"] if r[0] <= tn < r[1])
            work = data["backlog"].get(str(y), [None] * 366)[k]
            res["days"].append({"day": t, "awk": n, "from_work_rows": py, "work_backlog": work,
                                "ok": n == py and (work is None or work == n), "registered": y == 2025})
    reg = res["events"] + [x for x in res["days"] if x["registered"]]
    res["registered_ok"] = f"{sum(x['ok'] for x in reg)} of {len(reg)}"
    res["all_ok"] = f"{sum(x['ok'] for x in res['events'] + res['days'])} of {len(res['events']) + len(res['days'])}"
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:3])
