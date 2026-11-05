"""Project 22: build the study page index.html from session1.json, explore1.json, explore1b.json, check1.json (stdlib only).
Usage: python3 -I build.py   (run in projects/standing/)"""
import json, html

S = json.load(open('session1.json'))
E = json.load(open('explore1.json'))
B = json.load(open('explore1b.json'))
C = json.load(open('check1.json'))
S2 = json.load(open('session2.json'))
E2 = json.load(open('explore2.json'))
C2 = json.load(open('check2.json'))


def pct(x, d=0):
    return f'{100 * x:.{d}f}'


def n(x):
    return f'{x:,}'


# Figure 1: every year's species names, stacked by what became of them; axis capped at 10,000 (1891 broken and labelled)
YK = E['years_kinds']
W, H, L, T, BOT = 900, 360, 46, 20, 40
cap = 10000
y0, y1 = 1753, 2026
bw = (W - L - 10) / (y1 - y0 + 1)
ph = H - T - BOT
bars = []
for y in range(y0, y1 + 1):
    k = YK.get(str(y), {})
    st, mv, mg = k.get('standing', 0), k.get('moved', 0), k.get('merged', 0)
    ot = sum(v for kk, v in k.items() if kk not in ('standing', 'moved', 'merged'))
    tot = st + mv + mg + ot
    if not tot:
        continue
    x = L + (y - y0) * bw
    base = H - BOT
    parts = []
    scale = ph / cap
    for cls, v in (('st', st), ('mv', mv), ('mg', mg), ('ot', ot)):
        h = v * scale
        if base - h < T:
            h = base - T
        if h > 0:
            parts.append(f'<rect class="{cls}" x="{x:.1f}" y="{base - h:.1f}" width="{bw + 0.15:.2f}" height="{h:.1f}"/>')
        base -= h
    tip = f'{y}: {n(tot)} species names; {n(st)} stand, {n(mv)} moved, {n(mg)} merged, {n(ot)} void or other'
    bars.append(f'<g><title>{tip}</title>{"".join(parts)}</g>')
ax = []
for v in (2500, 5000, 7500, 10000):
    yy = H - BOT - v * ph / cap
    ax.append(f'<line class="ax" x1="{L}" x2="{W - 10}" y1="{yy:.1f}" y2="{yy:.1f}"/><text class="yr" x="{L - 6}" y="{yy + 5:.1f}" text-anchor="end">{v // 1000 if v % 1000 == 0 else v / 1000}k</text>')
for y in (1753, 1800, 1850, 1900, 1950, 2000):
    xx = L + (y - y0) * bw + bw / 2
    ax.append(f'<text class="yr" x="{xx:.1f}" y="{H - BOT + 22}" text-anchor="middle">{y}</text>')
x91 = L + (1891 - y0) * bw + bw / 2
k91 = sum(YK['1891'].values())
ax.append(f'<text class="yr" x="{x91 + 6:.1f}" y="{T + 12}">1891: {n(k91)} (bar cut at 10,000)</text>')
x96 = L + (1796 - y0) * bw + bw / 2
ax.append(f'<text class="yr" x="{x96:.1f}" y="{H - BOT - 2200 * ph / cap:.1f}" text-anchor="middle">1796</text>')
x53 = L + bw / 2
ax.append(f'<text class="yr" x="{x53 + 4:.1f}" y="{H - BOT - 6000 * ph / cap:.1f}">1753</text>')
fig1 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="f1t"><title id="f1t">Species names '
        f'published each year, 1753 to 2026, each bar split into the names that stand today, the names moved to another genus, the '
        f'names merged into a plant named before, and the names declared void</title>{"".join(ax)}{"".join(bars)}</svg></div>')

# Figure 2: decades, share standing and share moved among synonyms
D = E['decades_with_moved']
decs = sorted(int(d) for d in D)
W2, H2 = 900, 300
def px(d):
    return L + (d - 1750) / (2020 - 1750) * (W2 - L - 20)
def py(v):
    return H2 - BOT - v * (H2 - T - BOT)
p_st = ' '.join(f'{px(d):.1f},{py(D[str(d)]["share_standing"]):.1f}' for d in decs)
p_mv = ' '.join(f'{px(d):.1f},{py(D[str(d)]["moved_share_of_synonyms"]):.1f}' for d in decs)
ax2 = []
for v in (0, .25, .5, .75, 1):
    ax2.append(f'<line class="ax" x1="{L}" x2="{W2 - 20}" y1="{py(v):.1f}" y2="{py(v):.1f}"/><text class="yr" x="{L - 6}" y="{py(v) + 5:.1f}" text-anchor="end">{int(v * 100)}</text>')
