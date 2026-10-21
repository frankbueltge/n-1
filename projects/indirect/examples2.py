"""Project 14, session 2: examples for the page (exploratory; chosen after the count). English sentences with a you-form that have,
among their own translations, a French T and a French V sentence and a Russian T and a Russian V sentence: the four corners of the
hinge. Six drawn with seed 20261021 among those whose English is at most 32 characters; for each, one sentence per corner (the
lowest id), and whether each of the four French-Russian pairs is linked directly.

python3 examples2.py SENTENCES.csv LINKS.csv  -> examples2.json"""

import json
import random
import sys

import numpy as np

import lib
import lib2


def main(spath, lpath):
    lang, codes, _ = lib.read_sentences(spath)
    ix = {c: i for i, c in enumerate(codes)}
    FRA, RUS, ENG = ix["fra"], ix["rus"], ix["eng"]
    addr = np.full(len(lang), -1, dtype=np.int8)
    eng_text = {}
    other_text = {}
    with open(spath, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lg, text = line.rstrip("\n").split("\t", 2)
            if lg in ("fra", "rus"):
                addr[int(sid)] = lib2.address(lg, text)
                other_text[int(sid)] = text
            elif lg == "eng" and len(text) <= 32 and lib2.has_bridge_form(lg, text):
                eng_text[int(sid)] = text
    g, _, _ = lib.read_links(lpath, lang)
    indptr, nbr = g
    cand = []
    for b in sorted(eng_text):
        nb = nbr[indptr[b]:indptr[b + 1]]
        corners = {}
        for L, name in ((FRA, "fra"), (RUS, "rus")):
            for c, cn in ((1, "T"), (2, "V")):
                s = nb[(lang[nb] == L) & (addr[nb] == c)]
                if len(s):
                    corners[f"{name}_{cn}"] = int(s.min())
        if len(corners) == 4:
            cand.append((b, corners))
    rng = random.Random(20261021)
    picks = rng.sample(cand, 6)
    out = {"exploratory": True, "english_you_sentences_with_all_four_corners_(<=32_chars)": len(cand), "examples": []}
    for b, cr in picks:
        def linked(x, y):
            return bool(np.isin(y, nbr[indptr[x]:indptr[x + 1]]))
        out["examples"].append({
            "eng": {"id": b, "text": eng_text[b]},
            **{k: {"id": v, "text": other_text[v]} for k, v in cr.items()},
            "linked": {"T-T": linked(cr["fra_T"], cr["rus_T"]), "V-V": linked(cr["fra_V"], cr["rus_V"]),
                       "T-V": linked(cr["fra_T"], cr["rus_V"]), "V-T": linked(cr["fra_V"], cr["rus_T"])},
        })
    json.dump(out, open("examples2.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:3])
