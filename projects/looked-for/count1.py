"""The registered count of session 1 (SELECTION.md, 'Session 1's question'). Run once, after the readings were committed."""
import hashlib, json, time, urllib.request, urllib.parse

API = "https://api.gbif.org/v1/"
LOG = []

def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                body = r.read()
            LOG.append({"url": url, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "sha256": hashlib.sha256(body).hexdigest()})
            return json.loads(body)
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError(url)

def n(**f):
    return get("occurrence/search", limit=0, **f)["count"]

def facet(name, limit, **f):
    d = get("occurrence/search", limit=0, facet=name, facetLimit=limit, **f)
    return [(c["name"], c["count"]) for c in (d["facets"][0]["counts"] if d.get("facets") else [])]

out = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
out["total"] = n()
out["by_status"] = {s: n(occurrenceStatus=s) for s in ["PRESENT", "ABSENT"]}
# DETECTED and NOT_DETECTED are listed by /enumeration/basic/OccurrenceStatus, but the search answers
# "Cannot parse DETECTED into a known OccurrenceStatus" (HTTP 400, read 23:28 UTC); recorded, not counted.
out["refused_statuses"] = {"DETECTED": "Cannot parse DETECTED into a known OccurrenceStatus",
                           "NOT_DETECTED": "Cannot parse NOT_DETECTED into a known OccurrenceStatus"}
out["status_facet_unfiltered"] = dict(facet("occurrenceStatus", 10))
issues = ["OCCURRENCE_STATUS_INFERRED_FROM_INDIVIDUAL_COUNT", "OCCURRENCE_STATUS_INFERRED_FROM_BASIS_OF_RECORD",
          "INDIVIDUAL_COUNT_CONFLICTS_WITH_OCCURRENCE_STATUS", "OCCURRENCE_STATUS_UNPARSABLE"]
out["issue_by_status"] = {i: {s: n(occurrenceStatus=s, issue=i) for s in ["PRESENT", "ABSENT"]} | {"all": n(issue=i)} for i in issues}
ds = facet("datasetKey", 200000, occurrenceStatus="ABSENT")
out["absent_datasets"] = len(ds)
out["absent_dataset_facet_sum"] = sum(c for _, c in ds)
top = []
for key, c in ds[:10]:
    d = get(f"dataset/{key}")
    org = get(f"organization/{d['publishingOrganizationKey']}") if d.get("publishingOrganizationKey") else {}
    top.append({"datasetKey": key, "absent": c, "total": n(datasetKey=key), "title": d.get("title"),
                "publisher": org.get("title"), "license": d.get("license"), "doi": d.get("doi")})
out["absent_top10"] = top
out["absent_top10_share"] = sum(t["absent"] for t in top) / out["by_status"]["ABSENT"]
out["absent_dataset_counts"] = [c for _, c in ds]
names = {}
def kname(k):
    if k not in names:
        names[k] = get(f"species/{k}").get("scientificName", k)
    return names[k]
out["absent_by_kingdom"] = {kname(k): c for k, c in facet("kingdomKey", 50, occurrenceStatus="ABSENT")}
out["present_by_kingdom"] = {kname(k): c for k, c in facet("kingdomKey", 50, occurrenceStatus="PRESENT")}
out["absent_by_year"] = dict(sorted(facet("year", 1000, occurrenceStatus="ABSENT")))
out["present_by_year"] = dict(sorted(facet("year", 1000, occurrenceStatus="PRESENT")))
out["absent_by_country"] = dict(facet("country", 400, occurrenceStatus="ABSENT"))
A = out["by_status"]["ABSENT"]
inf = out["issue_by_status"]["OCCURRENCE_STATUS_INFERRED_FROM_INDIVIDUAL_COUNT"]["ABSENT"]
ak = out["absent_by_kingdom"]
out["predictions"] = {
    "P1 absent >= 10,000,000": A >= 10_000_000,
    "P2 absent < 2 % of all": A / out["total"] < 0.02,
    "P3 top ten datasets hold >= half of absent": out["absent_top10_share"] >= 0.5,
    "P4 Animalia absent > Plantae absent": ak.get("Animalia", 0) > ak.get("Plantae", 0),
    "P5 >= 10 % of absent inferred from a zero count": inf / A >= 0.10,
}
out["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(out, open("projects/looked-for/session1.json", "w"), indent=1)
json.dump(LOG, open("projects/looked-for/fetch_log.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ["total", "by_status", "issue_by_status", "absent_datasets", "absent_dataset_facet_sum",
      "absent_top10_share", "absent_by_kingdom", "predictions", "status_facet_unfiltered"]}, indent=1))
for t in top: print(t)
