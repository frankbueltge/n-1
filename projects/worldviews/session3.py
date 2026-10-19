"""Project 12 session 3: the registered run (SESSION3.md). Each country with its own edition, as its own edition draws it and as
the other 33 do. Reads the 34 editions from the scratch directory given as argv[1]; writes session3.json and selfmaps.json."""
import json, sys, time
import numpy as np
import shapely
import lib
from session1 import POVS, NATIONAL, read

CODES = {"arg": "ARG", "bdg": "BGD", "bra": "BRA", "chn": "CHN", "deu": "DEU", "egy": "EGY", "esp": "ESP", "fra": "FRA",
         "gbr": "GBR", "grc": "GRC", "idn": "IDN", "ind": "IND", "isr": "ISR", "ita": "ITA", "jpn": "JPN", "kor": "KOR",
         "mar": "MAR", "nep": "NPL", "nld": "NLD", "pak": "PAK", "pol": "POL", "prt": "PRT", "pse": "PSX", "rus": "RUS",
         "sau": "SAU", "swe": "SWE", "tur": "TUR", "twn": "TWN", "ukr": "UKR", "usa": "USA", "vnm": "VNM"}
STEP = 2.0  # km; one lattice point stands for STEP**2 km2
HALF = 16   # 'only its own map': at most 16 of the 33 others; 'withholds': at least 17


def drawing(units, code):
    gs = [g for a, g in units if (a["ADM0_A3"] or "").strip() == code]
    return shapely.union_all(gs) if gs else shapely.Polygon()


def lattice(geom, step=STEP):
    """Points of a step-km lattice inside geom, laid per polygon part (so far-apart parts cost nothing between them)."""
    xs, ys = [], []
    for part in getattr(geom, "geoms", [geom]):
        if part.is_empty or part.geom_type != "Polygon":
            continue
        x0, y0, x1, y1 = part.bounds
        gx = np.arange(np.floor(x0 / step) * step + step / 2, x1, step)
        gy = np.arange(np.floor(y0 / step) * step + step / 2, y1, step)
        if not len(gx) or not len(gy):
            continue
        X, Y = np.meshgrid(gx, gy)
        X, Y = X.ravel(), Y.ravel()
        shapely.prepare(part)
        m = shapely.contains_xy(part, X, Y)
        xs.append(X[m]); ys.append(Y[m])
    if not xs:
        return np.empty(0), np.empty(0)
    return np.concatenate(xs), np.concatenate(ys)


def compare(own, others, step=STEP, half=HALF):
    """own: geometry; others: list of geometries. Returns areas and the two lattice sets (registered definitions)."""
    allg = [own] + list(others)
    union = shapely.union_all(allg)
    inter = allg[0]
    for g in allg[1:]:
        inter = shapely.intersection(inter, g)
    d = lib.polys(shapely.difference(union, inter))
    X, Y = lattice(d, step)
    o = shapely.contains_xy(own, X, Y) if len(X) else np.zeros(0, bool)
    k = np.zeros(len(X), int)
    for g in others:
        if not g.is_empty and len(X):
            shapely.prepare(g)
            k += shapely.contains_xy(g, X, Y)
    only = o & (k <= half)
    withheld = (~o) & (k >= half + 1)
    areas = [g.area for g in others]
    med = float(np.median(areas))
    return {"own_km2": own.area, "median_km2": med, "excess_km2": own.area - med,
            "only_own_km2": float(only.sum() * step * step), "withheld_km2": float(withheld.sum() * step * step),
            "disagree_km2": d.area}, (X[only], Y[only]), (X[withheld], Y[withheld])


def main(d):
    t0 = time.time()
    eds = {"default": read(d, "ne_10m_admin_0_countries")}
    for p in POVS:
        eds[p] = read(d, "ne_10m_admin_0_countries_" + p)
    names = list(eds)
    out = {"countries": {}}
    maps = {}
    for x in NATIONAL:
        code = CODES[x]
        G = {e: drawing(eds[e], code) for e in names}
        others = [e for e in names if e != x]
        r, only, wh = compare(G[x], [G[e] for e in others])
        r["code"] = code
        r["areas_km2"] = {e: G[e].area for e in names}
        r["default_km2"] = G["default"].area
        out["countries"][x] = r
        maps[x] = {"only": [only[0].tolist(), only[1].tolist()], "withheld": [wh[0].tolist(), wh[1].tolist()]}
        print(x, round(r["excess_km2"]), round(r["only_own_km2"]), round(r["withheld_km2"]), round(time.time() - t0), flush=True)
    c = out["countries"]
    ex = {x: c[x]["excess_km2"] for x in c}
    no_twn = {x: v for x, v in ex.items() if x != "twn"}
    top = max(no_twn, key=no_twn.get)
    # self-naming in session 1's pieces
    pieces = json.load(open("pieces.json"))
    admin = {}
    for a, g in eds["default"]:
        admin.setdefault((a["ADM0_A3"] or "").strip(), a["ADMIN"])
    pov_of = {admin[CODES[x]]: x for x in NATIONAL}
    rare, selfn = [], 0
    for i, pc in enumerate(pieces):
        if pc["distinct"] == 1:
            continue
        cnt = {}
        for e, n in pc["owners"].items():
            cnt.setdefault(n, []).append(e)
        for n, es in cnt.items():
            if n in pov_of and 1 <= len(es) <= 5:
                s = pov_of[n] in es
                selfn += s
                rare.append({"piece": i, "name": n, "editions": es, "self": s, "area_km2": pc["area_km2"]})
    out["rare_names"] = rare
    out["predictions"] = {
        "P15": sum(1 for v in ex.values() if v > 1) >= 20,
        "P16": all(v >= -1 for v in ex.values()),
        "P17": no_twn[top] > 100000,
        "P18": top in ("ind", "mar"),
        "P19": selfn > len(rare) / 2,
        "P20": sum(1 for x in c if abs(c[x]["own_km2"] - c[x]["default_km2"]) <= 1) >= 5,
    }
    out["counts"] = {"larger": sum(1 for v in ex.values() if v > 1), "smaller": sum(1 for v in ex.values() if v < -1),
                     "top_excl_twn": top, "top_excess_km2": no_twn[top], "rare": len(rare), "self_named": selfn,
                     "within_1km2_of_default": sum(1 for x in c if abs(c[x]["own_km2"] - c[x]["default_km2"]) <= 1)}
    json.dump(out, open("session3.json", "w"), indent=1)
    json.dump(maps, open("selfmaps_raw.json", "w"))
    print(json.dumps(out["predictions"]), json.dumps(out["counts"]))


if __name__ == "__main__":
    main(sys.argv[1])
