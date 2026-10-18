"""Session 2, exploratory (named in SESSION2.md before the run, not predictions): automatic against manual,
the archive's versions, the .old directory file, and where the re-dated drifters ended."""
import json, os, sys
from collections import Counter
from lib import parse as parse_dir, zero_date
from datetime import datetime
from lib2 import parse, effective, value
from session2 import run
from fetch2 import ARCHIVE

VERSIONS = ARCHIVE + ["2013_04_16", "2013_06_30"]


def main(dd, dirsrc):
    out, joined, d = run(dd, dirsrc)
    # (a) the method against the person
    both = []
    for r in joined:
        x = d[r["id"]]
        a, m = effective(r["auto"], x["start"], x["end"]), effective(r["manual"], x["start"], x["end"])
        if a is not None and m is not None:
            both.append((a - m).total_seconds() / 86400)
    over = [s for s in both if abs(s) > 30]
    # (b) versions: how often each drifter's manual value was re-stated
    hist = {}
    for v in VERSIONS:
        for line in open(os.path.join(dd, v + "_drogueoff.dat"), encoding="latin-1"):
            r = parse(line)
            if r:
                hist.setdefault(r["id"], []).append((v, r["raw"][2]))
    # transitions between successive versions, by parsed value (raw strings differ by format and by one-day rounding)
    kind = lambda v: v if isinstance(v, str) else "date"
    trans, moved, first_set = Counter(), set(), Counter()
    for i, h in hist.items():
        vals = [value(m) for _, m in h]
        vals = [v for v in vals if v != "not_reassessed"]
        for a, b in zip(vals, vals[1:]):
            if isinstance(a, datetime) and isinstance(b, datetime):
                if abs((a - b).days) > 1:
                    trans["date -> other date (> 1 day)"] += 1
                    moved.add(i)
            elif kind(a) != kind(b):
                trans[kind(a) + " -> " + kind(b)] += 1
        fs = next((v for v, m in h if value(m) != "not_reassessed"), None)
        first_set[fs] += 1
    most = sorted(hist.items(), key=lambda kv: -len({value(m) for _, m in kv[1]}))[:3]
    # (c) the .old directory file against the current one
    old = {}
    for line in open(os.path.join(dd, "dirfl_10001_15000.old"), encoding="latin-1"):
        r = parse_dir(line) if line.strip() else None
        if r:
            old[r["id"]] = r
    cmp = Counter()
    moved_days = 0.0
    for i, r in old.items():
        c = d.get(i)
        if c is None:
            cmp["gone"] += 1
            continue
        if r["drogue_d"] == c["drogue_d"] and r["drogue_t"] == c["drogue_t"]:
            cmp["same drogue date"] += 1
        else:
            cmp["drogue date differs"] += 1
            if r["drogue"] and c["drogue"]:
                moved_days += (r["drogue"] - c["drogue"]).total_seconds() / 86400
        if r["end_d"] != c["end_d"]:
            cmp["end date differs"] += 1
        if r["death"] != c["death"]:
            cmp["death code differs"] += 1
    # (d) where the drifters re-dated by more than three years ended
    big = [r for r in joined if r["shift"] is not None and r["shift"] > 3 * 365.25]
    lat = [abs(d[r["id"]]["end_lat"]) for r in big]
    # (e) the carried share had the original dates stood (study window only; approximate)
    s1 = json.load(open("session1.json"))
    fc, cf = out["following_to_carried_days"], out["carried_to_following_days"]
    tot = s1["drogued_days"] + s1["carried_days"]
    res = {
        "a_auto_vs_manual": {"n": len(both), "differ_over_30_days": len(over), "share": round(len(over) / len(both), 4),
                             "manual_earlier_than_auto_over_30": sum(1 for s in over if s > 0)},
        "b_versions": {"versions": VERSIONS, "drifters": len(hist), "transitions_between_versions": dict(trans.most_common()), "drifters_whose_manual_date_moved_over_1_day": len(moved),
                       "first_version_with_manual_value": dict(first_set),
                       "most_restated": [{"id": i, "history": [m for _, m in h]} for i, h in most]},
        "c_old_vs_current": {"old_rows": len(old), **dict(cmp), "net_days_old_minus_current_where_both_dated": round(moved_days)},
        "d_redated_over_3_years": {"n": len(big), "end_lat_20_40": sum(1 for a in lat if 20 <= a <= 40),
                                   "share": round(sum(1 for a in lat if 20 <= a <= 40) / len(big), 4) if big else None,
                                   "start_south_of_35S": sum(1 for r in big if d[r["id"]]["start_lat"] < -35)},
        "e_carried_share_if_original_stood": {"today": round(s1["carried_days"] / tot, 4),
                                              "original": round((s1["carried_days"] - fc + cf) / tot, 4),
                                              "note": "study window 1992-2010 only; drifters outside it unchanged; approximate"},
    }
    json.dump(res, open("explore2.json", "w"), indent=1)
    print(json.dumps(res, indent=1)[:4000])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
