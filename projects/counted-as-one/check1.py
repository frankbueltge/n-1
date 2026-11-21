"""Registered check, project 26 session 1 (SELECTION.md): twelve overflows drawn with seed 20261121 from those with
2-40 activations, and the overflow with the most hours; each one's rows written as text and counted by awk alone
(check1.awk). Rows per company written as text and recounted by wc -l. Usage: python3 check1.py <start-stop dir>"""
import gzip, json, os, random, subprocess, sys, glob, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import count1
ssdir = sys.argv[1]
per = json.load(gzip.open("session1-per.json.gz", "rt"))
pool = sorted(r["uid"] for r in per if 2 <= r["acts"] <= 40)
rng = random.Random(20261121)
pick = rng.sample(pool, 12) + [max(per, key=lambda r: r["hours"])["uid"]]
want = {r["uid"]: r for r in per}
rows = {u: [] for u in pick}
tmp = tempfile.mkdtemp()
wc = {}
for f in sorted(glob.glob(os.path.join(ssdir, "*.csv")) + glob.glob(os.path.join(ssdir, "*.xlsx"))):
    txt = os.path.join(tmp, os.path.basename(f) + ".txt")
    with open(txt, "w") as out:
        for uid, _s, a, b in count1.read_startstop(f):
            if uid is None and a is None and b is None:
                continue  # blank spreadsheet row
            out.write(f"{uid}\t{a}\t{b}\n")
            u = str(uid).strip() if uid is not None else ""
            if u in rows:
                ha, hb = count1.hours_of(a), count1.hours_of(b)
                if ha is not None and hb is not None and hb >= ha and hb >= 0 and ha < count1.YEAR_H:
                    rows[u].append((max(ha, 0.0), min(hb, count1.YEAR_H)))
    wc[os.path.basename(f)] = int(subprocess.run(["wc", "-l", txt], capture_output=True, text=True).stdout.split()[0])
res = []
for u in pick:
    lines = "".join(f"{a:.6f} {b:.6f}\n" for a, b in sorted(rows[u]))
    o = subprocess.run(["awk", "-f", "check1.awk"], input=lines, capture_output=True, text=True).stdout.split()
    c, h = int(o[0]), float(o[1])
    ok = c == want[u]["count"] and abs(h - want[u]["hours"]) < 0.01
    res.append({"uid": u, "acts": len(rows[u]), "awk_count": c, "count": want[u]["count"], "awk_hours": h,
                "hours": want[u]["hours"], "ar_count": want[u].get("ar_count"), "held": ok})
s = json.load(open("session1.json"))
wc_ok = {k: {"wc": v, "count1_rows_nonblank": s["files"][k]["rows"] - (995359 if k.startswith("Southern") else 0),
             "held": v == s["files"][k]["rows"] - (995359 if k.startswith("Southern") else 0)} for k, v in wc.items()}
out = {"seed": 20261121, "pool": len(pool), "overflows": res, "held": sum(r["held"] for r in res), "of": len(res),
       "rows_per_file": wc_ok}
json.dump(out, open("check1.json", "w"), indent=1)
for r in res: print(r)
print(out["held"], "of", out["of"]); print(wc_ok)
