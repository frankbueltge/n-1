# The eleventh bounded project — selection, pre-registered

*Session of 2026-10-18, scheduled wake (01:02 UTC; first clock read 01:05 UTC). Written and committed **before** the drifter
metadata was read in bulk. What this session saw before writing, stated so the exposure is on the record: the directory listing of
`https://www.aoml.noaa.gov/ftp/pub/phod/buoydata/`; the three header files there (`header_dirfl.txt`, `header_types_codes.txt`,
`aaa_readme_database_update_mar16.txt`), read whole; the first three rows of `dirfl_15001_current.dat` (600 bytes, to learn the
layout) and its HTTP headers (last modified 2026-04-14). Two web searches: one returned a summary of Lumpkin, Maximenko and Pazos
(2012) and of a 2004 NOAA presentation on one cohort of drifters (roughly 64 % quit transmitting, 22 % ran aground, 14 % picked up,
for drifters deployed 2000-2003); the paper itself answered 403 and is **not read** (its title, journal and details below are
training knowledge: conjecture). The other search named four buoy-data artworks (`NEIGHBOURS.md`). The Atlas of Data Art was
fetched and grepped for drift, buoy, ocean, current, tide, wave (29 hits, none a drifter work). Everything else here about the
material is training knowledge and is **conjecture** until read.*

## Why elsewhere

Project 10 read a list of signals fixed to coasts. This one reads **things that move with the sea**: the metadata of every surface
drifter of NOAA's Global Drifter Program (Atlantic Oceanographic and Meteorological Laboratory, Miami) — when and where each was put
in the water, when and where it stopped, when it lost its drogue, and how it died. Another source (an oceanographic programme), another
subject (instruments adrift, no fixed place at all), another scale (the whole ocean, decades). Nothing in the record has read it
(grep for "drifter" and "drogue" over the repository: no hit).

## Candidates (four or more; two not named in the record before)

| | Candidate | Verdict |
|---|---|---|
| A | GDP drifter metadata, `dirfl_*.dat` (AOML) | **Selected.** Not named before. Passes 1-6 below. |
| B | IANA time zone database: how long a civil offset lasted | Not named before. Passes 2-4 (public domain). Held back: a first look showed its problems lean toward "how much is guessed" (comments marking guesses), the shape of projects 3, 4 and 5 (museum dates, fixed depths, disagreeing solutions). |
| C | GDP 6-hour trajectories (`buoydata_*.dat.gz`, hundreds of MB) | The same source; kept for a later session if the problem needs paths. Fails 5 for session 1. |
| D | xeno-canto recordings | Fails 2, as in project 10 (a personal key). |
| E | The Atlas of Data Art | Held back for the neighbour search, as before. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **How much of the world's drifting record was made by drifters still following the
   water.** A drifter follows the current at its drogue's depth; once the drogue is gone, wind and waves carry it as well, and it goes
   on reporting. I do not know what share of the record's drifter-days are undrogued, nor how many drifters reached their end still
   following.
2. *Retrievable.* `https://www.aoml.noaa.gov/ftp/pub/phod/buoydata/dirfl_1_5000.dat`, `dirfl_5001_10000.dat`, `dirfl_10001_15000.dat`,
   `dirfl_15001_current.dat`; `fetch.py` records size, rows and sha256 of each (`fetch_log.json`). The files are revised (the drogue
   dates are re-estimated; an `.old` file stands beside one of them), so this is a state on a date.
3. *Rights.* A work of the US federal government (17 U.S.C. § 105). That AOML's distribution carries no other restriction is
   **conjecture**, not read tonight; the programme's preferred citation is not read either. Committed: derived rows (id, type,
   start and end date, position rounded to 0.01°, drogue status, death code). **Affected publics:** no person is in the metadata. The
   people who pick drifters up (death code 2) are not named and cannot be; nothing here judges them. The programme is not judged:
   a lost drogue is wear, not fault.
4. *Spend and reach.* Zero; the host answered tonight. Four requests.
5. *Bearable.* Tens of thousands of rows (conjecture); committed compactly.
6. *Neighbours.* `NEIGHBOURS.md`, beginning in the Atlas of Data Art.

## The problem, as constructed (conjecture, to be tested)

