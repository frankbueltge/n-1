"""Session 2's structural probe (SESSION2.md, exposure): which statuses carry a 'why stopped' line. -> probe2.json"""
import json, time, urllib.parse, urllib.request
BASE = "https://clinicaltrials.gov/api/v2/studies"
def count(**q):
    q.update({"countTotal": "true", "pageSize": "1", "fields": "NCTId"})
    return json.load(urllib.request.urlopen(BASE + "?" + urllib.parse.urlencode(q), timeout=60))["totalCount"]
ver = json.load(urllib.request.urlopen("https://clinicaltrials.gov/api/v2/version", timeout=60))
term = "AREA[WhyStopped]NOT MISSING"
out = {"version": ver, "asked_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "query.term": term,
       "any_status": count(**{"query.term": term}),
       "stopped": count(**{"query.term": term, "filter.overallStatus": "TERMINATED,SUSPENDED,WITHDRAWN"})}
out["not_stopped"] = out["any_status"] - out["stopped"]
json.dump(out, open("probe2.json", "w"), indent=1)
print(out)
