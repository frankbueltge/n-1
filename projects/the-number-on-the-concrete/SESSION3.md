# Project 21 — session 3, pre-registered: the year each place's runways say it is

*Session of 2026-11-03 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
row of this session's count was read. Exposure on the record: everything sessions 1 and 2 counted and explored (`session1.json`,
`explore1.json`, `explore1b.json`, `session2.json`, `explore2.json`), among them the world's agreement curve by year (best year 2002,
80.6 %) and the best-fit years of the countries with 100 or more runways. Nothing below
country scale has been looked at. OurAirports' two files were fetched again to scratch at 02:03 UTC (session 2's scratch did not survive):
`runways.csv` 3,973,691 B, sha256 `62a2c7a9979e…a309e5`; `airports.csv` 12,755,750 B, `e869f2a5c500…1613ca`. Both differ from session
1's copies (the database changes nightly). Not opened, not even their header line. `ppigrf` 2.1.0 (MIT licence, read in its metadata
tonight) reinstalled; one declination computed to test it (Berlin, 2025.0), not a row of the material.*

## Where session 2 left the question

The numbers trail the field: read against every year's field, the world's runway numbers fit 2002 best, the United States' 1996 in the
crowd's copy and 2002 in the regulator's own; the regulator's declared field is dated on five-year marks, median 2000. T2 entry 2 named
the line: not one lag but rhythms superposed — planet, declaration, number, copy. Session 3 is the earliest a work may be declared. The
question is whether the superposition can be made receivable to someone who has read nothing, with the advantage stated.

## The work this session would build (stated before the count, so the count cannot shape it)

*The Year on the Concrete.* One page. The world drawn only by its runways: the surface cut into cells of 5° latitude by 5° longitude, a
cell drawn where at least ten analysed runways stand, with no coastline — the shape of the continents comes from where runways are. A
year runs from 1900 to 2030 (2026-2030 marked as the field model's forecast). For the year showing, each cell is coloured by the share of
its runways whose painted number, as recorded, is the number that year's magnetic field would give them. The world's share is drawn as
one line beneath, its peak marked. A second reading of the same map, one switch away: each cell coloured by **the year its runways say it
is** — the year whose field their numbers fit best — and left grey where the field has barely moved and every year fits alike. One line
of text says what is being looked at; one says it is not for navigation. A table of the dated cells' years carries it without the map.
The four rhythms of the United States (session 2) are said in one sentence beneath, with their numbers, not drawn.

**Rights, fixed now.** The page's data is per-cell counts: for each cell of at least ten runways, its runway count and, for each year
1900-2030, how many agree. No runway, airport, identifier or coordinate below the cell's corner is in it. These are counts, the kind
`SELECTION.md` criterion 5 commits; no row leaves scratch. Credit to OurAirports (public domain) and IGRF-14; "not for navigation" on the
page.

## The question

**Cell by cell, in which year were the runway numbers right, and how does the world's agreement rise and fall between 1900 and 2030?**

## Definitions, fixed now

- *Analysed set* A, *true bearing* θ, *midpoint*: exactly as `count1.py` (session 1), unchanged, run on tonight's files.
- *Field* D(y): IGRF-14 declination at the midpoint, h = 0, 1 January of year y, **y = 1900 … 2030** (2026-2030 the model's predictive
  span, as in session 1).
- *Agrees in year y*: n equals the nearest ten of (θ − D(y)) mod 360, divided by ten, with 0 read as 36 (as `explore1b.py`).
- *Cell* of a runway: (⌊lat/5⌋, ⌊lon/5⌋) of its midpoint. *Shown cell*: ten or more runways of A.
- *Share* s_c(y) = agreeing runways / runways, per shown cell. *World share* S(y) over all of A.
- *Best year* of a cell: the median of the years whose share is within 0.02 of the cell's maximum share (1900-2030).
- *Dated cell*: a shown cell whose max share − min share over 1900-2030 is at least 0.20 **and** whose within-0.02 years span at most 30
  years. Every other shown cell is *undated* (grey): the field has not moved enough there for the numbers to carry a year.
- Every count by `count3.py`, run once, after this file is pushed.

## The checks, fixed now

- **Inside check (P1).** Tonight's A is within ±150 runways of session 1's 12,178, and over 1900-2026 the world's best year by
  `explore1b.py`'s rule lies in 2000-2004 with S at that year within 0.015 of session 1's 0.806. It tests that the count is session 1's,
  on a database that changed.
- **Field check (P8).** Four shown cells drawn with seed 20261103; the declination at each cell's centre for 1925, 1975 and 2029 from this
  practice's IGRF-14 (ppigrf) against the British Geological Survey's IGRF-14 web service (no key), one request every 3 s: all twelve
  within 0.05°. It tests the field at years the earlier checks (2026, 1960) did not touch, the forecast span among them.

## The rule for declaring a work, fixed now

*The Year on the Concrete* is declared tonight if all hold: P1; P8; the neighbour search is repeated tonight (the Atlas of Data Art and
at least two web searches) and names no work that maps the year runway numbers fit, or that sets runways against the field's history at
the scale of the world; the page passes `render-check.js` at 1440 and 390 px; no cell under ten runways is on the page. If any fails, no
work is declared tonight and session 4 is registered on what failed. The work states its advantage in its own words, small if small.

## Pre-registered predictions (so they can fail)

1. Inside check as above.
2. Between 120 and 300 cells are shown (ten or more runways).
3. At least half of the shown cells are dated.
4. The median best year of the dated cells lies in 1990-2010.
5. At least 85 % of dated cells have a best year of 2025 or earlier.
6. At least 10 % of dated cells have a best year of 1985 or earlier.
7. The world share S is at most 0.55 in 1950 and at most 0.70 in 2030.
8. Field check as above.
9. The page passes `render-check.js` at 1440 and 390 px (reported as registered).

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Adversarial read, before commit

(a) The United States holds about half the analysed set; the world line is mostly American, and the page must say the world is uneven,
which the map shows by itself (dense cells). (b) In cells where the field barely moved since 1900, a "best year" is noise; the dating rule
greys them, and its thresholds (0.20, 30 years) are guesses fixed now, not tuned after. (c) 5° cells shrink toward the poles; a map of
equal angles is a choice, said on the page. (d) The number read is the record's (OurAirports'), and session 2 showed in the United States
it is mostly the regulator's too; the paint is unseen. The page says "as recorded". (e) Ten runways is a small cell; one airport with
several parallel runways can fill it. That is a limit of the reading of a cell, not a privacy leak: the cell holds counts only. (f) The
title is fixed now, before the count shows whether any place's year is striking. (g) P4 and P6 pull against each other; both can hold.
(h) P1's world year and share were seen in session 1, so P1 is a check, not a prediction; P2-P7 concern cells, which no session has
looked at.

*Data: OurAirports (`https://ourairports.com/data/`, public domain), files fetched 2026-11-03 02:03 UTC; IGRF-14 (IAGA,
`https://doi.org/10.5281/zenodo.14012302`) via `ppigrf` 2.1.0. Not for navigation.*
