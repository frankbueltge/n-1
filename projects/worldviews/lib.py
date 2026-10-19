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


def match(units, default_units):
    """Key each unit of an edition to the default unit it overlaps most (its owner key). None if it overlaps none."""
    tree = STRtree([g for _, g in default_units])
    keys = []
    for _, g in units:
        best, best_a = None, 0.0
        for i in tree.query(g):
            a = shapely.area(shapely.intersection(g, default_units[i][1]))
            if a > best_a:
                best, best_a = default_units[i][0], a
        keys.append(best)
    return keys


def moved(units, default_units):
    """Pieces of land whose owner in the edition differs from the default.

    Returns a list of (default_key, edition_key, geometry). edition_key None = land of a default unit lying in
    no unit of the edition ('left'); default_key None = edition land lying in no default unit ('added').
    """
    keys = match(units, default_units)
    out = []
    tree = STRtree([g for _, g in units])
    for dk, dg in default_units:
        covered = []
        for i in tree.query(dg):
            inter = shapely.intersection(dg, units[i][1])
            if inter.is_empty or inter.area == 0:
                continue
            covered.append(inter)
            if keys[i] != dk:
                out.append((dk, keys[i], inter))
        rest = shapely.difference(dg, shapely.union_all(covered)) if covered else dg
        if rest.area > 0:
            out.append((dk, None, rest))
    dunion = shapely.union_all([g for _, g in default_units])
    for (ek, eg), k in zip(units, keys):
        extra = shapely.difference(eg, dunion)
        if extra.area > 0:
            out.append((None, k, extra))
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
