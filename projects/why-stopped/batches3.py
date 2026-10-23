"""Session 3: every flagged reason into numbered reading batches (text and conditions only) and a key (index, NCT, sha256), both to
scratch. Usage: python3 batches3.py RAWDIR OUTDIR. Order: the register's page order."""
import hashlib, json, sys
import lib3

rows = [r for r in lib3.load(sys.argv[1]) if r["flag"]]
out = sys.argv[2]
key = []
for i, r in enumerate(rows):
    key.append({"i": i, "nct": r["nct"], "sha256": hashlib.sha256(r["why"].encode()).hexdigest()})
B = 100
for b in range(0, len(rows), B):
    with open("%s/batch_%02d.txt" % (out, b // B), "w") as f:
        for i in range(b, min(b + B, len(rows))):
            r = rows[i]
            f.write("%d| %s || %s\n" % (i, r["why"].replace("\n", " "), "; ".join(r["cond"])[:120]))
json.dump(key, open(out + "/key3.json", "w"))
print(len(rows), (len(rows) + B - 1) // B)
