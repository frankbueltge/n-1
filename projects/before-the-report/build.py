"""Project 25: build the study page index.html from session1.json, check1.json, explore1.json (stdlib only).
Usage: python3 -I build.py   (run in projects/before-the-report/)"""
import json, html
S = json.load(open('session1.json'))
C = json.load(open('check1.json'))
E = json.load(open('explore1.json'))
S2 = json.load(open('session2.json'))
C2 = json.load(open('check2.json'))
n = lambda x: f'{x:,}'
fmt = lambda x: f'{x:g}'
Y = E['event_median_W_by_year']
years = sorted(Y['drug'])

def panel(centre, x0, w, h, ymax=160):
    T, B, L = 30, 34, 34
    els = [f'<text class="pt" x="{x0 + L}" y="16">{ {"drug": "Drugs", "food": "Food", "device": "Devices"}[centre]}</text>']
    sx = lambda i: x0 + L + i * (w - L - 8) / (len(years) - 1)
    sy = lambda v: T + (1 - min(v, ymax) / ymax) * (h - T - B)
    for v in (0, 50, 100, 150):
        els.append(f'<line class="ax" x1="{x0 + L}" x2="{x0 + w - 8}" y1="{sy(v):.1f}" y2="{sy(v):.1f}"/>'
                   f'<text class="yr" x="{x0 + L - 5}" y="{sy(v) + 4:.1f}" text-anchor="end">{v}</text>')
    for i, y in enumerate(years):
        if y in ('2012', '2019', '2026'):
            els.append(f'<text class="yr" x="{sx(i):.1f}" y="{h - B + 18}" text-anchor="{"end" if y == "2026" else "start" if y == "2012" else "middle"}">{y}</text>')
    for k, cls in (('Class II', 'c2'), ('Class I', 'c1')):
        pts = [(sx(i), sy(Y[centre][y][k][1]), y, Y[centre][y][k]) for i, y in enumerate(years) if Y[centre][y][k][1] is not None]
        els.append(f'<polyline class="{cls}" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b, _, _ in pts)}"/>')
        for a, b, y, (cnt, m) in pts:
            els.append(f'<circle class="{cls}" cx="{a:.1f}" cy="{b:.1f}" r="3.2"><title>{centre}, {k}, reported {y}: '
                       f'{n(cnt)} recalls, median wait {fmt(m)} days</title></circle>')
    return ''.join(els)

W, H = 960, 300
pw = W / 3
fig = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ft"><title id="ft">Three small line charts, '
       f'2012 to 2026: median days from a recall\'s start to the FDA enforcement report, per report year, for the gravest class (Class I, '
       f'red) and Class II (grey). For drugs the red line lies above the grey in all fifteen years; for food and devices the lines cross.</title>'
       + panel('drug', 0, pw, H) + panel('food', pw, pw, H) + panel('device', 2 * pw, pw, H) + '</svg></div>')

ev = E['event_median_W']
tab = ''.join(f'<tr><td style="text-align:left">{ {"food": "Food", "drug": "Drugs", "device": "Devices"}[c]}</td>' + ''.join(
    f'<td>{fmt(ev[c][k]["median_W"])}</td>' for k in ('Class I', 'Class II', 'Class III')) + ''.join(
    f'<td>{fmt(ev[c][k]["median_C"])}</td>' for k in ('Class I', 'Class II', 'Class III')) +
    f'<td>{fmt(ev[c]["Class I"]["median_W_minus_C"])}–{fmt(max(ev[c][k]["median_W_minus_C"] for k in ("Class I","Class II","Class III")))}</td></tr>'
    for c in ('drug', 'food', 'device'))
cnt = '; '.join({"drug": "drugs ", "food": "food ", "device": "devices "}[c] + ' / '.join(n(ev[c][k]["events"]) for k in ('Class I', 'Class II', 'Class III')) for c in ('drug', 'food', 'device'))
yrs_longer = {c: sum(1 for y in years if Y[c][y]['Class I'][1] is not None and Y[c][y]['Class II'][1] is not None
                     and Y[c][y]['Class I'][1] > Y[c][y]['Class II'][1]) for c in ('drug', 'food', 'device')}
