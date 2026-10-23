"""The blind sheet of session 2: 20 flagged reasons the dating rule dates and 20 it does not, seed 20261024.

Population: flagged reasons on terminated or withdrawn studies with a stop month (SESSION2.md).
Usage: python3 sheet2.py RAWDIR OUTDIR. Writes OUTDIR/sheet2_texts.json (texts, shown to the reader), sheet2.json here
(position + sha256 of text) and OUTDIR/key2.json (not opened until the readings are committed). Prints the population size only.
"""
import hashlib, json, random, sys
from lib import load
from dating import line_month

raw, out = sys.argv[1], sys.argv[2]
rows = [r for r in load(raw) if r["flag"] and r["stop"] and r["status"] in ("TERMINATED", "WITHDRAWN")]
rng = random.Random(20261023 + 1)
dated = [r for r in rows if line_month(r["why"])]
undated = [r for r in rows if not line_month(r["why"])]
pick = rng.sample(dated, 20) + rng.sample(undated, 20)
rng.shuffle(pick)
json.dump([{"i": i, "text": r["why"]} for i, r in enumerate(pick)], open(out + "/sheet2_texts.json", "w"), indent=1)
json.dump([{"i": i, "sha256": hashlib.sha256(r["why"].encode()).hexdigest()} for i, r in enumerate(pick)],
          open("sheet2.json", "w"), indent=1)
json.dump([{"i": i, "nct": r["nct"], "line_month": line_month(r["why"]), "stop": r["stop"], "lastupd": r["lastupd"],
            "status": r["status"]} for i, r in enumerate(pick)], open(out + "/key2.json", "w"), indent=1)
print(len(rows), "in the population")