for d in (1750, 1800, 1850, 1900, 1950, 2000):
    ax2.append(f'<text class="yr" x="{px(d):.1f}" y="{H2 - BOT + 22}" text-anchor="middle">{d}s</text>')
fig2 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W2} {H2}" role="img" aria-labelledby="f2t"><title id="f2t">By decade of '
        f'publication: the share of species names that stand today, and among the names made synonyms, the share that were moved '
        f'rather than merged</title>{"".join(ax2)}<polyline class="lst" points="{p_st}"/><polyline class="lmv" points="{p_mv}"/></svg></div>')

rows = ''.join(f'<tr><td>{d}s</td><td>{n(D[str(d)]["n"])}</td><td>{pct(D[str(d)]["share_standing"])}</td>'
               f'<td>{pct(D[str(d)]["moved_share_of_synonyms"])}</td></tr>' for d in decs)
table = ('<div class="sc"><table><thead><tr><th>decade</th><th>species names</th><th>stand today (%)</th>'
         f'<th>moved, of synonyms (%)</th></tr></thead><tbody>{rows}</tbody></table></div>')

# exploratory 1753-1799 moved share (pooled)
mv = mg = 0
for y in range(1753, 1800):
    k = YK.get(str(y), {})
    mv += k.get('moved', 0); mg += k.get('merged', 0)
m1753_99 = mv / (mv + mg)
mv = mg = 0
for y in range(1900, 2000):
    k = YK.get(str(y), {})
    mv += k.get('moved', 0); mg += k.get('merged', 0)
m1900 = mv / (mv + mg)

tmv = sum(k.get('moved', 0) for k in YK.values()); tmg = sum(k.get('merged', 0) for k in YK.values())
P = S['predictions']
PRED = [
    ('P1', 'The names file holds between 1,300,000 and 1,700,000 rows', f'{n(S["rows"])} rows; <b>seen before the count</b> (the README states the size), so reported as seen, not as held'),
    ('P2', 'At least 95 % of species names carry a year', f'{pct(S["share_with_year"], 2)} %'),
    ('P3', 'The share standing overall lies between 30 % and 45 %', f'{pct(S["share_standing_overall"], 1)} %'),
    ('P4', 'The highest decade is 2010-19 or 2020-26, at 75 % or more', f'2020s, {pct(D["2020"]["share_standing"], 1)} %'),
    ('P5', 'The lowest decade (1,000 names or more) lies in 1800-1899', f'the 1790s, {pct(D["1790"]["share_standing"], 1)} %'),
    ('P6', 'Merged outnumber moved among synonyms', 'the flag is coded <code>T</code>, not <code>TRUE</code> as registered (exploratory, names with a year: merged ' + n(tmg) + ', moved ' + n(tmv) + ')'),
    ('P7', 'Moved share higher for 1753-1799 than for 1900-1999', f'as P6 (exploratory: {pct(m1753_99)} % against {pct(m1900)} %)'),
    ('P8', 'At least 35 % of standing names have a basionym', f'{pct(S["share_standing_with_basionym"], 1)} %'),
    ('P9', 'The median wait is at least 50 years', f'{S["wait_median"]:.0f} years'),
    ('P10', 'Unplaced names are at most 5 % of species names', f'{pct(S["kinds_all_species"]["unjudged"] / S["species_names"], 1)} %'),
    ('P11', 'Plants of the World Online agrees on 10 of 12', 'the site answered with a bot challenge, not circumvented (exploratory substitute: Kew\'s copy on GBIF, 11 of 12)'),
]
def verdict(k):
    if k in ('P6', 'P7'):
        return 'not testable'
    if k == 'P11':
        return 'not run'
    if k == 'P1':
        return 'seen'
    return 'held' if P[k] else 'failed'
plist = ''.join(f'<li><b>{k}</b> {html.escape(t)} — {verdict(k)}: {r}</li>' for k, t, r in PRED)

# Session 2: figure 3, per decade, share of v10's standing names undone by v16, and of v10's undone names standing by v16
D2 = E2['decades']
decs2 = sorted(int(d) for d in D2)
W3, H3, top3 = 900, 300, 0.06
def py3(v):
    return H3 - BOT - v / top3 * (H3 - T - BOT)
