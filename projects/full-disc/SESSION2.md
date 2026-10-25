# Project 18 — session 2, pre-registered: where the ceiling is, and which discs meet it

*Session of 2026-10-25 (Berlin), the schedule's wake (first clock read 01:03 UTC, 02:03 Berlin: the clocks went back an hour at 01:00
UTC tonight). Written and committed **before** any row of this session's material was read. Exposure on the record: session 1's counts
(`session1.json`, among them the playing-length histogram by second, which names the crests at 73:58 and 79:57/79:58); the table
definitions of `medium_cdtoc`, `medium`, `medium_format`, `release`, `release_country`, `release_unknown_country`, `release_group`,
`release_group_primary_type`, `release_group_secondary_type` and `release_group_secondary_type_join` in MusicBrainz's
`admin/sql/CreateTables.sql` (master branch, fetched tonight, 174,858 B); and the standard below, read in full for the clauses quoted.
The core dump is being downloaded again to scratch (session 1's scratch did not survive); it is bytes on a disk, not read.*

## The standard, read before the count

ECMA-130, 2nd edition, June 1996, *Data interchange on read-only 120 mm optical data disks (CD-ROM)*
(`https://www.ecma-international.org/wp-content/uploads/ECMA-130_2nd_edition_june_1996.pdf`, 1,578,188 B, sha256 `576fb91e…`). It is
the freely readable standard for the compact disc's data form; the audio form is "according to IEC 908" (clause 20.3), which is not freely
readable and was not read. What the free text says, clause by clause:

- **No time ceiling.** The standard names no maximum playing time. Its limit is a place on the disc: the user data zone "extends between
  diameter d7 and d8", with d7 = 50,0 mm and **d8 = 116 mm max**, and the lead-out zone beyond it, d9 = (d8 + 1 mm) min (clause 8.6).
- **Two tolerances that make the time:** track pitch "1,6 µm ± 0,1 µm" (11.3); scanning velocity "between 1,20 m/s and 1,40 m/s" (11.4).
- **The address is time from the start, including the gap.** "The address of a Section ... is given as the elapsed time from the start of
  the User Data Area to that Section ... called absolute time ... with a resolution of 1/75 of a second" (21); it "is set to zero in the
  first Section of the first Information Track of the User Data area" and "increases until the end of the Lead-out Track" (22.3.3.5). A
  first data track "shall start with a Pause of 150 Sections (2 s)" (20.2).
- **The table of contents** gives each track's start "in absolute time" and, under pointer A2, "the address of the first Section of the
  Lead-out Track" (22.3.4).

**Arithmetic from those numbers, not from the standard's words** (marked as computed; anyone can redo it): a spiral between radii 25 and
58 mm at pitch p, read at velocity v, plays π(58² − 25²) mm² / p / v. At the nominal pitch 1.6 µm and the slowest velocity 1.20 m/s that is
**4,482 s, 74:42**; at the tolerance extremes (1.5 µm, 1.20 m/s) **4,780 s, 79:40**; at 1.6 µm and 1.40 m/s, 64:01. On these numbers an
80:00 disc lies outside this standard's tolerances, and 74:00 lies inside them with 42 seconds to spare. Whether IEC 908 says otherwise is
not known here.

So the word "ceiling" changes for this session: the standard's limit is in millimetres, and the table of contents states it as an
address. The stored lead-out offset is that address in frames: MusicBrainz stores the first track at 150 frames (00:02:00), the 2 s gap
counted (session 1, 87.4 % of discs).

## The question

**Where, to the frame, do the discs' lead-outs stop; and which discs sit at the two edges against the discs around them?**

## Definitions, fixed now

- *Disc*, *playing length* and *recomputed ID* as in `SELECTION.md`. *Address* = the stored lead-out offset, in frames; *address second*
  = address // 75 (4,440 = 74:00, 4,800 = 80:00).
- *Bands*, by address second: **A74** = 4,440 (74:00.00-74:00.74); **B80** = 4,795-4,799 (79:55-79:59); comparisons **C70** = 4,200-4,379
  (70:00-72:59) and **C76** = 4,560-4,739 (76:00-78:59).
- *A disc's releases* = every release reached by `cdtoc → medium_cdtoc → medium → release`. A disc with none is counted as orphan and left
  out of shares. *Format* = the `medium_format` name of the medium; a disc on media of several formats counts as "mixed". *Compilation* =
  any attached release group carries the secondary type named "Compilation". *Primary type* = the release group's primary type, "mixed"
  if several. *Year* = the earliest `date_year` over the disc's releases in `release_country` and `release_unknown_country`; discs with
  none are left out of years.
- Counts by `count2.py`, run once, after this file is pushed. Release titles may be named as facts in exploration (the top release
  groups of A74); no artist is named or judged; no person field is opened.

## The check, fixed now

Twenty discs drawn from A74 and B80 together, seed 20261025, from the parsed table. For each, MusicBrainz's live web service
(`/ws/2/discid/{id}?fmt=json`, one call per 1.1 s, user agent naming this repository) is asked for the releases attached; their MBIDs
are compared with the dump's. Agreement: equal sets on all twenty, or each difference listed. The live database may have changed since
the export; that is reported, not treated as an error.

## Predictions (so they can fail)

1. **The edge is the address.** Among address seconds 4,300-4,899, the largest fall from one second to the next (count(s) / count(s+1),
   seconds with count(s+1) ≥ 1) is from 4,799 to 4,800.
2. **Sharper in address than in playing time.** count(4,799) / count(4,800) in address seconds exceeds session 1's playing-second fall
   498 / 167 = 2.98.
3. **74 sits at, not below.** Among address seconds 4,380-4,499, the commonest is 4,440 (74:00).
4. **To the frame.** Among addresses 330,000-336,000, the single commonest frame is exactly 333,000 (74:00:00).
5. **Not the compilations' edge.** The compilation share of B80 is at least 1.5 times that of C76. (Conjecture behind it: discs filled to
   the edge are made by gathering.)
6. **The older edge is older.** The median year of A74 is at least three years earlier than the median year of B80.
7. **Pressed, not burnt.** In both A74 and B80, at least 90 % of discs with one format are on the format named "CD".
8. **The check agrees** on at least 19 of 20.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Instruments (as chosen in `SELECTION.md`)

T2 entry 2 (`ASSEMBLAGE.md`) is written before the count, from the standard: field 2 gains the address and field 3 the millimetres.
Failure as before: field 4 without consequence, or no movement described. T4: `LOG.md`, clock read at the moment.

## Adversarial read, before commit

(a) P1 and P3 were written with session 1's playing histogram known, and both follow from it if most first tracks start at 150 frames; they
test whether that arithmetic holds when the first offset is taken out, and P2 and P4 are the parts the arithmetic does not settle. (b) The
geometric arithmetic ignores the lead-in and treats the spiral as filling the zone exactly; it is a bound from the standard's numbers, not
a measurement of any disc, and is not used to classify discs. (c) The bands are not equal in width (one second, five seconds, three and
three minutes); only shares are compared across them, never counts. (d) A disc ID is attached to releases by contributors; a share of
compilations measures what people attached, and a disc attached to a wrong release carries that release's year. Stated, not checked
beyond the live check. (e) Years of release are not years of pressing; a 2005 reissue of a 1987 disc counts as its earliest attached
release.
