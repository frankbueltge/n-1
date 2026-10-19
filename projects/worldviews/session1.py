"""Project 12 session 1: the registered run (SELECTION.md). Reads the 34 editions from the scratch directory given as argv[1]."""
import json, os, random, sys, time
import numpy as np
import shapefile, shapely
from shapely.geometry import shape
import lib

POVS = ["arg", "bdg", "bra", "chn", "deu", "egy", "esp", "fra", "gbr", "grc", "idn", "ind", "iso", "isr", "ita",
        "jpn", "kor", "mar", "nep", "nld", "pak", "pol", "prt", "pse", "rus", "sau", "swe", "tlc", "tur", "twn",
        "ukr", "usa", "vnm"]
NATIONAL = [p for p in POVS if p not in ("iso", "tlc")]
KEEP = ["ADMIN", "ADM0_A3", "SOVEREIGNT", "TYPE", "NOTE_ADM0", "NOTE_BRK"]


def read(d, name):
    r = shapefile.Reader(os.path.join(d, name, name))
    fields = [f[0] for f in r.fields[1:]]
    units = []
    for sr in r.iterShapeRecords():
        rec = dict(zip(fields, sr.record))
        g = lib.project(shape(sr.shape.__geo_interface__))
        units.append(({k: rec.get(k) for k in KEEP}, g))
    return units


