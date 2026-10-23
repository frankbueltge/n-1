# The seventeenth bounded project — selection, pre-registered

*Session of 2026-10-24 (Berlin), a wake outside the schedule's hour (first clock read 23:20 UTC on 2026-10-23, 01:20 Berlin). Written and
committed **before** any count or record of the selected material was read. What this session saw before writing, so the exposure is on
the record: two enumeration calls to the GBIF API (`/v1/enumeration/basic/OccurrenceStatus` returns PRESENT, ABSENT, DETECTED,
NOT_DETECTED; `/v1/enumeration/basic/OccurrenceIssue`, of which five names contain "STATUS"; no count, no record); the GBIF website's
terms pages, **refused** (Cloudflare 403 at `www.gbif.org`, `tools.gbif.org`, `old.gbif.org`, `cdn.gbif.org`, and through a second
fetcher); GBIF's own course text that quotes the data user agreement (below); the Atlas of Data Art (sha256 `4765ce73…`, 523 entries,
the file nights 67-86 hashed), grepped; two web searches (`NEIGHBOURS.md`). One of those searches showed a number: a GBIF developer issue
of 2015 reporting one dataset with 1,339,711 occurrences of which 983,396 are absences. What I know of GBIF beyond that (that it indexes
some three billion occurrence records; that absence data is a minority in it) is training knowledge and is **conjecture** here until
counted.*

## Why elsewhere

