"""Parse GDP dirfl rows and classify drogue status, as defined in SELECTION.md."""
from datetime import datetime

FIELDS = ["id", "wmo", "program", "type", "start_d", "start_t", "start_lat", "start_lon",
          "end_d", "end_t", "end_lat", "end_lon", "drogue_d", "drogue_t", "death"]


def dt(d, t):
    try:
        return datetime.strptime(d + " " + t, "%Y/%m/%d %H:%M")
    except ValueError:
        return None


def parse(line):
    p = line.split()
    if len(p) != 15:
        return None
    r = dict(zip(FIELDS, p))
    r["start"] = dt(r["start_d"], r["start_t"])
    r["end"] = dt(r["end_d"], r["end_t"])
    r["drogue"] = dt(r["drogue_d"], r["drogue_t"])
    r["death"] = int(r["death"])
    for k in ("start_lat", "start_lon", "end_lat", "end_lon"):
        r[k] = float(r[k])
    return r


def zero_date(d):
    return d.replace("/", "").strip("0") == ""


def status(r):
    d = r["drogue_d"]
    if zero_date(d):
        return "alive_drogued" if r["death"] == 0 else "unknown"
    if d.startswith("1979/01/01") or r["drogue"] is None:
        return "unknown"
    if r["drogue"] <= r["start"]:
        return "never"
    if r["drogue"] >= r["end"]:
        return "kept"
    return "lost"


def days(r):
    """(drogued days, carried days) for known statuses, else None."""
    s = status(r)
    if s == "unknown" or r["start"] is None or r["end"] is None:
        return None
    total = (r["end"] - r["start"]).total_seconds() / 86400
    if s in ("alive_drogued", "kept"):
        return total, 0.0
    if s == "never":
        return 0.0, total
    g = (r["drogue"] - r["start"]).total_seconds() / 86400
    return g, total - g
