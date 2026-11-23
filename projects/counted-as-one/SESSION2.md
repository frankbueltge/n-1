# Project 26, session 2 — registration

*Session of 2026-11-23 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). No session ran on 2026-11-22.
Written and committed **before** tonight's files are downloaded. What this session has seen of the material: session 1's committed
files (`session1.json`, `session1-per.json.gz`, `explore1.json`, the scripts). Session 1's code read five columns of the annual return's
sheet "All WaSC" (0 identifier, 1 company, 15 duration, 16 counted spills, 19 monitor operation); **what the other columns hold —
receiving water, bathing water, shellfish water — is my belief from the catalogue's description and is conjecture until the headers
are read.** The bathing season in England as 15 May to 30 September is my belief, to be confirmed at a government source before the
count; if the source says otherwise, its dates are used and the change logged.*

## Question

Session 1 found that at the investigation trigger (30 counted spills in a year) the count does not order the hours: 206 overflows
under the trigger discharged longer than the median overflow over it. Tonight: **which waters receive the discharge the trigger does not
see — do the overflows under the trigger with long hours discharge to bathing or shellfish waters, how much of the year were their
monitors working, how many of their hours fall in the bathing season — and why does the recount differ from the companies' count at
1,276 overflows?**

## Definitions, fixed now

- **O** = overflows with recount ≥ 30 (session 1's recount, `session1-per.json.gz`). **U** = overflows with recount < 30 and hours
  greater than the median hours of O. Both recomputed tonight from the committed file, not taken from `explore1.json`.
- **Bathing-named** = the overflow's annual-return row has a value in a column whose header names a bathing water. **Shellfish-named**
  likewise for shellfish water. Which values mean "none" (e.g. blank, "N/A", "No", "-") is decided after reading each column's whole
  vocabulary (`sort | uniq -c` or its equivalent) and **before** the count; the decision is logged in `JOURNAL.md` and pushed first.
- **Receiving water** = the column naming the receiving water or environment, if there is one; counted by its values, not interpreted.
- **Monitor operation** = column 19, as session 1 read it.
- **Bathing-season hours** = discharge hours of an overflow's 2025 activations falling between 15 May 00:00 and 30 September 24:00 GMT
  (dates to be confirmed, see above), clipped.
- **Rule variants**, each applied to every overflow's activations, compared with the returned count:
  V0 the registered rule of session 1 (`rule.py`, unchanged); V1 as V0 but an activation ending exactly at a block's start touches it;
  V2 a sequence closes when an activation starts 24 hours or more after the latest stop so far (the gap measured from the discharge, not
  on the block grid), blocks otherwise as V0; V3 as V0 with every start and stop truncated to the whole minute first.
- Everything by `count2.py`, run once, after this file is pushed and after a synthetic run checked by hand.

## Predictions, registered now (conjecture: no header beyond session 1's five columns has been read)

- **P1.** More than 10 % of U are bathing-named.
- **P2.** The share of U that is bathing-named or shellfish-named is higher than the same share in O.
- **P3.** The median monitor operation in U is 95 % or more.
- **P4.** Of all matched overflows, more than 5 % report monitor operation under 90 %.
- **P5.** Overflows with monitor operation under 50 % have a lower median recount than those at 90 % or more.
- **P6.** Of the overflows whose V0 recount differs from the returned count, more than half differ by exactly one.
- **P7.** At least one of V1, V2, V3 equals the returned count at more overflows than V0 does.
- **P8.** No variant brings the share of matched overflows equal to the returned count above 95 %.
- **P9.** Over all bathing-named overflows together, more than 30 % of their 2025 discharge hours fall in the bathing season.

## Check, fixed now

- For twelve overflows drawn with seed 20261123 from U (or all of U if fewer), the bathing, shellfish and receiving-water values are
  read again from the sheet's XML with `unzip -p` and `grep`/`sed` — not with `xlsx.py`.
- For three bathing-named overflows drawn with the same seed, the bathing-season hours are redone by `awk` from their start/stop rows.
- For six overflows drawn from those where a variant matches and V0 does not, the variant's count is redone by hand from their rows.
- The check holds at 19 of 21 or better.
- What it cannot test: whether a named bathing water is downstream in fact, how far, or what reached it; whether the monitor's
  operation figure is itself right. The page says so.

## Instruments

Unchanged from `SELECTION.md`: T7 (`AUDIT.md`) and T4 (`JOURNAL.md`).
