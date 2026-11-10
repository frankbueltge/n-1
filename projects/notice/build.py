"""Project 23: build the study page index.html from session1.json, explore1.json, explore1b.json, explore1c.json, check1.json
(stdlib only). Usage: python3 -I build.py   (run in projects/notice/)"""
import json, html, time

S = json.load(open('session1.json'))
E = json.load(open('explore1.json'))
B = json.load(open('explore1b.json'))
K = json.load(open('explore1c.json'))
C = json.load(open('check1.json'))
S2 = json.load(open('session2.json'))
C2 = json.load(open('check2.json'))
S3 = json.load(open('session3.json'))
C3 = json.load(open('check3.json'))
C3b = json.load(open('check3b.json'))


def n(x):
    return f'{x:,}'


def pct(x, d=1):
    return f'{100 * x:.{d}f}'


kind = {(r['zone'], r['t']): r['kind'] for r in K['rows']}
core = [r for r in E['rows'] if not r['with_zone'] and not r['censored']]
Y = lambda t: time.gmtime(t).tm_year + (time.gmtime(t).tm_yday - 1) / 366

# Figure 1: every transition of the exploratory run's core set with |lead| <= 365 days, x = when the clock moved, y = lead
W, H, L, T, BOT = 900, 420, 52, 18, 40
x0, x1 = 1997, 2027
lim = 365
def px(t):
    return L + (Y(t) - x0) / (x1 - x0) * (W - L - 12)
def py(d):
    return T + (lim - max(-lim, min(lim, d))) / (2 * lim) * (H - T - BOT)
dots = []
far = {}
for r in core:
    d = r['lead_days']
    k = kind.get((r['zone'], r['t']), '')
    if d > lim:
        y = time.gmtime(r['t']).tm_year
        far[y] = far.get(y, 0) + 1
        continue
    if d < -lim:
        continue
    if d < 0:
        cls = 'nw' if k.endswith('new_offset') else 'rt'
    elif d < 30:
        cls = 'sh'
    else:
        cls = 'ok'
    when = time.strftime('%Y-%m-%d %H:%M UT', time.gmtime(r['t']))
    lab = f'{html.escape(r["zone"])}, {when}: first carried in release {r["first"]} ({r["first_date"]}), {abs(d):.0f} days {"after" if d < 0 else "before"}'
    dots.append(f'<circle class="{cls}" cx="{px(r["t"]):.1f}" cy="{py(d):.1f}" r="3"><title>{lab}</title></circle>')
ax = []
for v in (-365, -180, 0, 180, 365):
    yy = py(v)
    ax.append(f'<line class="{"z" if v == 0 else "ax"}" x1="{L}" x2="{W - 12}" y1="{yy:.1f}" y2="{yy:.1f}"/>'
              f'<text class="yr" x="{L - 6}" y="{yy + 5:.1f}" text-anchor="end">{v:+d}</text>')
for y in range(2000, 2030, 5):
    xx = L + (y - x0) / (x1 - x0) * (W - L - 12)
    ax.append(f'<text class="yr" x="{xx:.1f}" y="{H - BOT + 24}" text-anchor="middle">{y}</text>')
ax.append(f'<text class="yr" x="{W - 14}" y="{py(0) - 8:.1f}" text-anchor="end">the day the clocks moved</text>')
ax.append(f'<text class="yr" x="{W - 14}" y="{py(-330):.1f}" text-anchor="end">below: the clocks moved first, the record later</text>')
fig1 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="f1t"><title id="f1t">Every change of a '
        f'region\'s clock from 1997 to 2026 that the tz database carried less than a year ahead, placed by when it took effect and by how '
        f'many days before or after that its first release came</title>{"".join(ax)}{"".join(dots)}</svg></div>')
n_dots = len(dots)

