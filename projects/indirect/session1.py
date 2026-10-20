"""Project 14, session 1: the registered count and the blind sheet (SELECTION.md).

python3 session1.py SENTENCES.csv LINKS.csv OUTDIR
Writes session1.json (counts; committed), OUTDIR/sheet.json (the 200 pairs, kind withheld) and OUTDIR/key.json (kinds and bridges,
not opened until the readings are committed). Prints counts only."""

import collections
import json
import random
import sys
import time

import numpy as np

import lib

SEED = 20261020


def main(spath, lpath, outdir):
    t0 = time.time()
    lang, codes, c1 = lib.read_sentences(spath)
    g, c2, pairs = lib.read_links(lpath, lang)
    n_ind, is_end = lib.count_indirect(g, lang)
    rng = random.Random(SEED)
    chains = lib.sample_chains(g, lang, is_end, 150, rng)
    direct = lib.sample_direct(pairs, 50, rng)
    deg = np.diff(g[0])
    linked = int((deg > 0).sum())
    items = [{"kind": "indirect", "a": a, "c": c, "bridge": b} for a, b, c in chains]
    items += [{"kind": "direct", "a": a, "c": c, "bridge": None} for a, c in direct]
    rng.shuffle(items)
    need = {x for it in items for x in (it["a"], it["c"], it["bridge"]) if x is not None}
    text = {}
    with open(spath, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lg, t = line.rstrip("\n").split("\t", 2)
            if int(sid) in need:
                text[int(sid)] = (lg, t)
    sheet, key = [], []
    for i, it in enumerate(items, 1):
        sheet.append({"n": i, "a": {"id": it["a"], "lang": text[it["a"]][0], "text": text[it["a"]][1]},
                      "c": {"id": it["c"], "lang": text[it["c"]][0], "text": text[it["c"]][1]}})
        b = it["bridge"]
        key.append({"n": i, "kind": it["kind"],
                    "bridge": None if b is None else {"id": b, "lang": text[b][0], "text": text[b][1]}})
    json.dump(sheet, open(f"{outdir}/sheet.json", "w"), ensure_ascii=False, indent=1)
    json.dump(key, open(f"{outdir}/key.json", "w"), ensure_ascii=False, indent=1)
    by_lang = collections.Counter(codes[l] for l in lang[lang >= 0].tolist())
    out = {
        "data": "Tatoeba weekly export of 2026-10-17 (sentences.csv, links.csv), CC BY 2.0 FR",
        "seed": SEED,
        **c1, **c2,
        "languages": len(codes),
        "sentences_with_a_cross_language_link": linked,
        "indirect_pairs": int(n_ind),
        "chain_ends": int(is_end.sum()),
        "ratio_indirect_to_direct": round(n_ind / c2["direct_pairs"], 3),
        "sentences_by_language_top20": by_lang.most_common(20),
        "sample": {"indirect": 150, "direct": 50},
        "seconds": round(time.time() - t0, 1),
    }
    json.dump(out, open("session1.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "sentences_by_language_top20"}, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