a, bc = S['all'], S['by_class']
pred = [
    ('1', 'median wait between 30 and 120 days', f'{fmt(a["median"])} days', True),
    ('2', 'Class I median lower than Class II', f'{fmt(bc["Class I"]["median"])} and {fmt(bc["Class II"]["median"])}', True),
    ('3', 'more than 10 % wait over a year', f'{100 * a["share_over365"]:.1f} %', False),
    ('4', 'devices have the longest median of the three centres', ', '.join(f'{c} {fmt(S["by_centre"][c]["median"])}' for c in ("food", "drug", "device")), True),
    ('5', 'fewer than 1 % reported before begun', f'{n(a["neg"])} records', True),
    ('6', '2025 lower median than 2013', f'{fmt(S["by_report_year"]["2025"]["median"])} and {fmt(S["by_report_year"]["2013"]["median"])}', True),
    ('7', 'Class I between 5 % and 20 % of records', f'{100 * S["class_counts"]["Class I"] / S["records"]:.1f} %', False),
    ('8', 'event median within 10 days of record median', f'{fmt(S["events"]["W"]["median"])} and {fmt(a["median"])}', True),
    ('9', 'earliest report in 2012', S['report_date_range'][0], True),
    ('10', 'classification sooner than report (medians)', f'{fmt(S["C_all"]["median"])} and {fmt(a["median"])}', True),
]
rows = ''.join(f'<tr><td>P{p}</td><td style="text-align:left">{html.escape(q)}</td><td>{html.escape(r)}</td><td>{"held" if h else "<b>failed</b>"}</td></tr>' for p, q, r, h in pred)
big = E['largest_drug_class1_event']

B2 = S2['by_centre_class']
GR = [('public', 'gp', 'press release first'), ('ambiguous', 'ga', 'not said (a form\'s list, or “other”)'),
      ('consignees', 'gc', 'customers only: the register may be the first public word'), ('unrecorded', 'gu', 'no method recorded')]
rws = [(c, k) for c in ('drug', 'food', 'device') for k in ('Class I', 'Class II', 'Class III')]
W2, RH, LX, BW = 960, 30, 150, 600
bars = []
for i, (c, k) in enumerate(rws):
    y = 34 + i * RH + (12 if i >= 3 else 0) + (12 if i >= 6 else 0)
    b = B2[c][k]; tot = b['events']; x = LX
    bars.append(f'<text class="yr" x="{LX - 8}" y="{y + 15}" text-anchor="end">{ {"drug": "Drugs", "food": "Food", "device": "Devices"}[c] if k == "Class I" else ""} {k}</text>')
    for g, cls, lab in GR:
        v = b['groups'][g]; wd = BW * v / tot
        if v:
            bars.append(f'<rect class="{cls}" x="{x:.1f}" y="{y}" width="{wd:.1f}" height="{RH - 8}"><title>{c}, {k}: {n(v)} of {n(tot)} recall events, {lab}</title></rect>')
        x += wd
    mw = b['W']['consignees'].get('median')
    bars.append(f'<text class="yr" x="{LX + BW + 10}" y="{y + 15}">{n(tot)} · {round(100 * b["groups"]["public"] / tot, 1):g} % · {fmt(mw)} d</text>')
leg = ''.join(f'<span class="lg"><i class="{cls}"></i>{html.escape(lab)}</span>' for g, cls, lab in GR)
fig2 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W2} {34 + 9 * RH + 30}" role="img" aria-labelledby="f2"><title id="f2">Nine stacked bars, '
        f'one per centre and class: how each recall event was first made known by the firm. Press release first (blue) is largest for drug '
        f'Class I, about a third; for most rows the dark segment, customers only, is the largest.</title>'
        f'<text class="yr" x="{LX + BW + 10}" y="20">events · press release · days*</text>' + ''.join(bars) + '</svg></div>'
        f'<p class="sm">{leg}</p>')
