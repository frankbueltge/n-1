# Project 24 — journal (T4 following-journal)

*Clocks from `date -u` at the moment of writing. Entries are not written ahead or after the fact; where one is, it says so.*

## Session 1 — 2026-11-11

- **02:04** Two files downloaded to scratch before the selection was written: `stripped.gz`, `names.gz` (hashes in `SELECTION.md`).
  Not decompressed.
- **02:05** Selection written and pushed (beab4b9) before any line was read. A first draft of this entry guessed the clock ("02:2x")
  instead of reading it; `date -u` said 02:05. The guess is struck here rather than kept as a time: a detour of the journal itself.
- **02:05** `count1.py` written and run on a synthetic file of ten lines (a prefix, a twin pair, a negative term, an empty line, a
  sequence above A300000). First run failed on the script: a median taken over an empty group (no synthetic sequence above A300000);
  guarded, re-run, every identifying length matched by hand. Pushed before the count.
- **02:05** The file read for the first time (its first lines): the format is as believed; header lines start `#`; names file the same
  form. No definition changed.
- **02:06** `count1.py` run once: 401,214 sequences, median identifying length 6, 5,861 never parted (3,394 twins, 2,467 beginnings of
  another), largest finite L 128 (four sequences of 128 shown terms that part from their nearest only at the last). Predictions: P1
  failed (401,214, above the registered 400,000 — the encyclopedia passed A400000 before tonight), P4 failed (20.3 % need three terms or
  fewer, not under 10 %), P9 failed (the six ones lead, then six zeros; the counting numbers third), P10 failed (6 and 6). 449 names have
  no line of terms: noted, not chased.
- **02:06** Check run: 18 of 18 by grep. Then, not registered: `explore1.py` on the twin groups. The largest are families of 33 to 37
  sequences entered together whose names say they are different objects and whose shown terms are the same. Detour: I had planned a
  per-group look at A-number spans as the next question; the families made the span question small beside the question of what the
  shown terms can carry.
- **T1, 02:07** `MAP.md` first drawn. The line from the search box to the advice of six terms moved session 2's question (written there).
- **02:13** Study page built and seen in a screenshot at 1440: the labels "40", "41+" and "never" ran into each other; "40" dropped,
  "never" set a line lower. `session1-per.json` (15 MB) gzipped after the run, not by the script — logged, not hidden. One sentence of
  the page first said "half are told apart by their first 6 terms"; the median says that of the finite ones; recounted (60.7 % by six of
  all) and rewritten. The Coxeter family's sentence first named "36 generators" from the first and last names only; every member's name
  read before it was written.
- **02:13** `render-check.js` 74 of 74 ok at 1440 and 390.
- **02:14** Before commit, the family of 37 checked member by member (identical lines to A063819): 35 Coxeter groups with relations of
  order 16 to 50, not 12 to 50 as first written from a looser match of sixteen terms (41 lines; the orders 12-15 show more terms and
  part within them). Page and night record corrected before anything was pushed.
