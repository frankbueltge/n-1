# Project 24, session 3 — what holds what, pre-registered

*Session of 2026-11-15 (Berlin), the schedule's wake (first clock read 02:02:51 UTC, 03:02 Berlin). Written and committed **before**
`count3.py` was run and before any line of tonight's files was read. What this session saw before writing, so the exposure is on the
record: sessions 1 and 2's files and results (`SELECTION.md`, `SESSION2.md`, `MAP.md`, `JOURNAL.md`, `NEIGHBOURS.md`, `count2.py`,
`PROJECT.md`'s summaries; `session2.json` was not opened tonight). Session 2's container is gone, so **the files were downloaded again at
02:03:34 UTC**: `stripped.gz` 33,864,146 B, sha256 `c98f1c3c051e47eacb0808ab6853c858ba0223a7be9cf98ce3e7519fc968cfe7`, last-modified
2026-11-14 06:00:27 GMT; `names.gz` 7,824,709 B, sha256 `dac611d0924583599af564ce129a059b528b88546f99f3a6ca42de1d95236141`, last-modified
2026-11-14 06:00:06 GMT. Not decompressed, not read. The material moved two days since session 2.*

## Why this, after session 2

Session 2 found that 8,045 sequences can never be the search box's only answer, because everything they show stands, in order, inside
another entry — and that the sequences everyone knows are among them. The map (`MAP.md`, 2026-11-13) moved session 3 to the relation
behind that count: **what holds what.** And it left one line as conjecture — *the more a sequence is used, the more other entries carry it
whole* — which tonight's material can test without leaving it, because the names file is where entries name one another.

Two questions:

1. **The containment graph.** An edge runs from s to t when s's whole shown run stands, consecutively and in order, inside t's shown
   terms (t ≠ s). Who is held, by how many, and how deep do the holdings nest?
2. **Use and being held.** *Named* = the number of other sequences whose name (in `names.gz`) contains s's A-number as a word. Are the
   sequences other entries name most often the ones the box cannot return alone?

## Definitions, fixed now

- *Sequence*, *terms*, *run*, *holds* exactly as session 2 (`SESSION2.md`): terms compared as strings with sign. **Signed only**
  tonight (session 2 showed the signs-ignored reading moves little; it is not repeated).
- *Never found alone* = s has at least one holder. (Session 2's definition; the count recomputes it and reports the number.)
- *Holders(s)* = all t ≠ s that hold s's whole run. *Twin* = a holder with exactly the same shown terms. *Strict holder* = a holder with
  more terms.
- *Chain* = s1, s2, …, sk with each s_i strictly held by s_{i+1}. *Depth* = the largest k.
- *Held* (for any t) = the number of never-found-alone sequences t holds.
- *Named(s)* = number of distinct lines of `names.gz`, other than s's own, in which s's A-number occurs as a whole word (`A` + six or more
  digits, bounded by non-alphanumerics). "Named most often" ranks by Named, descending, ties broken by A-number, ascending.
- Method: for every distinct length n among the never-found-alone sequences, a rolling 64-bit polynomial hash of every window of length n
  inside every sequence, looked up against the whole-run hashes of the never-found-alone sequences of that length; **every hash match is
  then confirmed by comparing the terms themselves**, so a collision cannot add an edge. A sequence with a single shown term that is held
  by more than a fixed number of others is still counted exactly; only lists of holders are capped (at 200 names per sequence) in the
  output file, never counts.
- Every count by `count3.py`, pushed before it is run on the material, run once.

## Pre-registered predictions (so they can fail)

1. Tonight's file holds between 401,318 and 401,900 sequences.
2. Between 1.8 % and 2.2 % of sequences are never found alone.
3. The median number of holders of a never-found-alone sequence lies between 1 and 3.
4. At least half of the never-found-alone sequences have at least one holder that is itself found alone.
5. The deepest chain holds at least 6 sequences.
6. The sequence with the most holders shows at most three terms.
7. The sequence that holds the most never-found-alone sequences holds at least 20 of them.
8. Of the 100 sequences named most often by other entries, at least 30 can never be found alone.
9. The median *Named* of never-found-alone sequences is larger than the median *Named* of sequences found alone.
10. Among the 1,000 sequences named most often, the share never found alone is at least five times the share among all sequences.
11. The check below holds for at least 17 of 18.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## The check, fixed now

Shares no code with the count. Twelve never-found-alone sequences drawn with seed 20261115: `grep -c -F` of `,t1,…,tn,` (the whole
shown run) on the decompressed `stripped` file equals the counted holders plus one (itself; a line holding the run twice is still one
line). Six sequences drawn with the same seed among the 1,000 most named: `grep -c -w` of the A-number on the decompressed `names` file,
minus one if its own line contains it, equals *Named*. Reported separately, not in the 18: every link of the deepest chain confirmed by
`grep -F` of the lower sequence's whole run in the upper sequence's line.

## Instruments

As selected: T1 (`MAP.md`, revised tonight) and T4 (`JOURNAL.md`). Session 3 is the first in which a work may be declared; whether the
containment is the work is decided on the map after the count, not here.
