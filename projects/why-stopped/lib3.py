"""Session 3: lib.load plus each study's conditions list."""
import glob, json
import lib

def load(rawdir):
    rows = lib.load(rawdir)
    cond = {}
    for p in sorted(glob.glob(rawdir + "/page_*.json")):
        for s in json.load(open(p)).get("studies", []):
            ps = s.get("protocolSection", {})
            cond[ps.get("identificationModule", {}).get("nctId")] = ps.get("conditionsModule", {}).get("conditions", [])
    for r in rows:
        r["cond"] = cond.get(r["nct"], [])
    return rows
