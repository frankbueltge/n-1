"""Exploratory, after the registered run and the reading rule: the identical games (whole move lists played twice or more) and the
position departure's own distribution. Writes explore1b.json. No account is named; pairs are compared only as same or different."""
import io, json, statistics, sys
from collections import Counter, defaultdict
import chess, zstandard
from lib import parse_pgn, san_tokens, position_departures

stream = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(open(sys.argv[1], "rb")), encoding="utf-8")
groups, keys = defaultdict(list), []
for h, mt in parse_pgn(stream):
    toks = san_tokens(mt)
    groups[tuple(toks)].append((frozenset((h.get("White"), h.get("Black"))), h.get("Termination"), h.get("Result"), h.get("Opening")))
    b, ks = chess.Board(), []
    for s in toks:
        b.push_san(s); ks.append(hash(b._transposition_key()))
    keys.append(ks)
pd = position_departures(keys)
ident = []
for seq, gs in groups.items():
    if len(gs) > 1:
        ident.append({"plies": len(seq), "games": len(gs), "distinct_pairs": len(set(g[0] for g in gs)),
                      "results": dict(Counter(g[2] for g in gs)), "terminations": dict(Counter(g[1] for g in gs)),
                      "opening_tag": gs[0][3], "moves": list(seq)})
ident.sort(key=lambda x: (-x["games"], -x["plies"]))
pdv = [p for p in pd if p is not None]
out = {"identical_groups": len(ident), "games_in_identical_groups": sum(x["games"] for x in ident),
       "identical_groups_all_distinct_pairs": sum(1 for x in ident if x["distinct_pairs"] == x["games"]),
       "identical_top": ident[:15],
       "position_never_depart": len(pd) - len(pdv), "position_median_departure_ply": statistics.median(pdv),
       "position_mean_departure_ply": round(statistics.mean(pdv), 3)}
json.dump(out, open("explore1b.json", "w"), indent=1)
print({k: v for k, v in out.items() if k != "identical_top"})
for x in ident[:15]: print(x["games"], x["plies"], x["distinct_pairs"], x["results"], x["terminations"], x["opening_tag"], " ".join(x["moves"]))
