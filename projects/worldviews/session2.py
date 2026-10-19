"""Project 12 session 2: the registered run (SESSION2.md). Nameless land in the 34 editions.

argv[1]: the scratch directory fetch.py wrote; argv[2]: the .shp stem of Natural Earth's breakaway-and-disputed-areas file.
(a) unnamed unit: blank ADMIN and blank ADM0_A3. (b) land left: default land in no unit of the edition -- the default's land
minus the union of the edition's units, which is lib.moved's 'left' summed over default units. (c) a unit whose TYPE reads
'Indeterminate'.
"""
import json, os, sys, time
from collections import Counter
import shapefile, shapely
from shapely.geometry import shape
import lib
from session1 import POVS

ALL = ["default"] + POVS


def read_raw(d, name):
    r = shapefile.Reader(os.path.join(d, name, name))
    fields = [f[0] for f in r.fields[1:]]
    out = []
    for sr in r.iterShapeRecords():
        rec = dict(zip(fields, sr.record))
        out.append((rec, lib.project(shape(sr.shape.__geo_interface__))))
    return out


def fname(p):
    return "ne_10m_admin_0_countries" + ("" if p == "default" else "_" + p)


def blank(rec):
    return not str(rec.get("ADMIN") or "").strip() and not str(rec.get("ADM0_A3") or "").strip()


def indeterminate(rec):
    return str(rec.get("TYPE") or "").strip().lower() == "indeterminate"


def rep(g):
    p = lib.unproject(g.representative_point())
    return [round(p.x, 3), round(p.y, 3)]


def under(g, units, skip=None):
    """Names (ADMIN, or '(unnamed unit)') of the units of one edition lying under g, with km2."""
    out = Counter()
    for j, (rec, ug) in enumerate(units):
        if j == skip or not shapely.intersects(g, ug):
            continue
        a = lib.polys(shapely.intersection(g, ug)).area
        if a >= lib.MIN_PIECE:
            out["(unnamed unit)" if blank(rec) else rec["ADMIN"]] += a
    return out


def main(d, disp):
    t0 = time.time()
    ed = {p: read_raw(d, fname(p)) for p in ALL}
    print("read", round(time.time() - t0), flush=True)
    dr = shapefile.Reader(disp)
    dfields = [f[0] for f in dr.fields[1:]]
    dfeats = [(dict(zip(dfields, sr.record)), lib.project(shape(sr.shape.__geo_interface__))) for sr in dr.iterShapeRecords()]
    default = ed["default"]
    dland = shapely.union_all([g for _, g in default])
    out = {"editions": {}, "unnamed_units": [], "left_pieces": [], "indeterminate_units": []}
    nameless = []
    for p in ALL:
        units = ed[p]
        a_geoms = [g for rec, g in units if blank(rec)]
        c_geoms = [g for rec, g in units if indeterminate(rec)]
        left = lib.polys(shapely.difference(dland, shapely.union_all([g for _, g in units]))) if p != "default" else shapely.Polygon()
        out["editions"][p] = {"units": len(units), "unnamed_units": len(a_geoms), "unnamed_km2": sum(g.area for g in a_geoms),
                              "left_km2": left.area, "left_pieces_1km2": len(lib.pieces(left)),
                              "indeterminate_units": len(c_geoms), "indeterminate_km2": sum(g.area for g in c_geoms)}
        nameless += a_geoms + c_geoms + ([left] if left.area > 0 else [])
        for j, (rec, g) in enumerate(units):
            if blank(rec):
                others = {}
                for q in ALL:
                    if q == p:
                        continue
                    c = under(g, ed[q])
                    if c:
                        top, ta = c.most_common(1)[0]
                        others[q] = {"name": top, "share": round(ta / g.area, 3), "names": len(c)}
                    else:
                        others[q] = {"name": "(no unit)", "share": 1.0, "names": 0}
                out["unnamed_units"].append({
                    "edition": p, "index": j, "record": {k: (v if isinstance(v, (int, float, str)) or v is None else str(v))
                                                         for k, v in rec.items()},
                    "area_km2": g.area, "point": rep(g),
                    "default_under": {k: round(v, 1) for k, v in under(g, default).most_common()},
                    "others": others,
                    "others_names": dict(Counter(o["name"] for o in others.values()).most_common())})
            if indeterminate(rec):
                out["indeterminate_units"].append({"edition": p, "name": rec.get("ADMIN"), "code": rec.get("ADM0_A3"),
                                                   "sovereignt": rec.get("SOVEREIGNT"), "area_km2": g.area, "point": rep(g)})
        for pc in lib.pieces(left, 1000.0):
            out["left_pieces"].append({
                "edition": p, "area_km2": pc.area, "point": rep(pc),
                "default_under": {k: round(v, 1) for k, v in under(pc, default).most_common()},
                "disputed_features": [a.get("BRK_NAME") for a, fg in dfeats
                                      if shapely.intersects(pc, fg) and lib.polys(shapely.intersection(pc, fg)).area >= 1.0]})
        print(p, out["editions"][p]["unnamed_units"], round(out["editions"][p]["left_km2"]),
              out["editions"][p]["indeterminate_units"], round(time.time() - t0), flush=True)
    u = shapely.union_all(nameless)
    out["nameless_km2"] = u.area
    out["nameless_pieces_1km2"] = len(lib.pieces(u))
    E = out["editions"]
    pse = [x for x in out["unnamed_units"] if x["edition"] == "pse"]
    rus = [x for x in out["unnamed_units"] if x["edition"] == "rus"]
    pse_isr = sum(x["default_under"].get("Israel", 0) for x in pse)
    pse_tot = sum(x["area_km2"] for x in pse)
    iso_left = [x["area_km2"] for x in out["left_pieces"] if x["edition"] == "iso"]
    iso_all = [pc.area for pc in lib.pieces(lib.polys(shapely.difference(dland, shapely.union_all([g for _, g in ed["iso"]]))), 0.0)]
    preds = {
        "P8 nameless land >= 800,000 km2": out["nameless_km2"] >= 800000,
        "P9 >= 6 editions besides ISO leave >= 1 km2 in no unit": sum(1 for p in POVS if p != "iso" and E[p]["left_km2"] >= 1) >= 6,
        "P10 > half of pse unnamed area on the default's Israel": pse_tot > 0 and pse_isr > pse_tot / 2,
        "P11 no unnamed unit > 100,000 km2": all(x["area_km2"] <= 100000 for x in out["unnamed_units"]),
        "P12 rus unnamed units on >= 3 distinct default units": len({k for x in rus for k in x["default_under"]}) >= 3,
        "P13 default types >= 3 units Indeterminate": E["default"]["indeterminate_units"] >= 3,
        "P14 > half of ISO's left land in one piece": bool(iso_all) and max(iso_all) > sum(iso_all) / 2,
    }
    out["predictions"] = preds
    out["checks"] = {"pse_unnamed_km2": pse_tot, "pse_on_israel_km2": pse_isr, "iso_left_largest_km2": max(iso_all) if iso_all else 0,
                     "iso_left_km2": sum(iso_all), "rus_default_under": sorted({k for x in rus for k in x["default_under"]})}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "session2.json"), "w"), indent=1,
              ensure_ascii=False, default=str)
    for k, v in preds.items():
        print(k, v)
    print("done", round(time.time() - t0))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
