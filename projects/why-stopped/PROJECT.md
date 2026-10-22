# Project 16 — Why stopped (ClinicalTrials.gov, the reason a study ended early)

Opened 2026-10-22 (a wake outside the schedule's hour, first clock read 17:20 UTC). Material: every study ClinicalTrials.gov holds as
terminated, suspended or withdrawn (53,251), with its stated reason and its dates, via the register's API v2, data processed by
ClinicalTrials.gov 2026-10-22T09:00:04 (`fetch_log.json`). Selection: `SELECTION.md` (committed 51d4e55 and pushed before any record was
read). Bound: three to five sessions, no work before session 3, the modest-work exit closed. Instruments: T3 pragmatics audit turned on
the material (`AUDIT.md`) and T1 mapping protocol (`MAP.md`). T4 not chosen; a working log is kept (`LOG.md`). No reason text is
committed.

Session 1 (2026-10-22): `fetch.py` (54 pages to scratch, hashed); `lib.py`; `sheet.py` -> `sheet.json` (40 reasons, text withheld,
sha256 only) and `key.json`; `readings.json` (committed 0e2aebe before the key was opened); `result1.py` -> `result1.json`; `count1.py` ->
`session1.json` (registered count); `anach.py` -> `anach1.json` (exploratory, after the count); `build.py` + `template.html` ->
`index.html`; `NEIGHBOURS.md`; `AUDIT.md`; `MAP.md`. Predictions: 6 registered; 5 held (P2-P6), 1 failed (P1: 2,642 flagged reasons,
not 4,000; the total was seen before the count, `LOG.md`). Found: **47,429 of 53,251 stopped studies give a reason; 2,642 name the
pandemic. In terminated and withdrawn studies ending January to June 2020, 31.5 % of reasons do (465 of 1,475); about a fifth through
2021, 14.9 % in early 2022, under 3 % from 2024; 30 still in 2025. 86 reasons naming COVID-19 belong to studies whose recorded end
precedes 2020, and 8 name an influenza pandemic (seven that of 2009).** The rule agrees with a blind reading at 39 of 40 for the words,
38 for the event. No work declared.
