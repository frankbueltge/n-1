"""Exploratory (named in SESSION3.md, run after the reading): (a) for every country whose own map gives it land, what each edition
names at a point of the largest such part; (b) the default's countries without an edition: area in each of the 34, and the spread
(largest minus median, median over all 34). Writes explore3.json."""
import json, sys
from collections import Counter
import numpy as np
import shapely
from shapely.geometry import shape
import lib
from session1 import POVS, NATIONAL, read
from session3 import CODES, drawing
from read3 import names_at


def main(d):
    eds = {"default": read(d, "ne_10m_admin_0_countries")}
    for p in POVS:
        eds[p] = read(d, "ne_10m_admin_0_countries_" + p)
    for units in eds.values():
        for _, g in units:
            shapely.prepare(g)
    maps = json.load(open("selfmaps.json"))
    out = {"largest_part_names": {}, "without_edition": {}}
    for x, m in maps.items():
        if not m["only"]:
            continue
        g = lib.project(shape(m["only"]))
        big = max(getattr(g, "geoms", [g]), key=lambda p: p.area)
        names = names_at(eds, big.representative_point())
        out["largest_part_names"][x] = {"part_km2_simplified": round(big.area), "tally": Counter(names.values()).most_common(),
                                        "own": names[x], "default": names["default"]}
    mine = set(CODES.values())
    codes = sorted({(a["ADM0_A3"] or "").strip() for a, _ in eds["default"]} - mine - {""})
    for code in codes:
        areas = [drawing(eds[e], code).area for e in eds]
        med = float(np.median(areas))
        name = [a["ADMIN"] for a, _ in eds["default"] if a["ADM0_A3"] == code][0]
        out["without_edition"][code] = {"name": name, "median_km2": round(med), "max_km2": round(max(areas)),
                                        "min_km2": round(min(areas)), "spread_km2": round(max(areas) - med)}
    json.dump(out, open("explore3.json", "w"), indent=1)
    for x, r in out["largest_part_names"].items():
        print(x, r["part_km2_simplified"], r["tally"])
    w = sorted(out["without_edition"].items(), key=lambda kv: -kv[1]["spread_km2"])[:12]
    for k, r in w:
        print(k, r)


if __name__ == "__main__":
    main(sys.argv[1])
