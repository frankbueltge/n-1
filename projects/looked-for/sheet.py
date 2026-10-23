"""Draw the check's 40 records (20 ABSENT, 20 PRESENT), as registered in SELECTION.md.

Writes, to the scratch directory given as argv[1]:
  sheet_text.txt   the publisher's fields only, shuffled, for reading (never committed)
  key.json         occurrence key, dataset key, interpreted status, issues (not opened until readings are committed)
and, to this directory:
  sheet.json       item number, sha256 of each item's shown text (no text)
Prints nothing about counts.
"""
import hashlib, json, random, sys, time, urllib.request, urllib.parse

API = "https://api.gbif.org/v1/occurrence/"
SHOW = ["occurrenceStatus", "individualCount", "organismQuantity", "organismQuantityType",
        "sampleSizeValue", "sampleSizeUnit", "samplingProtocol", "occurrenceRemarks", "scientificName"]
LOG = []

def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                body = r.read()
            LOG.append({"url": url, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "sha256": hashlib.sha256(body).hexdigest()})
            return json.loads(body)
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError(url)

def draw(status, n, rng):
    facets = get("search", occurrenceStatus=status, limit=0, facet="datasetKey", facetLimit=200000)
    counts = facets["facets"][0]["counts"] if facets.get("facets") else []
    keys = [c["name"] for c in counts]
    weights = [c["count"] for c in counts]
    out = []
    while len(out) < n:
        ds = rng.choices(keys, weights=weights)[0]
        m = min(weights[keys.index(ds)], 100000)
        off = rng.randrange(m)
        res = get("search", datasetKey=ds, occurrenceStatus=status, limit=1, offset=off)["results"]
        if not res:
            continue
        rec = res[0]
        verb = get(f"{rec['key']}/verbatim")
        shown = {}
        for k, v in verb.items():
            term = k.rsplit("/", 1)[-1]
            if term in SHOW and str(v).strip():
                shown[term] = str(v)
        out.append({"key": rec["key"], "datasetKey": ds, "status": rec.get("occurrenceStatus"),
                    "issues": rec.get("issues", []), "offset": off, "shown": shown})
    return out

def main():
    scratch = sys.argv[1]
    rng = random.Random(20261024)
    items = draw("ABSENT", 20, rng) + draw("PRESENT", 20, rng)
    rng.shuffle(items)
    lines, sheet, key = [], [], []
    for i, it in enumerate(items, 1):
        text = "\n".join(f"  {t}: {it['shown'][t]}" for t in SHOW if t in it["shown"]) or "  (no shown field)"
        lines.append(f"[{i}]\n{text}\n")
        sheet.append({"item": i, "sha256": hashlib.sha256(text.encode()).hexdigest(), "fields": sorted(it["shown"])})
        key.append({"item": i, "key": it["key"], "datasetKey": it["datasetKey"], "status": it["status"],
                    "issues": it["issues"], "offset": it["offset"]})
    open(f"{scratch}/sheet_text.txt", "w").write("\n".join(lines))
    json.dump(key, open(f"{scratch}/key.json", "w"), indent=1)
    json.dump({"seed": 20261024, "items": sheet}, open("projects/looked-for/sheet.json", "w"), indent=1)
    json.dump(LOG, open(f"{scratch}/sheet_fetch_log.json", "w"), indent=1)
    print("sheet written:", len(items), "items")

main()
