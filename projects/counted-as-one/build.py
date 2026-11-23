"""Project 26: build the study page index.html from session1.json, session1-per.json.gz, check1.json, explore1.json.
Stdlib only. Usage: python3 -I build.py   (run in projects/counted-as-one/)"""
import gzip, html, json, math
S = json.load(open('session1.json'))
P = json.load(gzip.open('session1-per.json.gz', 'rt'))
C = json.load(open('check1.json'))
E = json.load(open('explore1.json'))
E2 = json.load(open('explore1b.json'))
S2 = json.load(open('session2.json'))
C2 = json.load(open('check2.json'))
X2 = json.load(open('explore2.json'))
D2 = json.load(open('explore2b.json'))
P2 = json.load(gzip.open('session2-per.json.gz', 'rt'))
n = lambda x: f'{x:,.0f}'
pr = S['predictions']

# figure: every overflow with at least one counted spill, hours (log x) against counted spills (log y), binned
W, H, L, R, T, B = 960, 470, 64, 20, 20, 52
x0, x1 = -2, 4          # 0.01 h .. 10,000 h
y0, y1 = 0, math.log10(400)
sx = lambda h: L + (math.log10(h) - x0) / (x1 - x0) * (W - L - R)
sy = lambda c: T + (1 - (math.log10(c) - y0) / (y1 - y0)) * (H - T - B)
NX, NY = 72, 44
bins = {}
for r in P:
    if r['count'] < 1:
        continue
    h = min(max(r['hours'], 10 ** x0), 10 ** x1 * 0.999)
    i = int((math.log10(h) - x0) / (x1 - x0) * NX)
    j = int((math.log10(r['count']) - y0) / (y1 - y0) * NY)
    j = min(j, NY - 1)
    b = bins.setdefault((i, j), [0, 0])
    b[0] += 1
    b[1 if r['count'] >= 30 else 0] += 0
els = []
for v, lab in ((0.01, '36 s'), (0.1, '6 min'), (1, '1 h'), (10, '10 h'), (100, '100 h'), (1000, '1,000 h'), (10000, '10,000 h')):
    els.append(f'<line class="ax" x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{T}" y2="{H - B}"/>'
               f'<text class="yr" x="{sx(v):.1f}" y="{H - B + 18}" text-anchor="{"end" if v == 10000 else "start" if v == 0.01 else "middle"}">{lab}</text>')
for c in (1, 3, 10, 30, 100, 300):
    els.append(f'<line class="ax" x1="{L}" x2="{W - R}" y1="{sy(c):.1f}" y2="{sy(c):.1f}"/>'
               f'<text class="yr" x="{L - 7}" y="{sy(c) + 4:.1f}" text-anchor="end">{c}</text>')
cw = (W - L - R) / NX
ch = (H - T - B) / NY
mx = max(b[0] for b in bins.values())
for (i, j), (cnt, _) in sorted(bins.items()):
    op = 0.18 + 0.82 * math.log(cnt + 1) / math.log(mx + 1)
    hx, hy = L + i * cw, T + (NY - 1 - j) * ch
    lo_h = 10 ** (x0 + i * (x1 - x0) / NX); hi_h = 10 ** (x0 + (i + 1) * (x1 - x0) / NX)
    lo_c = 10 ** (y0 + j * (y1 - y0) / NY); hi_c = 10 ** (y0 + (j + 1) * (y1 - y0) / NY)
    els.append(f'<rect class="bn" x="{hx:.1f}" y="{hy:.1f}" width="{cw + .3:.1f}" height="{ch + .3:.1f}" fill-opacity="{op:.2f}">'
               f'<title>{cnt} overflow{"s" if cnt > 1 else ""}: {lo_h:.3g}–{hi_h:.3g} hours, counted {lo_c:.3g}–{hi_c:.3g}</title></rect>')
els.append(f'<line class="tg" x1="{L}" x2="{W - R}" y1="{sy(30):.1f}" y2="{sy(30):.1f}"/>'
           f'<text class="tl" x="{L + 6}" y="{sy(30) - 6:.1f}" text-anchor="start">30 counted spills: the one-year trigger for an investigation</text>')