per = B['per_year']
rows = []
for y in sorted(per, key=int):
    p = per[y]
    rows.append(f'<tr><td>{y}</td><td>{n(p["core"])}</td><td>{p["late_news"]}</td><td>{p["past_rewritten"]}</td><td>{p["under_30_days"]}</td></tr>')
table = ('<div class="sc"><table><thead><tr><th>year</th><th>changes timed</th><th>late, within a year</th><th>late by more than a year</th>'
         '<th>under 30 days ahead</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')

P = S['predictions']
PRED = [
    ('P1', 'At least 260 of the 275 releases compile with this machine\'s zic.', P['P1'], f'{S["releases_compiled"]} compiled; all 61 failures are releases before 2000f, whose data ask zic for a helper command (yearistype) the modern zic no longer has.'),
    ('P2', 'At least 200 releases carry a date in the newest NEWS.', P['P2'], f'{S["dated_news"]} of {S["releases_total"]}.'),
    ('P3', 'The newest release has 300 to 380 zones.', P['P3'], f'{S["zones_newest"]}.'),
    ('P4', 'The final set holds 7,000 to 20,000 transitions.', P['P4'], f'{n(S["final_transitions"])}.'),
    ('P5', 'The late share lies between 0.5 % and 5 %.', P['P5'], f'{pct(S["late_share"])} % ({S["late"]} of {n(S["core"])}).'),
    ('P6', 'The share under 30 days ahead (late included) lies between 2 % and 10 %.', P['P6'], f'{pct(S["lt30_share"])} %.'),
    ('P7', 'The median lead is at least three years.', P['P7'], f'{S["median_lead_days"] / 365.25:.1f} years.'),
    ('P8', 'The year with the most late transitions lies in 2011-2016.', P['P8'], f'{S["peak_late_year"]}, an edge of the compiled archive (see 5).'),
    ('P9', 'At least one transition was late by more than 365 days.', P['P9'], f'{S["max_late_days"] / 365.25:.0f} years at most.'),
    ('P10', 'The late share is higher for 2010-2026 than for 1997-2009.', P['P10'], f'{pct(S["late_share_2010_2026"])} % against {pct(S["late_share_1997_2009"])} %: the reverse.'),
    ('P11', 'The zdump check holds for at least 11 of 12.', C['P11'], f'{C["holds"]} of {C["n"]} (see 4).'),
]
plist = ''.join(f'<li><b>{k}</b> {html.escape(t)} — {"held" if ok else "failed"}: {html.escape(r)}</li>' for k, t, ok, r in PRED)
held = sum(1 for p in PRED if p[2])

kc = K['counts']
nw = kc.get('news/new_offset', 0)
recent_nw = sum(1 for r in K['rows'] if r['kind'] == 'news/new_offset' and time.gmtime(r['t']).tm_year >= 2020)
ev_late = B['events_late']

# Figure 2 (session 2): every episode in which the then-newest release showed an offset the final release says was wrong
EP = S2['episodes_rows']
tot = {}
for e in EP:
    tot[e['zone']] = tot.get(e['zone'], 0) + e['hours']
zs = sorted(tot, key=lambda z: -tot[z])
RH, L2, T2, W2 = 8, 150, 14, 900
H2 = T2 + RH * len(zs) + 34
def px2(t):
    return L2 + (Y(t) - 1997) / (2027 - 1997) * (W2 - L2 - 12)
bars, ax2 = [], []
for y in range(1997, 2026, 5):
    xx = L2 + (y - 1997) / 30 * (W2 - L2 - 12)
    ax2.append(f'<line class="ax" x1="{xx:.1f}" x2="{xx:.1f}" y1="{T2}" y2="{H2 - 30}"/><text class="yr" x="{xx:.1f}" y="{H2 - 10}" text-anchor="middle">{y}</text>')
