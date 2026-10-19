"""Session 3's reading rule (SESSION3.md), and the exact drawing of 'land only its own map gives it' for the work.

Reads the editions from argv[1] and session3.json. The 33 other drawings of a country fall into a few distinct geometries; laying
those few over one another gives the land covered by each count of editions exactly (no lattice), which checks the registered
lattice estimate. Writes verify3.json (the reading) and selfmaps.json (simplified lon/lat drawings for the pages)."""
import json, random, sys
import numpy as np
import shapely
from shapely.geometry import mapping
import lib
from session1 import POVS, NATIONAL, read
from session3 import CODES, drawing, HALF


def distinct(geoms):
    """[(geometry, how many of the given drawings are exactly it)]"""
    out = []
    for g in geoms:
        for i, (h, n) in enumerate(out):
            if shapely.equals_exact(shapely.normalize(g), shapely.normalize(h), 0.0):
                out[i] = (h, n + 1)
                break
        else:
            out.append((g, 1))
    return out


def coverage(own, others):
    """Exact: the land of own covered by at most HALF of the others, and the land outside own covered by at least HALF+1."""
    groups = distinct(others)
    universe = shapely.union_all([own] + [g for g, _ in groups])
    cells = [(universe, 0)]
    for g, n in groups:
        nxt = []
        for c, k in cells:
            a = lib.polys(shapely.intersection(c, g))
            b = lib.polys(shapely.difference(c, g))
            if a.area > 0:
                nxt.append((a, k + n))
            if b.area > 0:
                nxt.append((b, k))
        cells = nxt
    low = shapely.union_all([c for c, k in cells if k <= HALF]) if cells else shapely.Polygon()
    high = shapely.union_all([c for c, k in cells if k >= HALF + 1]) if cells else shapely.Polygon()
    only = lib.polys(shapely.intersection(own, low))
    withheld = lib.polys(shapely.difference(high, own))
    majority = high
    return only, withheld, majority, len(groups)


def ll(g, tol):
    s = shapely.set_precision(lib.unproject(g.simplify(tol)), 0.01)
    return mapping(s) if not s.is_empty else None


def names_at(eds, pt):
    x, y = pt.x, pt.y
    res = {}
    for e, units in eds.items():
        n = "(no unit)"
        for a, g in units:
            if shapely.contains_xy(g, x, y):
                n = a["ADMIN"] or "(unnamed unit)"
                break
        res[e] = n
    return res


def main(d):
    s3 = json.load(open("session3.json"))
    c = s3["countries"]
    eds = {"default": read(d, "ne_10m_admin_0_countries")}
    for p in POVS:
        eds[p] = read(d, "ne_10m_admin_0_countries_" + p)
    for units in eds.values():
        for _, g in units:
            shapely.prepare(g)
    top5 = sorted(c, key=lambda x: -c[x]["excess_km2"])[:5]
    low = min(c[x]["excess_km2"] for x in c)
    rest = [x for x in sorted(c) if x not in top5]
    rnd = random.Random(20261019).sample(rest, 5)
    read_set = top5 + ["ukr"] + [x for x in rnd if x != "ukr"]
    verify = {"top5": top5, "lowest_excess_km2": low, "lowest_note": "no negative excess; 16 share 0; Ukraine read in its place, the one of them whose own drawing differs from the default's",
              "random5": rnd, "countries": {}}
    maps = {}
    for x in NATIONAL:
        code = CODES[x]
        G = {e: drawing(eds[e], code) for e in eds}
        others = [G[e] for e in eds if e != x]
        only, withheld, majority, ngroups = coverage(G[x], others)
        row = {"only_own_exact_km2": only.area, "withheld_exact_km2": withheld.area,
               "only_own_lattice_km2": c[x]["only_own_km2"], "distinct_other_drawings": ngroups}
        tol = 8.0 if G[x].area > 1e6 else 2.0
        maps[x] = {"own": ll(G[x], tol), "others": ll(majority, tol), "only": ll(only, 1.0) if only.area > 0 else None,
                   "own_km2": round(G[x].area), "median_km2": round(c[x]["median_km2"]), "only_km2": round(only.area),
                   "default_km2": round(c[x]["default_km2"])}
        if x in read_set:
            recs = [{k: a[k] for k in ("ADMIN", "ADM0_A3", "TYPE", "SOVEREIGNT")} for a, g in eds[x] if (a["ADM0_A3"] or "").strip() == code]
            row["own_records"] = recs
            row["areas_km2"] = {e: round(v) for e, v in c[x]["areas_km2"].items()}
            if only.area > 0:
                parts = sorted(getattr(only, "geoms", [only]), key=lambda g: -g.area)
                big = parts[0]
                pt = big.representative_point()
                lp = lib.unproject(pt)
                row["only_parts"] = len(parts)
                row["largest_part_km2"] = big.area
                row["largest_part_point"] = [round(lp.x, 3), round(lp.y, 3)]
                row["names_there"] = names_at(eds, pt)
            verify["countries"][x] = row
        print(x, round(only.area), round(withheld.area), round(c[x]["only_own_km2"]), ngroups, flush=True)
    # the two rare names not self-named: what the named country's own edition calls the piece
    pieces = json.load(open("pieces.json"))
    verify["not_self_named"] = [{"piece": r["piece"], "name": r["name"], "editions": r["editions"],
                                 "area_km2": r["area_km2"], "owners": pieces[r["piece"]]["owners"]}
                                for r in s3["rare_names"] if not r["self"]]
    json.dump(verify, open("verify3.json", "w"), indent=1)
    json.dump(maps, open("selfmaps.json", "w"), separators=(",", ":"))


if __name__ == "__main__":
    main(sys.argv[1])
