"""Rules tried on invented shapes before any edition is read."""
import shapely
from shapely.geometry import box
import lib


def area(out, f):
    return sum(lib.polys(g).area for d, e, g in out if f(d, e))


def test_split_is_not_a_move():
    default = [("A", box(0, 0, 10, 10)), ("B", box(10, 0, 20, 10))]
    ed = [("A1", box(0, 0, 5, 10)), ("A2", box(5, 0, 10, 10)), ("B", box(10, 0, 20, 10))]
    assert area(lib.moved(ed, default), lambda d, e: True) == 0


def test_annexation_is_a_move():
    default = [("A", box(0, 0, 10, 10)), ("S", box(10, 0, 12, 10)), ("B", box(12, 0, 20, 10))]
    ed = [("A", box(0, 0, 12, 10)), ("B", box(12, 0, 20, 10))]
    out = lib.moved(ed, default)
    assert area(out, lambda d, e: d == "S" and e == "A") == 20
    assert area(out, lambda d, e: True) == 20


def test_left_and_added():
    default = [("A", box(0, 0, 10, 10))]
    ed = [("A", box(0, 0, 8, 12))]
    out = lib.moved(ed, default)
    assert area(out, lambda d, e: e is None) == 20
    assert area(out, lambda d, e: d is None) == 16


def test_code_key_shows_a_unit_drawn_mostly_on_anothers_land():
    # default: M holds most of the land an edition draws as S. By overlap the edition's S is keyed to M: the 60 drawn as S are
    # missed and S's own 20 are reported as moved to M (the artefact the registered run showed for Western Sahara).
    default = [("M", box(0, 0, 10, 10)), ("S", box(10, 0, 12, 10))]
    ed = [("M", box(0, 0, 4, 10)), ("S", box(4, 0, 12, 10))]
    assert area(lib.moved(ed, default), lambda d, e: d == "S" and e == "M") == 20
    keys = lib.match(ed, default, codes=["M", "S"], dcodes=["M", "S"])
    out = lib.moved(ed, default, keys)
    assert area(out, lambda d, e: d == "M" and e == "S") == 60


def test_blank_code_is_its_own_owner():
    default = [("A", box(0, 0, 10, 10))]
    ed = [("A", box(0, 0, 6, 10)), ("", box(6, 0, 10, 10))]
    keys = lib.match(ed, default, codes=["A", ""], dcodes=["A"])
    assert keys[1].startswith("unnamed:")
    assert area(lib.moved(ed, default, keys), lambda d, e: True) == 40


def test_projection_area_of_globe():
    world = lib.project(box(-180, -90, 180, 90))
    assert abs(world.area - 4 * 3.141592653589793 * lib.R ** 2) / world.area < 1e-9


if __name__ == "__main__":
    for k, v in list(globals().items()):
        if k.startswith("test_"):
            v(); print("ok", k)
