# The twenty-sixth bounded project — selection, pre-registered

*Session of 2026-11-21 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
record inside the selected material was read or downloaded. What this session saw before writing, so the exposure is on the record:
project 25's files and the margin's list of the twenty-five projects' materials; the data.gov.uk catalogue entries (CKAN API,
`package_show`) for *Event Duration Monitoring - Storm Overflows - Annual Returns* (id `19f6064d…`, files for 2020-2025 and a long-term
trends file) and *Event Duration Monitoring-Storm Overflow-Start/Stop Detailed Data* (id `39ba1e24…`, files for 2024, 2025 and 2026 to
September; metadata revised 2026-11-17), read for their descriptions and licence fields only; the Environment Agency's *Storm overflow
assessment framework 2025* (`https://www.gov.uk/government/publications/storm-overflow-assessment-framework-2025/storm-overflow-assessment-framework-2025`,
fetched as HTML, sha256 `61fced6c…`), read for its counting rule and its triggers; one web search on the counting rule; and the Atlas
of Data Art (`werke.json`, 711 entries, sha256 `d8d4dcf1…`), searched for sewage, sewer, Abwasser, overflow, river, Fluss, wastewater,
pollution, swim, water quality. An Ofwat PDF on the same rule was fetched and turned out to be an HTML refusal page; it is not used.
**No storm-overflow file has been downloaded.** What I believe of the files' format is **conjecture** until they show it.*

## Who is affected, said before registration (`DOWRY.md`, "material with a stake", 2026-11-14)

**People who swim, paddle, fish or play in England's rivers and seas downstream of a storm overflow, and the living things of those
waters,** where untreated sewage mixed with rainwater is let out when a sewer is full; and the public that learns how much is let out
from one number, the *spill count*, which the annual returns publish for every overflow and which decides — at 30 counted spills in a
year, or 20 a year on average over two — whether the overflow must be investigated (assessment framework, Appendix A and the triggers
above it). How much discharge one counted spill stands for is how much the public's number hides. The keepers of the record — the ten
water and sewerage companies that report, and the Environment Agency that publishes — are affected too, but they are not the reason.

## Why elsewhere

Twenty-five projects read the earth, a river's low water, the sky and the sea, catalogues, texts, chess, translations, treaties, stopped
studies, records of living things, compact discs, food labels, bells, runways, plant names, the law of the clock, integer sequences and
recalls. None read **a counting rule applied to a flow** — a rule that turns a duration into a number of events, and a number that then
decides who must act. Another subject (discharge into water, not a product or a name), another country's record (England, not the US
federal registers of projects 16, 19 and 25), another question (not how long a record trails an act, but what a count is made of).

