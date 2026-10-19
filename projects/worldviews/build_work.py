"""Build the work, Each by Its Own Map (each-by-its-own-map/index.html), from selfmaps.json, session3.json and explore3.json.
Keeps each country drawn by its own edition over the others' drawing and the land only its own map gives it; drops the predictions."""
import json, os
from build import ED

NAME = {"arg": "Argentina", "bdg": "Bangladesh", "bra": "Brazil", "chn": "China", "deu": "Germany", "egy": "Egypt", "esp": "Spain",
        "fra": "France", "gbr": "the United Kingdom", "grc": "Greece", "idn": "Indonesia", "ind": "India", "isr": "Israel", "ita": "Italy",
        "jpn": "Japan", "kor": "South Korea", "mar": "Morocco", "nep": "Nepal", "nld": "the Netherlands", "pak": "Pakistan",
        "pol": "Poland", "prt": "Portugal", "pse": "Palestine", "rus": "Russia", "sau": "Saudi Arabia", "swe": "Sweden",
        "tur": "Turkey", "twn": "Taiwan", "ukr": "Ukraine", "usa": "the United States", "vnm": "Vietnam"}


def rnd(gj, nd=2):
    if not gj:
        return []
    polys = gj["coordinates"] if gj["type"] == "MultiPolygon" else ([gj["coordinates"]] if gj["type"] == "Polygon" else [])
    return [[[[round(x, nd), round(y, nd)] for x, y in ring] for ring in poly] for poly in polys]


def main():
    maps = json.load(open("selfmaps.json"))
    s3 = json.load(open("session3.json"))
    ex = json.load(open("explore3.json"))["largest_part_names"]
    c = s3["countries"]
    larger = sorted((x for x in c if c[x]["excess_km2"] > 1), key=lambda x: -c[x]["excess_km2"])
    equal = sorted((x for x in c if abs(c[x]["excess_km2"]) <= 1), key=lambda x: NAME[x].replace("the ", ""))
    panels = []
    for x in larger:
        m = maps[x]
        t = ex.get(x, {}).get("tally", [])
        others = [[n, k] for n, k in t if n != NAME[x] and k >= 2]
        panels.append({"x": x, "name": NAME[x], "own": m["own_km2"], "med": m["median_km2"], "only": m["only_km2"],
                       "o": rnd(m["own"]), "m": rnd(m["others"]), "y": rnd(m["only"], 3), "there": others[:2]})
    data = {"panels": panels}
    eq = ", ".join(NAME[x] for x in equal)
    html = open("work_template.html").read()
    rep = {"{{DATA}}": json.dumps(data, separators=(",", ":"), ensure_ascii=False), "{{N_LARGER}}": str(len(larger)),
           "{{N_EQUAL}}": str(len(equal)), "{{EQUAL_LIST}}": eq, "{{CHN}}": f"{c['chn']['own_km2']:,.0f}",
           "{{TWN_MED}}": f"{c['twn']['median_km2']:,.0f}", "{{CHN_MED}}": f"{c['chn']['median_km2']:,.0f}",
           "{{TWN_ZERO}}": str(sum(1 for v in c["twn"]["areas_km2"].values() if v == 0))}
    for k, v in rep.items():
        html = html.replace(k, v)
    os.makedirs("each-by-its-own-map", exist_ok=True)
    open("each-by-its-own-map/index.html", "w").write(html)
    print(len(html), len(larger), len(equal))


if __name__ == "__main__":
    main()
