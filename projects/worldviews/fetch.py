"""Fetch Natural Earth 10m admin-0 countries: the default (de facto) edition and its point-of-view editions.

Files go to a scratch directory given as the first argument; fetch_log.json records url, size and sha256.
Natural Earth is in the public domain (https://www.naturalearthdata.com/about/terms-of-use/).
"""
import hashlib, json, sys, time, urllib.request, zipfile, os

BASE = "https://naciscdn.org/naturalearth/10m/cultural/"
POVS = ["arg", "bdg", "bra", "chn", "deu", "egy", "esp", "fra", "gbr", "grc", "idn", "ind", "iso", "isr", "ita",
        "jpn", "kor", "mar", "nep", "nld", "pak", "pol", "prt", "pse", "rus", "sau", "swe", "tlc", "tur", "twn",
        "ukr", "usa", "vnm"]
NAMES = ["ne_10m_admin_0_countries"] + ["ne_10m_admin_0_countries_" + p for p in POVS]


def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def main(out):
    os.makedirs(out, exist_ok=True)
    log = []
    for n in NAMES:
        url = BASE + n + ".zip"
        b = get(url)
        p = os.path.join(out, n + ".zip")
        open(p, "wb").write(b)
        with zipfile.ZipFile(p) as z:
            z.extractall(os.path.join(out, n))
        log.append({"name": n, "url": url, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                    "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        print(n, len(b))
    json.dump(log, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetch_log.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
