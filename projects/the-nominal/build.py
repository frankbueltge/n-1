"""Project 20: the study page, index.html, from session1.json (registered count), check1_compare.json (the check) and explore1.json
(exploratory); session 2 from session2.json (registered) and explore2.json (exploratory). Counts and figures only; no bell's row is drawn. Plateau form (T8): numbered sections, each naming the others it
connects to; a figure is the first entryway."""
import json, math

s = json.load(open("session1.json")); c = json.load(open("check1_compare.json")); e = json.load(open("explore1.json"))
s2 = json.load(open("session2.json")); e2 = json.load(open("explore2.json"))
f = lambda x: "{:,}".format(x)
W = 1000

def density(hist, width, lo, hi):
    n = sum(v for k, v in hist.items())
    return {int(k): v / n / width for k, v in hist.items() if lo <= int(k) < hi}, n

def fig_offsets():
    H, X0, lo, hi = 260, 30, -100, 100
    sx = lambda c: X0 + (c - lo) * (W - 2 * X0) / (hi - lo)
    ten, nt = density(e["tenor_d_hist_10c"], 10, lo, hi)
    rel, nr = density(e["r_hist_5c"], 5, lo, hi)
    mx = max(max(ten.values()), max(rel.values()))
    sy = lambda d: 10 + H - H * d / mx
    out = []
    for k, d in sorted(ten.items()):
        out.append('<g><title>rings whose tenor sits %+d to %+d cents from its named note: %s</title><rect class="t" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></g>'
                   % (k, k + 10, f(e["tenor_d_hist_10c"][str(k)]), sx(k) + .5, sy(d), sx(k + 10) - sx(k) - 1, 10 + H - sy(d)))
    for k, d in sorted(rel.items()):
        out.append('<g><title>bells %+d to %+d cents from their own tenor: %s</title><rect class="r" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></g>'
                   % (k, k + 5, f(e["r_hist_5c"][str(k)]), sx(k) + 1.5, sy(d), sx(k + 5) - sx(k) - 3, 10 + H - sy(d)))
    for c in range(lo, hi + 1, 25):
        out.append('<line class="ax" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/><text class="yr" x="%.1f" y="%d" text-anchor="middle">%+d</text>'
                   % (sx(c), sx(c), H + 10, H + 16, sx(c), H + 34, c) if c else
                   '<line class="z" x1="%.1f" x2="%.1f" y1="4" y2="%d"/><text class="yr" x="%.1f" y="%d" text-anchor="middle">0 cents</text>' % (sx(c), sx(c), H + 16, sx(c), H + 34))
    out.append('<line class="hs" x1="%.1f" x2="%.1f" y1="4" y2="%d"/><line class="hs" x1="%.1f" x2="%.1f" y1="4" y2="%d"/>' % (sx(-50), sx(-50), H + 10, sx(50), sx(50), H + 10))
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Two distributions on one axis of cents: rings against concert pitch, wide and flat; bells against their own tenor, narrow and tall">%s</svg>' % (W, H + 44, "".join(out))

def fig_eras():
    eras = [k for k in e["by_50y_era"] if k != "None" and int(k) >= 1350]
    H, X0 = 220, 60
    cw = (W - X0 - 10) / len(eras)
    sy = lambda v: 10 + H - H * v / 30
    out = []
    for v in (0, 10, 20, 30):
        out.append('<line class="ax" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="yr" x="%d" y="%.1f" text-anchor="end">%d</text>' % (X0, W - 10, sy(v), sy(v), X0 - 8, sy(v) + 5, v))
    pt, pr = [], []
    for i, k in enumerate(eras):
        b = e["by_50y_era"][k]; x = X0 + (i + .5) * cw
        out.append('<text class="yr" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (x, H + 34, k + "s" if i % 2 == 0 or len(eras) < 10 else ""))
        if b["median_abs_tenor_d"] is not None:
            pt.append((x, sy(b["median_abs_tenor_d"])))
            out.append('<g><title>tenors cast %s-%d: %s rings, median %.1f cents from A = 440 Hz</title><circle class="t" cx="%.1f" cy="%.1f" r="7"/></g>'
                       % (k, int(k) + 49, f(b["rings_tenor_cast"]), b["median_abs_tenor_d"], x, sy(b["median_abs_tenor_d"])))
        if b["median_abs_r"] is not None:
            pr.append((x, sy(b["median_abs_r"])))
            out.append('<g><title>bells cast %s-%d: %s bells, median %.1f cents from their own tenor</title><circle class="r" cx="%.1f" cy="%.1f" r="7"/></g>'
                       % (k, int(k) + 49, f(b["bells_r"]), b["median_abs_r"], x, sy(b["median_abs_r"])))
    line = lambda p, cl: '<polyline class="%s" points="%s"/>' % (cl, " ".join("%.1f,%.1f" % q for q in p))
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Median distance in cents by fifty-year era of casting: rings from concert pitch stay near 24 until 1900 and fall after; bells from their own tenor fall slowly">%s%s%s</svg>' % (
        W, H + 44, line(pt, "lt"), line(pr, "lr"), "".join(out))

