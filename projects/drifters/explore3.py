"""Exploratory (c), named after the reading rule was run (stated in ASSEMBLAGE.md entry 3): the person's date against the drifter's
first day, for the 1,022 and for all re-worked drifters; what today's directory writes for those the person dated to the first day;
and the drifter-days the 970 'unknown' would carry if the person's date were read. Not a prediction."""
import json, sys
from collections import Counter
from datetime import datetime
from session3 import run3
from lib import status, days

def at_start(r, x):
    return isinstance(r["manual"], datetime) and abs((r["manual"] - x["start"]).total_seconds()) / 86400 <= 1 or \
        isinstance(r["manual"], datetime) and r["manual"] < x["start"]

def main(dd, dirsrc):
    out, pop, d, old = run3(dd, dirsrc)
    from session2 import run
    s2, joined, _ = run(dd, dirsrc)
    unk = [r for r in pop if r["dclass"] == "unknown"]
    first = [r for r in joined if at_start(r, d[r["id"]])]
    st = Counter(status(d[r["id"]]) for r in first)
    u_first = sum(1 for r in unk if at_start(r, d[r["id"]]))
    # drifter-days of the 970, as the person dated them: drogued = manual - start (clipped), carried = the rest
    dr = ca = 0.0
    for r in unk:
        x = d[r["id"]]
        tot = (x["end"] - x["start"]).total_seconds() / 86400
        m = r["manual"]
        if m == "still_on":
            g = tot
        elif isinstance(m, datetime):
            g = max(0.0, min(tot, (m - x["start"]).total_seconds() / 86400))
        else:
            continue
        dr += g; ca += tot - g
    death = Counter(d[r["id"]]["death"] for r in unk)
    res = {"unknown_n": len(unk), "unknown_person_dated_first_day": u_first,
           "all_reworked_person_dated_first_day": len(first), "their_directory_status_today": dict(st),
           "unknown_days_if_person_read": {"drogued": round(dr), "carried": round(ca)},
           "unknown_death_codes": dict(sorted(death.items())),
           "note": "first day = the person's date within one day of the directory start, or before it"}
    json.dump(res, open("explore3.json", "w"), indent=1)
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
