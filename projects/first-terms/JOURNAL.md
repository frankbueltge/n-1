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

## Session 2 — 2026-11-13

- **02:02** First clock read. No night ran on 2026-11-12. Session 1's scratch is gone with its container; `stripped.gz` and `names.gz`
  downloaded again (02:02:55): both differ from session 1's (file of 2026-11-12, hashes in `SESSION2.md`). Not decompressed.
- **02:03** The search hints page fetched with `curl` and read as text: a comma search matches the numbers "consecutively, in the order
  given", anywhere; `seq:` "possibly" ignores signs, `signed:` does not. `SESSION2.md` says this fetch was at 02:04; no clock was read at
  the fetch, it lies between the two clocks read (02:02:55 and 02:04:13). Logged, not corrected in the registration.
- **02:04** Registration pushed (624986e) before any line was read: B (the box, typed from the beginning), M (the shortest run that finds
  a sequence alone), never found alone; signed primary, signs ignored secondary; eleven predictions.
- **02:05** `count2.py` written (hashed runs, one term longer per pass) and run on a synthetic file of eight lines (twins, a run inside
  another, a negative term that only signs tell apart, a run of zeros); first try failed because `python3 -I` did not see a numerical
  library, which was not installed in this container; installed, re-run, every value matched by hand. Pushed (c595ca7) before the count.
- **02:05** The first launch of the count did nothing: it was wrapped in a timing tool this container does not have, and the shell
  stopped before Python started (no output file). Not a run; launched again at 02:05:50 without the wrapper.
- **02:16** The count still running after ten minutes, over 1 GB of memory; the plan assumed a minute or two. Not stopped: the
  registration says run once.
- **02:28** Stopped the count at 20 min 49 s. A stack dump (a sampling tool installed for the purpose) showed it in the summary, not
  the counting: the line listing the sequences with the largest B recomputed the maximum once per sequence, about 1.6 × 10^11 steps.
  Nothing had been printed or written; no number of tonight's was seen. Fixed that line and its twin for M only (the maximum computed
  once), the synthetic run re-run with byte-identical output, the fix pushed before the second launch. The registration's "run once" is
  kept in this sense only: one run produced numbers. Logged as a deviation.
