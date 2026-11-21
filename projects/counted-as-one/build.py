"""Project 26: build the study page index.html from session1.json, session1-per.json.gz, check1.json, explore1.json.
Stdlib only. Usage: python3 -I build.py   (run in projects/counted-as-one/)"""
import gzip, html, json, math
S = json.load(open('session1.json'))
P = json.load(gzip.open('session1-per.json.gz', 'rt'))
C = json.load(open('check1.json'))
E = json.load(open('explore1.json'))
E2 = json.load(open('explore1b.json'))
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
svg.ch .mk{{fill:none;stroke:var(--fg);stroke-width:2}}svg.ch .ml{{font:600 12px system-ui,sans-serif;fill:var(--fg)}}
.sc{{overflow-x:auto}}.sc svg.ch{{min-width:680px}}.tw{{overflow-x:auto}}
table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
blockquote{{margin:1em 0;padding-left:14px;border-left:3px solid var(--line)}}
</style></head><body><main>
<p class="sm mut">Project 26, session 1 · 21 November 2026 · open; no work before session 3 · data: Environment Agency, Event Duration
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
<p class="sm mut">Companies are not compared or ranked on this page; overflows are named by the identifier the record gives them.</p>
</main></body></html>
'''
open('index.html', 'w').write(page)
print(len(page), 'bytes', len(bins), 'bins')
