#!/usr/bin/env python3
"""Project 23 session 1: the registered check (SELECTION.md). zdump -v, not count1.py's TZif reader, on the release before
the first appearance and on the first appearance, for twelve late transitions drawn with seed 20261107 from session1.json.
usage: python3 -I check1.py session1.json WORKDIR OUT.json"""
import json, random, subprocess, sys, time, calendar, os
r = json.load(open(sys.argv[1])); work = sys.argv[2]
order = list(r["release_dates"])
late = [x for x in r["rows"] if not x["with_zone"] and not x["censored"] and x["lead_days"] < 0]
random.seed(20261107)
sample = random.sample(late, min(12, len(late)))
def offset_at(rel, zone, t):
    y = time.gmtime(t).tm_year
    out = subprocess.run(["zdump", "-v", "-c", "%d,%d" % (y - 1, y + 2), os.path.join(work, "out", rel, zone)],
                         capture_output=True, text=True).stdout
    best = None
    for line in out.splitlines():
        p = line.split()
        if len(p) < 13 or p[6] != "UT":
            continue
        ut = calendar.timegm(time.strptime("%s %s %s %s" % (p[2], p[3], p[4], p[5]), "%b %d %H:%M:%S %Y"))
        off = int([q for q in p if q.startswith("gmtoff=")][0][7:])
        if ut <= t:
            best = off
    return best
res = []
for x in sample:
    i = order.index(x["first"]); prev = order[i - 1]
    before = offset_at(prev, x["zone"], x["t"]); after = offset_at(x["first"], x["zone"], x["t"])
    res.append({"zone": x["zone"], "t": x["t"], "offset": x["offset"], "prev_release": prev, "first": x["first"],
                "offset_prev_release": before, "offset_first": after,
                "holds": after == x["offset"] and before != x["offset"]})
n = sum(r_["holds"] for r_ in res)
json.dump({"n": len(res), "holds": n, "P11": n >= 11, "rows": res}, open(sys.argv[3], "w"), indent=1)
print(n, "of", len(res)); [print(q) for q in res]
