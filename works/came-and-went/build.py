"""Came and Went: the page, index.html, from projects/why-stopped/session3.json only (NCT numbers, readings, months; no reason text).
Run from this directory: python3 build.py"""
import collections, html, json

s = json.load(open("../../projects/why-stopped/session3.json"))
marks = s["marks"]  # [nct, read, status initial, stop month or "", last update month]
NAME = {"E": "came: participants (enrolment, visits, risk to them)", "S": "came: sites and work (closures, staff, restrictions, supply)",
        "F": "came: money and decisions", "U": "came: the pandemic named, not how", "W": "went: a study of COVID-19 stopped by the pandemic's own course",
        "C": "a study of COVID-19 stopped otherwise", "H": "another pandemic (influenza)", "N": "not the pandemic", "?": "could not be placed"}
ORDER = "ESFU"
mi = lambda m: int(m[:4]) * 12 + int(m[5:7]) - 1
M0, M1 = mi("2019-01"), mi("2026-10")
NCOL = M1 - M0 + 5  # column 0: every earlier end; then a gap
CW, CELL, PER = 12, 3.6, 3
X0, AX = 4, 250
GAP = 3  # empty columns between the earlier column and 2019
cols = collections.defaultdict(lambda: {"up": [], "down": []})
for nct, c, st, stop, lu in marks:
    if st == "S" or not stop:
        continue
    k = 0 if mi(stop) < M0 else mi(stop) - M0 + 1 + GAP
    if c in ORDER:
        cols[k]["up"].append((ORDER.index(c), nct, c, stop))
    else:
        cols[k]["down"].append((0 if c == "W" else 1, nct, c, stop))
g = []
def cell(x, y, nct, c, when):
    t = "%s · ended %s · %s, as read here" % (nct, when, NAME[c])
    return ('<a href="https://clinicaltrials.gov/study/%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" class="k%s">'
            '<title>%s</title></rect></a>' % (nct, x, y, CELL - .5, CELL - .5, "Q" if c == "?" else c, html.escape(t)))
maxup = maxdown = 0
for k, v in cols.items():
    for j, (o, nct, c, stop) in enumerate(sorted(v["up"])):
        g.append(cell(X0 + k * CW + (j % PER) * CELL, AX - 2 - (j // PER + 1) * CELL, nct, c, stop))
    for j, (o, nct, c, stop) in enumerate(sorted(v["down"])):
        g.append(cell(X0 + k * CW + (j % PER) * CELL, AX + 2 + (j // PER) * CELL, nct, c, stop))
    maxup = max(maxup, len(v["up"])); maxdown = max(maxdown, len(v["down"]))
W = X0 * 2 + NCOL * CW
H = AX + 2 + (maxdown // PER + 1) * CELL + 34
g.insert(0, '<line x1="0" x2="%d" y1="%d" y2="%d" class="ax"/>' % (W, AX, AX))
g.append('<text x="%.1f" y="%d" class="yl">earlier</text>' % (X0, H - 8))
for y in range(2019, 2027):
    k = mi("%d-01" % y) - M0 + 1 + GAP
    g.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="tk"/><text x="%.1f" y="%d" class="yl">%d</text>' % (
        X0 + k * CW - 1, X0 + k * CW - 1, AX - 6, H - 20, X0 + k * CW + 1, H - 8, y))
g.append('<text x="%d" y="16" class="lb">it came</text><text x="%d" y="%d" class="lb">it went</text>' % (W - 4, W - 4, AX + 14))
field = ('<svg class="field" viewBox="0 0 %d %d" role="img" aria-label="Every stopped study whose reason names the pandemic, one square each '
         'at the month the register says it ended: above the line the pandemic came, below it went">%s</svg>' % (W, H, "".join(g)))

# the suspended: still stopped now, at the year their entry last changed
sus = sorted([m for m in marks if m[2] == "S"], key=lambda m: (m[4], m[1]))
by = collections.defaultdict(list)
for m in sus:
    by[m[4][:4]].append(m)
SC, SP = 5, 12
g2, x = [], 4
for y in sorted(by):
    g2.append('<text x="%d" y="%d" class="yl">%s</text>' % (x, 12, y))
    for j, (nct, c, st, stop, lu) in enumerate(by[y]):
        t = "%s · suspended · entry last changed %s · %s, as read here" % (nct, lu, NAME[c])
        g2.append('<a href="https://clinicaltrials.gov/study/%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="k%s"><title>%s</title>'
                  '</rect></a>' % (nct, x + (j % SP) * SC, 18 + (j // SP) * SC, SC - 1, SC - 1, "Q" if c == "?" else c, html.escape(t)))
    x += SP * SC + 14
susp = ('<svg class="strip" viewBox="0 0 %d %d" role="img" aria-label="Suspended studies whose reason names the pandemic, by the year '
        'their entry last changed">%s</svg>' % (x, 18 + 5 * SC + 4, "".join(g2)))

# per year, for every reader (and without the picture)
yr = collections.defaultdict(collections.Counter)
for nct, c, st, stop, lu in marks:
    if st != "S" and stop:
        yr["before 2019" if stop < "2019" else stop[:4]][c] += 1
rows = []
for y in sorted(yr, key=lambda y: (y != "before 2019", y)):
    c = yr[y]
    rows.append("<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>" % (
        y, c["E"], c["S"], c["F"], c["U"], c["W"], c["C"], c["H"] + c["N"] + c["?"]))
table = ("<table><thead><tr><th>Ended</th><th>Participants</th><th>Sites, work</th><th>Money, decisions</th><th>Named only</th>"
         "<th>Went</th><th>Of COVID-19, otherwise</th><th>Other</th></tr></thead><tbody>%s</tbody></table>" % "".join(rows))

cat, grp = s["by_category"], s["by_group"]
fill = {"FIELD": field, "SUSP": susp, "TABLE": table, "N": "{:,}".format(s["flagged"]), "CAME": "{:,}".format(grp["came"]),
        "WENT": str(grp["went"]), "E": str(cat["E"]), "S": str(cat["S"]), "F": str(cat["F"]), "U": str(cat["U"]),
        "C": str(cat["C"]), "H": str(cat["H"]), "NN": str(cat["N"]), "Q": str(cat["?"]), "MC": s["median_stop_came"],
        "MW": s["median_stop_went"], "GAP": str(s["median_gap_months"]), "NS": str(len(sus)),
        "NOEND": str(sum(1 for m in marks if m[2] != "S" and not m[3])), "SHOWN": "{:,}".format(sum(1 for m in marks if m[2] != "S" and m[3])),
        "PRE": str(sum(1 for m in marks if m[2] != "S" and m[3] and m[3] < "2020-01" and m[1] in ORDER))}
page = open("template.html").read()
for k, v in fill.items():
    page = page.replace("{{%s}}" % k, v)
assert "{{" not in page
open("index.html", "w").write(page)
print(len(page), maxup, maxdown)
