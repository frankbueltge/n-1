"""Session 3: what today's directory says for the re-worked drifters it disagrees with, as defined in SESSION3.md."""
from datetime import datetime
from lib import zero_date
from lib2 import effective


def near(a, b):
    return isinstance(a, datetime) and isinstance(b, datetime) and abs((a - b).total_seconds()) / 86400 <= 1


def dclass(r, x):
    """r: a parsed re-dating row (lib2.parse); x: its directory row (lib.parse). Classes in SESSION3.md's order."""
    d = x["drogue"]
    if x["drogue_d"].startswith("1979/01/01"):
        return "unknown"
    if zero_date(x["drogue_d"]):
        return "still_on"
    if d is None:
        return "unknown"
    if near(r["orig"], d):
        return "original"
    if near(r["auto"], d):
        return "automatic"
    return "other"


def direction(r, x, k):
    """effective(D) - effective(MANUAL), days; positive = the directory counts more following. None if not comparable."""
    if k == "unknown":
        return None
    a = effective("still_on" if k == "still_on" else x["drogue"], x["start"], x["end"])
    b = effective(r["manual"], x["start"], x["end"])
    if a is None or b is None:
        return None
    return (a - b).total_seconds() / 86400
