"""Project 24: build the study page index.html from session1.json, check1.json, explore1.json (stdlib only).
Usage: python3 -I build.py   (run in projects/first-terms/)"""
import json, html

S = json.load(open('session1.json'))['summary']
C = json.load(open('check1.json'))
E = json.load(open('explore1.json'))


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
</style></head><body><main>
<p class="sm mut">Project 24, session 1 · 11 November 2026 · open; no work before session 3 · data: The On-Line Encyclopedia of Integer
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

<h2>6. What is not here</h2>
<p>Whether a shown term is right, and whether twins differ further on, are not in this file. The search box matches a run of numbers
anywhere in a sequence, not only at its beginning; that is session 2's question. No contributor is named or counted.</p>
<p class="sm mut">Files: <a href="SELECTION.md">SELECTION.md</a> · <a href="count1.py">count1.py</a> → <a href="session1.json">session1.json</a> and <a href="session1-per.json.gz">session1-per.json.gz</a> (every sequence: A-number, terms shown, kind, length, nearest partner; no terms)
· <a href="check1.py">check1.py</a> → <a href="check1.json">check1.json</a> · <a href="explore1.py">explore1.py</a> →
<a href="explore1.json">explore1.json</a> (exploratory) · <a href="JOURNAL.md">JOURNAL.md</a> · <a href="MAP.md">MAP.md</a> ·
<a href="NEIGHBOURS.md">NEIGHBOURS.md</a>. Data: <a href="https://oeis.org/">The On-Line Encyclopedia of Integer Sequences</a>,
CC BY-SA 4.0. Remainder.</p>
</main></body></html>
'''
open('index.html', 'w').write(page)
print('ok', held)
