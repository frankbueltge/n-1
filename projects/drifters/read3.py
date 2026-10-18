"""Reading rule of SESSION3.md: 20 random of the 1,022 (seed 20261018) and the 5 largest days of difference, raw lines beside each other."""
import json, os, random, sys
from session3 import run3
from read2 import raw_dir


def raw_file(dd, name="2013_06_30_drogueoff.dat"):
    return {l.split()[0]: l.rstrip() for l in open(os.path.join(dd, name), encoding="latin-1") if l.split() and l.split()[0].isdigit()}


def raw_old(dd):
    out = {}
    for l in open(os.path.join(dd, "dirfl_10001_15000.old"), encoding="latin-1"):
        p = l.split()
        if p and p[0] not in out:
            out[p[0]] = " ".join(p)
    return out


def main(dd, dirsrc):
    out, pop, d, old = run3(dd, dirsrc)
    rd, rf, ro = raw_dir(dirsrc), raw_file(dd), raw_old(dd)
    random.seed(20261018)
    sample = random.sample(pop, 20)
    top = sorted([r for r in pop if r["dir"] is not None], key=lambda r: -abs(r["dir"]))[:5]
    show = lambda r: {"id": r["id"], "redating_line": rf[r["id"]], "directory_row": rd[r["id"]], "old_row": ro.get(r["id"]),
                      "directory_says": r["dclass"], "days_more_following": None if r["dir"] is None else round(r["dir"], 1)}
    json.dump({"random_20": [show(r) for r in sample], "largest_5": [show(r) for r in top]}, open("verify3.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
