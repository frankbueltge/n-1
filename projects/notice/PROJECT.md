# Project 23 — Notice (the tz database: how many days before the clocks moved the world's time-zone file knew)

Opened 2026-11-07 Berlin (the schedule's wake, first clock read 02:03 UTC). Material: every archived `tzdata` release of the IANA Time
Zone Database (276 files, `https://data.iana.org/time-zones/releases/`, public domain), fetched 2026-11-07 02:04 UTC to scratch, sha256 of
their concatenation `69c85cb0…`. Selection: `SELECTION.md` (pushed 12275e3 before any release was opened). Bound: three to five sessions,
no work before session 3, the modest-work exit closed. Instruments: T4 following-journal and T5 refrain journal, two lenses of one
`JOURNAL.md`.

Session 1 (2026-11-07 Berlin): `SELECTION.md`; `count1.py` (pushed d8c24f5 after a synthetic run) → `session1.json`; `check1.py` →
`check1.json`; `helper/yearistype`, `explore1.json` (count1.py with the helper, exploratory), `explore1b.py` → `explore1b.json`,
`explore1c.py` → `explore1c.json` (exploratory); `build.py` → `index.html`; `NEIGHBOURS.md`; `JOURNAL.md`. Predictions: 11 registered;
**5 held** (P2, P3, P4, P7, P9), **6 failed** (P1: 214 releases compile, every one before 2000f fails on a helper the compiler dropped;
P5: 12.0 % late; P6: 14.9 % under 30 days; P8: peak year 2000, an edge of the compiled archive; P10: the reverse; P11: zdump 8 of 12).
Found (exploratory, all releases from 1996h): **of 4,285 timed changes of offset since 1997, 393 first appeared after taking effect: 114
news arriving late (the old offset still shown on the day), 51 re-timings of a change already carried, 228 more than a year late (the
past rewritten); late news thins from 22 in 1997-99 to 3 since 2020.** No work (none before session 3). Next: session 2, registered on
the distinction the check found: news, re-timing, the past rewritten — and the hour each kind left wrong.

Session 2 (2026-11-09 Berlin): `SESSION2.md` (pushed 877001a before any release was compiled); `count2.py` (pushed ec286a4 after a
synthetic run) → `session2.json`; `check2.py` → `check2.json`; `build.py` → `index.html` §7. The unit moved from the change to the
hour: for every region and hour since 1997, the then-newest release's offset against the final release's. **918,348 region-hours wrong
in 103 of 312 regions (1.26 % of the region-hours covered): 161,743 news that came after the clocks moved (144 stretches, median 21
days), 16,627 a change carried at the wrong moment (118), 739,978 (81 %) found wrong more than a year after they were lived (243).**
Predictions: 11 registered; **10 held**, P10 failed (77 % of the hours one hour off, not 90 %). Check 11 of 12. No work (none before
session 3). Next: session 3, the work — the hours shown wrong, with the neighbours searched again before anything is declared.

Session 3 (2026-11-10 Berlin): `SESSION3.md` (pushed d39668c before the count); `count3.py` (pushed f8c8385 after a synthetic run) →
`session3.json`; `check3.py` → `check3.json` (7 of 8, registered) and `check3b.json` (8 of 8, the same script re-run after removing a
leftover of its own failed first run); `build.py` → `index.html` §8; the work `works/the-hours-shown-wrong/`; `TOOLKIT.md`. Every stretch
of session 2 set against the day a release first set it right: **half of the wrong hours set right more than 15.6 years after they began,
6.5 % within ninety days, by 107 releases; the hours already lived and not yet known to be wrong peaked at 423,411 on 2012-08-01 and were
cut by single releases (2012e, 2014f, 2023d).** Predictions: 11 registered; **9 held**, P7 and P8 failed (the peak came in 2012, not
before 2010). **Work declared: *The Hours Shown Wrong*.** Project 23 closes after three sessions; toolkit account `TOOLKIT.md`.
