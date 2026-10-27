"""Project 19: the study page, index.html, from session1.json (registered), session1b.json (corrected), check1.json, explore1.json and
explore1b.json, explore1c.json (exploratory). Numbers only."""
import json, math

s = json.load(open("session1.json")); sb = json.load(open("session1b.json"))
c = json.load(open("check1.json")); e = json.load(open("explore1.json")); h = json.load(open("explore1b.json")); e3 = json.load(open("explore1c.json"))
f = lambda x: "{:,}".format(x)
pc = lambda a, b: "%.1f %%" % (100.0 * a / b)
W, X0 = 1008, 8
from count1 import grid_cal, grid_fat

def spikes(hist, lo, hi, scale, grid, unit, label):
    """One column per step from lo to hi (in hist's integer units); height on a square-root scale."""
    n = hi - lo; H = 220; cw = (W - 2 * X0) / n
    vals = [hist.get(str(k), 0) for k in range(lo, hi + 1)]
    mx = math.sqrt(max(vals))
    out = []
    for i, k in enumerate(range(lo, hi + 1)):
        v = vals[i]
        if not v:
            continue
        x = k / scale; hh = H * math.sqrt(v) / mx
        if grid(x):
            cls = "g"
        else:
            cls = "s0"
        out.append('<g><title>%s %s: %s labels</title><rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" class="%s"/></g>' % (
            ("%g" % x), unit, f(v), X0 + i * cw - 0.4, 10 + H - hh, max(cw, 1.2), hh, cls))
    step = {10: 100, 100: 100}[scale]
    for k in range(lo, hi + 1, step):
        x = X0 + (k - lo) * cw
        out.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="ax"/><text x="%.1f" y="%d" class="yr">%g %s</text>' % (
            x, x, H + 10, H + 16, x + 2, H + 32, k / scale, unit))
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>' % (W, H + 40, label, "".join(out))

fig1 = spikes(h["calories_by_tenth_kcal_0_300"], 400, 1300, 10, grid_cal, "kcal",
              "Declared calories per serving from 40 to 130, one column per tenth of a calorie")
fig2 = spikes(h["fat_by_hundredth_g_0_15"], 300, 1000, 100, grid_fat, "g",
              "Declared total fat per serving from 3 to 10 grams, one column per hundredth of a gram")

# figure 3: what the off-grid numbers are, three nutrients, one bar each
cls_order = [("on_grid", "on the grid", "g"), ("sig3_grid_behind", "a grid number sent to 100 g and back, three digits kept", "s0"),
             ("sig3_no_grid_behind", "the round trip, no grid number behind it", "s2"),
             ("not_sig3_grid_behind", "not the round trip", "s1"), ("not_sig3_no_grid_behind", "not the round trip", "s1"),
             ("untestable", "cannot be tested", "s3")]
rows = []
y = 10
for name, lab in (("calories", "Calories"), ("fat", "Total fat"), ("sodium", "Sodium")):
    d = e3["classes"][name]; tot = sum(d.values()); x = 120
    rows.append('<text x="0" y="%d" class="lb">%s</text>' % (y + 20, lab))
    for k, t, cl in cls_order:
        v = d.get(k, 0); w = (W - 130) * v / tot
        rows.append('<g><title>%s: %s, %s of %s</title><rect x="%.1f" y="%d" width="%.1f" height="28" class="%s"/></g>' % (
            lab, t, f(v), f(tot), x, y, w, cl))
        x += w
    y += 44
fig3 = '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Declared values by kind, for calories, total fat and sodium">%s</svg>' % (W, y, "".join(rows))

# figure 4: declared calories minus 4-4-9 of the declared grams, 5-kcal bins
A = {int(k): v for k, v in sb["atwater"]["hist_5kcal_clipped_200"]}
lo, hi = -60, 40; bins = list(range(lo, hi + 5, 5)); H4 = 200; bw = (W - 2 * X0) / len(bins); mx = max(A.get(b, 0) for b in bins)
g4 = []
for i, b in enumerate(bins):
    v = A.get(b, 0); hh = H4 * v / mx
    g4.append('<g><title>%d to %d kcal: %s labels</title><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="%s"/></g>' % (
        b, b + 5, f(v), X0 + i * bw, 10 + H4 - hh, bw - 2, hh, "s0" if b in (-5, 0) else "s1"))
    if b % 20 == 0:
        g4.append('<text x="%.1f" y="%d" class="yr">%s</text>' % (X0 + i * bw, H4 + 30, '0' if b == 0 else '%+d' % b))
