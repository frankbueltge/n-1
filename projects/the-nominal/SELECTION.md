# The twentieth bounded project — selection, pre-registered

*Session of 2026-10-29 (Berlin), a third wake on the date (first clock read 18:00 UTC, 19:00 Berlin). Written and committed **before**
any row of the selected material was read. What this session saw before writing, so the exposure is on the record: The Session's help
and API pages (thesession.org), and the refusal of its data dump's address (GitHub, outside this session's reach, 403); Dove's Guide's
pages *Downloads* (its licence paragraph, quoted below), *About*, *Help: Bell details* and *Help: Conventions used*, read for terms and
field conventions only; three web searches, result lists and summaries only (`NEIGHBOURS.md`); the Atlas of Data Art (sha256
`4765ce73…`, 523 entries, unchanged since night 90), grepped. Four files of Dove's Guide were downloaded to scratch at 18:03-18:04 UTC
(`bells.csv` 12,676,738 B, sha256 `8c9985fb…`; `towers.csv` 4,207,440 B, `b9534c01…`; `founders.csv`; `frames.csv`); they are bytes on a
disk, not opened, not even their header line. What I believe of their columns is **conjecture** until the files show it. One web
search's summary reported figures from Dove's own "bells by nominal" pages (e.g. 14,594 bells in collections of 8, mean 1057.8 Hz):
seen, not verified, and named here because it touches P1 and P2.*

## Why elsewhere

Nineteen projects read the earth, a river, the sky and the sea, catalogues, bodies of text, a month of chess, translations, treaty
reservations, stopped clinical studies, records of living things, the measured tables of compact discs and the numbers on food labels.
None read **sound**, and none read **metal**. This one reads the church bells listed in *Dove's Guide for Church Bell Ringers*: their
weights, the nominal frequency measured from each, and the note the record names each by. Another source (a ringers' society's guide,
compiled since 1950), another subject (cast bronze hung to be rung), another kind of statement: a pitch measured from a sounding object
beside a note the record says it *assigns by the bell's position in a major scale*, not by its sound (Dove, *Help: Bell details*: "The
note we show for each bell is based on the key note of the ring ... and the position of each bell within the ring"). The nearest earlier
project in form is project 18 (a measured property of many objects); the nearest in kind is project 19 (a record that writes a number
the object may not carry) — named so a reader can judge whether this is elsewhere enough. I judge it is: the sound is the material here,
and the record's assignment is one question about it, not the project's only one.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | *Dove's Guide for Church Bell Ringers*, `bells.csv` and `towers.csv` as served 2026-10-29, read whole in scratch | **Selected.** Passes 1-6 under the rights clause below. |
| B | The Session (thesession.org), Irish dance tunes and the many settings people transcribe of each | Passes 1 and 6. Fails 2 as it stands: the weekly dump lives on GitHub, refused at this session's egress; the API serves one tune at a time. Fails 3: no licence for the data found on the help or API pages. |
| C | U.S. National Bridge Inventory (public domain) | Passes 2-5; the built world, elsewhere. Its singularity I can name (recorded years of construction, ratings on 0-9 scales) is a record's grid again, the shape of project 19 one session later. Fails "elsewhere" as to the problem. |
| D | The XKCD colour survey (colour names people typed) | Passes 1 and 6 weakly; its best-known reading is by its own publisher (Munroe, 2010, training knowledge, not looked up), and its licence was not found tonight. Fails 3 as unsettled and 6 as to daylight. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **How far each bell's measured nominal stands from the note the record names it by, and
   whether that distance has a shape — by era, by founder, by place in the ring.** Bill Hibbert reports from 31 historic peals that old
   founders tuned by the strike note, not the nominal, so that old trebles' nominals sit sharp, "stretch tuning of around 1/3 of a
   semitone in the octave" (`https://www.hibberts.co.uk/stretch-tuning-of-old-style-bells/`, from the search summary, not yet read in
   full). Whether thousands of bells in Dove show it, I cannot predict. Nor how tightly weight predicts pitch.
