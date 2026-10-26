"""The Last Address: the page, index.html, from projects/full-disc/sets3.json, session3.json and check3.json only (release MBIDs,
medium positions, addresses in frames; no title, artist or sound). Run from this directory: python3 build.py"""
import collections, html, json, statistics

P = "../../projects/full-disc/"
s = json.load(open(P + "sets3.json"))
c = json.load(open(P + "session3.json"))
k = json.load(open(P + "check3.json"))
e = json.load(open(P + "explore3.json"))
FRAME, MAXF = 333000, 360000
sets = s["sets"]

def mmss(f):
    t = f // 75
    return "%d:%02d" % (t // 60, t % 60)

def kind(m, last):
    a = m["address"]
    if a is None: return "u"
    if a == FRAME: return "f"
    return "l" if last else "o"

def mini(r):
    W, BH, G, X0 = 160, 3, 1.2, 2
    n = len(r["media"])
    H = 6 + n * (BH + G) + 10
    sc = (W - 2 * X0) / MAXF
    g = []
    for i, m in enumerate(r["media"]):
        y = 4 + i * (BH + G); kd = kind(m, i == n - 1)
        if kd == "u":
            g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="u"/>' % (X0, y, 12, BH))
        else:
            g.append('<rect x="%.1f" y="%.1f" width="%.2f" height="%.1f" class="%s"/>' % (X0, y, m["address"] * sc, BH, kd))
    cx = X0 + FRAME * sc
    g.append('<line x1="%.2f" x2="%.2f" y1="1" y2="%.1f" class="c"/>' % (cx, cx, 6 + n * (BH + G)))
    last = r["media"][-1]["address"]
    lab = "%d discs" % n + ("" if last is None else " · last %s" % mmss(last))
    g.append('<text x="%.1f" y="%.1f" class="n">%s</text>' % (X0, H - 2, lab))
    t = "MusicBrainz release %s · %s" % (r["release"], lab)
    return ('<a href="https://musicbrainz.org/release/%s"><svg viewBox="0 0 %d %.1f" role="img" aria-label="%s"><title>%s</title>%s</svg></a>'
            % (r["release"], W, H, html.escape(t), html.escape(t), "".join(g)))

order = sorted(sets, key=lambda r: (len(r["media"]), r["media"][-1]["address"] or 0))
shelf = "".join(mini(r) for r in order)

# the remainder: last discs, not at the frame, in two-minute bins
lasts = [r["media"][-1]["address"] for r in sets if r["media"][-1]["address"] not in (None, FRAME)]
bins = collections.Counter(min(a // (75 * 120), 39) for a in lasts)
BW, BHMAX = 10, 90
mx = max(bins.values()) if bins else 1
g = []
for b in range(40):
    h = bins[b] / mx * BHMAX
    g.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" class="bar"><title>%d-%d min: %d last discs</title></rect>'
             % (20 + b * BW, 10 + BHMAX - h, BW - 1, h, 2 * b, 2 * b + 2, bins[b]))
g.append('<line x1="20" x2="%d" y1="%d" y2="%d" class="ax"/>' % (20 + 40 * BW, 10 + BHMAX, 10 + BHMAX))
for m in range(0, 81, 10):
    x = 20 + m / 2 * BW
    g.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="tk"/><text x="%.1f" y="%d" class="yl">%d:00</text>' % (x, x, 10 + BHMAX, 14 + BHMAX, x - 8, 26 + BHMAX, m))
cx = 20 + 74 / 2 * BW
g.append('<line x1="%.1f" x2="%.1f" y1="4" y2="%d" class="c"/>' % (cx, cx, 10 + BHMAX))
g.append('<text x="22" y="18" class="yl">%d last discs (most: %d)</text>' % (len(lasts), mx))
remfig = ('<svg class="big" viewBox="0 0 440 %d" role="img" aria-label="How long the last disc of each set plays, in two-minute bins">%s</svg>'
          % (32 + BHMAX, "".join(g)))

# per number of discs
by = collections.defaultdict(list)
for r in sets:
    by[len(r["media"])].append(r)
rows = []
for n in sorted(by):
    rs = by[n]
    nl = [m for r in rs for m in r["media"][:-1]]
    la = [r["media"][-1]["address"] for r in rs if r["media"][-1]["address"] not in (None, FRAME)]
    rows.append("<tr><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%s</td></tr>" % (
        n, len(rs), sum(1 for m in nl if m["address"] == FRAME), sum(1 for m in nl if m["address"] not in (None, FRAME)),
        sum(1 for r in rs for m in r["media"] if m["address"] is None), mmss(int(statistics.median(la))) if la else "–"))
table = ("<table><thead><tr><th>Discs in the set</th><th>Sets</th><th>Discs before the last, at 74:00:00</th>"
         "<th>Discs before the last, elsewhere</th><th>Discs nobody measured</th><th>Middle length of the last disc</th></tr></thead>"
         "<tbody>%s</tbody></table>" % "".join(rows))

nl = c["nonlast"]; la = c["last"]
V = {
    "N": len(sets), "R": c["R"], "SINGLES": c["singles"], "FRAMEDISCS": c["frame_discs"],
    "NLF": nl.get("frame", 0), "NLO": nl.get("other", 0), "NLU": nl.get("unmeasured", 0),
    "NLSHARE": round(100 * c["nonlast_frame_share_of_measured"]),
    "LF": la.get("frame", 0), "LO": la.get("other", 0), "LU": la.get("unmeasured", 0),
    "MEDLAST": mmss(int(c["last_not_frame_median_frames"])) if c["last_not_frame_median_frames"] else "–",
    "ALLFULL": e["sets_every_nonlast_at_frame"], "AGREE": k["agree"], "ANS": k["answered"],
    "TOP": c["commonest_leadouts_ge_270000"][0]["frame"], "TOPN": c["commonest_leadouts_ge_270000"][0]["discs"],
    "SECOND": mmss(c["commonest_leadouts_ge_270000"][1]["frame"]) + ":%02d" % (c["commonest_leadouts_ge_270000"][1]["frame"] % 75),
    "SECONDN": c["commonest_leadouts_ge_270000"][1]["discs"],
}
text = json.load(open("text.json"))
out = open("template.html").read()
for key in ("LEAD", "SHELFNOTE", "REMAINDER", "TALLY", "ABOUT"):
    out = out.replace("{{%s}}" % key, text[key].format(**V))
out = out.replace("{{SHELF}}", shelf).replace("{{TABLE}}", table).replace("{{REMFIG}}", remfig)
assert "{{" not in out, "unfilled placeholder"
open("index.html", "w").write(out)
print("ok", len(sets), "sets")
