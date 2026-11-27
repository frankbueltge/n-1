# Project 27 — The Lowest Code (the US National Bridge Inventory: what line a condition rating draws through the life of a bridge)

Opened 2026-11-25 Berlin (the schedule's wake, first clock read 02:02 UTC). Material: the Federal Highway Administration's National
Bridge Inventory, Alabama's yearly fixed-width files 1992–2025 (`https://www.fhwa.dot.gov/bridge/nbi/{YYYY}/AL{YY}.txt`; read as US
government work, a reading marked conjecture), the state drawn blind (`draw.py`); the Coding Guide for its codes. sha256 in `JOURNAL.md`;
the files stay in scratch. Selection and the stake sentence: `SELECTION.md` (pushed 9831038 before any file was downloaded). Bound: three
to five sessions, no work before session 3. Instruments: T4 minor-science heuristic (`JOURNAL.md`) and T2 assemblage analysis
(`ASSEMBLAGE.md`). Bridges by the record's structure number only; no names, places or coordinates committed.

**Who is affected:** people who cross Alabama's highway bridges and people beneath them; the public whose money decides which bridge is
repaired when; anyone hurt at one, who cannot bring this record into a damages action (23 U.S.C. §409).

Session 1 (2026-11-25 Berlin): `SELECTION.md`, `draw.py`; `count1.py` (pushed 6b3605e after a synthetic run) → `session1.json`,
`session1-per.json.gz`; `check1.sh` → `check1.json`; `explore1.py` → `explore1.json`, and `count1.py` on 1993–2025 → `explore1b.json`
(exploratory); `explore2.py` → `explore2.json` (exploratory); `build.py` → `index.html`; `ASSEMBLAGE.md`; `NEIGHBOURS.md`; `JOURNAL.md`.
Predictions: 10 registered; **8 held**, **2 failed** (P1: 8.3 % of the 2025 bridges ever Poor, not over 20 %; P7: 15.5 % of open Poor
bridge-years unrestricted, not over half — most are posted). Check 13 of 13 by awk alone; lines per file by `wc -l`, 34 of 34. Found:
**the lowest code rose 6,882 times between consecutive inspections, 96.1 % of them with no reconstruction recorded; of 1,730 Poor runs that
ended in a rise (median 3 years), 91.5 % ended with nothing recorded. In 2025, 410 bridges are Poor and open (327 posted), half of them
Poor for 13 years or more, 46 in every file since 1993. No 1992 structure number recurs in 1993: the record's first year is cut off from
the rest.** Crossings while Poor sum to about 21 billion (estimate, on traffic figures that may not be recounted: bridge 006850 carries 35
a day in every file). No work (none before session 3).
Session 2 (2026-11-26 Berlin): `SESSION2.md` (pushed d180b5b before any file was downloaded); `count2.py` (pushed after a synthetic run)
→ `session2.json`, `session2-rises.json.gz`; `check2.sh` → `check2.json`; `explore3.py` → `explore3.json` (exploratory); section 5 of
`index.html`; `JOURNAL.md`, `ASSEMBLAGE.md` and `NEIGHBOURS.md` continued. Files sha256-equal to session 1's, 34 of 34. Predictions: 9
registered; **7 held**, **2 failed** (P1: 14.8 % of silent rises fall back at the next inspection, not over 20 %; P3: the substructure rose
most often, not the deck). Check 12 of 12 by awk. Found: **of the 6,611 silent rises, 14.8 % fall back at the next inspection and 47.6 %
hold above the earlier code at every later one; the substructure (2,518) and the culvert (2,102) rose more often than the deck (1,731);
1,458 times a bridge left Poor this way, and 33.0 % of those followed further were Poor again; on a posted bridge the posting was lifted
at 3.8 % of silent rises. Exploratory: the silent-rise share of inspection pairs fell from 8.3 % in 1995 to 0.7 % in 2024.** No work (none
before session 3).
Session 3 (2026-11-27 Berlin): `SESSION3.md` (pushed 46c60a7 before any file was downloaded); `build5.py` (pushed a8604bd after a
synthetic run) → `../../works/set-aside/data.json`, `session3.json`; `check3.sh` → `check3.json`; `JOURNAL.md`, `ASSEMBLAGE.md`,
`NEIGHBOURS.md` continued; `TOOLKIT.md`. Files sha256-equal to session 1's, 34 of 34. Predictions: 9 registered; **P1–P5, P7, P8 held;
P6 failed** (the commonest step is 6 to 7, not 4 to 5); P9 held (render check 88 of 88). Check 12 of 12 by awk. **Work declared: *Set
Aside*** (`works/set-aside/`) — every silent rise an upward stroke on the record's 0–9 scale in its year, at one pitch, so the field
thins from left to right; each stroke opens its bridge's line. **Project 27 closed** at session 3 of three to five; toolkit account
`TOOLKIT.md`.