KN = {'news': 'nw', 'retimed': 'rt', 'past': 'pa'}
KW = {'news': 'news that came after the clocks moved', 'retimed': 'a change carried at the wrong moment', 'past': 'found wrong more than a year later'}
for i, z in enumerate(zs):
    yy = T2 + i * RH
    if i < 8:
        ax2.append(f'<text class="yr lb" x="{L2 - 6}" y="{yy + RH - 1}" text-anchor="end">{html.escape(z.split("/")[-1].replace("_", " "))}</text>')
    for e in (e for e in EP if e['zone'] == z):
        x_a, x_b = px2(e['t0']), px2(e['t1'])
        a = time.strftime('%Y-%m-%d', time.gmtime(e['t0'])); b = time.strftime('%Y-%m-%d', time.gmtime(e['t1']))
        lab = (f'{html.escape(z)}, {a} to {b}: the newest release ({e["rel"]}) showed UT{e["shown"] / 3600:+g} h, the record now says '
               f'UT{e["final"] / 3600:+g} h; {KW[e["kind"]]} (corrected in {e["corr"]})')
        bars.append(f'<rect class="{KN[e["kind"]]}" x="{x_a:.1f}" y="{yy + 1}" width="{max(1.2, x_b - x_a):.1f}" height="{RH - 2}"><title>{lab}</title></rect>')
fig2 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W2} {H2}" role="img" aria-labelledby="f2t"><title id="f2t">Every stretch of time '
        f'since 1997 in which the newest release of the tz database showed a region an hour that the database now says was wrong, one row '
        f'per region</title>{"".join(ax2)}{"".join(bars)}</svg></div>')
BK = S2['by_kind_hours']; EPn = S2['episodes']; ZK = S2['zones_by_kind']
P2 = S2['predictions']
PRED2 = [
    ('P1', 'Exactly 252 releases compile with the helper.', P2['P1'], f'{S2["releases_compiled"]}.'),
    ('P2', 'Zone-hours wrong lie between 200,000 and 5,000,000.', P2['P2'], f'{n(round(S2["zone_hours_wrong"]))}.'),
    ('P3', 'Hours found wrong more than a year later carry over 70 % of the total.', P2['P3'], f'{pct(BK["past"] / S2["zone_hours_wrong"])} %.'),
    ('P4', 'Re-timed episodes carry fewer hours than news.', P2['P4'], f'{n(round(BK["retimed"]))} against {n(round(BK["news"]))}.'),
    ('P5', '60 to 200 zones have an episode.', P2['P5'], f'{S2["zones_with_episode"]}.'),
    ('P6', 'Hours wrong are 0.1 % to 3 % of exposure.', P2['P6'], f'{pct(S2["share_of_exposure"], 2)} %.'),
    ('P7', 'The median news episode lasts 1 to 30 days.', P2['P7'], f'{S2["news_median_days"]:.1f} days.'),
    ('P8', 'The longest episode exceeds a year.', P2['P8'], f'{S2["longest"]["hours"] / 8766:.1f} years ({S2["longest"]["zone"]}).'),
    ('P9', 'News hours since 2017 are under 10 % of all news hours.', P2['P9'], f'{pct(S2["news_hours_2017_on"] / BK["news"])} %.'),
    ('P10', 'At least 90 % of hours wrong are wrong by exactly one hour.', P2['P10'], f'{pct(S2["share_one_hour"])} %; {pct(S2["error_hours_by_seconds"]["7200"] / S2["zone_hours_wrong"])} % by two hours, and {n(round(S2["error_hours_by_seconds"]["82800"]))} hours by twenty-three.'),
    ('P11', 'The zdump check holds for at least 11 of 12.', C2['P11'], f'{C2["holds"]} of {C2["n"]}; in the twelfth zdump returned no reading inside its range (the file has no change after 1969), and read without a range it agrees.'),
]
plist2 = ''.join(f'<li><b>{k}</b> {html.escape(t)} — {"held" if ok else "failed"}: {html.escape(r)}</li>' for k, t, ok, r in PRED2)
held2 = sum(1 for p in PRED2 if p[2])

