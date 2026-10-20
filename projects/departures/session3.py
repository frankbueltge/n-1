"""Session 3, the registered run (SESSION3.md): a visitor's game against the month.
Reads January and February 2013 from scratch; writes tree.json (the piece's data), session3.json, read3.json,
and, to scratch only, a sample of January move lists for the chess.js check (P16)."""
import bisect, io, json, random, statistics, sys, time
from collections import Counter
from multiprocessing import Pool
import chess, zstandard
from lib import parse_pgn, san_tokens, departures, lcp

jan_src, feb_src, scratch = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = time.time()


def read(src):
    stream = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(open(src, "rb")), encoding="utf-8")
    out = []
    for h, mt in parse_pgn(stream):
        if "FEN" in h or h.get("SetUp") == "1":
            continue
        toks = san_tokens(mt)
        if toks:
            out.append((toks, h.get("WhiteElo"), h.get("BlackElo"), h.get("White"), h.get("Black")))
    return out


def board_san(toks):
    """The file's moves rewritten as a board writes them; stops at the first token the board cannot read."""
    b, out = chess.Board(), []
    for t in toks:
        try:
            m = b.parse_san(t)
        except ValueError:
            break
        out.append(b.san(m))
        b.push(m)
    return out, len(out) == len(toks)


def band(w, b):
    try:
        r = (int(w) + int(b)) / 2
    except (TypeError, ValueError):
        return None
    return "<1400" if r < 1400 else ("1400-1799" if r < 1800 else ">=1800")


jan_raw, feb_raw = read(jan_src), read(feb_src)
with Pool(4) as pool:
    jan_b = pool.map(board_san, [g[0] for g in jan_raw], chunksize=500)
    feb_b = pool.map(board_san, [g[0] for g in feb_raw], chunksize=500)
print("read and rewritten", len(jan_raw), len(feb_raw), round(time.time() - t0), "s", flush=True)
jan = [g for g, _ in jan_b]
feb = [g for g, _ in feb_b]
jan_unreadable = sum(1 for _, ok in jan_b if not ok)
feb_unreadable = sum(1 for _, ok in feb_b if not ok)
respelled = sum(1 for (raw, *_), (g, _) in zip(jan_raw, jan_b) for a, b in zip(raw, g) if a != b)

# January: departures on board SAN, the tree of beginnings played by >= 2 games
dep = departures(jan)
pref = Counter()
for i, g in enumerate(jan):
    for k in range(1, min(dep[i][1], len(g)) + 1):
        pref[tuple(g[:k])] += 1
tree = {}
for p, c in pref.items():
    node = tree
    for m in p[:-1]:
        node = node[m][1]
    node.setdefault(p[-1], [0, {}])[0] = c
def compact(node):
    return {m: ([c, compact(ch)] if ch else c) for m, (c, ch) in sorted(node.items(), key=lambda kv: -kv[1][0])}
n_jan = len(jan)
# share of January's games that had left every other January game by ply k (k = 1..80)
dply = Counter(d for d, _ in dep if d is not None)
cdf, acc = [], 0
for k in range(1, 81):
    acc += dply.get(k, 0)
    cdf.append(round(acc / n_jan, 5))
json.dump({"games": n_jan, "tree": compact(tree), "left_by_ply": cdf}, open("tree.json", "w"), separators=(",", ":"))

# February against January
order = sorted(jan)
def true_shared(g):  # the longest beginning of g that some January game shares
    i = bisect.bisect_left(order, g)
    best = 0
    for j in (i - 1, i):
        if 0 <= j < len(order):
            best = max(best, lcp(order[j], g))
    return best
def horizon(g):  # smallest k with fewer than two January games sharing the first k plies, or None
    node = tree
    for k, m in enumerate(g, 1):
        if m not in node:
            return k
        node = node[m][1]
    return None
H, T, bands = [], [], {}
for (raw, we, be, *_), g in zip(feb_raw, feb):
    if not g:
        continue
    h = horizon(g)
    ts = true_shared(g)
    H.append(h)
    T.append(ts + 1 if ts < len(g) else None)
    bands.setdefault(band(we, be), []).append(h if h is not None else len(g) + 1)
n_feb = len(H)
left = [i for i in range(n_feb) if H[i] is not None]
stays = n_feb - len(left)
later = sum(1 for i in left if T[i] is None or T[i] > H[i])
med = statistics.median(h if h is not None else len(feb[i]) + 1 for i, h in enumerate(H) if feb[i])
bmed = {b: statistics.median(v) for b, v in bands.items() if b}
hist = Counter(h for h in H if h is not None)

pred = {
    "P12 median horizon ply in [7,10]": {"value": med, "held": 7 <= med <= 10},
    "P13 share staying in tree in [0.5,3]%": {"value": round(100 * stays / n_feb, 3), "held": 0.005 <= stays / n_feb <= 0.03},
    "P14 true departure later than horizon in [20,50]% of leavers": {"value": round(100 * later / len(left), 3),
                                                                    "held": 0.20 <= later / len(left) <= 0.50},
    "P15 >=1800 median at least 1 ply later than <1400": {"value": [bmed.get(">=1800"), bmed.get("<1400")],
                                                         "held": bmed[">=1800"] - bmed["<1400"] >= 1},
}

# reading rule: ten February games at random (seed 20261020), answered as the piece would
jan_pairs = Counter(frozenset((r[3], r[4])) for r in jan_raw)
rng = random.Random(20261020)
read3 = []
for i in rng.sample(range(n_feb), 10):
    g, h = feb[i], H[i]
    counts, node = [], tree
    for m in g[: (h - 1) if h else len(g)]:
        counts.append(node[m][0])
        node = node[m][1]
    read3.append({"plies": len(g), "horizon": h, "counts": counts, "true_departure": T[i],
                  "one_january_game_still_with_it": (T[i] is None or (h is not None and T[i] > h)),
                  "pair_seen_in_january": jan_pairs.get(frozenset((feb_raw[i][3], feb_raw[i][4])), 0) > 0,
                  "band": band(feb_raw[i][1], feb_raw[i][2])})
json.dump(read3, open("read3.json", "w"), indent=1)

# P16 sample, to scratch only (single games' move lists are not committed)
rng2 = random.Random(20261020)
sample = [jan[i] for i in rng2.sample(range(n_jan), 1000)]
json.dump(sample, open(scratch + "/p16_sample.json", "w"))

out = {"january_games": n_jan, "february_games": n_feb, "january_unreadable_tails": jan_unreadable,
       "february_unreadable_tails": feb_unreadable, "january_moves_respelled_by_board": respelled,
       "tree_nodes": len(pref), "tree_nodes_session2_file_spelling": 96388,
       "january_never_depart": sum(1 for d, _ in dep if d is None),
       "february_horizon_hist": {str(k): hist[k] for k in sorted(hist)}, "february_stay": stays,
       "february_true_later_than_horizon": later, "band_medians": bmed,
       "band_counts": {b: len(v) for b, v in bands.items() if b},
       "predictions": pred, "seconds": round(time.time() - t0)}
json.dump(out, open("session3.json", "w"), indent=1)
print(json.dumps(pred, indent=1))