def fig_years():
    yc = {int(k): v for k, v in e["year_counts"].items() if 1300 <= int(k) < 1600}
    H, X0 = 200, 30
    cw = (W - 2 * X0) / 300
    mx = max(yc.values())
    out = []
    for y in range(1300, 1600):
        v = yc.get(y, 0)
        if not v:
            continue
        h = H * math.sqrt(v / mx)
        cl = "t" if y % 100 == 99 else ("r" if y % 50 == 0 else "o")
        out.append('<g><title>%d: %s bells</title><rect class="%s" x="%.2f" y="%.1f" width="%.2f" height="%.1f"/></g>' % (y, f(v), cl, X0 + (y - 1300) * cw, 10 + H - h, max(cw - .4, 1.2), h))
    for y in range(1300, 1601, 50):
        x = X0 + (y - 1300) * cw
        out.append('<line class="ax" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/><text class="yr" x="%.1f" y="%d" text-anchor="middle">%d</text>' % (x, x, H + 10, H + 16, x, H + 34, y))
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Bells by the year the record gives them, 1300 to 1599: tall columns at 1399, 1499 and 1599, and at the round fifties">%s</svg>' % (W, H + 44, "".join(out))

def fig_circle():
    H, X0 = 240, 30
    h = {int(k): v for k, v in e2["hist_1c"].items()}
    n = sum(h.values()); ev = n / 100
    sx = lambda c: X0 + (c + 50) * (W - 2 * X0) / 100
    mx = max(h.values())
    sy = lambda v: 10 + H - H * v / mx
    out = ['<line class="hs" x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f"/>' % (sx(-50), sx(50), sy(ev), sy(ev))]
    for k in range(-50, 50):
        v = h.get(k, 0)
        out.append('<g><title>%+d to %+d cents above the nearest key at A = 440 Hz: %s rings</title><rect class="o" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></g>'
                   % (k, k + 1, f(v), sx(k) + .5, sy(v), sx(k + 1) - sx(k) - 1, 10 + H - sy(v)))
    for lab, key in (("A = 435", "A=435 (diapason normal)"), ("A = 439", "A=439 (new philharmonic)"), ("A = 440", "A=440"), ("A = 452.4", "A=452.4 (old philharmonic)")):
        c0 = e2["standards_positions"][key]; x = sx(c0)
        out.append('<line class="z" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/><text class="yr" x="%.1f" y="%d" text-anchor="%s">%s</text>'
                   % (x, x, H + 10, H + 18, x, H + 36 + (16 if key.startswith("A=439") else 0), "end" if c0 > 40 else "middle", lab))
    out.append('<text class="yr" x="%.1f" y="22">-50</text><text class="yr" x="%.1f" y="22" text-anchor="end">+50 cents</text>' % (sx(-50), sx(50)))
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Rings by where their heaviest bell stands between two keys, in one-cent steps: nearly flat, with a tall column at A = 440 and a cluster near A = 435">%s</svg>' % (W, H + 60, "".join(out))

def era_rows():
    rows = []
    for k, t in e2["by_cast_25y"].items():
        rows.append("<tr><td>%s-%d</td><td>%s</td><td>%.1f %%</td><td>%.1f %%</td><td>%.1f %%</td></tr>" % (
            k, int(k) + 24, f(t["n"]), 100 * t["A=435 (diapason normal)"]["share"], 100 * t["A=440"]["share"], 100 * t["A=452.4 (old philharmonic)"]["share"]))
    return "".join(rows)

