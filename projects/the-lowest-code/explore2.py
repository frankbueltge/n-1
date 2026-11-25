"""Project 27 session 1, exploratory (not registered): the bridges Poor and open in the 2025 file, and the sawtooth.
Usage: python3 explore2.py DIR OUT.json"""
import gzip, json, os, statistics, sys
from count1 import read_year

d, out = sys.argv[1:3]
per = json.load(gzip.open("session1-per.json.gz"))
r25, _ = read_year(os.path.join(d, "AL25.txt"), 2025, "01")
now = {b: r for b, r in r25.items() if r["L"] is not None and r["L"] <= 4 and r["open"] != "K"}
closed = sum(1 for r in r25.values() if r["L"] is not None and r["L"] <= 4 and r["open"] == "K")
lens = []
for b in now:
    sp = per[b]["spells"][-1]
    lens.append(sp[1] - sp[0] + 1)
status = {}
for r in now.values():
    status[r["open"]] = status.get(r["open"], 0) + 1
codes = {}
for r in now.values():
    codes[str(r["L"])] = codes.get(str(r["L"]), 0) + 1
# sawtooth: bridges (1993-2025) whose line has a rise with no reconstruction recorded followed later by a fall
saw = sum(1 for v in per.values() if v["rises_norecon"] > 0 and v["falls"] > 0)
res = {
    "poor_open_2025": len(now),
    "poor_closed_2025": closed,
    "poor_open_2025_item41": status,
    "poor_open_2025_lowest_code": codes,
    "poor_open_2025_adt_sum": sum(r["adt"] or 0 for r in now.values()),
    "current_spell_years_median": statistics.median(lens),
    "current_spell_years_ge10": sum(1 for x in lens if x >= 10),
    "current_spell_years_ge20": sum(1 for x in lens if x >= 20),
    "current_spell_years_33": sum(1 for x in lens if x >= 33),
    "bridges_with_norecon_rise_and_a_fall": saw,
    "note": "exploratory; a current spell is counted back through consecutive file years from 2025, 1992 included where numbers carry (they do not from 1992 to 1993)",
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
