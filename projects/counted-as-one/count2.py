"""Project 26, session 2: which waters receive the discharge the trigger does not see; rule variants against the returned count.

Usage: python3 -I count2.py <start-stop dir> <annual return xlsx> <session1-per.json.gz> <out dir>
Writes session2.json (summary, predictions) and session2-per.json.gz (per overflow).
Stdlib only; imports count1.py (readers), rule.py (V0, unchanged) and xlsx.py beside it.
Definitions: SESSION2.md; the vocabulary decision: JOURNAL.md, session 2, before the count.
"""
import gzip
import glob
import json
import math
import os
import random
import statistics
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import count1  # noqa: E402
import rule  # noqa: E402
import xlsx  # noqa: E402

SEASON = (count1.hours_of("2025-05-15T00:00:00Z"), count1.hours_of("2025-10-01T00:00:00Z"))


def clean(v):
    if v is None:
        return None
    s = str(v).replace("\xa0", " ").strip()
    return s or None


def named(v, nones):
    s = clean(v)
    return None if s is None or s in nones else s


def read_annual2(path):
    out, dup, hdr = {}, set(), None
    for _sh, r in xlsx.rows(path, "All WaSC"):
        if hdr is None:
            if r and r[0] == "Unique ID":
                hdr = r
            continue
        if not r or not r[0]:
            continue
        r = r + [None] * 30
        uid = str(r[0]).strip()
        rec = {"receiving": clean(r[11]),
               "shellfish": named(r[12], {"Not Applicable"}),
               "bathing": named(r[13], {"Not Applicable"}),
               "hsf_reason": clean(r[22])}
        if uid in out:
            dup.add(uid)
        out[uid] = rec
    return out, dup


def count_var(acts, closed=False, gap_close=False):
    """V1 (closed=True) and V2 (gap_close=True); with both False it must equal rule.count_spills (self-check)."""
    acts = sorted(acts)
    if not acts:
        return 0
    if gap_close:
        groups, cur, mx = [], [acts[0]], acts[0][1]
        for a, b in acts[1:]:
            if a - mx >= 24:
                groups.append(cur)
                cur, mx = [(a, b)], b
            else:
                cur.append((a, b))
                mx = max(mx, b)
        groups.append(cur)
        n = 0
        for g in groups:
            t0 = g[0][0]
            kk = lambda t: 0 if t < t0 + 12 else 1 + int(math.floor((t - t0 - 12) / 24))
            ks = set()
            for a, b in g:
                if b == a:
                    ks.add(kk(a))
                else:
                    hi = kk(b) if (closed or not _on_edge(b, t0)) else kk(b) - 1
                    ks.update(range(kk(a), max(kk(a), hi) + 1))
            n += len(ks)
        return n
    # grid rule with a parametrised touch
    i, n_all, total = 0, len(acts), 0
    while i < n_all:
        t0 = acts[i][0]
        k, last_hi = 0, None
        while True:
            lo = t0 if k == 0 else t0 + 12 + 24 * (k - 1)
            hi = t0 + 12 if k == 0 else t0 + 12 + 24 * k
            hit = False
            for a, b in acts[i:]:
                if a >= hi:
                    break
                if (lo <= a < hi) if a == b else (a < hi and (b >= lo if closed else b > lo)):
                    hit = True
                    break
            if not hit and k >= 1:
                break
            total += 1
            last_hi = hi
            k += 1
        empty_end = last_hi + 24
        while i < n_all and acts[i][0] < empty_end:
            i += 1
    return total


def _on_edge(b, t0):
    """True when b falls exactly on a block boundary (so under V0 the activation does not touch the block that starts at b)."""
    if b == t0 + 12:
        return True
    x = (b - t0 - 12) / 24
    return b > t0 + 12 and abs(x - round(x)) < 1e-9


def trunc_min(acts):
    return [(math.floor(a * 60 + 1e-9) / 60, math.floor(b * 60 + 1e-9) / 60) for a, b in acts]


def season_hours(acts):
    lo, hi = SEASON
    return sum(max(0.0, min(b, hi) - max(a, lo)) for a, b in acts)


