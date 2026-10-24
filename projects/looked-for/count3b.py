"""Session 3, the count as run (LOG.md 19:13-19:16): count3.py, the registered script, fetched every present record of S page by page;
a page deep in the set took over two minutes, so it was stopped before it printed anything, and the same registered quantities are read
here from facets instead. Definitions are SESSION3.md's, unchanged: a box is (eventID, one of the 13 names); filled if it has a PRESENT
record. The facet eventId gives, per name, the units holding a present record of it and how many. One deviation: boxes are dated by
month only (the day facet counts records, not boxes), so the page spreads every mark evenly within its month (an estimate).
The check (seed 20261026, 20 filled forms, 20 margin units) is drawn from identifiers alone before any total is printed."""
import hashlib, json, random, time, urllib.request, urllib.parse
from collections import Counter, defaultdict

API = "https://api.gbif.org/v1/"
S = "b6b4502f-ffc8-4048-a91b-af502288faa8"
COUNTER = "11711225"
LOG = []

def h(s):
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()

def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
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

def count(**f):
    return get("occurrence/search", limit=0, **f)["count"]

s2 = json.load(open("session2b.json"))
THIRTEEN = [n["acceptedTaxonKey"] for n in s2["datasets"]["S"]["absent_names"]]
NAMES = {n["acceptedTaxonKey"]: n["name"] for n in s2["datasets"]["S"]["absent_names"]}
assert len(THIRTEEN) == 13
out = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "dataset": S, "counter_taxon": COUNTER}

# 1. forms, by year and month
fy = sorted(facet("year", 1000, datasetKey=S, acceptedTaxonKey=COUNTER))
forms_total = count(datasetKey=S, acceptedTaxonKey=COUNTER)
forms_ym = {}
for y, _ in fy:
    for m, c in facet("month", 12, datasetKey=S, acceptedTaxonKey=COUNTER, year=y):
        forms_ym[f"{int(y):04d}-{int(m):02d}"] = c
out["forms_total"] = forms_total
out["forms_by_year"] = dict(fy)
out["forms_by_month"] = dict(sorted(forms_ym.items()))
out["forms_year_facet_sum"] = sum(c for _, c in fy)
out["forms_month_facet_sum"] = sum(forms_ym.values())
allnames = dict(facet("acceptedTaxonKey", 100000, datasetKey=S))
out["thirteen_records_any_status"] = {k: allnames.get(k, 0) for k in THIRTEEN}
out["thirteen_records_sum"] = sum(out["thirteen_records_any_status"].values())
out["thirteen_times_forms"] = 13 * forms_total

# 2. units with present records, per name and in all
n_present = count(datasetKey=S, occurrenceStatus="PRESENT")
ev_all = dict(facet("eventId", 200000, datasetKey=S, occurrenceStatus="PRESENT"))
per_name = {k: dict(facet("eventId", 200000, datasetKey=S, occurrenceStatus="PRESENT", acceptedTaxonKey=k)) for k in THIRTEEN}
filled = defaultdict(set)
of13 = Counter()
for k, evs in per_name.items():
    for ev, c in evs.items():
        filled[ev].add(k)
        of13[ev] += c
margin = {ev for ev, c in ev_all.items() if c > of13.get(ev, 0)}

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
                      "names_of_13_held": sum(1 for k in THIRTEEN if k in tk),
                      "other_names": len([k for k in tk if k not in THIRTEEN])})
out["check"] = check

# 4. totals
out["present_count_index"] = n_present
out["present_in_units"] = sum(ev_all.values())
out["present_units"] = len(ev_all)
out["filled_forms"] = len(filled)
out["filled_boxes"] = sum(len(v) for v in filled.values())
out["boxes_per_filled_form"] = {str(a): b for a, b in sorted(Counter(len(v) for v in filled.values()).items())}
out["margin_units"] = len(margin)
out["margin_units_also_filled"] = len(margin & set(filled))
out["margin_records_in_units"] = sum(ev_all[ev] - of13.get(ev, 0) for ev in margin)
out["thirteen"] = [{"acceptedTaxonKey": k, "name": NAMES[k], "asked": out["thirteen_records_any_status"][k],
                    "present_records": sum(per_name[k].values()), "filled_boxes": len(per_name[k])} for k in THIRTEEN]

# 5. by month: filled boxes per name, filled forms, margin records
boxes_m, forms_m, margin_m, present_m = {}, {}, {}, {}
for ym in sorted(forms_ym):
    y, m = int(ym[:4]), int(ym[5:])
    pc = count(datasetKey=S, occurrenceStatus="PRESENT", year=y, month=m)
    present_m[ym] = pc
    if pc == 0:
        continue
    names_m = dict(facet("acceptedTaxonKey", 100000, datasetKey=S, occurrenceStatus="PRESENT", year=y, month=m))
    r13 = sum(names_m.get(k, 0) for k in THIRTEEN)
    margin_m[ym] = pc - r13
    if r13 == 0:
        continue
    row = []
    evs_m = set()
    for i, k in enumerate(THIRTEEN):
        if names_m.get(k, 0):
            e = dict(facet("eventId", 100000, datasetKey=S, occurrenceStatus="PRESENT", acceptedTaxonKey=k, year=y, month=m))
            row.append([i, len(e)])
            evs_m |= set(e)
    boxes_m[ym] = row
    forms_m[ym] = len(evs_m)
out["present_by_month"] = present_m
out["present_dated_sum"] = sum(present_m.values())
out["filled_boxes_by_month"] = boxes_m
out["filled_forms_by_month"] = forms_m
out["filled_forms_dated_sum"] = sum(forms_m.values())
out["margin_records_by_month"] = margin_m
fyf = Counter()
for ym, c in forms_m.items():
    fyf[ym[:4]] += c
shares = {y: fyf.get(y, 0) / c for y, c in fy if c >= 10000}
out["filled_share_by_year_10000"] = shares

P = {}
P["P1 forms span >= 10 years"] = len(fy) >= 10
P["P2 filled forms <= 0.5 % of forms"] = len(filled) <= 0.005 * forms_total
P["P3 >= 18 of 20 filled forms hold all 13"] = sum(1 for c in check if c["kind"] == "filled" and c["names_of_13_held"] == 13) >= 18
P["P4 >= 18 of 20 margin units hold all 13"] = sum(1 for c in check if c["kind"] == "margin" and c["names_of_13_held"] == 13) >= 18
lo, hi = (min(shares.values()), max(shares.values())) if shares else (None, None)
P["P5 filled share max/min >= 10 (years >= 10,000 forms)"] = bool(shares) and ((lo == 0 and hi > 0) or (lo > 0 and hi / lo >= 10))
P["P6 no form has more than 3 filled"] = max((len(v) for v in filled.values()), default=0) <= 3
out["predictions"] = P
out["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(out, open("session3.json", "w"), indent=1, ensure_ascii=False)
json.dump(LOG, open("fetch_log3.json", "w"), indent=1)
print(json.dumps(P, indent=1))
