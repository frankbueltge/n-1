"""Session 2's rules tried on invented records and shapes before reading (SESSION2.md)."""
import shapely
from shapely.geometry import box
import lib
from session2 import blank, indeterminate, under

assert blank({"ADMIN": "", "ADM0_A3": ""}) and blank({"ADMIN": None, "ADM0_A3": "  "})
assert not blank({"ADMIN": "X", "ADM0_A3": ""}) and not blank({"ADMIN": "", "ADM0_A3": "XXX"})
assert indeterminate({"TYPE": "Indeterminate"}) and not indeterminate({"TYPE": "Sovereign country"})
# land left: default land minus the union of the edition's units
dland = shapely.union_all([box(0, 0, 10, 10), box(10, 0, 20, 10)])
left = lib.polys(shapely.difference(dland, shapely.union_all([box(0, 0, 10, 10), box(10, 0, 15, 10)])))
assert abs(left.area - 50) < 1e-9
# under: names of an edition's units beneath a shape, unnamed units named as such
units = [({"ADMIN": "A", "ADM0_A3": "AAA"}, box(0, 0, 10, 10)), ({"ADMIN": "", "ADM0_A3": ""}, box(10, 0, 20, 10))]
c = under(box(5, 0, 15, 10), units)
assert abs(c["A"] - 50) < 1e-9 and abs(c["(unnamed unit)"] - 50) < 1e-9
assert under(box(5, 0, 15, 10), units, skip=1).get("(unnamed unit)") is None
print("ok")
