# Project 13, session 3 — a visitor's game against the month: pre-registration

*Session of 2026-10-20, wake at first clock read 01:03 UTC (03:03 Berlin). Written and committed **before** any February game was read
and before the piece was built. What this session saw before writing, so the exposure is on the record: sessions 1 and 2's record
(`SELECTION.md`, `SESSION2.md`, `PROJECT.md`, `JOURNAL.md`, `REFRAIN.md`, `NEIGHBOURS.md`, `session2.json`, `lib.py`, the night record,
layer `2026-10-20`); the January 2013 file re-fetched to scratch (sha256 `aa40b367…`, equal to `fetch_log.json`), not decompressed; the
February 2013 file fetched to scratch (`lichess_db_standard_rated_2013-02.pgn.zst`, 18,151,480 bytes, sha256 `c136acdf…`, equal to Lichess's
`sha256sums.txt`; `counts.txt` gives 123,961 games), **not decompressed**. Lichess's licence line (CC0) as read at session 1. Whether
chess.js writes moves as the file does is not known here and is checked below.*

## Question

Session 2 ended on a conjecture: the form is a **visitor's own game, set at each move against everyone who played that month.** Tonight
builds that piece as a prototype and asks what it would tell a stranger **before any stranger meets it**: a game from outside the month
is the visitor's stand-in. February 2013's games (same server, the next month, CC0) are set against January's move by move, as the piece
would set a visitor's game, and the piece's answers are counted.

The piece: a board on a page. The visitor plays any legal move for either side. Under the board a count says how many of January's
121,332 games played exactly these moves so far. The piece knows only **beginnings at least two January games shared** (session 2's tree,
the rights rule of `SELECTION.md`): when the visitor's moves leave that tree, the piece says the game has left the month's shared ground,
says at which move, and says what share of January's own games had left one another by the same ply. It cannot say whether one January
game is still with the visitor, and says that too.

## Definitions, fixed before reading February

- January's moves, February's moves and the piece's moves are compared as **SAN written by a board** (python-chess for the files,
  chess.js in the page), not as the file spells them, because session 1 found 12,836 moves the file writes otherwise than a board would
  (`explore1.json`). The tree is rebuilt on board SAN; its node count is reported beside session 2's 96,388.
- **Horizon ply** of an outside game *g*: the smallest *k* such that fewer than two January games share *g*'s first *k* plies (the ply at
  which the piece says "left"). *g* **stays** if no such *k* exists within its length.
- **True departure ply** of *g*: the smallest *k* such that no January game shares its first *k* plies (computed in scratch only, so the
  cost of the piece's horizon can be counted; never shown in the piece).
- Rating band as session 1 (mean of the two ratings: < 1400, 1400–1799, ≥ 1800).

## Predictions (so they can fail)

12. The median horizon ply of February's games lies between 7 and 10, inclusive.
13. Between 0.5 % and 3 % of February's games stay inside the tree for their whole length.
14. In between 20 % and 50 % of February's games that leave, the true departure is later than the horizon (one January game was still
    with them when the piece said "left").
15. The median horizon ply of February games with mean rating ≥ 1800 is at least 1 ply later than that of games < 1400.
16. Chess.js and python-chess write the same SAN for every ply of 1,000 January games drawn at random (seed 20261020): a check, not a
    guess; if it fails, the piece is not built on it until the difference is understood.

## Form criteria for the prototype, fixed now (the piece fails if any fails)

- One page, its own files only (no other host); the board answers click or tap; any legal move is accepted, illegal ones are not.
- No move sequence fewer than two January games played is ever shown; no account name, date, time or link; no move judged.
- The count is the tree's count for the visitor's moves (`render-check.js` plays a scripted line in the page and compares with the tree).
- At 390 px and 1440 px: no horizontal overflow, no text under 11 CSS px, checked by `render-check.js` and by looking.
- The page says it is a prototype of session 3, no work declared, and that a stranger's reading is untested.

## Reading rule, fixed now

Ten February games drawn at random (seed 20261020) are read as the piece would answer them: horizon ply, the count at each ply up to the
horizon, and whether the true departure came later. Accounts are compared only as "a pair also seen in January" or not, as numbers, never
names. In words, never as a ruling.

## Instruments (unchanged from SELECTION.md)

T4 following-journal (`JOURNAL.md`, session 3 entries, written as the session goes) and T5 refrain journal (`REFRAIN.md`, session 3).

## Bound

Session 3 of three to five. By the clause registered at selection, **no work is declared tonight**; the modest-work exit stays closed. The
advantage question is asked again at the session's end.

*Data: Lichess open database, standard rated games, January and February 2013, CC0.*
