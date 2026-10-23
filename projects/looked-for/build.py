"""Project 17: the study page, index.html, from session1.json and result1.json (counts only; no record)."""
import html, json

s = json.load(open("session1.json"))
r = json.load(open("result1.json"))
A, T = s["by_status"]["ABSENT"], s["total"]
f = lambda x: "{:,}".format(x)
pc = lambda a, b: "%.1f %%" % (100 * a / b)
W, X0 = 1008, 8

# figure 1: all absences as one bar, a segment per dataset (the ten largest drawn apart, the other datasets as one grey run)
top = s["absent_top10"]
rest = A - sum(t["absent"] for t in top)
g, x = [], X0
SHORT = ["Norway, petroleum seabed surveys", "California, kelp forest monitoring", "France, Culicoides surveillance",
         "Sweden, forest inventory", "Ebro delta, phytoplankton", "Sweden, forest inventory (discontinued)",
         "New Zealand, mammal pellets", "Netherlands, beach wash-up", "Nova Scotia, eDNA", "Great Barrier Reef, seagrass"]
for i, t in enumerate(top):
    w = (W - 2 * X0) * t["absent"] / A
    g.append('<g><title>%s: %s absences (%s of all; %s of the dataset\'s %s records)</title>'
             '<rect x="%.1f" y="10" width="%.1f" height="70" class="s%d"/></g>' % (
                 html.escape(t["title"]), f(t["absent"]), pc(t["absent"], A), pc(t["absent"], t["total"]), f(t["total"]),
                 x, max(w - 1.5, 0.5), i % 2))
    if w > 60:
        g.append('<text x="%.1f" y="100" class="lb">%d</text>' % (x + 2, i + 1))
    x += w
w = (W - 2 * X0) * rest / A
g.append('<g><title>the other %s datasets: %s absences (%s)</title><rect x="%.1f" y="10" width="%.1f" height="70" class="bg"/></g>' % (
    f(s["absent_datasets"] - 10), f(rest), pc(rest, A), x, w))
g.append('<text x="%.1f" y="100" class="lb">the other %s datasets</text>' % (x + 2, f(s["absent_datasets"] - 10)))
fig1 = '<svg class="ch" viewBox="0 0 %d 110" role="img" aria-label="All absence records as one bar, divided by the dataset that published them">%s</svg>' % (W, "".join(g))
legend = "".join('<li>%s: <i>%s</i>, %s; %s absences, %s of its records. %s, <a href="https://doi.org/%s">doi:%s</a>.</li>' % (
    SHORT[i], html.escape(t["title"].strip()), html.escape(t["publisher"]), f(t["absent"]), pc(t["absent"], t["total"]),
    {"http://creativecommons.org/licenses/by/4.0/legalcode": "CC BY 4.0", "http://creativecommons.org/licenses/by-nc/4.0/legalcode": "CC BY-NC 4.0",
     "http://creativecommons.org/publicdomain/zero/1.0/legalcode": "CC0"}[t["license"]], t["doi"], t["doi"]) for i, t in enumerate(top))

# figure 2: share of each year's dated records that say absent, 1950-2026
Ay, Py = s["absent_by_year"], s["present_by_year"]
ys = list(range(1950, 2027))
H = 220
mx = max(Ay.get(str(y), 0) / (Ay.get(str(y), 0) + Py.get(str(y), 0)) for y in ys)
cw = (W - 2 * X0) / len(ys)
g2 = []
for i, y in enumerate(ys):
    a, p = Ay.get(str(y), 0), Py.get(str(y), 0)
    h = H * (a / (a + p)) / mx
    g2.append('<g><title>%d: %s absent of %s dated records (%s)</title><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="s0"/></g>' % (
        y, f(a), f(a + p), pc(a, a + p), X0 + i * cw, 10 + H - h, cw - 1.5, h))
    if y % 10 == 0:
        g2.append('<text x="%.1f" y="%d" class="yr">%d</text>' % (X0 + i * cw, H + 32, y))
        g2.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="ax"/>' % (X0 + i * cw, X0 + i * cw, H + 10, H + 16))
