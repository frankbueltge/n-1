"""Exploratory (named after the reading rule showed every sampled piece inside a disputed-areas feature): which of Natural Earth's
breakaway-and-disputed features hold contested land, and which are drawn alike in all 34 editions. argv[1]: the features' .shp stem.
Contested land is taken from contested.json (simplified for the page): areas are estimates."""
import json, sys
import shapefile, shapely
from shapely.geometry import shape
import lib

r = shapefile.Reader(sys.argv[1])
fields = [f[0] for f in r.fields[1:]]
feats = [(dict(zip(fields, sr.record)), lib.project(shape(sr.shape.__geo_interface__))) for sr in r.iterShapeRecords()]
cont = shapely.union_all([lib.project(shape(f["geom"])) for f in json.load(open("contested.json"))])
rows = []
for a, g in feats:
    inter = lib.polys(shapely.intersection(g, cont)).area
    rows.append({"name": a.get("BRK_NAME"), "type": a.get("TYPE"), "area_km2": round(g.area, 1), "contested_km2": round(inter, 1),
                 "share": round(inter / g.area, 3) if g.area else None})
rows.sort(key=lambda x: -x["area_km2"])
inside = shapely.union_all([g for _, g in feats])
out = {"features": len(rows), "with_contested_land": sum(1 for x in rows if x["share"] and x["share"] > 0.01),
       "drawn_alike": [x["name"] for x in rows if not x["share"] or x["share"] <= 0.01],
       "contested_outside_features_km2": round(lib.polys(shapely.difference(cont, inside)).area, 1),
       "rows": rows}
json.dump(out, open("explore1.json", "w"), indent=1, ensure_ascii=False)
print(out["features"], out["with_contested_land"], out["contested_outside_features_km2"])
print("drawn alike:", out["drawn_alike"])