def main(d):
    t0 = time.time()
    base = read(d, "ne_10m_admin_0_countries")
    default = [(i, g) for i, (a, g) in enumerate(base)]
    battrs = [a for a, g in base]
    land = shapely.union_all([g for _, g in default])
    out = {"default_units": len(default), "default_land_km2": land.area, "editions": {}}
    moved_geoms = {}
    piece_rows = []
    for p in POVS:
        units = read(d, "ne_10m_admin_0_countries_" + p)
        keys = lib.match([(None, g) for _, g in units], default,
                         codes=[a["ADM0_A3"] for a, _ in units], dcodes=[a["ADM0_A3"] for a in battrs])
        mv = lib.moved([(None, g) for _, g in units], default, keys)
        geoms = [lib.polys(g) for _, _, g in mv]
        total = sum(g.area for g in geoms)
        left = sum(lib.polys(g).area for dk, ek, g in mv if ek is None)
        added = sum(lib.polys(g).area for dk, ek, g in mv if dk is None)
        u = shapely.union_all(geoms) if geoms else shapely.Polygon()
        moved_geoms[p] = (u, units, keys)
        flows = {}
        for dk, ek, g in mv:
            a = lib.polys(g).area
            if a < lib.MIN_PIECE:
                continue
            k = (battrs[dk]["ADMIN"] if dk is not None else "(none)") + " -> " + (
                battrs[ek]["ADMIN"] if isinstance(ek, int) else ("(unnamed unit)" if ek else "(none)"))
            flows[k] = flows.get(k, 0) + a
        out["editions"][p] = {"units": len(units), "moved_km2": total, "left_km2": left, "added_km2": added,
                              "flows_km2": dict(sorted(flows.items(), key=lambda x: -x[1]))}
        print(p, len(units), round(total), round(time.time() - t0), flush=True)
    contested = shapely.union_all([u for u, _, _ in moved_geoms.values()])
    out["contested_km2"] = contested.area
    pcs = lib.pieces(contested)
    out["contested_pieces"] = len(pcs)
    # owners per place on a 2 km grid inside the contested land (estimate)
    gx, gy = [], []
    for g in lib.pieces(contested, 0.0):
        minx, miny, maxx, maxy = g.bounds
        X, Y = np.meshgrid(np.arange(np.floor(minx / 2) * 2, maxx, 2.0), np.arange(np.floor(miny / 2) * 2, maxy, 2.0))
        X, Y = X.ravel(), Y.ravel()
        shapely.prepare(g)
        hit = shapely.contains_xy(g, X, Y)
        gx.append(X[hit]); gy.append(Y[hit])
    xs, ys = np.concatenate(gx), np.concatenate(gy)
    owners = [set() for _ in range(len(xs))]

    def owner_of(units_keys, xs, ys):
        units, keys = units_keys
        res = np.full(len(xs), -1)
        for (_, g), k in zip(units, keys):
            shapely.prepare(g)
            hit = shapely.contains_xy(g, xs, ys)
            res[hit] = k if isinstance(k, int) else (-3 - int(k.split(":")[1]) if k else -2)
        return res
    cols = [owner_of(([(None, g) for g in [g for _, g in default]], list(range(len(default)))), xs, ys)]
    for p in POVS:
        _, units, keys = moved_geoms[p]
        cols.append(owner_of((units, keys), xs, ys))
    M = np.column_stack(cols)
    n_owners = np.array([len(set(r)) for r in M])
    cell = 4.0
    out["owners_area_km2_estimate"] = {str(k): float((n_owners == k).sum() * cell) for k in sorted(set(n_owners.tolist()))}
    out["grid_points"] = int(len(xs))
    nat = sorted(out["editions"][p]["moved_km2"] for p in NATIONAL)
    med = (nat[len(nat) // 2 - 1] + nat[len(nat) // 2]) / 2 if len(nat) % 2 == 0 else nat[len(nat) // 2]
    E = out["editions"]
    top = max(E, key=lambda p: E[p]["moved_km2"])
    preds = [
        ("P1", "at least 30 of 33 editions move >= 100,000 km2", sum(E[p]["moved_km2"] >= 1e5 for p in POVS), lambda v: v >= 30),
        ("P2", "contested land >= 1,000,000 km2", contested.area, lambda v: v >= 1e6),
        ("P3", "Argentina's edition moves most", top, lambda v: v == "arg"),
        ("P4", ">= 10,000 km2 with 3+ owners (estimate)", float((n_owners >= 3).sum() * cell), lambda v: v >= 1e4),
        ("P5", "ISO moves less than the national median", [E["iso"]["moved_km2"], med], lambda v: v[0] < v[1]),
        ("P6", "some edition leaves >= 1,000 km2 in no unit", max(E[p]["left_km2"] for p in POVS), lambda v: v >= 1000),
        ("P7", "contested land in >= 50 pieces", len(pcs), lambda v: v >= 50),
    ]
    out["predictions"] = [{"id": i, "text": t, "value": v, "held": bool(f(v))} for i, t, v, f in preds]
    out["national_median_km2"] = med
    # reading sample: 10 largest and 20 random contested pieces, with who owns them in each edition
    random.seed(20261019)
    big = sorted(pcs, key=lambda g: -g.area)
    sample = big[:10] + random.sample(big[10:], min(20, len(big) - 10))
    rows = []
    for g in sample:
        pt = g.representative_point()
        own = {}
        for name, cu in [("default", (default, list(range(len(default)))))] + [(p, (moved_geoms[p][1], moved_geoms[p][2])) for p in POVS]:
            units, keys = cu
            k = "(none)"
            for (_, ug), kk in zip(units, keys):
                if ug.contains(pt):
                    k = battrs[kk]["ADMIN"] if isinstance(kk, int) else ("(unnamed unit)" if kk else "(unkeyed)")
                    break
            own[name] = k
        lp = lib.unproject(pt)
        rows.append({"area_km2": g.area, "lon": round(lp.x, 2), "lat": round(lp.y, 2), "owners": own})
    out["sample"] = rows
    # geometry for the page: contested pieces simplified, in lon/lat
    feats = []
    for g in big:
        s = lib.unproject(g.simplify(2.0))
        feats.append({"area_km2": round(g.area), "geom": shapely.geometry.mapping(s)})
    json.dump(feats, open("contested.json", "w"), separators=(",", ":"))
    json.dump(out, open("session1.json", "w"), indent=1, default=float)
    for r in out["predictions"]:
        print(r)
    print("contested", round(contested.area), "pieces", len(pcs), "owners", out["owners_area_km2_estimate"], round(time.time() - t0))


if __name__ == "__main__":
    main(sys.argv[1])
