"""Project 18, session 3: the live check (SESSION3.md). For the 20 releases count3.py drew from R (seed 20261026), asks
MusicBrainz's web service for each release's media and disc IDs and compares them, position by position, with the dump's;
a 503 is asked again once after 5 s, as registered. Writes check3.json and fetch_log3.json.
Usage: python3 -I check3.py session3.json
"""
import hashlib, json, sys, time, urllib.request

UA = "n-1 research practice (https://github.com/frankbueltge/n-1; remainder@n-1.invalid)"

def ask(url, log):
    t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        body = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
        status = 200
    except urllib.error.HTTPError as e:
        body, status = e.read(), e.code
    log.append({"url": url, "clock": t, "status": status, "sha256": hashlib.sha256(body).hexdigest()})
    return status, body

def main(path):
    draw = json.load(open(path))["check_draw"]
    log, out = [], []
    for d in draw:
        url = "https://musicbrainz.org/ws/2/release/%s?inc=discids&fmt=json" % d["release"]
        status, body = ask(url, log)
        if status == 503:
            time.sleep(5)
            status, body = ask(url, log)
        rec = {"release": d["release"], "status": status, "dump": d["media"]}
        if status == 200:
            live = [{"position": m["position"], "discids": sorted(x["id"] for x in m.get("discs", []))}
                    for m in sorted(json.loads(body).get("media", []), key=lambda m: m["position"])]
            rec["live"] = live
            rec["agree"] = live == d["media"]
        out.append(rec)
        time.sleep(1.5)
    res = {"seed": 20261026, "agree": sum(1 for r in out if r.get("agree")),
           "answered": sum(1 for r in out if r["status"] == 200), "rows": out}
    json.dump(res, open("check3.json", "w"), indent=1)
    json.dump(log, open("fetch_log3.json", "w"), indent=1)
    print(res["answered"], res["agree"])

if __name__ == "__main__":
    main(sys.argv[1])
