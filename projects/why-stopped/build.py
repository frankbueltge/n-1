"""Project 16: the study page, index.html, from session1.json, result1.json, anach1.json, session2.json, result2.json and late2.json
(no reason text)."""
import html, json

s = json.load(open("session1.json"))
r = json.load(open("result1.json"))
a = json.load(open("anach1.json"))
s2 = json.load(open("session2.json"))
r2 = json.load(open("result2.json"))
l2 = json.load(open("late2.json"))

def mi(m):
    return int(m[:4]) * 12 + int(m[5:7]) - 1

# figure 1: one column per month, 2015-01 to 2026-10
mon = [x for x in s["monthly"] if "2015-01" <= x["m"] <= "2026-10"]
W, H, X0 = 1008, 260, 8
cw = (W - 2 * X0) / len(mon)
top = max(x["reasons"] for x in mon)
g = []
for i, x in enumerate(mon):
    hx = H * x["reasons"] / top
    hf = H * x["flagged"] / top
    g.append('<g><title>%s: %d stopped with a reason, %d naming the pandemic</title>'
             '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bg"/>'
             '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="hb"/></g>' % (
                 x["m"], x["reasons"], x["flagged"], X0 + i * cw, 10 + H - hx, cw - 1, hx, X0 + i * cw, 10 + H - hf, cw - 1, hf))
for y in range(2015, 2027):
    i = mi("%d-01" % y) - mi("2015-01")
    g.append('<text x="%.1f" y="%d" class="yr" style="text-anchor:start">%d</text>' % (X0 + i * cw + 2, H + 32, y))
    g.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="ax"/>' % (X0 + i * cw, X0 + i * cw, H + 10, H + 16))
fig = ('<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Stopped studies by month, 2015 to 2026, and those whose reason '
       'names the pandemic">%s</svg>' % (W, H + 40, "".join(g)))

# figure 2: the early ends, one line each from stop month to last update
it = [x for x in a["items"] if x["names"] != "not the pandemic (a company's name)"]
it.sort(key=lambda x: (x["names"] != "an influenza pandemic", x["stop"], x["last_update"]))
m0, m1 = mi("2007-01"), mi("2026-12")
sx = lambda m: X0 + (W - 2 * X0) * (mi(m) - m0) / (m1 - m0)
RH = 5
h2 = len(it) * RH + 20
g2 = ['<rect x="%.1f" y="0" width="%.1f" height="%d" class="ev"/>' % (sx("2020-01"), sx("2026-12") - sx("2020-01"), h2 - 14)]
for j, x in enumerate(it):
    y = 4 + j * RH
    c = "f" if x["names"] == "an influenza pandemic" else "n"
    g2.append('<g><title>%s: ends %s, entry last changed %s (names %s)</title><line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="l%s"/>'
              '<circle cx="%.1f" cy="%d" r="2.6" class="d%s"/></g>' % (
                  x["nct"], x["stop"], x["last_update"], x["names"], sx(x["stop"]), sx(x["last_update"]), y, y, c, sx(x["stop"]), y, c))
for y in range(2008, 2027, 2):
    g2.append('<text x="%.1f" y="%d" class="yr" style="text-anchor:start">%d</text>' % (sx("%d-01" % y) + 2, h2 + 6, y))
    g2.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="ax"/>' % (sx("%d-01" % y), sx("%d-01" % y), h2 - 14, h2 - 8))
fig2 = ('<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Studies whose recorded end precedes the pandemic their reason '
        'names, each as a line from end to last change">%s</svg>' % (W, h2 + 12, "".join(g2)))

# figure 3: the late lines, three clocks each: the register's end (dot), the month the line names (square), the last change (tick)
it3 = sorted(l2["items"], key=lambda x: (x["stop"], x["read_month"]))
m0, m1 = mi("2007-01"), mi("2026-12")
RH3 = 22
h3 = len(it3) * RH3 + 24
KC = {"decision": "kd", "halt": "kh", "cause": "kc", "writing": "kw", "world": "kx"}
g3 = ['<rect x="%.1f" y="0" width="%.1f" height="%d" class="ev"/>' % (sx("2020-01"), sx("2026-12") - sx("2020-01"), h3 - 18)]
for j, x in enumerate(it3):
    y = 12 + j * RH3
    c = KC[x["names_the_month_of"]]
    g3.append('<g><title>%s: the register ends it %s; its line names %s (%s); entry last changed %s</title>'
              '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="lr"/>'
              '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="lx %s"/>'
              '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="tk"/>'
              '<circle cx="%.1f" cy="%d" r="4.5" class="de"/>'
              '<rect x="%.1f" y="%d" width="9" height="9" class="%s"/></g>' % (
                  x["nct"], x["stop"], x["read_month"], l2["kinds"][x["names_the_month_of"]], x["lastupd"],
                  sx(x["read_month"]), sx(x["lastupd"]), y, y,
                  sx(x["stop"]), sx(x["read_month"]), y, y, c,
                  sx(x["lastupd"]), sx(x["lastupd"]), y - 6, y + 6,
                  sx(x["stop"]), y, sx(x["read_month"]) - 4.5, y - 4, c))
