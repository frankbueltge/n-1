"""Builds index.html (the project's page) from session1.json, explore1.json, explore1b.json, sample.json, session2.json, rows2.json and session3.json. Nothing is fetched at load."""
import json, html

s = json.load(open("session1.json")); e1 = json.load(open("explore1.json")); e = json.load(open("explore1b.json"))
sample = json.load(open("sample.json"))
s2 = json.load(open("session2.json"))
n = s["games"]
fmt = lambda x: f"{x:,}"

# chart 1: share of games still sharing every move with some other game, by ply
W, H, L, B = 760, 260, 44, 30
T = [t for t in s["together"] if t["ply"] <= 36]
bw = (W - L - 8) / len(T)
bars = []
for i, t in enumerate(T):
    f = t["still_shared"] / t["games_at_least_this_long"]
    h = f * (H - B - 10)
    x = L + i * bw
    bars.append(f'<rect x="{x+1:.1f}" y="{H-B-h:.1f}" width="{bw-2:.1f}" height="{h:.1f}" fill="var(--a)"><title>after ply {t["ply"]}: '
                f'{fmt(t["still_shared"])} of {fmt(t["games_at_least_this_long"])} games still share every move with another game</title></rect>')
    if t["ply"] % 5 == 0 or t["ply"] == 1:
        bars.append(f'<text x="{x+bw/2:.1f}" y="{H-B+16}" text-anchor="middle">{t["ply"]}</text>')
ax = "".join(f'<line x1="{L}" x2="{W-8}" y1="{H-B-v*(H-B-10):.1f}" y2="{H-B-v*(H-B-10):.1f}" stroke="var(--line)"/>'
             f'<text x="{L-6}" y="{H-B-v*(H-B-10)+4:.1f}" text-anchor="end">{int(v*100)} %</text>' for v in (0, .25, .5, .75, 1))
chart1 = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Share of games still sharing all their moves with another game, ply 1 to 36" '
          f'class="ch">{ax}{"".join(bars)}<text x="{(W+L)/2}" y="{H-2}" text-anchor="middle">ply (half-move)</text></svg>')

# chart 2: how many games become their own at each ply
hist = {int(k): v for k, v in s["departure_hist"].items()}
mx = max(hist.values()); P = range(1, 38)
bw = (W - L - 8) / len(P); b2 = []
for i, p in enumerate(P):
    v = hist.get(p, 0); h = v / mx * (H - B - 10); x = L + i * bw
    b2.append(f'<rect x="{x+1:.1f}" y="{H-B-h:.1f}" width="{bw-2:.1f}" height="{max(h,0):.1f}" fill="var(--c2)"><title>ply {p}: {fmt(v)} games</title></rect>')
    if p % 5 == 0 or p == 1:
        b2.append(f'<text x="{x+bw/2:.1f}" y="{H-B+16}" text-anchor="middle">{p}</text>')
ax2 = "".join(f'<line x1="{L}" x2="{W-8}" y1="{H-B-v/mx*(H-B-10):.1f}" y2="{H-B-v/mx*(H-B-10):.1f}" stroke="var(--line)"/>'
              f'<text x="{L-6}" y="{H-B-v/mx*(H-B-10)+4:.1f}" text-anchor="end">{fmt(v)}</text>' for v in (0, 5000, 10000, 15000))
chart2 = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Number of games whose own play begins at each ply" class="ch">{ax2}{"".join(b2)}'
          f'<text x="{(W+L)/2}" y="{H-2}" text-anchor="middle">the ply at which the game is no longer anyone else\'s</text></svg>')

def moves(seq):
    out = []
    for i, m in enumerate(seq):
        out.append((f"{i//2+1}. " if i % 2 == 0 else "") + m)
    return html.escape(" ".join(out))

seen, longest = set(), []
for x in sample:
    if x["why"] == "longest" and tuple(x["stem"]) not in seen:
        seen.add(tuple(x["stem"])); longest.append(x)
lrows = "".join(f'<tr><td>{x["stem_plies"]}</td><td>{html.escape(x["opening_tag"] or "")}</td><td>{"the same two accounts" if x["same_pair_as_partner"] else "two different pairs of accounts"}</td>'
                f'<td class="mv">{moves(x["stem"])}</td></tr>' for x in longest)
