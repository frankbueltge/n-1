#!/usr/bin/env python3
"""Exploratory, after the check (project 23 session 1). For each late transition in explore1.json (helper run), the offset the
release before its first appearance already showed at that instant (count1.py's reader, full file, not window-limited).
If equal to the new offset, the late arrival re-timed a change already carried: a correction of the instant, not news.
usage: python3 -I explore1c.py explore1.json WORK2 OUT.json"""
import json, os, sys, collections, importlib.util
spec = importlib.util.spec_from_file_location("c", os.path.join(os.path.dirname(os.path.abspath(__file__)), "count1.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
r = json.load(open(sys.argv[1])); work = sys.argv[2]; order = list(r["release_dates"])
core = [x for x in r["rows"] if not x["with_zone"] and not x["censored"]]
def off_at(rel, zone, t):
    p = os.path.join(work, "out", rel, zone)
    if not os.path.exists(p): return None
    import struct
    tr = c.read_tzif(p); b = None
    for tt, o in tr:
        if tt <= t: b = o
    return b
out = collections.Counter(); rows = []
for x in core:
    if x["lead_days"] >= 0: continue
    prev = order[order.index(x["first"]) - 1]
    o = off_at(prev, x["zone"], x["t"])
    kind = ("past" if x["lead_days"] < -365 else "news") + ("/retimed" if o == x["offset"] else "/new_offset")
    out[kind] += 1
    rows.append({"zone": x["zone"], "t": x["t"], "first": x["first"], "lead_days": x["lead_days"], "prev_offset_at_t": o, "kind": kind})
json.dump({"counts": dict(out), "rows": rows}, open(sys.argv[3], "w"), indent=0)
print(dict(out))
