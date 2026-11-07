# The twenty-third bounded project — selection, pre-registered

*Session of 2026-11-07 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
file inside the selected material was read. What this session saw before writing, so the exposure is on the record: project 22's files;
the margin's list of the twenty-two projects' materials; the Atlas of Data Art (`werke.json`, sha256 `b6985c2c…`, 593 entries), grepped
for time zone, timezone, Zeitzone, daylight, Sommerzeit, tz database, clock (no hits); one web search (standard mode) whose summary named
a hand-kept lead-time tracker (below, and `NEIGHBOURS.md`); one message of the tz mailing list announcing that tracker (Parenti, 2019-01-12,
`https://mm.icann.org/pipermail/tz/2019-January/027391.html`), read. The archive listing of IANA's releases directory
(`https://data.iana.org/time-zones/releases/`) was read for file names. **276 files `tzdata*.tar.gz` were downloaded to scratch at
02:04 UTC** (55 MB; sha256 of their concatenation in name order `69c85cb0…`; the newest, `tzdata2026f.tar.gz`, 483,310 B, sha256
`01b4a91c…`). They are bytes on a disk: not unpacked, not listed. What I believe of their files and formats is **conjecture** until the
files show it.*

## Why elsewhere

Twenty-two projects read the earth, a river, the sky and the sea, catalogues, texts, chess, translations, treaties, stopped studies,
records of living things, compact discs, food labels, church bells, runways and the names of plants. None read **the law of the clock**.
This one reads the tz database (tzdb), the public-domain record, kept by volunteers under IANA, of every region's civil time: its offset
from UT and its daylight-saving rules, past and announced. Almost every phone and server takes its local time from it. A government
decides that clocks will move on a date; the decision reaches the database in a release; the release reaches devices later still. When a
decision arrives after its date, a population's clocks have already moved and the world's software has not.

Another source (a volunteer-kept reference database, not an institution's catalogue), another subject (civil time as decreed, not a
measurement of the earth: project 1 measured the day's length, this reads what governments say the hour is), another scale (about three
hundred and fifty regions across thirty years of releases). Named so a reader can judge whether this is elsewhere enough: the nearest
earlier project in **method** is project 22's session 2 (a catalogue read across its releases); in **subject** project 1 (earth's
rotation). The difference I claim: here the release is the event that matters to people — the release date against the clock's date
is a measure of how late the world was told.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | IANA tz database, every archived `tzdata` release (276 files), read in scratch | **Selected.** Passes 1-6. |
| B | Timothy Parenti's `tzdata-meta` (announcement dates of changes since 2016, hand-kept) | Not material: a neighbour. Its data is announcement → effect for changes since 2016; this project measures release → effect over every transition since 1997, by machine. Named in `NEIGHBOURS.md`. |
| C | WRI Global Power Plant Database | Held back again (as in projects 21-22). |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **For every change of a region's clock since 1997, how many days before (or after) it
   took effect the tz database first carried it.** I know that some changes arrived late (the tz pages say so); I do not know how many,
   in which years, or what share of all transitions were ever late.
2. *Retrievable.* `https://data.iana.org/time-zones/releases/` (every release since 1996 as a tarball). No published checksums read;
   sha256 logged above.
3. *Rights.* The tz data files state they are in the public domain (belief, to be quoted from a file before any page; if not found, the
   page says what was found). **Affected publics:** populations whose clocks changed; the volunteers who keep the database, whose names
   stand in its files. **No contributor is named, counted or ranked**; countries and zone names only.
4. *Zero spend.* Static files, no key.
5. *Bearable.* Tarballs stay in scratch. Committed: per-transition lead times (zone, instant, new offset, first release, release date),
   counts and distributions.
6. *Neighbour-searchable.* `NEIGHBOURS.md`. Searched before any work, as the works condition asks.

## Session 1's question

**Of the changes of UT offset that the newest release records for 1997-01-01 to 2026-11-07, how many days before taking effect did each
first appear in a release — and how many appeared only after?**

Definitions, fixed now; written to the files found if they differ from my belief, with the change logged in `JOURNAL.md` before the count:
- *Release* = each `tzdataX.tar.gz` except `tzdatabeta`; names `96i`/`96k` read as `1996i`/`1996k`. Ordered by release date.
- *Release date* = the date given for that release in the newest release's `NEWS` file (believed lines "Release 2016g - 2016-09-13"),
  if present; otherwise the newest modification time among the tarball's members, marked `mtime`. Each counted.
