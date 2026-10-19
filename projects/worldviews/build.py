"""Build the session-1 study page (index.html) from session1.json, session1_registered.json, pieces.json, land.json, verify.json."""
import json
import shapely
from shapely.geometry import shape, mapping

ED = {"default": "the default (de facto)", "arg": "Argentina", "bdg": "Bangladesh", "bra": "Brazil", "chn": "China", "deu": "Germany",
      "egy": "Egypt", "esp": "Spain", "fra": "France", "gbr": "the United Kingdom", "grc": "Greece", "idn": "Indonesia", "ind": "India",
      "iso": "ISO", "isr": "Israel", "ita": "Italy", "jpn": "Japan", "kor": "South Korea", "mar": "Morocco", "nep": "Nepal",
      "nld": "the Netherlands", "pak": "Pakistan", "pol": "Poland", "prt": "Portugal", "pse": "Palestine", "rus": "Russia",
      "sau": "Saudi Arabia", "swe": "Sweden", "tlc": "top-level countries", "tur": "Turkey", "twn": "Taiwan", "ukr": "Ukraine",
      "usa": "the United States", "vnm": "Vietnam"}


def rnd(geom, nd):
    g = shapely.set_precision(shape(geom), 10 ** -nd)
    m = mapping(g)
    polys = m["coordinates"] if m["type"] == "MultiPolygon" else ([m["coordinates"]] if m["type"] == "Polygon" else [])
    return [[[[round(x, nd), round(y, nd)] for x, y in ring] for ring in poly] for poly in polys]


def main():
    s = json.load(open("session1.json"))
    reg = json.load(open("session1_registered.json"))
    pieces = json.load(open("pieces.json"))
    cont = json.load(open("contested.json"))
    land = json.load(open("land.json"))
    ver = json.load(open("verify.json"))
    pdata = []
    for f, p in zip(cont, pieces):
        pdata.append({"a": f["area_km2"], "g": rnd(f["geom"], 3), "o": p["owners"], "n": p["distinct"]})
    ldata = [rnd(l["geom"], 2) for l in land]
    eds = sorted(((k, v["moved_km2"], v["left_km2"]) for k, v in s["editions"].items()), key=lambda x: -x[1])
    preds_reg = {p["id"]: p for p in reg["predictions"]}
    rows = []
    for p in s["predictions"]:
        r = preds_reg[p["id"]]
        fmt = lambda v: (f"{v:,.0f}" if isinstance(v, float) else (", ".join(f"{x:,.0f}" for x in v) if isinstance(v, list) else str(v)))
        rows.append(f"<tr><td>{p['id']}</td><td>{p['text']}</td><td>{fmt(r['value'])} — {'held' if r['held'] else 'failed'}</td>"
                    f"<td>{fmt(p['value'])} — {'held' if p['held'] else 'failed'}</td></tr>")
    own = s["owners_area_km2_estimate"]
    three = sum(v for k, v in own.items() if int(k) >= 3)
    data = {"pieces": pdata, "land": ldata, "eds": ED, "edlist": [[k, round(m), round(l)] for k, m, l in eds]}
    t = open("template.html").read()
    held = sum(p["held"] for p in s["predictions"])
    rep = {"{{DATA}}": json.dumps(data, separators=(",", ":"), ensure_ascii=False),
           "{{CONT}}": f"{s['contested_km2']:,.0f}", "{{PIECES}}": str(s["contested_pieces"]),
           "{{THREE}}": f"{three:,.0f}", "{{PRED_ROWS}}": "\n".join(rows), "{{HELD}}": str(held),
           "{{TWN_UNIT}}": "9,483,217", "{{TWN_FLOW}}": f"{s['editions']['twn']['flows_km2']['China -> Taiwan']:,.0f}",
           "{{REST}}": f"{(s['contested_km2'] - s['editions']['twn']['flows_km2']['China -> Taiwan']) / 1e6:.1f} million",
           "{{N_VER}}": str(len(ver)), "{{N_VER_IN}}": str(sum(1 for v in ver if v["disputed_feature"])),
           "{{LAND}}": f"{s['default_land_km2'] / 1e6:,.1f}", "{{SHARE}}": f"{100 * s['contested_km2'] / s['default_land_km2']:.2f}",
           "{{TOP}}": ED[eds[0][0]], "{{TOP_KM}}": f"{eds[0][1]:,.0f}", "{{LOW}}": ED[eds[-1][0]], "{{LOW_KM}}": f"{eds[-1][1]:,.0f}"}
    for k, v in rep.items():
        t = t.replace(k, v)
    open("index.html", "w").write(t)
    print(len(t))


if __name__ == "__main__":
    main()
