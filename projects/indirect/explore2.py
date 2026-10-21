"""Project 14, session 2, exploratory (not registered; written after session2.json was read): why the chains through English "you"
disagree more than independent choice would. Every path fra-B-rus through an English bridge holding a you-form, linked ends included,
and per bridge how many T and V translations each side has.

python3 explore2.py SENTENCES.csv LINKS.csv  -> explore2.json"""

import collections
import json
import sys

import numpy as np

import lib
import lib2


def main(spath, lpath):
    lang, codes, _ = lib.read_sentences(spath)
    ix = {c: i for i, c in enumerate(codes)}
    FRA, RUS, ENG = ix["fra"], ix["rus"], ix["eng"]
    addr = np.full(len(lang), -1, dtype=np.int8)
    form = np.zeros(len(lang), dtype=bool)
    with open(spath, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lg, text = line.rstrip("\n").split("\t", 2)
            if lg in ("fra", "rus"):
                addr[int(sid)] = lib2.address(lg, text)
            elif lg == "eng":
                form[int(sid)] = lib2.has_bridge_form(lg, text)
    g, _, (u, v) = lib.read_links(lpath, lang)
    indptr, nbr = g
    n = len(lang)
    lu, lv = lang[u], lang[v]
    m = ((lu == FRA) & (lv == RUS)) | ((lu == RUS) & (lv == FRA))
    df = np.where(lang[u[m]] == FRA, u[m], v[m]); dr = np.where(lang[u[m]] == FRA, v[m], u[m])
    direct = np.unique(df * n + dr)
    bridges = np.flatnonzero((lang == ENG) & form)
    deg = indptr[bridges + 1] - indptr[bridges]
    Bs = np.repeat(bridges, deg)
    X = nbr[np.repeat(indptr[bridges], deg) + np.arange(len(Bs)) - np.repeat(np.cumsum(deg) - deg, deg)]
    ok = np.isin(addr[X], (1, 2))
    Bs, X = Bs[ok], X[ok]
    fsel, rsel = lang[X] == FRA, lang[X] == RUS
    BF, F = Bs[fsel], X[fsel]  # grouped by bridge, bridges ascending
    BR, R = Bs[rsel], X[rsel]
    ub = np.intersect1d(BF, BR)
    f0, f1 = np.searchsorted(BF, ub, "left"), np.searchsorted(BF, ub, "right")
    r0, r1 = np.searchsorted(BR, ub, "left"), np.searchsorted(BR, ub, "right")
    nf, nr = f1 - f0, r1 - r0
    k = nf * nr
    gi = np.repeat(np.arange(len(ub)), k)
    j = np.arange(k.sum()) - np.repeat(np.cumsum(k) - k, k)
    A = F[f0[gi] + j // nr[gi]]
    C = R[r0[gi] + j % nr[gi]]
    key = A * n + C
    pos = np.minimum(np.searchsorted(direct, key), len(direct) - 1)
    linked = direct[pos] == key
    agree = addr[A] == addr[C]
    paths_linked = {"agree": int((agree & linked).sum()), "disagree": int((~agree & linked).sum())}
    paths_unlinked = {"agree": int((agree & ~linked).sum()), "disagree": int((~agree & ~linked).sum())}
    per_bridge = collections.Counter()
    side = lambda t, v: "both" if t and v else "T" if t else "V"
    fT = np.add.reduceat((addr[F] == 1).astype(np.int64), f0); fV = nf - fT
    rT = np.add.reduceat((addr[R] == 1).astype(np.int64), r0); rV = nr - rT
    for a, b, c, d in zip(fT.tolist(), fV.tolist(), rT.tolist(), rV.tolist()):
        per_bridge[(side(a, b), side(c, d))] += 1
    out = {
        "exploratory": True,
        "note": "paths fra-B-rus through an English sentence with a you-form, both ends classified T or V; a path is a (fra, B, rus) triple",
        "paths_with_linked_ends": dict(paths_linked),
        "paths_with_unlinked_ends": dict(paths_unlinked),
        "bridges_with_classified_ends_on_both_sides": sum(per_bridge.values()),
        "bridges_by_french_side_and_russian_side": {f"{a}|{b}": c for (a, b), c in sorted(per_bridge.items())},
    }
    json.dump(out, open("explore2.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:3])
