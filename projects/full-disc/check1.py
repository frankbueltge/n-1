"""Project 18, session 1: the live check (SELECTION.md). Draws 20 rows of the parsed cdtoc table with seed 20261025 and asks
MusicBrainz's web service for each disc ID's sectors and offsets; writes check1.json and fetch_log.json.
Usage: python3 -I check1.py <path to mbdump/cdtoc>
"""
import hashlib, json, random, sys, time, urllib.request

UA = "n-1 research practice (https://github.com/frankbueltge/n-1; remainder@n-1.invalid)"

def main(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) == 7:
            rows.append((f[1], int(f[3]), int(f[4]), [int(x) for x in f[5].strip("{}").split(",")]))
    rnd = random.Random(20261025)
    drawn = rnd.sample(rows, 20)
    log, out = [], []
    for discid, tc, leadout, offs in drawn:
        url = "https://musicbrainz.org/ws/2/discid/%s?fmt=json&cdstubs=no" % discid
        t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        try:
            body = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
            status = 200
        except urllib.error.HTTPError as e:
            body, status = e.read(), e.code
        log.append({"url": url, "clock": t, "status": status, "sha256": hashlib.sha256(body).hexdigest()})
        rec = {"discid": discid, "dump_leadout": leadout, "dump_offsets": offs, "status": status}
        if status == 200:
            j = json.loads(body)
            rec["live_sectors"] = j.get("sectors")
            rec["live_offsets"] = j.get("offsets")
            rec["agree"] = j.get("sectors") == leadout and j.get("offsets") == offs
        out.append(rec)
        time.sleep(1.1)
    res = {"seed": 20261025, "population": len(rows), "agree": sum(1 for r in out if r.get("agree")),
           "answered": sum(1 for r in out if r["status"] == 200), "rows": out}
    json.dump(res, open("check1.json", "w"), indent=1)
    json.dump(log, open("fetch_log.json", "w"), indent=1)
    print(res["population"], res["answered"], res["agree"])

if __name__ == "__main__":
    main(sys.argv[1])
