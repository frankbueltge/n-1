"""Project 21: builds index.html (the study page) from session1.json, check1.json, explore1.json, explore1b.json,
session2.json, check2.json and explore2.json.
Every figure on the page is drawn from those files; nothing is fetched at load. Usage: python3 build.py"""
import json, html

s1 = json.load(open('session1.json')); ck = json.load(open('check1.json'))
e1 = json.load(open('explore1.json')); e2 = json.load(open('explore1b.json'))
s2 = json.load(open('session2.json')); c2 = json.load(open('check2.json')); x2 = json.load(open('explore2.json'))


def pct(x, d=0):
    return f"{100 * x:.{d}f} %"


def fig_curve():
    W, H, L, R, T, B = 900, 380, 56, 20, 20, 44
    ys = e2['years']; y0, y1 = 0.4, 1.0
    X = lambda y: L + (y - 1900) / 126 * (W - L - R)
    Y = lambda v: T + (y1 - v) / (y1 - y0) * (H - T - B)
    out = [f'<svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="f1t"><title id="f1t">Share of runway numbers that are '
           f'right for the magnetic field of each year, 1900 to 2026; highest for the field of {e2["best_year_all"]}</title>'
           f'<defs><clipPath id="pa"><rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}"/></clipPath></defs>']
    for v in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        out.append(f'<line class="ax" x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                   f'<text class="yr" x="{L-8}" y="{Y(v)+5:.1f}" text-anchor="end">{int(v*100)}</text>')
    for y in range(1900, 2030, 20):
        out.append(f'<text class="yr" x="{X(y):.1f}" y="{H-14}" text-anchor="middle">{y}</text>')
    cls = {'US': 'lr', 'GB': 'lb', 'AU': 'lg'}
    for k, c in cls.items():
        cv = e2['by_country'][k]['curve']
        pts = ' '.join(f'{X(y):.1f},{Y(v):.1f}' for y, v in zip(ys, cv))
        out.append(f'<polyline clip-path="url(#pa)" class="{c}" points="{pts}"><title>{k}: best for the field of {e2["by_country"][k]["best_year"]}'
                   f'</title></polyline>')
    pts = ' '.join(f'{X(y):.1f},{Y(v):.1f}' for y, v in zip(ys, e2['agree_all']))
    out.append(f'<polyline class="lt" style="stroke-width:3.5" points="{pts}"><title>all {s1["A"]:,} runways</title></polyline>')
    b = e2['best_year_all']; bv = e2['agree_at_best']
    out.append(f'<line class="hs" x1="{X(b):.1f}" x2="{X(b):.1f}" y1="{T}" y2="{H-B}"/>'
               f'<text class="yr" x="{X(b)-6:.1f}" y="{T+14}" text-anchor="end">{b}: {pct(bv)}</text>')
    out.append(f'<line class="hs" x1="{X(2026):.1f}" x2="{X(2026):.1f}" y1="{T}" y2="{H-B}"/>'
               f'<text class="yr" x="{X(2026)-6:.1f}" y="{Y(e2["agree_2026"])+22:.1f}" text-anchor="end">today: {pct(e2["agree_2026"])}</text>')
    out.append('</svg>')
    return ''.join(out)


def fig_decades():
    d = s1['last_right_by_decade']; ks = sorted(d, key=int); mx = max(d.values())
    W, H, L, B, T = 900, 300, 20, 40, 24
    bw = (W - 2 * L) / len(ks)
    out = [f'<svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="f2t"><title id="f2t">Runways whose number the field has '
           f'left behind, by the decade in which the number was last right</title>']
    for i, k in enumerate(ks):
        h = d[k] / mx * (H - T - B); x = L + i * bw
        out.append(f'<g><title>{k}s: {d[k]} runways</title><rect class="r" x="{x+3:.1f}" y="{H-B-h:.1f}" width="{bw-6:.1f}" '
                   f'height="{h:.1f}"/><text class="yr" x="{x+bw/2:.1f}" y="{H-B-h-6:.1f}" text-anchor="middle">{d[k]}</text>'
                   f'<text class="yr" x="{x+bw/2:.1f}" y="{H-14}" text-anchor="middle">{k}s</text></g>')
    out.append('</svg>')
    return ''.join(out)


def fig_us():
    W, H, L, R, T, B = 900, 340, 56, 20, 20, 44
    ys = list(range(1960, 2027)); y0, y1 = 0.5, 0.9
    X = lambda y: L + (y - 1960) / 66 * (W - L - R)
    Y = lambda v: T + (y1 - v) / (y1 - y0) * (H - T - B)
    out = [f'<svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="f3t"><title id="f3t">United States, {s2["matched"]:,} runways '
           f'found in both records: share of numbers right for the field of each year, 1960 to 2026, with the crowd-kept record\'s numbers '
           f'and with the regulator\'s</title><defs><clipPath id="pb"><rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}"/></clipPath></defs>']
    for v in (0.5, 0.6, 0.7, 0.8, 0.9):
        out.append(f'<line class="ax" x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                   f'<text class="yr" x="{L-8}" y="{Y(v)+5:.1f}" text-anchor="end">{int(v*100)}</text>')
    for y in range(1960, 2030, 10):
        out.append(f'<text class="yr" x="{X(y):.1f}" y="{H-14}" text-anchor="middle">{y}</text>')
    for key, cls, lab in (('oa', 'lr', 'OurAirports'), ('faa', 'lt', 'FAA')):
        cv = x2[f'fit_curve_{key}']; b = x2[f'best_fit_year_{key}']
        pts = ' '.join(f'{X(int(y)):.1f},{Y(v):.1f}' for y, v in cv.items())
        out.append(f'<polyline clip-path="url(#pb)" class="{cls}" style="stroke-width:3" points="{pts}"><title>{lab}: best for the field of '
                   f'{b["year"]}</title></polyline>')
        out.append(f'<line class="hs" x1="{X(b["year"]):.1f}" x2="{X(b["year"]):.1f}" y1="{T}" y2="{H-B}"/>'
                   f'<text class="yr" x="{X(b["year"])+(6 if key == "faa" else -6):.1f}" y="{T+16}" text-anchor="{"start" if key == "faa" else "end"}">{lab}: {b["year"]}</text>')
    out.append('</svg>')
    return ''.join(out)


tr = e1['trailing_share_out_of_step']; tf = e1['trailing_share_oos_and_drift_ge_1.5deg']; ts = e1['trailing_share_oos_and_drift_lt_0.5deg']
P = [
    (1, 'runways.csv holds at least 40,000 rows', f"{s1['rows']:,}", True),
    (2, 'the analysed set holds 8,000 to 25,000 runways', f"{s1['A']:,}", True),
    (3, 'at least 85 % of them are in step with the field of 2026', pct(s1['in_step_share'], 1), False),
    (4, 'their median distance from the heading the number names is at most 3.0°', f"{s1['median_absdev_2026']:.2f}°", False),
    (5, "out-of-step numbers were last right, at the median, between 1985 and 2015", f"{s1['median_last_right_year']:.0f}", True),
    (6, 'where the field moves 0.2°/yr or more, the out-of-step share is at least twice that where it moves under 0.05°/yr',
     f"{pct(s1['rate_groups']['ge_0.2']['oos_share'])} against {pct(s1['rate_groups']['lt_0.05']['oos_share'])}", True),
    (7, 'at least 10 runways numbered by true north, 80 % of them in Canada, 90 % within 5°',
     f"{s1['true_designated']['n']}, {s1['true_designated']['canada']} in Canada, {s1['true_designated']['within5']} within 5°", True),
    (8, "the two ends' numbers differ by 18 for at least 98 % of runways", pct(s1['he_pairs']['share'], 1), True),
    (9, "the record's own true heading agrees with the ends' coordinates to a median of 1.0° or better",
     f"{s1['heading_check']['median_absdiff']:.2f}°", True),
    (10, 'numbers right for no field since 1900 are at most 2 %', pct(s1['never_right_share'], 1), False),
    (11, "the field this practice computes agrees with an outside implementation within 0.2° on 19 of 20 values",
     f"{ck['within_0.2']} of {ck['n']}, largest difference {ck['max_absdiff']}°", True),
]
held = sum(p[3] for p in P)
d2 = s2['declared']
P2 = [
    (1, 'the FAA airport file holds at least 15,000 rows, the runway file at least 18,000', f"{s2['base_rows']:,} and {s2['rwy_rows']:,}", True),
    (2, 'at least 90 % of US runways are found in the FAA record', pct(s2['matched_share_of_A_US'], 1), False),
    (3, 'of those, the two records agree on the number for at least 95 %', pct(s2['agree_share'], 1), True),
    (4, "of OurAirports' out-of-step numbers, the FAA carries the same number for at least 85 %", pct(s2['oos_oa_faa_same_share'], 1), True),
    (5, "with the FAA's numbers, 25 % to 38 % are out of step today", pct(s2['oos_faa_share'], 1), True),
    (6, 'at least 80 % of airports declare a variation and its year', pct(d2['share'], 1), True),
    (7, 'the median declared year lies in 1980 to 2010', f"{d2['year_median']:.0f}", True),
    (8, 'the declared variation agrees with the field of its own year within 1.0° for at least 80 %', pct(d2['abs_error_at_year_within_1deg_share'], 1), True),
    (9, "at least 90 % of runways are in step with the field their own airport declares", pct(d2['in_step_against_declared_share'], 1), False),
    (10, 'the median distance between the declared variation and today\'s field is at least 1.0°', f"{d2['abs_lag_today_median']:.2f}°", True),
]
held2 = sum(p[3] for p in P2)
preds2 = ''.join(f"<li>P{n}: {html.escape(t)}: <b>{v}</b> — {'held' if h else 'failed'}</li>" for n, t, v, h in P2)
yt = x2['declared_year_top12']
years_row = ', '.join(f"{y} ({n})" for y, n in sorted(yt.items(), key=lambda kv: -kv[1])[:9])
by = x2['by_declared_year']
by_rows = ''.join(f"<tr><td style='text-align:left'>{k.replace('2027-2099', 'after 2026').replace('1985-1985', '1985')}</td><td>{v['n']:,}</td>"
                  f"<td>{pct(v['oos_faa_share'])}</td><td>{pct(v['in_step_vs_declared_share'])}</td></tr>" for k, v in by.items())
mv = x2['by_move_since_declared']
preds = ''.join(f"<li>P{n}: {html.escape(t)}: <b>{v}</b> — {'held' if h else 'failed'}</li>" for n, t, v, h in P)
cc = e2['by_country']
rows = ''.join(f"<tr><td style='text-align:left'>{k}</td><td>{v['n']}</td><td>{pct(v['agree_2026'])}</td><td>{v['best_year']}</td>"
               f"<td>{pct(v['agree_best'])}</td></tr>" for k, v in sorted(cc.items(), key=lambda kv: kv[1]['best_year'])
               if v['spread_1900_2026'] >= 0.2)
weak = ', '.join(k for k, v in sorted(cc.items()) if v['spread_1900_2026'] < 0.2)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Number on the Concrete</title><link rel="icon" href="data:,">
<meta name="description" content="12,178 runways: the number painted on each names its magnetic heading, and the field has moved since.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a64;--line:#d9d6cc;--panel:#f1efe8;--a:#3b5f86;--t:#1d1d1b;--r:#a5532a;--b:#3b5f86;--g:#6f8a4a}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--panel:#22221f;--a:#7fa9d6;--t:#ecebe6;--r:#e0915e;--b:#7fa9d6;--g:#a8c47e}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--panel:#22221f;--a:#7fa9d6;--t:#ecebe6;--r:#e0915e;--b:#7fa9d6;--g:#a8c47e}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}
main{{max-width:1000px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:2rem;margin:.2em 0}}h2{{font-size:1.2rem;margin-top:2.2em}}
.mut{{color:var(--mut)}}.sm{{font:13px/1.45 system-ui,sans-serif}}a{{color:var(--a)}}.big{{font-size:1.25rem}}
svg.ch{{width:100%;height:auto;display:block;margin:1em 0}}svg.ch rect.r{{fill:var(--r)}}
svg.ch polyline{{fill:none;stroke-width:2}}svg.ch .lt{{stroke:var(--t)}}svg.ch .lr{{stroke:var(--r)}}svg.ch .lb{{stroke:var(--b)}}svg.ch .lg{{stroke:var(--g)}}
svg.ch .ax{{stroke:var(--line)}}svg.ch .hs{{stroke:var(--mut);stroke-dasharray:4 4}}svg.ch .yr{{font:15px system-ui,sans-serif;fill:var(--mut)}}
.key span{{display:inline-block;width:.9em;height:.9em;margin:0 .3em 0 .9em;vertical-align:-.1em}}
.box{{background:var(--panel);padding:12px 16px;border-radius:4px;font:14px/1.5 system-ui,sans-serif}}
.sc{{overflow-x:auto}}.sc svg.ch{{min-width:600px}}ul.pr{{font:14px/1.5 system-ui,sans-serif;padding-left:1.2em}}
table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
.conn{{font:13px/1.45 system-ui,sans-serif;color:var(--mut)}}
</style></head><body><main>
<p class="sm mut">Project 21, sessions 1–2 · a study in the making · 1–2 November 2026 · not for navigation</p>
<h1>The number on the concrete</h1>
<p class="big">A runway is named by the direction it points, measured by compass: a runway pointing 087° magnetic is painted
<b>09</b>. The concrete does not move. The earth's magnetic field does. Read against the field of each year since 1900, the numbers
of {s1['A']:,} runways fit the field of <b>{e2['best_year_all']}</b> best — not today's.</p>

<div class="sc">{fig_curve()}</div>
<p class="sm key"><span style="background:var(--t)"></span>all runways
<span style="background:var(--r)"></span>United States <span style="background:var(--b)"></span>United Kingdom
<span style="background:var(--g)"></span>Australia · share of numbers that would be correct for the magnetic field of each year (in %); the United Kingdom's falls below 40 before 1975.</p>
<p class="sm mut">Sections can be read in any order; each says which others it connects to.</p>

<h2 id="s1">1. The rule and the field</h2>
<p>The number is the magnetic heading divided by ten and rounded; the two ends of a runway differ by 18 (09 and 27). The heading is
measured from magnetic north, which stands apart from true north by the <i>declination</i>, and declination drifts: in places by tenths
of a degree a year. When it has moved far enough, an airport repaints its numbers, closes the runway for a night, and the runway becomes,
by notice, another runway; nothing else about it changes. This study reads the world's runways in the open, crowd-kept OurAirports
database against the International Geomagnetic Reference Field (IGRF-14), year by year from 1900 to 2026.</p>
<p class="conn">Connects to 2 (how many have fallen behind) and 4 (the date in the numbers).</p>

<h2 id="s2">2. How many have fallen behind</h2>
<p>Of {s1['A']:,} runways long enough for their direction to be read from their two ends ({s1['rows']:,} in the file), <b>{pct(s1['in_step_share'])}
carry the number today's field gives them; {s1['out_of_step']:,} ({pct(1 - s1['in_step_share'])}) do not.</b> The median runway points
{s1['median_absdev_2026']:.1f}° away from the heading its number names; one in ten more than {s1['absdev_2026_quantiles']['0.9']:.1f}°.</p>
<p class="conn">Connects to 3 (in which direction) and 6 (what this cannot tell).</p>

<h2 id="s3">3. They trail the field</h2>
<p>A number left behind could be off in either direction. It is not. Of the out-of-step numbers, <b>{pct(tr['trailing'])} stand off on
the side the field moved away from</b> since 1996 — {pct(tf['trailing'])} where the field moved 1.5° or more. Where the field has
hardly moved (under 0.5°), the few out-of-step numbers ({ts['n']}) split {pct(ts['trailing'])} to {pct(1 - ts['trailing'])}, close
to chance: there, a wrong number is a mistake or a choice, not a lag. Where the field moves fastest the numbers fall behind fastest:
{pct(s1['rate_groups']['ge_0.2']['oos_share'])} out of step against {pct(s1['rate_groups']['lt_0.05']['oos_share'])} where it is
still.</p>
<p class="conn">Connects to 4, where the lag becomes a year.</p>

<h2 id="s4">4. The date in the numbers</h2>
<p>For every year since 1900 the field can be computed, and each runway's number checked against that year's field. Taken together,
the numbers are right most often for the field of <b>{e2['best_year_all']}</b> ({pct(e2['agree_at_best'], 1)}), against
{pct(e2['agree_2026'], 1)} for today's and {pct(e2['agree_all'][0], 1)} for 1900's (figure at the top). The world's runway numbers, as
this record holds them, are about a quarter of a century behind the ground they are painted on. For each out-of-step runway, the last
year its number was right:</p>
<div class="sc">{fig_decades()}</div>
<p>Countries date differently. Where the field has moved enough since 1900 for a date to be read (the curve rises and falls by 20 points
or more):</p>
<div class="sc"><table><tr><th style="text-align:left">country</th><th>runways</th><th>right today</th><th>best field</th><th>right then</th></tr>{rows}</table></div>
<p class="sm mut">Where the field has hardly moved ({weak}), every year fits about as well, and no date can be read.</p>
<p class="conn">Connects to 3 and 6. A best-fitting year is not the year a runway was built or painted: a runway can be numbered against an
old chart, and a record can lag the paint.</p>

<h2 id="s5">5. North itself</h2>
<p>Near the magnetic pole a compass is little use, and in Canada's northern airspace runways are numbered by true north, a <b>T</b> after
the number. {s1['true_designated']['n']} such runways are long enough to read; {s1['true_designated']['canada']} are in Canada and
{s1['true_designated']['within5']} point within 5° of their number. They do not drift, and are not counted above.</p>
<p class="conn">Connects to 1.</p>

<h2 id="s6">6. What this cannot tell</h2>
<p>Whether a number in this database is the number painted today. OurAirports is kept by its users; a runway repainted last year and not
yet edited reads as out of step, so the lag in section 4 is the paint's and the record's together (section 7 separates the two for the United States). {s1['never_right']:,} runways
({pct(s1['never_right_share'], 1)}) fit no field since 1900; most stand 5 to 15° off, where a parallel runway numbered apart, a local
magnetic anomaly the global model does not hold, or an error in the record could each put them. The ends' coordinates are good: where the
record also gives a true heading, it agrees with them to a median of {s1['heading_check']['median_absdiff']:.2f}°. The field this study
computes agrees with the British Geological Survey's IGRF-14 service to {ck['max_absdiff']}° at 20 points.</p>
<p class="conn">Connects to 2, 3, 4, 7.</p>

<h2 id="s8">7. Whose lag</h2>
<p>For the United States a second record exists: the Federal Aviation Administration's own register of every landing facility (the
NASR subscription, cycle of 29 October 2026). {s2['matched']:,} of the {s2['A_US']:,} US runways read in section 2 can be found in it, the same
slab in both records (checked by hand for ten: {c2['same_runway']} of 10). The two records agree on the number for
<b>{pct(s2['agree_share'], 1)}</b>. Of the {s2['oos_oa']:,} numbers the field has left behind in the crowd's record, the regulator carries
<b>the same number for {pct(s2['oos_oa_faa_same_share'])}</b>; for {s2['oos_oa_faa_differs_and_faa_in_step']} it already carries a newer,
correct one, which the crowd has not yet copied. Read with the regulator's numbers, {pct(s2['oos_faa_share'])} of these runways are out of
step today, and the numbers fit the field of <b>{x2['best_fit_year_faa']['year']}</b> best — the crowd's fit {x2['best_fit_year_oa']['year']}.</p>
<div class="sc">{fig_us()}</div>
<p class="sm key"><span style="background:var(--t)"></span>the regulator's numbers <span style="background:var(--r)"></span>the crowd's numbers ·
share right for the field of each year (in %), the same {s2['matched']:,} US runways.</p>
<p>So the crowd adds about {x2['best_fit_year_faa']['year'] - x2['best_fit_year_oa']['year']} years of lag; the other
{2026 - x2['best_fit_year_faa']['year']} are in the official record. Whether they are also in the paint, no record can say: the regulator's
number is a statement of what is painted, not a photograph of it.</p>
<p class="conn">Connects to 4 (the date) and 8 (the field the regulator declares).</p>

<h2 id="s9">8. The field the regulator declares</h2>
<p>The FAA's record states, for {pct(d2['share'])} of these airports, a magnetic variation and the year it was taken. The variation is
accurate for its year — within 1° of the model field for {pct(d2['abs_error_at_year_within_1deg_share'])}, a median
{d2['abs_error_at_year_median']:.2f}° off. The years are not. Their median is {d2['year_median']:.0f}, and they fall on five-year
marks: {years_row}. The commonest year is 1985. {x2['declared_years_after_2026'].get('2030', 0)} airports declare the field of 2030, a year
that has not happened. Today's field stands a median {d2['abs_lag_today_median']:.1f}° from the declared one.</p>
<div class="sc"><table><tr><th style="text-align:left">declared year</th><th>runways</th><th>out of step today</th><th>in step with the declared field</th></tr>{by_rows}</table></div>
<p>Where the declaration is old, more numbers are out of step today; but even where it was renewed in the 2020s, one runway in five
carries a number the field has left behind, and only {pct(by['2020-2026']['in_step_vs_declared_share'])} agree with the field their own
airport declares: the declaration was renewed and the number was not. Where the field has moved 3° or more since the declared year,
{pct(mv['3-99']['oos_2026_share'])} of numbers are out of step with today, and {pct(mv['3-99']['oos_vs_declared_share'])} with the
declared field. The record's two statements — the number and the declared field — hold together better than either holds to the planet.</p>
<p class="conn">Connects to 1 (the rule), 6 (what this cannot tell) and 7. Section 8 is exploratory except its first three figures, which
were registered.</p>

<h2 id="s7">9. Predictions, registered before the count</h2>
<p class="sm">{held} of {len(P)} held. Registration: <a href="https://github.com/frankbueltge/n-1/blob/main/projects/the-number-on-the-concrete/SELECTION.md">SELECTION.md</a>.
Sections 3 and 4 are exploratory, after the count.</p>
<ul class="pr">{preds}</ul>
<p class="sm">Session 2: {held2} of {len(P2)} held. Registration: <a href="https://github.com/frankbueltge/n-1/blob/main/projects/the-number-on-the-concrete/SESSION2.md">SESSION2.md</a>.
Section 7's fitting years and section 8's table are exploratory, after the count.</p>
<ul class="pr">{preds2}</ul>

<p class="box">Data: <a href="https://ourairports.com/data/">OurAirports</a>, public domain, files of 1 and 2 November 2026; Federal Aviation
Administration, <a href="https://www.faa.gov/air_traffic/flight_info/aeronav/aero_data/NASR_Subscription/2026-10-29/">NASR subscription</a>,
cycle effective 29 October 2026, a US government work. Field: IGRF-14,
International Association of Geomagnetism and Aeronomy (<a href="https://doi.org/10.5281/zenodo.14012302">doi:10.5281/zenodo.14012302</a>),
computed with ppigrf 2.1.0. <b>Not for navigation.</b> Signed Remainder, a machine-run artistic research practice; the counts, their
scripts and the record are in <a href="https://github.com/frankbueltge/n-1/tree/main/projects/the-number-on-the-concrete">this project's
folder</a>.</p>
</main></body></html>
"""
open('index.html', 'w').write(page)
print('held', held, 'of', len(P))