eg = S2['event_groups']; ne = S2['events']; rf = S2['register_first_all']
dc1, dc2 = B2['drug']['Class I'], B2['drug']['Class II']
yd = S2['by_year_drug_consignees']
p2 = [('1', 'fewer than 15 % of events begin with a press release', f'{100 * S2["event_group_share"]["public"]:.1f} %', True),
      ('2', 'press release more often in Class I than Class II, in each centre', ', '.join(f'{c} {100 * B2[c]["Class I"]["share_public"]:.1f} / {100 * B2[c]["Class II"]["share_public"]:.1f} %' for c in ('food', 'drug', 'device')), True),
      ('3', 'among Class I, food announces most often', f'drugs {100 * dc1["share_public"]:.1f} %, food {100 * B2["food"]["Class I"]["share_public"]:.1f} %', False),
      ('4', 'customers-only is more than half of all events', f'{100 * S2["event_group_share"]["consignees"]:.1f} %', True),
      ('5', 'drug Class I: customers-only waits longer than press-release-first', f'{fmt(dc1["W"]["consignees"]["median"])} and {fmt(dc1["W"]["public"]["median"])} days', False),
      ('6', 'drug Class I customers-only median over 50 days', f'{fmt(dc1["W"]["consignees"]["median"])} days', False),
      ('7', 'within customers-only, drug Class I longer than Class II', f'{fmt(dc1["W"]["consignees"]["median"])} and {fmt(dc2["W"]["consignees"]["median"])} days', True),
      ('8', 'at least 100 drug Class I customers-only events over 90 days', n(dc1['W']['consignees']['over90']), True),
      ('9', '“Letter” the most frequent notice', f'{S2["top_strings"][0][0]} ({n(S2["top_strings"][0][1])} entries)', True),
      ('10', 'fewer than 1 % of events record no method', f'{100 * S2["event_group_share"]["unrecorded"]:.1f} %', False)]
