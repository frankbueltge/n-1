"""Exploratory (after the registered run): who owns each contested piece in each of the 34 editions.

Reads contested.json (session1.py) and the editions from argv[1]. One point per piece: the representative point of the piece as
simplified for the page; a piece whose point all 34 editions give to one owner is flagged (the point fell outside the true piece).
Writes pieces.json (owners per piece) and land.json (the default edition's units, simplified, for drawing).
"""
import json, os, sys
import numpy as np
import shapefile, shapely
from shapely.geometry import shape
import lib
from session1 import POVS, read


def main(d):
    feats = json.load(open("contested.json"))
    pts = [lib.project(shape(f["geom"]).representative_point()) for f in feats]
    xs = np.array([p.x for p in pts]); ys = np.array([p.y for p in pts])
    base = read(d, "ne_10m_admin_0_countries")
    default = [(i, g) for i, (a, g) in enumerate(base)]
    names = [a["ADMIN"] for a, g in base]

    def owners(units, _keys):
        res = ["(none)"] * len(xs)
        for a, g in units:
            shapely.prepare(g)
            for i in np.nonzero(shapely.contains_xy(g, xs, ys))[0]:
                res[i] = a["ADMIN"] or "(unnamed unit)"
        return res
    cols = {"default": owners(base, None)}
    for p in POVS:
        units = read(d, "ne_10m_admin_0_countries_" + p)
        cols[p] = owners(units, None)
    out = []
    for i, f in enumerate(feats):
        own = {e: cols[e][i] for e in cols}
        out.append({"area_km2": f["area_km2"], "owners": own, "distinct": len(set(own.values()))})
    json.dump(out, open("pieces.json", "w"), indent=0)
    land = []
    for (a, g) in base:
        s = shapely.set_precision(lib.unproject(g.simplify(12.0)), 0.01)
        if not s.is_empty:
            land.append({"name": a["ADMIN"], "geom": shapely.geometry.mapping(s)})
    json.dump(land, open("land.json", "w"), separators=(",", ":"))
    print(len(out), sum(1 for r in out if r["distinct"] == 1), "flagged")


if __name__ == "__main__":
    main(sys.argv[1])
