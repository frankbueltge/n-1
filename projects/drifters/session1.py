"""Session 1, as registered in SELECTION.md. Input: the scratch directory fetch.py wrote."""
import json, os, statistics, sys
from collections import Counter
from lib import parse, status, days
from fetch import FILES


def era(y):
    return "before 2000" if y < 2000 else ("2000-2009" if y < 2010 else "2010 and after")


def main(src):
    rows, bad, dup, seen = [], 0, 0, set()
    for f in FILES:
        for line in open(os.path.join(src, f), encoding="latin-1"):
            if not line.strip():
                continue
            r = parse(line)
            if r is None or r["start"] is None or r["end"] is None:
                bad += 1
                continue
            if r["id"] in seen:
                dup += 1
                continue
            seen.add(r["id"])
            r["status"] = status(r)
            r["days"] = days(r)
            rows.append(r)
    dead = [r for r in rows if r["death"] != 0]
    codes = Counter(r["death"] for r in dead)
    st = Counter(r["status"] for r in rows)
    known = [r for r in rows if r["days"] is not None]
    drog = sum(r["days"][0] for r in known)
    carr = sum(r["days"][1] for r in known)
    kd = [r for r in known if r["death"] != 0]
    kept = sum(1 for r in kd if r["status"] == "kept")
    med = statistics.median(r["days"][0] for r in kd)
    by_era = {}
    for e in ("before 2000", "2000-2009", "2010 and after"):
        sub = [r for r in kd if era(r["start"].year) == e]
        by_era[e] = {"n": len(sub), "median_drogued_days": round(statistics.median(r["days"][0] for r in sub), 1) if sub else None,
                     "kept_share": round(sum(1 for r in sub if r["status"] == "kept") / len(sub), 4) if sub else None,
                     "carried_share": round(sum(r["days"][1] for r in sub) / max(1e-9, sum(sum(r["days"]) for r in sub)), 4) if sub else None}
    code_by_status = {s: dict(Counter(r["death"] for r in dead if r["status"] == s)) for s in st}
    out = {
        "drifters": len(rows), "bad_rows": bad, "duplicate_ids": dup, "alive": len(rows) - len(dead), "dead": len(dead),
        "death_codes": dict(sorted(codes.items())), "status": dict(st), "death_code_by_status": code_by_status,
        "known_status": len(known), "drogued_days": round(drog), "carried_days": round(carr),
        "carried_share": round(carr / (drog + carr), 4), "dead_known": len(kd), "kept_to_end": kept,
        "kept_share": round(kept / len(kd), 4), "median_drogued_days_dead_known": round(med, 1), "by_era": by_era,
        "start_years": [min(r["start"].year for r in rows), max(r["start"].year for r in rows)],
    }
    p = out
    pr = {
        "P1 >=25000 drifters": p["drifters"] >= 25000,
        "P2 quit >= half of dead": codes[3] / len(dead) >= 0.5,
        "P3 aground > picked up": codes[1] > codes[2],
        "P4 kept to end < 25% (dead, known)": p["kept_share"] < 0.25,
        "P5 carried days >= 35%": p["carried_share"] >= 0.35,
        "P6 median drogued days < 365": med < 365,
        "P7 2010+ median > 2000-2009 median": by_era["2010 and after"]["median_drogued_days"] > by_era["2000-2009"]["median_drogued_days"],
    }
    out["predictions"] = pr
    json.dump(out, open("session1.json", "w"), indent=1)
    # compact derived rows for the page: id, type, start date, end date, lat/lon rounded 0.01, status, code, drogued, carried
    keep = [[r["id"], r["type"], r["start_d"], r["end_d"], round(r["start_lat"], 2), round(r["start_lon"], 2),
             round(r["end_lat"], 2), round(r["end_lon"], 2), r["status"], r["death"],
             None if r["days"] is None else round(r["days"][0], 1), None if r["days"] is None else round(r["days"][1], 1)]
            for r in rows]
    json.dump({"fields": ["id", "type", "start", "end", "start_lat", "start_lon", "end_lat", "end_lon", "status", "death",
                          "drogued_days", "carried_days"], "rows": keep}, open("rows.json", "w"), separators=(",", ":"))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
