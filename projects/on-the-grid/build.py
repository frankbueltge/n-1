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

# session 2: the lattice of serving size (10-130 g or ml) against lawful calories (10-300), predicted and held
from decimal import ROUND_HALF_EVEN
from explore2 import predicted
s2 = json.load(open("session2.json")); e2 = json.load(open("explore2.json")); c2 = json.load(open("check2.json"))
cells = json.load(open("session2_cells.json"))["cells"]
GR = list(range(10, 51, 5)) + list(range(60, 301, 10)); SS = list(range(10, 131))
cw5 = (W - 60) / len(SS); rh = 7

def lattice(kind):
    out = []
    for j, g in enumerate(reversed(GR)):
        y = 6 + j * rh
        if g % 50 == 0 or g == 10:
            out.append('<text x="0" y="%.1f" class="yr">%d</text>' % (y + rh, g))
        if kind == "pred":
            run = None
            for i, sv in enumerate(SS + [None]):
                v = predicted(g, sv, ROUND_HALF_EVEN) if sv is not None else None
                if run and (v != run[1]):
                    out.append('<rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" class="%s"/>' % (
                        60 + run[0] * cw5, y, (i - run[0]) * cw5, rh - 1, "g" if run[1] else "s0"))
                    run = None
                if run is None and sv is not None:
                    run = (i, v)
        else:
            for i, sv in enumerate(SS):
                k = "%d|%d" % (g, sv)
                if k not in cells:
                    continue
                n, on = cells[k]
                out.append('<g><title>%d kcal on %d g or ml: %s records, %s on the grid</title><rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" class="%s"/></g>' % (
                    g, sv, f(n), f(on), 60 + i * cw5, y, cw5, rh - 1, "g" if on * 2 >= n else "s0"))
    H = 6 + len(GR) * rh
    for sv in range(10, 121, 20):
        x = 60 + (sv - 10) * cw5
        out.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="ax"/><text x="%.1f" y="%d" class="yr">%d g</text>' % (x, x, H, H + 6, x + 2, H + 22, sv))
    lab = ("What the arithmetic predicts: for each lawful calorie number (rows, 10 to 300) and each serving size (columns, 10 to 130 g or ml), "
           "whether sending it to 100 g as a whole number and back with three digits returns it unchanged") if kind == "pred" else (
           "What the record holds: the same lattice, one cell for every combination at least one food has, coloured by whether most of them are on the grid")
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>' % (W, H + 30, lab, "".join(out))

fig5 = lattice("pred"); fig6 = lattice("held")
win_n = win_on = win_agree = 0
for g in GR:
    for sv in SS:
        k = "%d|%d" % (g, sv)
        if k in cells:
            n, on = cells[k]; win_n += n; win_on += on
            win_agree += on if predicted(g, sv, ROUND_HALF_EVEN) else n - on

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
L2 = s2["LI_calories"]; P2 = s2["predictions_registered"]; B = s2["LI_calories_bands"]
b10 = [B["10<=g<100|s<=100"]["n"] + B["10<=g<100|s>100"]["n"], B["10<=g<100|s<=100"]["on"] + B["10<=g<100|s>100"]["on"]]
he = e2["consistency"]["calories|LI|half_even"]; hu = e2["consistency"]["calories|LI|half_up"]
sod = e2["consistency"]["sodium|LI|half_even"]; fat = e2["consistency"]["fat|LI|half_even"]
he_not = he.get("on_not_consistent", 0) + he.get("off_not_consistent", 0); hu_not = hu.get("on_not_consistent", 0) + hu.get("off_not_consistent", 0)
GD = e2["groups"]["D"]; nD = sum(GD["source"].values()); nDo = nD - GD["source"].get("LI", 0)
A2 = e2["calories_predicted_agree"]["LI|half_even"]
txt2 = [
    (P2["P1 LI calories: predicted (g, s only) agrees with actual on-grid status >= 97%"],
     "From the serving size and the lawful number alone, the arithmetic predicts for at least 97 %% of foods whether the record holds a "
     "number on the grid: %s as registered. With the way back rounded as the record rounds it (decimal, half to even, found after the "
     "count): %s." % (pc(L2["agree"], L2["n"]), pc(A2["agree"], A2["n"]))),
    (P2["P2 LI on-grid calories: consistent with back-conversion >= 95%"],
     "At least 95 %% of calorie values on the grid are the record's own back-conversion: %s." % pc(L2["on_consistent"], L2["on"])),
    (P2["P3 LI calories g>=100, s<=100: on-grid share >= 97%"],
     "Where the arithmetic cannot move a number of 100 or more (servings up to 100 g), at least 97 %% are on the grid: %s. "
     "Most of the rest are numbers no lawful one explains (below)." % pc(B["g>=100|s<=100"]["on"], B["g>=100|s<=100"]["n"])),
    (P2["P4 LI calories 10<=g<100: on-grid share <= 60%"],
     "Below 100 calories, where three digits keep a tenth, at most 60 %% are on the grid: %s." % pc(b10[1], b10[0])),
    (P2["P5 off-grid, consistent, no ghost (class D): non-LI share >= 25%"],
     "Of the numbers no lawful one explains, at least 25 %% come from sources other than the main one, which supplies 94 %% of all: %s." % ("%.1f %%" % (100 * s2["class_D_other_share"]))),
    (P2["P6 LI on-grid fat: consistent >= 95%"], "Fat the same, at least 95 %%: %s." % ("%.1f %%" % (100 * s2["LI_fat_on_consistent_rate"]))),
    (P2["P7 LI on-grid sodium: consistent >= 95%"], "Sodium the same, at least 95 %%: %s." % ("%.1f %%" % (100 * s2["LI_sodium_on_consistent_rate"]))),
    (c2["P8 agree >=19 of 20"], "The live database agrees on at least 19 of 20 foods drawn at random: %d of 20 answered (the rest refused for rate), "
     "%d agrees." % (c2["answered"], c2["agree"])),
]
li2 = ['<li><b>%s</b> %s</li>' % ("Held." if ok else "Failed.", tx) for ok, tx in txt2]
V.update({
    "{{FIG5}}": fig5, "{{FIG6}}": fig6, "{{PREDS2}}": "".join(li2), "{{N2}}": f(L2["n"]),
    "{{WIN}}": f(win_n), "{{WINP}}": pc(win_agree, win_n), "{{HENOT}}": f(he_not), "{{HUNOT}}": f(hu_not),
    "{{SODNOT}}": f(sod.get("on_not_consistent", 0) + sod.get("off_not_consistent", 0)), "{{SODN}}": f(sum(sod.values())),
    "{{ND}}": f(nD), "{{NDO}}": f(nDo), "{{NDW}}": f(GD["v_whole"].get("True", 0)), "{{ND100}}": f(GD["s_eq_100"].get("True", 0)),
    "{{NDNZ}}": f(GD["marketCountry"].get("New Zealand", 0)), "{{NE}}": f(sum(e2["groups"]["E"]["source"].values())),
})
t = open("template.html").read()
for k, v in V.items():
    t = t.replace(k, v)
assert "{{" not in t, t[t.find("{{"):t.find("{{") + 30]
open("index.html", "w").write(t)
print("ok", len(t))
