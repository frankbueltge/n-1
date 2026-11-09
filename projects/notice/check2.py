#!/usr/bin/env python3
"""Project 23 session 2: the registered check (SESSION2.md). Twelve episodes drawn with seed 20261109 from session2.json; at each
midpoint, zdump -v (not count2's TZif reader) on the release current at that instant and on the final; holds if both offsets equal
count2's (shown, final) and differ.
usage: python3 -I check2.py session2.json WORKDIR OUT.json"""
import calendar, json, os, random, subprocess, sys, time
r = json.load(open(sys.argv[1])); work = sys.argv[2]
dates = r["release_dates"]; order = list(dates)
ts = lambda s: calendar.timegm(tuple(map(int, s.split("-"))) + (0, 0, 0))
random.seed(20261109)
sample = random.sample(r["episodes_rows"], 12)
def offset_at(rel, zone, t):
    y = time.gmtime(t).tm_year
    out = subprocess.run(["zdump", "-v", "-c", "%d,%d" % (max(y - 30, 1900), y + 2), os.path.join(work, "out", rel, zone)],
                         capture_output=True, text=True).stdout
    best = None
    for line in out.splitlines():
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
res = []
for e in sample:
    tm = (e["t0"] + e["t1"]) // 2
    cur = [n for n in order if ts(dates[n]) <= tm][-1]
    a, b = offset_at(cur, e["zone"], tm), offset_at(order[-1], e["zone"], tm)
    res.append({"zone": e["zone"], "kind": e["kind"], "t_mid": tm, "current": cur, "zdump_current": a, "zdump_final": b,
                "count2_shown": e["shown"], "count2_final": e["final"], "holds": a == e["shown"] and b == e["final"] and a != b})
n = sum(x["holds"] for x in res)
json.dump({"n": len(res), "holds": n, "P11": n >= 11, "rows": res}, open(sys.argv[3], "w"), indent=1)
print(n, "of", len(res)); [print(x) for x in res]
