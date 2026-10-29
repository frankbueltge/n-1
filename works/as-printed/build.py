"""As Printed: the work's page, from session3.json, panels3.json and session4.json in projects/on-the-grid/ (declared in session 4 by
the rule in SESSION4.md; the draft it was built from stands in projects/on-the-grid/work-draft/). Run from this directory: python3 build.py"""
import html, json

P = "../../projects/on-the-grid/"
s = json.load(open(P + "session3.json"))
panels = json.load(open(P + "panels3.json"))["panels"]
c = json.load(open(P + "session4.json"))["agg"]
fate = s["fate"]

def num(x):
    x = float(x)
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else ("%g" % x)

def line(label, d, unit, big=False):
    if not d:
        return '<div class="row"><span>%s</span><span class="n">&nbsp;</span></div>' % label
    v, r = d["v"], d["r"]
    if r is None:
        shown = '<span class="n gap" title="no number the law allows gives what the database keeps">&nbsp;</span>'
        under = '<span class="db">database: %s%s · %s</span>' % (num(v), unit, "no lawful number gives this" if d["n_pre"] == 0 else "more than one lawful number gives this")
    else:
        shown = '<span class="n">%s%s</span>' % (num(r), unit)
        under = '<span class="db">database: %s%s</span>' % (num(v), unit) if abs(float(v) - r) > 1e-9 else ""
    return '<div class="row%s"><span>%s</span>%s</div>%s' % (" cal" if big else "", label, shown, under)

cards = []
for p in panels:
    serving = "%s%s" % (num(p["servingSize"]), (p["unit"] or "").lower().replace("grm", "g").replace("mlt", "ml"))
    hh = (p.get("household") or "").strip()
    desc = html.escape((p.get("description") or "").strip())
    body = ('<a class="panel%s" href="https://fdc.nal.usda.gov/food-details/%d/nutrients" title="FoodData Central %d">'
            '<span class="what">%s</span><span class="title">Nutrition Facts</span>'
            '<span class="serv">Serving size %s%s</span><span class="thick"></span>%s<span class="thin"></span>%s%s</a>') % (
        " lost" if p["fate"] == "unrestorable" else "", p["fdcId"], p["fdcId"], desc, html.escape(serving),
        (" (%s)" % html.escape(hh)) if hh else "", line("Calories", p.get("calories"), "", True),
        line("Total Fat", p.get("fat"), "g"), line("Sodium", p.get("sodium"), "mg"))
    cards.append(body)
given = "".join(x for x, p in zip(cards, panels) if p["fate"] == "given_back")
lost = "".join(x for x, p in zip(cards, panels) if p["fate"] == "unrestorable")

def tot(src, k):
    return fate["calories|" + src].get(k, 0)
T = {k: tot("LI", k) + tot("other", k) for k in ("testable", "kept", "given_back", "ambiguous", "unrestorable")}
W = 1000.0
x = 0; bar = []
for k, cls, lab in (("kept", "bk", "kept as printed"), ("given_back", "bg", "given back"), ("ambiguous", "ba", "ambiguous"),
                    ("unrestorable", "bu", "cannot be given back")):
    w = W * T[k] / T["testable"]
    bar.append('<rect x="%.2f" y="0" width="%.2f" height="28" class="%s"><title>%s: %s</title></rect>' % (x, w, cls, lab, format(T[k], ",")))
    x += w
barsvg = ('<svg class="bar" viewBox="0 0 1000 28" preserveAspectRatio="none" role="img" aria-label="All %s calorie values: kept, '
          'given back, ambiguous, cannot be given back">%s</svg>' % (format(T["testable"], ","), "".join(bar)))

def pct(a, b):
    return "%.1f %%" % (100.0 * a / b) if b else "–"
rows = []
for src, name in (("LI", "Label Insight (the main source)"), ("other", "the other sources")):
    f = fate["calories|" + src]
    rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        name, format(f["testable"], ","), format(f.get("kept", 0), ","), format(f.get("given_back", 0), ","),
        format(f.get("ambiguous", 0), ","), format(f.get("unrestorable", 0), ",")))
rows.append("<tr><td>all</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(format(T[k], ",") for k in (
    "testable", "kept", "given_back", "ambiguous", "unrestorable")))
table = ("<table><thead><tr><th>Calorie values</th><th>All</th><th>Kept as printed</th><th>Given back</th><th>Ambiguous</th>"
         "<th>Cannot be given back</th></tr></thead><tbody>%s</tbody></table>" % "".join(rows))
nut = []
for k, name in (("calories", "Calories"), ("fat", "Total fat"), ("sodium", "Sodium")):
    f = fate[k + "|LI"]
    nut.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        name, format(f["testable"], ","), pct(f["restored"], f["testable"]), pct(f.get("given_back", 0), f["restored"]),
        pct(f.get("unrestorable", 0) + f.get("ambiguous", 0), f["testable"])))
nutt = ("<table><thead><tr><th>Main source</th><th>Values</th><th>One lawful number</th><th>of those, given back</th>"
        "<th>None, or more than one</th></tr></thead><tbody>%s</tbody></table>" % "".join(nut))

li = fate["calories|LI"]
check = ("<table><thead><tr><th>Photographed panels, read blind</th><th>Read</th><th>Print the number given back</th>"
         "<th>Print the database’s number</th><th>Print another</th></tr></thead><tbody>"
         "<tr><td>number given back</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>"
         "<tr><td>number kept as printed</td><td>%d</td><td colspan=\"2\">%d (the two are one)</td><td>%d</td></tr></tbody></table>" % (
             c["legible_given"], c["given_r_eq"], c["given_v_eq"], c["given_neither"], c["legible_kept"], c["kept_v_eq"],
             c["legible_kept"] - c["kept_v_eq"]))
t = open("template.html").read()
for k, v in {"{{GIVEN}}": given, "{{LOST}}": lost, "{{BAR}}": barsvg, "{{TABLE}}": table, "{{NUTT}}": nutt,
             "{{N}}": format(T["testable"], ","), "{{NLI}}": format(li["testable"], ","), "{{RLI}}": format(li["restored"], ","),
             "{{GLI}}": format(li["given_back"], ","), "{{ULI}}": format(li["unrestorable"], ","), "{{ALI}}": format(li["ambiguous"], ","),
             "{{KALL}}": format(T["kept"], ","), "{{GALL}}": format(T["given_back"], ","), "{{UALL}}": format(T["unrestorable"] + T["ambiguous"], ","),
             "{{PH}}": str(c["with_photograph"]), "{{LG}}": str(c["legible_given"]), "{{LR}}": str(c["given_r_eq"]),
             "{{LV}}": str(c["given_v_eq"]), "{{LN}}": str(c["given_neither"]), "{{SR}}": str(c["given_serving_match_r_eq"]),
             "{{SN}}": str(c["given_serving_match"]), "{{CHECK}}": check}.items():
    t = t.replace(k, v)
assert "{{" not in t
open("index.html", "w").write(t)
print("ok", len(t))
