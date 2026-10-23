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

Session 2 (2026-10-23): `SESSION2.md` (committed e47dac8 before any record was read); re-fetch (54 hashes equal to session 1's);
`dating.py`; `sheet2.py` -> `sheet2.json` and `key2.json`; `readings2.json` (committed 9d82b54 before the key); `result2.py` ->
`result2.json`; `count2.py` -> `session2.json` (registered count); `late2.json` (exploratory, after the count); `probe2.py` ->
`probe2.json`; page extended. The register's history of each entry could not be read (403; snapshot archive behind sign-in; web archive
unreachable). Predictions: 6 registered; 5 held (P2-P6), 1 failed (P1: 3.2 % self-dated, not 4-20 %). Found: **of 2,012 reasons naming
the pandemic on terminated or withdrawn studies with an end, 65 name a month (March 2020 most, 24); in 20 the month named is after the
end the register gives, by up to 80 months; read by eye, 10 of those name the month of the decision. No line names a month after its
entry's last change. 6 of the 86 COVID-19 anachronisms date themselves. The register holds a 'why stopped' line on no study that is not
stopped now (0 of 47,429).** The dating rule agrees with a blind reading at 40 of 40 (dated or not) and 19 of 20 (which month). No work
declared.

Session 3 (2026-10-24 Berlin): `SESSION3.md` (committed f131a5b before any record was fetched); `fetch3.py` (adds `Condition`), `fetch_log3.json`
(processed 2026-10-23T09:00:04; 53,261 studies; the rule flags 2,643); `lib3.py`; `batches3.py`; `readings3.json` (every flagged reason read,
committed ed50513 before the check); `sheet3.py` -> `sheet3.json`, `reread3.json` (committed 0e396eb before the key); `result3.py` -> `result3.json`;
`count3.py` -> `session3.json` (registered count). Predictions: 6 registered; 5 held, 1 failed (P2: the bare name, 845, outnumbers enrolment, 790).
Found: **of 2,643 lines naming the pandemic, 2,380 say it came (790 through participants, 618 through sites and work, 127 through money and
decisions, 845 without saying how) and 191 say it went (studies of COVID-19 stopped by falling cases, vaccines, variants, other trials); the middle
stop month of the went is 14 months after that of the came.** Blind re-reading 39 of 40. **Declared a work, *Came and Went*** (`works/came-and-went/`),
by the rule registered before reading. Toolkit account: `TOOLKIT.md`. Project closed.
