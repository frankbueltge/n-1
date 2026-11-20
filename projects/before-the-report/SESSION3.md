# Project 25, session 3 — the work, pre-registered

*Session of 2026-11-20 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
enforcement file was downloaded tonight and before the work's data script was run. What this session saw before writing: sessions 1 and
2's files and results (`PROJECT.md`, `SESSION2.md`, `JOURNAL.md`, `ASSEMBLAGE.md`, `NEIGHBOURS.md`, `count2.py`, `session1.json` — its
per-report-year record counts and the event-level W summary, median 44 days over 27,896 events). Nothing else of tonight's material.*

## The question the work asks

Sessions 1 and 2 measured a delay: a recall begins on one day (the firm's first notice, in 78 % of events addressed to customers only)
and the FDA's public list names it a median 47 to 50 days later. A delay measured is a number; a delay *undergone* is a stretch of days
in which some people know and the list does not. **The work asks: on any given day, how many recalls have already begun that the public
list does not yet name — and what does that stretch sound and look like when it is let pass rather than summed?**

## Form, fixed now (to be argued in `WORK.md`)

Duration, played. One calendar year of the register passes at one day per second (about six minutes). Every recall event that **began**
that day is a quiet click — softer when the firm's first notice went to customers only, a clear struck tone when it was a press release.
Every recall event the list **named** that day sounds in the register's own rhythm: the list appears weekly, so the names arrive as one
chord per week whose loudness follows how many it holds. On the screen, each event is a thread from the day it began to the day it was
named, drawn as the year passes; one number stands above it all: **begun, not yet on the list** — the events with start ≤ that day <
listing, counted on that day. Sound starts only when the visitor presses play; the page reads and works silently. A year selector
(the complete report years of the material). Three short paragraphs below.

## Definitions, fixed now

- *Record*, *event* exactly as session 1 and 2 (`SELECTION.md`, `SESSION2.md`): an event is a centre and an `event_id`.
- *Start* S of an event = the earliest valid `recall_initiation_date` among its records. *Listing* L = the earliest valid `report_date`.
  Events with no valid S or L, or with L < S, are kept out of the threads and the count and counted as excluded.
- *Notice* of an event exactly as `count2.py` (`group()` and the event rule, imported unchanged).
- *Gravest class* exactly as `count2.py`.
- *Begun, not yet on the list* on day t = number of events with S ≤ t < L. An event that began and has not yet been listed when the
  files were exported is **not in the files** (the register holds only what it has listed), so the count on the most recent days is
  a lower bound; the work shows only complete calendar years, ending at least 365 days before the export.
- The work's data: one line per event (S, L as day numbers, centre, gravest class, notice group); no firm, product or reason text.
- Every number by `build3.py`, pushed after a synthetic run and before it runs on the material, run once.

## Predictions, registered now (all conjecture)

- **P1.** The files hold at least 27,896 events.
- **P2.** In 2025, the median over the year's days of *begun, not yet on the list* lies between 250 and 650.
- **P3.** In every complete calendar year of the material, *begun, not yet on the list* never falls to zero on any day.
- **P4.** In 2025, the largest daily value of *begun, not yet on the list* is less than twice the year's median.
- **P5.** Of all events with L in 2025, at least 95 % have an L falling on one and the same weekday.
- **P6.** Of all events with S in 2025, fewer than 5 % have notice **public**.
- **P7.** Excluded events (no valid S or L, or L < S) are fewer than 20.
- **P8.** The work's data file, uncompressed, is under 2 MB.
- **P9.** The check (below): at least 11 of 12.
- **P10.** The render check passes at 1440 and 390 wide with the work's page among the pages probed.

## The check, fixed now

- **A second tool.** Twelve events drawn with seed 20261120 (four per centre): for each, `jq` selects the event's records by `event_id`
  from the unzipped file, takes the minimum initiation and report dates; the check holds if they equal the work's S and L for that event.
- **The count, again.** For three days drawn with the same seed in 2025, *begun, not yet on the list* recomputed with `jq` over all three
  files (events grouped by `event_id`, minimum dates), compared with the work's value.

## Neighbours

Searched again before the work is declared: the Atlas of Data Art (fetched fresh), and a web search on sonified or played recall and
regulatory-delay data. Named in `NEIGHBOURS.md` with how far each was read.