def main(ssdir, arpath, per1path, outdir):
    per1 = {r["uid"]: r for r in json.load(gzip.open(per1path, "rt"))}
    files = sorted(glob.glob(os.path.join(ssdir, "*.csv")) + glob.glob(os.path.join(ssdir, "*.xlsx")))
    acts = {}
    for f in files:
        for uid, _site, a, b in count1.read_startstop(f):
            uid = (str(uid).strip() if uid is not None else "")
            ha, hb = count1.hours_of(a), count1.hours_of(b)
            if not uid or ha is None or hb is None or hb < ha or hb < 0 or ha >= count1.YEAR_H:
                continue
            acts.setdefault(uid, []).append((max(ha, 0.0), min(hb, count1.YEAR_H)))
    ar, dup = read_annual2(arpath)

    per, selfcheck_bad = [], 0
    for uid, lst in acts.items():
        p1 = per1[uid]
        v0 = len(rule.count_spills(lst))
        assert v0 == p1["count"], uid
        if count_var(lst) != v0:
            selfcheck_bad += 1
        row = dict(p1)
        row.update({"v1": count_var(lst, closed=True), "v2": count_var(lst, gap_close=True),
                    "v3": len(rule.count_spills(trunc_min(lst))), "season_h": round(season_hours(lst), 4)})
        a = ar.get(uid) if uid not in dup else None
        if a:
            row.update(a)
        per.append(row)

    O = [r for r in per if r["count"] >= 30]
    medO = statistics.median(r["hours"] for r in O)
    U = [r for r in per if r["count"] < 30 and r["hours"] > medO]
    share = lambda xs, f: sum(1 for r in xs if f(r)) / len(xs) if xs else None
    bath = lambda r: r.get("bathing") is not None
    bs = lambda r: r.get("bathing") is not None or r.get("shellfish") is not None
    matched = [r for r in per if r.get("ar_count") is not None]
    withpct = [r for r in matched if isinstance(r.get("edm_pct"), float)]
    lowop = [r["count"] for r in withpct if r["edm_pct"] < 50]
    hiop = [r["count"] for r in withpct if r["edm_pct"] >= 90]
    diff = [r for r in matched if r["count"] != r["ar_count"]]
    eq = {v: sum(1 for r in matched if r[v if v != "v0" else "count"] == r["ar_count"]) for v in ("v0", "v1", "v2", "v3")}
    bathed = [r for r in per if bath(r)]
    bh, bsh = sum(r["hours"] for r in bathed), sum(r["season_h"] for r in bathed)

    preds = {
        "P1": {"value": share(U, bath), "held": share(U, bath) > 0.10},
        "P2": {"value": [share(U, bs), share(O, bs)], "held": share(U, bs) > share(O, bs)},
        "P3": {"value": statistics.median(r["edm_pct"] for r in U if isinstance(r.get("edm_pct"), float)),
               "held": statistics.median(r["edm_pct"] for r in U if isinstance(r.get("edm_pct"), float)) >= 95},
        "P4": {"value": share(withpct, lambda r: r["edm_pct"] < 90), "held": share(withpct, lambda r: r["edm_pct"] < 90) > 0.05},
        "P5": {"value": [statistics.median(lowop) if lowop else None, statistics.median(hiop)],
               "held": bool(lowop) and statistics.median(lowop) < statistics.median(hiop)},
        "P6": {"value": share(diff, lambda r: abs(r["count"] - r["ar_count"]) == 1),
               "held": share(diff, lambda r: abs(r["count"] - r["ar_count"]) == 1) > 0.5},
        "P7": {"value": eq, "held": max(eq["v1"], eq["v2"], eq["v3"]) > eq["v0"]},
        "P8": {"value": {k: v / len(matched) for k, v in eq.items()}, "held": max(eq.values()) / len(matched) <= 0.95},
        "P9": {"value": bsh / bh if bh else None, "held": bool(bh) and bsh / bh > 0.30},
    }
    # reconciliation by variant, among the V0-differing
    recon = {v: sum(1 for r in diff if r[v] == r["ar_count"]) for v in ("v1", "v2", "v3")}
    recon_any = sum(1 for r in diff if any(r[v] == r["ar_count"] for v in ("v1", "v2", "v3")))
    summary = {
        "season_hours_window": SEASON, "overflows": len(per), "annual_rows": len(ar), "annual_duplicate_ids": sorted(dup),
        "selfcheck_generic_equals_v0_bad": selfcheck_bad,
        "O": len(O), "median_hours_O": medO, "U": len(U),
        "U_bathing": sum(1 for r in U if bath(r)), "U_shellfish": sum(1 for r in U if r.get("shellfish")),
        "O_bathing": sum(1 for r in O if bath(r)), "O_shellfish": sum(1 for r in O if r.get("shellfish")),
        "all_bathing": len(bathed), "all_shellfish": sum(1 for r in per if r.get("shellfish")),
        "U_hours": sum(r["hours"] for r in U), "U_season_hours": sum(r["season_h"] for r in U),
        "bathing_hours": bh, "bathing_season_hours": bsh,
        "season_share_of_year": (SEASON[1] - SEASON[0]) / count1.YEAR_H,
        "all_hours": sum(r["hours"] for r in per), "all_season_hours": sum(r["season_h"] for r in per),
        "matched": len(matched), "with_pct": len(withpct), "lowop_lt50": len(lowop), "hiop_ge90": len(hiop),
        "differing": len(diff), "recon_by_variant": recon, "recon_any": recon_any,
        "predictions": preds,
    }
    rnd = random.Random(20261123)
    summary["check_draw_U"] = sorted(r["uid"] for r in rnd.sample(U, min(12, len(U))))
    summary["check_draw_bathing"] = sorted(r["uid"] for r in rnd.sample(bathed, min(3, len(bathed))))
    vm = [r for r in matched if r["count"] != r["ar_count"] and any(r[v] == r["ar_count"] for v in ("v1", "v2", "v3"))]
    summary["check_draw_variant"] = sorted(r["uid"] for r in rnd.sample(vm, min(6, len(vm))))
    os.makedirs(outdir, exist_ok=True)
    json.dump(summary, open(os.path.join(outdir, "session2.json"), "w"), indent=1, default=str)
    keep = ("uid", "count", "ar_count", "hours", "season_h", "edm_pct", "v1", "v2", "v3", "bathing", "shellfish", "receiving", "hsf_reason")
    with gzip.open(os.path.join(outdir, "session2-per.json.gz"), "wt") as h:
        json.dump([{k: r.get(k) for k in keep} for r in per], h)
    print(json.dumps({k: summary[k] for k in ("overflows", "U", "selfcheck_generic_equals_v0_bad", "differing", "recon_by_variant")}, default=str))
    for k, v in preds.items():
        print(k, v)


if __name__ == "__main__":
    main(*sys.argv[1:5])
