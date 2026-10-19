"""Fetch the January 2013 Lichess file to scratch and check it against the publisher's checksum."""
import hashlib, json, os, sys, urllib.request

URL = "https://database.lichess.org/standard/lichess_db_standard_rated_2013-01.pgn.zst"
SUMS = "https://database.lichess.org/standard/sha256sums.txt"
out = sys.argv[1]
if not os.path.exists(out):
    urllib.request.urlretrieve(URL, out)
h = hashlib.sha256(open(out, "rb").read()).hexdigest()
pub = [l.split()[0] for l in urllib.request.urlopen(SUMS).read().decode().splitlines() if l.endswith(os.path.basename(URL))][0]
log = {"url": URL, "bytes": os.path.getsize(out), "sha256": h, "publisher_sha256": pub, "equal": h == pub, "fetched": "2026-10-19"}
json.dump(log, open(os.path.join(os.path.dirname(__file__), "fetch_log.json"), "w"), indent=1)
print(log)
