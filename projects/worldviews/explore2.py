"""Exploratory, named after the registered run was read (JOURNAL.md, session 2): the nameless land without Antarctica, as pieces
with each edition's state at one point of each piece. argv[1]: the scratch directory fetch.py wrote. Writes explore2.json and
nameless.json (simplified geometry for the page)."""
import json, sys
import shapely
from shapely.geometry import mapping
import lib
from session1 import POVS
from session2 import ALL, read_raw, fname, blank, indeterminate

d = sys.argv[1]
ed = {p: read_raw(d, fname(p)) for p in ALL}
dland = shapely.union_all([g for _, g in ed["default"]])
geoms, kinds = [], {"unnamed": [], "left": [], "indeterminate": []}
for p in ALL:
    units = ed[p]
    for rec, g in units:
        if blank(rec):
            kinds["unnamed"].append(g)
        elif indeterminate(rec) and rec.get("ADM0_A3") != "ATA":
            kinds["indeterminate"].append(g)
    if p != "default":
        left = lib.polys(shapely.difference(dland, shapely.union_all([g for _, g in units])))
        if left.area > 0:
            kinds["left"].append(left)
u = shapely.union_all(sum(kinds.values(), []))
out = {"nameless_without_antarctica_km2": u.area, "by_kind_union_km2": {k: shapely.union_all(v).area for k, v in kinds.items()},
       "pieces": []}
pcs = sorted(lib.pieces(u, 0.0), key=lambda g: -g.area)
feats = []
for pc in pcs:
    pt = pc.representative_point()
    st = {}
    for p in ALL:
        s = "(no unit)"
        for rec, g in ed[p]:
            if shapely.intersects(g, pt):
                s = "(unnamed unit)" if blank(rec) else rec["ADMIN"] + (" [indeterminate]" if indeterminate(rec) else "")
                break
        st[p] = s
    q = lib.unproject(pt)
    row = {"area_km2": pc.area, "point": [round(q.x, 3), round(q.y, 3)], "states": st,
           "editions_naming_no_one": sum(1 for v in st.values() if v in ("(no unit)", "(unnamed unit)") or v.endswith("[indeterminate]"))}
    out["pieces"].append(row)
    if pc.area >= 1.0:
        feats.append({"geom": mapping(lib.unproject(shapely.simplify(pc, 1.0))), **row})
json.dump(out, open("explore2.json", "w"), indent=1, ensure_ascii=False)
json.dump(feats, open("nameless.json", "w"), ensure_ascii=False)
print(round(out["nameless_without_antarctica_km2"]), {k: round(v) for k, v in out["by_kind_union_km2"].items()}, len(pcs), len(feats))
for r in out["pieces"][:25]:
    print(round(r["area_km2"]), r["point"], r["editions_naming_no_one"], sorted(set(r["states"].values()))[:6])
