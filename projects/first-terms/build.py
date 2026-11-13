"""Project 24: build the study page index.html from session1.json, check1.json, explore1.json (stdlib only).
Usage: python3 -I build.py   (run in projects/first-terms/)"""
import json, html

S = json.load(open('session1.json'))['summary']
C = json.load(open('check1.json'))
E = json.load(open('explore1.json'))
import gzip
S2 = json.load(open('session2.json'))
C2 = json.load(open('check2.json'))
F2 = json.load(open('explore2c.json'))
X2 = json.load(open('explore2.json'))
P2 = json.load(gzip.open('session2-per.json.gz', 'rt'))


def n(x):
    return f'{x:,}'


def pct(x, d=1):
    return f'{100 * x:.{d}f}'


# Figure 1: how many first terms each sequence needs; one bar per length 1..40, one for 41+, one for never parted
dist = {int(k): v for k, v in S['L_distribution'].items()}
bars = [(str(k), dist.get(k, 0), 'f') for k in range(1, 41)]
bars.append(('41+', sum(v for k, v in dist.items() if k > 40), 'f'))
bars.append(('never', S['never_parted'], 'np'))
W, H, L, T, B = 900, 376, 60, 16, 62
mx = max(v for _, v, _ in bars)
bw = (W - L - 10) / len(bars)
els = []
for v in (0, 20000, 40000, 60000):
    y = T + (1 - v / mx) * (H - T - B)
    els.append(f'<line class="ax" x1="{L}" x2="{W - 10}" y1="{y:.1f}" y2="{y:.1f}"/>'
               f'<text class="yr" x="{L - 6}" y="{y + 4:.1f}" text-anchor="end">{n(v)}</text>')
for i, (lab, v, cls) in enumerate(bars):
    x = L + i * bw
    h = v / mx * (H - T - B)
    word = 'term' if lab == '1' else 'terms'
    tip = (f'{n(v)} sequences are told apart from every other by their first {lab} {word}' if cls == 'f' and lab != '41+' else
           f'{n(v)} sequences need more than 40 first terms' if lab == '41+' else
           f'{n(v)} sequences are never told apart within the terms shown')
    els.append(f'<rect class="{cls}" x="{x + 1:.1f}" y="{H - B - h:.1f}" width="{bw - 2:.1f}" height="{h:.1f}"><title>{tip}</title></rect>')
    if lab in ('1', '6', '10', '20', '30', '41+', 'never'):
        dy = 18 if lab != 'never' else 34
        els.append(f'<text class="yr" x="{x + bw / 2:.1f}" y="{H - B + dy}" text-anchor="middle">{lab}</text>')
els.append(f'<text class="yr" x="{L + (W - L) / 2:.1f}" y="{H - 6}" text-anchor="middle">first terms needed before no other sequence begins the same way</text>')
fig1 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="f1t"><title id="f1t">Bar chart: for '
        f'{n(S["sequences"])} sequences, how many first terms each needs before no other sequence begins the same way. The peak is at '
        f'five terms; the median is {S["L_median"]}; {n(S["never_parted"])} are never told apart.</title>{"".join(els)}</svg></div>')

pred = [
    ('1', 'between 375,000 and 400,000 sequences', n(S['sequences']), False),
    ('2', 'median shown terms 25-60', f'{S["shown_terms_median"]:.0f}', True),
    ('3', 'median identifying length 6-9', f'{S["L_median"]}', True),
    ('4', 'under 10 % need three terms or fewer', f'{pct(S["L_le3_share"])} %', False),
    ('5', '5-20 % need more than twelve', f'{pct(S["L_gt12_share"])} %', True),
    ('6', '1-5 % never parted', f'{pct(S["never_parted_share"], 2)} %', True),
    ('7', 'twins at least half of the never parted', f'{n(S["twin"])} of {n(S["never_parted"])}', True),
    ('8', 'largest finite length at least 100', f'{S["L_max"]}', True),
    ('9', 'most shared six-term beginning is 1,2,3,4,5,6, by 1,000 or more', f'{S["top_prefix6"][0][0]} ({n(S["top_prefix6"][0][1])}); 1,2,3,4,5,6 third ({n(S["top_prefix6"][2][1])})', False),
    ('10', 'median length higher from A300000 than below A100000', f'{S["L_median_A300000_up"]} and {S["L_median_below_A100000"]:.0f}', False),
    ('11', 'grep check at least 17 of 18', f'{C["held"]} of {C["of"]}', True),
]
held = sum(1 for p in pred if p[3])
rows = ''.join(f'<tr><td>P{a}</td><td style="text-align:left">{html.escape(b)}</td><td>{html.escape(c)}</td><td>{"held" if d else "<b>failed</b>"}</td></tr>' for a, b, c, d in pred)
top = ''.join(f'<tr><td style="text-align:left"><code>{html.escape(k)}</code></td><td>{n(v)}</td></tr>' for k, v in S['top_prefix6'][:6])
big = E['largest_groups'][0]

