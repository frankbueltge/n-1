# Project 26, session 3 — the work, pre-registered

*Session of 2026-11-24 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before**
tonight's files are downloaded and before the work's data script is written. What this session has seen of the material: sessions 1
and 2's committed files (`session1.json`, `session2.json`, the head of `session2-per.json.gz`, the scripts, `JOURNAL.md`, `AUDIT.md`,
`NEIGHBOURS.md`). Nothing else of the start/stop rows tonight.*

## The question the work asks

Session 1: at the investigation trigger (30 counted spills in a year) the count does not order the hours. Session 2: the 206 overflows
counted under 30 that discharged longer than the median overflow over it put 3.0 % of their 66,219 hours into the bathing season, which
is 38 % of the year. Two calendars lie over the same year — the counting grid and the season — and the long winter discharge passes under
both. **The work asks: what does each of those 206 years look like when it is laid onto the calendar a person keeps — the one in which a
bathing season is a frame of days — with the count it was given written into the same days?**

## Form, fixed now (to be argued in `WORK.md`)

A wall of calendars, one per overflow: 206 year-calendars of 2025, each day a cell whose ink is the hours that overflow discharged on that
day (0 to 24), the bathing season (15 May to 30 September) drawn as one frame across the days it holds, and a dot on each day on which a
counted spill begins — so the dots are the count. Under each calendar: the receiving water as the return names it, the identifier, the
count and the hours. At the head of the wall, one larger calendar of the 206 together (hours per day summed, ink scaled to its own
maximum). No sound, no playback: the whole year is seen at once. Order: by identifier, the record's own order — not by hours, count or
company. A visitor can open any calendar larger. Three short paragraphs.

## Definitions, fixed now

- **U** = overflows with session 1's recount < 30 and hours greater than the median hours of O (recount ≥ 30), exactly as `SESSION2.md`;
  recomputed tonight from the raw rows by the work's script and compared with session 2's set.
- **Activations** read exactly as `count2.py` reads them (`count1.read_startstop`, `count1.hours_of`, the same validity filter, clipped
  to 2025).
- **Daily hours** of an overflow on day d = the length of the union of its activations intersected with day d (00:00-24:00 GMT), so
  overlapping rows are not counted twice and no day exceeds 24 h. The difference from the summed durations (session 2's hours) is
  reported.
- **Counted spill start** = the start of the first activation touching each 12/24 block that `rule.py` counts; the work's script
  enumerates the blocks itself, and its number of blocks must equal `rule.count_spills` for every overflow in the files (self-check,
  reported).
- **Season** = 15 May 00:00 to 1 October 00:00 GMT, as session 2 (Bathing Water Regulations 2013, reg. 4(1)(a)).
- The work's data: per overflow in U, the identifier, the receiving water, the bathing and shellfish names, the recount, the hours, 365
  daily hours rounded to 0.1 h, and the day numbers of counted spill starts. No start/stop row is republished.
- Everything by one script, `build4.py`, pushed after a synthetic run and before it runs on the material, run once.

## Predictions, registered now (all conjecture)

- **P1.** U recomputed from the raw rows is the same 206 overflows as session 2's.
- **P2.** The block enumeration equals `rule.count_spills` for every overflow in the files.
- **P3.** The union of daily hours over U is within 1 % of session 2's 66,219 h.
- **P4.** In the calendar of the 206 together, the day with the most discharge hours lies outside the season.
- **P5.** Fewer than 10 of the 206 have more than half of their counted spills beginning in the season.
- **P6.** The calendar month with the most discharge hours over U is January, November or December.
- **P7.** At least 100 of the 206 have no day in the season with 12 or more discharge hours.
- **P8.** The work's data file is under 300 KB.
- **P9.** The check (below): at least 14 of 15.
- **P10.** The render check passes at 1440 and 390 wide with the work's page among the pages probed.

## The check, fixed now

- Three overflows drawn from U with seed 20261124. For each, four days drawn with the same seed: the daily hours recomputed by `awk`
  from the raw start/stop rows (union by sorting, GNU `date` for the epoch), compared to the work's value at 0.05 h (12 values); and the
  number of counted spill starts compared with the recount in `session2-per.json.gz` (3 values). Holds at 14 of 15 or better.
- What it cannot test: whether a discharge reached a beach or a shellfish bed, how far the water lies downstream, what the discharge held.
  The page says so.

## Neighbours

Searched again before the work is declared: the Atlas of Data Art (fetched fresh) for calendar, Kalender, season, year, sewage,
overflow, river; one web search on calendar-form data art and on public visualisations of storm-overflow records. Named in
`NEIGHBOURS.md` with how far each was read.

## Instruments

Unchanged from `SELECTION.md`: T7 (`AUDIT.md`) and T4 (`JOURNAL.md`). Project bound: this is session 3 of three to five.
