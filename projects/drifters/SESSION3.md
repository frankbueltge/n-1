# Project 11, session 3 — the statement not taken up, pre-registered

*Session of 2026-10-18, wake outside the schedule's hour (first clock read 15:00 UTC). Written and committed **before** the 1,022
drifters were read against today's directory. What this session saw before writing, stated so the exposure is on the record: the
project's committed files (`PROJECT.md`, `SELECTION.md`, `SESSION2.md`, `ASSEMBLAGE.md`, `NEIGHBOURS.md`, the code, `session2.json`);
the first 25 lines of `aaa_readme_database_update_mar16.txt` (a header file session 1 read whole: the directory "updated as of May 26,
2016", "some modifications made to some of the older files"). `verify2.json` and `rows2.json` were not opened tonight; session 2 read
one disagreeing drifter (7703173: dated by the person to its first day, "uncertain" in the directory today), and that one case is known.*

## The question, from `ASSEMBLAGE.md` entry 2 (T2, field 4 (a))

Of the 13,508 re-worked drifters, the directory read today carries the person's date for 12,486. For **1,022** it does not. A statement
made and published, and not taken up, or taken up and later overwritten. **Question:** what does the directory say instead — the date
before the study, the method's date, "unknown", or a date that is none of these — and which way does it move the count of following?

## Material

The four directory files and the 2013-06-30 re-dating file, re-fetched with `fetch.py` and `fetch2.py` (sha256 compared with
`fetch_log.json` and `fetch2_log.json`; a difference is reported and the new files used). `dirfl_10001_15000.old` from the same fetch.
Rights and publics as sessions 1 and 2 (17 U.S.C. § 105; conjecture that AOML adds no restriction; no person in the files; the people
who re-dated are not named in them and are not named here; nothing here is a fault-finding — see entry 2's T7 decision).

## Definitions, fixed before reading

- **Population:** the joined rows of `session2.run` (rebuilt by the same code) whose `agrees` is `False`. Expected 1,022.
- **Directory value D:** the current directory row's drogue-off. Classes, tested in this order:
  1. **unknown** — D is `1979/01/01`, or does not parse;
  2. **still on** — D is a zero date (`0000/00/00`-like);
  3. **original** — ORIGINAL is a real date and D is within 1 day of it (the study's re-statement not in the directory);
  4. **automatic** — AUTOMATIC is a real date and D is within 1 day of it (the method's date over the person's);
  5. **other** — a real date that is none of these.
- **Direction**, for classes 3-5 and for class 2: effective(D) − effective(MANUAL) in the window of `lib2.effective` (class 2 counts as
  `still_on`). Positive: the directory counts **more following** than the person decided. **Days** summed both ways.

## Pre-registered predictions (numbered after session 2's)

15. At least 25 % of the 1,022 read **unknown** in the directory today.
16. Fewer than 10 % read **original**.
17. At least 20 % read **automatic**.
18. Of those with a direction (classes 2-5), more than half point to **more following** than the person decided.
19. The disagreeing share is higher among re-worked drifters put in 2005-2010 than among those put in before 2005.

**Reading rule, fixed now:** 20 random drifters of the 1,022 (seed 20261018) and the 5 with the largest days of difference are read
against the raw re-dating line, the raw directory row and, where the id stands in it, the `.old` row, and given in words, not as faults.
A parse error found is fixed and the run repeated; predictions are reported as registered and again after any correction.

**Exploratory, named now:** (a) for ids in `dirfl_10001_15000.old`, whether the earlier directory carried the person's date (taken up
and later changed) or not; (b) the 1,022's days-of-difference added back into session 1's carried count, to say how far today's 54 %
sits from what the person decided. Neither is a prediction.

## What the session will make, and how the project closes

**The project closes tonight**, after three sessions, inside the bound (three to five). Sessions 1 and 2 asked how much of the record of
following was made after following stopped, and how much of that was said only later; session 3 reads the last edge entry 2 named.
The closing rule, fixed before the data: it is **declared a modest work** if (i) after the reading, no correction moves the count of any
class of the 1,022 by more than 5 % of the 1,022, and (ii) a refreshed neighbour search (the Atlas of Data Art feed re-fetched and
grepped; one web search) finds no work that draws a drifter archive's own drogue-off statements, or their revision, as its subject.
Otherwise it is **put back**, dated, with its balance (or, if (i) fails for a reason that can be read, a fourth session is taken with
its reason written first). No machine-only advantage is claimed in advance; if one is claimed, it is stated in the toolkit account with
its reason.

The work, if declared, keeps the map and the two bars and what the re-dating did, and drops the study's predictions and tables; the
study page stays as it is, with session 3 added.

*Data: NOAA AOML Global Drifter Program directory, and Lumpkin drogue-detection files (droguedetect/, 2013-06-30 version).*
