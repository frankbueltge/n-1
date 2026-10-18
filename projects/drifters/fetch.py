"""Fetch the four GDP drifter directory files to scratch; log size, rows, sha256."""
import hashlib, json, os, sys, time, urllib.request

BASE = "https://www.aoml.noaa.gov/ftp/pub/phod/buoydata/"
FILES = ["dirfl_1_5000.dat", "dirfl_5001_10000.dat", "dirfl_10001_15000.dat", "dirfl_15001_current.dat"]


def main(out):
    os.makedirs(out, exist_ok=True)
    log = {"fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "files": []}
    for f in FILES:
        for attempt in range(6):  # retries added in session 3: the host reset connections
            try:
                data = urllib.request.urlopen(BASE + f, timeout=120).read()
                break
            except OSError:
                if attempt == 5:
                    raise
                time.sleep(10 * (attempt + 1))
        open(os.path.join(out, f), "wb").write(data)
        log["files"].append({"file": f, "url": BASE + f, "bytes": len(data),
                             "rows": data.count(b"\n"), "sha256": hashlib.sha256(data).hexdigest()})
        time.sleep(2)
    json.dump(log, open("fetch_log.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
