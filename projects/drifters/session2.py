"""Session 2, as registered in SESSION2.md. Inputs: the scratch directories fetch2.py and fetch.py wrote."""
import json, os, statistics, sys
from collections import Counter
from lib import parse as parse_dir, zero_date
from lib2 import parse, shift, klass, agrees, STUDY_END
from fetch import FILES

CARRIED_S1 = 6607633


def directory(src):
    out = {}
    for f in FILES:
        for line in open(os.path.join(src, f), encoding="latin-1"):
            r = parse_dir(line) if line.strip() else None
            if r and r["start"] and r["end"] and r["id"] not in out:
                out[r["id"]] = r
    return out


def run(dd, dirsrc, name="2013_06_30_drogueoff.dat"):
    d = directory(dirsrc)
    rows, bad = [], 0
    for line in open(os.path.join(dd, name), encoding="latin-1"):
        r = parse(line)
        if r is None:
            if line.split() and line.split()[0].isdigit():
                bad += 1
            continue
        if "bad" in (r["orig"], r["auto"], r["manual"]):
            bad += 1
            continue
        rows.append(r)
    joined = [r for r in rows if r["id"] in d]
    for r in joined:
        x = d[r["id"]]
        r["shift"] = shift(r["orig"], r["manual"], x["start"], x["end"])
        r["class"] = klass(r["shift"])
        r["agrees"] = agrees(r["manual"], x["drogue"], zero_date(x["drogue_d"]), x["end"])
        r["auto_shift"] = shift(r["orig"], r["auto"], x["start"], x["end"])
    comp = [r for r in joined if r["shift"] is not None]
    cls = Counter(r["class"] for r in joined)
    fc = sum(r["shift"] for r in comp if r["shift"] > 1)
    cf = sum(-r["shift"] for r in comp if r["shift"] < -1)
    earlier = [r["shift"] for r in comp if r["shift"] > 1]
    ag = [r["agrees"] for r in joined if r["agrees"] is not None]
    kinds = lambda k: dict(Counter(v if isinstance(v, str) else "date" for v in (r[k] for r in rows)))
    out = {"file": name, "parsed_rows": len(rows), "bad_rows": bad, "joined": len(joined),
           "joined_share": round(len(joined) / len(rows), 4), "value_kinds": {k: kinds(k) for k in ("orig", "auto", "manual")},
           "comparable": len(comp), "classes": dict(cls), "earlier_share": round(cls["earlier"] / len(comp), 4),
           "following_to_carried_days": round(fc), "carried_to_following_days": round(cf),
           "ratio": round(fc / cf, 2) if cf else None, "share_of_s1_carried": round(fc / CARRIED_S1, 4),
           "median_earlier_shift": round(statistics.median(earlier), 1), "agree_n": len(ag), "agree": sum(ag),
           "agree_share": round(sum(ag) / len(ag), 4), "study_end": STUDY_END.date().isoformat()}
    out["predictions"] = {
        "P8 >= 5000 rows": len(rows) >= 5000,
        "P9 >= 95% ids in directory": out["joined_share"] >= 0.95,
        "P10 >= 30% moved earlier": out["earlier_share"] >= 0.30,
        "P11 F->C >= 5x C->F": cf == 0 or fc >= 5 * cf,
        "P12 F->C >= 5% of s1 carried": fc >= 0.05 * CARRIED_S1,
        "P13 median earlier shift > 30 d": out["median_earlier_shift"] > 30,
        "P14 directory agrees >= 80%": out["agree_share"] >= 0.80,
    }
    return out, joined, d


def main(dd, dirsrc, tag="session2"):
    out, joined, d = run(dd, dirsrc)
    json.dump(out, open(tag + ".json", "w"), indent=1)
    keep = [[r["id"]] + r["raw"] + [None if r["shift"] is None else round(r["shift"], 1), r["class"], r["agrees"],
                                    None if r["auto_shift"] is None else round(r["auto_shift"], 1)] for r in joined]
    json.dump({"fields": ["id", "original", "automatic", "manual", "shift_days", "class", "directory_agrees", "auto_shift_days"],
               "rows": keep}, open("rows2.json", "w"), separators=(",", ":"))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
