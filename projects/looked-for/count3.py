"""Session 3, the registered count (SESSION3.md, committed a6c1466 before any record or count was read).
Forms counted by the one name written once per unit; every PRESENT record of S fetched to scratch; the check (20 filled forms, 20 margin
units, seed 20261026) drawn from identifiers alone and asked before any total of the present records is printed."""
import hashlib, json, os, random, sys, time, urllib.request, urllib.parse
from collections import Counter, defaultdict

API = "https://api.gbif.org/v1/"
S = "b6b4502f-ffc8-4048-a91b-af502288faa8"
COUNTER = "11711225"  # Callistephanus pallida, the name with most absences, never present (session2b.json)
SCRATCH = sys.argv[1]
LOG = []

def h(s):
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()

def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                body = r.read()
            logurl = url
            if "eventId" in params:
                logurl = logurl.replace(urllib.parse.quote_plus(params["eventId"]), h(params["eventId"]))
            LOG.append({"url": logurl, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "sha256": hashlib.sha256(body).hexdigest()})
            return json.loads(body)
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError(url)

def facet(name, limit, **f):
    d = get("occurrence/search", limit=0, facet=name, facetLimit=limit, **f)
    return [(c["name"], c["count"]) for c in (d["facets"][0]["counts"] if d.get("facets") else [])]

s2 = json.load(open("session2b.json"))
THIRTEEN = [n["acceptedTaxonKey"] for n in s2["datasets"]["S"]["absent_names"]]
NAMES = {n["acceptedTaxonKey"]: n["name"] for n in s2["datasets"]["S"]["absent_names"]}
assert len(THIRTEEN) == 13
out = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "dataset": S, "counter_taxon": COUNTER}

# 1. forms, by year and month
fy = facet("year", 1000, datasetKey=S, acceptedTaxonKey=COUNTER)
forms_total = get("occurrence/search", limit=0, datasetKey=S, acceptedTaxonKey=COUNTER)["count"]
forms_ym = {}
for y, _ in sorted(fy):
    for m, c in facet("month", 12, datasetKey=S, acceptedTaxonKey=COUNTER, year=y):
        forms_ym[f"{int(y):04d}-{int(m):02d}"] = c
out["forms_total"] = forms_total
out["forms_by_year"] = {y: c for y, c in sorted(fy)}
out["forms_by_month"] = dict(sorted(forms_ym.items()))
out["forms_year_facet_sum"] = sum(c for _, c in fy)
out["forms_month_facet_sum"] = sum(forms_ym.values())
allnames = dict(facet("acceptedTaxonKey", 100000, datasetKey=S))
out["thirteen_records_any_status"] = {k: allnames.get(k, 0) for k in THIRTEEN}
out["thirteen_records_sum"] = sum(out["thirteen_records_any_status"].values())
out["thirteen_times_forms"] = 13 * forms_total

# 2. every present record of S, to scratch
n_present = get("occurrence/search", limit=0, datasetKey=S, occurrenceStatus="PRESENT")["count"]
recs, off = [], 0
while off < n_present:
    d = get("occurrence/search", limit=300, offset=off, datasetKey=S, occurrenceStatus="PRESENT")
    for r in d["results"]:
        recs.append({k: r.get(k) for k in ("key", "eventID", "eventDate", "year", "month", "day", "acceptedTaxonKey", "taxonRank")})
    if not d["results"]:
        break
    off += 300
json.dump(recs, open(os.path.join(SCRATCH, "present3.json"), "w"))
assert len({r["key"] for r in recs}) == len(recs), "duplicate keys across pages"

filled = defaultdict(set)   # eventID -> names filled
margin = set()
for r in recs:
    ev = r["eventID"]
    if ev is None:
        continue
    k = str(r["acceptedTaxonKey"]) if r["acceptedTaxonKey"] is not None else None
    if k in THIRTEEN:
        filled[ev].add(k)
    else:
        margin.add(ev)

