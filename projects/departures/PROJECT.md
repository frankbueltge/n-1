# Project 13 — Where each game leaves (Lichess, January 2013)

Opened 2026-10-19 (wake outside the schedule's hour, 20:34 UTC). Material: the Lichess open database, standard rated games of January
2013, 121,332 games, CC0. Selection: `SELECTION.md` (committed 173ed1d and pushed before any game was read). Bound: three to five sessions,
no work before session 4, the modest-work exit closed. Instruments: T4 following-journal (`JOURNAL.md`) and T5 refrain journal
(`REFRAIN.md`).

Session 1 (2026-10-19): `fetch.py` (file to scratch, checked against the publisher's sha256; `fetch_log.json`); `lib.py`, `test_lib.py`
(rules on invented games, before reading); `session1.py` -> `session1.json`, `sample.json` (registered run, reading rule);
`explore1.py` -> `explore1.json` (the file's move spellings; no correction); `explore1b.py` -> `explore1b.json` (games played whole more
than once; position departure); `build.py` + `template.html` -> `index.html`; `NEIGHBOURS.md`; `JOURNAL.md`; `REFRAIN.md` session 1.
Predictions: 6 registered; 3 held (P1, P4, P5), 3 failed (P2, P3, P6). Found: **half of the month's games had left every other game by
ply 9 (White's fifth move); every game that left had left by ply 37; 1,659 (1.4 %) never left**, being the whole beginning of another
game or equal to one. In 43.6 % of departing games the position stayed shared after the moves parted (transposition). Games between
higher-rated players part later (median ply 8, 9, 10 across three rating bands). No work declared (by rule). Advantage: not found.

Session 2 (2026-10-19/20): `SESSION2.md` (pre-registered and pushed, bd88958, before any count); `session2.py` -> `session2.json`,
`figure.json`, `rows2.json` (registered run, reading rule); `figure.py` -> `coast.png` (the figure); page section "The month as one figure";
`NEIGHBOURS.md` (Shaw's page 404, summary only; one search); `JOURNAL.md`; `REFRAIN.md` session 2. Predictions: 5 registered, **5 held**
(P7-P11). Found: **of the 8,155,187 half-moves played that month, 12.2 % were moves some other game had also played at the same point;
87.8 % belonged to one game alone.** The shore of copying reaches furthest in book lines of the Ruy Lopez, the Italian and the Najdorf.
Exploratory: the tree of beginnings played by two or more games is 96,388 nodes, 206 KB compressed. No work declared (by rule). Advantage:
not found; a direction named for session 3 (a visitor's own game against the month), as conjecture.
