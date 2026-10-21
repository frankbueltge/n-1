"""Which You: built from committed files only (projects/indirect/sheet3.json, read3.json, key3.json, result3.json).

python3 build.py  ->  index.html"""

import html
import json
import pathlib

HERE = pathlib.Path(__file__).parent
P = HERE.parent.parent / "projects" / "indirect"
NAMES = {
 "asm": "Assamese", "ber": "Berber", "ces": "Czech", "cmn": "Mandarin", "deu": "German", "ell": "Greek", "fin": "Finnish",
 "fra": "French", "gos": "Gronings", "hau": "Hausa", "heb": "Hebrew", "hun": "Hungarian", "hye": "Armenian", "ido": "Ido",
 "ina": "Interlingua", "ita": "Italian", "jpn": "Japanese", "kab": "Kabyle", "knc": "Kanuri", "lat": "Latin",
 "lfn": "Lingua Franca Nova", "lvs": "Latvian", "mkd": "Macedonian", "nld": "Dutch", "pol": "Polish", "por": "Portuguese",
 "rhg": "Rohingya", "run": "Kirundi", "rus": "Russian", "spa": "Spanish", "swh": "Swahili", "tgl": "Tagalog", "tir": "Tigrinya",
 "tlh": "Klingon", "tok": "Toki Pona", "tur": "Turkish", "ukr": "Ukrainian", "vol": "Volapük", "yid": "Yiddish",
}


def main():
    sheet = {r["n"]: r for r in json.load(open(P / "sheet3.json"))}
    read = {r["n"]: r for r in json.load(open(P / "read3.json"))["readings"]}
    key = json.load(open(P / "key3.json"))
    res = json.load(open(P / "result3.json"))["predictions"]
    n_of = {r["id"]: r["n"] for r in key["rows"]}
    groups = []
    for g in key["groups"]:
        tr = []
        for x in g["translations"]:
            s, r = sheet[n_of[x]], read[n_of[x]]
            tr.append({"id": x, "lang": NAMES[s["lang"]], "text": s["text"], "r": r["reading"], "low": r["confidence"] == "low",
                       "note": r["note"]})
        groups.append({"eng": g["eng"], "en": g["eng_text"], "t": tr, "links": g["links"]})
    a, d = res["P13"]["agree"], res["P13"]["disagree"]
    langs = len({t["lang"] for g in groups for t in g["t"]})
    nojs = []
    for i, g in enumerate(groups):
        items = "".join(f'<li><b>{html.escape(t["lang"])}</b> ({ {"T": "one, close", "V": "polite or several", "both": "both", "unmarked": "does not say", "cannot": "not read"}[t["r"]] }): '
                        f'<a href="https://tatoeba.org/en/sentences/show/{t["id"]}">{html.escape(t["text"])}</a></li>' for t in g["t"])
        nojs.append(f'<li><a href="https://tatoeba.org/en/sentences/show/{g["eng"]}">{html.escape(g["en"])}</a><ul>{items}</ul></li>')
    page = (HERE / "template.html").read_text()
    page = page.replace("/*DATA*/null", json.dumps(groups, ensure_ascii=False).replace("</", "<\\/"))
    for k, v in {"{{SPLIT}}": res["P14"]["observed"], "{{AGREE}}": a["pairs"], "{{AGREE_L}}": a["linked"], "{{DIS}}": d["pairs"],
                 "{{DIS_L}}": d["linked"], "{{LANGS}}": langs, "{{N}}": sum(len(g["t"]) for g in groups),
                 "{{LOW}}": sum(t["low"] for g in groups for t in g["t"]), "{{NOJS}}": "".join(nojs)}.items():
        page = page.replace(k, str(v))
    (HERE / "index.html").write_text(page)


if __name__ == "__main__":
    main()
