"""Session 3's rules tried on invented shapes, before any edition is read for them."""
import shapely
from shapely.geometry import box
from session3 import compare, lattice


def test():
    core = box(0, 0, 100, 100)
    claim = box(100, 0, 120, 100)  # 2,000 km2 only the own map draws
    lost = box(0, 0, 10, 100)      # 1,000 km2 the own map leaves out, all others draw
    own = shapely.union(shapely.difference(core, lost), claim)
    others = [core] * 33
    r, only, wh = compare(own, others)
    assert abs(r["own_km2"] - 11000) < 1e-6 and r["median_km2"] == 10000 and abs(r["excess_km2"] - 1000) < 1e-6
    assert abs(r["only_own_km2"] - 2000) < 1e-6, r
    assert abs(r["withheld_km2"] - 1000) < 1e-6, r
    # a claim 17 others share is not 'only its own'
    others2 = [shapely.union(core, claim)] * 17 + [core] * 16
    r2, _, _ = compare(shapely.union(core, claim), others2)
    assert r2["only_own_km2"] == 0 and r2["withheld_km2"] == 0
    # 16 others share it: still 'only its own map' by the registered threshold
    others3 = [shapely.union(core, claim)] * 16 + [core] * 17
    r3, _, _ = compare(shapely.union(core, claim), others3)
    assert abs(r3["only_own_km2"] - 2000) < 1e-6
    # all agree: nothing to count; empty drawings allowed
    r4, _, _ = compare(core, [core] * 32 + [shapely.Polygon()])
    assert r4["median_km2"] == 10000 and r4["only_own_km2"] == 0
    # lattice laid per part: two far boxes, no points between
    X, Y = lattice(shapely.union(box(0, 0, 4, 4), box(10000, 0, 10004, 4)))
    assert len(X) == 8
    print("ok")


if __name__ == "__main__":
    test()
