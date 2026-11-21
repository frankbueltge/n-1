"""Exploratory (not registered): read session1.json and session1-per.json.gz and print what the page needs.
Usage: python3 explore1.py  -> explore1.json"""
import gzip, json, statistics
d = json.load(open("session1.json"))
per = json.load(gzip.open("session1-per.json.gz", "rt"))
blank = d["files"]["Southern Water 2025 EDM Detailed Data.xlsx"]["malformed"] - 0
out = {}
nonblank = d["rows"] - 995359
out["rows_nonblank"] = nonblank
out["malformed_nonblank"] = d["malformed"] - 995359
out["malformed_nonblank_share"] = out["malformed_nonblank"] / nonblank
m = [r for r in per if r.get("ar_count") is not None]
diff = [r["count"] - r["ar_count"] for r in m]
out["count_diff_quantiles"] = {p: sorted(diff)[int(p * (len(diff) - 1))] for p in (0.01, 0.05, 0.5, 0.95, 0.99)}
out["count_diff_max"] = max(diff); out["count_diff_min"] = min(diff)
hd = [r["hours"] - r["ar_hours"] for r in m if r.get("ar_hours") is not None]
out["hours_within_0.1h"] = sum(1 for x in hd if abs(x) <= 0.1); out["hours_compared"] = len(hd)
out["hours_total_recount"] = sum(r["hours"] for r in per)
out["hours_total_annual_matched"] = sum(r["ar_hours"] for r in m if r.get("ar_hours") is not None)
out["count_total_annual_matched"] = sum(r["ar_count"] for r in m)
# trigger: 30 counted spills in one year
out["over30_recount"] = sum(1 for r in per if r["count"] >= 30)
out["over30_annual"] = sum(1 for r in m if r["ar_count"] >= 30)
out["cross_trigger_recount_only"] = sum(1 for r in m if r["count"] >= 30 > r["ar_count"])
out["cross_trigger_annual_only"] = sum(1 for r in m if r["ar_count"] >= 30 > r["count"])
# what 30 counted spills can hold: hours among overflows counted 28-32 by the return
band = sorted(r["ar_hours"] for r in m if r.get("ar_hours") is not None and 28 <= r["ar_count"] <= 32)
out["band_28_32_n"] = len(band)
out["band_28_32_hours_min_med_max"] = [band[0], statistics.median(band), band[-1]] if band else None
# overflows under the trigger with more hours than the median overflow over it
over = [r["ar_hours"] for r in m if r.get("ar_hours") is not None and r["ar_count"] >= 30]
med_over = statistics.median(over)
out["median_hours_over_trigger"] = med_over
out["under_trigger_with_more_hours_than_that"] = sum(1 for r in m if r.get("ar_hours") is not None and r["ar_count"] < 30 and r["ar_hours"] > med_over)
lo = min((r for r in m if r["ar_count"] >= 30 and r.get("ar_hours") is not None), key=lambda r: r["ar_hours"])
hi = max((r for r in m if r["ar_count"] < 30 and r.get("ar_hours") is not None), key=lambda r: r["ar_hours"])
out["fewest_hours_over_trigger"] = {k: lo[k] for k in ("uid", "acts", "hours", "count", "ar_count", "ar_hours")}
out["most_hours_under_trigger"] = {k: hi[k] for k in ("uid", "acts", "hours", "count", "ar_count", "ar_hours")}
L = d["longest_sequence"]["uid"]
out["longest_sequence_overflow"] = next(r for r in per if r["uid"] == L)
json.dump(out, open("explore1.json", "w"), indent=1)
print(json.dumps(out, indent=1))