rows2 = ''.join(f'<tr><td>P{p}</td><td style="text-align:left">{html.escape(q)}</td><td>{html.escape(r)}</td><td>{"held" if h else "<b>failed</b>"}</td></tr>' for p, q, r, h in p2)
yl = sum(1 for y in yd if yd[y]['Class I'] is not None and yd[y]['Class II'] is not None and yd[y]['Class I'] > yd[y]['Class II'])
sec5 = f'''
<h2 id="s2">5. Whose word came first</h2>
<p class="sm mut">Session 2 · 19 November 2026 · files of 18 November 2026, the same {n(S2["records"])} entries.</p>
<p>Each entry also says how the firm <i>first</i> made the recall known. Of <b>{n(ne)}</b> recall events, <b>{n(eg["public"])}</b>
({100 * S2["event_group_share"]["public"]:.1f} %) began with a press release. In <b>{n(eg["consignees"])}</b> ({100 * S2["event_group_share"]["consignees"]:.1f} %)
the first notice went only to those who held or passed on the product — by letter, telephone, e-mail, visit or fax. For these the
register may have been the first public word, and it came a median <b>{fmt(rf["median"])} days</b> after the recall began; {n(rf["over365"])}
waited more than a year (two of them the impossible start dates of section 2). {n(eg["ambiguous"])} events cannot say: their entries carry a form's own sentence, “Two or more of the
following: Email, Fax, Letter, Press Release, Telephone, Visit”, which lists every method and marks none, or the word “Other”. In food
that is {n(sum(B2["food"][k]["groups"]["ambiguous"] for k in ("Class I", "Class II", "Class III")))} of {n(sum(B2["food"][k]["events"] for k in ("Class I", "Class II", "Class III")))} classed events. {n(eg["unrecorded"])} record no method.</p>
{fig2}
<p class="sm mut">Each bar is all recall events of one centre and class, by how the firm first made the recall known. Right: events, the share
that began with a press release, and the median days to the register for those whose first notice went to customers only. Hover a segment
for the count. *Median days to the register, customers-only events.</p>
<p>The gravest recalls are the most often announced: {n(dc1["groups"]["public"])} of {n(dc1["events"])} Class I drug recalls began with a
press release, against {100 * dc2["share_public"]:.1f} % of Class II. <b>But announcing does not hurry the register.</b> Class I drug recalls
first announced to the public were listed a median {fmt(dc1["W"]["public"]["median"])} days after they began; those first told to customers
only, {fmt(dc1["W"]["consignees"]["median"])}. And where the register may be the first public word, the gravest drug recalls still wait
longer than the lesser ones — {fmt(dc1["W"]["consignees"]["median"])} days against {fmt(dc2["W"]["consignees"]["median"])}, and in
{yl} of the {len(yd)} report years (not registered: from {fmt(yd["2012"]["Class I"])} against {fmt(yd["2012"]["Class II"])} days in 2012
to {fmt(yd["2026"]["Class I"])} against {fmt(yd["2026"]["Class II"])} in 2026). The longest: a Class I drug recall first made known by
telephone and listed {n(S2["longest_register_first_drug_class1"][0]["W"])} days later (event {S2["longest_register_first_drug_class1"][0]["event_id"]}, reported 2012).</p>
<p><b>What this cannot say.</b> The field holds only the first method. A firm may have announced the recall later; and for devices the FDA has
issued “Early Alerts” for likely Class I recalls since a pilot begun in November 2024, which a law firm's review puts at 1 to 3 weeks after
the first customer letters (<a href="https://www.thefdalawblog.com/2025/10/how-early-is-too-early-cdrh-expands-early-alert-communications-for-potentially-high-risk-device-recalls/">FDA
Law Blog, 1 October 2025</a>). Neither shows in this register.
The customers-only count is therefore an upper bound on the recalls for which the register was the first public word.</p>
<p>Ten predictions were pushed before the files were downloaded. Six held. Two definitions were decided after reading the field's
values and before the count: “N/A” counts as no method, “Other” as not said (<a href="JOURNAL.md">JOURNAL.md</a>, 02:05).</p>
<div class="tw"><table><tr><th></th><th style="text-align:left">registered</th><th>found</th><th></th></tr>{rows2}</table></div>
<p class="sm mut">Check: {C2["held"]} of {C2["of"]} events (twelve drawn at random, four per centre, and the three longest customers-only
Class I drug waits) recomputed with <code>jq</code> and the system's <code>date</code>; the entries whose first notice is exactly “Press
Release” recounted by <code>jq</code> alone per centre, agreeing. The random draw held no press-release event; three were checked
afterwards by hand, 3 of 3 (not registered). Count <a href="count2.py">count2.py</a> → <a href="session2.json">session2.json</a>;
check <a href="check2.json">check2.json</a>; registration <a href="SESSION2.md">SESSION2.md</a>.</p>
'''

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Before the Report</title><link rel="icon" href="data:,">
<meta name="description" content="Every recall in the FDA's open enforcement files, 2012 to 2026, and how long the public register trails the day the recall began.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a64;--line:#d9d6cc;--a:#3b5f86;--c2:#8f8d85;--c1:#b23b2e}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--a:#7fa9d6;--c2:#8a887f;--c1:#ff6b5a}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--a:#7fa9d6;--c2:#8a887f;--c1:#ff6b5a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}
main{{max-width:1000px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:2rem;margin:.2em 0}}h2{{font-size:1.2rem;margin-top:2.2em}}
.mut{{color:var(--mut)}}.sm{{font:13px/1.45 system-ui,sans-serif}}a{{color:var(--a)}}.big{{font-size:1.25rem}}
svg.ch{{width:100%;height:auto;display:block;margin:1em 0}}svg.ch .ax{{stroke:var(--line)}}svg.ch .yr{{font:12px system-ui,sans-serif;fill:var(--mut)}}
svg.ch .pt{{font:600 14px system-ui,sans-serif;fill:var(--fg)}}svg.ch polyline{{fill:none;stroke-width:2.5}}
svg.ch polyline.c1{{stroke:var(--c1)}}svg.ch polyline.c2{{stroke:var(--c2)}}svg.ch circle.c1{{fill:var(--c1)}}svg.ch circle.c2{{fill:var(--c2)}}
.sc{{overflow-x:auto}}.sc svg.ch{{min-width:640px}}.k1{{color:var(--c1);font-weight:600}}.k2{{color:var(--c2);font-weight:600}}
.tw{{overflow-x:auto}}svg.ch rect.gp,.lg i.gp{{fill:var(--a);background:var(--a)}}svg.ch rect.ga,.lg i.ga{{fill:var(--c2);background:var(--c2);opacity:.55}}svg.ch rect.gc,.lg i.gc{{fill:var(--fg);background:var(--fg);opacity:.82}}svg.ch rect.gu,.lg i.gu{{fill:var(--line);background:var(--line)}}.lg{{display:inline-block;margin-right:14px}}.lg i{{display:inline-block;width:11px;height:11px;margin-right:5px;vertical-align:-1px}}table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
</style></head><body><main>
<p class="sm mut">Project 25, sessions 1–2 · 18–19 November 2026 · open; no work before session 3 · data: U.S. Food and Drug Administration,
openFDA enforcement reports (food, drugs, devices), export of 17 November 2026, CC0 · this page CC BY 4.0 · Remainder</p>
<h1>Before the Report</h1>
<p class="big">When a firm calls back a food, a drug or a medical device, the FDA classes the danger and lists the recall in its weekly
enforcement report. Across <b>{n(S["records"])}</b> listed products since 2012, the list comes a median <b>{fmt(a["median"])} days</b> after
the recall began. For drugs, the gravest recalls — <span class="k1">Class I</span>, products that “predictably could cause serious
health problems or death” — wait <b>longer</b> than the <span class="k2">Class II</span> ones, in <b>every one of the fifteen
years</b>.</p>
{fig}
<p class="sm mut">Median days from the day the firm first began notifying of the recall to the day the FDA's enforcement report listed it,
per recall (all products of one recall event together), by the year of the report. Red: Class I. Grey: Class II. Hover a point for the
count. Points above 160 days are drawn at the top edge; the table below has the medians over all years.</p>

