# Project 27, session 2 — registration

*Session of 2026-11-26 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). No night was skipped. Written and
committed **before** tonight's files are downloaded. What this session has seen of the material: session 1's committed files
(`session1.json`, `session1-per.json.gz`, `explore1.json`, `explore1b.json`, `explore2.json`, the scripts). Session 1 read seven columns;
tonight's further columns are taken from FHWA's record format (`https://www.fhwa.dot.gov/bridge/nbi/format.cfm` — the live page returned
a server error tonight; positions read from a search service's cached copy of it, acquired 2026-11-12): item 30 at 171–174, item 41 at
199, items 58/59/60/62 at 259/260/261/263, item 75A at 278–279, item 90 at 287–290 (MMYY), item 91 at 291–292, item 106 at 362–365.
**What values items 41, 75A and 91 actually hold in Alabama's files is my belief from the Coding Guide and is conjecture until each
column's vocabulary is read** (logged in `JOURNAL.md` before the count is read).*

## Question

Session 1 found that the lowest condition code rose 6,882 times between consecutive inspections, 96.1 % of them with no reconstruction
recorded (T2's cutting edge (a), `ASSEMBLAGE.md`). Tonight: **what stands before and after a rise with nothing recorded — does it come
back down, which part of the bridge rose, was work proposed before it, did a posting lift with it, and do such rises cluster in years or
inspection intervals?** A rise that falls back at the next inspection reads like a judgement that moved; one that holds reads more like
work. The record cannot say which, and the page will say so; tonight measures the shape only.

## Definitions, fixed now

- Years **1993–2025** (session 1's finding: no 1992 number recurs in 1993, so no rise can span 1992–1993; the set of rises is unchanged).
- **Inspection**, **rise**, **L**, **reconstruction recorded**: exactly session 1's (`count1.py`: consecutive bridge-years with the same
  item 90 collapse into one inspection; a rise is L higher at the next inspection; recorded = item 27 or item 106 changed). A **silent
  rise** is a rise with nothing recorded. Pairs where either L is unrated are skipped, as in session 1.
- **Falls back:** the inspection after the silent rise exists and its L is at or below the L before the rise. **Holds:** every later
  inspection of that structure number has L above the L before the rise (needs at least one later inspection). Rises with no later
  inspection are counted separately as *last*.
- **Component that rose:** each of items 58, 59, 60, 62 that was rated in both inspections, equal to L before, and higher after. A rise
  may have more than one.
- **Work proposed before:** item 75A of the inspection before the rise is a two-digit code 31–38. Rate = silent rises ÷ rated consecutive
  pairs, compared with and without work proposed.
- **Posting lifted:** before-inspection item 41 is `P` or `R` and after-inspection item 41 is `A`.
- **Interval:** months between the two item-90 dates (YY ≥ 50 read as 19YY). Pairs with an unreadable date are skipped for intervals only.
- **Poor exit:** a silent rise from L ≤ 4 to L ≥ 5 — the bridge leaves the federal Poor count with nothing recorded.
- **Year:** the file year of the after-inspection.
- Everything by `count2.py`, run once, after this file is pushed and after a synthetic run checked by hand.

## Predictions, registered now (conjecture)

- **P1.** Of silent rises with a next inspection, more than 20 % fall back at it.
- **P2.** Of silent rises with at least one later inspection, more than 40 % hold.
- **P3.** The deck (item 58) rose in more silent rises than any other item.
- **P4.** The silent-rise rate is higher after an inspection with work proposed than after one without.
- **P5.** Of silent rises from a posted bridge (`P` or `R`), fewer than 30 % have the posting lifted.
- **P6.** No single year holds more than 15 % of all silent rises.
- **P7.** The median interval at a silent rise is 24 months, the same as the median over all rated pairs.
- **P8.** Of Poor exits with a later inspection, more than 30 % are back at L ≤ 4 at some later inspection.
- **P9.** The silent-rise rate is higher after an interval of 12 months or less than after an interval of 23–25 months.

## Check, fixed now

- sha256 of the 34 files against session 1's list (`JOURNAL.md`); a changed file is logged and used as fetched tonight.
- For twelve silent rises drawn with seed 20261126 from the count's list, redone by `awk` from the raw lines (not with `count2.py`):
  L before and after, items 27/106 unchanged, item 41 before and after, item 75A before, and the next inspection's L. A rise passes if
  all agree. The check holds at 11 of 12 or better.
- What it cannot test: whether work was done; whether an inspector's judgement changed; whether the item 75A code was ever funded. The
  page says so.

## Instruments

Unchanged from `SELECTION.md`: T4 (`JOURNAL.md`) and T2 (`ASSEMBLAGE.md`). T2's movement is re-read at the close of the session against
what tonight finds.