fig4 = '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Declared calories minus four, four and nine times the declared grams, in five-calorie bins">%s</svg>' % (W, H4 + 40, "".join(g4))

P = s["predictions_registered"]; PB = sb["predictions_registered"]
txt = {
    "P1 >=400000 foods": "At least 400,000 branded foods: %s (corrected count %s)." % (f(s["foods"]), f(sb["foods"])),
    "P2 >=85% declare calories": "At least 85 %% declare calories: %s." % pc(sb["declared"]["calories"], sb["foods"]),
    "P3 >=90% calories on grid": "At least 90 %% of declared calories on the grid: %s." % pc(sb["on_grid"]["calories"], sb["declared"]["calories"]),
    "P4 >=90% total fat on grid": "At least 90 %% of declared total fat on the grid: %s." % pc(sb["on_grid"]["fat"], sb["declared"]["fat"]),
    "P5 >=90% sodium on grid": "At least 90 %% of declared sodium on the grid: %s." % pc(sb["on_grid"]["sodium"], sb["declared"]["sodium"]),
    "P6 median |d| <=10 kcal": "The median gap between declared calories and 4-4-9 of the declared grams is at most 10 kcal: %g kcal." % sb["atwater"]["median_abs_d"],
    "P7 >=80% trans fat exactly 0": "At least 80 %% of declared trans fat is exactly 0: %s." % pc(sb["trans_fat_zero"], sb["trans_fat_declared"]),
}
li = ['<li><b>%s</b> %s</li>' % ("Held." if PB[k] else "Failed.", txt[k]) for k in P]
li.append('<li><b>Failed.</b> The live database agrees on at least 19 of 20 foods drawn at random: %d of 20 answered (the rest were refused for '
          'rate), %d agree. In each of the three that disagree, this file holds a number just off the grid (8.01, 8.03, 8.99 g) and the live '
          'service gives the grid number (8.0, 8.0, 9.0), which is also the file\'s number rounded to one decimal.</li>' % (c["answered"], c["agree"]))
ec = e["classes"]["calories"]; off_c = sum(v for k, v in ec.items() if k != "on_grid")
e3c = e3["classes"]["calories"]
V = {
    "{{N}}": f(sb["foods"]), "{{NC}}": f(sb["declared"]["calories"]),
    "{{GC}}": pc(sb["on_grid"]["calories"], sb["declared"]["calories"]), "{{GF}}": pc(sb["on_grid"]["fat"], sb["declared"]["fat"]),
    "{{GS}}": pc(sb["on_grid"]["sodium"], sb["declared"]["sodium"]), "{{GFI}}": pc(sb["on_grid"]["fiber"], sb["declared"]["fiber"]),
    "{{GT}}": pc(sb["on_grid"]["transFat"], sb["declared"]["transFat"]),
    "{{OFFC}}": f(off_c), "{{RT}}": f(ec["off_explained_round_trip"]), "{{RTP}}": pc(ec["off_explained_round_trip"], off_c),
    "{{S3}}": f(e3c["sig3_grid_behind"]), "{{S3P}}": pc(e3c["sig3_grid_behind"], off_c),
    "{{BACK}}": pc(e3c["on_grid"] + e3c["sig3_grid_behind"], sum(e3c.values())),
    "{{NOG}}": f(e3c["sig3_no_grid_behind"]), "{{DIFF}}": f(e3c["not_sig3_grid_behind"] + e3c["not_sig3_no_grid_behind"]), "{{C801}}": f(h["calories_by_tenth_kcal_0_300"].get("801", 0)),
    "{{C800}}": f(h["calories_by_tenth_kcal_0_300"].get("800", 0)), "{{C899}}": f(h["calories_by_tenth_kcal_0_300"].get("899", 0)),
    "{{AT}}": f(sb["atwater"]["n"]), "{{AT5}}": "%.0f %%" % (100 * sb["atwater"]["share_abs_d_le_5"]),
    "{{AT10}}": "%.0f %%" % (100 * sb["atwater"]["share_abs_d_le_10"]), "{{AT0}}": "%.1f %%" % (100 * sb["atwater"]["share_d_eq_0"]),
    "{{FIG1}}": fig1, "{{FIG2}}": fig2, "{{FIG3}}": fig3, "{{FIG4}}": fig4, "{{PREDS}}": "".join(li),
}
t = open("template.html").read()
for k, v in V.items():
    t = t.replace(k, v)
assert "{{" not in t, t[t.find("{{"):t.find("{{") + 30]
open("index.html", "w").write(t)
print("ok", len(t))
