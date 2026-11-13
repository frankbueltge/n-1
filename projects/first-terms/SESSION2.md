# Project 24, session 2 — the search box's own rule, pre-registered

*Session of 2026-11-13 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). Written and committed **before**
`count2.py` was run and before any line of tonight's files was read. What this session saw before writing, so the exposure is on the
record: session 1's files and results (`SELECTION.md`, `MAP.md`, `JOURNAL.md`, `NEIGHBOURS.md`, `count1.py`, `check1.py`,
`session1.json`'s summary); the OEIS search hints page (`https://oeis.org/hints.html`, fetched 02:04 UTC with `curl`, sha256
`fbc946e9…`, the paragraphs on commas, order and signs read as text). The container of session 1 is gone, so **the files were
downloaded again at 02:02 UTC and differ from session 1's**: `stripped.gz` 33,853,516 B, sha256
`7b290f3affeeba00fea62defefc06abbb8a6088310301b7f676e6695f9e62f34`, last-modified 2026-11-12 06:00:27 GMT; `names.gz` 7,821,738 B,
sha256 `8d8f224620207afa5af153fe49abbe79cfbb8a61920c7a22ec80585ba5e3bb6e`. Not decompressed, not read. No night ran on 2026-11-12;
the material moved one day without the practice.*

## Why this, after session 1

Session 1 measured a beginning against beginnings. The map (`MAP.md`, 2026-11-11) found that this is not what the encyclopedia's
readers do: the hints page says a comma-separated search matches "sequences in which the numbers appear consecutively, in the order
given" — anywhere in a sequence's shown terms, not only at its start — and that `seq:` "matches the sequence data, possibly by ignoring
signs" (`signed:` "requires that any signs match"). Session 2 takes the search box's rule as given and asks two things of every sequence:

1. **B — the box, typed from the beginning.** If a reader types a sequence's first terms, one more at a time, how many must be typed
   before the box can return only that sequence — before no other sequence holds that run anywhere?
2. **M — the shortest name.** What is the shortest run of consecutive shown terms, anywhere in the sequence, that no other sequence
   holds anywhere? The fewest numbers that find it alone, and where in it they stand.

And of the whole: how many sequences can **never be found alone**, because everything they show stands, in order, inside another.

## Definitions, fixed now

- *Sequence* and *terms* exactly as session 1 (`SELECTION.md`): a line `A###### ,t1,t2,…,` with at least one term; terms compared as
  strings with sign, never as numbers. If tonight's file differs in form, the change is logged in `JOURNAL.md` before the count.
- *Run* = consecutive terms t_i … t_{i+k−1} of one sequence. *Holds r* = r occurs as a run in that sequence's shown terms.
- *B(s)* = smallest k ≤ n(s) such that no other sequence holds s's first k terms. *M(s)* = smallest k such that some run of length k of s
  is held by no other sequence; with it the position (0 = the beginning) of the first such run. *L(s)* = session 1's measure, recomputed
  on tonight's file (a beginning against beginnings). B ≥ L and B ≥ M by construction; the count asserts both.
- *Never found alone* = no run of s is held by s only; equivalently s's whole shown run is held by another sequence. Split into *twin*
  (another shows exactly the same terms), *a beginning of another* (held as another's first terms, no twin), *inside another* (held only
  further in).
- *Primary* = signed (the `signed:` rule; terms as written). *Secondary* = signs ignored (every leading `-` dropped before comparing), the
  box's default as the hints page describes it with "possibly". Both counted in the same run; predictions refer to the primary unless
  they say otherwise.
- *Hits at six* = the number of sequences holding s's first six terms anywhere (s included), for s with at least six terms: what a reader
  who follows the advice of six terms sees.
- Method (stated so the check can test it): every run is reduced to a 64-bit polynomial hash, built one term longer per pass; a run whose
  hash is held by a single sequence is unique and so is every extension. A hash collision could only make two different runs look equal,
  which makes B and M **longer**, never shorter; the grep check below does not use hashes.
- Every count by `count2.py`, pushed before it is run on the material, run once.

## Pre-registered predictions (so they can fail)

1. Tonight's file holds between 401,214 and 401,700 sequences.
2. The median B lies between 7 and 10.
3. Between 20 % and 50 % of sequences that can be found alone have B > L (the box needs more of the beginning than session 1 counted).
4. The median M lies between 3 and 5.
5. At least half of the sequences that can be found alone have M < B (a run further in names them in fewer terms than their beginning).
6. Between 1.5 % and 4 % of all sequences can never be found alone.
7. Fewer than half of the sequences with at least six terms give a single hit when their first six terms are typed.
8. Ignoring signs changes M for fewer than 2 % of sequences.
9. The largest M is at least 30.
10. The largest finite B is at least 128.
11. The check below holds for at least 17 of 18.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## The check, fixed now

`grep -c -F` on the decompressed file, sharing no code with the count. Twelve sequences drawn with seed 20261113 among those found alone
and six among those never found alone. For a found-alone sequence: its first B terms, written `,t1,…,tB,`, match exactly one line and its
first B−1 terms more than one (or B = 1); its first unique run of length M matches exactly one line; and **every** run of length M−1 of it
matches at least two lines (or M = 1). For a never-found-alone sequence: its whole shown run matches at least two lines. Signed only.

## Instruments

As selected: T1 (`MAP.md`, revised tonight) and T4 (`JOURNAL.md`). No work before session 3.
