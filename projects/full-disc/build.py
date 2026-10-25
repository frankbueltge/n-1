"""Project 18: the study page, index.html, from session1.json, check1.json and explore1.json (numbers only)."""
import json

s = json.load(open("session1.json"))
c = json.load(open("check1.json"))
e = json.load(open("explore1.json"))
f = lambda x: "{:,}".format(x)
N = s["rows_parsed"]
B = {int(k): v for k, v in s["by_second"].items()}
M = {int(k): v for k, v in s["by_minute"].items()}
mmss = lambda t: "%d:%02d" % (t // 60, t % 60)
W, X0 = 1008, 8

# figure 1: every disc by playing length, 10-second columns, 0:00 to 90:00
cols = 540
H = 240
vals = [sum(B.get(t, 0) for t in range(i * 10, i * 10 + 10)) for i in range(cols)]
mx = max(vals)
cw = (W - 2 * X0) / cols
g = []
for i, v in enumerate(vals):
    h = H * v / mx
    cls = "s0" if i * 10 in (4430,) or i * 10 in (4790,) else "s1"
    g.append('<g><title>%s to %s: %s discs</title><rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" class="%s"/></g>' % (
        mmss(i * 10), mmss(i * 10 + 9), f(v), X0 + i * cw, 10 + H - h, cw + 0.05, max(h, 0.0), cls))
for m in range(0, 81, 10):
    x = X0 + m * 6 * cw
    g.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="ax"/><text x="%.1f" y="%d" class="yr">%d min</text>' % (
        x, x, H + 10, H + 16, x + 2, H + 32, m))
for m, lab in ((74, "74:00"), (80, "80:00")):
    x = X0 + m * 6 * cw
    g.append('<line x1="%.1f" x2="%.1f" y1="4" y2="%d" class="gr"/><text x="%.1f" y="14" class="lb" text-anchor="end">%s</text>' % (
        x, x, H + 10, x - 4, lab))
fig1 = '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="Every disc by its playing length, in ten-second columns from zero to ninety minutes">%s</svg>' % (W, H + 40, "".join(g))

# figure 2: the last ninety seconds before each ceiling and thirty after, one column per second
def panel(lo, hi, crest, label):
    n = hi - lo
    H2, w2 = 180, (W - 2 * X0) / n
    mx2 = max(B.get(t, 0) for t in range(4380, 4470))
    out = []
    for i, t in enumerate(range(lo, hi)):
        v = B.get(t, 0)
        h = H2 * v / mx2
        out.append('<g><title>%s: %s discs</title><rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" class="%s"/></g>' % (
            mmss(t), f(v), X0 + i * w2, 10 + H2 - h, w2 - 1, h, "s0" if t == crest else "s1"))
        if t % 30 == 0:
            out.append('<text x="%.1f" y="%d" class="yr">%s</text>' % (X0 + i * w2, H2 + 30, mmss(t)))
    i = crest - lo
    out.append('<text x="%.1f" y="%.1f" class="lb" text-anchor="end">%s, %s discs</text>' % (
        X0 + i * w2 - 8, 10 + H2 - H2 * B[crest] / mx2 + 14, mmss(crest), f(B[crest])))
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>' % (W, H2 + 40, label, "".join(out))
fig2a = panel(4350, 4470, 4438, "Discs by playing length, one column per second, from 72:30 to 74:30")
fig2b = panel(4710, 4830, 4797, "Discs by playing length, one column per second, from 78:30 to 80:30")

