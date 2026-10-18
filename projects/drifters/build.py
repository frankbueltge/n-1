"""Build index.html from session1.json, explore1.json, rows.json and template.html."""
import json
s = json.load(open("session1.json")); e = json.load(open("explore1.json")); d = json.load(open("rows.json"))
log = json.load(open("fetch_log.json"))
F = d["fields"]; R = [dict(zip(F, r)) for r in d["rows"]]
known = [r for r in R if r["carried_days"] is not None]
data = {"r": [[0, round(r["start_lat"], 1), round(r["start_lon"], 1), round(r["end_lat"], 1), round(r["end_lon"], 1),
               round(r["drogued_days"]), round(r["carried_days"]), r["status"][0], r["start"][:7], r["end"][:7], r["death"]] for r in known]}
# "Another drifter" walks the longest-carried first, then a fixed shuffle
order = sorted(range(len(known)), key=lambda i: -known[i]["carried_days"])
data["order"] = order[:10] + order[10::97]
dead = [r for r in R if r["death"] != 0]
def pct(a, b): return f"{100 * a / b:.0f}"
rows = []
for st, label in (("kept", "still following"), ("lost", "drogue lost on the way"), ("never", "drogue off when put in"), ("unknown", "drogue record unreadable")):
    sub = [r for r in dead if r["status"] == st]
    n = len(sub)
    rows.append(f"<tr><td>{label}</td><td>{n:,}</td>" + "".join(f"<td>{pct(sum(1 for r in sub if r['death'] == c), n)} %</td>" for c in (3, 1, 2)) + "</tr>")
ds = e["death_share_by_status"]
P = s["predictions"]
found = {"P1": f"{s['drifters']:,} drifters", "P2": f"{pct(s['death_codes']['3'], s['dead'])} % quit",
         "P3": f"aground {s['death_codes']['1']:,}, picked up {s['death_codes']['2']:,}",
         "P4": f"{s['kept_share'] * 100:.1f} % kept it to the end", "P5": f"{s['carried_share'] * 100:.1f} % carried",
         "P6": f"median {s['median_drogued_days_dead_known']:.0f} days",
         "P7": f"{s['by_era']['2010 and after']['median_drogued_days']:.0f} against {s['by_era']['2000-2009']['median_drogued_days']:.0f} days"}
words = {"P1": "at least 25,000 drifters", "P2": "of dead drifters, at least half 'quit transmitting'",
         "P3": "more ran aground than were picked up", "P4": "under 25 % kept their drogue to the end",
         "P5": "at least 35 % of drifter-days carried", "P6": "median days with a drogue under a year",
         "P7": "drifters put in since 2010 keep their drogue longer than those of 2000-2009"}
pr = []
for k, v in P.items():
    key = k.split()[0]
    pr.append(f"<tr><td>{key}</td><td>{words[key]}</td><td>{found[key]}</td><td>{'held' if v else '<b>failed</b>'}</td></tr>")
c3 = e["carried_over_3_years"]
sub = {"DATA": json.dumps(data, separators=(",", ":")),
       "DROG": s["drogued_days"], "CARR": s["carried_days"], "DROG_M": f"{s['drogued_days'] / 1e6:.2f}", "CARR_M": f"{s['carried_days'] / 1e6:.2f}",
       "CARR_PCT": f"{s['carried_share'] * 100:.0f}", "DROG_PCT": f"{100 - s['carried_share'] * 100:.0f}", "N": f"{s['drifters']:,}", "Y0": s["start_years"][0], "Y1": s["start_years"][1],
       "N_KNOWN": f"{s['known_status']:,}", "N_KEPT": f"{sum(1 for r in known if r['carried_days'] == 0):,}",
       "N_CARRIED": f"{sum(1 for r in known if r['carried_days'] > 0):,}", "N_C3": f"{c3['n']:,}", "C3_PCT": f"{c3['share'] * 100:.0f}",
       "K_PCT": f"{e['kept_drogue_to_end']['share'] * 100:.0f}", "S_PCT": f"{e['all_starts']['share'] * 100:.0f}",
       "DEATH_ROWS": "\n".join(rows), "PRED_ROWS": "".join(pr), "FETCHED": log["fetched_utc"][:10],
       "PK": f"{ds['kept']['2'] * 100:.0f}", "PL": f"{ds['lost']['2'] * 100:.0f}", "AK": f"{ds['kept']['1'] * 100:.0f}", "AL": f"{ds['lost']['1'] * 100:.0f}",
       "N_UNK": f"{s['status']['unknown']:,}"}
t = open("template.html").read()
for k, v in sub.items():
    t = t.replace("{{" + k + "}}", str(v))
assert "{{" not in t
open("index.html", "w").write(t)
print(len(t))