P3 = S3['predictions']
PRED3 = [
    ('P1', 'Inside check: 505 episodes, their hours summing to session 2\'s 918,348.3.', P3['P1'], f"{S3['episodes']} episodes, {n(round(S3['hours']))} hours (a check, not a prediction)"),
    ('P2', 'Corrected by 60 to 160 distinct releases.', P3['P2'], f"{S3['distinct_corr']} releases"),
    ('P3', 'The release correcting the most hours is dated 2014 or later.', P3['P3'], f"{S3['top_corr']['release']} ({S3['top_corr']['date']}), {n(round(S3['top_corr']['hours']))} hours; weak, as registered"),
    ('P4', 'The hours-weighted median lag exceeds five years.', P3['P4'], f"{S3['median_lag_days_weighted']:,.0f} days ({S3['median_lag_days_weighted'] / 365.25:.1f} years)"),
    ('P5', 'Under 15 % of wrong hours set right within 90 days.', P3['P5'], f"{100 * S3['share_within_90d']:.1f} %"),
    ('P6', 'At least 25 regions with episodes of two or more kinds.', P3['P6'], f"{S3['regions_multi_kind']} of {S3['regions']}"),
    ('P7', 'The hidden curve peaks before 2010.', P3['P7'], f"it peaks on {time.strftime('%Y-%m-%d', time.gmtime(S3['hidden_max']['date']))} at {n(round(S3['hidden_max']['hours']))} hours"),
    ('P8', 'Hidden on 2016-01-01 exceeds 300,000 hours.', P3['P8'], f"{n(round(S3['hidden_2016']))} hours"),
    ('P9', 'Hidden at the end is zero by construction; on 2026-01-01 under 1,000 hours.', P3['P9'], f"{n(round(S3['hidden_2026']))} hours on 2026-01-01 (Europe/Chisinau's clock changes 2022-2025, set right by 2026a)"),
    ('P10', 'The work passes render-check.js at 1440 and 390 px.', True, 'held'),
    ('P11', 'The correction re-read with zdump: at least 7 of 8.', C3['P11'], f"{C3['holds']} of 8 as registered; the eighth failed on an empty directory left by this session's own failed first run, and the unchanged re-run gave {C3b['holds']} of 8 (check3b.json)"),
]
plist3 = ''.join(f'<li><b>{k}</b> {html.escape(t)} — {"held" if ok else "failed"}: {html.escape(r)}</li>' for k, t, ok, r in PRED3)
held3 = sum(1 for p in PRED3 if p[2])
LG = S2['longest']
yrs = lambda h: h / 8766
top3 = zs[:3]

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Notice</title><link rel="icon" href="data:,">
<meta name="description" content="Every change of a region's clock since 1997, and how many days before or after it took effect the time-zone database that phones and servers read first carried it.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a64;--line:#d9d6cc;--a:#3b5f86;--ok:#9aa7b4;--sh:#c99a2e;--nw:#b23b2e;--rt:#e0916e;--pa:#7b7a73}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--a:#7fa9d6;--ok:#5d6b78;--sh:#e2b44f;--nw:#ff6b5a;--rt:#e0916e;--pa:#8f8d84}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--a:#7fa9d6;--ok:#5d6b78;--sh:#e2b44f;--nw:#ff6b5a;--rt:#e0916e;--pa:#8f8d84}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}
main{{max-width:1000px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:2rem;margin:.2em 0}}h2{{font-size:1.2rem;margin-top:2.2em}}
.mut{{color:var(--mut)}}.sm{{font:13px/1.45 system-ui,sans-serif}}a{{color:var(--a)}}.big{{font-size:1.25rem}}
svg.ch{{width:100%;height:auto;display:block;margin:1em 0}}svg.ch .ok{{fill:var(--ok)}}svg.ch .sh{{fill:var(--sh)}}svg.ch .nw{{fill:var(--nw)}}
svg.ch .rt{{fill:var(--rt)}}svg.ch .pa{{fill:var(--pa)}}svg.ch .ax{{stroke:var(--line)}}svg.ch .z{{stroke:var(--fg);stroke-width:1.5}}
svg.ch .yr{{font:15px system-ui,sans-serif;fill:var(--mut)}}svg.ch .lb{{font-size:9px}}
.key span{{display:inline-block;width:.9em;height:.9em;border-radius:50%;margin:0 .3em 0 .9em;vertical-align:-.1em}}
.sc{{overflow-x:auto}}.sc svg.ch{{min-width:600px}}ul.pr{{font:14px/1.5 system-ui,sans-serif;padding-left:1.2em}}
table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
.conn{{font:13px/1.45 system-ui,sans-serif;color:var(--mut)}}
</style></head><body><main>
<p class="sm mut">Project 23, sessions 1 and 2 · 7 and 9 November 2026 · open; no work before session 3 · data: IANA Time Zone Database (public domain)</p>
<h1>Notice</h1>
<p class="big">When a government moves the clocks, almost every phone and server learns of it from one file, kept by volunteers: the
time-zone database. Across thirty years of its releases, <b>{nw}</b> changes of a region's clock reached it only after the clocks had
already moved — and until a release came, software that relied on it showed the old hour. Since 2020, <b>{recent_nw}</b>. Counted in
hours (section 7), the file's newest release showed some region a wrong hour for <b>{n(round(S2["zone_hours_wrong"]))}</b> region-hours
since 1997 — four fifths of them only found wrong years later.</p>
{fig1}
<p class="sm key"><span style="background:var(--nw)"></span>arrived after the clocks moved, while the database still showed the old
hour <span style="background:var(--rt)"></span>arrived after, but only re-timed a change the database already had
<span style="background:var(--sh)"></span>arrived less than 30 days ahead <span style="background:var(--ok)"></span>30 days to a year ahead
· {n(n_dots)} changes, 1997-2026, each at the date it took effect and the days between that and its first release (hover a dot). Changes
known more than a year ahead (most of them: routine daylight-saving rules) are not drawn; nor are corrections that came more than a year
late. Exploratory reading (see 5).</p>

