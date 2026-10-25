"""Project 18, session 2: the live check (SESSION2.md). For the 20 discs count2.py drew from bands A74 and B80 (seed 20261025),
asks MusicBrainz's web service which releases each disc ID is attached to and compares the sets with the dump's; writes
check2.json and fetch_log2.json.
Usage: python3 -I check2.py session2.json
"""
import hashlib, json, sys, time, urllib.request

UA = "n-1 research practice (https://github.com/frankbueltge/n-1; remainder@n-1.invalid)"

def main(path):
    draw = json.load(open(path))["check_draw"]
    log, out = [], []
    for d in draw:
        url = "https://musicbrainz.org/ws/2/discid/%s?fmt=json&cdstubs=no" % d["discid"]
        t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        try:
            body = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
            status = 200
        except urllib.error.HTTPError as e:
            body, status = e.read(), e.code
        log.append({"url": url, "clock": t, "status": status, "sha256": hashlib.sha256(body).hexdigest()})
        rec = {"discid": d["discid"], "band": d["band"], "dump_releases": d["releases"], "status": status}
        if status == 200:
            live = sorted(r["id"] for r in json.loads(body).get("releases", []))
            rec["live_releases"] = live
            rec["agree"] = live == d["releases"]
        out.append(rec)
        time.sleep(1.1)
    res = {"seed": 20261025, "agree": sum(1 for r in out if r.get("agree")),
           "answered": sum(1 for r in out if r["status"] == 200), "rows": out}
    json.dump(res, open("check2.json", "w"), indent=1)
    json.dump(log, open("fetch_log2.json", "w"), indent=1)
    print(res["answered"], res["agree"])

if __name__ == "__main__":
    main(sys.argv[1])