lo, hi, lg = E['fewest_hours_over_trigger'], E['most_hours_under_trigger'], E['longest_sequence_overflow']
for r, anchor, dx, lab in ((lo, 'start', 10, f'{lo["uid"]}: 1 h 16 min, counted {lo["count"]}'),
                           (hi, 'end', -10, f'{hi["uid"]}: {hi["hours"]:,.0f} h, counted {hi["count"]}'),
                           (lg, 'end', -10, f'{lg["uid"]}: {lg["hours"]:,.0f} h in {lg["acts"]} activations, counted {lg["count"]}')):
    cx, cy = sx(r['hours']), sy(r['count'])
    els.append(f'<circle class="mk" cx="{cx:.1f}" cy="{cy:.1f}" r="6"/>'
               f'<text class="ml" x="{cx + dx:.1f}" y="{cy + 4:.1f}" text-anchor="{anchor}">{lab}</text>')
els.append(f'<text class="yr" x="{(L + W - R) / 2:.0f}" y="{H - 10}" text-anchor="middle">hours of discharge recorded in 2025 (log scale)</text>'
           f'<text class="yr" x="14" y="{(T + H - B) / 2:.0f}" transform="rotate(-90 14 {(T + H - B) / 2:.0f})" text-anchor="middle">counted spills (log scale)</text>')
nfig = sum(1 for r in P if r['count'] >= 1)
fig = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ft"><title id="ft">A density plot of '
       f'{n(nfig)} storm overflows: hours of discharge in 2025 across, counted spills up. The cloud rises with the hours but is wide: at '
       f'the trigger line of 30 counted spills it spans from about one hour to several hundred. Three overflows are marked: one with 1 h 16 '
       f'min counted 44, one with 567 hours counted 27, and one with 5,446 hours counted 235.</title>' + ''.join(els) + '</svg></div>')

qh = S['spill_hours_quantiles']
lt1, ge12, nsp = S['spills_lt_1h'], S['spills_ge_12h'], S['counted_spills']
rows = [
    ('1', 'median hours per counted spill (per overflow) between 2 and 6', f'{pr["P1"]["value"]:.2f} h', pr['P1']['held']),
    ('2', 'more than 25 % of counted spills hold under an hour', f'{100 * pr["P2"]["value"]:.1f} %', pr['P2']['held']),
    ('3', 'fewer than 10 % of counted spills hold 12 hours or more', f'{100 * pr["P3"]["value"]:.1f} %', pr['P3']['held']),
    ('4', 'activations ÷ counted spills greater than 2', f'{pr["P4"]["value"]:.2f}', pr['P4']['held']),
    ('5', 'count below activations for over 70 % of overflows with 2+ activations', f'{100 * pr["P5"]["value"]:.1f} %', pr['P5']['held']),
    ('6', 'recount equals the returned count for over 80 % of overflows', f'{100 * pr["P6"]["value"]:.1f} %', pr['P6']['held']),
    ('7', 'the top 10 % of overflows by hours hold over half the hours', f'{100 * pr["P7"]["value"]:.1f} %', pr['P7']['held']),
    ('8', 'the longest counting sequence spans more than 30 days', f'{pr["P8"]["value"]:.1f} days', pr['P8']['held']),
    ('9', 'fewer than 1 % of start/stop rows malformed', f'{100 * pr["P9"]["value"]:.1f} % (blank rows; 0.016 % of non-blank)', pr['P9']['held']),
    ('10', 'hours per count lower for counts 1–10 than for counts over 60', f'{pr["P10"]["value"][0]:.2f} h and {pr["P10"]["value"][1]:.2f} h', pr['P10']['held']),
]
tab = ''.join(f'<tr><td>P{p}</td><td style="text-align:left">{html.escape(q)}</td><td>{html.escape(v)}</td><td>{"held" if h else "<b>failed</b>"}</td></tr>'
              for p, q, v, h in rows)