# 3. the check, drawn from identifiers alone, before any total is printed
rng = random.Random(20261026)
fs = rng.sample(sorted(filled), 20)
ms = rng.sample(sorted(margin), 20)
check = []
for kind, evs in (("filled", fs), ("margin", ms)):
    for ev in evs:
        tk = dict(facet("acceptedTaxonKey", 1000, datasetKey=S, eventId=ev))
        st = dict(facet("occurrenceStatus", 10, datasetKey=S, eventId=ev))
        check.append({"kind": kind, "event": h(ev), "records": sum(st.values()), "by_status": st,
                      "names_of_13_held": sum(1 for k in THIRTEEN if k in tk), "other_names": len([k for k in tk if k not in THIRTEEN])})
out["check"] = check

# 4. totals
out["present_records_fetched"] = len(recs)
out["present_count_index"] = n_present
out["present_without_event"] = sum(1 for r in recs if r["eventID"] is None)
out["filled_forms"] = len(filled)
out["filled_boxes"] = sum(len(v) for v in filled.values())
out["boxes_per_filled_form"] = dict(sorted(Counter(len(v) for v in filled.values()).items()))
out["margin_units"] = len(margin)
out["margin_units_also_filled"] = len(margin & set(filled))
pres13 = Counter(); boxes13 = Counter()
for r in recs:
    k = str(r["acceptedTaxonKey"]) if r["acceptedTaxonKey"] is not None else None
    if k in THIRTEEN:
        pres13[k] += 1
for ev, ks in filled.items():
    for k in ks:
        boxes13[k] += 1
out["thirteen"] = [{"acceptedTaxonKey": k, "name": NAMES[k], "asked": out["thirteen_records_any_status"][k],
                    "present_records": pres13[k], "filled_boxes": boxes13[k]} for k in THIRTEEN]
# filled boxes by date (one box counted on the date of its first present record), margin records by month
first = {}
for r in recs:
    ev = r["eventID"]; k = str(r["acceptedTaxonKey"]) if r["acceptedTaxonKey"] is not None else None
    if ev is None or k not in THIRTEEN:
        continue
    d = (r["year"] or 0, r["month"] or 0, r["day"] or 0)
    if (ev, k) not in first or d < first[(ev, k)]:
        first[(ev, k)] = d
bd = Counter((y, m, dd, THIRTEEN.index(k)) for (ev, k), (y, m, dd) in first.items())
out["filled_boxes_by_day"] = [[y, m, dd, i, c] for (y, m, dd, i), c in sorted(bd.items())]
fm = Counter()
for ev, ks in filled.items():
    d = min(first[(ev, k)] for k in ks)
    fm[f"{d[0]:04d}-{d[1]:02d}"] += 1
out["filled_forms_by_month"] = dict(sorted(fm.items()))
mm = Counter(f"{(r['year'] or 0):04d}-{(r['month'] or 0):02d}" for r in recs
             if not (r["acceptedTaxonKey"] is not None and str(r["acceptedTaxonKey"]) in THIRTEEN))
out["margin_records_by_month"] = dict(sorted(mm.items()))
out["margin_records"] = sum(mm.values())
fy_filled = Counter()
for k, c in fm.items():
    fy_filled[k[:4]] += c
shares = {y: fy_filled.get(f"{int(y):04d}", 0) / c for y, c in fy if c >= 10000}
out["filled_share_by_year_10000"] = shares

P = {}
P["P1 forms span >= 10 years"] = len(fy) >= 10
P["P2 filled forms <= 0.5 % of forms"] = len(filled) <= 0.005 * forms_total
P["P3 >= 18 of 20 filled forms hold all 13"] = sum(1 for c in check if c["kind"] == "filled" and c["names_of_13_held"] == 13) >= 18
P["P4 >= 18 of 20 margin units hold all 13"] = sum(1 for c in check if c["kind"] == "margin" and c["names_of_13_held"] == 13) >= 18
lo = min(shares.values()) if shares else None
hi = max(shares.values()) if shares else None
P["P5 filled share max/min >= 10 (years >= 10,000 forms)"] = (lo == 0 and hi > 0) or (lo is not None and lo > 0 and hi / lo >= 10)
P["P6 no form has more than 3 filled"] = max((len(v) for v in filled.values()), default=0) <= 3
out["predictions"] = P
out["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(out, open("session3.json", "w"), indent=1, ensure_ascii=False)
json.dump(LOG, open("fetch_log3.json", "w"), indent=1)
print(json.dumps(P, indent=1))