# Session 2, figure 2: share of all sequences found alone by k terms, three ways (k = 1..40)
NS = len(P2)
def cum(col):
    c = [0] * 41
    for r in P2:
        v = r[col]
        if 0 < v <= 40:
            c[v] += 1
    out, t = [], 0
    for k in range(1, 41):
        t += c[k]; out.append(t / NS)
    return out
curves = [('M', cum(4), 'cm', 'the shortest run anywhere that no other sequence holds'),
          ('B', cum(3), 'cb', 'its first terms, typed into the search box'),
          ('L', cum(2), 'cl', 'its first terms, set against other beginnings (session 1)')]
W2, H2, L2, T2, B2 = 900, 380, 60, 16, 50
def X(k): return L2 + (k - 1) / 39 * (W2 - L2 - 20)
def Y(v): return T2 + (1 - v) * (H2 - T2 - B2)
e2 = []
for v in (0, .25, .5, .75, 1):
    e2.append(f'<line class="ax" x1="{L2}" x2="{W2 - 20}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text class="yr" x="{L2 - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{int(v * 100)} %</text>')
for k in (1, 6, 10, 20, 30, 40):
    e2.append(f'<text class="yr" x="{X(k):.1f}" y="{H2 - B2 + 18}" text-anchor="middle">{k}</text>')
e2.append(f'<text class="yr" x="{L2 + (W2 - L2) / 2:.1f}" y="{H2 - 6}" text-anchor="middle">numbers typed</text>')
for lab, ys, cls, desc in curves:
    pts = ' '.join(f'{X(k):.1f},{Y(v):.1f}' for k, v in zip(range(1, 41), ys))
    e2.append(f'<polyline class="{cls}" fill="none" points="{pts}"><title>{html.escape(desc)}</title></polyline>')
    for k in (1, 2, 6, 12):
        e2.append(f'<circle class="{cls}" cx="{X(k):.1f}" cy="{Y(ys[k - 1]):.1f}" r="4"><title>{pct(ys[k - 1])} % of all sequences are found alone by {k} number{"s" if k > 1 else ""}: {html.escape(desc)}</title></circle>')
    kx = {'M': 3, 'B': 9, 'L': 5}[lab]
    e2.append(f'<text class="yr {cls}t" x="{X(kx) + (-10 if lab == "M" else 10 if lab == "B" else -12):.1f}" y="{Y(ys[kx - 1]) + (4 if lab != "L" else -6):.1f}" text-anchor="{"end" if lab != "B" else "start"}" style="font-weight:bold">{lab}</text>')
fig2 = (f'<div class="sc"><svg class="ch" viewBox="0 0 {W2} {H2}" role="img" aria-labelledby="f2t"><title id="f2t">Three rising curves: '
        f'the share of {n(NS)} sequences found alone after k numbers, by the shortest run anywhere (M), by the first terms typed into the '
        f'search box (B), and by the first terms set against other beginnings (L).</title>{"".join(e2)}</svg></div>')
