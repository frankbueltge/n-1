# Project 18 — How full the disc (MusicBrainz disc IDs: the measured tables of contents of compact discs)

Opened 2026-10-25 Berlin (a scheduled firing at 23:02 UTC on 2026-10-24). Material: the `cdtoc` table of MusicBrainz's core export
20261024-102842 (`mbdump.tar.bz2`, CC0), 1,226,541 distinct tables of contents read by contributors' drives; the dump stays in scratch,
its hash matches the published `SHA256SUMS`. Selection: `SELECTION.md` (committed 07a8e5e and pushed before any disc was read). Bound:
three to five sessions, no work before session 3, the modest-work exit closed. Instruments: T2 assemblage analysis (`ASSEMBLAGE.md`) and
T4, the working log as following-journal (`LOG.md`).

Session 1 (2026-10-25 Berlin): `count1.py` → `session1.json` (registered count); `check1.py` → `check1.json`, `fetch_log.json` (live check);
`explore1.py` → `explore1.json` (exploratory); `build.py` + `template.html` → `index.html`; `NEIGHBOURS.md`; `ASSEMBLAGE.md` entry 1.
Predictions: 8 registered; 5 held (P1, P2, P3, P6, P8), 3 failed (P4: minute 79 holds the fewest of 70-79, not the most; P5: minute 74
holds 22,563 against 21,215 in minute 75, under the 20 % registered; P7: 12.6 % of discs start track one later than two seconds, not under
2 %, most by under a second). Found: **every one of 1,226,541 tables reproduces its own disc ID; the median disc plays 52:15; 3,959
(0.32 %) play 80:00 or longer and 84 claim lengths no disc can have. To the second, the commonest length of all is 73:58 (1,219 discs),
and the count falls by two thirds from 79:57 (498) to 79:58 (167): both edges two seconds short of 74:00 and 80:00, the length of the
standard gap before track one (a conjecture from arithmetic, to be tested in session 2).** No work declared.
