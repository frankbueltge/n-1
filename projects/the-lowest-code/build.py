"""Project 27: the study page (index.html) from session1.json, explore1.json, explore2.json, check1.json and
session1-per.json.gz. Standard library only. Usage: python3 build.py"""
import gzip
import json

S = json.load(open("session1.json"))
E1 = json.load(open("explore1.json"))
E1B = json.load(open("explore1b.json"))
E2 = json.load(open("explore2.json"))
C = json.load(open("check1.json"))
PER = json.load(gzip.open("session1-per.json.gz"))

YEARS = list(range(1992, 2026))
# every bridge whose lowest code in the 2025 file is 4 or less, open or closed (explore2.json splits the two)
rows = []
for b, v in PER.items():
    L = v["L"]
    if L[-1] in "01234":
        sp = v["spells"][-1]
        rows.append((sp[1] - sp[0] + 1, b, L, v["rises_norecon"]))
rows.sort(key=lambda r: (-r[0], r[1]))

COL = {"9": "#2f6070", "8": "#4a7d8c", "7": "#7aa3ae", "6": "#b3c8cc", "5": "#d9e2e2",
       "4": "#e3a25a", "3": "#c8552f", "2": "#8f2418", "1": "#5a120b", "0": "#2a0805", "N": "#9aa0a0"}
cw, rh, left, top = 26, 2, 52, 22
W = left + cw * (len(YEARS) - 1) + 10
H = top + rh * len(rows) + 30
parts = []
for i, (_, b, L, _) in enumerate(rows):
    y = top + i * rh
    s = L[1:]  # 1993..2025: no 1992 number carries into 1993
    j = 0
    while j < len(s):
        k = j
        while k < len(s) and s[k] == s[j]:
            k += 1
        if s[j] != "-":
            parts.append(f'<rect x="{left + j * cw}" y="{y}" width="{(k - j) * cw}" height="{rh}" fill="{COL[s[j]]}"/>')
        j = k
ticks = "".join(
    f'<text class="yr" x="{left + (y - 1993) * cw + cw / 2:.0f}" y="{top - 6}" text-anchor="middle">{y}</text>'
    for y in (1993, 2000, 2005, 2010, 2015, 2020, 2025))
legend = "".join(
    f'<rect x="{left + i * 70}" y="{H - 18}" width="14" height="10" fill="{COL[c]}"/><text class="yr" x="{left + i * 70 + 18}" y="{H - 9}">{c}</text>'
    for i, c in enumerate(["9", "7", "5", "4", "3", "2", "N"]))
svg = (f'<svg class="ch" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ft"><title id="ft">{len(rows)} Alabama highway bridges whose '
       f'lowest condition code is Poor (4 or less) in the 2025 file, one thin row each, 1993 to 2025 across, coloured by the code each year: '
       f'blue for 5 to 9, orange for 4, red for 3, dark red for 2 or less, blank where the number is not in the file. Sorted by how long '
       f'the current Poor run has lasted; the top rows are orange and red from edge to edge.</title>{ticks}{"".join(parts)}{legend}</svg>')

def pct(x):
    return f"{100 * x:.1f} %"

def n(x):
    return f"{x:,}"

pred = [
    ("P1", "more than 20 % of the 2025 bridges have been Poor at least once", pct(S["P1_share_last_ever_poor"]), False),
    ("P2", "median length of Poor spells that end in a rise: 2 to 6 years", f'{S["P2_median_years_spells_rose"]:.0f} years', True),
    ("P3", "of those, more than 40 % end with no reconstruction recorded", pct(S["P3_share_rose_norecon"]), True),
    ("P4", "more than 50 % of all rises come with no reconstruction recorded", pct(S["P4_share_rises_norecon"]), True),
    ("P5", "falls of two steps or more under 15 % of falls", pct(S["P5_share_falls_2plus"]), True),
    ("P6", "longest Poor spell of a bridge open in 2025 over 20 years", f'{S["P6_longest_spell_open_last"]} years', True),
    ("P7", "more than half of open Poor bridge-years unrestricted (item 41 = A)", pct(S["P7_share_poor_open_A"]), False),
    ("P8", "crossings while Poor (estimate) over one billion", f'{S["P8_crossings_while_poor_estimate"] / 1e9:.1f} billion', True),
    ("P9", "under 1 % of records malformed", pct(S["P9_share_malformed"]), True),
    ("P10", "over 99 % of lines carry Alabama's code, every year", pct(S["P10_min_file_share_fips_ok"]) + " (lowest file)", True),
]
ptab = "".join(f'<tr><td style="text-align:left">{k}</td><td style="text-align:left">{t}</td><td>{v}</td><td>{"held" if h else "failed"}</td></tr>'
               for k, t, v, h in pred)
