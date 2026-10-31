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

Session 2 (2026-10-30 Berlin, the schedule's wake): `SESSION2.md` and `count2.py` pushed before the count (f88bef3); `count2.py` →
`session2.json` (registered count, inside check); `explore2.py` → `explore2.json` (exploratory); page section 8; `REFRAIN.md` entry 2.
Predictions: 8 registered; **4 held** (P1: positions not even but weakly held, concentration 0.10 over 6,549 rings; P4: before 1800,
0.012; P7: 1,018 of 1,204 rings with a tuning year have a tenor 50+ years older; P8: towers.csv's Hz agrees with the tenor's for 6,546 of
6,547), **4 failed** (P2: 1950 and later 0.28, centred −8.5, not ≥ 0.5 within ±10 of A = 440; P3: 1850-1899 0.03, no centre near old
philharmonic pitch; P5: 3 of 5 large foundries 1880-1949 with Rayleigh p < 0.01, not two thirds; P6: Loughborough −20.5, Gillett −20.5).
Found (exploration after the count): **positions between the keys are nearly even, with two narrow columns: 382 rings (5.8 %) within
1.5 cents of A = 440 and 287 (4.4 %) of A = 435, the French diapason normal of 1859, against 3 % for an even spread; old philharmonic
pitch 2.8 %, no trace.** A = 435 is strongest among tenors cast 1925-1974 (9.7 %, 8.2 %) and in the Gillett foundry's rings (11.2 %);
A = 440 among tenors cast 1975-1999 (33.7 %) and in Whitechapel's (10.0 %). The columns are not made by whole-hertz recording (4,540
whole-hertz tenors and 2,009 others give the same rates). No work declared.
Next: session 3, registered before its count; a work may be declared from it. The opening the refrain journal moved to: the pitch that
belongs to one tower alone.

Session 3 (2026-10-31 Berlin, the schedule's wake): `SESSION3.md` and `count3.py` pushed before the count (c568460), the work's form and
the declaring rule in them; `count3.py` → `session3.json` (registered count and inside check); `explore3.py` → `explore3.json`
(exploratory); `sound3_render.js` + `sound3.py` → `sound3.json` (sound check); page section 9; `REFRAIN.md` entry 3; `TOOLKIT.md`.
`bells.csv` had changed since session 2 (203 B); the count reproduces session 2's 1-cent histogram exactly.
Predictions: 8 registered; **5 held** (P1: first decade over 25 % at A = 440 is the 1970s; P3: median beat before 1900 6.2 per second;
P5: 74 decades hold a ring; P7: inside check, difference 0; P8: sound check within 0.0001 cent), **3 failed** (P2: the 1410s and 1830s
concentrate above 0.25, 0.28 each; P4: since 1990 the median beat is 4.9, not ≤ 2.0; P6: most rings in the 1920s, 359).
Found: **the share of rings on A = 440 peaks in the 1970s (29 %) and 1980s (27 %) and falls after (16 %, 8 %, 11 %, 5 %); 1930-1959 rings
gather at A = 435. Since 1990, 503 of 722 rings dated are old heaviest bells retuned, beating a median 5.8 per second against A = 440; new
ones 2.5 (exploratory).** **Declared a work, *Between the Keys*** (`works/between-the-keys/`), by the rule registered before the count:
P7, P8, neighbours searched again, render-check ok. The project closes (toolkit account `TOOLKIT.md`).
