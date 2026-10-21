"""Project 14, session 2: the hinge counted for French-Russian address (SESSION2.md).

python3 session2.py SENTENCES.csv LINKS.csv OUTDIR
Writes OUTDIR/session2.json (the registered count; not looked at until the rule check is read and committed), OUTDIR/check_sheet.json
(80 sentences, class withheld) and OUTDIR/check_key.json. Prints nothing of the count."""

import collections
import json
import random
import sys
import time

import numpy as np

import lib
import lib2

SEED = 20261021
CLASSES = ["eng-you", "eng-other", "epo-vi", "epo-other", "other"]


def main(spath, lpath, outdir):
    t0 = time.time()
    lang, codes, _ = lib.read_sentences(spath)
    ix = {c: i for i, c in enumerate(codes)}
    FRA, RUS, ENG, EPO = ix["fra"], ix["rus"], ix["eng"], ix["epo"]
    addr = np.full(len(lang), -1, dtype=np.int8)
    form = np.zeros(len(lang), dtype=bool)
    with open(spath, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lg, text = line.rstrip("\n").split("\t", 2)
            if lg in ("fra", "rus"):
                addr[int(sid)] = lib2.address(lg, text)
            elif lg in ("eng", "epo"):
                form[int(sid)] = lib2.has_bridge_form(lg, text)
    g, _, (u, v) = lib.read_links(lpath, lang)
    # direct fra-rus pairs
    lu, lv = lang[u], lang[v]
    m = ((lu == FRA) & (lv == RUS)) | ((lu == RUS) & (lv == FRA))
    du, dv = u[m], v[m]
    df = np.where(lang[du] == FRA, du, dv); dr = np.where(lang[du] == FRA, dv, du)
    direct = lib2.disagreement(addr[df], addr[dr])
    # chains fra-B-rus
    a_ids = np.flatnonzero(lang == FRA).astype(np.int64)
    A, B, C = lib2.chains_between(g, lang, FRA, RUS, a_ids)
    lb = lang[B]
    cls = np.full(len(B), 4, dtype=np.int8)
    cls[(lb == ENG) & form[B]] = 0
    cls[(lb == ENG) & ~form[B]] = 1
    cls[(lb == EPO) & form[B]] = 2
    cls[(lb == EPO) & ~form[B]] = 3
    by_class = {}
    for k, name in enumerate(CLASSES):
        s = cls == k
        d = lib2.disagreement(addr[A[s]], addr[C[s]])
        d["distinct_pairs"] = int(len(np.unique(A[s] * len(lang) + C[s])))
        by_class[name] = d
    allc = lib2.disagreement(addr[A], addr[C])
    allc["distinct_pairs"] = int(len(np.unique(A * len(lang) + C)))
    other = cls == 4
    top = collections.Counter(codes[x] for x in lb[other].tolist()).most_common(12)
    by_other_lang = {}
    for code, _ in top:
        s = other & (lb == ix[code])
        by_other_lang[code] = lib2.disagreement(addr[A[s]], addr[C[s]])
    ends_f, ends_r = np.unique(A), np.unique(C)
    end_classes = {"fra": collections.Counter(addr[ends_f].tolist()), "rus": collections.Counter(addr[ends_r].tolist())}
    names = {0: "none", 1: "T", 2: "V", 3: "mixed"}
    out = {
        "data": "Tatoeba weekly export of 2026-10-17 (sentences.csv, links.csv), CC BY 2.0 FR",
        "seed": SEED,
        "sentences": {"fra": int((lang == FRA).sum()), "rus": int((lang == RUS).sum())},
        "distinct_chain_ends": {k: {names[c]: int(n) for c, n in sorted(v.items())} for k, v in end_classes.items()},
        "direct": direct,
        "chains_all": allc,
        "chains_by_bridge_class": by_class,
        "other_by_bridge_language_top12": by_other_lang,
        "seconds": round(time.time() - t0, 1),
    }
    json.dump(out, open(f"{outdir}/session2.json", "w"), indent=1)
    # the rule check: 10 per class per language among distinct chain ends
    rng = random.Random(SEED)
    picks = []
    for lg, ends in (("fra", ends_f), ("rus", ends_r)):
        for c in (0, 1, 2, 3):
            pool = sorted(ends[addr[ends] == c].tolist())
            picks += [(lg, x, c) for x in rng.sample(pool, 10)]
    rng.shuffle(picks)
    need = {x for _, x, _ in picks}
    text = {}
    with open(spath, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lg, t = line.rstrip("\n").split("\t", 2)
            if int(sid) in need:
                text[int(sid)] = t
    sheet = [{"n": i, "id": x, "lang": lg, "text": text[x]} for i, (lg, x, _) in enumerate(picks, 1)]
    key = [{"n": i, "id": x, "rule": names[c]} for i, (_, x, c) in enumerate(picks, 1)]
    json.dump(sheet, open(f"{outdir}/check_sheet.json", "w"), ensure_ascii=False, indent=1)
    json.dump(key, open(f"{outdir}/check_key.json", "w"), indent=1)
    print("done", round(time.time() - t0, 1), "s; chains:", len(A))


if __name__ == "__main__":
    main(*sys.argv[1:4])
