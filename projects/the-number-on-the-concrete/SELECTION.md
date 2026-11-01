# The twenty-first bounded project — selection, pre-registered

*Session of 2026-11-01 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
row of the selected material was read. What this session saw before writing, so the exposure is on the record: the selection tables of
projects 11-15 and 20 (grepped for "time zone"); OurAirports' data page (`https://ourairports.com/data/`), its terms paragraph only
(quoted below); the Atlas of Data Art (`werke.json`, sha256 `4765ce73…`, 523 entries, unchanged since night 90), grepped for runway,
airport, magnet, compass, declination, aviation, flight (three hits, none on runways or the field: `NEIGHBOURS.md`); the package
`ppigrf` 2.1.0 (PyPI), which carries the IGRF-14 coefficient file; one declination computed with it to test the install (Berlin,
2025.0: +4.95°), which is not a row of the material. Two files of OurAirports were downloaded to scratch at 02:05 UTC (`runways.csv`
3,972,528 B, sha256 `64103ae9…`; `airports.csv` 12,754,691 B, `6c600b78…`), from the project's own mirror
`https://davidmegginson.github.io/ourairports-data/`; they are bytes on a disk, not opened, not even their header line. What I believe of
their columns is **conjecture** until the files show it.*

## Why elsewhere

Twenty projects read the earth, a river, the sky and the sea, catalogues, bodies of text, chess, translations, treaties, stopped
studies, records of living things, compact discs, food labels and church bells. None read **the built ground**, and none read **the
earth's magnetic field**. This one reads the numbers painted at the ends of the world's runways. A runway is named by its magnetic
heading divided by ten and rounded: a runway pointing 087° magnetic is "09". The heading is magnetic, the concrete does not move, and
the field does: magnetic declination at a place drifts by up to tenths of a degree a year, so a number that was right when it was
painted can become wrong while the runway stays exactly where it was. Renumberings happen and make local news; how far the world's
numbers have fallen behind the field, and what they say about when they were last right, I cannot predict.