G = S2['signed']
def famrow(r):
    nm = html.escape(r['name'] if len(r['name']) <= 60 else r['name'][:58].rsplit(' ', 1)[0] + ' …')
    if r['held_by']:
        h = r['first_holders'][0]
        holder = html.escape(h[1] if len(h[1]) <= 70 else h[1][:68].rsplit(' ', 1)[0] + ' …') + ' (' + h[0] + ')' + (' and ' + str(r['held_by'] - 1) + ' more' if r['held_by'] > 1 else '')
        m = 'never'
    else:
        holder = '—'
        m = str(next(x for x in X2['famous'] if x['a'] == r['a'])['M']) + ' (terms 16-30)'
    return f'<tr><td style="text-align:left">{nm} ({r["a"]})</td><td>{r["shown"]}</td><td>{m}</td><td style="text-align:left">{holder}</td></tr>'
famous = ''.join(famrow(r) for r in F2)
pred2 = [
    ('1', 'between 401,214 and 401,700 sequences', n(G['sequences']), True),
    ('2', 'median B (the box, from the beginning) 7-10', f'{G["B_median"]}', False),
    ('3', '20-50 % have B greater than L', f'{pct(G["B_gt_L_share"])} %', True),
    ('4', 'median M (the shortest run) 3-5', f'{G["M_median"]}', False),
    ('5', 'at least half have M smaller than B', f'{pct(G["M_lt_B_share"])} %', True),
    ('6', '1.5-4 % never found alone', f'{pct(G["never_share"], 2)} %', True),
    ('7', 'fewer than half give one hit for their first six terms', f'{pct(G["hits6_single_share"])} %', False),
    ('8', 'ignoring signs changes M for under 2 %', f'{pct(S2["signs_ignored"]["M_changed_vs_signed_share"])} %', False),
    ('9', 'largest M at least 30', f'{G["M_max"]}', True),
    ('10', 'largest B at least 128', f'{G["B_max"]}', True),
    ('11', 'grep check at least 17 of 18', f'{C2["held"]} of {C2["of"]}', True),
]
held2 = sum(1 for p in pred2 if p[3])
rows2 = ''.join(f'<tr><td>P{a}</td><td style="text-align:left">{html.escape(b)}</td><td>{html.escape(c)}</td><td>{"held" if d else "<b>failed</b>"}</td></tr>' for a, b, c, d in pred2)
more50 = S2['signed']['hits6_distribution_to_50']['51']

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>First Terms</title><link rel="icon" href="data:,">
<meta name="description" content="Every sequence in the On-Line Encyclopedia of Integer Sequences, and how many of its first terms must be shown before no other sequence begins the same way.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a64;--line:#d9d6cc;--a:#3b5f86;--f:#9aa7b4;--np:#b23b2e}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--a:#7fa9d6;--f:#5d6b78;--np:#ff6b5a}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a3a197;--line:#3a3934;--a:#7fa9d6;--f:#5d6b78;--np:#ff6b5a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}
main{{max-width:1000px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:2rem;margin:.2em 0}}h2{{font-size:1.2rem;margin-top:2.2em}}
.mut{{color:var(--mut)}}.sm{{font:13px/1.45 system-ui,sans-serif}}a{{color:var(--a)}}.big{{font-size:1.25rem}}
svg.ch{{width:100%;height:auto;display:block;margin:1em 0}}svg.ch .f{{fill:var(--f)}}svg.ch .np{{fill:var(--np)}}svg.ch .ax{{stroke:var(--line)}}
svg.ch .yr{{font:13px system-ui,sans-serif;fill:var(--mut)}}.sc{{overflow-x:auto}}.sc svg.ch{{min-width:600px}}
table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
code{{font-size:.9em;overflow-wrap:anywhere}}
svg.ch polyline{{stroke-width:2.5}}svg.ch .cm{{stroke:var(--np);fill:var(--np)}}svg.ch polyline.cm,svg.ch polyline.cb,svg.ch polyline.cl{{fill:none}}svg.ch .cb{{stroke:var(--a);fill:var(--a)}}svg.ch .cl{{stroke:var(--f);fill:var(--f)}}svg.ch .cmt{{fill:var(--np)}}svg.ch .cbt{{fill:var(--a)}}svg.ch .clt{{fill:var(--mut)}}
</style></head><body><main>
<p class="sm mut">Project 24, sessions 1 and 2 · 11 and 13 November 2026 · open; no work before session 3 · data: The On-Line Encyclopedia of Integer
Sequences, <a href="https://oeis.org/">oeis.org</a>, CC BY-SA 4.0 · this page CC BY-SA 4.0</p>
<h1>First Terms</h1>
<p class="big">The On-Line Encyclopedia of Integer Sequences holds <b>{n(S["sequences"])}</b> sequences of whole numbers, each shown by
its first terms. Set every one against every other: three in five are told apart from all the rest by their first <b>six</b> terms. But
<b>{n(S["never_parted"])}</b> are never told apart by what is shown: {n(S["twin"])} show exactly the same terms as another sequence,
and {n(S["beginning_of_another"])} show only the beginning of another.</p>
{fig1}
<p class="sm mut">Each bar: the sequences that need that many first terms before no other sequence in the encyclopedia begins with the
same ones (hover a bar). Red: never told apart within the terms shown. File of 10 November 2026.</p>

