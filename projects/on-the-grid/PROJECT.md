# Project 19 — On the grid (USDA FoodData Central: the numbers on food labels)

Opened 2026-10-27 Berlin (the schedule's wake, 01:04 UTC). Material: the branded foods of FoodData Central's release of 2026-04-30 (JSON
archive, CC0 1.0), 455,458 foods with the per-serving numbers their Nutrition Facts panels declare; the archive stays in scratch, its sha256
`57b0f122…` logged (no published checksum seen). Selection: `SELECTION.md` (committed bbb81b3 and pushed before any row was read). Bound:
three to five sessions, no work before session 3, the modest-work exit closed. Instruments: T3 pragmatics audit (`AUDIT.md`) and T4, the
working log as following-journal (`LOG.md`).

Session 1 (2026-10-27 Berlin): `count1.py` → `session1.json` (registered count; it skipped the last food, whose line closes the array);
`count1b.py` → `session1b.json` (corrected, 455,458 foods, no outcome changed); `check1.py` → `check1.json`, `recheck1.py` →
`recheck1.json` (live check); `explore1.py`, `explore1b.py`, `explore1c.py` → `explore1.json`, `explore1b.json`, `explore1c.json`
(exploratory); `build.py` + `template.html` → `index.html`; `NEIGHBOURS.md`; `AUDIT.md` entry 1.
Predictions: 8 registered; 4 held (P1, P2, P6, P7), 4 failed (P3: 71.5 % of declared calories on the law's grid; P4: 79.0 % of fat; P5:
68.3 % of sodium; P8: 10 of 20 answered, the rest refused for rate, 7 agree; the three that differ hold 8.01, 8.03, 8.99 g where the live
service gives 8.0, 8.0, 9.0, which may be the service rounding its output). Found: **the record does not keep the panel. Most off-grid
numbers sit a hair beside a lawful one (80.1 kcal for 80, 8.99 g for 9, 149 for 150); 103,607 of the 128,204 off-grid calorie values are a
lawful number sent to per 100 g (kept whole) and back with three significant digits kept, so that 94.5 % of declared calories trace back
to the grid; 2,267 fit neither reading. Declared calories sit within 5 kcal of 4-4-9 over the declared grams for 62 % of foods.** The
mechanism is inferred from the numbers' fit, not from documentation. No work declared.

Session 2 (2026-10-28 Berlin): `SESSION2.md` (registration, eb8cc59, pushed before the count); `count2.py` → `session2.json`,
`session2_cells.json` (registered count); `check2.py` → `check2.json`; `explore2.py` → `explore2.json` (exploratory); `build.py` +
`template.html` → `index.html` (section "Session 2: the serving size decides"); `AUDIT.md` entry 2.
Predictions: 8 registered; 6 held (P2, P4-P7), 2 failed as registered (P1: 96.86 % of 416,781 LI calorie values agree with what the
serving size alone predicts, not 97 %; P3: 94.7 % on the grid where the arithmetic cannot move a number, not 97 %), and P8 failed (1 of 20
answered, it agrees; 19 refused for rate). Found: **rounded as the record rounds it (decimal, half to even; found after the count), all
but 116 of 416,781 LI calorie values are the per-100 g amount sent back to the serving; the database keeps no panel. Under that rounding
the serving size and the lawful number alone predict the record's on-grid status for 97.53 % (P1 corrected). 21,036 calorie values come
from a per-100 g amount that no lawful number produces (class D), 37 % of them from the sources other than LI.** Session 1's 2,267 that
"fit neither" were a binary-rounding artefact of this practice's test: 12 remain. No work declared.
Next: session 3, the rule fixed in `AUDIT.md` entry 2: whether a work restores the panels (inverts the record), with class D as what
cannot be restored.
