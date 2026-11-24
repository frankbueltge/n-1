"""Project 26, session 3: the data of the work Out of Season (a wall of calendars).

Usage: python3 -I build4.py <start-stop dir> <annual return xlsx> <session2-per.json.gz> <out dir>
Writes session3.json (summary, predictions) and data.json (the work's data, per overflow in U).
Stdlib only; imports count1.py (readers), rule.py (the rule, unchanged) and count2.py (annual-return reader) beside it.
Definitions and predictions: SESSION3.md (pushed a6f3332 before tonight's download).
"""
import glob
import gzip
import json
import math
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import count1  # noqa: E402
import count2  # noqa: E402
import rule  # noqa: E402

DAYS = 365
SEASON = count2.SEASON  # (3216.0, 6552.0) hours: 15 May 00:00 to 1 Oct 00:00 GMT
SEASON_D = (int(SEASON[0] // 24), int(SEASON[1] // 24))  # day 134 .. 272 inclusive -> range(134, 273)


def lo_of(t0, k):
    return t0 if k == 0 else t0 + 12 + 24 * (k - 1)


def k_at(t0, t):
    """Largest k with lo_of(t0, k) <= t."""
    k = 0 if t < t0 + 12 else 1 + int(math.floor((t - t0 - 12) / 24))
    while k > 0 and lo_of(t0, k) > t:
        k -= 1
    while lo_of(t0, k + 1) <= t:
        k += 1
    return k


def blocks(acts):
    """Own enumeration of the 12/24 blocks (independent of rule.py). Returns the first-touch time of each counted block."""
    acts = sorted(acts)
    out = []
    t0, maxk, first = None, -1, {}
    for a, b in acts:
        if t0 is not None:
            ka = k_at(t0, a)
            if ka > maxk + 1:  # block maxk+1 was empty: the sequence closed
                out.extend(first[k] for k in range(maxk + 1))
                t0, maxk, first = None, -1, {}
        if t0 is None:
            t0 = a
        ka = k_at(t0, a)
        if b == a:
            kb = ka
        else:
            kb = k_at(t0, b)
            if lo_of(t0, kb) >= b:  # ends exactly at a block's start: does not touch it
                kb -= 1
        for k in range(ka, kb + 1):
            if k not in first:
                first[k] = max(a, lo_of(t0, k))
        maxk = max(maxk, kb)
    if t0 is not None:
        out.extend(first[k] for k in range(maxk + 1))
    return out


def daily_union(acts):
    """Hours per day of the union of activations (no double counting); also returns the union's total."""
    iv = sorted(acts)
    merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    day = [0.0] * DAYS
    for a, b in merged:
        d = int(a // 24)
        while d < DAYS and d * 24 < b:
            day[d] += max(0.0, min(b, (d + 1) * 24) - max(a, d * 24))
            d += 1
    return day, sum(b - a for a, b in merged)


def main(ssdir, arpath, per2path, outdir):
    per2 = {r["uid"]: r for r in json.load(gzip.open(per2path, "rt"))}
    files = sorted(glob.glob(os.path.join(ssdir, "*.csv")) + glob.glob(os.path.join(ssdir, "*.xlsx")))
    acts = {}
    for f in files:
        for uid, _site, a, b in count1.read_startstop(f):
            uid = (str(uid).strip() if uid is not None else "")
            ha, hb = count1.hours_of(a), count1.hours_of(b)
            if not uid or ha is None or hb is None or hb < ha or hb < 0 or ha >= count1.YEAR_H:
                continue
            acts.setdefault(uid, []).append((max(ha, 0.0), min(hb, count1.YEAR_H)))
    ar, dup = count2.read_annual2(arpath)

    enum_bad, counts, hours = [], {}, {}
    for uid, lst in acts.items():
        c = len(rule.count_spills(lst))
        if len(blocks(lst)) != c:
            enum_bad.append(uid)
        counts[uid] = c
        hours[uid] = sum(b - a for a, b in lst)
    O = [u for u in acts if counts[u] >= 30]
    medO = statistics.median(hours[u] for u in O)
    U = sorted(u for u in acts if counts[u] < 30 and hours[u] > medO)
    U2 = sorted(u for u, r in per2.items() if r["count"] < 30 and r["hours"] > 241.11)

    data, tot_union, tot_sum = [], 0.0, 0.0
    together = [0.0] * DAYS
    month_h = [0.0] * 12
    in_season_starts_majority, no_long_season_day = 0, 0
    mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    mstart = [sum(mdays[:i]) for i in range(12)]
    for u in U:
        day, un = daily_union(acts[u])
        st = blocks(acts[u])
        sd = [int(t // 24) for t in st]
        tot_union += un
        tot_sum += hours[u]
        for d in range(DAYS):
            together[d] += day[d]
        for m in range(12):
            month_h[m] += sum(day[mstart[m]:mstart[m] + mdays[m]])
        ins = sum(1 for d in sd if SEASON_D[0] <= d < SEASON_D[1])
        if ins * 2 > len(sd):
            in_season_starts_majority += 1
        if max(day[SEASON_D[0]:SEASON_D[1]]) < 12:
            no_long_season_day += 1
        a = ar.get(u) if u not in dup else None
        data.append({"id": u, "water": (a or {}).get("receiving"), "bathing": (a or {}).get("bathing"),
                     "shellfish": (a or {}).get("shellfish"), "count": counts[u], "hours": round(hours[u], 1),
                     "days": [round(x, 1) for x in day], "starts": sd})
    peak = max(range(DAYS), key=lambda d: together[d])
    os.makedirs(outdir, exist_ok=True)
    dpath = os.path.join(outdir, "data.json")
    with open(dpath, "w") as h:
        json.dump({"season_days": [SEASON_D[0], SEASON_D[1] - 1], "overflows": data,
                   "together": [round(x, 1) for x in together],
                   "attribution": "Contains Environment Agency data. © Environment Agency copyright and/or database right 2026."},
                  h, separators=(",", ":"))
    size = os.path.getsize(dpath)
    rng = random.Random(20261124)
    draw = rng.sample(U, 3)
    draw_days = {u: sorted(rng.sample(range(DAYS), 4)) for u in draw}
    preds = {
        "P1": {"value": [len(U), len(U2), U == U2], "held": U == U2},
        "P2": {"value": len(enum_bad), "held": not enum_bad},
        "P3": {"value": [tot_union, tot_sum, abs(tot_union - 66219.3497) / 66219.3497],
               "held": abs(tot_union - 66219.3497) / 66219.3497 <= 0.01},
        "P4": {"value": [peak, together[peak]], "held": not (SEASON_D[0] <= peak < SEASON_D[1])},
        "P5": {"value": in_season_starts_majority, "held": in_season_starts_majority < 10},
        "P6": {"value": [round(x, 1) for x in month_h], "held": max(range(12), key=lambda m: month_h[m]) in (0, 10, 11)},
        "P7": {"value": no_long_season_day, "held": no_long_season_day >= 100},
        "P8": {"value": size, "held": size < 300 * 1024},
    }
    summary = {"overflows": len(acts), "O": len(O), "median_hours_O": medO, "U": len(U), "enum_bad": enum_bad[:20],
               "U_union_hours": tot_union, "U_summed_hours": tot_sum, "season_days": [SEASON_D[0], SEASON_D[1] - 1],
               "together_peak_day": peak, "together_season_hours": sum(together[SEASON_D[0]:SEASON_D[1]]),
               "U_starts": sum(len(r["starts"]) for r in data),
               "U_starts_in_season": sum(1 for r in data for d in r["starts"] if SEASON_D[0] <= d < SEASON_D[1]),
               "U_bathing": sum(1 for r in data if r["bathing"]), "U_shellfish": sum(1 for r in data if r["shellfish"]),
               "data_bytes": size, "predictions": preds,
               "check_draw": {u: {"days": draw_days[u], "hours": [round(next(r for r in data if r["id"] == u)["days"][d], 4)
                                                                    for d in draw_days[u]],
                                  "starts": len(next(r for r in data if r["id"] == u)["starts"]), "count": counts[u]}
                              for u in draw}}
    with open(os.path.join(outdir, "session3.json"), "w") as h:
        json.dump(summary, h, indent=1)
    print(json.dumps({k: v["held"] for k, v in preds.items()}), len(U), size)


if __name__ == "__main__":
    main(*sys.argv[1:5])
