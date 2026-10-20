"""Project 14: the link graph of a Tatoeba export, and the chains in it.

Definitions are SELECTION.md's. Sentences are indexed by their Tatoeba id. A chain A-B-C has A linked to B, B linked to C,
the three in three different languages, and no link between A and C."""

import random

import numpy as np

UNKNOWN = "\\N"


def read_sentences(path):
    """Return (lang array indexed by id, list of language codes, counts). Language index -1: no sentence or unknown language."""
    ids, langs, codes, code_ix = [], [], [], {}
    unknown = 0
    with open(path, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lang, _ = line.split("\t", 2)
            if lang == UNKNOWN:
                unknown += 1
                continue
            if lang not in code_ix:
                code_ix[lang] = len(codes)
                codes.append(lang)
            ids.append(int(sid))
            langs.append(code_ix[lang])
    ids = np.array(ids, dtype=np.int64)
    lang = np.full(int(ids.max()) + 1, -1, dtype=np.int32)
    lang[ids] = np.array(langs, dtype=np.int32)
    return lang, codes, {"sentences_known_language": int(len(ids)), "sentences_unknown_language": unknown}


def read_links(path, lang):
    """Return the undirected cross-language links as a CSR graph (indptr, nbr) over ids, and counts."""
    a = np.fromfile(path, dtype=np.int64, sep=" ").reshape(-1, 2)  # sep=" " matches any whitespace, tabs and newlines included
    return build_graph(a, lang)


def build_graph(a, lang):
    n = len(lang)
    counts = {"link_rows": int(len(a))}
    inside = (a[:, 0] < n) & (a[:, 1] < n)
    a = a[inside]
    known = (lang[a[:, 0]] >= 0) & (lang[a[:, 1]] >= 0)
    counts["link_rows_missing_or_unknown_end"] = int((~inside).sum() + (~known).sum())
    a = a[known]
    a = a[a[:, 0] != a[:, 1]]
    u = np.minimum(a[:, 0], a[:, 1])
    v = np.maximum(a[:, 0], a[:, 1])
    key = np.unique(u * n + v)
    u, v = key // n, key % n
    same = lang[u] == lang[v]
    counts["undirected_links_same_language"] = int(same.sum())
    u, v = u[~same], v[~same]
    counts["direct_pairs"] = int(len(u))
    src = np.concatenate([u, v])
    dst = np.concatenate([v, u])
    order = np.lexsort((dst, src))
    src, dst = src[order], dst[order]
    indptr = np.zeros(n + 1, dtype=np.int64)
    np.add.at(indptr, src + 1, 1)
    indptr = np.cumsum(indptr)
    return (indptr, dst), counts, (u, v)


def nbrs(g, x):
    indptr, nbr = g
    return nbr[indptr[x]:indptr[x + 1]]


def far_ends(g, lang, a, b):
    """The far ends C of chains a-b-C (b assumed linked to a in another language)."""
    near = set(nbrs(g, a).tolist())
    la, lb = lang[a], lang[b]
    return [c for c in nbrs(g, b).tolist() if c != a and lang[c] != la and lang[c] != lb and c not in near]


def bridges(g, lang, a):
    """A's bridges that lead to at least one far end."""
    return [b for b in nbrs(g, a).tolist() if far_ends(g, lang, a, b)]


def count_indirect(g, lang, budget=40_000_000):
    """Distinct unordered indirect pairs, the number of chain ends, and the ends themselves (a boolean array).

    Vectorised over blocks of A: every path A-B-C is generated, filtered by the chain rule, and its (A, C) keys made unique."""
    indptr, nbr = g
    n = len(lang)
    deg = np.diff(indptr)
    is_end = np.zeros(n, dtype=bool)
    per_a_total = 0
    # paths starting at A: sum over B in N(A) of deg(B)
    path_len = np.zeros(n, dtype=np.int64)
    src_all = np.repeat(np.arange(n, dtype=np.int64), deg)
    np.add.at(path_len, src_all, deg[nbr])
    del src_all
    cum = np.cumsum(path_len)
    a0 = 0
    while a0 < n:
        base = cum[a0 - 1] if a0 > 0 else 0
        a1 = int(np.searchsorted(cum, base + budget, side="right"))
        a1 = max(a1, a0 + 1)
        a1 = min(a1, n)
        e0, e1 = indptr[a0], indptr[a1]
        if e1 > e0:
            A = np.repeat(np.arange(a0, a1, dtype=np.int64), deg[a0:a1])
            B = nbr[e0:e1]
            dB = deg[B]
            A2 = np.repeat(A, dB)
            B2 = np.repeat(B, dB)
            starts = np.repeat(indptr[B], dB)
            offs = np.arange(len(A2), dtype=np.int64) - np.repeat(np.cumsum(dB) - dB, dB)
            C2 = nbr[starts + offs]
            la, lb, lc = lang[A2], lang[B2], lang[C2]
            keep = (C2 != A2) & (lc != la) & (lc != lb)
            A2, C2 = A2[keep], C2[keep]
            keys = np.unique(A2 * n + C2)
            direct = A * n + B  # every link of A (the graph holds cross-language links only; same-language C is excluded above)
            keys = keys[~np.isin(keys, direct, assume_unique=False)]
            per_a_total += len(keys)
            is_end[np.unique(keys // n)] = True
        a0 = a1
    assert per_a_total % 2 == 0
    return per_a_total // 2, is_end


def sample_chains(g, lang, is_end, k, rng):
    ends = np.flatnonzero(is_end)
    out = []
    while len(out) < k:
        a = int(ends[rng.randrange(len(ends))])
        bs = bridges(g, lang, a)
        b = bs[rng.randrange(len(bs))]
        cs = far_ends(g, lang, a, b)
        c = cs[rng.randrange(len(cs))]
        out.append((a, b, c))
    return out


def sample_direct(pairs, k, rng):
    u, v = pairs
    picks = rng.sample(range(len(u)), k)
    return [(int(u[i]), int(v[i])) for i in picks]
