# Project 21 — session 2, pre-registered: the record's lag or the paint's?

*Session of 2026-11-02 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
row of tonight's files was read. What this session saw before writing, so the exposure is on the record: session 1's files
(`SELECTION.md`, `session1.json`, `explore1.json`, `explore1b.json`, `count1.py`); the FAA's NASR subscription page for the cycle effective
2026-10-29 (`https://www.faa.gov/air_traffic/flight_info/aeronav/aero_data/NASR_Subscription/2026-10-29/`), grepped for its links only.
Three files were downloaded to scratch at 02:03:57-02:03:59 UTC and not opened, not even their header lines: OurAirports `runways.csv`
(3,973,355 B, sha256 `d937116b…`) and `airports.csv` (12,755,603 B, `1aab80cc…`), re-fetched because session 1's copies were in a
container that is gone and the files change nightly; and the FAA's `29_Oct_2026_APT_CSV.zip` (8,502,128 B, `6e1e422f…`, from
`https://nfdc.faa.gov/webContent/28DaySub/extra/`). What I believe of the FAA file's names and columns is **conjecture** from memory of
the NASR CSV layout until the files show it.*

## Why this question

Session 1 found that 28 % of 12,178 runways carry a number the magnetic field has left behind, nearly all trailing it, and that the
numbers fit the field of 2002 best (the United States' 1996). It could not say whose lag that is: a crowd-kept database that has not
caught up with the paint, or the paint itself. The United States holds 5,704 of session 1's 12,178 runways and its regulator publishes
every public and private landing facility in the NASR subscription, a US government work (17 U.S.C. § 105; no terms on the page restrict
it — the page was grepped, not read whole, so that is a conjecture). NASR also records, per airport, a **magnetic variation and the year
it was taken** (believed). That is a second, official statement of the field, with its own date. So tonight asks two things of one file:
whether the official number agrees with the crowd's, and what year of field the regulator's own record says it is.

## Session 2's question

**For the United States: (a) where OurAirports' number is out of step, does the FAA's record carry the same number (the lag is the
official record's, and as far as any record can say, the paint's) or an updated one (the lag is the crowd's)? (b) In which year was the
FAA's recorded magnetic variation taken, how far does it stand from the field of that year and of 2026, and do the numbers agree with the
field the FAA itself declares?**

Definitions, fixed now; written to the columns found if they differ from my belief, with the change logged before the count:

- *A_US* = session 1's analysed set A (definitions in `SELECTION.md`, unchanged, computed by session 1's own functions imported from
  `count1.py`) on tonight's OurAirports files, restricted to airports with `iso_country` = US.
- *FAA airport* = one row of the NASR airport base file (believed `APT_BASE.csv`), key `SITE_NO`, identifier `ARPT_ID`. An A_US runway's
  airport is joined to it by OurAirports' `local_code` = `ARPT_ID`; failing that, `ident` = `ARPT_ID`; failing that, an `ident` of four
  characters beginning with `K` with the K removed. Unjoined airports counted.
- *FAA runway* = one row of the runway file (believed `APT_RWY.csv`) whose `RWY_ID` has the form `n[LCR]/m[LCR]` with numeric ends;
  helipads, waterways and lettered runways counted and left out. Its two ends (believed `APT_RWY_END.csv`, `RWY_END_ID`, `LAT_DECIMAL`,
  `LONG_DECIMAL`, `TRUE_ALIGNMENT`).
- *Match* = within the joined airport, the FAA runway whose axis differs least from the A_US runway's axis (bearings compared modulo 180°),
  if that difference is ≤ 3°; when two or more FAA runways are within 3° (parallels), the one whose low-end number or high-end number equals
  either of OurAirports' numbers, and failing that the one whose midpoint (where both ends carry coordinates) lies nearest. The FAA axis is
  the bearing between its end coordinates where both are given, else the low end's `TRUE_ALIGNMENT`. Unmatched runways counted.
- *FAA number for the A_US runway* = the number of the FAA end whose heading lies within 90° of OurAirports' low end's direction (so the two
  are compared on the same end). *Agree* = the same number, suffix ignored.
- *Out of step (OA)* = session 1's definition on OurAirports' number; *out of step (FAA)* = the same with the FAA number, field IGRF-14 at
  2026.0 at OurAirports' midpoint.
- *Declared variation* V = the FAA airport's magnetic variation in degrees (believed `MAG_VARN`, with `MAG_HEMIS` E/W; E positive) and its
  year Y (believed `MAG_VARN_YEAR`). Airports without both are counted and left out of (b).
- *Variation error at its year* = V − D(Y) at the FAA airport's reference point (believed `LAT_DECIMAL`, `LONG_DECIMAL`), D from IGRF-14 on
  1 January of Y; for Y < 1900 not computed. *Variation lag today* = D(2026) − V, signed in the sense the field moved.
- *In step against the declared field* = |θ − V − 10·n_FAA| ≤ 5° (θ the OurAirports true bearing as in session 1).
- Counts per runway (not per airport) except for (b)'s variation statistics, which count each joined airport once.
- Every count by `count2.py`, run once, after this file and that script are pushed.

## Pre-registered predictions (so they can fail)

1. The FAA airport file holds at least 15,000 rows; the runway file at least 18,000.
2. At least 90 % of A_US runways are joined to an FAA airport and matched to an FAA runway.
3. Of matched runways, OurAirports' number agrees with the FAA's for at least 95 %.
4. Of matched runways out of step (OA), the FAA number is the same as OurAirports' for at least 85 % (the lag is the official record's, not
   the crowd's).
5. The out-of-step share with the FAA number lies between 25 % and 38 % (session 1 found 31.7 % for the US on OurAirports' numbers).
6. At least 80 % of joined airports carry both a declared variation and its year.
7. The median year Y of the declared variation lies in 1980 … 2010.
8. The declared variation agrees with IGRF-14 at its own year within 1.0° for at least 80 % of airports with Y ≥ 1900.
9. At least 90 % of matched runways are in step against the declared field (the numbers agree with the field the FAA itself declares).
10. The median |variation lag today| is at least 1.0°.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## The check, fixed now

- **The join, by hand:** ten matched pairs drawn with seed 20261102; for each, OurAirports' row and the FAA's runway row are read side by
  side (identifier, both numbers, both axes) and recorded as agree / disagree in `check2.json`. Pass: ten of ten are the same physical
  runway (same airport, axes within 3°).

## Instruments (unchanged)

T2 assemblage analysis, entry 2; T4 following-journal, session 2. Failure criteria as in `SELECTION.md`.

## Adversarial read, before commit

(a) OurAirports may import its US rows from NASR. If so, agreement (P3, P4) shows only that the two records share a source, and says
nothing of the paint; the session cannot see paint, and a number in NASR is the regulator's statement of what is painted, not a
photograph. That limit stands and is written on the page. (b) The declared variation's year may be the year of an isogonic chart the
airport's figure was read from, not a survey at the field; the "error at its year" then measures the chart's interpolation as well as the
field. (c) Matching by axis within 3° can pair a runway with a different runway at an airport with crossing runways only if their axes
differ by ≤ 3° — then they are parallels, handled by the number and distance rule; a wrong pair among parallels would read as disagreement
and is what the hand check looks for. (d) The FAA file holds facilities closed or private; nothing is filtered by use, because OurAirports'
A already holds what it holds. (e) P9 tests numbers against a declared field that may have been chosen to fit the numbers; that is not
circular for the question asked (do the record's two statements agree with each other), and it is not a measurement of the planet.
(f) Nothing tonight is for navigation; the page says so.

*Data: OurAirports, public domain, fetched 2026-11-02 02:03 UTC; FAA NASR 28-day subscription, cycle effective 2026-10-29, US government
work; IGRF-14 (IAGA) via `ppigrf` 2.1.0. Not for navigation.*