held = sum(1 for r in rows if r[3])

# session 2 figure: hours per day of 2025, three rows, each scaled to its own peak, bathing season shaded
W2, RH, G2, L2 = 960, 92, 30, 196
days = 365
bw = (W2 - L2 - 10) / days
els2 = [f'<rect class="ss" x="{L2 + 134 * bw:.1f}" y="0" width="{139 * bw:.1f}" height="{3 * (RH + G2):.0f}"/>',
        f'<text class="tl2" x="{L2 + 203.5 * bw:.1f}" y="14" text-anchor="middle">bathing season, 15 May – 30 September</text>']
labels = (('all', f'all {n(S2["overflows"])} overflows'), ('bathing', f'{n(S2["all_bathing"])} bathing-named'),
          ('U', f'{S2["U"]} long, under the trigger'))
for i, (g, lab) in enumerate(labels):
    y0r = 24 + i * (RH + G2)
    v = D2[g]; mxv = max(v)
    sh = sum(v[134:273]) / sum(v)
    els2.append(f'<text class="yr" x="{L2 - 8}" y="{y0r + RH / 2:.0f}" text-anchor="end">{html.escape(lab)}</text>'
                f'<text class="yr" x="{L2 - 8}" y="{y0r + RH / 2 + 16:.0f}" text-anchor="end">{100 * sh:.1f} % of hours in season</text>')
    for d, x in enumerate(v):
        if x <= 0:
            continue
        hh = RH * x / mxv
        els2.append(f'<rect class="db" x="{L2 + d * bw:.2f}" y="{y0r + RH - hh:.1f}" width="{bw + .15:.2f}" height="{hh:.1f}"/>')
    els2.append(f'<line class="ax" x1="{L2}" x2="{W2 - 10}" y1="{y0r + RH}" y2="{y0r + RH}"/>')
for m, d in (('Jan', 0), ('Apr', 90), ('Jul', 181), ('Oct', 273), ('Dec', 334)):
    els2.append(f'<text class="yr" x="{L2 + d * bw:.1f}" y="{3 * (RH + G2) + 10:.0f}">{m}</text>')
fig2 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W2} {3 * (RH + G2) + 16}" role="img" aria-labelledby="ft2"><title id="ft2">Hours of '
        f'discharge on each day of 2025, in three rows: all overflows, those with a bathing water named, and the {S2["U"]} long-discharging '
        f'overflows under the trigger. The bathing season from 15 May to 30 September is shaded; in every row the bars there are low, and '
        f'in the last row almost absent.</title>' + ''.join(els2) + '</svg></div>')
ub = [r for r in P2 if r['count'] < 30 and r['hours'] > S2['median_hours_O'] and r['bathing']]
ub.sort(key=lambda r: -r['hours'])
tab2 = ''.join(f'<tr><td style="text-align:left">{html.escape(r["uid"])}</td><td style="text-align:left">{html.escape(r["bathing"])}</td>'
               f'<td>{r["hours"]:,.0f}</td><td>{r["count"]}</td><td>{r["season_h"]:,.1f}</td></tr>' for r in ub)
