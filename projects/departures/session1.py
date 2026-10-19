"""Session 1, the registered run (SELECTION.md). Reads the PGN from scratch; writes session1.json and sample.json."""
import io, json, random, statistics, sys, time
from collections import Counter
import chess, zstandard
from lib import parse_pgn, san_tokens, departures, position_departures

src = sys.argv[1]
t0 = time.time()
stream = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(open(src, "rb")), encoding="utf-8")
games, meta, excluded = [], [], Counter()
for h, mt in parse_pgn(stream):
    if "FEN" in h or h.get("SetUp") == "1":
        excluded["non-standard start"] += 1; continue
    toks = san_tokens(mt)
    if not toks:
        excluded["no moves"] += 1; continue
    games.append(toks)
    try:
        r = (int(h["WhiteElo"]) + int(h["BlackElo"])) / 2
    except (KeyError, ValueError):
        r = None
    meta.append({"pair": frozenset((h.get("White"), h.get("Black"))), "rating": r,
                 "termination": h.get("Termination"), "result": h.get("Result"), "opening": h.get("Opening")})
print("parsed", len(games), dict(excluded), round(time.time() - t0), "s", flush=True)

dep = departures(games)
print("departures done", round(time.time() - t0), "s", flush=True)

# positions after each ply, keyed by a 64-bit hash of python-chess's transposition key
keys, bad = [], 0
for i, g in enumerate(games):
    b, ks = chess.Board(), []
    try:
        for s in g:
            b.push_san(s)
            ks.append(hash(b._transposition_key()))
    except ValueError:
        bad += 1
    keys.append(ks)
    if i % 20000 == 0:
        print("positions", i, round(time.time() - t0), "s", flush=True)
pdep = position_departures(keys)
print("positions done", bad, "unparsed", round(time.time() - t0), "s", flush=True)

n = len(games)
departing = [i for i in range(n) if dep[i][0] is not None]
never = n - len(departing)
dp = [dep[i][0] for i in departing]
med = statistics.median(dp)
stems = sorted(departing, key=lambda i: -dep[i][1])
longest = dep[stems[0]][1]
later = sum(1 for i in departing if pdep[i] is None or pdep[i] > dep[i][0])
bands = {"<1400": [], "1400-1799": [], ">=1800": [], "unrated": []}
for i in departing:
    r = meta[i]["rating"]
    k = "unrated" if r is None else "<1400" if r < 1400 else "1400-1799" if r < 1800 else ">=1800"
    bands[k].append(dep[i][0])
band_med = {k: (statistics.median(v) if v else None, len(v)) for k, v in bands.items()}
# identical full move lists
full = Counter(tuple(g) for g in games)
ident = sorted(((len(k), c) for k, c in full.items() if c > 1), reverse=True)
hist = Counter(dp)
maxlen = max(len(g) for g in games)
# games still in shared ground after ply p (among games at least p plies long)
together = []
for p in range(1, 61):
    alive = [i for i in range(n) if len(games[i]) >= p]
    shared = sum(1 for i in alive if dep[i][0] is None or dep[i][0] > p)
    together.append({"ply": p, "games_at_least_this_long": len(alive), "still_shared": shared})

pred = {
    "P1 median departure ply in [9,14]": {"value": med, "held": 9 <= med <= 14},
    "P2 at least 3% never depart": {"value": round(100 * never / n, 3), "held": never / n >= 0.03},
    "P3 longest stem >= 40 plies": {"value": longest, "held": longest >= 40},
    "P4 position departure later in >= 20%": {"value": round(100 * later / len(departing), 3), "held": later / len(departing) >= 0.20},
    "P5 >=1800 median at least 2 plies later than <1400": {"value": [band_med[">=1800"][0], band_med["<1400"][0]],
        "held": band_med[">=1800"][0] is not None and band_med["<1400"][0] is not None and band_med[">=1800"][0] - band_med["<1400"][0] >= 2},
    "P6 identical pair of >= 30 plies": {"value": ident[0][0] if ident else 0, "held": bool(ident) and ident[0][0] >= 30},
}
out = {"games": n, "excluded": dict(excluded), "unparsed_for_positions": bad, "never_depart": never,
       "departing": len(departing), "median_departure_ply": med, "mean_departure_ply": round(statistics.mean(dp), 3),
       "departure_hist": {str(k): hist[k] for k in sorted(hist)}, "longest_stem": longest,
       "position_later_count": later, "band_median_departure": band_med,
       "identical_lists_top": ident[:20], "identical_groups": len(ident), "max_game_plies": maxlen,
       "together": together, "predictions": pred, "seconds": round(time.time() - t0)}
json.dump(out, open("session1.json", "w"), indent=1)

# the reading rule: 10 longest stems, 20 random departing games (seed 20261019)
order = sorted(range(n), key=lambda i: games[i])
pos = {g: j for j, g in enumerate(order)}
def partner(i):
    j = pos[i]; best, who = -1, None
    for k in (j - 1, j + 1):
        if 0 <= k < n:
            from lib import lcp
            l = lcp(games[i], games[order[k]])
            if l > best: best, who = l, order[k]
    return who
random.seed(20261019)
pick = [("longest", i) for i in stems[:10]] + [("random", i) for i in random.sample(departing, 20)]
sample = []
for why, i in pick:
    q = partner(i)
    sample.append({"why": why, "stem_plies": dep[i][1], "stem": games[i][:dep[i][1]], "departure_ply": dep[i][0],
                   "position_departure": pdep[i], "game_plies": len(games[i]), "tail_plies": len(games[i]) - dep[i][1],
                   "same_pair_as_partner": meta[i]["pair"] == meta[q]["pair"], "partner_plies": len(games[q]),
                   "rating_band": None if meta[i]["rating"] is None else int(meta[i]["rating"] // 200 * 200),
                   "termination": meta[i]["termination"], "opening_tag": meta[i]["opening"]})
json.dump(sample, open("sample.json", "w"), indent=1)
print(json.dumps(pred, indent=1)); print("done", round(time.time() - t0), "s")
