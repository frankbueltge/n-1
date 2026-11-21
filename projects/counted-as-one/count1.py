"""Project 26, session 1: the 12/24 count made of every 2025 storm-overflow activation in England.

Usage: python3 count1.py <start-stop dir> <annual return xlsx> <out dir>
Writes session1.json (summary, predictions) and session1-per.json.gz (per overflow aggregates).
Stdlib only; rule.py and xlsx.py beside it. Definitions: SELECTION.md; changes after reading the
files: JOURNAL.md.
"""
import csv
import glob
import gzip
import json
import os
import statistics
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rule  # noqa: E402
import xlsx  # noqa: E402

EPOCH = datetime(2025, 1, 1, tzinfo=timezone.utc)
YEAR_H = 365 * 24.0
EXCEL0 = datetime(1899, 12, 30, tzinfo=timezone.utc)


def hours_of(v):
    """A time cell -> hours since 2025-01-01 00:00 GMT, or None if unparseable."""
    if v is None:
        return None
    if isinstance(v, float):
        return (v - (EPOCH - EXCEL0).days) * 24.0
    s = str(v).strip()
    if not s:
        return None
    try:
        return (float(s) - (EPOCH - EXCEL0).days) * 24.0
    except ValueError:
        pass
    s2 = s.replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s2)
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return (d - EPOCH).total_seconds() / 3600.0


def read_startstop(path):
    if path.lower().endswith(".csv"):
        with open(path, encoding="utf-8-sig", newline="") as h:
            rd = csv.reader(h)
            next(rd)
            for r in rd:
                yield (r + [None] * 4)[:4]
    else:
        first = True
        for _sh, r in xlsx.rows(path):
            if first:
                first = False
                continue
            yield (r + [None] * 4)[:4]


def dur_hours(s):
    if s is None:
        return None
    if isinstance(s, float):
        return s * 24.0  # a time cell stored as a fraction of a day
    s = str(s).strip()
    if not s:
        return None
    p = s.split(":")
    try:
        if len(p) == 3:
            return int(p[0]) + int(p[1]) / 60 + float(p[2]) / 3600
        return float(s) * 24.0
    except ValueError:
        return None


def read_annual(path):
    out = {}
    dup = 0
    header_seen = False
    for _sh, r in xlsx.rows(path, "All WaSC"):
        if not header_seen:
            if r and r[0] == "Unique ID":
                header_seen = True
            continue
        if not r or not r[0]:
            continue
        r = r + [None] * 26
        uid = str(r[0]).strip()
        cnt = r[16]
        rec = {"company": r[1], "count": cnt if isinstance(cnt, float) else None,
               "hours": dur_hours(r[15]), "edm_pct": r[19] if isinstance(r[19], float) else None,
               "raw_count": None if isinstance(cnt, float) else cnt}
        if uid in out:
            dup += 1
            out[uid].append(rec)
        else:
            out[uid] = [rec]
    return out, dup


