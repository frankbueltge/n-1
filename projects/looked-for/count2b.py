"""Session 2, verified correction (LOG.md 01:08). count2.py faceted on taxonKey, which the index counts at every rank of a record's
classification (a coral counts under its species, genus, family...), so 'names' and 'never found' were inflated and S's never-found
share came out at 123 %. Here the same counts on acceptedTaxonKey, the record's own taxon, whose facet sums to the status count.
P3 and P4 are reported as registered (session2.json) and again here."""
import hashlib, json, time, urllib.request, urllib.parse

API = "https://api.gbif.org/v1/"
LOG = []
SETS = {"S": "b6b4502f-ffc8-4048-a91b-af502288faa8", "K": "154d6192-bea0-4bcb-ab58-1c573081591d",
        "F": "d59ccafb-251e-46cf-9319-37b58d88e7c5"}

def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                body = r.read()
            LOG.append({"url": url, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "sha256": hashlib.sha256(body).hexdigest()})
            return json.loads(body)
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError(url)

def facet(name, limit, **f):
    d = get("occurrence/search", limit=0, facet=name, facetLimit=limit, **f)
    return [(c["name"], c["count"]) for c in (d["facets"][0]["counts"] if d.get("facets") else [])]

s2 = json.load(open("session2.json"))
out = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "facet": "acceptedTaxonKey", "datasets": {}}
for tag, key in SETS.items():
    D = s2["datasets"][tag]
    ta = dict(facet("acceptedTaxonKey", 100000, datasetKey=key, occurrenceStatus="ABSENT"))
    tp = dict(facet("acceptedTaxonKey", 100000, datasetKey=key, occurrenceStatus="PRESENT"))
    names = {}
    def nm(k):
        if k not in names:
            names[k] = get(f"species/{k}").get("scientificName")
        return names[k]
    d = {"names_absent": len(ta), "names_present": len(tp), "names_any": len(set(ta) | set(tp)),
         "absent_facet_sum": sum(ta.values()), "present_facet_sum": sum(tp.values()),
         "sums_match_status_counts": sum(ta.values()) == D["absent"] and sum(tp.values()) == D["present"]}
    never = sorted(((k, c) for k, c in ta.items() if k not in tp), key=lambda x: -x[1])
    d["never_found_names"] = len(never)
    d["never_found_absences"] = sum(c for _, c in never)
    d["never_found_share_of_absences"] = d["never_found_absences"] / D["absent"]
    d["never_found"] = [{"acceptedTaxonKey": k, "absent": c, "name": nm(k)} for k, c in never]
    if tag == "S":
        d["absent_names"] = [{"acceptedTaxonKey": k, "name": nm(k), "absent": c, "present": tp.get(k, 0)}
                             for k, c in sorted(ta.items(), key=lambda x: -x[1])]
        d["present_only_names"] = len(set(tp) - set(ta))
        d["present_only_records"] = sum(c for k, c in tp.items() if k not in ta)
    out["datasets"][tag] = d
X = out["datasets"]
out["predictions_corrected"] = {
    "P3 each holds a never-found name": {t: X[t]["never_found_names"] >= 1 for t in X},
    "P4 S never-found >= 10 % of its absences": X["S"]["never_found_share_of_absences"] >= 0.10,
}
out["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(out, open("session2b.json", "w"), indent=1, ensure_ascii=False)
json.dump(LOG, open("fetch_log2b.json", "w"), indent=1)
for t, d in X.items():
    print(t, {k: v for k, v in d.items() if k not in ("never_found", "absent_names")})
    print("  never", [(a["name"], a["absent"]) for a in d["never_found"]])
for a in X["S"]["absent_names"]: print(a)
print(out["predictions_corrected"])
