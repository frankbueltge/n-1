"""Exploratory check of explore1's 'drawn alike': who each of the 34 editions draws at one point inside six large features. argv[1]: editions dir."""
import json, sys
from collections import Counter
import shapely
from shapely.geometry import Point
import lib
from session1 import POVS, read

PTS = {"W. Sahara (Disputed, west of the berm), near Laayoune": (-13.2, 27.15), "Donetsk People's Republic, near Donetsk": (37.8, 48.0),
       "Abkhazia, near Sukhumi": (41.0, 43.0), "South Ossetia, near Tskhinvali": (43.95, 42.25),
       "Artsakh, near Stepanakert": (46.75, 39.82), "Israel (Disputed feature), near Tel Aviv": (34.85, 32.1)}
pts = {k: lib.project(Point(*v)) for k, v in PTS.items()}
res = {k: {} for k in PTS}
for name in ["ne_10m_admin_0_countries"] + ["ne_10m_admin_0_countries_" + p for p in POVS]:
    units = read(sys.argv[1], name)
    ed = "default" if name.endswith("countries") else name[-3:]
    for k, p in pts.items():
        res[k][ed] = next((a["ADMIN"] for a, g in units if g.contains(p)), "(none)")
out = {k: {"lonlat": PTS[k], "owners": dict(Counter(v.values())), "by_edition": v} for k, v in res.items()}
json.dump(out, open("explore1b.json", "w"), indent=1, ensure_ascii=False)
for k, v in out.items():
    print(k, v["owners"])