p_lost = ' '.join(f'{px(d):.1f},{py3(D2[str(d)]["lost_share"]):.1f}' for d in decs2)
p_rais = ' '.join(f'{px(d):.1f},{py3(D2[str(d)]["raised_share"]):.1f}' for d in decs2)
ax3 = []
for v in (0, .02, .04, .06):
    ax3.append(f'<line class="ax" x1="{L}" x2="{W3 - 20}" y1="{py3(v):.1f}" y2="{py3(v):.1f}"/><text class="yr" x="{L - 6}" y="{py3(v) + 5:.1f}" text-anchor="end">{int(v * 100)}</text>')
for d in (1750, 1800, 1850, 1900, 1950, 2000):
    ax3.append(f'<text class="yr" x="{px(d):.1f}" y="{H3 - BOT + 22}" text-anchor="middle">{d}s</text>')
dots3 = ''.join(f'<g><title>{d}s: of {n(D2[str(d)]["standing_v10"])} names standing in December 2022, {n(D2[str(d)]["lost"])} no longer stand in June 2026 ({pct(D2[str(d)]["lost_share"], 1)} %); of {n(D2[str(d)]["undone_v10"])} undone, {n(D2[str(d)]["raised"])} now stand ({pct(D2[str(d)]["raised_share"], 1)} %)</title><circle class="dl" cx="{px(d):.1f}" cy="{py3(D2[str(d)]["lost_share"]):.1f}" r="4"/><circle class="dr" cx="{px(d):.1f}" cy="{py3(D2[str(d)]["raised_share"]):.1f}" r="4"/></g>' for d in decs2)
fig3 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W3} {H3}" role="img" aria-labelledby="f3t"><title id="f3t">By decade of '
        f'publication: the share of names standing in December 2022 that no longer stood in June 2026, and the share of names undone in '
        f'December 2022 that stood in June 2026</title>{"".join(ax3)}<polyline class="llo" points="{p_lost}"/><polyline class="lra" points="{p_rais}"/>{dots3}</svg></div>')
