# Project 20 — session 3, pre-registered: the rings heard against one fork, decade by decade

*Session of 2026-10-31 (Berlin), the schedule's wake (first clock read 02:04 UTC, 03:04 Berlin). Written and committed **before** any
row of this session's count was read. Exposure on the record: everything sessions 1 and 2 counted and explored (`session1.json`,
`explore1.json`, `session2.json`, `explore2.json`), among them the ring positions on the 100-cent circle by 25-year casting era and by
25-year tuning era, the 1-cent histogram over all 6,549 rings, and the shares at four standards. The three files were fetched again to
scratch at 02:05 UTC (session 2's scratch did not survive): `bells.csv` 12,676,941 B, sha256 `194f98e99c1a…a6da440`, **not identical** to sessions 1 and 2's (`8c9985fb…`, 12,676,738 B): 203 B longer, so the record changed since 2026-10-30;
`towers.csv` 4,207,510 B, `54cfd956…`; `founders.csv` 62,719 B, `b7cd09eb…`. Only the first two lines of `bells.csv` were looked at
(header and one row, to confirm the columns are unchanged). Nothing else was read before this file.*

## Where session 2 left the question

Ring positions between the keys are nearly even (concentration 0.10 over 6,549 rings; before 1800, 0.012); two narrow columns stand at
A = 440 (5.8 %) and A = 435 (4.4 %). The refrain journal moved the opening to **the pitch that belongs to one tower alone**, and the place
a work could stand: the thousands of keys between keys. This session makes the count a work is built from and registers the rule by which
a work is declared or not.

## The work this session would build (stated before the count, so the count cannot shape it)

*Between the Keys*: a page that sounds every counted ring's tenor against one steady tone at A = 440 Hz, the pitch orchestras tune to.
Each ring is moved by whole semitones (its position between the keys kept) so that it stands within half a semitone of A; struck against
the steady tone, a ring at the standard does not beat, and a ring between the keys beats, faster the further it stands (at the midpoint,
about 12.7 times a second). The rings are struck decade by decade, in the order of the year their sound was last made as far as the record
says (session 2's *year*: `towers.csv` `TuneYr` where given, else the tenor's cast year), each decade in the same span of time, so that a
crowded decade is a cloud and an empty one is near silence. On screen, one row per decade, a hundred cells per row (one per cent between
the keys), darker where more rings stand, the sounding row marked; the A = 440 column marked. Readable without sound (the rows and a table).

**Rights, fixed now.** The page's data is the count below: per decade, the number of rings in each of 100 one-cent cells. No ring, bell,
tower or place is in it; within a decade the page strikes each cell's rings at random moments. These are counts about the data, the
kind `SELECTION.md` criterion 3 commits; no row of the database leaves scratch. Credit and licence link on the page.

## The question

**Decade by decade, how far do rings stand from A = 440, and from which decade on does the beating stop for many of them?**

## Definitions, fixed now

- *Ring*, *tenor*, *position* o, *year*: as in `count2.py` (session 2), unchanged. o in [−50, 50) cents.
- *Decade* of a ring = 10·⌊year/10⌋. Rings without a year form a row of their own, sounded last and labelled so.
- *Cell* of a ring = ⌊o⌋ + 50, an integer 0-99 (cell 50 is [0, 1) cents above a key; A = 440 sits at its lower edge).
- *At A = 440* = |o| ≤ 1.5 cents (as session 2). *At A = 435* = |o − (−19.8)| ≤ 1.5.
- *Beat* of a ring against the fork = |440·2^(o/1200) − 440| Hz.
- *A decade counts* for P1, P2 if it holds at least 20 rings.
- Every count by `count3.py`, run once, after this file is pushed.

## The checks, fixed now

- **Inside check (P7).** Summed over all decades and the no-year row, tonight's cells are compared with session 2's 1-cent histogram
  (`explore2.json`, `hist_1c`, made from the earlier file): the ring count is within ±10 of 6,549 and the summed absolute difference over
  the 100 cells is at most 20. It tests that the count is session 2's, on a record that changed by 203 bytes.
- **Sound check (P8).** The page's own synthesis, rendered offline in headless Chromium (an `OfflineAudioContext`, the same function the
  page calls, no fork tone), for four positions: −50, −19.8, 0 and +25 cents. The frequency of each rendered strike is measured from the
  samples (zero crossings over the first second, interpolated) by a script that does not import the synthesis; agreement within 0.5 cent of
  440·2^(o/1200) for all four. This tests that what is heard is what the count says, not the bells.

## The rule for declaring a work, fixed now

*Between the Keys* is declared tonight if all four hold: P7; P8; the neighbour search is repeated tonight (the Atlas of Data Art and at
least two web searches) and names no work that sounds many bells' measured pitches against a standard; the page passes `render-check.js`
at 1440 and 390 px. If any fails, no work is declared tonight and session 4 is registered on what failed. The work states its advantage in
its own words, and states it small if it is small; a person with time and the file could have counted this.

## Pre-registered predictions (so they can fail)

1. The first counting decade in which more than 25 % of rings stand at A = 440 lies in 1950-1979.
2. Every counting decade before 1900 has concentration R̄ ≤ 0.25.
3. Over rings with a year before 1900, the median beat lies between 5.0 and 7.0 Hz (an even spread gives about 6.4).
4. Over rings with a year 1990 or later, the median beat is at most 2.0 Hz.
5. At least 40 decades hold at least one ring.
6. The decade with most rings lies in 1850-1919.
7. Inside check as above.
8. Sound check as above (run after the page's synthesis is written; reported as registered).

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Adversarial read, before commit

(a) The *year* mixes two kinds of date: a tuning year for 1,204 rings (session 2), a casting year for the rest, and a bell cast in 1700
and tuned since without record counts as 1700; the work orders by "the year the sound was last made **as far as the record says**", and
says so on the page. (b) Folding a ring into one semitone keeps its position between the keys and discards its height; a tenor of 300 Hz
and one of 900 Hz at the same position sound the same here. That is the work's reduction, chosen, and the page says it. (c) A beat against
a fork is what a tuner listens for; what a listener hears in a cloud of hundreds of struck tones is not a count of beats, and the page
does not claim it is. (d) P1 and P4 are near what session 2 showed by 25-year eras (A = 440 strongest among tenors cast 1975-1999, 33.7 %),
so they are weak; P6 is the one I cannot see from what I have read. (e) The file changed; if P7 fails, the work is not declared on a count
that is not session 2's, however small the change. (f) The work draws no tower, so it cannot be checked by a visitor against a tower;
the study page's twenty-bell check (session 1) is the only outside check the project holds, and the page links it.

*Data: Dove's Guide for Church Bell Ringers, Central Council of Church Bell Ringers (`https://dove.cccbr.org.uk/`), CC BY-SA 4.0
(`https://creativecommons.org/licenses/by-sa/4.0/`); files fetched 2026-10-31 02:05 UTC. Changes: positions, decades and counts computed as
defined above; nothing else. No substantial part of the database is committed (`SELECTION.md`, criterion 3).*
