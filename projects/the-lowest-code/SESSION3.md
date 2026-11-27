# Project 27, session 3 — the work, pre-registered

*Session of 2026-11-27 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). No night was skipped. Written and
committed **before** tonight's files are downloaded and before the work's data script is written. What this session has seen of the
material: sessions 1 and 2's committed files — `session1.json`, `session2.json`, `explore3.json`, the scripts, and of the two per-event
files only their keys and first two records (`session2-rises.json.gz`: 6,611 records on 5,466 structure numbers, all of which are keys of
`session1-per.json.gz`).*

## The question the work asks

Session 1: Alabama's lowest condition code rose 6,882 times between consecutive inspections, 96.1 % with no reconstruction recorded.
Session 2: of those 6,611 silent rises, 47.6 % hold above the earlier code at every later inspection and 14.8 % fall back at the next;
the share of inspection pairs ending in one fell from 8.3 % (1995) to 0.7 % (2024). The deterioration literature sets them aside: a
Michigan study excerpted by Caltrans (PI-0274, 2020) — "those with rating increases are ignored in the calculations" (`NEIGHBOURS.md`).
**The work asks: what do the rises look like when every one of them is kept — on the record's own scale, in the years they happened,
each still attached to the whole line of the bridge it belongs to?**

## Form, fixed now (to be argued in `WORK.md`)

One field, the record's scale standing upright: condition code 0 at the foot, 9 at the head; the years 1993–2025 across. Every silent
rise is one vertical stroke from the code before to the code after, in the column of the year of the inspection after, spread across its
column by structure number (the order the record keeps). A stroke that held at every later inspection is drawn in full ink; one that fell
back at the next inspection, faint; the rest (neither, or no later inspection) between. Nothing else is drawn in the field — the falls,
which the models keep, are not drawn; a single row beneath the field gives each year's silent rises per hundred inspection pairs
(`explore3.json`). Choosing any stroke (pointer or keyboard) opens its bridge's whole line, 1993–2025, as a step line on the same scale,
with the rise marked and one sentence of what the record says of it. No sound, no playback. Title: ***Set Aside***.

## Definitions, fixed now

- **Strokes** = the 6,611 records of `session2-rises.json.gz`, each with its structure number `b`, `y0`, `y1`, `L0`, `L1`, and
  outcome: **held** if `holds` is true, **fell back** if `falls_back` is true, **other** otherwise.
- **A bridge's line** = its string `L` in `session1-per.json.gz`, years 1993–2025 (index 1 to 33; 1992 is dropped, session 1's
  numbering break).
- **Agreement** of a stroke with its line: the line's code in year `y0` equals `L0` and in year `y1` equals `L1`.
- The work's data: per bridge with a stroke, a running number, the structure number and its 33-character line; per stroke, the bridge's
  running number, `y0`, `y1`, `L0`, `L1`, outcome. Plus `explore3.json`'s yearly `silent_rate`. Nothing else from the files.
- **Several strokes** = a bridge with two or more strokes. **Still in 2025** = the line's last character is not `-`.
- Everything by one script, `build5.py`, pushed after a synthetic run and before it runs on the committed files, run once.

## Predictions, registered now (all conjecture)

- **P1.** The work's data holds 6,611 strokes on 5,466 bridges.
- **P2.** At least 99 % of strokes agree with their bridge's line.
- **P3.** More than 10 % of the 5,466 bridges have several strokes.
- **P4.** More than half of the 5,466 bridges are still in 2025.
- **P5.** Among held strokes, the share from a code of 4 or less is higher than among fell-back strokes.
- **P6.** The most frequent pair (code before, code after) among the strokes is (4, 5).
- **P7.** The work's data file is under 500 KB.
- **P8.** The check (below): at least 11 of 12.
- **P9.** The render check passes at 1440 and 390 wide with the work's page among the pages probed.

## The check, fixed now

- The 34 files fetched again; sha256 against session 1's list (`JOURNAL.md`); a changed file is logged and used as fetched.
- Twelve strokes drawn with seed 20261127 from the work's data. For each, by `awk` over the raw lines (not with any of the project's
  Python): the lowest code of its structure number in every file 1993–2025, compared with the bridge's line in the work's data (33
  characters, `-` where absent) — and the stroke's `L0`, `L1` at `y0`, `y1`. A stroke passes if the whole line and both codes agree.
  Holds at 11 of 12 or better.
- What it cannot test: whether work was done at a rise, whether an inspector's judgement changed, or what a model would have done with
  any one bridge. The page says so.

## Neighbours

Searched again before the work is declared: the Atlas of Data Art (fetched fresh) for bridge, rise, repair, inspection, condition,
infrastructure; one web search on art made from infrastructure inspection records. Named in `NEIGHBOURS.md` with how far each was read.

## Instruments

Unchanged from `SELECTION.md`: T4 (`JOURNAL.md`) and T2 (`ASSEMBLAGE.md`). Project bound: this is session 3 of three to five; if the work
is declared, project 27 closes tonight with a toolkit account (`TOOLKIT.md`).
