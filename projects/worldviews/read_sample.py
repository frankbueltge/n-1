"""Reading rule (SELECTION.md): the 30 sampled pieces against Natural Earth's breakaway-and-disputed-areas file. argv[1]: its .shp stem."""
import json, sys
import shapefile
from shapely.geometry import shape, Point
from collections import Counter

r = shapefile.Reader(sys.argv[1])
fields = [f[0] for f in r.fields[1:]]
feats = [(dict(zip(fields, sr.record)), shape(sr.shape.__geo_interface__)) for sr in r.iterShapeRecords()]
d = json.load(open("session1.json"))
out = []
for i, s in enumerate(d["sample"]):
    p = Point(s["lon"], s["lat"])
    hits = [a for a, g in feats if g.buffer(0).contains(p)]
    out.append({"i": i, "area_km2": round(s["area_km2"]), "lon": s["lon"], "lat": s["lat"],
                "owners": dict(Counter(s["owners"].values())),
                "disputed_feature": [{k: a.get(k) for k in ("BRK_NAME", "NOTE_BRK", "TYPE") if k in a} for a in hits]})
json.dump(out, open("verify.json", "w"), indent=1, ensure_ascii=False)
print(sum(1 for o in out if o["disputed_feature"]), "of", len(out), "inside a disputed-areas feature")
for o in out:
    print(o["i"], o["area_km2"], [f.get("BRK_NAME") for f in o["disputed_feature"]])