pr2 = S2['predictions']
rows2 = [
    ('1', 'over 10 % of the long under-trigger overflows have a bathing water named', f'{100 * pr2["P1"]["value"]:.1f} %', pr2['P1']['held']),
    ('2', 'bathing or shellfish water named more often among them than over the trigger', f'{100 * pr2["P2"]["value"][0]:.1f} % against {100 * pr2["P2"]["value"][1]:.1f} %', pr2['P2']['held']),
    ('3', 'their median monitor operation 95 % or more', f'{pr2["P3"]["value"]:.2f} %', pr2['P3']['held']),
    ('4', 'over 5 % of all monitors operated under 90 % of the year', f'{100 * pr2["P4"]["value"]:.1f} %', pr2['P4']['held']),
    ('5', 'monitors under 50 % operation have a lower median count than those at 90 %+', f'{pr2["P5"]["value"][0]:.0f} against {pr2["P5"]["value"][1]:.0f}', pr2['P5']['held']),
    ('6', 'of recounts differing from the returned count, over half differ by one', f'{100 * pr2["P6"]["value"]:.1f} %', pr2['P6']['held']),
    ('7', 'one of three rule variants matches the returned count more often than the rule as read', f'best variant {max(pr2["P7"]["value"][k] for k in ("v1","v2","v3")):,} against {pr2["P7"]["value"]["v0"]:,}', pr2['P7']['held']),
    ('8', 'no variant matches over 95 % of overflows', f'{100 * max(pr2["P8"]["value"].values()):.1f} % at most', pr2['P8']['held']),
    ('9', 'over 30 % of the bathing-named overflows’ hours fall in the bathing season', f'{100 * pr2["P9"]["value"]:.1f} %', pr2['P9']['held']),
]
tab3 = ''.join(f'<tr><td>P{p}</td><td style="text-align:left">{html.escape(q)}</td><td>{html.escape(v)}</td><td>{"held" if h else "<b>failed</b>"}</td></tr>'
               for p, q, v, h in rows2)
