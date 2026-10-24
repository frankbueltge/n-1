"""The registered count of session 2 (SESSION2.md). Run once, after readings2.json was committed."""
import hashlib, json, random, statistics, sys, time, urllib.request, urllib.parse
from collections import Counter

API = "https://api.gbif.org/v1/"
LOG = []
SCRATCH = sys.argv[1]
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

def n(**f):
    return get("occurrence/search", limit=0, **f)["count"]

def facet(name, limit, **f):
    d = get("occurrence/search", limit=0, facet=name, facetLimit=limit, **f)
    return [(c["name"], c["count"]) for c in (d["facets"][0]["counts"] if d.get("facets") else [])]

rng = random.Random(20261025)
out = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "datasets": {}}
private = {}
for tag, key in SETS.items():
    d = {"datasetKey": key, "total": n(datasetKey=key),
         "absent": n(datasetKey=key, occurrenceStatus="ABSENT"), "present": n(datasetKey=key, occurrenceStatus="PRESENT")}
    FL = 100000
    ta = dict(facet("taxonKey", FL, datasetKey=key, occurrenceStatus="ABSENT"))
    tp = dict(facet("taxonKey", FL, datasetKey=key, occurrenceStatus="PRESENT"))
    d["names_absent"], d["names_present"], d["facet_limit"] = len(ta), len(tp), FL
    d["facet_capped"] = len(ta) >= FL or len(tp) >= FL
    d["names_any"] = len(set(ta) | set(tp))
    never = sorted(((k, c) for k, c in ta.items() if k not in tp), key=lambda x: -x[1])
    d["never_found_names"] = len(never)
    d["never_found_absences"] = sum(c for _, c in never)
    d["never_found_share_of_absences"] = d["never_found_absences"] / d["absent"] if d["absent"] else None
    d["never_found_sum_check"] = sum(ta.values())
    d["never_found"] = [{"taxonKey": k, "absent": c, "name": get(f"species/{k}").get("scientificName")} for k, c in never[:40]]
    d["never_found_rest"] = [[k, c] for k, c in never[40:]]
    d["protocol_facet"] = facet("samplingProtocol", 20, datasetKey=key)
    units, nounit, seen, draws = [], 0, set(), 0
    m = min(d["total"], 100000)
    while draws < 20:
        off = rng.randrange(m)
        res = get("occurrence/search", datasetKey=key, limit=1, offset=off)["results"]
        if not res:
            continue
        eid = res[0].get("eventID")
        if not eid:
            nounit += 1; draws += 1; continue
        if eid in seen:
            continue
        seen.add(eid); draws += 1
        L = n(datasetKey=key, eventId=eid)
        A = n(datasetKey=key, eventId=eid, occurrenceStatus="ABSENT")
        units.append({"eventID_sha256": hashlib.sha256(eid.encode()).hexdigest(), "offset": off, "list_length": L,
                      "absent": A, "absent_share": A / L if L else None})
        private.setdefault(tag, []).append(eid)
    d["no_unit_draws"] = nounit
    d["units"] = units
    lens = [u["list_length"] for u in units]
    if lens:
        mode, mc = Counter(lens).most_common(1)[0]
        d["list_length_mode"], d["units_at_mode"] = mode, mc
        d["list_length_min"], d["list_length_median"], d["list_length_max"] = min(lens), statistics.median(lens), max(lens)
        d["absent_share_median"] = statistics.median(u["absent_share"] for u in units)
    out["datasets"][tag] = d
D = out["datasets"]
def meas(t): return len(D[t]["units"]) >= 15
P = {}
P["P1 fixed list (>=15 of 20 units share a list length), per dataset"] = {t: (D[t]["units_at_mode"] >= 15 if meas(t) else "not measurable") for t in D}
P["P2 S median unit >= 95 % absent"] = (D["S"]["absent_share_median"] >= 0.95) if meas("S") else "not measurable"
P["P3 each holds a never-found name"] = {t: (D[t]["never_found_names"] >= 1 if not D[t]["facet_capped"] else "not measurable") for t in D}
P["P4 S never-found >= 10 % of its absences"] = (D["S"]["never_found_share_of_absences"] >= 0.10) if not D["S"]["facet_capped"] else "not measurable"
reading = {"S": "hold", "K": "fail", "F": "hold"}
agree = {t: ((P["P1 fixed list (>=15 of 20 units share a list length), per dataset"][t] is True) == (reading[t] == "hold"))
         for t in D if meas(t)}
P["P5 reading (b) agrees with P1 in >= 2 of 3"] = {"per_dataset": agree, "held": sum(agree.values()) >= 2}
out["predictions"] = P
out["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(out, open("session2.json", "w"), indent=1, ensure_ascii=False)
json.dump(LOG, open("fetch_log2.json", "w"), indent=1)
json.dump(private, open(f"{SCRATCH}/event_ids2.json", "w"), indent=1)
for t, x in D.items():
    print(t, {k: x[k] for k in x if k not in ("units", "never_found", "never_found_rest", "protocol_facet")})
    print("  lens", [u["list_length"] for u in x["units"]], "shares", [round(u["absent_share"], 3) for u in x["units"]])
    print("  protocols", x["protocol_facet"][:6])
    print("  never top", [(a["name"], a["absent"]) for a in x["never_found"][:12]])
print(json.dumps(P, indent=1))
