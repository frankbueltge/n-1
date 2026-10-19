"""Exploratory, after the registered run: does the file write one move in more than one way? Counts SAN tokens that differ from
python-chess's canonical SAN for the same move, and recomputes departures on canonical moves (UCI)."""
import io, json, statistics, sys
from collections import Counter
import chess, zstandard
from lib import parse_pgn, san_tokens, departures

stream = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(open(sys.argv[1], "rb")), encoding="utf-8")
uci_games, odd, odd_games, kinds = [], 0, 0, Counter()
for h, mt in parse_pgn(stream):
    toks = san_tokens(mt)
    b, u, here = chess.Board(), [], False
    for s in toks:
        m = b.parse_san(s)
        c = b.san(m)
        if c != s:
            odd += 1; here = True
            kinds["piece letter + full square" if len(s.rstrip("+#")) == 5 and s[0] in "NBRQK" else "other"] += 1
            if len(kinds) < 3 and sum(kinds.values()) < 4: print("written", s, "canonical", c)
        u.append(m.uci()); b.push(m)
    odd_games += here
    uci_games.append(u)
dep = departures(uci_games)
dp = [d[0] for d in dep if d[0] is not None]
never = sum(1 for d in dep if d[0] is None)
out = {"tokens_not_canonical": odd, "games_with_such_a_token": odd_games, "kinds": dict(kinds),
       "canonical_never_depart": never, "canonical_median_departure_ply": statistics.median(dp),
       "canonical_mean_departure_ply": round(statistics.mean(dp), 3), "canonical_longest_stem": max(d[1] for d in dep if d[0] is not None)}
json.dump(out, open("explore1.json", "w"), indent=1); print(out)