REL = {'v10': 'Dec 2022', 'v11': 'Oct 2023', 'v12': 'Oct 2023', 'v13': 'May 2025', 'v14': 'Jul 2025', 'v15': 'Jan 2026', 'v16': 'Jun 2026'}
steprows = ''.join(f'<tr><td>{k.split("-")[0]} → {k.split("-")[1]}</td><td>{REL[k.split("-")[0]]} → {REL[k.split("-")[1]]}</td><td>{n(v["changed"])}</td></tr>' for k, v in S2['steps'].items())
steptable = f'<div class="sc"><table><thead><tr><th>releases</th><th>dates</th><th>species names that changed</th></tr></thead><tbody>{steprows}</tbody></table></div>'
LBL = {'standing': 'stood', 'moved': 'moved', 'merged': 'merged', 'void': 'void', 'unjudged': 'unplaced'}
flowrows = ''.join(f'<tr><td style="text-align:left">{LBL.get(x, x)} → {LBL.get(y, y)}</td><td>{n(m)}</td></tr>' for x, y, m in S2['flow_kinds'][:12])
flowtable = f'<div class="sc"><table><thead><tr><th style="text-align:left">December 2022 → June 2026</th><th>species names</th></tr></thead><tbody>{flowrows}</tbody></table></div>'
SA = {(a, b, c): m for a, b, c, m in E2['v10_v16_changes_by_accepted_link']}
mm_same = SA[('merged', 'moved', 'same accepted')]
same_all = sum(m for (a, b, c), m in SA.items() if c == 'same accepted')
P2 = S2['predictions']
lo20, lo18 = S2['lost_share_2000_2022'], S2['lost_share_1800_1899']
PRED2 = [
    ('P1', 'At least 98 % of the 2022 species names are still there in 2026, by id', f'{pct(S2["share_v10_present_in_v16"], 2)} %'),
    ('P2', 'Between 1 % and 5 % changed kind', f'{pct(S2["share_changed"], 2)} % ({n(S2["changed"])} of {n(S2["present_in_both"])})'),
    ('P3', 'More names lost their standing than gained it', f'{n(S2["standing_out"])} lost, {n(S2["standing_in"])} gained'),
    ('P4', 'Names of 2000-2022 lost standing more often than names of the 1800s', f'{pct(lo20[0], 1)} % against {pct(lo18[0], 1)} %'),
    ('P5', 'Of names sunk to synonyms, more were moved than merged', f'{n(S2["standing_to_synonym"]["moved"])} moved, {n(S2["standing_to_synonym"]["merged"])} merged'),
    ('P6', 'At least 10 % of the 2022 unplaced names got a verdict', f'{pct(S2["unjudged_judged_v16"] / S2["unjudged_v10_in_both"], 1)} %'),
    ('P7', 'The share standing moved by less than one point', f'{pct(S2["share_standing_v10"][0], 2)} % to {pct(S2["share_standing_v16"][0], 2)} %'),
    ('P8', 'No single publication holds 5 % of the changes', f'<i>{html.escape(S2["top_publication"][0])}</i>, {n(S2["top_publication"][1])} ({pct(S2["top_publication"][1] / S2["changed"], 1)} %)'),
    ('P9', 'The busiest step is v12 → v13, the longest interval', f'it is v10 → v11 ({n(S2["steps"]["v10-v11"]["changed"])} changes)'),
    ('P10', 'At least 5,000 names of 2022 or earlier were added after 2022', f'{n(S2["added_v16_year_le_2022"])}'),
    ('P11', 'Fewer than 0.1 % of names reversed a verdict within the seven releases', f'{n(S2["reversals"])} of {n(S2["present_all_seven"])} ({pct(S2["reversals"] / S2["present_all_seven"], 3)} %)'),
]
plist2 = ''.join(f'<li><b>{k}</b> {html.escape(t)} — {"held" if P2[k] else "failed"}: {r}</li>' for k, t, r in PRED2)
c2 = C2['rows']
y53 = E['year_1753']; bk = E['revis_gen_pl_1891']; b96 = B['top'][0]
nb = E['decades_without_that_book']['1890']
q = S['wait_quartiles']

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Standing</title><link rel="icon" href="data:,">
<meta name="description" content="Every species name of a vascular plant published since 1753, and what became of it: stands, moved, merged or void.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a64;--line:#d9d6cc;--panel:#f1efe8;--a:#3b5f86;--st:#4f7a3a;--mv:#3b5f86;--mg:#b9654a;--ot:#a9a69b}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--panel:#22221f;--a:#7fa9d6;--st:#93bf6f;--mv:#7fa9d6;--mg:#e0916e;--ot:#6b6a64}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--panel:#22221f;--a:#7fa9d6;--st:#93bf6f;--mv:#7fa9d6;--mg:#e0916e;--ot:#6b6a64}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}
main{{max-width:1000px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:2rem;margin:.2em 0}}h2{{font-size:1.2rem;margin-top:2.2em}}
.mut{{color:var(--mut)}}.sm{{font:13px/1.45 system-ui,sans-serif}}a{{color:var(--a)}}.big{{font-size:1.25rem}}
svg.ch{{width:100%;height:auto;display:block;margin:1em 0}}svg.ch .st{{fill:var(--st)}}svg.ch .mv{{fill:var(--mv)}}svg.ch .mg{{fill:var(--mg)}}svg.ch .ot{{fill:var(--ot)}}
svg.ch polyline{{fill:none;stroke-width:2.5}}svg.ch .lst{{stroke:var(--st)}}svg.ch .lmv{{stroke:var(--mv)}}
svg.ch .llo{{stroke:var(--mg)}}svg.ch .lra{{stroke:var(--st)}}svg.ch .dl{{fill:var(--mg)}}svg.ch .dr{{fill:var(--st)}}
svg.ch .ax{{stroke:var(--line)}}svg.ch .yr{{font:15px system-ui,sans-serif;fill:var(--mut)}}
.key span{{display:inline-block;width:.9em;height:.9em;margin:0 .3em 0 .9em;vertical-align:-.1em}}
.sc{{overflow-x:auto}}.sc svg.ch{{min-width:600px}}ul.pr{{font:14px/1.5 system-ui,sans-serif;padding-left:1.2em}}
table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
.conn{{font:13px/1.45 system-ui,sans-serif;color:var(--mut)}}
</style></head><body><main>
<p class="sm mut">Project 22, sessions 1-2 · 4-5 November 2026 · open; no work before session 3 · data: Royal Botanic Gardens, Kew, World Checklist of Vascular Plants (CC BY)</p>
<h1>Standing</h1>
<p class="big">Every plant has a name, and many have had several. Of the <b>{n(S["species_with_year"])}</b> species names
of vascular plants published since 1753, <b>{pct(S["share_standing_overall"])} %</b> stand today as the name of a plant. The rest were
undone by a later statement — and the plant did not change.</p>
{fig1}
<p class="sm key"><span style="background:var(--st)"></span>stands today <span style="background:var(--mv)"></span>moved (same plant,
another genus) <span style="background:var(--mg)"></span>merged (a plant already named) <span style="background:var(--ot)"></span>void
or other · species names published each year, 1753-2026 (hover a bar for its year)</p>
<p class="sm mut">Sections can be read in any order; each says which others it connects to.</p>

