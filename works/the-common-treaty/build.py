"""The Common Treaty: built from committed files only (projects/held-back/common3.json, session3.json).

python3 build.py  ->  index.html"""

import html
import json
import pathlib

HERE = pathlib.Path(__file__).parent
P = HERE.parent.parent / "projects" / "held-back"
NAMES = {
 "CERD": "Elimination of Racial Discrimination (1965)", "ICCPR": "Civil and Political Rights (1966)",
 "ICESCR": "Economic, Social and Cultural Rights (1966)", "CEDAW": "Discrimination against Women (1979)",
 "CAT": "Against Torture (1984)", "CRC": "Rights of the Child (1989)", "CRMW": "Migrant Workers (1990)",
 "CED": "Enforced Disappearance (2006)", "CRPD": "Rights of Persons with Disabilities (2006)",
}
ORDER = ["CERD", "ICCPR", "ICESCR", "CEDAW", "CAT", "CRC", "CRMW", "CED", "CRPD"]


def label(article, para):
    if para == 0:
        return str(article)
    if para > 900:
        return f"{article}({chr(96 + para - 900)})"
    return f"{article}.{para}"


def main():
    c = json.load(open(P / "common3.json"))
    s = json.load(open(P / "session3.json"))
    rows, nojs = [], []
    for t in ORDER:
        ct, st = c["treaties"][t], s["treaties"][t]
        provs = ct["provisions"]
        key = {f'{p["article"]}({p["para"]})': p["id"] for p in provs}
        idx = {p["id"]: i for i, p in enumerate(provs)}
        years = {}
        for y, v in ct["years"].items():
            if int(y) >= ct["year_20"]:
                years[y] = {"n": v["parties"], "on": sorted(idx[i] for i in v["common"]),
                            "h": {str(idx[int(k)]): n for k, n in v["holders"].items()}}
        on26 = sorted(idx[key[k]] for k in st["common_2026_articled"])
        broken = {str(idx[key[k]]): [b["state"] for b in v] for k, v in st["broken"].items()}
        sig = st["general_upon_signature_only"]
        gen = [g for g in st["general_parties"] if g not in sig]
        rows.append({"t": t, "name": NAMES[t], "p": [label(p["article"], p["para"]) for p in provs], "y20": ct["year_20"],
                     "years": years, "on26": on26, "broken": broken, "gen": gen, "gensig": sig})
        on14 = set(years["2014"]["on"])
        cells = ", ".join(label(provs[i]["article"], provs[i]["para"]) for i in sorted(on14)) or "none"
        gone = ", ".join(f'{label(provs[int(i)]["article"], provs[int(i)]["para"])} ({html.escape(", ".join(v))})'
                         for i, v in broken.items())
        nojs.append(f'<tr><th scope="row">{t}<br><small>{NAMES[t]}</small></th><td>{ct["year_20"]}</td>'
                    f'<td>{len(years[str(ct["year_20"])]["on"])} of {len(provs)}</td><td>{len(on14)}: {cells}</td>'
                    f'<td>{len(on26)}{"; no longer: " + gone if gone else ""}</td><td>{len(gen)}</td></tr>')
    tot = s["totals"]
    page = (HERE / "template.html").read_text()
    page = page.replace("/*DATA*/null", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/"))
    read = sum(v["read"] for v in s["treaties"].values())
    for k, v in {"{{C14}}": tot["common_2014"], "{{C26}}": tot["still_common_2026_articled"],
                 "{{C26B}}": tot["still_common_without_range_signature_chapeau"], "{{RET}}": tot["returned"],
                 "{{READ}}": read, "{{NPROV}}": sum(len(c["treaties"][t]["provisions"]) for t in ORDER),
                 "{{NOJS}}": "".join(nojs)}.items():
        page = page.replace(k, str(v))
    (HERE / "index.html").write_text(page)


if __name__ == "__main__":
    main()