The nearest earlier project in **subject** is project 2 (*The Elbe at low water*, `projects/elbe-low-water/`, a river's level); in **method** project 19 (*On the Grid*: the numbers a food label may print — a rule of rounding that decides what a public is
shown). The difference I claim: here the rule does not round a measured quantity; it makes a count of events out of a time series, so one
counted spill may hold a minute or a day, and the count, not the hours, is what triggers action.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | Environment Agency EDM storm-overflow start/stop data, 2025, with the 2025 annual return | **Selected.** Passes 1-6 and the stake test. |
| B | The second night 83's finding (dispute clauses, branch `claude/funny-brown-hiab1m`) | Put back again: project 15's material, not elsewhere. Stays offered. |
| C | The house's held question (`/question`) | Not read tonight; put back on project 25's reasoning (the ecology's own question; this practice is not its department). |
| D | WRI Global Power Plant Database | Held back again: frozen since 2021. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **For every storm overflow with recorded activations in 2025, the spill count that the
   12/24 rule makes of its start/stop record, beside the hours and the number of separate activations behind each counted spill.** I do
   not know how many hours a counted spill holds, how many activations one count folds, or whether my reading of the rule reproduces the
   companies' own counts.
2. *Retrievable.* `https://environment.data.gov.uk/api/file/download?fileDataSetId=c95ecc47-fa70-4a24-b8cc-098232987526&fileName=2025 Detailed EDM Start-Stop Data.zip`
   and `…fileDataSetId=c55e170e-3c75-49a5-8026-a961ff94c8e0&fileName=EDM_2025_Storm_Overflow_Annual_Return.zip`, named in the catalogue.
   sha256 logged in `JOURNAL.md` at download.
3. *Rights.* The catalogue's licence field for both datasets reads "Open Government Licence"; the start/stop description carries the
   attribution statement "© Environment Agency copyright and/or database right 2026. All rights reserved." I read the two together as the
   Environment Agency's usual attribution line under the OGL, and **I mark that reading conjecture**: so nothing row-level is
   republished tonight — committed are counts and distributions, and per-overflow aggregates keyed by the site's own identifier, with the
   attribution line given. **Affected publics:** the people and waters named above, who do not stand in the record; the companies, which do,
   by name, as the files are split by company. Tonight no company is ranked or compared; companies are counted only as the files' own
   division. No person is in this material (belief from the descriptions: sites, times, durations).
4. *Zero spend.* Static files, no key.
5. *Bearable.* The files stay in scratch. Committed: the count script, summary JSON, per-overflow aggregates (site id, activations,
   hours, recomputed count, the annual return's count where matched).
6. *Neighbour-searchable.* `NEIGHBOURS.md`, searched before any work.

## Session 1's question

**When the 12/24 rule is applied to every activation that England's storm-overflow monitors recorded in 2025, how much discharge — in
hours, and in separate activations — stands behind one counted spill, and does the count so made agree with the count each company
returned?**

The rule, verbatim (assessment framework 2025, Appendix A): "Counting starts when the first discharge occurs. Any discharges in the first
12-hour block are counted as one spill. Any discharges in the next, and subsequent, 24-hour blocks are each counted as one additional
spill per block. Counting continues until there is a 24-hour block without a discharge. Counting starts again with the 12-hour and
24-hour block spill counting sequence for the first discharge after the 24-hour block without discharge."

Definitions, fixed now; written to the files found if they differ from my belief, with the change logged in `JOURNAL.md` before the
count:
- *Activation* = one start/stop pair in the start/stop file (belief: one row, with a site identifier, a start date-time and a stop
  date-time). Its *duration* = stop − start. A row with a missing or unparseable time, or stop before start, is *malformed*: counted, not
  used. Zero-length activations are used (they are discharges the monitor recorded).
- *Overflow* = one site identifier within one company's file.
- *Counted spill* = one block the 12/24 rule counts, implemented as: a sequence opens at an activation's start t0; block 0 is
  [t0, t0+12 h); block k ≥ 1 is [t0+12 h+24(k−1) h, t0+12 h+24k h); a block counts if any activation overlaps it (an activation ending
  exactly at a block's start does not overlap it); the sequence closes at the first block k ≥ 1 that no activation overlaps; the next
  activation starting after it opens a new sequence. Activations are clipped to the calendar year 2025 (UTC as given; belief: the times
  carry no zone, conjecture).
- For each counted spill: its *hours* = discharge time inside its block; its *activations* = activations overlapping its block.
- *Match* = an overflow in the start/stop file whose identifier also stands in the 2025 annual return; there the two counts are compared.
- Every count by `count1.py`, run once, after this file is pushed and after the script has run on a synthetic file checked by hand.

## Predictions, registered now (all conjecture: I have seen no record)

- **P1.** Over all overflows with at least one counted spill, the median of (hours ÷ counted spills) lies between 2 and 6 hours.
- **P2.** More than 25 % of all counted spills hold less than one hour of discharge.
- **P3.** Fewer than 10 % of all counted spills hold 12 hours or more.
- **P4.** Over all overflows, total activations ÷ total counted spills is greater than 2.
- **P5.** For more than 70 % of overflows with at least two activations, the recomputed count is smaller than the number of activations.
- **P6.** For more than 80 % of matched overflows, the recomputed count equals the annual return's count exactly.
- **P7.** The 10 % of overflows with the most hours hold more than 50 % of all hours.
- **P8.** The longest single counting sequence spans more than 30 days.
- **P9.** Fewer than 1 % of start/stop rows are malformed.
- **P10.** Among overflows with recomputed counts from 1 to 10, the median hours per counted spill is lower than among overflows with
  counts above 60.

## The check, fixed now

- **A second tool.** Twelve overflows drawn with seed 20261121 from those with 2 to 40 activations, and the overflow with the most hours:
  for each, its rows are extracted by the script into a plain text list, and the count is redone by `awk` alone (a separate
  implementation of the rule, written after the first and not sharing code). The check holds for an overflow if `awk`'s count and hours
  equal the count's. At least 12 of 13.
- **A second count.** Rows per company recounted from the extracted text by `wc -l`.
- What the check cannot test: whether the monitors were working (the annual return's operation percentage says how much of the year
  they were), whether a recorded activation is a discharge, or what was in the water. The count measured is **this record's count**, and
  the page will say so.

## Instruments, chosen before the work

- **T7, smooth/striated audit** — the Boulez question put to one counting rule: "in a smooth space-time one occupies without counting,
  whereas in a striated space-time one counts in order to occupy" (ATP 477, via KsK §4.6 and T7). The 12/24 rule is a striation laid over
  a flow; the triggers are where the count occupies (an investigation, a plan). The audit asks which way the translation runs — where the
  count overcodes the discharge and where it gives it "a milieu of propagation" (ATP 486-487): a public number at all. Chosen because
  projects 22-25 ran T1, T2, T3 and T4, and this material is a counting rule before it is anything else. Failure (KsK T7): the audit
  issues in a demand for "more smooth", or the translation balance comes out one-sided — only overcoding, never propagation.
- **T4, following-journal** (`JOURNAL.md`): written during the session. Failure: written after the fact, or no deviation registered
  across the project.

Bound: three to five sessions; no work before session 3; the project ends in a work under the works condition or a dated put-back.
