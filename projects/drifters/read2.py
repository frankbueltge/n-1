"""Reading rule of SESSION2.md: 30 random rows (seed 20261018) and the 10 largest shifts, raw line beside directory row."""
import json, os, random, sys
from session2 import run
from fetch import FILES


def raw_dir(src):
    out = {}
    for f in FILES:
        for line in open(os.path.join(src, f), encoding="latin-1"):
            p = line.split()
            if p and p[0] not in out:
                out[p[0]] = " ".join(p)
    return out


def main(dd, dirsrc):
    out, joined, d = run(dd, dirsrc)
    raw = raw_dir(dirsrc)
    random.seed(20261018)
    sample = random.sample(joined, 30)
    top = sorted([r for r in joined if r["shift"] is not None], key=lambda r: -r["shift"])[:10]
    show = lambda r: {"id": r["id"], "file_row": r["raw"], "shift_days": None if r["shift"] is None else round(r["shift"], 1),
                      "class": r["class"], "directory_agrees": r["agrees"], "directory_row": raw[r["id"]]}
    json.dump({"random_30": [show(r) for r in sample], "largest_10": [show(r) for r in top]}, open("verify2.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
