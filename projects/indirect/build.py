"""Build index.html from session 1 (session1.json, result1.json, bridges.json, sheet.json, key.json) and session 2 (session2.json, result2.json, explore2.json, examples2.json)."""
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
s2 = json.load(open("session2.json")); r2 = json.load(open("result2.json")); x2 = json.load(open("explore2.json")); ex2 = json.load(open("examples2.json"))
res["predictions"] = res["predictions"] + [{**p, "value": (f'{p["value"]*100:.1f} %' if p["id"] in ("P7", "P8", "P10", "P11") else f'{p["value"]:.2f}×' if p["id"] == "P9" else f'{p["value"]:,}')} for p in r2["predictions"]]
pc = lambda v: f"{v*100:.1f} %"
cb = s2["chains_by_bridge_class"]; ol = s2["other_by_bridge_language_top12"]
LN = {"deu": "German", "ukr": "Ukrainian", "ita": "Italian", "hun": "Hungarian", "spa": "Spanish", "nld": "Dutch", "cmn": "Chinese",
      "por": "Portuguese", "jpn": "Japanese"}
s2rows = [("linked directly", s2["direct"], "var(--a)")] + [(f"via {LN[k]}", ol[k], "var(--a)") for k in sorted(LN, key=lambda k: ol[k]["disagree_share"])] + [
    ('via English "you"', cb["eng-you"], "var(--c2)"), ('via Esperanto "vi"', cb["epo-vi"], "var(--c2)")]
def s2chart():
    W, h, y0, X0 = 250, 36, 32, 195
    parts = []
    for i, (lab, d, col) in enumerate(s2rows):
        y = y0 + i * h
        x = d["disagree_share"] * W
        bx = d["independence_baseline"] * W
        parts.append(f'<text x="0" y="{y+16}" fill="currentColor">{E(lab)}</text>'
                     f'<rect x="{X0}" y="{y+2}" width="{max(x,1):.1f}" height="18" fill="{col}"/>'
                     f'<line x1="{X0+bx:.1f}" x2="{X0+bx:.1f}" y1="{y-2}" y2="{y+24}" stroke="currentColor" stroke-width="2"/>'
                     f'<text x="{X0+max(x,bx)+8:.1f}" y="{y+16}" fill="currentColor">{pc(d["disagree_share"])}</text>'
                     f'<text x="600" y="{y+16}" text-anchor="end" fill="var(--mut)">{d["both_classified"]:,}</text>')
    H = y0 + len(s2rows) * h + 8
    return (f'<svg class="ch2" viewBox="0 0 600 {H}" role="img" aria-label="Disagreement on who is addressed, by what stands between a French and a Russian translation">'
            f'<text x="600" y="18" text-anchor="end" fill="var(--mut)">pairs</text>'
            f'<line x1="{X0}" x2="{X0}" y1="2" y2="22" stroke="currentColor" stroke-width="2"/><text x="{X0+8}" y="18" fill="var(--mut)">chance</text>' + "".join(parts) + "</svg>")
def corner(lbl, s, lk):
    return f'<li><span class="k">{lbl}</span> {link(s["id"], lbl[:3], s["text"]).split(" <span")[0]}</li>'
exs = []
for e in ex2["examples"]:
    L = e["linked"]; yn = lambda v: "linked" if v else "not linked"
    exs.append(f'<div class="xc"><div class="en">{link(e["eng"]["id"], "eng", e["eng"]["text"])}</div><ul>'
               + corner("fra tu", e["fra_T"], None) + corner("fra vous", e["fra_V"], None) + corner("rus ты", e["rus_T"], None) + corner("rus вы", e["rus_V"], None)
               + f'</ul><p class="k">tu–ты {yn(L["T-T"])} · vous–вы {yn(L["V-V"])} · tu–вы {yn(L["T-V"])} · vous–ты {yn(L["V-T"])}</p></div>')
la, lu = x2["paths_with_linked_ends"], x2["paths_with_unlinked_ends"]
agree_all = la["agree"] + lu["agree"]; dis_all = la["disagree"] + lu["disagree"]
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
             "NFIRST": str(br["counts"]["first"]), "NSECOND": str(br["counts"]["second"]),
             "S2CHAINS": f(s2["chains_all"]["n"]), "S2DIRECT": pc(s2["direct"]["disagree_share"]), "S2ENGYOU": pc(cb["eng-you"]["disagree_share"]),
             "S2DEU": pc(ol["deu"]["disagree_share"]), "S2CHART": s2chart(), "S2AGREEALL": pc(agree_all / (agree_all + dis_all)),
             "S2LINKEDAGREE": pc(la["agree"] / agree_all), "S2LINKEDDIS": f'{la["disagree"] / dis_all * 100:.2f} %', "S2BRIDGES": f(x2["bridges_with_classified_ends_on_both_sides"]),
             "S2BOTHBOTH": f(x2["bridges_by_french_side_and_russian_side"]["both|both"]), "S2EXAMPLES": "".join(exs),
             "S2CHECKN": str(r2["rule_check"]["T_or_V_by_rule"]), "S2CHECKA": str(r2["rule_check"]["agreeing_with_reading"])}.items():
    out = out.replace("{{" + k + "}}", v)
assert "{{" not in out
open("index.html", "w").write(out)
