"""Session 2's reading rule (SESSION2.md): raw records of the unnamed units, and the left pieces no disputed feature explains.
argv[1]: the scratch directory fetch.py wrote."""
import json, os, sys
import shapefile, shapely
from shapely.geometry import shape, Point
import lib

d = sys.argv[1]
s = json.load(open("session2.json"))
out = {"unnamed_raw": [], "unexplained_left": []}
for p in ("pse", "rus"):
    n = "ne_10m_admin_0_countries_" + p
    r = shapefile.Reader(os.path.join(d, n, n))
    fields = [f[0] for f in r.fields[1:]]
    for u in [x for x in s["unnamed_units"] if x["edition"] == p]:
        rec = r.record(u["index"])
        vals = dict(zip(fields, rec))
        nonblank = {k: v for k, v in vals.items() if str(v).strip() not in ("", "0", "-99", "None", "0.0", "-99.0")}
        out["unnamed_raw"].append({"edition": p, "index": u["index"], "fields": len(fields), "nonblank": nonblank})
for lp in [x for x in s["left_pieces"] if not x["disputed_features"]]:
    p = lp["edition"]
    n = "ne_10m_admin_0_countries_" + p
    r = shapefile.Reader(os.path.join(d, n, n))
    fields = [f[0] for f in r.fields[1:]]
    lon, lat = lp["point"]
    pt = lib.project(Point(lon, lat))
    near = []
    for sr in r.iterShapeRecords():
        g = lib.project(shape(sr.shape.__geo_interface__))
        dist = g.distance(pt)
        if dist < 60:
            rec = dict(zip(fields, sr.record))
            near.append({"ADMIN": rec["ADMIN"], "TYPE": rec["TYPE"], "km": round(dist, 1)})
    out["unexplained_left"].append({**lp, "edition_units_within_60km": near})
json.dump(out, open("verify2.json", "w"), indent=1, ensure_ascii=False, default=str)
for x in out["unnamed_raw"]:
    print(x["edition"], x["index"], x["fields"], x["nonblank"])
for x in out["unexplained_left"]:
    print(x["edition"], round(x["area_km2"]), x["point"], x["edition_units_within_60km"])
