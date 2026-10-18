"""Build index.html from session1.json, explore1.json, rows.json, session2.json, explore2.json, rows2.json and template.html."""
import json
s = json.load(open("session1.json")); e = json.load(open("explore1.json")); d = json.load(open("rows.json"))
log = json.load(open("fetch_log.json"))
F = d["fields"]; R = [dict(zip(F, r)) for r in d["rows"]]
known = [r for r in R if r["carried_days"] is not None]
s2 = json.load(open("session2.json")); e2 = json.load(open("explore2.json")); d2 = json.load(open("rows2.json"))
log2 = json.load(open("fetch2_log.json"))
R2 = [dict(zip(d2["fields"], r)) for r in d2["rows"]]
shift = {r["id"]: r["shift_days"] for r in R2 if r["shift_days"] is not None and r["shift_days"] > 1}
data = {"r": [[0, round(r["start_lat"], 1), round(r["start_lon"], 1), round(r["end_lat"], 1), round(r["end_lon"], 1),
               round(r["drogued_days"]), round(r["carried_days"]), r["status"][0], r["start"][:7], r["end"][:7], r["death"], round(shift.get(r["id"], 0))] for r in known]}
data["sh"] = sorted((round(v) for v in shift.values()), reverse=True)
data["lt"] = sorted((round(-r["shift_days"]) for r in R2 if r["shift_days"] is not None and r["shift_days"] < -1), reverse=True)
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
         "P7": f"{s['by_era']['2010 and after']['median_drogued_days']:.0f} against {s['by_era']['2000-2009']['median_drogued_days']:.0f} days",
         "P8": f"{s2['parsed_rows']:,} rows", "P9": f"{s2['joined_share'] * 100:.1f} %", "P10": f"{s2['earlier_share'] * 100:.1f} %",
         "P11": f"{s2['ratio']:.0f} times", "P12": f"{s2['share_of_s1_carried'] * 100:.1f} %", "P13": f"median {s2['median_earlier_shift']:.0f} days",
         "P14": f"{s2['agree_share'] * 100:.1f} %"}
words = {"P1": "at least 25,000 drifters", "P2": "of dead drifters, at least half 'quit transmitting'",
         "P3": "more ran aground than were picked up", "P4": "under 25 % kept their drogue to the end",
         "P5": "at least 35 % of drifter-days carried", "P6": "median days with a drogue under a year",
         "P7": "drifters put in since 2010 keep their drogue longer than those of 2000-2009",
         "P8": "the re-dating file holds at least 5,000 drifters", "P9": "at least 95 % of them stand in today's directory",
         "P10": "at least 30 % of re-worked drifters lost their drogue earlier than first written",
         "P11": "days re-stated as carried at least five times those re-stated as following",
         "P12": "days re-stated as carried at least 5 % of today's carried days",
         "P13": "half of the drifters re-dated earlier moved by more than 30 days",
         "P14": "today's directory carries the hand-made date for at least 80 %"}
pr = []
P = dict(P, **s2["predictions"])
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
VN = {"9999": "not yet", "9998": "unclear", "1979": "unknown from start", "9990": "still on"}
hist = e2["b_versions"]["most_restated"][0]
vh = "".join(f"<th>{v[2:4]}-{v[5:7]}-{v[8:10]}</th>" for v in e2["b_versions"]["versions"])
vr = "".join(f"<td>{VN.get(m[:4], m)}</td>" for m in hist["history"])
old = e2["e_carried_share_if_original_stood"]["original"]
tot = s["drogued_days"] + s["carried_days"]
am = e2["a_auto_vs_manual"]; big = e2["d_redated_over_3_years"]
sub.update({"RE_FILE": f"{s2['parsed_rows']:,}", "RE_N": f"{s2['classes']['earlier']:,}", "FC_M": f"{s2['following_to_carried_days'] / 1e6:.2f}",
            "CF_K": f"{s2['carried_to_following_days'] / 1e3:.0f}", "MED": f"{s2['median_earlier_shift']:.0f}",
            "OLD_PCT": f"{old * 100:.0f}", "OLD_FPCT": f"{100 - old * 100:.0f}", "OLD_C": round(old * tot), "OLD_F": round((1 - old) * tot),
            "LATER_N": f"{s2['classes']['later']:,}", "HELD_N": f"{s2['classes']['held']:,}",
            "AM_N": f"{am['differ_over_30_days']:,}", "AM_PCT": f"{am['share'] * 100:.0f}", "AM_E": f"{am['manual_earlier_than_auto_over_30']:,}",
            "V_HEAD": vh, "V_ROW": vr, "V_ID": hist["id"], "BIG_N": big["n"], "BIG_PCT": f"{big['share'] * 100:.0f}", "BIG_S": big["start_south_of_35S"],
            "AG_PCT": f"{s2['agree_share'] * 100:.0f}", "AG": f"{s2['agree']:,}", "AG_N": f"{s2['agree_n']:,}", "FETCHED2": log2["fetched_utc"][:10]})
t = open("template.html").read()
for k, v in sub.items():
    t = t.replace("{{" + k + "}}", str(v))
assert "{{" not in t
open("index.html", "w").write(t)
print(len(t))
