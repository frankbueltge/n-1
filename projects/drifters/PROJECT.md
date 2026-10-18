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