P = s["predictions"]
lab = {
    "P1 at least 1,000,000 discs": "At least 1,000,000 discs: %s." % f(N),
    "P2 median between 40:00 and 55:00": "The median playing length lies between 40:00 and 55:00: %s." % mmss(int(s["length_seconds"]["median"])),
    "P3 under 1 % at or over 80:00": "Fewer than 1 %% play 80:00 or longer: %s (%.2f %%)." % (f(s["at_or_over_80_00"]), 100 * s["share_at_or_over_80_00"]),
    "P4 bin 79 above every bin 70-78": "The minute 79:00-79:59 holds more discs than any minute from 70 to 78: it holds the fewest (%s, against %s to %s)." % (
        f(M[79]), f(min(M[m] for m in range(70, 79))), f(max(M[m] for m in range(70, 79)))),
    "P5 bin 74 at least 1.2 x bin 75": "The minute 74:00-74:59 holds at least 20 %% more than 75:00-75:59: %s against %s. The crest is in minute 73." % (f(M[74]), f(M[75])),
    "P6 at least 99.9 % reproduced": "At least 99.9 %% of stored disc IDs are reproduced from their tables: %s of %s." % (f(s["reproduced_ids"]), f(N)),
    "P7 under 2 % pregap": "Fewer than 2 %% of discs start track one later than two seconds: %s (%.1f %%), most by under a second." % (f(s["pregap_over_zero"]), 100 * s["pregap_share"]),
}
preds = "".join('<li><b>%s</b> %s</li>' % ("Held." if P[k] else "Failed.", lab[k]) for k in lab)
preds += '<li><b>Held.</b> The live database agrees with the export on at least 19 of 20 drawn discs: %d of %d answered, all %d agree; one call was refused for rate.</li>' % (
    c["answered"], 20, c["agree"])

t = open("template.html").read()
rep = {
    "{{N}}": f(N), "{{FIG1}}": fig1, "{{FIG2A}}": fig2a, "{{FIG2B}}": fig2b, "{{PREDS}}": preds,
    "{{C7358}}": f(B[4438]), "{{C7957}}": f(B[4797]), "{{C7958}}": f(B[4798]), "{{C3600}}": f(B[3600]),
    "{{MED}}": mmss(int(s["length_seconds"]["median"])), "{{O80}}": f(s["at_or_over_80_00"]), "{{O74}}": f(s["at_or_over_74_00"]),
    "{{PAST}}": f(e["leadout_past_99_59_74"]), "{{F150}}": f(e["first_offset_150"]), "{{F182}}": f(e["first_offset_top20"][1]["discs"]),
    "{{F183}}": f(e["first_offset_top20"][2]["discs"]), "{{F1S}}": f(e["first_offset_225_or_more"]), "{{TS}}": s["source"].split("TIMESTAMP ")[1][:16],
}
for k, v in rep.items():
    t = t.replace(k, v)
assert "{{FIG1" not in t
open("index.html", "w").write(t)
print("ok", len(t))

# session 2
s2 = json.load(open("session2.json"))
c2 = json.load(open("check2.json"))
e2 = json.load(open("explore2.json"))
FA = {int(k): v for k, v in s2["frames_330000_336000"].items()}
FB = {int(k): v for k, v in s2["frames_357000_361000"].items()}
mxf = FA[333000]
def fpanel(F, centre, label, lab):
    lo, hi = centre - 300, centre + 300
    H3, w3 = 200, (W - 2 * X0) / (hi - lo)
    out = []
    for i, x in enumerate(range(lo, hi)):
        v = F.get(x, 0)
        h = H3 * v / mxf
        sec = (x // 75) % 60; mn = x // 75 // 60; fr = x % 75
        out.append('<g><title>%d:%02d:%02d: %s discs</title><rect x="%.2f" y="%.1f" width="%.2f" height="%.1f" class="%s"/></g>' % (
            mn, sec, fr, f(v), X0 + i * w3, 10 + H3 - max(h, 0.6 if v else 0), w3 + 0.05, max(h, 0.6 if v else 0), "s0" if x == centre else "s1"))
        if fr == 0 and i > 0:
            out.append('<text x="%.1f" y="%d" class="yr" text-anchor="middle">%d:%02d</text>' % (X0 + i * w3, H3 + 30, mn, sec))
    out.append('<text x="%.1f" y="24" class="lb" text-anchor="end">%s</text>' % (X0 + 300 * w3 - 8, lab))
    return '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>' % (W, H3 + 40, label, "".join(out))
fig3a = fpanel(FA, 333000, "Discs by the address where their music ends, one column per frame, four seconds either side of 74:00:00",
               "74:00:00, %s discs" % f(FA[333000]))
fig3b = fpanel(FB, 360000, "The same, four seconds either side of 80:00:00, on the same scale",
               "80:00:00, %s discs" % f(FB.get(360000, 0)))
second = sorted((v for k, v in FA.items() if k != 333000), reverse=True)[0]
pct = lambda x: "%d %%" % round(100 * x)
order = ["frame 333,000 (74:00:00)", "frame 333,150 (74:02:00)", "rest of 74:00 second", "C70 (70:00-72:59)", "B80 (79:55-79:59)"]
names = {order[0]: "at exactly 74:00:00", order[1]: "at exactly 74:02:00 (74:00 of music after the gap)",
         order[2]: "elsewhere in the second 74:00", order[3]: "between 70:00 and 72:59", order[4]: "between 79:55 and 79:59"}
rows_ = "".join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%d</td></tr>' % (
    names[g], f(e2[g]["discs"]), pct(e2[g]["audiobook_share"]), pct(e2[g]["cd_r_share"]), e2[g]["median_year"]) for g in order)
