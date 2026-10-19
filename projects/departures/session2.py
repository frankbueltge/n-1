"""Session 2, the registered run (SESSION2.md): the month as one figure. Reads the PGN from scratch; writes session2.json, figure.json, rows2.json."""
import gzip, io, json, random, statistics, sys, time
from collections import Counter
import zstandard
from lib import parse_pgn, san_tokens, departures, lcp

ROWS, PLIES = 1000, 60
src = sys.argv[1]
t0 = time.time()
stream = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(open(src, "rb")), encoding="utf-8")
games, meta = [], []
for h, mt in parse_pgn(stream):
    if "FEN" in h or h.get("SetUp") == "1":
        continue
    toks = san_tokens(mt)
    if not toks:
        continue
    games.append(toks)
    meta.append({"pair": frozenset((h.get("White"), h.get("Black"))), "opening": h.get("Opening")})
n = len(games)
dep = departures(games)
print("parsed and departed", n, round(time.time() - t0), "s", flush=True)

# P7: shared plies over all plies (a never-departing game is shared over its whole length)
total = sum(len(g) for g in games)
shared = sum(min(dep[i][1], len(games[i])) for i in range(n))
# P8
first = Counter(g[0] for g in games)

# the figure: games in move order, binned into ROWS rows
order = sorted(range(n), key=lambda i: games[i])
def dply(i):  # departure ply; a never-departing game counts as departing after its last ply
    return dep[i][0] if dep[i][0] is not None else len(games[i]) + 1
bounds = [round(r * n / ROWS) for r in range(ROWS + 1)]
rows = []
for r in range(ROWS):
    idx = order[bounds[r]:bounds[r + 1]]
    cells = []
    for p in range(1, PLIES + 1):
        s = sum(1 for i in idx if len(games[i]) >= p and dply(i) > p)
        o = sum(1 for i in idx if len(games[i]) >= p and dply(i) <= p)
        cells.append([s, o])
    rows.append({"games": len(idx), "median": statistics.median(dply(i) for i in idx), "cells": cells,
                 "common": lcp(games[idx[0]], games[idx[-1]])})
meds = [r["median"] for r in rows]
# first-move spans for labels
spans = []
for r, row in enumerate(rows):
    m = games[order[bounds[r]]][0]
    if spans and spans[-1]["move"] == m:
        spans[-1]["to"] = r
    else:
        spans.append({"move": m, "from": r, "to": r})
for s in spans:
    s["games"] = first[s["move"]]

# P11 and the exploratory trie of shared beginnings (nodes played by >= 2 games)
pref = Counter()
for i in range(n):
    g = games[i]
    for k in range(1, min(dep[i][1], len(g)) + 1):
        pref[tuple(g[:k])] += 1
trie = {}
for p, c in pref.items():
    node = trie
    for m in p[:-1]:
        node = node[m][1]
    node.setdefault(p[-1], [0, {}])[0] = c
def compact(node):
    return {m: ([c, compact(ch)] if ch else c) for m, (c, ch) in node.items()}
blob = json.dumps(compact(trie), separators=(",", ":")).encode()

pred = {
    "P7 shared share of all plies in [10,20]%": {"value": round(100 * shared / total, 3), "held": 0.10 <= shared / total <= 0.20},
    "P8 more than half begin 1.e4": {"value": round(100 * first["e4"] / n, 3), "held": first["e4"] / n > 0.5},
    "P9 latest row median >= 16": {"value": max(meds), "held": max(meds) >= 16},
    "P10 fewer than 5% of rows median >= 13": {"value": round(100 * sum(1 for m in meds if m >= 13) / ROWS, 3),
                                              "held": sum(1 for m in meds if m >= 13) / ROWS < 0.05},
    "P11 shared beginnings < 500,000": {"value": len(pref), "held": len(pref) < 500000},
}
out = {"games": n, "plies_total": total, "plies_shared": shared, "first_moves": first.most_common(),
       "rows": ROWS, "row_median_hist": dict(sorted(Counter(meds).items())), "spans": spans,
       "shared_beginnings": len(pref), "trie_json_bytes": len(blob), "trie_json_gzip_bytes": len(gzip.compress(blob, 9)),
       "predictions": pred, "seconds": round(time.time() - t0)}
json.dump(out, open("session2.json", "w"), indent=1)
json.dump({"plies": PLIES, "rows": [{"m": r["median"], "c": r["cells"]} for r in rows], "spans": spans,
           "games": n}, open("figure.json", "w"), separators=(",", ":"))

# reading rule: 5 latest-median rows, 5 random rows (seed 20261020)
latest = sorted(range(ROWS), key=lambda r: -meds[r])[:5]
random.seed(20261020)
pick = [("latest", r) for r in latest] + [("random", r) for r in random.sample(range(ROWS), 5)]
read = []
for why, r in pick:
    idx = order[bounds[r]:bounds[r + 1]]
    read.append({"why": why, "row": r, "games": len(idx), "median_departure": meds[r],
                 "shared_beginning": games[idx[0]][:rows[r]["common"]],
                 "distinct_pairs": len({meta[i]["pair"] for i in idx}),
                 "opening_tags": Counter(meta[i]["opening"] for i in idx).most_common(3)})
json.dump(read, open("rows2.json", "w"), indent=1)
print(json.dumps(pred, indent=1)); print("done", round(time.time() - t0), "s")
