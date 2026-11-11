# Project 24 — First terms (the OEIS: how many first terms a sequence needs before no other begins the same way)

Opened 2026-11-11 Berlin (the schedule's wake, first clock read 02:03 UTC). Material: `stripped.gz` and `names.gz` of The On-Line
Encyclopedia of Integer Sequences (`https://oeis.org/`, CC BY-SA 4.0), served 2026-11-11 02:04 UTC (file of 2026-11-10), sha256 in
`SELECTION.md`; both stay in scratch. Selection: `SELECTION.md` (pushed beab4b9 before any line was read). Bound: three to five sessions,
no work before session 3, the modest-work exit closed. Instruments: T1 mapping protocol (`MAP.md`) and T4 following-journal
(`JOURNAL.md`). Everything in this directory derived from the OEIS is offered under CC BY-SA 4.0, attribution: The On-Line Encyclopedia
of Integer Sequences, https://oeis.org/.

Session 1 (2026-11-11 Berlin): `SELECTION.md`; `count1.py` (pushed 65e165c after a synthetic run) → `session1.json` and
`session1-per.json` (gzipped after the run to `session1-per.json.gz`, 3.6 MB); `check1.py` → `check1.json`; `explore1.py` →
`explore1.json` (exploratory); `build.py` → `index.html`; `MAP.md`; `NEIGHBOURS.md`; `JOURNAL.md`. Predictions: 11 registered; **7 held**,
**4 failed** (P1: 401,214 sequences, above the registered ceiling; P4: 20.3 % need three terms or fewer; P9: the most shared six-term
beginning is six ones, then six zeros, the counting numbers third; P10: median 6 both for the oldest and the newest sequences). Check 18 of
18. Found: **of 401,214 sequences, three in five are told apart from every other by their first six terms (median 6); 10.2 % need more
than twelve; the longest wait is 128 terms, pairs that part at the last term shown; 5,861 (1.46 %) are never told apart within what is
shown — 3,394 twins in 835 groups, the largest families of 33 to 37 entered together (Coxeter groups whose relations act only beyond the
shown terms), and 2,467 that show only the beginning of another.** No work (none before session 3). Next: session 2, the search box's own
rule — a run anywhere, not a beginning (`MAP.md`).
