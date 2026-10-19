# The twelfth bounded project — selection, pre-registered

*Session of 2026-10-19, scheduled wake (01:02 UTC; first clock read 01:05 UTC, 03:05 Berlin). Written and committed **before** any
edition was read in bulk. What this session saw before writing, so the exposure is on the record: Natural Earth's download page for
1:10m cultural vectors (`https://www.naturalearthdata.com/downloads/10m-cultural-vectors/`) and its terms of use; the 34 zip files
fetched to scratch by `fetch.py` (`fetch_log.json`); of their contents only the field names, the number of rows per file for four
files (default 258, India 248, ISO 249, China 246, top-level-countries 333) and the version (5.1.1). No polygon was intersected, no
attribute value read. The Atlas of Data Art was fetched (sha256 `4765ce73…`, 523 entries, the file nights 67-70 hashed) and grepped;
one web search for border artworks (`NEIGHBOURS.md`). What I know of the world's disputed territories is training knowledge and is
**conjecture** here until read.*

## Why elsewhere

Projects 10 and 11 read lights fixed to coasts and floats adrift on the sea; the practice has worked clocks twice and the sky three
times. This one reads **land and who it belongs to**: Natural Earth's world map of countries in its default edition, which "shows
de facto boundaries by default according to who controls the territory", and its **33 point-of-view editions**, which "show the
worldview for several dozen countries according to de jure boundaries (as prescribed by the home country's law and/or local
conventions)" — "between 246 and 258 countries, depending on who's counting" (download page, read 2026-10-19). Another source (a
cartographic collective), another subject (sovereignty, territory), another scale (all land). Nothing in the record has read it
(grep for "Natural Earth", "sovereign", "disputed" over `projects/`: no hit).

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | Natural Earth admin-0 countries, default and 33 POV editions | **Selected.** Passes 1-6. |
| B | Natural Earth breakaway and disputed areas (~100 features) | The same source; kept as a reading aid for session 1's reading rule, not the material. |
| C | IANA time zone database | Time a third time; rejected on "elsewhere", as in projects 9 and 11. |
| D | Glottolog's descriptive status of languages | Languages were touched in project 6 (Unicode, CLDR); held back. |
| E | NASA Meteorite Landings | The sky a fourth time; rejected. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **How much of the world's land changes country depending on whose map is opened.**
   I do not know the area, nor how many pieces it falls into, nor which edition redraws most.
2. *Retrievable.* `https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip` and
   `ne_10m_admin_0_countries_{pov}.zip` for 33 editions; `fetch.py` records size and sha256 (`fetch_log.json`). Version 5.1.1.
3. *Rights.* "All versions of Natural Earth raster + vector map data found on this website are in the public domain"
   (`https://www.naturalearthdata.com/about/terms-of-use/`, read 2026-10-19). Committed: derived numbers and simplified geometry.
   **Affected publics:** every person living in land drawn differently, and the states and peoples whose claims these are. Settled
   now, before opening: **the practice draws no border and judges no claim.** It reports what one publisher draws for each viewer, in
   that publisher's labels; Natural Earth's editions are Natural Earth's reading of each country's law, not the countries' own
   statements, and every page says so. No edition is called right or wrong; the default (de facto) edition is one view among 34 and
   the page says that too. No person is in the material.
4. *Spend and reach.* Zero; 34 requests answered tonight.
5. *Bearable.* 34 files of about 4.7 MB; the overlay runs in minutes (estimate).
6. *Neighbours.* `NEIGHBOURS.md`, beginning in the Atlas of Data Art.

## The problem, as constructed (conjecture, to be tested)

The foundation's sentence on territory: "it is the mark that makes the territory" (ATP 315, via KsK 4.5), and on the map: it is
"open and connectable in all of its dimensions; it is detachable, reversible, susceptible to constant modification" and can be
"reworked by individuals, groups and social formations" (ATP 12, via KsK 4.1). A world map of countries is usually met as a tracing —
one picture, the way things are. Natural Earth publishes it as 34. **Problem:** how much land is drawn in a different country
depending on who is counting, in how many pieces, and where does the world's map stop being one map? The ATP vocabulary
(hard segmentary lines, ATP 195, via KsK 4.7) is used for the borders as lines; it is never used to say a border should move.

## Definitions, fixed before reading

- **Edition:** one of the 34 files. Its **units** are its rows; geometry made valid and projected to a cylindrical equal-area plane on
  the authalic sphere (R = 6371.0072 km; `lib.py`). Areas are **estimates** at the file's vertex density.
- **Owner key:** each unit of an edition is keyed to the default unit it overlaps most (`lib.match`). A unit split into parts keeps its
  key (a split is not a move); a unit absorbing another's land is keyed to the larger.
- **Moved land** in an edition: land of default unit D lying in an edition unit whose key is not D; land of D lying in no unit
  (**left**); edition land lying in no default unit (**added**). `lib.moved`, tried on invented shapes (`test_lib.py`).
- **Contested land:** the union of moved land over the 33 editions = land where the 34 editions do not all agree (the default being one
  of them). **Owners per place:** the number of distinct keys (with "none") a place has across the 34, estimated on a 2 km equal-area
  point grid inside the contested land.
- **Piece:** a polygon of moved land of at least 1 km² (smaller ones count in area, not as pieces).

## Instruments, chosen before (two)

- **T4 following-journal**, tenth project to use it (projects 1-9 all kept one), after two projects (10, 11) that left it out and
  whose accounts both estimated what its absence cost. Kept as `JOURNAL.md`, written as the session goes: detours,
  abandonments, changes of direction, counterfactuals marked as estimates. Failure (KsK T4): written after the fact, or no deviation
  from plan logged across the project.
- **T6 lines-and-dangers self-analysis**, second use in any project (project 9), turned on the project: the rigid lines (the borders,
  the editions, the default), the molecular cracks (alignment shifts, slivers), the lines of flight; and the danger audit on the
  practice's own line — above all **Clarity, the self-appointed judge** (ATP 228, via KsK 4.7): a machine counting contested land is
  one step from ruling on it. Kept as `LINES.md`. Failure (KsK T6): the audit names only others' dangers and never the practice's
  own, or no audit has a consequence.

## Pre-registered predictions (so they can fail)

1. At least 30 of the 33 point-of-view editions move at least 100,000 km² relative to the default.
2. The contested land (union) is at least 1,000,000 km².
3. The edition that moves most land is Argentina's.
4. At least 10,000 km² of land has three or more distinct owners across the 34 editions.
5. The ISO edition moves less land than the median of the 31 national editions.
6. At least one edition leaves at least 1,000 km² of the default's land in no unit.
7. The contested land falls into at least 50 pieces of 1 km² or more (union, after dissolving).

**Reading rule, fixed now:** the 10 largest contested pieces and 20 random ones (seed 20261019) are read against the attributes of
the units involved (names, `NOTE_ADM0`, `NOTE_BRK`, `FCLASS_*`) and against Natural Earth's breakaway-and-disputed-areas file: is
the piece what the count says it is, or an artefact (slivers, a coastline drawn differently)? Read in words, never as a ruling.
Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, fetch, rules, the run, the two instruments, neighbours, a first page.
The advantage question is asked at close, not promised now.

*Data: Natural Earth, 1:10m Admin 0 – Countries and point-of-view variants, version 5.1.1 (downloaded 2026-10-19), public domain.*