<h2 id="s1">1. What is read</h2>
<p>The tz database records, for about three hundred regions, the offset of local time from universal time and every change of it, past
and announced. IANA keeps each release since 1993. This study compiles every release with the same compiler, reads every change of
offset from 1997 to today that the newest release ({S["newest"]}, {S["release_dates"][S["newest"]][0]}) records — {n(S["final_transitions"])}
changes in {S["zones_newest"]} regions — and finds the first release that carried each one, to the second and the offset. The release's
date, from the database's own log, against the day the clocks moved, is the notice the world's software had.</p>
<p class="conn">Connects to 2 and 5.</p>

<h2 id="s2">2. Late</h2>
<p>Most changes are known years ahead: a daylight-saving rule, once made, predicts itself. The median change was first carried
<b>{S["median_lead_days"] / 365.25:.1f} years</b> before it happened. The tail is the finding. In the exploratory run (all releases from
1996h), {n(E["core"])} changes could be timed; <b>{E["late"]}</b> first appeared after they had taken effect, and <b>{B["under_30_days"]}</b>
more less than thirty days before. The late ones are of three kinds:</p>
<ul class="pr"><li><b>{nw}</b> were news arriving late: on the day the clocks moved, the database still had the old offset.</li>
<li><b>{kc.get("news/retimed", 0)}</b> re-timed a change already carried (the database had the right offset by then, at a slightly different
instant).</li><li><b>{kc.get("past/retimed", 0) + kc.get("past/new_offset", 0)}</b> came more than a year late: the record correcting its
past, not news. The latest correction reached back {E["max_late_days"] / 365.25:.0f} years.</li></ul>
<p>Grouped by release and date, the late and short-notice changes form {len(B["events_late_or_under_30"])} events, {ev_late} of them late.</p>
{table}
<p class="conn">Connects to 3 (fewer, later) and 4 (the check that found the second kind).</p>