held = sum(h for *_, h in pred)

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Lowest Code</title><link rel="icon" href="data:,">
<meta name="description" content="Every Alabama highway bridge followed through the National Bridge Inventory's yearly files, 1992 to 2025: how long its lowest condition code stays Poor, and how often it rises with no reconstruction recorded.">
<style>
:root{{--bg:#f6f5f2;--fg:#1c1b19;--mut:#66625c;--line:#d8d4cc;--a:#2f6070}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151413;--fg:#ebe8e2;--mut:#a39e96;--line:#36332f;--a:#8cc0cf}}}}
:root[data-theme="dark"]{{--bg:#151413;--fg:#ebe8e2;--mut:#a39e96;--line:#36332f;--a:#8cc0cf}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}
main{{max-width:1000px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:2rem;margin:.2em 0}}h2{{font-size:1.2rem;margin-top:2.2em}}
.mut{{color:var(--mut)}}.sm{{font:13px/1.45 system-ui,sans-serif}}a{{color:var(--a)}}.big{{font-size:1.25rem}}
svg.ch{{width:100%;height:auto;display:block;margin:1em 0}}svg.ch .yr{{font:12px system-ui,sans-serif;fill:var(--mut)}}
.sc{{overflow-x:auto}}.sc svg.ch{{min-width:640px}}.tw{{overflow-x:auto}}
table{{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif}}table th,table td{{padding:3px 10px;border-bottom:1px solid var(--line);text-align:right}}
blockquote{{margin:1em 0;padding-left:14px;border-left:3px solid var(--line)}}
</style></head><body><main>
<p class="sm mut">Project 27, session 1 · 25 November 2026 · open; no work before session 3 · data: Federal Highway Administration, National
Bridge Inventory, Alabama, yearly files 1992–2025 (read as a US government work, a reading marked conjecture in
<a href="https://github.com/frankbueltge/n-1/blob/main/projects/the-lowest-code/SELECTION.md">SELECTION.md</a>) · this page CC BY 4.0 · Remainder</p>
<h1>The Lowest Code</h1>
<p class="big">Usually every two years, more often for a weak one, an inspector stands under each highway bridge in the United States and gives its deck, its
superstructure and its substructure (or, for a culvert, the culvert) a number from 9, excellent, to 0, failed. Since 2018 a bridge is
called <b>Poor</b> when the lowest of these is 4 or less. Concrete and steel left alone only decay; the number is a judgement made at a
date. Followed through 33 years of Alabama's records, the number rose <b>{n(S["rises"])}</b> times — and <b>{n(S["rises_norecon"])}</b> of those
rises ({pct(S["P4_share_rises_norecon"])}) came with no reconstruction recorded. In 2025, <b>{n(E2["poor_open_2025"])}</b> Alabama bridges
are Poor and open to traffic; half of them have been Poor for <b>{E2["current_spell_years_median"]:.0f} years</b> or more, and
<b>{E2["current_spell_years_33"]}</b> in every file since their number began in 1993.</p>
<div class="sc">{svg}</div>
<p class="sm mut">The {len(rows)} bridges whose lowest code is 4 or less in the 2025 file ({E2["poor_open_2025"]} open, {E2["poor_closed_2025"]}
closed to all traffic), one row each, by structure number in the record; no names, no places. Codes 5 to 9 in blue, 4 orange, 3 red, 2 and
below dark red, N (not applicable) grey, blank where the number is not in that year's file.</p>

<h2>1. What is followed</h2>
<p>The Federal Highway Administration publishes each state's inventory once a year, one fixed-width line per structure. For each bridge
this study takes the least of the four condition codes (deck, superstructure, substructure, culvert), whether it is open, posted or closed,
the date of its inspection, its year built and year reconstructed, and the traffic the record says crosses it each day. A bridge is
followed by its structure number. The Coding Guide defines 4 as "POOR CONDITION - advanced section loss, deterioration, spalling or scour",
and 3 as "SERIOUS CONDITION … Local failures are possible."</p>
<p>The record holds its bridges by number, and the numbers break. <b>Not one of the {n(E1["per_year"]["1992"])} structure numbers of the 1992
file recurs in 1993</b>: Alabama's 1992 file numbers its bridges in another scheme, so every line on this page begins in 1993. After that,
between 51 and 381 numbers enter each year and between 71 and 285 leave — replacements, new bridges and renumberings, which the record does
not tell apart.</p>

<h2>2. How long Poor lasts</h2>
<p>From 1993 to 2025, {n(E1B["spells"])} times a bridge's lowest code fell to 4 or less and stayed there for a run of years. {n(E1B["spells_by_outcome"]["rose"])}
of those runs ended with the code rising to 5 or more, after a median of {S["P2_median_years_spells_rose"]:.0f} years; {n(E1B["spells_by_outcome"]["left"])}
ended with the number leaving the files; {n(E1B["spells_by_outcome"]["censored"])} are still running in 2025. Of the runs that ended in a rise,
{pct(S["P3_share_rose_norecon"])} ended with no reconstruction recorded — neither the year built nor the year reconstructed changed.</p>
<p>That is what the record says, not what was done. The Coding Guide does not count as reconstruction, among others, "Emergency repair to
restore structural integrity to the previous status following an accident" or "Work performed to keep a bridge operational while plans for
complete rehabilitation or replacement are under preparation". A rise with nothing recorded may be such work, or a different judgement of
the same steel. The record cannot say which.</p>
<p>Among open Poor bridge-years, {pct(S["P7_share_poor_open_A"])} were open with no restriction; most were posted for load. The traffic the
record gives for those years adds up to <b>about {S["P8_crossings_while_poor_estimate"] / 1e9:.0f} billion crossings</b> — an
<b>estimate</b>, the record's own daily figure times 365, and that figure is not always counted again: bridge 006850, steel, built 1960,
code 3 in its substructure in every file from 1993 to 2025, posted, carries 35 vehicles a day in each of them.</p>

<h2>3. Predictions and check</h2>
<p>Registered before any file was downloaded (<a href="https://github.com/frankbueltge/n-1/blob/main/projects/the-lowest-code/SELECTION.md">SELECTION.md</a>);
the count run once. {held} of 10 held.</p>
<div class="tw"><table><tr><th style="text-align:left"></th><th style="text-align:left">prediction</th><th>found</th><th></th></tr>{ptab}</table></div>
<p class="sm">Check: twelve bridges drawn at random from those ever Poor, and the one Poor longest, recomputed from the raw lines by awk alone —
{C["held"]} of {C["checked"]} agree in every figure. Lines per file by <code>wc -l</code>: {C["wc_l"]["equal"]} of 34 agree. What the check cannot
test: whether an inspector's code is right, what work a rise reflects, or how many people crossed. The line measured here is this record's
line.</p>

<h2>4. Who this is about</h2>
<p>People who cross these bridges, and people beneath them; the public whose money decides which bridge is repaired when; and anyone hurt at
one, who cannot bring this record into a damages action: the disclaimer before every file quotes 23 U.S.C. §409, under which such data
"shall not be subject to discovery or admitted into evidence in a federal or state court proceeding". Nothing on this page judges a bridge
safe or unsafe.</p>
<p class="sm mut">Files: <a href="https://github.com/frankbueltge/n-1/tree/main/projects/the-lowest-code">projects/the-lowest-code</a>
(count1.py, session1.json, check1.sh, check1.json, explore1.py, explore2.py, JOURNAL.md, ASSEMBLAGE.md, NEIGHBOURS.md). Section 1's
entry and exit figures and section 2's spell figures are from the 1993–2025 run (explore1.json, explore1b.json), the rest from the
registered count.</p>
</main></body></html>
"""
open("index.html", "w").write(html)
print(len(html), len(rows))
