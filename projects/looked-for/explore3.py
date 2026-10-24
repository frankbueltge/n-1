"""Session 3, exploratory, after the registered count (LOG.md): where in time S's present and absent records fall, and the 13 names'
present records by year. Not registered; reported as exploratory."""
import hashlib, json, time, urllib.request, urllib.parse
API = "https://api.gbif.org/v1/"; S = "b6b4502f-ffc8-4048-a91b-af502288faa8"; LOG = []
def facet(name, limit, **f):
    url = API + "occurrence/search?" + urllib.parse.urlencode(dict(limit=0, facet=name, facetLimit=limit, **f), doseq=True)
    body = urllib.request.urlopen(url, timeout=120).read()
    LOG.append({"url": url, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sha256": hashlib.sha256(body).hexdigest()})
    d = json.loads(body)
    return {c["name"]: c["count"] for c in d["facets"][0]["counts"]} if d.get("facets") else {}
s3 = json.load(open("session3.json")); T = [t["acceptedTaxonKey"] for t in s3["thirteen"]]
out = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "present_by_year": facet("year", 1000, datasetKey=S, occurrenceStatus="PRESENT"),
       "absent_by_year": facet("year", 1000, datasetKey=S, occurrenceStatus="ABSENT"),
       "present13_by_year": facet("year", 1000, datasetKey=S, occurrenceStatus="PRESENT", acceptedTaxonKey=T),
       "basis_present": facet("basisOfRecord", 20, datasetKey=S, occurrenceStatus="PRESENT"),
       "basis_absent": facet("basisOfRecord", 20, datasetKey=S, occurrenceStatus="ABSENT")}
out["present_dated"] = sum(out["present_by_year"].values())
json.dump(out, open("explore3.json", "w"), indent=1); json.dump(LOG, open("fetch_log3x.json", "w"), indent=1)
print(json.dumps(out, indent=1))
