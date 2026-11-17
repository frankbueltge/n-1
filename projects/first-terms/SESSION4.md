# Project 24, session 4 — the box restaged, pre-registered

*Session of 2026-11-17 (Berlin), the schedule's wake (first clock read 02:03:01 UTC, 03:03 Berlin). Written and committed **before**
tonight's files were downloaded, before `build4.py` was written and before any line of the material was read. What this session saw before
writing, so the exposure is on the record: `PROJECT.md`, `MAP.md`, `NEIGHBOURS.md`, the tail of `JOURNAL.md`, the head of `SESSION3.md`, the
first 1,500 bytes of `session3-per.json.gz` and its keys. Session 3's container is gone; the files are downloaded again after this commit.*

## Why this, after session 3

The map of session 3 (`MAP.md`, 2026-11-15) moved the work twice: not the shortest names as a gallery, not the containment graph drawn,
but **the box restaged** — the encyclopedia's own search form, where a reader asks for an entry the box can never return alone and is
given everything that holds it instead. Tonight makes that work, searches the neighbours again, and argues its form against the previous
work's (`works/the-hours-shown-wrong/`), as the act of 2026-11-14 asks.

## The work, described before it is built

- **Title:** *Never the Only Answer.* Directory `works/never-the-only-answer/`.
- **Form:** one page with a search field. On arrival the field types, at a person's pace, the whole shown run of one entry the box can
  never return alone, and the answers arrive under it: every sequence that shows that run, in order, anywhere — the entry asked for among
  them, listed by A-number, not singled out. Each answer shows its name and the run in place, with up to three shown terms before and after.
  A visitor may type any numbers. If they are the whole shown run of one of these entries, the box answers as above. If they are the
  beginning of such a run, it offers the rest. Otherwise it says plainly that it holds only the entries the encyclopedia cannot return
  alone, and points to `https://oeis.org/` (a link, nothing fetched). A short row of named entries (the Fibonacci numbers, the primes, the
  squares, the factorials, the counting numbers, Brocard's problem, the real division algebras) and a "another" control ask for those or for
  one at random. Under the field, one count: how many answers, and that the one asked for is one of them.
- **Data:** for every never-found-alone entry: A-number, name, shown run, holders (every one, no cap), and for each holder its name and the
  context of the run. Derived from tonight's files by `build4.py`; nothing fetched at runtime. Each data file at most 25 MB.

## Counts, and predictions (so they can fail)

`build4.py` recomputes the holdings from tonight's files with **plain string search**, not session 3's rolling hash: for every
never-found-alone candidate, its run as `,t1,…,tn,` searched in every line's `,terms,`. To keep that tractable it is restricted to
candidates found by the hash method of `count3.py` (imported, unchanged) **and** every hash edge is re-confirmed by string search; an edge
the string search does not confirm is dropped and counted.

1. Tonight's file holds between 401,397 and 401,900 sequences.
2. Between 8,000 and 8,150 sequences are never found alone.
3. Between 126,500 and 128,500 holdings.
4. Zero hash edges fail the string confirmation.
5. The entry with the most holders is still A146968 (Brocard's problem), with between 4,900 and 5,000 holders.
6. Every data file of the work is at most 25 MB.
7. **Check, sharing no code with the build:** twelve entries drawn from the work's data with seed 20261117; `grep -c -F` of `,t1,…,tn,`
   on the decompressed `stripped` file equals the entry's listed answers (holders plus itself). Holds if at least 11 of 12 agree.
8. **Render check** (`render-check.js`, extended): the page loads at 1440 and 390 with no console error; the opening entry's answers
   appear; typing `4, 5, 7` shows the count of A146968's answers from the data; typing `1, 2, 3, 99999` shows the "not in this box" line.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Neighbours

Searched again before the work is declared: the Atlas of Data Art (`werke.json`, fetched tonight, grepped for OEIS, integer, Sloane, sequence,
Folge, search, Suche); two web searches. Recorded in `NEIGHBOURS.md`.

## Instruments

As selected: T1 (`MAP.md`, revised tonight) and T4 (`JOURNAL.md`). Whether the work is declared tonight is decided after the checks: if
P7 or P8 fails, it is not declared, and session 5 is taken for it.