<h2 id="s1">1. A name, and a verdict on it</h2>
<p>A species name is made once, in print, in a year: a genus and an epithet, <i>Rosa canina</i>. Botanical names count from 1753. Later
botanists may decide that the plant belongs in another genus — the epithet is carried over and the old name becomes a <i>synonym</i>,
"moved" here — or that it is the same plant as one named earlier, and the later name is sunk into the older one, "merged" here. Some names
are void under the rules of naming. Kew's World Checklist of Vascular Plants records, for every published name, the verdict of the field
as Kew reads it: {n(S["rows"])} names, {n(S["species_names"])} of them of species. This study reads them by the year each name was made.</p>
<p class="conn">Connects to 2 (how much stands) and 4 (in what form).</p>

<h2 id="s2">2. How much of each year stands</h2>
<p>The share standing climbs from under one in five for the names of the late eighteenth and early nineteenth centuries to
<b>{pct(D["2020"]["share_standing"])} %</b> for the names of the 2020s. The lowest decade is the 1790s
(<b>{pct(D["1790"]["share_standing"])} %</b>). The year 1753 itself is an exception: <b>{pct(y53["share_standing"])} %</b> of its
{n(y53["n"])} species names stand. The recent names stand partly because they are good and partly because no one has yet looked again:
the right end of the curve is untested, not proven.</p>
{table}
<p class="conn">Connects to 3 (two books) and 6 (what this cannot tell).</p>

<h2 id="s3">3. Two books the field refused</h2>
<p>The two deepest years are each one publication. In 1891, <i>Revis. Gen. Pl.</i> made <b>{n(bk["n"])}</b> species names, most of them
new combinations under older genus names; <b>{n(bk["standing"])}</b> stand ({pct(bk["share_standing"], 1)} %). Without it, the 1890s stand
at {pct(nb["share_standing"])} % instead of {pct(D["1890"]["share_standing"])} %. In 1796, <i>{html.escape(b96[0])}</i> made
<b>{n(b96[1])}</b>; <b>{b96[2]["Accepted"]}</b> stand and {n(b96[2]["Illegitimate"])} are declared illegitimate. The tall bar of 1891 in
the figure is almost entirely blue and red. (Exploratory: found after the registered count.)</p>
<p class="conn">Connects to 2, and to 4: the 1891 names were mostly moved, not merged.</p>

<h2 id="s4">4. Moved or merged</h2>
<p>A name that was moved is not wholly gone: its epithet lives on inside another name. A name that was merged is. Of the undone names of
1753, <b>{pct(y53["moved_share_of_synonyms"])} %</b> were moved. Through the nineteenth century the share falls to about a third: those
names fell mostly by being found to be plants already named. Then it rises again, to <b>{pct(D["2020"]["moved_share_of_synonyms"])} %</b>
for the undone names of the 2020s. The names of the long middle, from the 1760s to the 1940s, were undone mostly by doubling; those of 1753 and of recent decades mostly by regrouping. (Exploratory: the registered count
expected the flag spelled <code>TRUE</code>, and it is spelled <code>T</code>; see 7.)</p>
{fig2}
<p class="sm key"><span style="background:var(--st)"></span>share of the decade's species names that stand today
<span style="background:var(--mv)"></span>share moved, among the decade's names made synonyms · in %</p>
<p class="conn">Connects to 5 (the epithet that waits).</p>

<h2 id="s5">5. The epithet that waits</h2>
<p>Of the {n(S["standing_n"])} standing species names, <b>{pct(S["share_standing_with_basionym"])} %</b> stand on an epithet first
published under another name — moved names, returning. For those, the standing name came a median <b>{S["wait_median"]:.0f} years</b>
after the epithet (half between {q[0]:.0f} and {q[2]:.0f} years).</p>
<p class="conn">Connects to 4.</p>

