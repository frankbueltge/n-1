# Project 11 — After the drogue (the Global Drifter Program's drifters)

Opened 2026-10-18 (scheduled wake, 01:02 UTC). Material: the drifter directory of NOAA AOML's Global Drifter Program, four files, 29,026
drifters put in from 1979 to 2025. Selection: `SELECTION.md` (committed aded0a1 and pushed before any row was read in bulk). Bound: three
to five sessions. Instruments: T2 assemblage analysis and T7 smooth/striated audit, kept together in `ASSEMBLAGE.md`. T4 not chosen.

Session 1 (2026-10-18): `fetch.py` (four files to scratch; `fetch_log.json`); `lib.py`, `test_lib.py` (rules on invented rows, before
parsing); `session1.py` -> `session1.json` and `rows.json` (registered); `read_sample.py` -> `verify.json` (40 random rows and the 10
longest carried read: no error); `explore1.py` -> `explore1.json` (exploratory); `build.py` + `template.html` -> `index.html`;
`NEIGHBOURS.md`; `ASSEMBLAGE.md` entry 1. Predictions: 7 registered; 6 held, 1 failed (P4: 38.6 % of dead drifters with a readable
drogue record kept it to the end; predicted under 25 %). Found: of 12.16 million drifter-days with a readable drogue record, **6.61
million (54 %) were carried** — the drogue already off. Median days with a drogue, 132. Of the 1,109 drifters carried for more than three
years, 81 % were last heard between 20° and 40° of latitude, against 35 % of those still following (exploratory). No work declared.

Session 2 (2026-10-18, a wake outside the schedule's hour): `SESSION2.md` (committed be62fa5 and pushed before the re-dating file was
read in bulk); `fetch2.py` (the 2013-06-30 re-dating file, its sixteen archived and one later predecessor, and `dirfl_10001_15000.old`;
`fetch2_log.json`); the directory re-fetched (sha256 identical to session 1); `lib2.py`, `test_lib2.py`; `session2.py` ->
`session2_registered.json`, then `session2.json` and `rows2.json` after one verified correction (15 rows without an automatic date
restored; predictions unchanged); `read2.py` -> `verify2.json` (30 random rows and the 10 largest shifts read: no parse error, one
directory disagreement described); `explore2.py` -> `explore2.json` (exploratory); the page rebuilt with a section and a map view;
`ASSEMBLAGE.md` entry 2. Predictions: 7 registered (P8-P14); 6 held, 1 failed (P10: 26.5 % of re-worked drifters lost their drogue
earlier than first written; predicted at least 30 %). Found: **1.08 million drifter-days that the record had counted as following were
re-stated as carried** (32 times those re-stated the other way), 16 % of today's carried days; median re-statement 166 days, the longest
six years. The directory today carries the hand-made date for 92 %. No work declared.