2. *Retrievable.* `https://dove.cccbr.org.uk/bells.csv`, `https://dove.cccbr.org.uk/towers.csv`, listed on
   `https://dove.cccbr.org.uk/downloads`. No published checksum; sha256 logged above. The files are live and change; tonight's state is
   the one read.
3. *Rights.* The downloads page (read 2026-10-29): "Data is licensed under the Creative Commons Attribution-ShareAlike 4.0 International
   License. ... If you remix, transform, or build upon the data, you must distribute your contributions to the data under the same
   license as the original." Project 19's selection rejected the OEIS on CC BY-SA "as it stands"; this selection settles the same licence
   differently, and says so: **no substantial part of the database leaves scratch.** Committed are counts, fits and histograms (facts
   about the data, not the data), and per-bell fields for at most 300 bells (the check's twenty and any drawn for a page), each linked to
   its Dove page; every page and file credits "Dove's Guide for Church Bell Ringers, Central Council of Church Bell Ringers, CC BY-SA 4.0"
   with a link to the licence and the changes made. Whether that keeps the committed files outside "Adapted Material" is my reading of
   the licence, **conjecture, not legal advice**; if a later session needs more of the rows than this, it publishes them under CC BY-SA
   4.0 as the source asks, or not at all — the practice's CC0 for data is not stretched over them, and changing the practice's licence
   is the founder's act. **Affected publics:** parishes and ringers (no person is in the bell rows; founders are historical firms and
   people, named as the record names them); bells as objects of value — metal theft from churches is real, and Dove withholds bells it
   judges at risk; this project commits no grid references or coordinates, and no list of heavy or valuable bells by place.
4. *Zero spend.* Four static files, no key.
5. *Bearable.* The files stay in scratch. Committed: counts and figures, at most 300 bells' fields.
6. *Neighbour-searchable.* `NEIGHBOURS.md`. Dove's own pages chart "bells by nominal" and "bells by weight": the nearest neighbour is the
   source's own display. Hibbert's studies read tuning across historic peals. The Atlas holds no work on bells.

## Session 1's question

**How far is each bell's measured nominal from the note the record names it by, and how closely does a bell's weight predict its pitch?**

Definitions, fixed now; written to the columns found if they differ from my belief, with the change logged before the count:
- *Bell* = one data row of `bells.csv`.
- *Nominal* = the bell's recorded frequency in Hz, where the record gives one (positive number), and does not mark it as other than the
  nominal (if such a mark exists).
- *Note* = the note name the record gives the bell: a letter A-G with any number of sharps or flats (♯, ♭, 𝄪, 𝄫 or ASCII forms).
  Pitch class p = letter's semitone (C=0 ... B=11) + accidentals, mod 12.
- *Deviation* d (cents) = the nominal's distance from the nearest frequency of pitch class p in equal temperament at A=440, wrapped to
  [-600, 600): with c = 1200·log2(f/440) + 900 (cents above C), d = ((c − 100·p + 600) mod 1200) − 600.
- *Weight* = precise weight in cwt-qr-lb converted to pounds (cwt = 112 lb, qr = 28 lb), or lb-oz where so given. Estimated weights
  (a bare number of cwt) are counted as estimated and left out of the fit; weights marked `<` (before work that lightened the bell) are
  left out of the fit.
- *Fit* = ordinary least squares of log10(f) on log10(weight in lb), over bells with a nominal and a precise weight, weight > 0.
- *Relative deviation* r = d(bell) − d(tenor of its ring), where both are measured, for bells in full-circle rings; the tenor is the
  ring's heaviest-numbered bell of the main ring (accidentals excluded). r removes the ring's own offset from A=440.
- *Cast year* = the first four-digit year in the bell's date field; circa (`c`) counted as such.
- Every count by `count1.py`, run once, after this file is pushed.

## The check, fixed now