P2 = s2["predictions"]
preds2 = [
    ("P1", "Positions not spread evenly, but weakly held (concentration at most 0.25).", "concentration %.2f over %s rings." % (s2["all"]["R"], f(s2["all"]["n"]))),
    ("P2", "Rings tuned (or, without a tuning year, cast) 1950 or later: concentration at least 0.5, centred within 10 cents of A = 440.", "%.2f, centred at %+.1f." % (s2["by_era"]["1950 and later"]["R"], s2["by_era"]["1950 and later"]["mean_cents"])),
    ("P3", "1850-1899: concentration at least 0.2, centred on old philharmonic pitch (+48).", "%.2f, centred at %+.1f." % (s2["by_era"]["1850-1899"]["R"], s2["by_era"]["1850-1899"]["mean_cents"])),
    ("P4", "Before 1800: concentration at most 0.10.", "%.3f." % s2["by_era"]["before 1800"]["R"]),
    ("P5", "Two thirds of large foundries 1880-1949 hold a house pitch.", "%d of %d." % (sum(1 for v in s2["foundries_1880_1949"].values() if v["rayleigh_p"] < 0.01), len(s2["foundries_1880_1949"]))),
    ("P6", "Taylor's and Gillett's centres differ by more than 10 cents.", "%+.1f and %+.1f." % (s2["foundries_1880_1949"]["Loughborough"]["mean_cents"], s2["foundries_1880_1949"]["Gillett"]["mean_cents"])),
    ("P7", "At least 30 % of rings with a tuning year have a tenor cast 50 years before it.", "%s of %s." % (f(s2["retune"]["gap_ge_50"]), f(s2["retune"]["with_tuneyr"]))),
    ("P8", "The tower file's frequency agrees with the tenor's for 95 %.", "%s of %s." % (f(s2["check"]["agree"]), f(s2["check"]["rings_with_tower_hz"]))),
]
items2 = "".join('<li><b>%s %s</b> %s %s</li>' % (k, "held" if P2[k] else "failed", t, o) for k, t, o in preds2)
nh2 = sum(1 for k in P2 if P2[k] is True)
al = e2["all"]
P = s["predictions"]
preds = [
    ("P1", "The file holds at least 40,000 bells.", "%s bells (seen before the count, while the parser was written)." % f(s["bells"])),
    ("P2", "At least 25 % carry a nominal.", "%.1f %% (seen before the count, as P1)." % (100 * s["share_with_nominal"])),
    ("P3", "Median distance from the named note at most 20 cents.", "%.1f cents." % s["median_abs_dev_cents"]),
    ("P4", "At least 90 % within 50 cents of the named note.", "%.1f %%." % (100 * s["share_abs_dev_le_50"])),
    ("P5", "Weight-pitch slope between -0.40 and -0.27.", "%.3f." % s["fit"]["slope"]),
    ("P6", "Scatter about it at most a quarter octave.", "%.2f octave." % s["fit"]["resid_sd_octaves"]),
    ("P7", "Before 1600 the commonest year is 1499 or 1599.", "1499, %s bells." % f(s["modal_years_before_1600"][0][1])),
    ("P8", "At least 20 % of weights are estimates.", "%.1f %%." % (100 * s["share_estimated"])),
    ("P9", "Old trebles of eight at least 10 cents sharp of their tenor; new ones within 5.", "old: %+.1f cents (%d bells); new: %+.1f (%d)." % (
        s["trebles_of_8"]["old_median_r"], s["trebles_of_8"]["old_n"], s["trebles_of_8"]["new_median_r"], s["trebles_of_8"]["new_n"])),
    ("P10", "The check agrees on at least 19 of 20.", "%d of %d; this page's cents within %.1f of Dove's own." % (c["agree_all_three"], c["of"], c["max_abs_diff_cents_vs_dove"])),
]
held = {k: v for k, v in P.items()}; held["P10"] = c["agree_all_three"] >= 19
items = "".join('<li><b>%s %s</b> %s %s</li>' % (k, "held" if held[k] else "failed", t, o) for k, t, o in preds)
nh = sum(1 for k in held if held[k])
far = e["bells_named_not_nearest_in_rings"]
b19 = e["by_50y_era"]