def q(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main(ssdir, arpath, outdir):
    files = sorted(glob.glob(os.path.join(ssdir, "*.csv")) + glob.glob(os.path.join(ssdir, "*.xlsx")))
    per_file = {}
    acts = {}  # uid -> list of (start, stop)
    where = {}
    two_files = set()
    for f in files:
        name = os.path.basename(f)
        st = {"rows": 0, "malformed": 0, "outside_2025": 0, "clipped": 0, "used": 0}
        for uid, _site, a, b in read_startstop(f):
            st["rows"] += 1
            uid = (str(uid).strip() if uid is not None else "")
            ha, hb = hours_of(a), hours_of(b)
            if not uid or ha is None or hb is None or hb < ha:
                st["malformed"] += 1
                continue
            if hb < 0 or ha >= YEAR_H:
                st["outside_2025"] += 1
                continue
            if ha < 0 or hb > YEAR_H:
                st["clipped"] += 1
                ha, hb = max(ha, 0.0), min(hb, YEAR_H)
            st["used"] += 1
            acts.setdefault(uid, []).append((ha, hb))
            if uid in where and where[uid] != name:
                two_files.add(uid)
            where[uid] = name
        per_file[name] = st

    annual, ar_dup = read_annual(arpath)

    spills_all = []
    per = []
    longest = None
    for uid, lst in acts.items():
        sp = rule.count_spills(lst)
        spills_all.extend(sp)
        seqs = {}
        for s in sp:
            seqs.setdefault(s["seq"], []).append(s)
        for k, ss in seqs.items():
            span = (ss[-1]["hi"] - ss[0]["lo"]) / 24.0
            if longest is None or span > longest["days"]:
                longest = {"uid": uid, "days": span, "blocks": len(ss),
                           "start_h": ss[0]["lo"], "end_h": ss[-1]["hi"]}
        H = sum(b - a for a, b in lst)
        ar = annual.get(uid)
        row = {"uid": uid, "file": where[uid], "acts": len(lst), "hours": round(H, 4), "count": len(sp)}
        if ar and len(ar) == 1:
            row["ar_count"] = ar[0]["count"]
            row["ar_hours"] = None if ar[0]["hours"] is None else round(ar[0]["hours"], 4)
            row["edm_pct"] = ar[0]["edm_pct"]
        elif ar:
            row["ar_rows"] = len(ar)
        per.append(row)

    with_c = [r for r in per if r["count"] >= 1]
    hps = [r["hours"] / r["count"] for r in with_c]
    n_sp = len(spills_all)
    lt1 = sum(1 for s in spills_all if s["hours"] < 1)
    ge12 = sum(1 for s in spills_all if s["hours"] >= 12)
    tot_acts = sum(r["acts"] for r in per)
    tot_cnt = sum(r["count"] for r in per)
    two = [r for r in per if r["acts"] >= 2]
    p5 = sum(1 for r in two if r["count"] < r["acts"])
    matched = [r for r in per if r.get("ar_count") is not None]
    p6 = sum(1 for r in matched if abs(r["count"] - r["ar_count"]) < 1e-9)
    hs = sorted((r["hours"] for r in per), reverse=True)
    top = hs[: max(1, round(len(hs) * 0.10))]
    tot_h = sum(hs)
    low = [r["hours"] / r["count"] for r in with_c if 1 <= r["count"] <= 10]
    high = [r["hours"] / r["count"] for r in with_c if r["count"] > 60]
    rows_all = sum(s["rows"] for s in per_file.values())
    malformed = sum(s["malformed"] for s in per_file.values())

    preds = {
        "P1": {"value": statistics.median(hps), "held": 2 <= statistics.median(hps) <= 6},
        "P2": {"value": lt1 / n_sp, "held": lt1 / n_sp > 0.25},
        "P3": {"value": ge12 / n_sp, "held": ge12 / n_sp < 0.10},
        "P4": {"value": tot_acts / tot_cnt, "held": tot_acts / tot_cnt > 2},
        "P5": {"value": p5 / len(two), "held": p5 / len(two) > 0.70},
        "P6": {"value": p6 / len(matched) if matched else None, "held": bool(matched) and p6 / len(matched) > 0.80},
        "P7": {"value": sum(top) / tot_h, "held": sum(top) / tot_h > 0.50},
        "P8": {"value": longest["days"], "held": longest["days"] > 30},
        "P9": {"value": malformed / rows_all, "held": malformed / rows_all < 0.01},
        "P10": {"value": [statistics.median(low) if low else None, statistics.median(high) if high else None],
                "held": bool(low and high) and statistics.median(low) < statistics.median(high)},
    }
    hours_sp = [s["hours"] for s in spills_all]
    acts_sp = [s["acts"] for s in spills_all]
    summary = {
        "files": per_file, "rows": rows_all, "malformed": malformed,
        "overflows_with_activations": len(per), "ids_in_two_files": sorted(two_files),
        "activations_used": tot_acts, "hours_total": tot_h, "counted_spills": tot_cnt,
        "annual_return_ids": len(annual), "annual_return_duplicate_rows": ar_dup,
        "matched": len(matched), "matched_equal": p6,
        "matched_recount_higher": sum(1 for r in matched if r["count"] > r["ar_count"]),
        "matched_recount_lower": sum(1 for r in matched if r["count"] < r["ar_count"]),
        "spill_hours_quantiles": {p: q(hours_sp, p) for p in (0.1, 0.25, 0.5, 0.75, 0.9, 0.99)},
        "spill_acts_quantiles": {p: q(acts_sp, p) for p in (0.5, 0.9, 0.99)},
        "spill_acts_max": max(acts_sp),
        "spills_lt_1h": lt1, "spills_ge_12h": ge12,
        "hours_per_count_quantiles": {p: q(hps, p) for p in (0.1, 0.25, 0.5, 0.75, 0.9)},
        "longest_sequence": longest,
        "predictions": preds,
        "attribution": "© Environment Agency copyright and/or database right 2026. All rights reserved. (Open Government Licence per the data.gov.uk catalogue)",
    }
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "session1.json"), "w") as h:
        json.dump(summary, h, indent=1, default=str)
    with gzip.open(os.path.join(outdir, "session1-per.json.gz"), "wt") as h:
        json.dump(sorted(per, key=lambda r: r["uid"]), h)
    for k, v in preds.items():
        print(k, v)
    print(json.dumps({k: summary[k] for k in ("rows", "malformed", "overflows_with_activations", "activations_used",
                                               "counted_spills", "matched", "matched_equal", "longest_sequence")}, default=str))


if __name__ == "__main__":
    main(*sys.argv[1:4])