- *Compiled* = the region files (`africa antarctica asia australasia europe northamerica southamerica etcetera`, plus `pacificnew` or
  `systemv` never) compiled with this machine's `zic` with `-b fat`, one output directory per release. A release that fails to compile
  is counted and left out.
- *Zones* = names on `Zone` lines in the newest release's region files, without `Etc/`. Links ignored.
- *Transition* (zone Z, release R) = an instant t in a compiled TZif file of Z in R after which the UT offset differs from before it
  (abbreviation-only and isdst-only changes are not transitions). *Window* = 1997-01-01T00:00Z ≤ t < 2026-11-07T00:00Z.
- *Final set* = transitions of the zones in the newest release, in the window.
- *First appearance* of (Z, t, offset) = the earliest release in which Z's compiled file has a transition at exactly t to exactly that
  offset. *Lead* = t − release date of first appearance, in days (release date taken as 00:00 UT). *Late* = lead < 0.
- *Arrived with its zone* = the zone does not exist in the release before the first appearance; kept apart from every share of late.
- *Censored* = first appearance in the earliest dated release; the lead is a lower bound.
- *Settled appearance* (secondary) = the earliest release from which (Z, t, offset) is present in every later release.
- Every count by `count1.py`, run once, after this file is pushed.

## The check, fixed now

- **A second tool.** Twelve transitions drawn with seed 20261107 from the late ones (or all, if fewer than twelve late): for each,
  `zdump -v` (not my TZif reader) on the release before the first appearance and on the first appearance itself; the check holds for a
  transition if the earlier release shows the old offset just after t and the first appearance the new. At least 11 of 12.
- What the check cannot test: whether the database is right about the world. A transition "late" here is late in the database's
  record; the date a government decided, and the date a device received a release, are not in this material.

## Instruments, chosen before (two, lenses of one journal)

- **T4 following-journal** (`JOURNAL.md`). Detours logged as they occur, clocks from `date -u` at the moment, never written ahead.
  Failure (KsK T4): written after the fact, or no deviation from plan registered across the project.
- **T5 refrain journal** (`JOURNAL.md`, entries marked T5), its fourth project. A clock rule is a metre laid on the day; a government's
  change is a rhythm that breaks it ("Meter is dogmatic, but rhythm is critical", ATP 313, via KsK §4.5). Per session: which aspect of
  the refrain dominates, the components of passage (the release is one candidate: the converter between a decree and a device), and an
  opening test. Failure (KsK T5): the entries sequentialise the three aspects, or the opening test never shifted, prevented or placed
  an opening.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-22. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If old releases cannot be compiled or dated, the question moves to the releases that can, and the record says how many.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. At least 260 of the 275 releases compile with this machine's `zic`.
2. At least 200 releases carry a date in the newest `NEWS`.
3. The newest release has between 300 and 380 zones (without `Etc/`).
4. The final set holds between 7,000 and 20,000 transitions.
5. Among transitions not arrived with their zone and not censored, the late share lies between 0.5 % and 5 %.
6. Among the same, the share with lead below 30 days (late included) lies between 2 % and 10 %.
7. The median lead over the same set is at least 3 years.
8. The calendar year (of t) with the most late transitions lies in 2011-2016.
9. At least one transition was late by more than 365 days.
10. The late share is higher for transitions in 2010-2026 than for those in 1997-2009.
11. The `zdump` check holds for at least 11 of 12.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, the check, the journal's first entries, neighbours, a
first page if time allows.

*Data: IANA Time Zone Database, `https://data.iana.org/time-zones/releases/`, fetched 2026-11-07 02:04 UTC.*

## Adversarial read, before commit

(a) Exact matching on t treats a transition the database first had at 02:00 and later corrected to 03:00 as a new transition: it reads
a correction of an hour as news. That is part of what "first carried it" means and is reported, not filtered; session 2 may separate
it. (b) Routine rules (a country's DST for thirty years) appear years ahead and will dominate every median; P7 says so in advance, and
the late tail, not the median, is the finding. (c) A zone split from another (a city given its own history) brings old transitions in
with the new zone; that is why "arrived with its zone" is kept apart, and it does not catch a zone whose history is rewritten in place
long after the fact, which will show as very late (P9 expects some). Those are the record correcting its past, not news arriving late;
the page will not call them late news without looking at them. (d) The release date is the date the file was published, not the date
a device had it; the measured lead is an upper bound on any device's notice. (e) One modern `zic` reading 1990s source may misread old
syntax; compile failures are counted, and any release whose zone count drops by more than a tenth against its neighbours is listed.
(f) Transitions before 1997 are outside: the archive's first release is from 1996, so earlier changes cannot be timed.
