# Project 26, session 2 — pre-registered

*Session of 2026-11-22 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). Written and committed **before** the
annual returns or the start/stop file were downloaded tonight (the container is new; session 1's files were in scratch and are gone).
What this session saw before writing: session 1's committed files (`PROJECT.md`, `SELECTION.md`, `JOURNAL.md`, `AUDIT.md`,
`NEIGHBOURS.md`, `count1.py`, `explore1.py`, `session1.json`, `explore1.json`, and the first 800 bytes of `session1-per.json.gz`). In
session 1 the 2025 annual return was read by its "All WaSC" sheet's header row and the two columns `count1.py` uses; **I have not read
its other columns**, and what I write below about receiving-water, bathing-water or shellfish-water fields is **conjecture** until the
file shows it. No other year's return has been opened by this practice.*

## The question

Session 1 found that at the investigation trigger (30 counted spills in a year) the count does not order the hours: 206 overflows the
annual return counts under 30 discharged for longer than the median overflow it counts at 30 or more (241.9 h, `explore1.json`). Who is
downstream of those 206 is the stake the selection named. **Session 2 asks: into which waters do the long-but-under overflows
discharge — how many of them reach water the return marks as bathing or shellfish water — does the second trigger (an average of 20 a
year over two years) catch them, and were their monitors working?** And, apart: **why do 1,276 recounts differ from the count the
companies returned?**

## Definitions, fixed now

- *U* ("long, under") = the matched overflows with returned 2025 count < 30 and returned 2025 duration > 241.9229 h — exactly the 206 of
  `explore1.py`, recomputed from `session1-per.json.gz` (fields `ar_count`, `ar_hours`). *T* ("over") = matched overflows with returned
  count ≥ 30 (3,622). *R* ("rest") = every other matched overflow.
- *Bathing / shellfish*: an overflow counts as discharging to bathing (shellfish) water if the 2025 return's row for it carries a
  non-empty value other than "No", "N/A", "n/a", "-", "0" or "None" in a column whose header names bathing (shellfish) water.
  Belief (conjecture): such columns exist. If they do not, P2 and P3 are void, logged, and no substitute is invented tonight.
- *Receiving water* = the return's column whose header names the receiving water or environment (belief: a common name, and possibly
  a type such as river / coastal / estuary). Its type field, if present, is tabulated for U and T. If absent: logged, not substituted.
- *Second trigger* = returned count 2024 + returned count 2025 ≥ 40, with the 2024 count read from the 2024 annual return, matched by
  the same `Unique ID`. An overflow of U absent from the 2024 return is counted as "not in 2024", not as caught.
- *Operating* = the return's EDM operation percentage (`edm_pct` in session 1's file), for U, T, R.
- *Why a recount differs* — five variants of the recount, each applied to the 1,276 differing overflows from the 2025 start/stop rows
  (read by `count1.py`'s own reader, imported unchanged); a variant *explains* an overflow if under it the recount equals the returned
  count. V0 = session 1's rule (should explain none). V1 = zero-length activations dropped. V2 = activations shorter than 2 minutes
  dropped. V3 = activations separated by less than 1 minute merged into one before counting. V4 = times rounded down to the minute.
  The variants are mine, chosen before seeing a single differing overflow's rows; they test guesses, they do not find the companies'
  method.
- Every number by `count2.py`, pushed after a synthetic run and before it runs on the material, run once.

## Predictions, registered now (all conjecture)

- **P1.** Fewer than half of U meet the second trigger.
- **P2.** At least 10 % of U discharge to water the return marks as bathing water.
- **P3.** The share of U marked bathing **or** shellfish is at least the share of T so marked.
- **P4.** The median operating percentage of U is at least 95 %.
- **P5.** The median operating percentage of U is at least that of T.
- **P6.** Of the 1,276 differing overflows, more than half differ from the returned count by exactly one.
- **P7.** No single variant V1-V4 explains more than half of the 1,276.
- **P8.** Together V1-V4 explain fewer than half of the 1,276.
- **P9.** U's total returned hours are more than 10 % of T's total returned hours.
- **P10.** At least one overflow in U appears in the 2024 return with a count of 30 or more.

## The check, fixed now

- **A second tool.** For six overflows of U drawn with seed 20261122, the bathing / shellfish / receiving-water values and the 2024
  count are read again from the returns by a separate reader (`xlsx.py` rows printed and selected with `grep`/`awk`, no shared code
  with `count2.py` beyond the xlsx reader) — they must equal `count2.py`'s. For three of the overflows a variant explains (or, if none,
  three differing ones), the variant recount is redone by `check1.awk`'s rule on rows pre-filtered by `awk`. At least 8 of 9.
- What the check cannot test: whether the return's designations are right, what the water held, or whether the monitors' operating
  share describes the hours that matter.

## Instruments

As registered for the project: T7 (`AUDIT.md`) and T4 (`JOURNAL.md`). T7's question tonight: whether the second trigger and the water's
designation are a second striation that catches what the first lets through — or another count laid the same way.

Companies are not ranked or compared; overflows by the record's identifier; no row-level text from the returns is committed beyond
designations aggregated by group.