for y in range(2008, 2027, 2):
    g3.append('<text x="%.1f" y="%d" class="yr" style="text-anchor:start">%d</text>' % (sx("%d-01" % y) + 2, h3 + 4, y))
    g3.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="ax"/>' % (sx("%d-01" % y), sx("%d-01" % y), h3 - 18, h3 - 12))
fig3 = ('<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Twenty studies whose reason names a month after the end the '
        'register gives: the end, the month named, and the entry\'s last change">%s</svg>' % (W, h3 + 10, "".join(g3)))
P2 = {"P%d" % x["n"]: x for x in s2["predictions"]}
P2["P6"] = r2["P6"]
pl2 = ["<li>%s %s: %s (%s).</li>" % ("Held," if v["held"] else "<b>Failed</b>,", k, html.escape(v["registered"]),
       html.escape(str(v["value"][1] if isinstance(v["value"], list) else v["value"]) + ("" if k in ("P5", "P6") else " %")))
       for k, v in sorted(P2.items())]
kb = l2["by_kind"]

gaps = sorted(mi(x["last_update"]) - mi(x["stop"]) for x in it if x["names"] == "COVID-19")
P = s["predictions"]
P["P6"] = r["P6"]
pl = []
for k in sorted(P):
    v = P[k]
    pl.append("<li>%s %s: %s.</li>" % ("Held," if v["held"] else "<b>Failed</b>,", k, html.escape(v["registered"])))
k = a["by_kind"]
rep = {
    "{{STOPPED}}": "{:,}".format(s["stopped"]), "{{WHY}}": "{:,}".format(s["with_reason"]), "{{FLAG}}": "{:,}".format(s["flagged_all"]),
    "{{H1}}": "%.0f %%" % (100 * s["half_years"]["2020H1"]["share"]), "{{Y25}}": str(s["years"]["2025"]["flagged"]),
    "{{FIG}}": fig, "{{FIG2}}": fig2, "{{ANACH}}": str(s["anachronisms"]["count"]), "{{ANCOV}}": str(k["COVID-19"]),
    "{{ANFLU}}": str(k["an influenza pandemic"]), "{{GAP}}": str(gaps[len(gaps) // 2]),
    "{{AGREE}}": str(r["agree_words"]), "{{AGREE2}}": str(r["agree_event"]),
    "{{PRED}}": "".join(pl), "{{NHELD}}": str(sum(v["held"] for v in P.values())),
    "{{FIG3}}": fig3, "{{POP}}": "{:,}".format(s2["population"]), "{{DATED}}": str(s2["self_dated"]), "{{LATE}}": str(s2["late_lines"]),
    "{{FWD}}": str(s2["forward_lines"]), "{{KD}}": str(kb["decision"]), "{{KH}}": str(kb["halt"]), "{{KC}}": str(kb["cause"]),
    "{{KW}}": str(kb["writing"]), "{{AD}}": str(s2["anachronisms_self_dated"]), "{{M03}}": str(dict(s2["line_month_top"])["2020-03"]),
    "{{AG2}}": str(r2["agree_dated"]), "{{AGM}}": str(r2["agree_month"]), "{{BOTH}}": str(r2["both_dated"]),
    "{{PRED2}}": "".join(pl2), "{{NHELD2}}": str(sum(v["held"] for v in P2.values())),
    "{{GAPMAX}}": str(s2["late_gap_months"]["max"]),
}
page = open("template.html").read()
for a_, b in rep.items():
    page = page.replace(a_, b)
assert "{{" not in page
open("index.html", "w").write(page)
print("ok", len(mon), len(it))