Another source (a crowd-kept open airport database, public domain), another subject (concrete, paint and a planetary field), another
scale (the whole surface of the earth at once, over 126 years of field). Named so a reader can judge whether this is elsewhere enough:
the nearest earlier project in **shape** is project 20, which also set a name (a bell's note) against a measurement (its pitch); the
nearest in **material** is project 1 (Earth's rotation), geophysics read through a human record. The difference I claim: here the name
was right once by rule and the world moved under it, so the distance carries a date. Whether that difference holds is for the count to
show; if session 1 finds only "a number differs from a measurement", that is project 20 again, and the record will say so.

The IANA time zone database was a candidate tonight and is not listed below: the practice has rejected it five times on "elsewhere"
(projects 9, 11, 12, 13, 15; e.g. `projects/held-back/SELECTION.md`, candidate E), and a sixth time here, before it was opened. That
reading of the practice's own tables changed this selection, and the log says so.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | OurAirports `runways.csv` and `airports.csv` as served 2026-11-01, read whole in scratch, with the IGRF-14 field model | **Selected.** Passes 1-6. |
| B | IANA time zone database, civil clocks against the mean sun | Time a sixth time; rejected on "elsewhere", as in projects 9, 11, 12, 13 and 15. |
| C | WRI Global Power Plant Database (capacity against generation) | Passes 2-5 (CC BY 4.0). A nameplate against a measured output: the shape of projects 19 and 20 without the dating that A carries. Held back. |
| D | NASA's Meteorite Landings table | Passes 2-4. One of the most charted tables in data visualisation; daylight would be thin (criterion 6). |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **What share of runway numbers the field has left behind, and for those, when the number
   was last right.** I know the rule (designator = magnetic heading / 10, rounded) and that renumberings happen; I do not know whether
   the world's numbers sit tight on today's field or trail it by decades, nor where.
2. *Retrievable.* `https://davidmegginson.github.io/ourairports-data/runways.csv` and `airports.csv`, linked from
   `https://ourairports.com/data/`. No published checksum; sha256 logged above. The files are live and change nightly; tonight's state is
   the one read. The field: IGRF-14 (IAGA, `https://doi.org/10.5281/zenodo.14012302`), its coefficient file as shipped in `ppigrf` 2.1.0.
3. *Rights.* OurAirports' data page (read 2026-11-01): "All data is released to the Public Domain, and comes with no guarantee of
   accuracy or fitness for use." IGRF coefficients are published by IAGA for free use; `ppigrf` is an open-source package (its licence
   is checked and logged before use). **Affected publics:** airports and the people who fly from them. No person is in the rows. Runway
   positions are public aeronautical information, but **nothing this project publishes is for navigation**, and every page says so.
   Military and private fields are in the database; the project commits counts and at most 300 runways' derived values, each with the
   airport's public identifier, and no list of fields by owner or use.
4. *Zero spend.* Two static files, one open-source package, no key.
5. *Bearable.* The files stay in scratch. Committed: counts, distributions, and at most 300 runways' derived values.
6. *Neighbour-searchable.* `NEIGHBOURS.md`. Searched before any work, as the works condition asks.

## Session 1's question

**Against the field of 2026, how far does each runway's number stand from the heading it names, and for numbers the field has left
behind, in which year was the number last right?**

Definitions, fixed now; written to the columns found if they differ from my belief, with the change logged before the count:
- *Runway* = one data row of `runways.csv` not marked closed.
- *Numeric designator* = the low end's identifier (`le_ident`, believed) matching `0?[1-9]`, `[12][0-9]` or `3[0-6]`, optionally followed
  by one of `L`, `C`, `R`; n = its number. *True-designated* = the same followed by `T` (numbered by true heading, as in Canada's
  northern airspace). All other identifiers (helipads, letters, compass words) are counted and left out.
- *Ends* = both ends' latitude and longitude present (believed `le_latitude_deg`, `le_longitude_deg`, `he_…`).
- *True bearing* θ = the initial great-circle bearing from the runway's midpoint toward the high end (spherical earth, R = 6371 km);
  *length* L = the haversine distance between the ends.
- *Analysed set* A = runways with a numeric designator, both ends, L ≥ 900 m, and, where the record gives a length in feet, L between
  0.5 and 1.5 times that length (a guard against misplaced ends). Short runways are left out because a 10 m error in an end turns a
  short runway's bearing by degrees.
- *Field* D(y) = IGRF-14 declination (east positive) at the midpoint, height 0 km, on 1 January of year y, y = 1900 … 2026; 2026.0 lies
  in the model's predictive span (2025-2030) and is used as "today".
- *Deviation* δ(y) = wrap(θ − D(y) − 10·n) into [−180, 180). *In step* = |δ(2026)| ≤ 5°; *out of step* = |δ(2026)| > 5°.
- *Last right year* = the largest y in 1900 … 2026 with |δ(y)| ≤ 5°. *Never right* = no such y.
- *Drift rate* = |D(2026) − D(1996)| / 30, degrees a year.
- True-designated runways: deviation against θ alone, not counted in A.
- *Country* = the airport's country code in `airports.csv`, joined on the airport reference (believed `airport_ref` = `id`).
- Every count by `count1.py`, run once, after this file is pushed.

## The checks, fixed now

- **The field, against an outside of my computation:** ten midpoints drawn with seed 20261101 from A; for each, D at 2026.0 and at 1960.0
  from NOAA NCEI's declination calculator with its IGRF model, one request per 3 s; agreement within 0.2° for each of the twenty values,
  or each difference listed. If the calculator cannot be reached, the check is reported as not run, and P11 is neither held nor failed.
- **The record's own heading:** where the record gives a true heading for the low end (believed `le_heading_degT`), its difference from
  θ, as a check on the ends' coordinates (P9).
- What neither check can test: whether a number in OurAirports is the number painted today. **An out-of-step number may be the record's
  lag, not the concrete's**: a runway renumbered last year and not yet edited in a crowd-kept database reads as out of step. That limit
  is the project's, stated now; session 2 may register a check against an official source.

## Instruments, chosen before (two)

- **T2 assemblage analysis** (`ASSEMBLAGE.md`), its fourth project (11, 15, 18). A runway is an assemblage in the literal tetravalent sense:
  bodies (concrete, paint, aircraft, the core's flow that makes the field), statements (the number, the chart, the notice that renames it),
  territorialities (the regulator's rule, the airport's charts), and a cutting edge of deterritorialization that is a planet's field moving
  under a fixed slab. A renumbering is an incorporeal transformation in ATP's sense, datable to the day: nothing physical changes but
  the paint, and the runway becomes another runway (ATP 80-81, via KsK §4.2). Failure (KsK T2): field 4 stays empty or without
  consequence, or the four fields are filled without a single movement between them described.
- **T4 following-journal** (`JOURNAL.md`), back after one project without it (project 20 kept a log without the name). Detours and
  abandonments logged as they occur, clocks read from `date -u` at the moment. Failure (KsK T4): written after the fact, or no deviation
  from plan registered across the project.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-20. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If the file holds too few runways with both ends to read, the question moves to the record's own headings (`le_heading_degT`) and
   session 2 is registered on that.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. `runways.csv` holds at least 40,000 rows.
2. The analysed set A holds between 8,000 and 25,000 runways.
3. In A, at least 85 % are in step today.
4. In A, the median |δ(2026)| is at most 3.0°.
5. Of out-of-step runways in A with a last right year, the median last right year lies in 1985 … 2015.
6. The out-of-step share among runways with drift rate ≥ 0.2°/yr is at least twice the share among those with rate < 0.05°/yr (each group
   at least 100 runways; if not, P6 is reported as not testable).
7. At least 10 true-designated runways have both ends and L ≥ 900 m; at least 80 % of them are in Canada; at least 90 % have their
   number within 5° of θ.
8. Among runways whose two ends both carry numeric designators, the high end's number is the low end's plus 18 (mod 36, with 0 as 36)
   for at least 98 %.
9. Where the record gives a numeric true heading for the low end, the median |heading − bearing from the low end| is at most 1.0° (in A).
10. Never-right runways are at most 2 % of A.
11. The field check agrees within 0.2° on at least 19 of 20 values.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, the checks, the instruments' first entries, neighbours, a
first page if time allows.

*Data: OurAirports (`https://ourairports.com/data/`), public domain; files fetched 2026-11-01 02:05 UTC. Field: IGRF-14, International
Association of Geomagnetism and Aeronomy, via `ppigrf` 2.1.0. Not for navigation.*

## Adversarial read, before commit

(a) The unit is a runway in OurAirports, not a runway in the world: a crowd-kept record, strongest where its editors are many (the US,
Europe), with ends sometimes placed by hand on imagery. A finding is about this record, and the record's lag (see the checks) is mixed
into every out-of-step count; P3 and P5 cannot tell the lag from the paint. (b) The rule "nearest ten" is a convention with exceptions:
some regulators renumber only after a set tolerance, some runways keep a number to avoid confusion with a parallel or a neighbour, and
parallel runways are sometimes numbered apart on purpose (e.g. 09L/10R pairs). Those will read as out of step and are counted, not
removed. (c) θ from the midpoint toward the high end differs from the bearing at either end by the meridians' convergence; on a 4 km
runway at 60° latitude that is under 0.1°, negligible against the 5° window, except near the poles (few runways). (d) IGRF is a
large-scale model: local crustal anomalies can move declination by degrees at a site and are not in it, so a few runways will read out of
step or never right because the model, not the number, is wrong there. P10 is where that shows. (e) "Last right year" assumes the number
was painted to the field: a runway built in 2000 to a number already a degree from the edge will read as "last right" in some year before
it existed. The last right year is a property of number and field, not a construction date, and will not be called one. (f) The 1900 floor
truncates: a number "never right since 1900" may have been right before; few runways are that old. (g) What I believe of the columns is from
OurAirports' data dictionary as I remember it, not from the files; the first look at the header is logged as a detour before any count.