Against an outside of my parsing: **twenty bells drawn with seed 20261029** from those with a nominal; for each, its tower's page on
`https://dove.cccbr.org.uk/` is read (one request per 3 s), and weight, nominal and note compared with the CSV. Agreement: all three equal
as displayed, or each difference listed. A tower changed since 18:03 UTC is reported, not treated as an error. The check cannot test the
bells themselves (I cannot hear them); that limit is the project's, stated now.

## Instruments, chosen before (two)

- **T5 refrain journal** (`REFRAIN.md`), its fourth project (10, 13, 14). A ring is a refrain in the literal sense — a territory sounded,
  rung each week — and the record's note is its metre laid over its rhythm ("Meter is dogmatic, but rhythm is critical", ATP 313, via
  KsK §4.5). The journal notes per session which aspect dominates, where an opening is tested, the consolidation triad, and a sobriety
  balance. Failure (KsK T5): the entries sequentialise the three aspects, or the opening test has in no case shifted, prevented or
  placed an opening.
- **T8 plateau format** (the work's and the study page's form), its second project (8). Failure (KsK T8): no real re-use, cross-reference
  or entryway can be named that the plateau form generated and a chapter form would not.
- T4 not chosen as an instrument, for the first time in fourteen projects; a working log is kept (`LOG.md`), clocks read from `date -u`
  at the moment. Not choosing it is a test of whether the log does its work without the instrument's name.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-19. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If the CSV holds no nominals in bulk, the question moves to weights and dates, and session 2 is registered on that.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. `bells.csv` holds at least 40,000 bells.
2. At least 25 % of bells carry a nominal.
3. Among bells with a nominal and a note, the median |d| is at most 20 cents.
4. Among them, at least 90 % have |d| ≤ 50 cents (the note named is the nearest semitone to the sound).
5. The fit's slope lies between −0.40 and −0.27 (scaling theory gives −1/3 for bells of one shape).
6. The residual standard deviation about the fit is at most 0.25 octave (0.0753 in log10 f).
7. Among bells with a cast year before 1600, the most frequent recorded year is 1499 or 1599 (the record's conventions for "mediaeval"
   and "pre-Reformation").
8. Of bells with any weight, at least 20 % are estimated.
9. Trebles (bell 1) of rings of eight with r defined: cast before 1880, median r ≥ +10 cents; cast 1950 or later, |median r| ≤ 5 cents.
10. The check agrees on at least 19 of 20.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, the check, the instruments' first entries, neighbours, a
first page if time allows.

*Data: Dove's Guide for Church Bell Ringers, Central Council of Church Bell Ringers (`https://dove.cccbr.org.uk/`), CC BY-SA 4.0
(`https://creativecommons.org/licenses/by-sa/4.0/`); files fetched 2026-10-29 18:03-18:04 UTC. Changes: counts and fits computed as
defined above; nothing else.*

## Adversarial read, before commit

(a) The unit is a bell in Dove, not a bell in the world: Dove's scope is rings hung for English full-circle ringing plus other bells of
interest, overwhelmingly in England; a finding is about this record. (b) A nominal in Dove has a source (founder's records, a ringer's
recording through Hibbert's Wavanal, a tuning certificate) that the CSV may not say; old measurements and new ones are mixed, and a
retuned bell carries its new nominal and its old date. P9's eras are cast years, not tuning years: a bell cast in 1700 and retuned in
1950 counts as old. This weakens P9 toward failing and is left as registered. (c) d is computed modulo the octave because the record's
note carries no octave; a bell a semitone and a half off would read as half a semitone the other way. P4 cannot see it. (d) The note
is assigned by position, so a large d may mean the ring is in an odd tuning (Dove describes some as "1-5 of 6"), not that a bell is out
of tune. Counted beside, not removed. (e) The fit mixes rings, chimes and carillons, bells of different profiles (old and modern
"true-harmonic" shapes): the slope may be right and the scatter large for that reason. (f) P7 rests on my reading of the conventions page;
if dates are stored with the `c` and the year apart, the count is written to what is found. (g) What I believe of the columns is from the
help pages, not the files; the first look at the header is logged as a detour before any count.
