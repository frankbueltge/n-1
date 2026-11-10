#!/usr/bin/env python3
"""Project 23 session 3: the registered check P11 (SESSION3.md). Eight past-found-wrong episodes drawn with seed 20261110 from
session2.json. For each, tau = t0 + min(1800, (t1 - t0)/2); the release current at t0 (rel), the correcting release (corr) and 2026f,
fetched again and compiled with zic and session 1's helper, read with zdump -v (not count2's reader). Holds if rel shows count2's
shown at tau, 2026f shows count2's final, they differ, and corr shows the final's offset.
usage: python3 -I check3.py session2.json WORKDIR OUT.json"""
import calendar, json, os, random, subprocess, sys, tarfile, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REGION = ["africa", "antarctica", "asia", "australasia", "europe", "northamerica", "southamerica", "etcetera"]
r = json.load(open(sys.argv[1])); work = sys.argv[2]
random.seed(20261110)
sample = random.sample([e for e in r["episodes_rows"] if e["kind"] == "past"], 8)
def fname(rel):
    return "tzdata%s.tar.gz" % rel
def build(rel):
    out = os.path.join(work, "out", rel)
    if os.path.isdir(out):
        return out
    src = os.path.join(work, "src", rel); os.makedirs(src, exist_ok=True); os.makedirs(out, exist_ok=True)
    tp = os.path.join(work, fname(rel))
    if not os.path.exists(tp):
        urllib.request.urlretrieve("https://data.iana.org/time-zones/releases/" + fname(rel), tp)
    with tarfile.open(tp) as tf:
        tf.extractall(src, filter="data")
    files = [f for f in REGION if os.path.exists(os.path.join(src, f))]
    env = dict(os.environ, PATH=os.path.join(HERE, "helper") + os.pathsep + os.environ.get("PATH", ""))
    subprocess.run(["zic", "-b", "fat", "-d", out] + files, cwd=src, capture_output=True, env=env, check=True)
    return out
def offset_at(rel, zone, t):
    y = time.gmtime(t).tm_year
    txt = subprocess.run(["zdump", "-v", "-c", "%d,%d" % (max(y - 60, 1900), y + 2), os.path.join(build(rel), zone)],
                         capture_output=True, text=True).stdout
    best = None
    for line in txt.splitlines():
        p = line.split()
        if len(p) < 13 or p[6] != "UT" or "gmtoff=" not in line:
            continue
        try:
            ut = calendar.timegm(time.strptime("%s %s %s %s" % (p[2], p[3], p[4], p[5]), "%b %d %H:%M:%S %Y"))
        except ValueError:
            continue
        if ut <= t:
            best = int([q for q in p if q.startswith("gmtoff=")][0][7:])
    return best
rows = []
for e in sample:
    tau = e["t0"] + int(min(1800, (e["t1"] - e["t0"]) / 2))
    a, c, f = offset_at(e["rel"], e["zone"], tau), offset_at(e["corr"], e["zone"], tau), offset_at("2026f", e["zone"], tau)
    rows.append({"zone": e["zone"], "tau": tau, "rel": e["rel"], "corr": e["corr"], "zdump_rel": a, "zdump_corr": c,
                 "zdump_final": f, "count2_shown": e["shown"], "count2_final": e["final"],
                 "holds": a == e["shown"] and f == e["final"] and a != f and c == f})
n = sum(x["holds"] for x in rows)
json.dump({"n": len(rows), "holds": n, "P11": n >= 7, "rows": rows}, open(sys.argv[3], "w"), indent=1)
print(n, "of", len(rows)); [print(x) for x in rows]