page = open("template.html").read()
rep = {
    "{{N}}": f(s["bells"]), "{{NN}}": f(s["with_nominal"]), "{{RINGS}}": f(e["rings_with_tenor_d"]),
    "{{MT}}": "%.0f" % e["median_abs_tenor_d"], "{{MR}}": "%.1f" % e["median_abs_r"], "{{GT25}}": "%.0f %%" % (100 * e["share_abs_tenor_d_gt_25"]),
    "{{FIG1}}": fig_offsets(), "{{FIG2}}": fig_eras(), "{{FIG3}}": fig_years(),
    "{{MD}}": "%.0f" % s["median_abs_dev_cents"], "{{LE50}}": "%.1f %%" % (100 * s["share_abs_dev_le_50"]),
    "{{FAR}}": f(far["ring_offset"] + far["inside_ring"]), "{{FARO}}": f(far["ring_offset"]), "{{FARI}}": f(far["inside_ring"]),
    "{{E1850}}": "%.0f" % b19["1850"]["median_abs_tenor_d"], "{{E1950}}": "%.0f" % b19["1950"]["median_abs_tenor_d"], "{{E2000}}": "%.0f" % b19["2000"]["median_abs_tenor_d"],
    "{{R1400}}": "%.0f" % b19["1400"]["median_abs_r"], "{{R1900}}": "%.0f" % b19["1900"]["median_abs_r"],
    "{{PRE}}": f(e["pre1600"]["n"]), "{{CIRCA}}": f(e["pre1600"]["circa"]), "{{E99}}": f(e["pre1600"]["ending_99"]), "{{E50}}": f(e["pre1600"]["ending_00_or_50"]),
    "{{Y1499}}": f(e["year_counts"]["1499"]), "{{Y1399}}": f(e["year_counts"]["1399"]), "{{Y1599}}": f(e["year_counts"]["1599"]),
    "{{FN}}": f(s["fit"]["n"]), "{{SL}}": "%.2f" % s["fit"]["slope"], "{{SD}}": "%.2f" % s["fit"]["resid_sd_octaves"],
    "{{SLO}}": "%.2f" % e["fit_by_era_shape"]["before 1800 / standard"]["slope"], "{{SDO}}": "%.2f" % e["fit_by_era_shape"]["before 1800 / standard"]["resid_sd_octaves"],
    "{{SLN}}": "%.2f" % e["fit_by_era_shape"]["1900 and after / standard"]["slope"], "{{SDN}}": "%.2f" % e["fit_by_era_shape"]["1900 and after / standard"]["resid_sd_octaves"],
    "{{PREDS}}": items, "{{NH}}": str(nh),
    "{{FIG4}}": fig_circle(), "{{ERAS2}}": era_rows(), "{{PREDS2}}": items2, "{{NH2}}": str(nh2), "{{R2}}": f(al["n"]),
    "{{C440}}": f(al["A=440"]["within_1.5c"]), "{{S440}}": "%.1f %%" % (100 * al["A=440"]["share"]),
    "{{C435}}": f(al["A=435 (diapason normal)"]["within_1.5c"]), "{{S435}}": "%.1f %%" % (100 * al["A=435 (diapason normal)"]["share"]),
    "{{C452}}": f(al["A=452.4 (old philharmonic)"]["within_1.5c"]), "{{S452}}": "%.1f %%" % (100 * al["A=452.4 (old philharmonic)"]["share"]),
    "{{CONC}}": "%.2f" % s2["all"]["R"], "{{G435}}": "%.0f %%" % (100 * e2["by_foundry"]["Gillett"]["A=435 (diapason normal)"]["share"]),
    "{{W440}}": "%.0f %%" % (100 * e2["by_foundry"]["Whitechapel"]["A=440"]["share"]),
}
for k, v in rep.items():
    page = page.replace(k, v)
s3 = json.load(open("session3.json"))
e3 = json.load(open("explore3.json"))
for k, v in {"{{T1970}}": "%.0f %%" % (100 * s3["decades"]["1970"]["share_440"]), "{{T1980}}": "%.0f %%" % (100 * s3["decades"]["1980"]["share_440"]),
             "{{T1990}}": "%.0f %%" % (100 * s3["decades"]["1990"]["share_440"]), "{{T2000}}": "%.0f %%" % (100 * s3["decades"]["2000"]["share_440"]),
             "{{O1990}}": str(e3["1990-2029"]["tenor_50y_older_than_tuning"]["n"]), "{{N1990}}": str(e3["1990-2029"]["all"]["n"]),
             "{{BO}}": "%.1f" % e3["1990-2029"]["tenor_50y_older_than_tuning"]["median_beat_hz"],
             "{{BN}}": "%.1f" % e3["1990-2029"]["tenor_new_when_sounded"]["median_beat_hz"]}.items():
    page = page.replace(k, v)
assert "{{" not in page, page[page.index("{{"):page.index("{{") + 30]
open("index.html", "w").write(page)
print("ok", nh)
