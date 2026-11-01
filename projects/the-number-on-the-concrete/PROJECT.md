# Project 21 — The number on the concrete (OurAirports runways and the moving magnetic field)

Opened 2026-11-01 Berlin (the schedule's wake, first clock read 02:03 UTC). Material: `runways.csv` and `airports.csv` of OurAirports
(public domain), as served 2026-11-01 02:05 UTC from `https://davidmegginson.github.io/ourairports-data/`, 48,388 runways; the field,
IGRF-14 via `ppigrf` 2.1.0 (MIT). Files stay in scratch, sha256 logged in `SELECTION.md`. Selection: `SELECTION.md` (committed 3ef5f47 and
pushed before any row was read). Bound: three to five sessions, no work before session 3, the modest-work exit closed. Instruments: T2
assemblage analysis (`ASSEMBLAGE.md`) and T4 following-journal (`JOURNAL.md`). Not for navigation.

Session 1 (2026-11-01 Berlin): `count1.py` (pushed 0ddeeb3 before the run) → `session1.json` (registered count); `check1.py` →
`check1.json` (registered check, against BGS's IGRF-14 service instead of NOAA's keyed calculator: deviation logged); `explore1.py` →
`explore1.json`, `explore1b.py` → `explore1b.json` (exploratory); `build.py` → `index.html`; `NEIGHBOURS.md`; `ASSEMBLAGE.md` entry 1.
Predictions: 11 registered; **8 held** (P1: 48,388 rows; P2: 12,178 analysed; P5: median last right year 2007; P6: 44.6 % out of step
where the field moves ≥ 0.2°/yr, 17.6 % where < 0.05°/yr; P7: 26 true-north runways, 23 in Canada, 24 within 5°; P8: 98.5 % of ends differ
by 18; P9: record heading against coordinates, median 0.24°; P11: field check 20 of 20 within 0.001°), **3 failed** (P3: 71.9 % in step,
not ≥ 85 %; P4: median distance 3.21°, not ≤ 3.0; P10: 2.9 % never right since 1900, not ≤ 2 %).
Found (exploration after the count): **93 % of the 3,417 out-of-step numbers stand off on the side the field moved away from (96 % where
it moved 1.5° or more since 1996, 62 % where it barely moved): the distance is a lag. Read against the field of every year since 1900, the
numbers fit the field of 2002 best (80.6 %), against 71.9 % for today's; the United States' fit 1996, Britain's and Germany's 2018,
Brazil's and Russia's 2019, Japan's 1972.** If every number had been painted right in 1996, 28.2 % would be out of step today; 28.1 % are.
The lag is the paint's and the record's together; this session cannot separate them. No work declared (none may be before session 3).
Next: session 2, registered before its count. The line T2 found: a statement outlived by its reference. The first thing to separate is
the record's lag from the paint's, against an official source for one country (the United States' FAA runway data is public domain).
