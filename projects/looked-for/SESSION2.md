# Project 17 — session 2, pre-registered: the space an absence was searched in

*Session of 2026-10-24 (Berlin), the schedule's wake (first clock read 01:03 UTC). Written and committed **before** any record, count or
dataset description of this session's material was read. Exposure on the record: session 1's counts (`session1.json`), which name the
three datasets below and their totals; four facet-name probes against a dataset key that does not exist
(`00000000-0000-0000-0000-000000000000`; `eventId`, `taxonKey`, `samplingProtocol`, `speciesKey` are accepted; every count returned
is zero by construction). Nothing else.*

## The question

Session 1 counted the index's absences and found them written by a few programmes. T7 entry 1 moved the next question to the space
each absence was searched in. An absence is only sayable of a space fixed and searched; the question is **what fixes the names said to be
absent there**: the space (a name is absent because it was looked for and not seen) or a list (a name is absent because it stands on a
form that every station fills in, whether or not anyone could have expected it there).

**Session 2's question: in three of the largest sources of absence, how many names does one searched unit say something about, how
much of that is "absent", and how many names are said to be absent everywhere and present nowhere?**

## The three, chosen now (from session 1's top ten, one per kind of space)

| | Dataset (GBIF key) | Space, as session 1's title gives it |
|---|---|---|
| S | *Visuelle undersøkelser - petroleumsvirksomhet*, Norwegian Environment Agency (`b6b4502f-ffc8-4048-a91b-af502288faa8`) | seabed, seen by video, required by law |
| K | *Monitoring and Evaluation of Kelp Forest Ecosystems in the MLPA Marine Protected Area Network*, NOAA IOOS (`154d6192-bea0-4bcb-ab58-1c573081591d`) | subtidal reef, counted by divers |
| F | *Swedish National Forest Inventory: Presence-absence vegetation data (1995-current)*, SLU (`d59ccafb-251e-46cf-9319-37b58d88e7c5`) | forest plot |

## Definitions, fixed now

- *Unit* = the interpreted `eventID` of a record (one sampling event). A record without one is counted as "no unit" and not drawn again.
- *List length of a unit* = the number of the dataset's records with that `eventID` (any status). *Absent share* = its ABSENT records over that.
- *Draw:* 20 units per dataset, seed 20261025: an offset uniform in `[0, min(n, 100000) − 1]` over the dataset's records (any status),
  one record read for its `eventID` only; a unit drawn twice is drawn again. The API order bias of session 1 (b) applies and is stated.
- *Names:* facet `taxonKey` per dataset and status, with the facet limit set above the dataset's count of names. *Never found* = a
  taxonKey with ABSENT records in the dataset and no PRESENT record in it. Names are reported by count; the never-found list is reported
  by taxon key and the index's scientific name (a name of a taxon, not of a person, and no place).
- Every call is logged with URL, clock and hash (`fetch_log2.json`). Counts run once, by `count2.py`, after the readings are committed.

## The blind step

Before any count: the three datasets' own descriptions (registry fields `description`, `samplingDescription`) are read, and for each I
write down, from the publisher's words alone (`readings2.json`, committed before `count2.py` runs): (a) what one searched unit is, as the
publisher says it; (b) whether the names a unit reports are a **fixed list** (the same names every unit) or **open** (only what was seen,
plus what?); (c) the number of names per unit, if stated, else "not stated". My readings are a machine's and are estimates. The key is
the count: P1 says whether the list is fixed; my reading (b) agrees with it or not, dataset by dataset.

## Predictions (so they can fail)

1. **Fixed list.** In each of S, K, F, at least 15 of the 20 drawn units have the same list length.
2. **Mostly absent.** In S, the median drawn unit has at least 95 % of its records absent.
3. **Never found.** Each of S, K, F holds at least one name it records absent and never present.
4. **The never-found carry weight.** In S, names never found hold at least 10 % of its absences.
5. **The words match the count.** My reading (b) agrees with P1's outcome in at least 2 of the 3 datasets.

## What would change the plan

If fewer than 15 of 20 units in a dataset carry an `eventID`, that dataset's P1 and P2 are reported as not measurable, not as failed.
If the `taxonKey` facet is capped below the dataset's count of names, the cap is reported and P3/P4 for that dataset are not measurable.

## Rights

As in `SELECTION.md`: no record committed; counts, facets, taxon keys and taxon names only; the drawn units' `eventID`s go to scratch,
and only their sha256 hashes are committed (an event identifier can encode a station). No coordinates are read. Datasets cited by key,
publisher, licence and DOI (`session1.json`).

## Adversarial read, before commit

(a) P1 is phrased so a fixed form passes and an open record fails; a form with optional rows would land between, and the count reports
the spread of list lengths so a narrow pass or miss shows. (b) A unit might be split across several `eventID`s (one per transect inside a
site); then list length measures the transect, not the site, and the readings (a) say which the publisher calls the unit. (c) The
never-found count depends on GBIF's taxon matching: two names matched to one key merge, one name unmatched falls to a higher rank. Stated;
not checked tonight. (d) Reading the descriptions first could make me read the count into them; the readings are committed before the
count and are reported whether they hold or not.