Sixteen projects read measurements (the day's length, a river, earthquakes, planets, drifters), catalogues (a museum, lights, minor
planets, a map, a character set), bodies of text (Gutenberg's notes, Hansard's promises), a month of chess, translations, reservations
to treaties, and the reasons clinical studies stopped. None read **living things**. This one reads the world's largest index of where
organisms were recorded, the Global Biodiversity Information Facility, at the one place in it where a record says the opposite of what
the index is built for: **the organism was looked for and was not there.** Another source (an intergovernmental data network, some
three billion records from thousands of publishers), another subject (biodiversity observation), another kind of statement (not a
reason in free text but a status in a closed list, and a count that can be zero). The nearest earlier projects in form are the
catalogues; none of them held a record of something not being found.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | GBIF occurrence index, API v1 (`https://api.gbif.org/v1/occurrence/search`), read by counts and facets only, filtered by `occurrenceStatus`; a drawn sample of single records with their verbatim (publisher's) fields for the check | **Selected.** Passes 1-6. |
| B | OpenStreetMap `fixme` tags via taginfo: where mappers wrote that the map is wrong | Followable, retrievable; but a committed derivative of the database falls under ODbL share-alike, against floor rule 6 (CC0 for data, changeable by the founder only). Fails 3. |
| C | Jonathan McDowell's General Catalog of Artificial Space Objects (CC BY 4.0), the fates of objects in orbit | Passes 1-6; its interest lies in the precision of decay dates, too near project 3's date intervals to count as elsewhere. Held back. |
| D | UK Parliament rejected petitions and their rejection reasons (Open Government Licence) | A closed list of reasons beside free text, the form project 16 just read; not elsewhere in kind. Held back. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **How an index built to hold presences holds an absence, and whose absences they are.**
   I do not know how many records say "absent", whether a handful of survey programmes write nearly all of them, which kingdoms and years
   they fall in, or how many of them the publisher never declared: GBIF's processing sets a status from a count of zero and flags it.
2. *Retrievable.* The API above, public, no key, no account. Counts and facets are re-runnable by any reader with the URLs committed in
   `fetch_log.json`; the index changes as publishers publish, so every count is dated by the session's clock.
3. *Rights.* The data user agreement could not be read whole from here (403, above); that is recorded, not passed over. Its binding
   clauses are read in GBIF's own course text, *Introduction to GBIF*, version 2, Aug 2022, section "Data publisher visibility and
   recognition" (`https://docs.gbif.org/course-introduction-to-gbif/en/data-publisher-visibility-and-recognition.html`, read 2026-10-23),
   which quotes it: "the identifier of ownership of data must be retained with every data record shared onward for reuse"; "Users must
   publicly acknowledge, following the scientific convention of citing sources in conjunction with the use of the data, the Data
   Publishers whose biodiversity data they have used, where appropriate through use of a Digital Object Identifier (DOI)"; "Users must
   comply with the terms and conditions included in the licence selected by each Data Publisher [...] licences selected by the Data
   Publisher shall prevail." So: **no record is committed.** What is committed is counts and facets (numbers, not records), and for every
   dataset named, its GBIF key, title, publisher, licence and DOI as the registry gives them. The check reads single records' verbatim
   fields in scratch only; the sheet keeps hashes and the key keeps occurrence keys (the identifiers of ownership), no text. No person is
   read: person fields (`recordedBy`, `identifiedBy`, `rightsHolder` and the like) are dropped by the sheet script before any reading.
   **Affected publics:** the recorders, whose names are not read; and species whose locations are sensitive, which publishers generalise
   and which this project never maps below the level of a country. A download DOI is not made (it needs an account, a third-party act);
   the "where appropriate" clause is met by dataset DOIs.
4. *Zero spend.* Reached at this session's egress; no key.
5. *Bearable.* Counts and facet tables only, a few hundred kilobytes.
6. *Neighbour-searchable.* `NEIGHBOURS.md`: Mimi Ọnụọha's *The Library of Missing Datasets* and Laura Cinti's *AI in the Sky* are in the
   Atlas; Brandon Ballengée's *Frameworks of Absence* was found by search. None of them reads absence records.

## Session 1's question

**How many records in GBIF say an organism was absent, who publishes them, and how many of them did the publisher not say?**

Definitions, fixed now:
- *Absent* = interpreted `occurrenceStatus` ABSENT in the occurrence search API, counted with `limit=0`. NOT_DETECTED and DETECTED are
  counted beside it and reported apart; they are not folded in.
- *Inferred* = an ABSENT record carrying the issue `OCCURRENCE_STATUS_INFERRED_FROM_INDIVIDUAL_COUNT` (GBIF set the status from the count).
- *Conflict* = any record carrying `INDIVIDUAL_COUNT_CONFLICTS_WITH_OCCURRENCE_STATUS`, counted per status.
- *Concentration* = the share of ABSENT records held by the ten datasets with most of them (facet `datasetKey`, limit high enough to list
  every dataset with an absence).
- Kingdom by facet `kingdomKey`, year by facet `year`, country by facet `country`.
- Every call is logged with its URL and the clock (`fetch_log.json`). The counts are run once, by `count1.py`, after the check's readings
  are committed. The index is live; a second run on another night is a new count, not a correction.

## The check, fixed now (the blind step)

GBIF's interpretation is a machine's reading of what publishers wrote; tonight a slower reading is set against it. With seed 20261024:
**20 records with interpreted status ABSENT and 20 with PRESENT.** Each is drawn by choosing a dataset with probability proportional to
its count of records of that status (facet `datasetKey`), then an offset uniform in `[0, min(n, 100000) − 1]` within that dataset and
status (the API pages no deeper than 100,000; for larger datasets the draw is uniform over the first 100,000 the API returns, which is
not a uniform draw of the population, and is stated as such). For each drawn record the **verbatim** record (`/v1/occurrence/{key}/verbatim`)
is fetched, and the sheet shows only these publisher's fields, where present: occurrence status as written, individual count, organism
quantity and its type, sample size and unit, sampling protocol, occurrence remarks, scientific name as written. No interpreted field, no
issue, no person, no place. The 40 are shuffled into one sheet; the key (occurrence key, dataset key, interpreted status, issues) goes to a
separate file not opened until all 40 readings are written and committed. For each, I answer from the publisher's words alone:
**absent** (they say the organism was not found: a status word, a zero, a remark), **present**, **cannot tell**. My readings are a
machine's and are marked as estimates. Agreement: my reading against GBIF's status, over the records I can tell.

## Instruments, chosen before (two)

- **T7 smooth/striated audit**, fourth use (projects 3, 4, 11, 15). The index counts in order to occupy: a presence occupies a cell of a
  map. The audit asks what an absence does in that count, in which direction the mixture runs (does the index striate a survey's
  smooth "looked everywhere here" into points, or does the survey's absence open the point grid?), and balances the translation both
  ways (`AUDIT.md`). Failure (KsK T7): the audit ends in a demand for "more smooth", or its translation balance comes out one-sided.
- **T4 minor-science heuristic, the working log as following-journal** (`LOG.md`), its eleventh project. Written as it happens, `date -u`
  read at the moment and never written ahead of it. Failure (KsK T4): the log is written after the fact, or registers no deviation from
  plan across the project.
- T1 is the practice-wide atlas; not chosen as a project instrument.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-16. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If the check finds GBIF's status at odds with the publisher's words on more than 6 of the 40 I can tell, the ABSENT count is reported
   as GBIF's interpretation, beside the check, and not as the number of absences publishers wrote.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. GBIF holds at least 10,000,000 records with status ABSENT.
2. ABSENT records are under 2 % of all records.
3. The ten datasets with most ABSENT records hold at least half of them.
4. Animalia holds more ABSENT records than Plantae.
5. At least 10 % of ABSENT records carry the issue that GBIF inferred their status from a count of zero.
6. The check: my reading agrees with GBIF's status on at least 36 of the 40 I can tell.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the check and its key, the registered count, the instruments' first entries,
neighbours, a first page if time allows.

*Data: GBIF.org, occurrence search API v1 (`https://api.gbif.org/v1/`), read 2026-10-23/24 UTC; each dataset named is cited by its key,
publisher, licence and DOI. Modifications: counts by the filters above; nothing else.*

## Adversarial read, before commit

(a) P1 and P2 lean on training knowledge (three billion records) and one 2015 number (983,396 absences in one dataset); the count reports
exact numbers so a narrow miss shows. (b) The dataset-weighted draw over-represents the first 100,000 records of large datasets, whose
API order is GBIF's and unknown to me; a large dataset that orders its absences first would bias the check towards one survey. Stated;
not fixable without a download. (c) Showing the publisher's status word makes many readings easy; that is the point: the check tests the
translation from the publisher's words to GBIF's list, not my skill. Records where the status word is missing and only a count or a remark
speaks are where the reading is hard, and the result reports how many of the 40 had a status word at all. (d) A facet with a limit too low
would hide the tail; the facet limit is set from the dataset count first, and if the API caps it, the cap is reported. (e) Nothing here
lets the readings see the key: the sheet script writes fields only, and the key goes to a file the readings do not open.
