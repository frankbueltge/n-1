"""The blind sheet: 20 flagged and 20 unflagged stated reasons, stop month 2020-2022, seed 20261023.

Usage: python3 sheet.py RAWDIR OUTDIR. Writes OUTDIR/sheet_texts.json (texts, shown to the reader),
sheet.json here (position + sha256 of text), and OUTDIR/key.json (not opened until readings are committed).
"""
import hashlib, json, random, sys
from lib import load

raw, out = sys.argv[1], sys.argv[2]
rows = [r for r in load(raw) if r["why"] and r["stop"] and "2020" <= r["stop"][:4] <= "2022"]
rng = random.Random(20261023)
pick = rng.sample([r for r in rows if r["flag"]], 20) + rng.sample([r for r in rows if not r["flag"]], 20)
rng.shuffle(pick)
json.dump([{"i": i, "text": r["why"]} for i, r in enumerate(pick)], open(out + "/sheet_texts.json", "w"), indent=1)
json.dump([{"i": i, "sha256": hashlib.sha256(r["why"].encode()).hexdigest()} for i, r in enumerate(pick)],
          open("sheet.json", "w"), indent=1)
json.dump([{"i": i, "nct": r["nct"], "flag": r["flag"], "stop": r["stop"], "status": r["status"]} for i, r in enumerate(pick)],
          open(out + "/key.json", "w"), indent=1)
print(len(rows), "eligible")
