"""Project 27, session 3: the data of the work *Set Aside* (definitions: SESSION3.md). Standard library only.

Usage: python3 build5.py RISES.json.gz PER.json.gz EXPLORE3.json OUT_DATA.json OUT_SESSION.json
"""
import gzip
import json
import os
import sys
from collections import Counter

FIRST, LAST = 1993, 2025


def outcome(r):
    if r["holds"]:
        return "h"
    if r["falls_back"]:
        return "f"
    return "o"


def main(rises_p, per_p, ex_p, out_data, out_sess):
    rises = json.load(gzip.open(rises_p, "rt"))
    per = json.load(gzip.open(per_p, "rt"))
    ex = json.load(open(ex_p))
    order = sorted({r["b"] for r in rises})
    idx = {b: i for i, b in enumerate(order)}
    lines = [per[b]["L"][1:] for b in order]  # 1993..2025, 33 characters
    strokes = []
    agree = 0
    for r in sorted(rises, key=lambda r: (r["y1"], r["b"], r["y0"])):
        i = idx[r["b"]]
        line = lines[i]
        if line[r["y0"] - FIRST] == str(r["L0"]) and line[r["y1"] - FIRST] == str(r["L1"]):
            agree += 1
        strokes.append([i, r["y0"], r["y1"], r["L0"], r["L1"], outcome(r)])
    rate = {y: v["silent_rate"] for y, v in ex["by_year"].items()}
    data = {
        "about": "Set Aside (Remainder, 2026). Silent rises of the lowest condition code in Alabama's National Bridge "
                 "Inventory files 1993-2025, from projects/the-lowest-code/session2-rises.json.gz and session1-per.json.gz. "
                 "Stroke = [bridge, y0, y1, code before, code after, h=held|f=fell back|o=other]. Line = lowest code per "
                 "file year 1993-2025, '-' where the structure number is absent, 'N' where no item is rated.",
        "first": FIRST,
        "bridges": order,
        "lines": lines,
        "strokes": strokes,
        "rate": rate,
    }
    with open(out_data, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    n_b = len(order)
    per_b = Counter(s[0] for s in strokes)
    several = sum(1 for v in per_b.values() if v >= 2)
    still = sum(1 for l in lines if l[-1] != "-")
    held = [s for s in strokes if s[5] == "h"]
    fell = [s for s in strokes if s[5] == "f"]
    sh = sum(1 for s in held if s[3] <= 4) / len(held) if held else None
    sf = sum(1 for s in fell if s[3] <= 4) / len(fell) if fell else None
    pairs = Counter((s[3], s[4]) for s in strokes)
    top = pairs.most_common(5)
    size = os.path.getsize(out_data)
    sess = {
        "P1_strokes": len(strokes), "P1_bridges": n_b,
        "P2_agree": agree, "P2_share": agree / len(strokes) if strokes else None,
        "P3_several": several, "P3_share": several / n_b if n_b else None,
        "P4_still_2025": still, "P4_share": still / n_b if n_b else None,
        "P5_held_from_poor": sh, "P5_fell_from_poor": sf, "held": len(held), "fell_back": len(fell),
        "other": len(strokes) - len(held) - len(fell),
        "P6_top_pairs": [[list(k), v] for k, v in top],
        "P7_bytes": size,
        "max_strokes_one_bridge": max(per_b.values()) if per_b else 0,
    }
    with open(out_sess, "w") as f:
        json.dump(sess, f, indent=1, sort_keys=True)
    print(json.dumps(sess, sort_keys=True))


if __name__ == "__main__":
    main(*sys.argv[1:6])