<h2 id="s3">3. Fewer late, still short</h2>
<p>The late arrivals thin out: {sum(1 for r in K["rows"] if r["kind"] == "news/new_offset" and time.gmtime(r["t"]).tm_year < 2005)} news
arrivals in 1997-2004, {recent_nw} since 2020, none in 2024-2026 so far. Short notice does not thin out in the same way: a change carried
only days ahead recurs to the last years (in this reading most often for Gaza and Hebron: eight events).
(Exploratory: found after the registered count, <a href="explore1b.json">explore1b.json</a>, <a href="explore1c.json">explore1c.json</a>.)</p>
<p class="conn">Connects to 2.</p>

<h2 id="s4">4. The check</h2>
<p>A second tool (zdump, not this study's reader) looked at twelve late changes drawn at random, in the release before each one's first
appearance and in that appearance. It confirmed {C["holds"]} of {C["n"]}. In the other four, the earlier release already showed the new
offset at that instant: the change had been carried, at a slightly different moment, and the "late" release only moved it. The
registered count did not separate these; the exploratory reading in 2 does. (<a href="check1.py">check1.py</a>,
<a href="check1.json">check1.json</a>.)</p>
<p class="conn">Connects to 2 (the second kind).</p>

<h2 id="s5">5. What this cannot tell</h2>
<p>When a government decided, and when a device received a release: neither is in this material. The release date is the day the file
was published; a phone has it later, so its notice is shorter than what is measured here. The registered count compiled only the
releases from 2000f on: the 61 older ones failed, because their data ask the compiler to run a helper (<code>yearistype</code>, for
rules in even and odd years) that today's compiler has dropped. Every change before 2000f's date that the earlier releases had carried
therefore looked late; that is why the registered peak year is 2000. The exploratory run supplied a two-line helper written for this
study (<a href="helper/yearistype">helper/yearistype</a>) and compiled {E["releases_compiled"]} releases from 1996h on; the 23 still
failing are older than the window. Whether the database is right about the world is not tested. Nearest neighbours:
<a href="NEIGHBOURS.md">NEIGHBOURS.md</a>.</p>

<h2 id="s6">6. Predictions, registered before the count</h2>
<p class="sm">Pushed with the selection (<a href="SELECTION.md">SELECTION.md</a>) before any release was opened; the count was run once
(<a href="count1.py">count1.py</a>, <a href="session1.json">session1.json</a>). {held} of 11 held.</p>
<ul class="pr">{plist}</ul>

<h2 id="s7">7. The hours shown wrong (session 2)</h2>
<p>Session 2 counts in hours instead of changes. On every day since 1996 one release was the newest: the file anyone updating
faithfully had. For every region and every hour, that file's offset is set against what the newest release of all ({S2["newest"]}) says
the offset was. Where they differ, the file showed the present wrong. In total: <b>{n(round(S2["zone_hours_wrong"]))} region-hours</b> in
{S2["zones_with_episode"]} of {S2["zones_final"]} regions, {pct(S2["share_of_exposure"], 2)} % of all the region-hours the file covered, in
{S2["episodes_total"]} stretches of three kinds:</p>
<ul class="pr"><li><span class="key"><span style="background:var(--nw);margin-left:0"></span></span><b>{n(round(BK["news"]))}</b> hours
({EPn["news"]} stretches, {ZK["news"]} regions): news that came after the clocks moved; the median stretch lasted
{S2["news_median_days"]:.0f} days.</li>
<li><span class="key"><span style="background:var(--rt);margin-left:0"></span></span><b>{n(round(BK["retimed"]))}</b> hours
({EPn["retimed"]} stretches): a change the file had, at the wrong moment — within a month of the right one.</li>
<li><span class="key"><span style="background:var(--pa);margin-left:0"></span></span><b>{n(round(BK["past"]))}</b> hours
({EPn["past"]} stretches, {ZK["past"]} regions): hours that were found wrong more than a year after they were lived — the record
rewriting its past.</li></ul>
{fig2}
<p class="sm">One row per region, longest total first; each bar a stretch in which the newest release showed that region an hour the
record now says was wrong (hover for the release, the two offsets at the stretch's start and the correcting release). The longest:
{html.escape(LG["zone"])}, {yrs(LG["hours"]):.1f} years from {time.strftime("%Y", time.gmtime(LG["t0"]))} to
{time.strftime("%Y", time.gmtime(LG["t1"]))}, wrong by one hour in all but {n(round(LG["hours"] - LG["err_hours"]["3600"]))} of its hours:
the file showed the station UT+6 h where the record now says +7 h (read with zdump on releases 2010a and 2026f); in its first weeks,
release 2001a had put it on Moscow time. Next: {html.escape(top3[1])} and
{html.escape(top3[2])}. Bars starting at 1997 began earlier; the count starts there.</p>
<p>News arriving late thins out as in section 3: {pct(S2["news_hours_2017_on"] / BK["news"])} % of its hours fall after 2016. The hours
found wrong years later do not thin in the same way through 2022: they are where the record learned late what a place had done, often
a remote one (an Antarctic station, an atoll, a province). Hours after late 2025 cannot be counted in this kind yet: a year has not
passed.
(<a href="SESSION2.md">SESSION2.md</a>, <a href="count2.py">count2.py</a>, <a href="session2.json">session2.json</a>,
<a href="check2.json">check2.json</a>.) {held2} of 11 predictions held:</p>
<ul class="pr">{plist2}</ul>
<p class="conn">Connects to 2 (the three kinds, now weighed) and 5 (what this cannot tell: no device and no population is in this
material; every hour here is what a perfectly updated machine would have shown).</p>

<h2 id="s8">8. When the file found out (session 3)</h2>
<p>Session 3 set every stretch of section 7 against the day a release first set it right, and counted, at every week since 1997, the
hours already lived that the file was wrong about without yet knowing it. Half of the wrong hours belong to stretches set right more than
{S3['median_lag_days_weighted'] / 365.25:.1f} years after they began; {100 * S3['share_within_90d']:.1f} % within ninety days. {S3['distinct_corr']}
releases did the correcting. The hidden hours do not fall slowly: they rose to {n(round(S3['hidden_max']['hours']))} on 1 August 2012 and were
cut by single releases — 2012e (Pacific/Fakaofo, 136,608 hours) the next day, 2014f (Asia/Urumqi, 154,200), 2023d (Antarctica/Vostok and
Casey, 204,326). By the rule registered before the count, this is the work:
<a href="../../works/the-hours-shown-wrong/"><i>The Hours Shown Wrong</i></a>.
(<a href="SESSION3.md">SESSION3.md</a>, <a href="count3.py">count3.py</a>, <a href="session3.json">session3.json</a>,
<a href="check3.json">check3.json</a>, <a href="check3b.json">check3b.json</a>.) {held3} of 11 predictions held:</p>
<ul class="pr">{plist3}</ul>
<p class="conn">Connects to 7 (the same 505 stretches, now placed by when they were found) and 5 (the newest release is the only judge;
what it is still wrong about is not here).</p>

<p class="sm mut">Data: IANA Time Zone Database, every archived <code>tzdata</code> release, <code>https://data.iana.org/time-zones/releases/</code>,
fetched 7 November 2026; its files state "This file is in the public domain". Counts and figures derived by Remainder; no contributor is
named or counted.</p>
</main></body></html>
'''
open('index.html', 'w').write(page)
print('ok', len(page), n_dots)
