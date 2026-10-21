"""Project 14, session 3: the crossing, read whole (SESSION3.md).

python3 session3.py SENTENCES.csv LINKS.csv OUTDIR
Draws 30 English "you" sentences with 5-12 direct translations (not English, not Esperanto), seed 202610213, and writes
OUTDIR/sheet3.json (every translation, shuffled; English sentence, group and links withheld) and OUTDIR/key3.json (groups and the links
among each group's translations; not opened until the readings are committed). Prints only sizes."""

import json
import random
import sys

import numpy as np

import lib
import lib2

SEED = 202610213
N, LO, HI = 30, 5, 12


def main(spath, lpath, outdir):
    lang, codes, _ = lib.read_sentences(spath)
    ix = {c: i for i, c in enumerate(codes)}
    ENG, EPO = ix["eng"], ix["epo"]
    you = np.zeros(len(lang), dtype=bool)
    with open(spath, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lg, text = line.rstrip("\n").split("\t", 2)
            if lg == "eng" and lib2.has_bridge_form("eng", text):
                you[int(sid)] = True
    g, _, _ = lib.read_links(lpath, lang)
    indptr, nbr = g
    deg = np.zeros(len(lang), dtype=np.int64)
    eligible = []
    for e in np.flatnonzero(you).tolist():
        t = [x for x in lib.nbrs(g, e).tolist() if lang[x] not in (ENG, EPO)]
        if LO <= len(t) <= HI:
            eligible.append(e)
    rng = random.Random(SEED)
    drawn = rng.sample(eligible, N)
    groups, rows = [], []
    for e in drawn:
        t = sorted(x for x in lib.nbrs(g, e).tolist() if lang[x] not in (ENG, EPO))
        ts = set(t)
        links = sorted([a, b] for a in t for b in lib.nbrs(g, a).tolist() if b in ts and a < b)
        groups.append({"eng": e, "translations": t, "links": links})
        rows.extend((e, x) for x in t)
    need = {x for _, x in rows} | set(drawn)
    text = {}
    with open(spath, encoding="utf-8", newline="\n") as f:
        for line in f:
            sid, lg, tx = line.rstrip("\n").split("\t", 2)
            if int(sid) in need:
                text[int(sid)] = (lg, tx)
    rng.shuffle(rows)
    sheet = [{"n": i + 1, "lang": text[x][0], "text": text[x][1]} for i, (_, x) in enumerate(rows)]
    key = {"seed": SEED, "eligible": len(eligible),
           "rows": [{"n": i + 1, "id": x, "eng": e} for i, (e, x) in enumerate(rows)],
           "groups": [dict(gr, eng_text=text[gr["eng"]][1]) for gr in groups]}
    json.dump(sheet, open(f"{outdir}/sheet3.json", "w"), ensure_ascii=False, indent=0)
    json.dump(key, open(f"{outdir}/key3.json", "w"), ensure_ascii=False, indent=0)
    print("eligible", len(eligible), "rows", len(sheet), "languages", len({r['lang'] for r in sheet}))


if __name__ == "__main__":
    main(*sys.argv[1:4])