held2 = sum(1 for r in rows2 if r[3])
ye = X2['year_edge_by_difference']

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Counted as One</title><link rel="icon" href="data:,">
<meta name="description" content="Every storm-overflow discharge England's monitors recorded in 2025, and what the 12/24 counting rule makes of it.">
<style>
:root{{--bg:#f7f8f6;--fg:#1b1e1d;--mut:#62686a;--line:#d5dad8;--a:#2f6070;--b:#1f4d5c;--t:#b0452b}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121515;--fg:#e8ecea;--mut:#9aa3a3;--line:#323a3a;--a:#7fb8c8;--b:#9fd3e0;--t:#ff7a5c}}}}
:root[data-theme="dark"]{{--bg:#121515;--fg:#e8ecea;--mut:#9aa3a3;--line:#323a3a;--a:#7fb8c8;--b:#9fd3e0;--t:#ff7a5c}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}
main{{max-width:1000px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:2rem;margin:.2em 0}}h2{{font-size:1.2rem;margin-top:2.2em}}
.mut{{color:var(--mut)}}.sm{{font:13px/1.45 system-ui,sans-serif}}a{{color:var(--a)}}.big{{font-size:1.25rem}}
svg.ch{{width:100%;height:auto;display:block;margin:1em 0}}svg.ch .ax{{stroke:var(--line)}}svg.ch .yr{{font:12px system-ui,sans-serif;fill:var(--mut)}}
svg.ch rect.bn{{fill:var(--b)}}svg.ch .tg{{stroke:var(--t);stroke-width:2;stroke-dasharray:6 4}}svg.ch .tl{{font:600 12px system-ui,sans-serif;fill:var(--t)}}
svg.ch rect.ss{{fill:var(--t);fill-opacity:.09}}svg.ch rect.db{{fill:var(--b)}}svg.ch .tl2{{font:600 12px system-ui,sans-serif;fill:var(--t)}}
svg.ch .mk{{fill:none;stroke:var(--fg);stroke-width:2}}svg.ch .ml{{font:600 12px system-ui,sans-serif;fill:var(--fg)}}
.sc{{overflow-x:auto}}.sc svg.ch{{min-width:680px}}.tw{{overflow-x:auto}}
table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
blockquote{{margin:1em 0;padding-left:14px;border-left:3px solid var(--line)}}
</style></head><body><main>
<p class="sm mut">Project 26, sessions 1–2 · 21 and 23 November 2026 · open; no work before session 3 · data: Environment Agency, Event Duration
Monitoring storm-overflow start/stop data 2025 and the 2025 annual return, “© Environment Agency copyright and/or database right 2026. All
rights reserved.”, Open Government Licence per the data.gov.uk catalogue · this page CC BY 4.0 · Remainder</p>
<h1>Counted as One</h1>
<p class="big">When a sewer in England fills with rain, a storm overflow lets sewage and rainwater out into a river or the sea, and a monitor
records when it starts and stops. The public is told one number per overflow, its <b>spill count</b>, and at 30 counted spills in a year
the overflow is to be investigated, unless the year's rainfall was exceptional. In 2025 the monitors recorded <b>{n(S["activations_used"])}</b> discharges at <b>{n(S["overflows_with_activations"])}</b>
overflows, <b>{n(S["hours_total"])} hours</b> in all. The counting rule made them <b>{n(nsp)}</b> spills — and a spill so counted held
anything from under a minute to a full day. <b>One overflow that discharged for 1 hour 16 minutes is counted 44 spills, over the trigger;
another that discharged for 567 hours is counted 27, under it.</b></p>
{fig}
<p class="sm mut">Every overflow with at least one counted spill in 2025 ({n(nfig)}), placed by its recorded hours (across) and its counted
spills (up), both on log scales; darker squares hold more overflows; hover a square for its count. Dashed: the one-year trigger. Counts are
this study's, made by the rule below from the companies' start/stop records, and equal the companies' own returned counts for
{100 * pr["P6"]["value"]:.1f} % of overflows.</p>
<h2>1. The rule</h2>
<p>The Environment Agency's <a href="https://www.gov.uk/government/publications/storm-overflow-assessment-framework-2025/storm-overflow-assessment-framework-2025">storm
overflow assessment framework 2025</a> (Appendix A) fixes how a spill is counted:</p>
<blockquote>“Counting starts when the first discharge occurs. Any discharges in the first 12-hour block are counted as one spill. Any
discharges in the next, and subsequent, 24-hour blocks are each counted as one additional spill per block. Counting continues until there is
a 24-hour block without a discharge.”</blockquote>
<p>So ten short discharges inside twelve hours are one spill; a discharge that runs for four days is five. The rule turns a stretch of
time into a number of events. The same framework sends an overflow to investigation at 30 counted spills in one year, or 20 a year on
average over two, leaving out years of exceptional rainfall.</p>
<h2>2. What one counted spill holds</h2>
<p>Of {n(nsp)} counted spills, <b>{n(lt1)}</b> ({100 * lt1 / nsp:.1f} %) hold less than an hour of discharge, and <b>{n(ge12)}</b>
({100 * ge12 / nsp:.1f} %) hold twelve hours or more. {n(E2["under_one_minute"])} hold under a minute; {n(E2["exactly_24h_or_more"])} hold a full 24 hours. The median counted spill holds
{int(qh["0.5"])} h {round(qh["0.5"] % 1 * 60)} min; one in ten holds {qh["0.9"]:.1f} hours or more. On average one counted spill folds {pr["P4"]["value"]:.1f} separately recorded discharges; one folds
{S["spill_acts_max"]:,}. Overflows counted 1 to 10 times discharged a median {pr["P10"]["value"][0]:.1f} hours per counted spill;
those counted over 60 times, {pr["P10"]["value"][1]:.1f}. The longest unbroken count, at {lg["uid"]}, ran from 1 January to 12
August without a discharge-free day: {S["longest_sequence"]["blocks"]} counted spills in one run. That overflow recorded {lg["acts"]} discharges in
the year, {lg["hours"]:,.0f} hours, {lg["count"]} counted spills.</p>
<h2>3. The trigger does not sort the hours</h2>
<p>{n(E["over30_annual"])} overflows were returned with 30 or more counted spills. Their median discharge was
{E["median_hours_over_trigger"]:.0f} hours. Below the trigger, <b>{E["under_trigger_with_more_hours_than_that"]}</b> overflows discharged
for longer than that. Among the {E["band_28_32_n"]} overflows returned with 28 to 32 counted spills — at the trigger — the hours run from
{E["band_28_32_hours_min_med_max"][0]:.1f} to {E["band_28_32_hours_min_med_max"][2]:.0f} (median {E["band_28_32_hours_min_med_max"][1]:.0f}).
The rule reads frequency, as it says it does; what it hands the public as one number is frequency and duration folded together, and at the
line where action begins the two come apart.</p>
<p><b>What this cannot say.</b> The record is the companies' own, not verified by the Environment Agency (its catalogue says so for the
start/stop data). A recorded activation is the monitor's reading that the overflow discharged; how much flowed, and what was in it, is not
in the record. Monitors that worked for only part of the year undercount; the annual return gives each monitor's operating share, not used
tonight. Discharges of 2025 that no monitor recorded are not here.</p>
<h2>4. Predictions and check</h2>
<p>Ten predictions were pushed before any file was downloaded (<a href="SELECTION.md">SELECTION.md</a>). {held} held.
P3 failed: a long discharge is counted once a day, so a day-long spill is common, not rare. P9 failed on its own terms: one company's
spreadsheet carries 995,359 blank rows after its data, which the registered measure counted as malformed; of the non-blank rows, 174
(0.016 %) are.</p>
<div class="tw"><table><tr><th></th><th style="text-align:left">registered</th><th>found</th><th></th></tr>{tab}</table></div>
<p class="sm mut">The recount equals the company's returned count for {n(S["matched_equal"])} of {n(S["matched"])} overflows; it is higher
for {n(S["matched_recount_higher"])} and lower for {n(S["matched_recount_lower"])}, mostly by one (not explained tonight). Recounted hours
agree with the returned durations within 0.1 h for {n(E["hours_within_0.1h"])}. Check: {C["held"]} of {C["of"]} overflows (twelve drawn
with seed {C["seed"]}, and the one with the most hours) counted again by a separate implementation in <code>awk</code>; rows per file
recounted by <code>wc -l</code>, all ten agreeing; the two marked overflows redone from the raw file with <code>grep</code>, the system's
<code>date</code> and <code>awk</code>. Rule <a href="rule.py">rule.py</a>; count <a href="count1.py">count1.py</a> →
<a href="session1.json">session1.json</a>, per overflow <a href="session1-per.json.gz">session1-per.json.gz</a>; check
<a href="check1.py">check1.py</a>, <a href="check1.awk">check1.awk</a> → <a href="check1.json">check1.json</a>; exploration
<a href="explore1.json">explore1.json</a>; journal <a href="JOURNAL.md">JOURNAL.md</a>.</p>
<h2>5. Where the discharge the trigger does not see goes, and when</h2>
<p class="sm mut">Session 2, 23 November 2026. Registration and nine predictions: <a href="SESSION2.md">SESSION2.md</a>, pushed before the
files were downloaded again.</p>
<p>{S2["U"]} overflows discharged for longer than the median overflow over the trigger ({S2["median_hours_O"]:.0f} hours) and were counted
under 30. The annual return names, for each overflow that carries a bathing-water or shellfish-water monitoring requirement, the water it
is monitored for. <b>{S2["U_bathing"]} of the {S2["U"]} are monitored for a bathing water</b> and {S2["U_shellfish"]} for a shellfish water.
Every one of the {S2["U"]} is entered in the return's own review column as “{html.escape(X2["hsf_reason_U"][0][0])}”. Their monitors
worked a median {pr2["P3"]["value"]:.2f} % of the year: these are not gaps in the record.</p>
<p><b>But almost none of their discharge falls in the bathing season.</b> Of their {n(S2["U_hours"])} hours, {n(S2["U_season_hours"])}
({100 * S2["U_season_hours"] / S2["U_hours"]:.1f} %) fall between 15 May and 30 September, the season the Bathing Water Regulations 2013
fix (reg. 4), which is {100 * S2["season_share_of_year"]:.0f} % of the year; {X2["U_season_zero"]} of them discharged not at all in it. Across
all overflows the share is {100 * S2["all_season_hours"] / S2["all_hours"]:.1f} %; for those monitored for a bathing water,
{100 * S2["bathing_season_hours"] / S2["bathing_hours"]:.1f} %. The Environment Agency calls 2025 “significantly drier than 2024 across large parts of England”
(<a href="https://www.gov.uk/government/news/fewer-and-shorter-storm-overflow-spills-in-2025-new-monitoring-data-shows">press release</a>).
The long discharges under the trigger are winter discharges: they fall outside the season the regulations set for bathing waters.</p>
{fig2}
<p class="sm mut">Hours of discharge recorded on each day of 2025, each row scaled to its own highest day. Shaded: the bathing season. Daily
sums from <a href="explore2b.json">explore2b.json</a> (exploratory); the season shares from <a href="session2.json">session2.json</a>, and both
agree.</p>
<div class="tw"><table><tr><th style="text-align:left">overflow</th><th style="text-align:left">bathing water named</th><th>hours 2025</th><th>counted</th><th>hours in season</th></tr>{tab2}</table></div>
<p class="sm mut">The {S2["U_bathing"]} long under-trigger overflows monitored for a bathing water. “Named” means the overflow carries a
bathing-water monitoring requirement and the company entered the water; it does not say how far away the water is or what reached it.</p>
<p><b>Monitors.</b> {100 * pr2["P4"]["value"]:.1f} % of monitors worked less than 90 % of 2025. The {S2["lowop_lt50"]} that worked less than
half the year were counted a median {pr2["P5"]["value"][0]:.0f} spills, against {pr2["P5"]["value"][1]:.0f} for those working 90 % or more: a
count is also a count of the time the monitor was listening.</p>
<p><b>Why the recount differs.</b> At {n(S2["differing"])} overflows the recount and the returned count part, at
{100 * pr2["P6"]["value"]:.1f} % of them by exactly one. Three readings of the rule were tried against all overflows: an activation ending
exactly on a block's edge touching the next block; a count that restarts after 24 hours without discharge measured from the last stop rather
than on the block grid; times cut to the minute. None matches the returned counts more often than the rule as read ({n(pr2["P7"]["value"]["v0"])}
of {n(S2["matched"])}); the restart reading reconciles {S2["recon_by_variant"]["v2"]} of the differing overflows and breaks far more. What the
differences share is the year's edge: {ye["+1"]["with_activation_within_36h_of_year_edge"]} of the {ye["+1"]["n"]} overflows recounted one higher
discharged within 36 hours of 1 January or 31 December, against {ye["equal"]["with_activation_within_36h_of_year_edge"]:,} of the
{ye["equal"]["n"]:,} that agree. A count carried across New Year in the companies' records, and opened afresh in this one, would do this; that is
<b>conjecture</b>, not tested tonight.</p>
<div class="tw"><table><tr><th></th><th style="text-align:left">registered</th><th>found</th><th></th></tr>{tab3}</table></div>
<p class="sm mut">{held2} of 9 held. P1 failed narrowly ({S2["U_bathing"]} of {S2["U"]}); P7 failed — the rule as read is the closest of the
four; P9 failed — the bathing-named overflows discharge mostly out of season. Check {C2["held"]} of {C2["of"]}: the receiving, shellfish and
bathing values of twelve drawn overflows read again from the spreadsheet's XML with <code>unzip</code>, <code>sed</code>, <code>grep</code>
and <code>awk</code> (<a href="check2.sh">check2.sh</a>); the season hours of three drawn overflows redone with <code>grep</code>, the system's
<code>date</code> and <code>awk</code> (<a href="check2b.sh">check2b.sh</a>); six variant-reconciled counts redone, one by hand and all six by a
separate <code>awk</code> implementation (<a href="check2c.awk">check2c.awk</a>) → <a href="check2.json">check2.json</a>. Count
<a href="count2.py">count2.py</a> → <a href="session2.json">session2.json</a>, per overflow <a href="session2-per.json.gz">session2-per.json.gz</a>;
exploration <a href="explore2.json">explore2.json</a>. The record says where an overflow is monitored for; it cannot say what reached a
bather, nor whether a monitor's own operating figure is right.</p>
<p class="sm mut">Companies are not compared or ranked on this page; overflows are named by the identifier the record gives them.</p>
</main></body></html>
'''
open('index.html', 'w').write(page)
print(len(page), 'bytes', len(bins), 'bins')