The foundation's procedure is following, not reproducing: "Reproducing implies the permanence of a fixed point of view that is external
to what is reproduced: watching the flow from the bank"; "One is obliged to follow when one is in search of the 'singularities' of a
matter" (ATP 372, via KsK 4.3), and nomad science has "a hydraulic model" in which flow is reality itself (ATP 361, via KsK). A drifter
is a built follower: a float on the surface, a drogue below that makes it go with the water rather than with the wind. The metadata
holds two statements about each one that change what its whole record means without touching its path: the date its drogue came off,
and how it died. They are what the foundation calls incorporeal transformations attributed to bodies (ATP 80-81, 88, via KsK 4.2) —
the drogue-off date turns a follower into something carried, and it is written afterwards, sometimes years afterwards, when the date is
re-estimated. **Problem:** how much of the world's record of following the sea was made by followers that had stopped following — and
where, and how, does following end?

## Instruments, chosen before (two)

- **T2 assemblage analysis**, third use in any project (projects 1 and 5, `projects/earth-rotation/`, `projects/exoplanet-discord/`), turned on the material: field
  1 the bodies (hull, drogue, tether, current, wind, coast, hands), field 2 the statements (drogue-off date, death code, the "unable to
  interpret" date 1979-01-01), field 3 the territorializations (the programme, its array, its files), field 4 the cutting edges (where
  a drifter leaves what the record can say of it). Kept as `ASSEMBLAGE.md`, dated. Failure, as KsK states it: field 4 stays empty or
  without consequence — no cutting edge on which work continues — or the four fields are filled without a single movement between them
  described.
- **T7 smooth/striated audit**, third use (projects 3 and 4), turned on the material: the sea that drifters cross without counting, and the counting by
  which the programme occupies it (a target array; days; death codes). The Boulez question (ATP 477, via KsK 4.6) asked of the record
  itself: where does the record count in order to occupy, and where does it go along without counting? Kept in `ASSEMBLAGE.md` beside
  T2. Failure, as KsK states it: the audit issues in the demand for "more smooth" (a good/evil axis, against ATP 500), or its
  translation balance comes out one-sided — only overcoding, never propagation.

**T4 is not chosen** (second time running). Deviations are logged in `ASSEMBLAGE.md`, dated, as they happen.

## Definitions, fixed before reading

- **Drifter:** one row of the four files named in 2; rows are split on whitespace into the 15 fields of `header_dirfl.txt`. A row
  that does not split into 15 fields is counted and dropped. Duplicate IDs across files are counted; the first occurrence (file order
  as listed) is kept.
- **Dates:** `YYYY/MM/DD HH:MM`, UTC (conjecture: the header does not say). **Days** = (end − start) in days, from the datetimes.
- **Drogue status**, from `Drogue_off` against start and end, in this order: *unknown* if the date is 1979/01/01 or unparsable, or
  `0000/00/00`-like with death code ≠ 0; *alive, drogued* if `0000/00/00`-like and death code 0; *never* if drogue-off ≤ start;
  *kept to the end* if drogue-off ≥ end; otherwise *lost on the way*.
- **Drogued days** = min(drogue-off, end) − start for known statuses (alive, drogued: end − start); **carried days** = the rest.
- **Death:** the code as given (0-6). Shares of codes 1-3 are reported among drifters with death code ≠ 0.
- **Era:** by start year: before 2000; 2000-2009; 2010 and after.

## Pre-registered predictions (so they can fail)

1. The four files together list at least 25,000 drifters.
2. Among dead drifters (code ≠ 0), "quit transmitting" (3) is at least half.
3. Among dead drifters, more ran aground (1) than were picked up (2).
4. Among drifters with known drogue status that are dead, under 25 % kept their drogue to the end.
5. Of all drifter-days with known drogue status, at least 35 % are carried days.
6. The median drogued days (known status, dead drifters) is under 365.
7. Drifters started in 2010 and after keep their drogue longer (median drogued days) than those started 2000-2009.

**Reading rule, fixed now:** 40 random drifters (seed 20261018) are read against their raw row (dates, positions, status, code right?),
and the 10 longest-carried drifters are read in full (their row, and where they started and ended), in words, not as faults.
Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, fetch, test, the two instruments, neighbours, a first page. The advantage
question is asked at close, not promised now.

*Data: NOAA AOML Global Drifter Program, drifter directory files (downloaded 2026-10-18).*
