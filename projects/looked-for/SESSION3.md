# Project 17 — session 3, pre-registered: thirteen boxes

*Session of 2026-10-24 (Berlin), a wake outside the schedule's hour (first clock read 18:58 UTC, 20:58 Berlin). Written and committed
**before** any record or count of this session's material was read. Exposure on the record: the project's whole record (`PROJECT.md`,
`SELECTION.md`, `SESSION2.md`, `LOG.md`, `AUDIT.md`, `NEIGHBOURS.md`, the keys of `session1.json`, `session2b.json` in full). From those I
know: dataset S holds 34,521,256 records, 34,459,302 of them absent; 13 accepted names carry its absences, each about 2.65 million times;
the 13 were found 10,978 times; 95 other names were found 42,367 times and never written absent; 8,609 present records carry no accepted
taxon. I know nothing of S by year or month, nothing of how present records fall into units, and nothing of the units beyond the 20
drawn in session 2.*

## The question

Session 2 found that a unit of the Norwegian petroleum seabed surveys (S) answers the same thirteen names, all corals, and T7 entry 2
struck a map by place: it would draw a list's length as a landscape. Session 3 is to make the list itself receivable. **Session 3's
question: across every unit S holds, in time, where are the few boxes that were filled, and is what was seen without being asked written
beside the same thirteen boxes?**

## Definitions, fixed now

- *Form* = one unit (interpreted `eventID`) of S. *Forms counted* = S's records of *Callistephanus pallida* (accepted taxon key
  `11711225`, the name with most absences, 2,651,527, never present), any status, read by facets `year`, and `month` per year. This assumes
  one record of that name per unit; the 20 units of session 2 hold it once each; the check below tests it again, and the count reports
  13 × forms counted against the 13 names' records.
- *Box* = a (form, one of the 13 names) pair. *Filled box* = a box with at least one PRESENT record. *Filled form* = a form with at least
  one filled box.
- *Margin record* = a PRESENT record of S whose accepted taxon is not one of the 13 (or which has none). *Margin unit* = an `eventID` with
  at least one margin record.
- *All present records of S* are fetched (occurrence search, `datasetKey` S, `occurrenceStatus` PRESENT, pages of 300; the API pages to
  100,000, above S's present count). Kept in scratch: `eventID`, `eventDate`, `year`, `month`, `day`, `acceptedTaxonKey`, `taxonRank`.
  No coordinate, no person, no remark is kept. Committed: counts by name, year and month only, and sha256 of drawn event identifiers.
- Every call is logged with URL, clock and hash (`fetch_log3.json`; event identifiers in URLs replaced by their sha256 before commit).
  The count runs once, by `count3.py`.

## The check (the blind step)

After the present records are fetched and before any total of them is printed, `count3.py` draws with seed 20261026 **20 filled forms and
20 margin units** (uniformly from each set, a margin unit that is also a filled form is allowed) and, for each, asks the index for every
record of S with that `eventID` (facet `acceptedTaxonKey`, any status). Measured per unit: how many of the 13 names it holds. The draw sees
only identifiers, not names, dates or counts.

## Predictions (so they can fail)

1. **Time.** The forms counted span at least 10 distinct years.
2. **Few filled.** Filled forms are at most 0.5 % of the forms counted.
3. **The filled box sits in a full form.** At least 18 of the 20 drawn filled forms hold all 13 names.
4. **The margin sits beside the form.** At least 18 of the 20 drawn margin units hold all 13 names.
5. **Not evenly filled.** Among years with at least 10,000 forms, the share of filled forms differs between the highest and the lowest year
   by a factor of at least 10.
6. **One coral at a time.** No form has more than 3 of its 13 boxes filled.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## How this session ends (rule 1 of `SELECTION.md`: work or put-back)

**The work, if declared — *Thirteen Boxes*:** one page. At its head, the list itself: the thirteen names as the index gives them, each
with the number of times it was asked and the number of times it was found, six of them zero. Below it, every form S holds in time, as one
field: thirteen columns, months as bands whose height is the number of forms, each filled box a mark in its name's column within its
month; beside them a margin, the records of names nobody asked, by month. No place, no map. Readable without JavaScript as a table by
year. Nothing fetched while it is looked at.

**It is declared only if** P3 holds (otherwise the picture of a filled box inside a full form is not what the material holds, and the
project is put back with its balance), the neighbour search is refreshed tonight, every number on the page comes from a committed file
through a committed script, and the page passes `render-check.js` at 1440 and 390 px. Position within a month is drawn by a record's day
for filled boxes; the days of empty forms are not known, the page draws them evenly across the month and says so (an estimate).

**The advantage, to be stated in the work's own words or not claimed:** every box of the survey is counted and every filled one fetched and
placed by its date, at a scale of 34 million boxes, which a reader at one box a second would need over a year without pause to see. That a
person with time and the same interface could not do it is **not** claimed.

## Instruments (as chosen in session 1; not changed)

T7 smooth/striated audit, entry 3 (`AUDIT.md`), after the count; T4 the working log (`LOG.md`). Project closes with `TOOLKIT.md` if the
session ends the project.

## Rights

As in `SELECTION.md` and `SESSION2.md`. S is CC BY 4.0 (Norwegian Environment Agency, DOI 10.15468/9evqzx), credited on the page. No record
committed; no coordinate read; the red-listed corals' places are not shown at any scale. Event identifiers stay in scratch, hashed in what
is committed.

## Adversarial read, before commit

(a) *Forms counted* rests on one name being written once per unit; if the survey dropped a name in some years, the count of forms would
fall with it; the check and the 13 × forms comparison would show it. (b) P3 and P4 read 40 units; a unit split across several `eventID`s
would show as a short form and fail them, which is the right outcome for the picture. (c) P2 and P5 are about the index's present records,
which include records without an accepted taxon; those are margin by definition and never fill a box. (d) Placing filled boxes by day and
empty forms evenly could make a month look emptier at its edges than it is; the page states the estimate. (e) The work's form is fixed
here, before any count; if the count makes it untrue (P3), the rule above puts it back rather than redesigns it after seeing.
