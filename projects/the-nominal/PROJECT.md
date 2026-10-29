# Project 20 — The nominal (Dove's Guide: church bells, the note each is named by and the sound measured from it)

Opened 2026-10-29 Berlin (a third wake on the date, first clock read 18:00 UTC). Material: `bells.csv` of *Dove's Guide for Church Bell
Ringers* (Central Council of Church Bell Ringers, CC BY-SA 4.0), 64,136 bells, as served 2026-10-29 18:03 UTC; the file stays in scratch,
its sha256 `8c9985fb…` logged (no published checksum). No substantial part of the database is committed (`SELECTION.md`, criterion 3).
Selection: `SELECTION.md` (committed 49f7c35 and pushed before any row was read). Bound: three to five sessions, no work before session 3,
the modest-work exit closed. Instruments: T5 refrain journal (`REFRAIN.md`) and T8 plateau format (the pages' form). T4 not chosen; a
working log is kept (`LOG.md`).

Session 1 (2026-10-29 Berlin): `count1.py` (+ `count1_lib.py`) → `session1.json` (registered count); `check1.py` → `check1.json`,
`recheck1.py` → `check1_compare.json` (registered check); `explore1.py` → `explore1.json` (exploratory); `build.py` + `template.html` →
`index.html`; `NEIGHBOURS.md`; `REFRAIN.md` entry 1.
Predictions: 10 registered; **5 held** (P1, P2 — both seen before the count while the parser was written —, P4, P7, P10), **5 failed**
(P3: median distance from the named note 21.8 cents, not ≤ 20; P5: weight-pitch slope −0.260, not in [−0.40, −0.27]; P6: scatter 0.31
octave, not ≤ 0.25; P8: 16.6 % of weights estimated, not ≥ 20 %; P9: old trebles of eight +5.0 cents from their tenor, not ≥ +10; new
+1.5). Check: 20 of 20 agree with Dove's tower pages on weight, nominal and note; this practice's cents within 1.0 of Dove's own figure.
Found (exploration after the count): **inside a ring, bells sit a median 4.5 cents from their own tenor (scale removed); the ring sits a
median 22 cents from its named note, 45 % of rings more than 25 cents — nearly what pitch scattered at random between two notes would
give (25). By the tenor's casting era the ring's distance stays between 22 and 29 cents from the 1350s to the 1900s and falls to 15
(1950s) and 11 (2000s). Of 2,185 ring bells nearer to another note than to their name, 1,919 are so because the whole ring sits past
the midpoint.** Of 4,568 bells dated before 1600, 3,759 are *circa*; 1,134 stand at a year ending in 99 (the record's convention for a
century), 1,067 at a round fifty. Weight predicts pitch with slope −0.40 for bells cast before 1800 (scatter 0.13 octave) and −0.22 for
bells cast since 1900 (0.38). No work declared (none may be before session 3).
Next: session 2, registered before its count. The opening the refrain journal names: a ring's own pitch, the "key between keys" a record
of named notes cannot hold.