P2 = s2["predictions"]; B2 = s2["bands"]
lab2 = {
    "P1 largest fall 4300-4899 is 4799->4800": "Between 71:40 and 81:40, the steepest fall from one second of address to the next is from 79:59 to 80:00: %s to %s." % (
        f(s2["largest_falls_4300_4899"][0]["counts"][0]), f(s2["largest_falls_4300_4899"][0]["counts"][1])),
    "P2 address fall 4799/4800 exceeds 498/167": "That fall is steeper in address than in playing time: %.2f against 2.98, about the same." % s2["fall_4799_4800_address"],
    "P3 commonest second 4380-4499 is 4440": "Between 73:00 and 74:59 the commonest second of address is 74:00 (%s discs)." % f(int(s2["address_seconds"]["4440"])),
    "P4 commonest frame 330000-336000 is 333000": "The commonest single frame near it is exactly 74:00:00: %s discs." % f(FA[333000]),
    "P5 B80 compilation share at least 1.5 x C76": "Discs filled to the 80 edge are more often compilations: %s, against %s between 76:00 and 78:59." % (
        pct(B2["B80"]["compilation_share"]), pct(B2["C76"]["compilation_share"])),
    "P6 A74 median year at least 3 earlier than B80": "The 74 edge is older: median year %d, against %d at the 80 edge." % (B2["A74"]["median_year"], B2["B80"]["median_year"]),
    "P7 CD at least 90 % of one-format discs in A74 and B80": "Pressed, not burnt: at the 74 edge %s of single-format discs are plain CD, at the 80 edge %s." % (
        pct(B2["A74"]["share_CD_of_one_format"]), pct(B2["B80"]["share_CD_of_one_format"])),
}
preds2 = "".join('<li><b>%s</b> %s</li>' % ("Held." if P2[k] else "Failed.", lab2[k]) for k in lab2)
preds2 += '<li><b>Failed.</b> The live database agrees on at least 19 of 20 drawn discs: %d answered and all %d agree; three calls were refused for rate (asked again by hand, outside the registration, they agree).</li>' % (
    c2["answered"], c2["agree"])
t = open("index.html").read()
for k, v in {"{{FIG3A}}": fig3a, "{{FIG3B}}": fig3b, "{{F333}}": f(FA[333000]), "{{F333N}}": f(second), "{{ROWS}}": rows_,
             "{{PREDS2}}": preds2, "{{ABS}}": pct(e2[order[0]]["audiobook_share"]), "{{ABC}}": pct(e2[order[3]]["audiobook_share"]),
             "{{AB80}}": pct(e2[order[4]]["audiobook_share"])}.items():
    t = t.replace(k, v)
assert "{{" not in t
open("index.html", "w").write(t)
print("ok2", len(t))