<h2>1. What is read</h2>
<p>The encyclopedia publishes one file with every sequence's A-number and its shown terms (median {S["shown_terms_median"]:.0f} terms).
A reader who has some numbers types them into the search box and is shown every sequence that contains them. This study asks the
plainer question for a beginning: for each sequence, the smallest number of first terms that no other sequence shares. Terms are compared
as written, with their signs; where the indexing starts is ignored.</p>

<h2>2. What was found</h2>
<p>{pct(S["L_le3_share"])} % of the sequences are told apart by three terms or fewer; {pct(S["L_gt12_share"])} % need more than twelve.
The longest wait is {S["L_max"]} terms: A355823 (1 if every exponent in the prime factorisation of n is a power of 2) and A355825 (1 if
every exponent has an odd number of 1-bits in binary) agree on their first 127 terms and part at the 128th, which is the last one shown.
They must: 128 = 2<sup>7</sup> is the first number with an exponent, 7, that is not a power of two but has an odd number of 1-bits.
The encyclopedia shows exactly as far as the difference.</p>
<p>Beginnings are crowded. The six-term beginnings shared by the most sequences:</p>
<table><tr><th style="text-align:left">first six terms</th><th>sequences</th></tr>{top}</table>

<h2>3. The twins</h2>
<p>{n(S["twin"])} sequences fall into {n(E["twin_groups"])} groups that show identical terms ({n(E["group_sizes"]["2"])} pairs; the median
group shows {E["twin_shown_terms_median"]:.0f} terms). The largest groups are families entered together. One group of {big["size"]} sequences
shows the same sixteen terms, <code>1, 36, 1260, 44100, 1543500, …</code>: the growth series of the fundamental group of a closed surface of
genus 9 (A063819), the expansion of (1+x)/(1−35x) (A170755), and the counts of reduced words in Coxeter groups on 36 generators whose
relations have orders running from 16 to 50 (35 of them). Their names say they are different objects; their shown terms cannot. A
relation of order k, by the standard fact about such groups (not checked here), changes nothing before words of length 2k — so with
sixteen terms shown, a relation of order 16 and one of order 50 look the same. Where they part, if they do, lies beyond the file — this
study does not test it.</p>

<h2>4. The check</h2>
<p>For eighteen sequences drawn at random (seed 20261111), a second tool — <code>grep</code> on the decompressed file, sharing no code
with the count — matched the identifying beginning exactly once and the one term shorter more than once, or matched a never-parted
sequence's full terms at least twice: <b>{C["held"]} of {C["of"]}</b>.</p>

<h2>5. Predictions, registered before the count</h2>
<p class="sm">Pushed with the selection (<code>SELECTION.md</code>, commit beab4b9) before any line was read. {held} of 11 held.</p>
<table><tr><th>#</th><th style="text-align:left">registered</th><th>found</th><th></th></tr>{rows}</table>

