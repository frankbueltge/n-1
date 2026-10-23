"""Session 3: as fetch.py with Condition (the conditions list) added. Fetch every stopped study (terminated, suspended, withdrawn) from ClinicalTrials.gov API v2 to scratch.

Usage: python3 fetch.py OUTDIR. Writes page_NNN.json and fetch_log.json (hashes, timestamp) to OUTDIR.
"""
import hashlib, json, sys, time, urllib.parse, urllib.request

BASE = "https://clinicaltrials.gov/api/v2/studies"
FIELDS = ["NCTId", "OverallStatus", "WhyStopped", "StudyType", "StartDate", "PrimaryCompletionDate", "PrimaryCompletionDateType",
          "CompletionDate", "CompletionDateType", "LastUpdatePostDate", "Condition"]

def main(out):
    ver = json.load(urllib.request.urlopen("https://clinicaltrials.gov/api/v2/version", timeout=60))
    token, n, log = None, 0, {"version": ver, "fields": FIELDS, "pages": []}
    while True:
        q = {"filter.overallStatus": "TERMINATED,SUSPENDED,WITHDRAWN", "pageSize": "1000",
             "fields": ",".join(FIELDS), "countTotal": "true"}
        if token:
            q["pageToken"] = token
        url = BASE + "?" + urllib.parse.urlencode(q)
        for attempt in range(5):
            try:
                raw = urllib.request.urlopen(url, timeout=120).read()
                break
            except Exception as e:
                time.sleep(2 ** attempt)
        else:
            raise SystemExit("fetch failed at page %d" % n)
        d = json.loads(raw)
        path = "%s/page_%03d.json" % (out, n)
        open(path, "wb").write(raw)
        log["pages"].append({"n": n, "sha256": hashlib.sha256(raw).hexdigest(), "studies": len(d.get("studies", []))})
        if n == 0:
            log["totalCount"] = d.get("totalCount")
        token = d.get("nextPageToken")
        n += 1
        if not token:
            break
        time.sleep(0.5)
    log["fetched_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    json.dump(log, open(out + "/fetch_log.json", "w"), indent=1)
    print(log["totalCount"], sum(p["studies"] for p in log["pages"]), len(log["pages"]))

if __name__ == "__main__":
    main(sys.argv[1])