<h2 id="s6">6. What this cannot tell</h2>
<p>Whether the verdicts are right. A name "stands" here in Kew's view on 4 June 2026; other checklists disagree, and some of today's
standing names will fall. Why a name fell: the argument is in a monograph, not in a column. Anything about the plants themselves. The
registered check against Kew's public website could not run (the site answered with a bot challenge, which was not circumvented); against
Kew's own copy of the checklist on GBIF, {C["agree"]} of {C["n"]} sampled names carry the same verdict (the twelfth, illegitimate here,
is a synonym there, whose scheme has no class for it). Nearest neighbours: <a href="NEIGHBOURS.md">NEIGHBOURS.md</a>.</p>
<p class="conn">Connects to 2 and 3.</p>

<h2 id="s7">7. Predictions, registered before the count</h2>
<p class="sm">Pushed with the selection (<a href="SELECTION.md">SELECTION.md</a>) before any row was read; the count was run once
(<a href="count1.py">count1.py</a>, <a href="session1.json">session1.json</a>).</p>
<ul class="pr">{plist}</ul>
<h2 id="s8">8. Three and a half years of verdicts</h2>
<p>Kew keeps its earlier releases. Seven of them, from December 2022 to June 2026, hold the same {n(S2["present_in_both"])} species
names under the same ids, and <b>{n(S2["changed"])}</b> of them ({pct(S2["share_changed"], 1)} %) carry a different verdict at the end than
at the start. <b>{n(S2["standing_out"])}</b> names stopped standing and <b>{n(S2["standing_in"])}</b> began to; the share standing still
rose a little ({pct(S2["share_standing_v10"][0], 1)} % to {pct(S2["share_standing_v16"][0], 1)} %), because new names arrive standing.
Not one plant changed.</p>
{fig3}
<p class="sm key"><span style="background:var(--mg)"></span>of the names standing in December 2022, the share no longer standing in June
2026 <span style="background:var(--st)"></span>of the names undone in December 2022, the share standing in June 2026 · in %, by decade
of publication (hover a point)</p>
<p>The verdict moves on old names and new ones alike, but not equally: about one standing name in seventy from the eighteenth century
was undone in these three and a half years, one in twenty-five of the 2020s. The newest names are where the field is still deciding — in
both directions: {pct(D2["2020"]["raised_share"], 1)} % of the 2020s' undone names stand again.</p>
{flowtable}
<p>The largest single flow is not a verdict on a plant. Of the {n(S2["flow_kinds"][0][2])} names that went from merged to moved,
<b>{n(mm_same)}</b> point to the same accepted name before and after: the synonym was not re-placed, it was re-described — the record
now says the name shares its type with the accepted one, where before it said nothing. In all, at least {n(same_all)} of the
{n(S2["changed"])} changes (34 % or more; the exploratory file keeps the thirty largest classes, which hold all but 58) keep the same accepted name; the record corrected its own grammar.
The merged → moved flow was heaviest in the first step: {n(S2["steps"]["v10-v11"]["flows_top"][0][2])} of that step's
{n(S2["steps"]["v10-v11"]["changed"])} changes. (Exploratory: found after the registered count, <a href="explore2.json">explore2.json</a>.)</p>
{steptable}
<p class="sm">Eleven predictions were registered before any of the archived releases was opened
(<a href="SESSION2.md">SESSION2.md</a>); the count ran once (<a href="count2.py">count2.py</a>, <a href="session2.json">session2.json</a>).</p>
<ul class="pr">{plist2}</ul>
<p class="sm">Check (information, not a pass mark): twelve changed names looked up in Kew's copy on GBIF
(<a href="check2.json">check2.json</a>). Four are informative — their two releases differ in a status GBIF can show — and all four show
the 2026 verdict there; the other eight differ only in the moved/merged flag or in a void class GBIF's scheme does not carry.</p>
<p class="conn">Connects to 2 (the untested right end, now tested a little) and 4 (moved or merged: part of that split is the record's
own late spelling).</p>

<p class="sm mut">Data: Royal Botanic Gardens, Kew. World Checklist of Vascular Plants, versions 10-16 (8 December 2022 to 4 June 2026),
<code>https://sftp.kew.org/pub/data-repositories/WCVP/</code>; Govaerts, R., Nic Lughadha, E., Black, N., Turner, R., Paton, A. (2021),
<i>Scientific Data</i> 8:215, <code>https://doi.org/10.1038/s41597-021-00997-6</code>. Licence: CC BY 4.0 (the paper), CC BY 3.0 (the
download's README). Counts and figures derived by Remainder; no author is ranked.</p>
</main></body></html>
'''
open('index.html', 'w').write(page)
print('ok', len(page))
