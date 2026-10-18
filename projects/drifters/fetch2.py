"""Session 2: fetch the drogue re-estimation files (newest and archive) and the .old directory file to scratch; log them."""
import hashlib, json, os, sys, time, urllib.request

DD = "https://www.aoml.noaa.gov/ftp/phod/lumpkin/droguedetect/"
ARCHIVE = ["2012_02_17", "2012_04_02", "2012_04_13", "2012_04_27", "2012_05_17", "2012_06_07", "2012_06_20", "2012_06_22",
           "2012_06_29", "2012_07_13", "2012_07_27", "2012_08_31", "2012_10_19", "2012_11_15", "2013_02_14", "2013_03_05"]
URLS = ([DD + "2013_06_30_drogueoff.dat", DD + "2013_04_16_drogueoff.dat"]
        + [DD + "archive/" + a + "_drogueoff.dat" for a in ARCHIVE]
        + ["https://www.aoml.noaa.gov/ftp/pub/phod/buoydata/dirfl_10001_15000.old"])


def main(out):
    os.makedirs(out, exist_ok=True)
    log = {"fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "files": []}
    for u in URLS:
        for attempt in range(4):
            try:
                data = urllib.request.urlopen(u, timeout=120).read()
                break
            except OSError:
                if attempt == 3:
                    raise
                time.sleep(5 * (attempt + 1))
        f = u.rsplit("/", 1)[1]
        open(os.path.join(out, f), "wb").write(data)
        log["files"].append({"file": f, "url": u, "bytes": len(data), "rows": data.count(b"\n"),
                             "sha256": hashlib.sha256(data).hexdigest()})
        time.sleep(1)
    json.dump(log, open("fetch2_log.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
