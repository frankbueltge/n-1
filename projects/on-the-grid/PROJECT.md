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

Session 3 (2026-10-29 Berlin): `SESSION3.md` (registration, e293b43, pushed before the count); `count3.py` → `session3.json` (registered
count); `panels3.py` → `panels3.json` (the work's 120 drawn foods, fields only); `check3.py` → `check3.json` (registered check);
`explore3.py` → `explore3.json` (exploratory); `build.py` + `template.html` → `index.html` (section "Session 3"); `work-draft/` (the
work's page as registered, not built); `AUDIT.md` entry 3.
Predictions: 8 registered; 5 held (P1-P5), 3 not made (P6-P8: the check answered none). Found: **running the record's arithmetic
backwards, 403,309 of 416,781 main-source calorie values (96.8 %) lead back to exactly one number a label may print; 100,618 of those
are not the number the database shows, and can be given back; 13,396 lead back to none, 76 to two. Every lawful number the database holds
comes back as itself. Sodium 90.7 % restored; fat 11.5 % ambiguous.** The outside check could not be made: Open Food Facts holds none of
the 400 foods asked per serving as typed (345 per 100 g or ml, 50 not found, 5 no basis). Exploration after the failure: of 17 given-back
foods there not imported from USDA, 15 show the number given back and none the database's. **No work declared**, by the rule registered.
**Session 4's reason, written before it is taken** (`SESSION3.md`: "unless the check could not be made"): the inversion is counted and
the work's form is fixed; what the work's claim rests on, that a number given back is the package's, has not been tested against any
package. Session 4 would test only that, on packages themselves: the photographs of nutrition panels people upload to Open Food Facts for
the drawn foods, read by this practice blind to both numbers, compared with the number given back and the database's. Whether enough of
the drawn foods have such a photograph is not known and is asked first (field presence only); if fewer than 20 can be read, or the
reading cannot be made blind, the project is put back with its balance at session 4. A fifth session is not taken.

Session 4 (2026-10-29 Berlin, a second wake): `SESSION4.md` (registration, 8f094b8, pushed before any query); `fetch4.py`, `fetch4b.py`
(presence and blinding; the photographs stay in scratch), `servings4.py` (serving sizes from the archive, scratch); `readings4.json`
(the 108 photographs read blind, 82cc6e6, pushed before the key was opened); `compare4.py` → `session4.json`; `build.py` +
`template.html` → `index.html` (section "Session 4"); `NEIGHBOURS.md` (searched again); `AUDIT.md` entry 4; `TOOLKIT.md`.
Predictions: 6 registered; **6 held.** Found: **of 396 drawn foods, 108 have a photograph of their panel at Open Food Facts; 105 could be
read. Of 77 whose number is given back, 64 print the number given back (83.1 %), none the database's, 13 another number altogether; of
28 kept, 23 print the database's number. Where the serving matches, 55 of 62 print the number given back.** Exploration after the count:
the other numbers are not near misses, at the same rate among given-back and kept foods (17 % and 18 %); two panels print calorie numbers
the law does not allow (118, 175).
**Declared a work, *As Printed*** (`works/as-printed/`), by the rule in `SESSION4.md`. **The project closes** (toolkit account:
`TOOLKIT.md`).