traps = [x for x in e["identical_top"] if x["plies"] >= 7]
trows = "".join(f'<tr><td>{x["games"]}</td><td>{x["plies"]}</td><td>{x["distinct_pairs"]}</td><td>{html.escape(x["opening_tag"] or "")}</td><td class="mv">{moves(x["moves"])}</td></tr>' for x in traps)
pr = "".join(f'<tr><td>{html.escape(k)}</td><td>{html.escape(json.dumps(v["value"]))}</td><td>{"held" if v["held"] else "<b>failed</b>"}</td></tr>' for k, v in s["predictions"].items())
bm = s["band_median_departure"]
held = sum(v["held"] for v in s["predictions"].values())

# the figure's labels: first-move blocks of at least 20 rows, at their middle; the ply axis
labels = "".join(f'<span class="{"b" if x["to"]-x["from"] >= 200 else ""}" style="top:{(x["from"]+x["to"]+1)/2/s2["rows"]*100:.2f}%">1.{html.escape(x["move"])} '
                 f'<br><small>{fmt(x["games"])}</small></span>' for x in s2["spans"] if x["to"] - x["from"] + 1 >= 20)
axis = "".join(f'<span style="left:{(p-0.5)/60*100:.2f}%">{p}</span>' for p in (1, 10, 20, 30, 40, 50, 60)) 
pr2 = "".join(f'<tr><td>{html.escape(k)}</td><td>{html.escape(json.dumps(v["value"]))}</td><td>{"held" if v["held"] else "<b>failed</b>"}</td></tr>' for k, v in s2["predictions"].items())
held2 = sum(v["held"] for v in s2["predictions"].values())
rows2 = json.load(open("rows2.json"))
s3 = json.load(open("session3.json"))
latest = max(r["median_departure"] for r in rows2)
page = open("template.html").read()
for k, v in {"N": fmt(n), "CHART1": chart1, "CHART2": chart2, "LROWS": lrows, "TROWS": trows, "PR": pr, "HELD": str(held),
             "NEVER": fmt(s["never_depart"]), "NEVERPCT": f'{100*s["never_depart"]/n:.1f}', "MED": str(s["median_departure_ply"]),
             "LONG": str(s["longest_stem"]), "LATER": f'{100*s["position_later_count"]/s["departing"]:.1f}',
             "B1": f'{bm["<1400"][0]:g}', "B2": f'{bm["1400-1799"][0]:g}', "B3": f'{bm[">=1800"][0]:g}',
             "AT10": fmt(s["together"][9]["still_shared"]), "AT20": fmt(s["together"][19]["still_shared"]), "AT30": fmt(s["together"][29]["still_shared"]),
             "IDG": fmt(e["identical_groups"]), "IDN": fmt(e["games_in_identical_groups"]), "ODD": fmt(e1["tokens_not_canonical"]),
             "PMED": f'{e["position_median_departure_ply"]:g}',
             "FIGLABELS": labels, "FIGAXIS": axis, "PR2": pr2, "HELD2": str(held2), "PLIES": fmt(s2["plies_total"]),
             "SHAREPCT": f'{100*s2["plies_shared"]/s2["plies_total"]:.1f}', "OWNPCT": f'{100-100*s2["plies_shared"]/s2["plies_total"]:.1f}',
             "LATEST": f'{latest:g}', "FEBN": fmt(s3["february_games"]),
             "FEBMED": f'{s3["predictions"]["P12 median horizon ply in [7,10]"]["value"]:g}',
             "FEBSTAY": f'{100*s3["february_stay"]/s3["february_games"]:.1f}',
             "FIGALT": f'The {fmt(n)} games of January 2013 as lines stacked in move order: a narrow blue band of shared moves at the left, '
                       f'mostly ending between half-move 5 and 12, and amber, each game alone, everywhere to its right.'}.items():
    page = page.replace("{{" + k + "}}", v)
assert "{{" not in page
open("index.html", "w").write(page)
print("ok", len(page))
