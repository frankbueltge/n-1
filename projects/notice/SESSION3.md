# Project 23, session 3 — the hours shown wrong, and when they were found, pre-registered

*Session of 2026-11-10 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). Written and committed **before**
`count3.py` was run. What this session saw before writing, so the exposure is on the record: everything sessions 1 and 2 published
(`session1.json`, `explore1*.json`, `session2.json`, `check1.json`, `check2.json`, `JOURNAL.md`, the study page); tonight, in addition,
the key list of `session2.json` and the first ~400 characters of each key printed once at 02:02 UTC (among them the first rows of
`episodes_rows`, the totals by kind, the longest episode, the opening of `by_year`, `release_dates`). Not seen: any episode grouped by its
correcting release, any lag distribution, any count of what was already lived and not yet found wrong at a given date.*

## Where session 2 left the question

On every day since 1996 one release of the tz database was the newest. Session 2 counted the hours in which it showed, for some region,
an offset for the present that the newest release of all (2026f) now says was wrong: 918,348 region-hours in 103 of 312 regions, in 505
episodes. Four fifths were found wrong more than a year after they were lived. Session 2's T5 opening test moved session 3 there: the
larger kind is not news that came late, but **the past found wrong**. The work must show both times at once — when an hour was lived,
and when the file learned it had been wrong about it.

## The question

**For each hour the file showed wrong, how long after it was lived did the file learn that — and at any date since 1997, how many
already-lived hours was the file wrong about without yet knowing it?**

## The work this session would build (stated before the count, so the count cannot shape it)

*The Hours Shown Wrong.* One page, one square figure. Across: the time the hours were lived, 1997 to 2026. Up: the date of the release that
first set them right, 1997 to 2026. **Every episode is one horizontal line, from the first to the last hour it was wrong, at the height of
the day it was corrected.** The diagonal is the present: a line on it was set right as it was lived; the further above, the later the file
learned. Three colours for the three kinds of session 2: news after the clocks moved, a change carried at the wrong moment, the past
found wrong. A slider (and Play) moves a date T: at T, every line already corrected is drawn; every hour already lived but not yet
corrected is drawn faint, below the diagonal's row at T, and **one number counts it: the hours the file was wrong about on that day
without knowing it.** Pointing at a line names the region (its tz identifier), the hours, the offset shown and the offset now held, the
release current and the release that corrected it. One line says what is being looked at, in words for someone who has read nothing.
A table carries the same counts by year without the picture.

**Rights, fixed now.** The page's data are the 505 episodes of `session2.json` (tz identifiers, instants, offsets, release names) and
counts. The tz database is public domain (IANA); region identifiers are place names, not persons. No person, no device and no population
is on the page, and the page says that no device is in this material.

## Definitions, fixed now

- *Episode*, *kind*, *correction*, *lag*, *region*, *release date*: exactly as `SESSION2.md`, read from `session2.json`
  (`episodes_rows`, `release_dates`). Nothing is recomputed from the releases except in the check below.
- *Corrected at* of an episode: `release_dates[corr]` at 00:00 UT.
- *Hidden at T* (region-hours): over all episodes, the hours of [t0, min(t1, T)) when corrected-at > T. That is: lived by T, wrong, and
  not yet set right by any release dated on or before T.
- *Lag weighted by hours*: each episode's `lag_days` counted once per region-hour.
- Every count by `count3.py`, run once, after this file is pushed. The page is built from `session3.json` and `session2.json` only.

## The check, fixed now (floor rule 3)

**P11, the correction re-read.** Eight episodes drawn with seed 20261110 from the past-found-wrong episodes of `session2.json`. For each,
τ = t0 + min(1800, (t1 − t0)/2). The three releases involved — the one current at t0 (`rel`), the correcting one (`corr`), and 2026f — are
fetched again and compiled with `zic` and session 1's helper, and read with `zdump -v` (not count2's reader). Holds if: `rel` shows
count2's `shown` at τ, 2026f shows count2's `final` at τ, they differ, and `corr` shows the final's offset at τ. At least 7 of 8.

## The rule for declaring a work, fixed now

*The Hours Shown Wrong* is declared tonight if all hold: P1; P11; the neighbour search is repeated tonight (the Atlas of Data Art and at
least two web searches) and names no work that draws the errors of a time-zone database by the time lived against the time they were
found; the page passes `render-check.js` at 1440 and 390 px. If any fails, no work is declared tonight and session 4 is registered on
what failed. The work states its advantage in its own words, small if small.

## Pre-registered predictions (so they can fail)

1. **Inside check.** 505 episodes; their hours sum to session 2's 918,348.3 (within 0.1). Seen before: a check, not a prediction.
2. The episodes were corrected by between 60 and 160 distinct releases.
3. The release that corrected the most region-hours is dated 2014 or later.
4. The hours-weighted median lag exceeds five years.
5. Fewer than 15 % of wrong region-hours were set right within 90 days of the start of their episode.
6. At least 25 regions have episodes of two or more kinds.
7. The hidden curve reaches its maximum before 2010-01-01.
8. Hidden at 2016-01-01 exceeds 300,000 region-hours.
9. Hidden at 2026-11-07 is zero only by construction (every episode is corrected by 2026f, released 2026-10); hidden on the first day of
   2026 is under 1,000 region-hours.
10. The page passes `render-check.js` at 1440 and 390 px (reported as registered).
11. The correction re-read as above: at least 7 of 8.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Instruments (chosen in session 1, continued)

- **T4** (`JOURNAL.md`): detours logged as they occur, clocks read from `date -u` at the moment.
- **T5** (`JOURNAL.md`): the session's refrain balance, with the opening test asked of the work itself — is it opened at a point the
  material made, or where the neighbour's question presses?

## Adversarial read, before commit

(a) **The final release is the only judge.** A line's height is the day of the first release that agreed with 2026f; if 2026f is itself
wrong, so is the whole upper half. Said on the page. (b) **A release date is not the day anyone learned.** The list may have known weeks
before; a device received it later. Heights are the file's, not a person's. (c) **Episodes, not hours, are lines**: one line can stand
for 187,680 hours (Vostok) or for one; line length carries the hours, so the eye weighs them. (d) **Region is a tz identifier**, not a
country or a population; Antarctica/Vostok is a station. The page names identifiers as identifiers. (e) **Releases before 2000f compile
only through the practice's own helper**; the 1997-2000 corner rests on it (`SESSION2.md` (d)). (f) **P9 leans on the definition**:
nothing can be hidden after the final, so only its first half is a prediction. (g) **P3 leans on the longest episode** (Vostok, corrected
by 2023d, 187,680 hours), seen before writing: if no other release corrected more, P3 holds by what is already known. Weak, reported so.
(h) **The hidden curve counts only what 2026f calls wrong**: hours a later release will find wrong are hidden still, and not on the page.

*Data: IANA Time Zone Database, releases 1993g-2026f, `https://data.iana.org/time-zones/releases/`, public domain; fetched 2026-11-07 and
2026-11-09 (sha256 of the concatenation `69c85cb0…`), and for the check again tonight.*
