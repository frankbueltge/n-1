# Project 13 — neighbours (searched before the material was read)

*2026-10-19, session 1. The search begins in the Atlas of Data Art (`https://frankbueltge.de/atlas/werke.json`, sha256 `4765ce73…`,
523 entries): grepped for chess, schach, game(s), spiel, opening, move(s). No entry works with chess; the hits are video-game works
(e.g. Lawrence Lek, *Nepenthe*; Alice Bucknell, *The Alluvials*), none of them about play recorded as moves. Then two web searches
(standard mode). Every item below is **from a search result, not seen**, unless marked otherwise.*

| Neighbour | What it does (from the source's own description) | Distance to this project |
|---|---|---|
| Santiago Ortiz, famous chess matches as 3-D wireframes (FlowingData, 2026-03-02, `https://flowingdata.com/2026/03/02/famous-chess-matches-visualized-as-3-d-wireframes/`) | Piece positions lifted one step per move, for single famous games | One game at a time, a canon of famous ones; here, a month of unfamous games against each other. |
| Lu, Wang, Lin et al., *Chess Evolution Visualization* (IEEE TVCG 2014, `https://people.cs.nycu.edu.tw/~yushuen/data/ChessVis14.pdf`) | A tree of positions from one game, transpositions merged | Analysis tool, one game; not a work. |
| Georg Mühleck, Michael Schlosser, *Fine Art, Fine Chess, Fine Data* (ISEA 1995, `https://isea-archives.siggraph.org/art-events/georg-muhleck-michael-schlosser-fine-art-fine-chess-fine-data`) | Cellular automata on chessmen with chess compositions | Composed problems, not played games. |
| Jeffrey Shaw, *Another Kind of Chess Game* (ISEA archive, `https://isea-archives.siggraph.org/art-events/another-kind-of-chess-game-by-jeffrey-shaw`) | Session 2: the page answers 404 (2026-10-19, 23:19 UTC). A search summary describes it: ISEA 2016, a 3-D rendering of Giuseppe Castiglione's painted chessboard projected on a low table, its sixteen segments flipped between painted and chessboard faces by sixteen buttons. **Not seen.** | A board as a painting to be rearranged; no game played, no population of games. Far. |
| Opening trees (chess.com forum, ChessRoots on the Lichess database; `https://alternativeto.net/software/chessroots/about`) | Trees of all openings, for study | Tools for players; they draw the shared stem and stop where this project begins. |
| ChessFlow (commercial, `https://peerpush.com/p/chessflow`) | One game turned into brushstrokes | A product; one game. |

**Daylight so far (conjecture until session 2's refreshed search):** no neighbour found shows where each game of a whole population
leaves all the others. The opening trees are the nearest material neighbour and the opposite cut: they keep what is shared and drop
what is not.

**Session 2 (2026-10-19/20).** One further web search (standard mode) for an artwork or installation drawing a game database as a tree of
departures: none returned; the results were the session 1 neighbours again (ChessFlow, the chess.com opening-tree thread), Lichess's
Opening Explorer (a player's tool over the database, `https://lichess.org/@/lichess/blog/opening-explorer/Vs0xMTAA`, from a search result,
not seen) and a World Chess map of openings by origin (`https://worldchess.com/new-projects`, not seen). The Opening Explorer is the nearest
material neighbour for a piece in which a visitor plays moves and is told how many games played them: it counts the games at each
position for study. Distance, conjecture until read: it answers a player choosing the next move; it does not mark the move at which the
visitor's game leaves everyone, and it draws on the whole database, not on one month as a closed population.

**Session 3 (2026-10-20).** No new search. The prototype brings the session 2 entry for Lichess's Opening Explorer from "nearest material
neighbour" to near neighbour in form: both let a person play moves and see how many games of a database played them. Distance, still from
a search result and not seen: the explorer counts positions (transpositions merged) over the whole database for a player choosing a next
move; the prototype counts move sequences in one closed month and marks the move at which fewer than two of its games remain. Daylight
in form only; no advantage follows from it (`JOURNAL.md`, session 3).

**Session 4 (2026-10-20). The Opening Explorer, read.** Not the explorer itself (it answers 401 without a token, and a token needs an
account with a third party, which is the founder's act) but its documentation: Lichess's API specification at `lichess-org/api`, master
`fedb6b86`, `doc/specs/tags/openingexplorer/lichess.yaml` and `doc/specs/schemas/OpeningExplorerLichess.yaml`,
`OpeningExplorerLichessGame.yaml` (read 2026-10-20, 09:42 UTC). What it documents: the endpoint `https://explorer.lichess.org/lichess`,
"Aggregated rated games from all Lichess players"; a root position (`fen`) and moves replayed from it (`play`, UCI); filters by speed, by
rating group, and by month (`since`, `until`, "Include only games from this month or later" / "or earlier"); a response of white wins,
draws and black wins for the position and for each next move, an optional `history` by month, and **game references naming both
players**: `topGames`, `recentGames`, and on each move a `game` field (in the schema, a single game's reference; that it is filled when
one game played the move is training knowledge, not read). Against session 3's daylight:

| Session 3's difference | After reading |
|---|---|
| a closed month | **withdrawn**: `since=2013-01&until=2013-01` is the same cut |
| sequences, not positions | stands: the explorer is keyed by position, so transpositions merge |
| the moment the count falls below two | stands, as a threshold: the explorer gives counts and marks no horizon |
| (not listed in session 3) | the piece never shows a game fewer than two played and names no one; the explorer names the players of the games it shows |

**Daylight, restated:** a different cut on the same counts, and a stricter rights rule. Neither is a capacity a person lacks.
