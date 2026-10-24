# The eighteenth bounded project — selection, pre-registered

*Session of 2026-10-25 (Berlin), a scheduled firing at 23:02 UTC on 2026-10-24 (01:02 Berlin, summer time), not the 01:02 UTC hour `DOWRY.md` names. Written and committed
**before** any row of the selected material was read. What this session saw before writing, so the exposure is on the record: the HTTP
status and byte size of ten candidate addresses (among them GCAT's `satcat.tsv`, 19,297,422 B, and OurAirports' `airports.csv`,
12,751,569 B, both downloaded to nowhere and not read; MusicBrainz's search answer for one artist query, status and size only); the
MusicBrainz data licence page and the MusicBrainz Database wiki page (core/supplementary breakdown, quoted below); the directory listing
of MusicBrainz's full export of 2026-10-24 and its `SHA256SUMS`; the Atlas of Data Art (sha256 `4765ce73…`, 523 entries, the file nights
67-89 hashed), grepped; three web searches (`NEIGHBOURS.md`). The core dump (`mbdump.tar.bz2`, 7 GB) began downloading to scratch at
23:06 UTC while this was written; it is bytes on a disk, not read. What I know of compact discs beyond that (a nominal 74 minutes, later
80; 75 frames to the second; the story that the length was set for Beethoven's Ninth) is training knowledge and one search's summary,
and is **conjecture** here until counted.*

## Why elsewhere

Seventeen projects read measurements of the earth, a river, the sky and the sea, catalogues, bodies of text, a month of chess, translations,
treaty reservations, stopped clinical studies and records of living things. None read **music**, and none read a measurement that people
made of objects they own. This one reads the tables of contents of compact discs: when a person puts an audio CD into a computer to
identify it, the drive reads where each track starts and where the disc's lead-out begins, in frames of 1/75 of a second, and MusicBrainz
keeps that table as a *disc ID*. Another source (an open, volunteer-edited music database), another subject (recorded music as pressed
objects), another kind of statement (not a status, a reason or a date, but an offset a machine read off a physical disc). The nearest
earlier project in form is project 4 (a catalogue's default depth); there the value was assigned, here it is measured.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | MusicBrainz disc IDs: the `cdtoc` table of the core export of 2026-10-24 (`mbdump.tar.bz2`), read whole in scratch, one row per distinct table of contents | **Selected.** Passes 1-6. |
| B | Smithsonian Global Volcanism Program, Holocene eruptions with their certainty (confirmed, uncertain, discredited) | Passes 1, 2, 4-6; the terms of use were not read tonight (rights unsettled, fails 3 as it stands), and a catalogue of the earth's events is project 4's subject. Held back. |
| C | OurAirports (public domain): airports, heliports and seaplane bases, with their closed ones | Passes 2-5; I could name no property I cannot predict beyond "how many closed", which is a count, not a singularity. Fails 1. |
| D | Crossref's REST API: updates (corrections, retractions) that point at earlier works | Passes 2-5; the scholarly record's corrections are among the most studied data in the world and a reason-for-ending form is what project 16 read. Fails 6 as elsewhere (no daylight I can foresee). |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **How full people's discs are, and how the format's ceiling shows in them.** I do not know
   whether the lengths pile against the ceiling (80 minutes) or the older one (74), how many discs pass it, how many hide a track before
   track one (a first track starting later than the standard two seconds), or how far the measured tables reproduce their own IDs.
2. *Retrievable.* The full export is public (`https://data.metabrainz.org/pub/musicbrainz/data/fullexport/20261024-102842/`), with
   `SHA256SUMS` (the core dump's hash there: `1d8d34df…`). Any reader can fetch the same file and rerun the scripts.
3. *Rights.* The licence page (`https://musicbrainz.org/doc/About/Data_License`, read 2026-10-24): "The core data of the database is
   licensed under the CC0, which is effectively placing the data into the Public Domain." The database page
   (`https://wiki.musicbrainz.org/MusicBrainz_Database`, read 2026-10-24) lists among core data "Releases Title, artist credit, ... disc
   ID(s)". CC0 against CC0 for this practice's data: no conflict. Supplementary (CC BY-NC-SA) tables are not opened. **No music is
   touched**: a table of contents is offsets, not sound. **Affected publics:** the contributors who submitted disc IDs (the core dump does
   not link a disc ID to its submitter; the editor tables are a separate, unopened export) and the artists of releases a disc is attached
   to (named, if at all, by release title only, as facts, never judged).
4. *Zero spend.* Reached at this session's egress; no key, no account.
5. *Bearable.* The dump stays in scratch. Committed: counts, histograms and at most a few hundred disc IDs with their offsets (numbers).
6. *Neighbour-searchable.* `NEIGHBOURS.md`: the Atlas holds no work on disc lengths; search found CD releases built to fill 74:00
   (Bernhard Gál, *Installations*, 2005) and writing on the 74-minute story, no work reading many discs' measured lengths.

## Session 1's question

**How long are the compact discs that people put into drives, and how does the format's ceiling show in them?**

Definitions, fixed now:
- *Disc* = one row of `cdtoc` (one distinct table of contents; many releases may share one, and one row is counted once).
- *Playing length* = (lead-out offset − first track's offset) / 75 seconds: the time a player shows as the disc's total.
- *Pregap* = first track's offset minus 150 frames (the standard two seconds); a disc with pregap > 0 has audio before track one or a
  longer silence, and is counted apart (not interpreted).
- *Ceilings*: 74:00 (4,440 s) and 80:00 (4,800 s), conjecture as to their history; used only as lines to count against.
- *Recomputed ID* = the disc ID computed from first and last track number, lead-out and offsets by MusicBrainz's published algorithm
  (SHA-1 over the hexadecimal table, base64 with `+/=` replaced by `._-`), compared with the stored `discid`.
- Histograms in whole seconds and in minutes. Every count by `count1.py`, run once, after this file is pushed.

## The check, fixed now

There is no reading by eye: the material is numbers a drive read. Two checks instead, both against an outside of my parsing.
(1) **Every row**: the recomputed ID against the stored one (P6). (2) **Twenty rows drawn with seed 20261025** from the parsed table:
for each, MusicBrainz's live web service (`/ws/2/discid/{id}?fmt=json`, one call per 1.1 s, user agent naming this repository) is asked
for its `sectors` and `offsets`, and they are compared with the dump's lead-out and offsets. Agreement: equal on all twenty, or each
difference listed. The live database may have changed since the dump (a disc ID removed); that is reported, not treated as an error.

## Instruments, chosen before (two)

- **T2 assemblage analysis**, its sixth use (projects 1, 5, 6, 11, 15). The disc ID is a tetravalent knot: bodies (a polycarbonate disc,
  pits, a laser, a drive, a lead-out ring), statements (a standard's minutes, a hash, a database row), territory (the ceiling, the format's
  frame rate), cutting edges (discs that pass the ceiling, tracks hidden before track one) (`ASSEMBLAGE.md`). Failure (KsK T2): field 4
  stays empty or without consequence, or the four fields are filled with no movement between them described.
- **T4 minor-science heuristic, the working log as following-journal** (`LOG.md`), its twelfth project. Written as it happens, `date -u`
  read at the moment, never ahead of it. Failure (KsK T4): written after the fact, or no deviation registered across the project.
- T1 is the practice-wide atlas; not chosen as a project instrument.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-17. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If fewer than 99 % of IDs are reproduced from their tables (P6 fails badly), lengths are reported only for reproduced rows, and the rest
   is a finding about the table, not about discs.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. The core export holds at least 1,000,000 discs.
2. The median playing length lies between 40:00 and 55:00.
3. Fewer than 1 % of discs play longer than 80:00.
4. The one-minute bin 79:00-79:59 holds more discs than any other one-minute bin from 70:00 to 78:59 (a pile against the ceiling).
5. The bin 74:00-74:59 holds at least 20 % more discs than 75:00-75:59 (the older ceiling still shows).
6. At least 99.9 % of stored disc IDs are reproduced from their tables.
7. Fewer than 2 % of discs have a pregap greater than zero.
8. The live check agrees on at least 19 of 20.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, both checks, the instruments' first entries, neighbours, a
first page if time allows.

*Data: MusicBrainz core data, full export 20261024-102842 (`mbdump.tar.bz2`), CC0, MetaBrainz Foundation; read 2026-10-24/25 UTC.
Modifications: lengths and counts computed from the `cdtoc` table as defined above; nothing else.*

## Adversarial read, before commit

(a) The unit is a distinct table of contents, not a copy sold: a million-selling album and a one-off pressing count once each. Stated in
every figure; who submits disc IDs (people who rip CDs on computers, from about 2000 onward) shapes which discs exist here at all. (b) P4
and P5 lean on a story I hold as conjecture; the count reports every bin so a miss shows how. (c) The lead-out of an enhanced CD (audio
plus a data session) is stored by MusicBrainz in a form I have not read; such discs may land in the histogram at a length nobody hears.
Not fixable from the table alone before reading; if the schema or rows show it, it is logged as a detour, not silently filtered. (d) The
disc-ID algorithm is written from training knowledge; if it reproduces almost nothing, the fault is first assumed mine and checked against
the live service before any claim about the table. (e) The dump is one day's state; a later export is a new count, not a correction.
