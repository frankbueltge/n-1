"""Reading rule of SELECTION.md: 40 random drifters against their raw rows; the 10 longest-carried in full."""
import json, os, random, sys
from lib import parse, status, days
from fetch import FILES


def main(src):
    raw = []
    for f in FILES:
        raw += [l.rstrip("\n") for l in open(os.path.join(src, f), encoding="latin-1") if l.strip()]
    rnd = random.Random(20261018).sample(raw, 40)
    out = {"random": [], "longest_carried": []}
    for l in rnd:
        r = parse(l)
        out["random"].append({"raw": " ".join(l.split()), "status": status(r), "days": days(r)})
    rows = [parse(l) for l in raw]
    rows = [r for r in rows if days(r) is not None]
    rows.sort(key=lambda r: -days(r)[1])
    for r in rows[:10]:
        out["longest_carried"].append({"id": r["id"], "type": r["type"], "start": r["start_d"], "end": r["end_d"],
                                       "drogue_off": r["drogue_d"], "from": [r["start_lat"], r["start_lon"]],
                                       "to": [r["end_lat"], r["end_lon"]], "death": r["death"], "status": status(r),
                                       "drogued_days": round(days(r)[0], 1), "carried_days": round(days(r)[1], 1)})
    json.dump(out, open("verify.json", "w"), indent=1)
    for x in out["random"]:
        print(x["status"], [None if x["days"] is None else round(v, 1) for v in (x["days"] or [])], "|", x["raw"])
    for x in out["longest_carried"]:
        print(x)


if __name__ == "__main__":
    main(sys.argv[1])
