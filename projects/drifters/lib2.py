"""Session 2: parse the drogue re-estimation file and compare its dates, as defined in SESSION2.md."""
from datetime import datetime

STUDY_END = datetime(2010, 11, 19)
SPECIAL = {"9990": "still_on", "9999": "not_reassessed", "9998": "unclear",
           "NNNN": "none"}  # added after the registered run: 15 rows carry no automatic date (verified correction)


def value(s):
    """A date field -> datetime, or one of 'still_on', 'uncertain', 'not_reassessed', 'unclear', 'bad'."""
    p = s.split("-")
    if len(p) != 3:
        return "bad"
    if p[0] in SPECIAL:
        return SPECIAL[p[0]]
    try:
        d = datetime(int(p[0]), int(p[1]), int(p[2]))
    except ValueError:
        return "bad"
    return "uncertain" if d == datetime(1979, 1, 1) else d


def parse(line):
    p = line.split()
    if len(p) != 4 or not p[0].isdigit():
        return None
    return {"id": p[0], "orig": value(p[1]), "auto": value(p[2]), "manual": value(p[3]),
            "raw": p[1:]}


def effective(v, start, end):
    """Effective date in the window [start, T], T = min(end, STUDY_END); None if not comparable."""
    t = min(end, STUDY_END)
    if v == "still_on":
        return t
    if isinstance(v, datetime):
        return max(start, min(v, t))
    return None


def shift(orig, manual, start, end):
    a, b = effective(orig, start, end), effective(manual, start, end)
    if a is None or b is None:
        return None
    return (a - b).total_seconds() / 86400


def klass(s):
    if s is None:
        return "not_comparable"
    return "earlier" if s > 1 else ("later" if s < -1 else "held")


def agrees(manual, dir_drogue, dir_drogue_zero, end):
    """Does the current directory carry the manual decision? None if manual is not a date or 9990."""
    t = min(end, STUDY_END)
    if manual == "still_on":
        if dir_drogue_zero:
            return True
        return dir_drogue is not None and (dir_drogue - t).total_seconds() / 86400 >= -1
    if isinstance(manual, datetime):
        return dir_drogue is not None and abs((dir_drogue - manual).total_seconds()) / 86400 <= 1
    return None
