"""Definitions of SELECTION.md, as code. Departure ply, stem, never-departs; position departure."""
import re
from collections import Counter

_COMMENT = re.compile(r"\{[^}]*\}|;[^\n]*|\([^)]*\)")
_NUM = re.compile(r"^\d+\.(\.\.)?$|^\d+\.\.\.$")
_RESULTS = {"1-0", "0-1", "1/2-1/2", "*"}


def parse_pgn(lines):
    """Yield (headers, movetext) per game from an iterable of text lines."""
    headers, moves, in_moves = {}, [], False
    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("["):
            if in_moves:
                yield headers, " ".join(moves)
                headers, moves, in_moves = {}, [], False
            m = re.match(r'\[(\w+) "(.*)"\]', line)
            if m:
                headers[m.group(1)] = m.group(2)
        elif line.strip():
            in_moves = True
            moves.append(line)
    if headers or moves:
        yield headers, " ".join(moves)


def san_tokens(movetext):
    """SAN tokens: move numbers, comments, annotations, NAGs and the result removed."""
    text = _COMMENT.sub(" ", movetext)
    out = []
    for tok in text.split():
        if tok in _RESULTS or tok.startswith("$"):
            continue
        tok = re.sub(r"^\d+\.(\.\.)?", "", tok)  # "1.e4" -> "e4"
        if not tok or _NUM.match(tok):
            continue
        tok = tok.rstrip("!?")
        if tok:
            out.append(tok)
    return out


def lcp(a, b):
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def departures(games):
    """games: list of move lists. Returns list of (departure_ply or None, stem_len).
    Departure ply k (1-based): smallest k with no other game sharing the first k plies.
    None: never departs (the whole list is a prefix of, or equal to, another game's)."""
    order = sorted(range(len(games)), key=lambda i: games[i])
    best = [0] * len(games)
    for a, b in zip(order, order[1:]):
        l = lcp(games[a], games[b])
        best[a] = max(best[a], l)
        best[b] = max(best[b], l)
    out = []
    for i, g in enumerate(games):
        k = best[i] + 1
        out.append((k if k <= len(g) else None, best[i]))
    return out


def position_departures(keys):
    """keys: per game, list of position keys after each ply (index 0 = after ply 1).
    Returns per game the first ply whose position occurs in no other game at any ply, or None."""
    seen = Counter()
    for ks in keys:
        seen.update(set(ks))
    out = []
    for ks in keys:
        p = None
        for j, h in enumerate(ks, 1):
            if seen[h] == 1:
                p = j
                break
        out.append(p)
    return out
