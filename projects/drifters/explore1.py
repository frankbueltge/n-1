"""Exploratory (not registered): where do long-carried drifters end, against drifters that ended still following?"""
import json, statistics
d = json.load(open("rows.json"))
F = d["fields"]; R = [dict(zip(F, r)) for r in d["rows"]]
def band(rows):
    n = len(rows)
    g = sum(1 for r in rows if 20 <= abs(r["end_lat"]) <= 40)
    return {"n": n, "end_in_20_40_lat": g, "share": round(g / n, 4) if n else None,
            "median_abs_end_lat": round(statistics.median(abs(r["end_lat"]) for r in rows), 1) if n else None}
dead = [r for r in R if r["death"] != 0 and r["carried_days"] is not None]
out = {
 "note": "exploratory, not registered in SELECTION.md",
 "carried_over_3_years": band([r for r in dead if r["carried_days"] > 3 * 365.25]),
 "carried_1_to_3_years": band([r for r in dead if 365.25 < r["carried_days"] <= 3 * 365.25]),
 "kept_drogue_to_end": band([r for r in dead if r["status"] == "kept"]),
 "all_starts": {"n": len(R), "start_in_20_40_lat": sum(1 for r in R if 20 <= abs(r["start_lat"]) <= 40)},
 "death_share_by_status": {},
}
for s in ("kept", "lost", "never"):
    sub = [r for r in R if r["status"] == s and r["death"] != 0]
    out["death_share_by_status"][s] = {c: round(sum(1 for r in sub if r["death"] == c) / len(sub), 4) for c in (1, 2, 3)}
out["all_starts"]["share"] = round(out["all_starts"]["start_in_20_40_lat"] / len(R), 4)
yrs = [r["carried_days"] / 365.25 for r in dead if r["carried_days"]]
out["carried_dead_with_any_carried"] = len(yrs)
out["carried_over_3_years_count"] = sum(1 for y in yrs if y > 3)
json.dump(out, open("explore1.json", "w"), indent=1); print(json.dumps(out, indent=1))
