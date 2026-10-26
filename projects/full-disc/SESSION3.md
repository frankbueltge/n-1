# Project 18 — session 3, pre-registered: the sets the frame cuts

*Session of 2026-10-26 (Berlin), the schedule's wake (first clock read 01:04 UTC, 02:04 Berlin). Written and committed **before** any
row of this session's material is read. Exposure on the record: sessions 1 and 2's counts (`session1.json`, `session2.json`,
`explore2.json`), among them that 502 discs end at frame 333,000, that 475 of them are attached to a release, that 74 % of those carry the
secondary type Audiobook and 19 % sit on CD-R, and the titles of the top release groups at the 74 edge (book titles, seen in session 2).
The table definitions of `medium` and `medium_cdtoc` re-read tonight from `admin/sql/CreateTables.sql` (master, 174,858 B, the size
session 2 fetched). The neighbour search repeated (`NEIGHBOURS.md`, session 3). The core dump is downloading again to scratch; it is
bytes on a disk, not read. I have no count of how many media any of these releases has, or how long their other discs are.*

## The question

Session 2 found the commonest compact-disc length to be one frame, 74:00:00, held mostly by audiobooks, and read it as a program's cut
at the last address. That reading is a conjecture until the rest of each release is read: **a cut at a fixed length leaves every disc of
a set full but the last, and the last holds what is left over.** So: **in the releases that hold a disc ending at 74:00:00, are the
other discs cut at the same frame, and is the last one the remainder?**

## Definitions, fixed now

- *Frame disc* = a row of `cdtoc` whose lead-out offset is exactly 333,000. *Address* = a lead-out offset in frames.
- **R** = every release that has at least one medium (via `medium_cdtoc → medium`) carrying a frame disc.
- For a release in R, its *media* = every row of `medium` with that release, in `position` order; *last* = the highest position. A
  *set* = a release in R with two or more media.
- A medium's *address* = the lead-out of its attached `cdtoc` rows: 333,000 if any of them is a frame disc, otherwise the largest. A
  medium with no attached row is *unmeasured* and is counted apart, never given a length.
- *At the frame* = a medium whose address is 333,000.
- Counts by `count3.py`, run once, after this file is pushed. No release title, artist or person field is opened; release MBIDs and
  medium positions are the only identifiers committed.

## The check, fixed now

Twenty releases drawn from R, seed 20261026, from the parsed tables. For each, MusicBrainz's live web service
(`/ws/2/release/{mbid}?inc=discids&fmt=json`, one call per 1.5 s, user agent naming this repository; a 503 is asked again once after 5 s,
inside the registration) is asked for its media; for each position, the set of disc IDs is compared with the dump's. Agreement: equal
number of media and equal disc-ID sets at every position. The live database may have changed since the export; that is reported.

## Predictions (so they can fail)

1. R holds at least 100 releases.
2. At least 80 % of releases in R are sets.
3. **The cut.** Among the measured media of sets that are not last, at least 70 % are at the frame.
4. **The remainder.** Among the measured last media of sets, at most 10 % are at the frame.
5. The median address of measured last media of sets that are not at the frame lies between 25:00 and 50:00 (112,500-225,000 frames):
   the remainder is spread, not a fixed tail.
6. Of measured last media of sets, at least 95 % have an address of at most 333,000 (the remainder is never longer than the cut).
7. Among all `cdtoc` lead-outs of at least 270,000 frames (60:00), 333,000 is the single commonest.
8. The check agrees on at least 19 of 20.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## How this session ends (rule 1 of `SELECTION.md`: work or put-back)

**The work is declared if** P3 holds and the check agrees on at least 18 of 20. Otherwise the project is put back with its balance; the
form below is not redesigned after seeing.

**The work, if declared — *The Last Address*:** one page. Every set in R is one row; each of its media is a bar from zero to its address,
in position order; a single vertical line stands at 74:00:00. Bars at the frame in one colour, last media in another, unmeasured media as
an empty outline of no length. Each row links to the release's page in MusicBrainz. No title, artist or sound on the page. Below, the
counts and a table readable without the picture; nothing is fetched while it is looked at.

**The advantage, stated so it can fail.** A listener hears a disc end; a player shows minutes and seconds. The cut shows only at the
table's own resolution, one seventy-fifth of a second, and only across many sets read together: the work reads every disc of every
release that holds the frame, against the frame. A person with time and the export could do the same; the claim is that the reading is
whole and to the frame, and it is small. It **fails** if P3 fails: then 74:00:00 is not a cut that sets share, and the page would show
an accident.

## Instruments (as chosen in `SELECTION.md`)

T2 entry 3 (`ASSEMBLAGE.md`), written before the count. Failure as before. T4: `LOG.md`, clock read at the moment.

## Adversarial read, before commit

(a) A release may hold media that are not CDs (a booklet, a DVD) and so never measured; they are counted as unmeasured, not as remainders.
(b) A contributor may attach a disc ID to a wrong medium position; the check tests a sample, not every row. (c) P5 and P6 assume the last
position is the last part of the book; a set may carry a bonus disc at the end. Stated, not corrected. (d) A set whose middle discs are
unmeasured can still pass P3 only on the media measured; the share of unmeasured media is reported beside it. (e) "Program" stays a
conjecture: the tables show where discs end, not what made them end there; the page will say "cut at", never name a tool. (f) P7 reads
the whole table, so it tests whether 74:00:00 is singular or one of several fixed cuts; if another frame wins, that is a finding, not a
failure of the work's rule.

*Data: MusicBrainz core data, full export 20261024-102842 (`mbdump.tar.bz2`), CC0, MetaBrainz Foundation. Modifications: the selection
and definitions above; nothing else.*
