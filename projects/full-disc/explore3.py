"""Project 18, session 3: exploration, after the registered count (not registered; reported as exploration).
Reads sets3.json and session3.json (committed) and three type tables of the export; writes explore3.json:
the secondary types of the release groups in R, the formats of their media, and the addresses of the non-last media of sets
that are not at the frame.
Usage: python3 -I explore3.py <path to mbdump/>
"""
import json, sys
from collections import Counter

FRAME = 333000

def rows(d, table):
    for line in open(d + "/" + table, encoding="utf-8"):
        yield line.rstrip("\n").split("\t")

def main(d):
    s = json.load(open("sets3.json"))
    allr = s["sets"] + s["singles"]
    rgs = {r["release_group"] for r in allr}
    stype = {int(f[0]): f[1] for f in rows(d, "release_group_secondary_type")}
    types = {}
    for f in rows(d, "release_group_secondary_type_join"):
        g = int(f[0])
        if g in rgs: types.setdefault(g, set()).add(stype[int(f[1])])
    def kind(r):
        t = types.get(r["release_group"], set())
        return "Audiobook" if "Audiobook" in t else ("Spokenword" if "Spokenword" in t else ("other type" if t else "no type"))
    by_kind = Counter(kind(r) for r in allr)
    set_kind = Counter(kind(r) for r in s["sets"])
    fmts = Counter(m["format"] or "none" for r in s["sets"] for m in r["media"])
    other_nonlast = Counter()
    frame_at = Counter()
    for r in s["sets"]:
        n = len(r["media"])
        for i, m in enumerate(r["media"]):
            if m["address"] == FRAME: frame_at["last" if i == n - 1 else "not last"] += 1
            if i < n - 1 and m["address"] is not None and m["address"] != FRAME:
                other_nonlast[m["address"] // 75] += 1
    full_sets = sum(1 for r in s["sets"] if all(m["address"] == FRAME for m in r["media"][:-1]))
    out = {"releases_by_kind": dict(by_kind), "sets_by_kind": dict(set_kind), "set_media_formats": dict(fmts.most_common()),
           "sets_every_nonlast_at_frame": full_sets,
           "nonlast_other_address_seconds_top": [{"second": k, "media": v} for k, v in other_nonlast.most_common(15)],
           "frame_media_position": dict(frame_at)}
    json.dump(out, open("explore3.json", "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main(sys.argv[1].rstrip("/"))
