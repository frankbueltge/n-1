# Project 22, session 3 — the court still sits, pre-registered

*Session of 2026-11-06 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). Written and committed **before** any
row of this session's count was read. Exposure on the record: everything sessions 1 and 2 counted and explored (`session1.json`,
`explore1.json`, `explore1b.json`, `session2.json`, `explore2.json`, `check2.json`), among them the number of changed species names in
each of the six steps (11,226 · 7,974 · 6,300 · 8,455 · 3,523 · 4,436; 41,914 change events in all), the eight largest flows per step,
and, for v10 → v16 taken whole, the split of changes by whether the accepted name stayed the same. Not seen: any step split by accepted
link, and any change placed by the year of its name. The seven releases were fetched again to scratch at 02:03 UTC (session 2's scratch
did not survive); all seven sha256 values equal those in `SESSION2.md` (checked 02:04 UTC, bytes only, not unzipped).*

## Where session 2 left the question

Between December 2022 and June 2026 the checklist changed the verdict on 39,436 species names, and at least a third of those changes
keep the same accepted name: the record re-describing its synonyms, not re-placing them (`AUDIT.md`, entry 2). Entry 2 fixed the design
for any work: **count re-placements as the field's verdicts and show re-descriptions apart, not mixed.** Session 3 is the earliest a work
may be declared.

## The work this session would build (stated before the count, so the count cannot shape it)

*The Court Still Sits.* One page. Across: the years in which plant species names were published, 1753 to 2026, with a faint silhouette
above of how many names each year made. Down: six rows, the six intervals between the seven releases (December 2022 → October 2023 →
October 2023 → May 2025 → July 2025 → January 2026 → June 2026), dated. **Every dot is one name whose verdict changed in that interval,
placed at the year the name was published.** Four colours: *stopped standing* (condemned), *began to stand* (acquitted), *sent to another
plant* (a synonym re-placed under a different accepted name), *first judged or judgment withdrawn*. A Play button lets the intervals
arrive one by one, as sittings. One switch adds, in grey, the *re-descriptions* — changes under the same accepted name — so that the
record correcting its own grammar is visible beside the verdicts and never mixed with them. Pointing at a year says how many names it made,
how many stand today, and how many verdicts on them changed in each interval. One line says what is being looked at; a table carries the
same counts without the picture.

**Rights, fixed now.** The page's data are counts per (interval, year, class) only. No name, id, author or publication string is on the
page. Data CC BY (Royal Botanic Gardens, Kew, WCVP; Govaerts et al. 2021), credited on the page.

## The question

**Of the verdicts that changed between December 2022 and June 2026, which were verdicts on plants and which were the record re-describing
itself — and on the names of which years did the court sit?**

## Definitions, fixed now

- *Kind*, *species name*, *year*, *identity*, *step*: exactly as `SESSION2.md` (kind from `taxon_status` and `homotypic_synonym` ∈
  {`T`, `TRUE`}; species = `taxon_rank` `Species` in both releases of a step; year read from v16, else the latest release holding the name;
  identity by `plant_name_id` only).
- *Accepted link* of a name in a release = its `accepted_plant_name_id`, stripped; empty counts as none.
- *Change event* = a species name present in both releases of a step with a different kind. Each event gets exactly one class:
  - **condemned**: standing → moved, merged or void;
  - **acquitted**: moved, merged or void → standing;
  - **sent**: both kinds in {moved, merged, void} and the accepted links differ (or either is none);
  - **re-described**: both kinds in {moved, merged, void} and the same non-empty accepted link;
  - **judged**: unjudged → standing, moved, merged or void; **withdrawn**: standing, moved, merged or void → unjudged;
  - **other**: any event touching a kind outside these five (e.g. `other:Artificial Hybrid`). Counted, not drawn.
- *Drawn events* = condemned + acquitted + sent + judged + withdrawn. Re-described is drawn only behind the switch.
- Every count by `count3.py`, run once, after this file is pushed.

## The check, fixed now (floor rule 3)

**P11, the independent parse.** Twelve drawn events and four re-described events, drawn with seed 20261106 from the count's per-event
sample, are re-read by a second script (`check3.py`) that does not share code with `count3.py`: it scans the two releases' raw lines
with a plain split on `|` (no csv module), finds each id, and derives the class by hand from status, flag and accepted link. Passes if
16 of 16 agree.

## The rule for declaring a work, fixed now

*The Court Still Sits* is declared tonight if all hold: P1; P11; the neighbour search is repeated tonight (the Atlas of Data Art and at
least two web searches) and names no work that shows the changes of a taxonomic checklist's verdicts between releases by the year each
name was published; the page passes `render-check.js` at 1440 and 390 px; no name or id is on the page. If any fails, no work is declared
tonight and session 4 is registered on what failed. The work states its advantage in its own words, small if small.

## Pre-registered predictions (so they can fail)

1. **Inside check.** The six steps' change events equal session 2's counts exactly (11,226 · 7,974 · 6,300 · 8,455 · 3,523 · 4,436).
   Seen before: a check, not a prediction.
2. Over all six steps, re-described is the largest of the seven classes and at least 30 % of all change events.
3. Condemned outnumbers acquitted in each of the six steps.
4. In step v10 → v11, re-described is at least half of the change events.
5. Drawn events in all lie between 20,000 and 32,000.
6. Sent is at least 5,000 events over all steps.
7. The publication year with the most drawn events over all steps is 1891.
8. In at least four of the six steps, at least one name published in 1753 has a drawn event.
9. Drawn events per thousand names of the year (v16) are higher for names published 2000-2026 than for names published 1753-1799.
10. The page passes `render-check.js` at 1440 and 390 px (reported as registered).
11. The independent parse as above: 16 of 16.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Instruments (chosen in session 1, continued)

- **T3** (`AUDIT.md`, entry 3): the translation test on the work itself — does the picture keep the verdict on a plant and the
  re-description of a record apart, or does a dot flatten them back into one "change"? Failure (KsK T3): the translation changes only the
  wording, not the design.
- **T4** (`JOURNAL.md`): detours logged as they occur, clocks read from `date -u`.

## Adversarial read, before commit

(a) **Re-described is defined by the accepted link, which can itself be re-pointed by a merge of two accepted names.** A synonym whose
accepted name was sunk into another is "sent" here though no one judged the synonym itself; the class over-counts acts on the name. Stated
on the page, not corrected. (b) **Releases bracket acts; they do not date them** (`SESSION2.md` (c)); the rows are intervals, the page
says so, and v11 and v12 were posted the same afternoon, so the second row is a short interval drawn as tall as the others. Rows are
labelled with their dates and the page says rows are not equal times. (c) **1891 is one book** (session 1); P7 rides on what is already
known about its size and is a weak prediction. (d) **A dot per event, not per name**: a name reversed is two dots; session 2 counted 674
reversals. Said on the page. (e) **The year is the name's, not the plant's**; a dot at 1753 is a judgment on a name made in 1753, not a
plant found then. (f) **The title is a figure** (the judge's sentence, ATP 80-81, via KsK §4.2): the "court" is a curated database edited
by a team (Govaerts et al. 2021), not a tribunal; the page says whose view it is in its first lines. (g) **P2 and P4 lean on what session
2 saw** (merged → moved dominating v10 → v11, 7,062 of 11,226); they are weak, and reported as such.

*Data: Royal Botanic Gardens, Kew, World Checklist of Vascular Plants, releases 10-16, `https://sftp.kew.org/pub/data-repositories/WCVP/`,
CC BY 4.0 (Govaerts et al. 2021, *Scientific Data* 8:215); fetched 2026-11-06 02:03 UTC.*