for v in (2, 4, 6, 8):
    yv = 10 + H - H * (v / 100) / mx
    g2.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="gr"/><text x="%d" y="%.1f" class="yr">%d %%</text>' % (
        X0, W - X0, yv, yv, X0 + 2, yv - 3, v))
fig2 = '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Share of each year\'s records that say absent, 1950 to 2026">%s</svg>' % (W, H + 40, "".join(g2))

# figure 3: the check, forty squares
g3 = []
for j, row in enumerate(r["rows"]):
    cls = "s0" if row["gbif"] == "ABSENT" else "s1"
    hollow = row["reading"] == "cannot tell"
    g3.append('<g><title>item %d: GBIF %s; read from the publisher\'s words: %s</title><rect x="%d" y="6" width="20" height="20" class="%s"/></g>' % (
        j + 1, row["gbif"].lower(), row["reading"], 6 + j * 25, "ho" if hollow else cls))
fig3 = '<svg class="ch" viewBox="0 0 %d 34" role="img" aria-label="Forty drawn records, by GBIF status and by reading">%s</svg>' % (6 + 40 * 25, "".join(g3))

K = s["absent_by_kingdom"]
kin = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (k, f(v), pc(v, v + s["present_by_kingdom"].get(k, 0)))
              for k, v in K.items() if v > 1000)
inf = s["issue_by_status"]["OCCURRENCE_STATUS_INFERRED_FROM_INDIVIDUAL_COUNT"]
bor = s["issue_by_status"]["OCCURRENCE_STATUS_INFERRED_FROM_BASIS_OF_RECORD"]
unp = s["issue_by_status"]["OCCURRENCE_STATUS_UNPARSABLE"]
P = s["predictions"]
pred = [("P1", "at least 10,000,000 records say absent", P["P1 absent >= 10,000,000"], f(A)),
        ("P2", "under 2 % of all records", P["P2 absent < 2 % of all"], pc(A, T)),
        ("P3", "the ten largest sources hold at least half", P["P3 top ten datasets hold >= half of absent"], "%.1f %%" % (100 * s["absent_top10_share"])),
        ("P4", "more animal absences than plant", P["P4 Animalia absent > Plantae absent"], "%s against %s" % (f(K["Animalia"]), f(K["Plantae"]))),
        ("P5", "at least 10 % of absences inferred by GBIF from a count of zero", P["P5 >= 10 % of absent inferred from a zero count"], "%s, %s" % (f(inf["ABSENT"]), pc(inf["ABSENT"], A))),
        ("P6", "the check agrees on at least 36 of the records I can tell", r["agree"] >= 36, "%d of %d" % (r["agree"], r["tellable"]))]
plist = "".join("<li><b>%s %s.</b> %s: %s.</li>" % (k, "held" if ok else "failed", d, v) for k, d, ok, v in pred)

page = open("template.html").read()
for k, v in {"FIG1": fig1, "FIG2": fig2, "FIG3": fig3, "LEGEND": legend, "KIN": kin, "PRED": plist,
             "TOTAL": f(T), "ABSENT": f(A), "SHARE": pc(A, T), "NDS": f(s["absent_datasets"]), "TOP10": "%.0f %%" % (100 * s["absent_top10_share"]),
             "N1": f(top[0]["absent"]), "N1S": pc(top[0]["absent"], A), "N1D": pc(top[0]["absent"], top[0]["total"]),
             "INFP": f(inf["PRESENT"]), "INFA": f(inf["ABSENT"]), "BOR": f(bor["all"]), "UNP": f(unp["all"]),
             "AGREE": "%d of %d" % (r["agree"], r["tellable"]), "READ": s["started_utc"], "Y23": f(Ay["2023"])}.items():
    page = page.replace("{{%s}}" % k, v)
assert "{{" not in page
open("index.html", "w").write(page)
print("ok", len(page))