<h2>1. What is read</h2>
<p>The FDA publishes every enforcement report entry since June 2012 as three open files, one each for food, drugs and devices. Each entry
is one product in a recall and carries three dates: the day the firm began notifying the public or its customers, the day the FDA
classified the hazard, and the day the report listed it. This study counts the days between them, for every entry. A recall event
(one firm, one problem, often many products) is counted once, at its earliest dates and its gravest class.</p>

<h2>2. What was found</h2>
<div class="tw"><table><tr><th></th><th colspan="3">days to the report (median)</th><th colspan="3">days to classification (median)</th><th>classification to report</th></tr>
<tr><th></th><th>Class I</th><th>II</th><th>III</th><th>Class I</th><th>II</th><th>III</th><th></th></tr>{tab}</table></div>
<p class="sm mut">Recall events counted, Class I / II / III: {cnt}.</p>
<p>For food the three classes wait alike (the gravest was the longer in {yrs_longer["food"]} of 15 years); for devices the gravest is
usually the quicker ({yrs_longer["device"]} of 15). For drugs Class I was the longer in {yrs_longer["drug"]} of 15. The whole difference
lies before the FDA's classification: once a recall is classed, every centre and every class is listed a median 7 or 8 days later — the
weekly rhythm of the report. Between 2013 and 2016 the gravest drug recalls waited a median of 118 to 149 days; since 2018 the gap is
smaller (26 to 45.5 days against 22 to 27.5) but has not closed.</p>
<p>One drug recall shows why products are the wrong unit. A single event of {n(big["records"])} homeopathic products, recalled for microbial
contamination, began on 20 July 2018 and was listed on 20 March 2019, {big["W"]} days later; it alone is a quarter of all Class I drug
entries. Its first notice was a press release. <b>So the wait measured here is the register's wait, not the public's:</b> a firm may
have told the public long before the list did. How often the register is the first public word — and how long those recalls wait — is
<a href="#s2">section 5</a>.</p>
<p>The register also holds dates that cannot be true: a food recall begun in the year 212 (F-0880-2013, a wait of 657,484 days) and a
device recall begun in 1930 (Z-0139-2014). Six device entries were listed before they began. They are counted as found and move no
median.</p>

<h2>3. What was predicted</h2>
<p>Ten predictions were pushed before the files were downloaded. Eight held.</p>
<div class="tw"><table><tr><th></th><th style="text-align:left">registered</th><th>found</th><th></th></tr>{rows}</table></div>
<p class="sm mut">Check: {C["held"]} of {C["of"]} entries (twelve drawn at random, four per centre, and the three longest waits) recomputed
with a second tool (<code>jq</code> and the system's <code>date</code>); the counts of entries and of negative waits per centre recomputed by
<code>jq</code> alone, all agreeing. No firm is named here; entries are cited by recall number.</p>

<h2>4. Who is affected</h2>
<p>People who ate, took or were treated with a recalled product, and the public that reads of recalls in the FDA's report. What waits is
the public record of a danger the firm has already acknowledged.</p>
{sec5}
<p class="sm mut">Sources: openFDA download files (sha256 and record in <a href="JOURNAL.md">JOURNAL.md</a>); registration
<a href="SELECTION.md">SELECTION.md</a>; count <a href="count1.py">count1.py</a> → <a href="session1.json">session1.json</a>; exploration
<a href="explore1.py">explore1.py</a> → <a href="explore1.json">explore1.json</a> (not registered); check <a href="check1.json">check1.json</a>;
neighbours <a href="NEIGHBOURS.md">NEIGHBOURS.md</a>. The weekly report and its rule: “All recalls monitored by FDA are included in the
Enforcement Report once they are classified” (<a href="https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/enforcement-reports">FDA,
Enforcement Reports</a>, read 18 November 2026; the same page says some recalls are listed while their classification is pending — five
entries in these files are “Not Yet Classified”). The FDA's own caution stands with its data: “Do not rely on openFDA to make
decisions regarding medical care.”</p>
</main></body></html>
'''
open('index.html', 'w').write(page)
print(len(page), yrs_longer)
