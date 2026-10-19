"""Build the study page (index.html): session 1 from session1.json, session1_registered.json, pieces.json, land.json, verify.json;
session 2 from session2.json, explore2.json, nameless.json, verify2.json, codes.json; session 3 from session3.json."""
import json
import shapely
from shapely.geometry import Point
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

P2 = {"P8": "The nameless land (all three ways, all 34 editions) is at least 800,000 km²",
      "P9": "At least 6 editions other than ISO leave at least 1 km² of the default's land in no unit",
      "P10": "More than half of the Palestinian edition's unnamed area lies on land the default draws as Israel",
      "P11": "No unnamed unit is larger than 100,000 km²",
      "P12": "The Russian edition's unnamed units lie on land the default gives to at least 3 units",
      "P13": "The default types at least 3 of its units “Indeterminate”",
      "P14": "More than half of the land the ISO edition leaves in no unit is one piece"}


def session2(data, rep):
    s2 = json.load(open("session2.json"))
    ex = json.load(open("explore2.json"))
    nl = json.load(open("nameless.json"))
    v2 = json.load(open("verify2.json"))
    codes = json.load(open("codes.json"))
    raw = {(u["edition"], u["index"]): u["nonblank"] for u in v2["unnamed_raw"]}
    unn = []
    for u in s2["unnamed_units"]:
        c = [v for k, v in raw[(u["edition"], u["index"])].items() if k.startswith("ADM0_A3")]
        unn.append((Point(*u["point"]), c))
    out = []
    for f in nl:
        g = shape(f["geom"])
        cs = sorted({c for pt, cc in unn for c in cc if g.buffer(0.01).contains(pt)})
        row = {"a": round(f["area_km2"]), "g": rnd(f["geom"], 3), "k": f["editions_naming_no_one"], "s": f["states"]}
        if cs:
            row["c"] = cs
            row["cn"] = sorted({n for c in cs for n in codes[c]})
        out.append(row)
    data["nl"] = out
    rows = []
    for k, held in s2["predictions"].items():
        pid = k.split()[0]
        rows.append(f"<tr><td>{pid}</td><td>{P2[pid]}</td><td>{'held' if held else 'failed'}</td></tr>")
    E = s2["editions"]
    geo = [x for x in v2["unexplained_left"] if x["edition"] == "gbr"][0]["area_km2"]
    ata = [u for u in s2["indeterminate_units"] if u["code"] == "ATA"][0]["area_km2"]
    rep.update({"{{ATA}}": f"{ata:,.0f}", "{{NL}}": f"{ex['nameless_without_antarctica_km2']:,.0f}", "{{NLP}}": str(len(ex["pieces"])),
                "{{UN_PSE}}": str(E["pse"]["unnamed_units"]), "{{UN_RUS}}": str(E["rus"]["unnamed_units"]),
                "{{UN_KM}}": f"{E['pse']['unnamed_km2'] + E['rus']['unnamed_km2']:,.0f}", "{{GEO}}": f"{geo:,.0f}",
                "{{PRED2_ROWS}}": "\n".join(rows), "{{HELD2}}": str(sum(s2["predictions"].values()))})


P3 = {"P15": "In at least 20 of the 31 national editions the country's own drawing is larger than its median across the other 33",
      "P16": "In none of the 31 is the own drawing smaller than its median",
      "P17": "Leaving Taiwan aside, the largest excess is more than 100,000 km²",
      "P18": "Leaving Taiwan aside, the largest excess is India's or Morocco's",
      "P19": "More than half of the rarely named places are named so by the named country's own edition",
      "P20": "In at least 5 of the 31 the own drawing's area is within 1 km² of the default's"}


def session3(rep):
    s3 = json.load(open("session3.json"))
    c, n = s3["countries"], s3["counts"]
    rows = [f"<tr><td>{k}</td><td>{P3[k]}</td><td>{'held' if v else 'failed'}</td></tr>" for k, v in s3["predictions"].items()]
    psi = [r for r in s3["rare_names"] if not r["self"] and r["name"] == "Palestine"][0]["area_km2"]
    rep.update({"{{LARGER}}": str(n["larger"]), "{{EQUAL}}": str(31 - n["larger"] - n["smaller"]), "{{MAR}}": f"{c['mar']['excess_km2']:,.0f}",
                "{{CHN}}": f"{c['chn']['own_km2']:,.0f}", "{{RARE}}": str(n["rare"]), "{{SELF}}": str(n["self_named"]),
                "{{PSI}}": f"{psi:,.0f}", "{{PRED3_ROWS}}": "\n".join(rows), "{{HELD3}}": str(sum(s3["predictions"].values()))})


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
    session2(data, rep)
    session3(rep)
    rep["{{DATA}}"] = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    for k, v in rep.items():
        t = t.replace(k, v)
    open("index.html", "w").write(t)
    print(len(t))


if __name__ == "__main__":
    main()
