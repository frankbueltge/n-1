"""Session 3 blind step: 40 flagged reasons drawn with seed 20261024 + 3, text and conditions only, to scratch; the key (sheet number ->
index) to a separate scratch file. Usage: python3 sheet3.py RAWDIR OUTDIR."""
import json, random, sys
import lib3

rows = [r for r in lib3.load(sys.argv[1]) if r["flag"]]
rnd = random.Random(20261024 + 3)
pick = rnd.sample(range(len(rows)), 40)
out = sys.argv[2]
with open(out + "/sheet3.txt", "w") as f:
    for n, i in enumerate(pick, 1):
        f.write("%d| %s || %s\n" % (n, rows[i]["why"].replace("\n", " "), "; ".join(rows[i]["cond"])[:120]))
json.dump([{"n": n, "i": i, "nct": rows[i]["nct"]} for n, i in enumerate(pick, 1)], open(out + "/sheet3_key.json", "w"))
json.dump({"seed": 20261024 + 3, "nct": [rows[i]["nct"] for i in pick]}, open("sheet3.json", "w"), indent=1)
