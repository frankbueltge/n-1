"""Session 3, as registered in SESSION3.md. Inputs: the scratch directories fetch2.py and fetch.py wrote."""
import json, os, statistics, sys
from collections import Counter
from session2 import run
from lib import parse as parse_dir
from lib3 import dclass, direction

CARRIED_S1, TOTAL_S1 = 6607633, None


def old_rows(dd):
    out = {}
    p = os.path.join(dd, "dirfl_10001_15000.old")
    for line in open(p, encoding="latin-1"):
        r = parse_dir(line) if line.strip() else None
        if r and r["id"] not in out:
            out[r["id"]] = r
    return out


def run3(dd, dirsrc):
    s2, joined, d = run(dd, dirsrc)
    pop = [r for r in joined if r["agrees"] is False]
    for r in pop:
        x = d[r["id"]]
        r["dclass"] = dclass(r, x)
        r["dir"] = direction(r, x, r["dclass"])
    cls = Counter(r["dclass"] for r in pop)
    n = len(pop)
    dirs = [r["dir"] for r in pop if r["dir"] is not None]
    more = [v for v in dirs if v > 1]
    less = [v for v in dirs if v < -1]
    era = lambda r: "2005-2010" if d[r["id"]]["start"].year >= 2005 else "before 2005"
    tot = Counter(era(r) for r in joined)
    dis = Counter(era(r) for r in pop)
    share = {k: round(dis[k] / tot[k], 4) for k in tot}
    # exploratory (a): the .old directory file
    old = old_rows(dd)
    from lib2 import effective
    from lib3 import near
    def old_carries(r):
        o = old[r["id"]]
        if r["manual"] == "still_on":
            return o["drogue_d"].replace("/", "").strip("0") == ""
        return near(r["manual"], o["drogue"])
    inold = [r for r in pop if r["id"] in old]
    oc = Counter(old_carries(r) for r in inold)
    oldcls = Counter(dclass(r, old[r["id"]]) for r in inold if not old_carries(r))
    out = {"population": n, "classes": dict(cls), "class_share": {k: round(v / n, 4) for k, v in cls.items()},
           "with_direction": len(dirs), "more_following": len(more), "less_following": len(less),
           "held_within_1_day": len(dirs) - len(more) - len(less),
           "days_more_following": round(sum(more)), "days_less_following": round(-sum(less)),
           "median_more_following": round(statistics.median(more), 1) if more else None,
           "disagree_share_by_era": share, "joined_by_era": dict(tot),
           "explore_a_old_file": {"in_old": len(inold), "old_carries_manual": oc[True], "old_does_not": oc[False],
                                  "old_class_when_not": dict(oldcls)},
           "explore_b": {"net_days_more_following": round(sum(dirs)),
                         "s1_carried": CARRIED_S1, "s1_carried_plus_net": CARRIED_S1 + round(sum(dirs))}}
    out["predictions"] = {
        "P15 >= 25% unknown": cls["unknown"] / n >= 0.25,
        "P16 < 10% original": cls["original"] / n < 0.10,
        "P17 >= 20% automatic": cls["automatic"] / n >= 0.20,
        "P18 > half of directed point to more following": len(more) > len(dirs) / 2,
        "P19 disagree share 2005-2010 > before 2005": share["2005-2010"] > share["before 2005"],
    }
    return out, pop, d, old


def main(dd, dirsrc, tag="session3"):
    out, pop, d, old = run3(dd, dirsrc)
    json.dump(out, open(tag + ".json", "w"), indent=1)
    keep = [[r["id"]] + r["raw"] + [d[r["id"]]["drogue_d"], r["dclass"], None if r["dir"] is None else round(r["dir"], 1)] for r in pop]
    json.dump({"fields": ["id", "original", "automatic", "manual", "directory_drogue_off", "directory_says", "days_more_following"],
               "rows": keep}, open("rows3.json", "w"), separators=(",", ":"))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