<h2>6. The search box (session 2)</h2>
<p class="big">The search box does not match beginnings. It matches the numbers typed, in order, anywhere in a sequence. Read that way,
<b>{n(G["never_found_alone"])}</b> sequences can never be its only answer: everything they show stands, in order, inside another entry.
Among them are the sequences everyone knows.</p>
<div class="sc"><table><tr><th style="text-align:left">sequence</th><th>terms shown</th><th>fewest numbers that find it alone</th><th style="text-align:left">held whole inside</th></tr>{famous}</table></div>
<p class="sm mut">File of 12 November 2026, {n(G["sequences"])} sequences. Holders found with <code>grep</code> on the whole shown run, not with the count.</p>
<p>The Fibonacci numbers stand inside the same numbers with a 1 in front; the squares inside "[0, −1, −1] together with A000290"; the
ones inside the decimal expansion of 1/576. The Catalan numbers can be found alone, but only by fifteen of their later terms, the 16th to the 30th of 31 shown. Of all
sequences, {pct(G["never_share"], 1)} % can never be found alone: {n(G["never_kinds"]["twin"])} twins, {n(G["never_kinds"]["beginning of another"])}
that are the beginning of another, and {n(G["never_kinds"]["inside another"])} that stand further inside another.</p>
{fig2}
<p class="sm mut">For each number of terms typed, the share of all sequences found alone. <span style="color:var(--np)">M</span>: the
shortest run of a sequence's terms, anywhere, that no other sequence holds. <span style="color:var(--a)">B</span>: its first terms, typed into
the box. L: its first terms against other beginnings (session 1). Hover a dot.</p>
<p>Typed from the beginning, a sequence needs more numbers in the box than against other beginnings for {pct(G["B_gt_L_share"], 0)} % of
them; the median stays at {G["B_median"]}. But typed from its first terms, {n(more50)} sequences — one in five — still share their first six
numbers with fifty or more others. And the shortest run that finds a sequence alone is short: {n(X2["M_eq_1"])} sequences hold a single
number no other sequence holds, and the median is {G["M_median"]}. That run stands at the beginning for only {pct(G["M_at_beginning_share"], 1)} %;
for the rest it stands further in. The longest shortest-run is {G["M_max"]} terms, for two sequences of period six (A120325
and A354354): 117 of their 121 shown terms are needed before no other sequence holds the run.</p>
<p>The check: for eighteen sequences drawn at random (seed 20261113), <code>grep</code> found the first B terms and the shortest run in
exactly one line, and every shorter run in at least two ({C2["held"]} of {C2["of"]}). Ignoring signs, as the box may, leaves
{n(S2["signs_ignored"]["never_found_alone"])} never found alone.</p>
<p class="sm">Predictions, pushed before the count (<code>SESSION2.md</code>, commit 624986e). {held2} of 11 held.</p>
<table><tr><th>#</th><th style="text-align:left">registered</th><th>found</th><th></th></tr>{rows2}</table>

<h2>7. What is not here</h2>
<p>Whether a shown term is right, and whether twins differ further on, are not in this file. Why the sequences after A200000 are about a
quarter as often unfindable as those before is not in it either. No contributor is named or counted.</p>
<p class="sm mut">Files: <a href="SELECTION.md">SELECTION.md</a> · <a href="count1.py">count1.py</a> → <a href="session1.json">session1.json</a> and <a href="session1-per.json.gz">session1-per.json.gz</a> (every sequence: A-number, terms shown, kind, length, nearest partner; no terms)
· <a href="check1.py">check1.py</a> → <a href="check1.json">check1.json</a> · <a href="explore1.py">explore1.py</a> →
<a href="explore1.json">explore1.json</a> (exploratory) · <a href="JOURNAL.md">JOURNAL.md</a> · <a href="MAP.md">MAP.md</a> ·
<a href="NEIGHBOURS.md">NEIGHBOURS.md</a> · session 2: <a href="SESSION2.md">SESSION2.md</a> · <a href="count2.py">count2.py</a> → <a href="session2.json">session2.json</a> and <a href="session2-per.json.gz">session2-per.json.gz</a> · <a href="check2.py">check2.py</a> → <a href="check2.json">check2.json</a> · <a href="explore2.py">explore2.py</a>, <a href="explore2b.py">explore2b.py</a>, <a href="explore2c.py">explore2c.py</a> (exploratory). Data: <a href="https://oeis.org/">The On-Line Encyclopedia of Integer Sequences</a>,
CC BY-SA 4.0. Remainder.</p>
</main></body></html>
'''
open('index.html', 'w').write(page)
print('ok', held, held2)
