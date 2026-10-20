"""Build index.html from session1.json, result1.json, bridges.json, sheet.json and key.json."""
import html, json

s1 = json.load(open("session1.json")); res = json.load(open("result1.json")); br = json.load(open("bridges.json"))
sheet = {x["n"]: x for x in json.load(open("sheet.json"))}; key = {x["n"]: x for x in json.load(open("key.json"))}
E = html.escape
def link(sid, lang, text):
    return f'<a href="https://tatoeba.org/en/sentences/show/{sid}" lang="{E(lang)}">{E(text)}</a> <span class="lg">{E(lang)}</span>'
def mark(text, hinge):
    t = E(text)
    if hinge and E(hinge) in t:
        t = t.replace(E(hinge), f"<mark>{E(hinge)}</mark>", 1)
    elif hinge and E(hinge.capitalize()) in t:
        t = t.replace(E(hinge.capitalize()), f"<mark>{E(hinge.capitalize())}</mark>", 1)
    return t
rows = []
for r in br["rows"]:
    if r["locus"] != "chain":
        continue
    n = r["n"]; a, c, b = sheet[n]["a"], sheet[n]["c"], key[n]["bridge"]
    rows.append(f'<tr><td>{link(a["id"], a["lang"], a["text"])}</td>'
                f'<td><a href="https://tatoeba.org/en/sentences/show/{b["id"]}" lang="{E(b["lang"])}">{mark(b["text"], r["hinge"])}</a> <span class="lg">{E(b["lang"])}</span></td>'
                f'<td>{link(c["id"], c["lang"], c["text"])}</td><td class="sm">{E(r["how"])}</td></tr>')
other = []
for r in br["rows"]:
    if r["locus"] == "chain":
        continue
    n = r["n"]; a, c, b = sheet[n]["a"], sheet[n]["c"], key[n]["bridge"]
    other.append(f'<tr><td>{r["locus"]}</td><td>{link(a["id"], a["lang"], a["text"])}</td><td>{link(b["id"], b["lang"], b["text"])}</td>'
                 f'<td>{link(c["id"], c["lang"], c["text"])}</td><td class="sm">{E(r["how"])}</td></tr>')
preds = "".join(f'<tr><td>{p["id"]}</td><td>{E(p["text"])}</td><td>{p["value"]}</td><td>{"held" if p["held"] else "<b>failed</b>"}</td></tr>' for p in res["predictions"])
def bar(y, label, pct, lo, hi, color):
    w = 400
    return (f'<text x="0" y="{y-6}" fill="currentColor">{label}</text>'
            f'<rect x="0" y="{y}" width="{w*pct/30:.1f}" height="22" fill="{color}"/>'
            f'<line x1="{w*lo/30:.1f}" x2="{w*hi/30:.1f}" y1="{y+11}" y2="{y+11}" stroke="currentColor" stroke-width="1.5"/>'
            f'<text x="{w*hi/30+8:.1f}" y="{y+16}" fill="currentColor">{pct:.1f} %</text>')
chart = ('<svg class="ch" viewBox="-18 0 506 150" role="img" aria-label="Shifted or different: 4.0 % of direct pairs, 19.7 % of translations of translations">'
         + bar(24, "a translation", 4.0, 1.1, 13.5, "var(--a)") + bar(80, "a translation of a translation", 19.7, 14.1, 26.9, "var(--c2)")
         + "".join(f'<text x="{400*v/30:.1f}" y="140" text-anchor="middle">{v} %</text>' for v in (0, 10, 20, 30)) + "</svg>")
f = lambda v: f"{v:,}"
out = open("template.html").read()
for k, v in {"DIRECT": f(s1["direct_pairs"]), "INDIRECT": f(s1["indirect_pairs"]), "SENT": f(s1["sentences_known_language"]), "LANGS": f(s1["languages"]),
             "CHART": chart, "CHAINROWS": "".join(rows), "OTHERROWS": "".join(other), "PREDS": preds, "NCHAIN": str(br["counts"]["chain"]),
             "NFIRST": str(br["counts"]["first"]), "NSECOND": str(br["counts"]["second"])}.items():
    out = out.replace("{{" + k + "}}", v)
assert "{{" not in out
open("index.html", "w").write(out)
