"""Rules for project 12, fixed before the editions are read in bulk (SELECTION.md).

Geometry is projected to a cylindrical equal-area plane on the authalic sphere (x = R*lon, y = R*sin(lat), km),
so a planar area there is an area on the sphere. Straight segments in that plane are not geodesics: areas are
estimates at the 10m scale's vertex density.
"""
import math
import numpy as np
import shapely
from shapely.strtree import STRtree

R = 6371.0072  # km, authalic radius of WGS84
MIN_PIECE = 1.0  # km2: a moved piece smaller than this is counted in area but not as a piece


def project(geom):
    def f(c):
        lon = np.radians(c[:, 0])
        lat = np.radians(np.clip(c[:, 1], -90, 90))
        return np.column_stack([R * lon, R * np.sin(lat)])
    return shapely.make_valid(shapely.transform(geom, f))


def unproject(geom):
    def f(c):
        return np.column_stack([np.degrees(c[:, 0] / R), np.degrees(np.arcsin(np.clip(c[:, 1] / R, -1, 1)))])
    return shapely.transform(geom, f)


def match(units, default_units, codes=None, dcodes=None):
    """Key each unit of an edition to a default unit (its owner key).

    Registered rule: the default unit it overlaps most; None if it overlaps none. Correction of 2026-10-19 (JOURNAL.md, 01:55),
    used when codes are given: a unit whose ADM0_A3 equals a default unit's is keyed to that unit; a unit with a blank code is its
    own key ('unnamed:i'); only the rest fall back to the largest overlap. The registered rule keyed an edition's Western Sahara
    (mostly land the default draws in Morocco) to Morocco, hiding the move.
    """
    tree = STRtree([g for _, g in default_units])
    bycode = {}
    if dcodes is not None:
        for (dk, _), c in zip(default_units, dcodes):
            if c:
                bycode.setdefault(c, dk)
    keys = []
    for j, (_, g) in enumerate(units):
        if codes is not None:
            c = (codes[j] or "").strip()
            if not c:
                keys.append("unnamed:%d" % j)
                continue
            if c in bycode:
                keys.append(bycode[c])
                continue
        best, best_a = None, 0.0
        for i in tree.query(g):
            a = shapely.area(shapely.intersection(g, default_units[i][1]))
            if a > best_a:
                best, best_a = default_units[i][0], a
        keys.append(best)
    return keys


def moved(units, default_units, keys=None):
    """Pieces of land whose owner in the edition differs from the default.

    Returns a list of (default_key, edition_key, geometry). edition_key None = land of a default unit lying in
    no unit of the edition ('left'); default_key None = edition land lying in no default unit ('added').
    Fast path (same definition): a default unit whose edition counterpart (the union of edition units keyed to it)
    is geometrically identical moves nothing and is skipped.
    """
    if keys is None:
        keys = match(units, default_units)
    dmap = dict(default_units)
    by_key = {}
    for (_, g), k in zip(units, keys):
        by_key.setdefault(k, []).append(g)
    etree = STRtree([g for _, g in units])
    dtree = STRtree([g for _, g in default_units])
    out = []
    for dk, dg in default_units:
        mine = by_key.get(dk, [])
        eg = mine[0] if len(mine) == 1 else (shapely.union_all(mine) if mine else shapely.Polygon())
        if len(mine) == 1 and shapely.equals_exact(shapely.normalize(eg), shapely.normalize(dg), 0.0):
            continue
        lost = polys(shapely.difference(dg, eg)) if mine else dg
        if lost.area > 0:
            given = []
            for i in etree.query(lost):
                if keys[i] == dk:
                    continue
                inter = polys(shapely.intersection(lost, units[i][1]))
                if inter.area > 0:
                    out.append((dk, keys[i], inter))
                    given.append(inter)
            rest = polys(shapely.difference(lost, shapely.union_all(given))) if given else lost
            if rest.area > 0:
                out.append((dk, None, rest))
        if mine:
            gained = polys(shapely.difference(eg, dg))
            if gained.area > 0:
                near = [default_units[i][1] for i in dtree.query(gained) if default_units[i][0] != dk]
                extra = polys(shapely.difference(gained, shapely.union_all(near))) if near else gained
                if extra.area > 0:
                    out.append((None, dk, extra))
    for (_, g), k in zip(units, keys):
        if k is None:
            out.append((None, None, g))
    return out


def pieces(geom, min_area=MIN_PIECE):
    parts = list(getattr(geom, "geoms", [geom]))
    return [p for p in parts if p.geom_type == "Polygon" and p.area >= min_area]


def polys(geom):
    """Polygonal part only (intersections can return lines and points)."""
    if geom.geom_type in ("Polygon", "MultiPolygon"):
        return geom
    ps = [g for g in getattr(geom, "geoms", []) if g.geom_type in ("Polygon", "MultiPolygon")]
    return shapely.union_all(ps) if ps else shapely.Polygon()
