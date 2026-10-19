"""The codes the blank units keep (verify2.json), looked up in Natural Earth's disputed-areas file (argv[1]: its .shp stem).
Writes codes.json: code -> the BRK_NAME of each feature carrying that code in any field. The names are the publisher's."""
import json, sys
import shapefile

v = json.load(open("verify2.json"))
codes = sorted({val for u in v["unnamed_raw"] for k, val in u["nonblank"].items() if k.startswith("ADM0_A3")})
r = shapefile.Reader(sys.argv[1])
f = [x[0] for x in r.fields[1:]]
out = {c: [] for c in codes}
for rec in r.records():
    d = dict(zip(f, rec))
    for c in codes:
        if c in [val for val in d.values() if isinstance(val, str)] and d["BRK_NAME"] not in out[c]:
            out[c].append(d["BRK_NAME"])
json.dump(out, open("codes.json", "w"), indent=1, ensure_ascii=False)
print(out)
