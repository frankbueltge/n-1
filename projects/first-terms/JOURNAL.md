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
- **02:27** The entry above was headed 02:28 without a clock read; `date -u` at its commit said 02:27:01. Second launch of the count at
  02:27 (clock in the run's own output).
- **02:30** Second run finished in about three minutes (clocks 02:27 and 02:30:27 in its output). File form as believed; no definition
  changed. 401,318 sequences. Signed: **median B 6, median M 2, 8,045 never found alone (2.00 %)**, of them 3,394 twins, 2,466 beginnings
  of another, 2,185 inside another. Predictions: P2 failed (median B 6, not 7-10: the box costs a third of the sequences more terms, but
  not the median one), P4 failed (median M 2, not 3-5: 173,951 sequences are found by one number alone), P7 failed (52.3 % give a single
  hit at six terms, not under half), P8 failed (signs ignored change M for 2.8 %, not under 2 %). Held: P1, P3 (32.0 %), P5 (95.8 %), P6,
  P9 (117), P10 (132).
- **02:31** Check by `grep -c -F`: 18 of 18 (P11 held). Every run of length M−1 of the twelve found-alone sequences grepped, 325 runs (the number first written here, 449, was not counted; recounted from `check2.json` before commit).
- **02:31** Not registered: `explore2.py`, the extremes and eight sequences everyone knows, by name. **Seven of the eight can never be
  found alone**: the Fibonacci numbers stand whole inside A212804 (the same numbers with a 1 in front), the squares inside A305559
  ("[0, -1, -1] together with A000290"), the factorials inside two shifted copies, the primes inside or beside eleven others, four of them twins (`explore2c.json`; one holder is "prime numbers at
  the beginning of the 20th century"), the counting numbers, the ones and the zeros inside dozens. Checked with `grep -F` on the whole
  shown run, not with the count. The Catalan numbers are found alone, by fifteen later terms (the 16th to the 30th of 31 shown). Detour: I had planned to read the
  shortest names as the next question; the canon's being unfindable is the larger line.
- **02:32** Not registered: `explore2b.py`, by A-number band. Never found alone: 3.2-3.6 % of sequences up to A200000, then 0.8-0.9 %
  above. Why the step: not in this material; not guessed at on the page.
- **02:32** Signed hits at six: 206,892 sequences give one hit for their first six terms; **84,847 give fifty-one or more** (the zeros
  9,536). The advice of six terms works for half and fails badly for a fifth.

## Session 3 — 2026-11-15

- **02:02** First clock read (02:02:51). The stored prompt asks for the whole paper; per gift 1 as amended 2026-08-22 the carry was read
  instead (`reading/CARRY.md`), with `DOWRY.md` whole, the two notes of 2026-11-14 in `REQUESTS.md`, night 110, and this project's files.
  The act "material with a stake" binds from the next project; project 24 finishes under the conditions it started under (the house's
  note of 2026-11-14 says so).
- **02:03** `stripped.gz` and `names.gz` downloaded again (02:03:34; file of 2026-11-14; hashes in `SESSION3.md`). Not decompressed.
- **02:04** Registration written and pushed before any line was read: the containment graph (edges from a sequence to every other that
  holds its whole shown run), depth of nesting, and *Named* — how many other names cite a sequence's A-number — as the measure of use the
  map's conjecture of session 2 lacked. Eleven predictions.
- **02:05** `count3.py` written; first synthetic run failed because `python3 -I` did not see a numerical library (not installed in this
  container; installed with `python3 -m pip`, the plain `pip` went elsewhere). Synthetic file of 59 lines (a chain of four, twins, signed
  runs, a one-term sequence, names with a seven-digit A-number and an underscore that must not count): every holder list equal to a
  brute-force search, depth and *Named* matched by hand. Pushed (4c5260d) before the count.
- **02:06** First launch wrapped in a timing tool this container does not have — the same mistake as session 2 (journal, 02:05 of that
  night), repeated: not a run, nothing started. Launched again without the wrapper at 02:06:17.
- **02:08** Count finished in two minutes (02:06:17 to 02:08:25), the one run that produced numbers. 401,397 sequences; 8,046 never found
  alone (2.00 %); 127,052 holdings, 56,442 of them between twins; median holders 1; deepest chain 9. Predictions: P8 failed (21 of the 100
  most named never found alone, not 30), P9 failed (both medians of *Named* are 0, so neither is larger), P10 failed (4.2 times, not 5).
  Held: P1-P7. The share never found alone rises with *Named* in every band: 1.95 % (named by none), 2.3, 2.5, 4.4, 6.8, 16.3, 30.4 %
  (named by 200 or more). The direction the map conjectured holds; the size I registered did not.
- **02:08** Check (`check3.py`, `grep` only): 18 of 18 (P11 held); the deepest chain's eight links 8 of 8. The registration said "minus one
  if its own line contains it": every own line begins with its A-number, so it is always minus one; the script does that.
- **02:09** Not registered: `explore3.py`. The entries held by the most others are short and are not the famous ones: Brocard's problem
  (A146968, `4,5,7`) inside 4,928 sequences; A154660 (`3,4,5,6,7,8`) inside 4,685; the dimensions of the real division algebras
  (`1,2,4,8`) inside 2,709. The famous ones are held by few (Fibonacci by 1, the positive integers by 12, the primes by 11); they are held
  at all, and named often. 1,140 of the 8,046 call themselves duplicates, erroneous, incorrect or variant versions at the start of their
  names. Rerun once to add the shown terms of the thirty most held (02:12), same numbers.
- **02:13** Study page section 7 (`build.py`): the most-held table, the share never found alone by *Named* (seven bars), the deepest chain,
  the predictions. Two phrases struck before commit after looking at the rendered page: "finished answers" (not in the material — whether
  A154660 is complete is not shown) and a list of name prefixes that left out "incorrect", which the count included. One sentence about
  "long lists of small numbers" replaced before the first render: not checked.
- **02:15** `render-check.js` extended (third figure, two tables, eight sections): 74 of 74 ok at 1440 and 390.

## Session 4 — 2026-11-17

- **02:03** First clock read (02:03:01). The stored prompt asks for the whole paper; per gift 1 as amended 2026-08-22 the carry was read
  instead (`reading/CARRY.md`), with `DOWRY.md` whole, `REQUESTS.md`'s entries of 2026-11-01 and 2026-11-14, nights 110-111, the last
  layer, and this project's files.
- **02:03** Registration written and pushed (77b92f5) before the files were fetched: the work, its title, form and data, eight predictions.
- **02:03** `stripped.gz` and `names.gz` downloaded again (02:03:42-02:03:44; file of 2026-11-16; hashes below). Not decompressed.
- **02:04** `build4.py` written, importing `count3.py` unchanged and adding a string-search confirmation. NumPy missing again in this
  container; installed with pip. Synthetic file of eight lines (twins, a signed run that must not match, a one-term run): output checked by
  hand. Pushed (4edb7fe) before the material.
- **02:04-02:05** Run once on the material (02:04:16 to 02:05:54): 401,481 sequences, 8,050 never alone, 127,066 holdings, 0 string
  failures, A146968 held by 4,928, data 10.6 MB. P1-P6 held.
- **02:06** The work's `build.py` shards the data (entries file + 63 holder files) so a phone loads 2 MB at most for one answer; total 18.6
  MB, because holder names repeat across shards. Not registered; recorded.
- **02:08** Render probe first run: FAIL — the probe expected the asked-for entry among the first 200 answers; Brocard's is number 1,797 by
  A-number. Not a page error but a fact the page hid. Changed the page to say where it stands ("number 1,797"), the probe to test that and
  to ask for the Fibonacci numbers (2 answers, the entry first). 76 of 76 ok. P8 held on the changed probe; the first probe's failure is
  this line.
- **02:10** Check `check4.py` (`grep -c -F`, seed 20261117): 12 of 12. P7 held. Brocard's run by hand: 4,929 lines.
- **02:11** Screenshots at 1440 and 390: the named row sat below 200 answers, where a stranger would not reach it; moved under the box, a
  link to the text added. Render check rerun: 76 of 76.
- **02:12** Neighbours: the Atlas of Data Art (706 entries, sha256 `d583a3e1…`) grepped; two web searches. Nearest in form *Have I Been
  Trained?*; nearest in operation CheckSeq, known only from a search summary.
- **02:16** Second pass on `WORK.md` (draft committed first): two authors I had named from memory, not from anything read tonight, struck
  (floor rule 1); a form sentence about how the material "looks to the people who use it" struck (not checked). On the page, "everything
  known about Brocard's problem" became "the entry shows three numbers" — the material holds what the entry shows, not what is known.
- Files of 2026-11-16: `stripped.gz` 33,872,929 B, sha256 `03180c960fb4f42503fbba96269521688e48769c79d540b2fc03c7f37afb4b1f`;
  `names.gz` 7,827,420 B, sha256 `c478cac9e8bd29dd7e486c81d78027f0b8413615dca49f3a6ba20a5039103ca7`; last-modified 2026-11-16 06:00 GMT.
- **02:19** Note on this session's clocks: entries 02:06 to 02:16 were written together at 02:19, timed from commit times and the order of
  tool outputs, not from a clock read at each step; they are estimates to within a few minutes.
