"""The dating rule of project 16 session 2 (SESSION2.md): the months a stated reason names, and the line's month (the latest)."""
import re

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10,
          "nov": 11, "dec": 12}
NAMES = (r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept(?:ember)?|sep|oct(?:ober)?|"
         r"nov(?:ember)?|dec(?:ember)?)")
YEAR = r"(20[0-2]\d)"
# (a) month name, optional full stop, optional day (with optional ordinal suffix) and/or comma, then a year
NAMED = re.compile(r"\b" + NAMES + r"\.?\s*(?:\d{1,2}(?:st|nd|rd|th)?\s*)?,?\s*" + YEAR + r"\b", re.I)
# (b) numeric forms
ISO = re.compile(r"\b" + YEAR + r"-(\d{1,2})-(\d{1,2})\b")
DMY = re.compile(r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-]" + YEAR + r"\b")
MY = re.compile(r"(?<![\d/.\-])(\d{1,2})[/.]" + YEAR + r"\b")
YEAR_ONLY = re.compile(r"\b" + YEAR + r"\b")

def stated_months(text):
    out = []
    for m in NAMED.finditer(text):
        out.append((int(m.group(2)), MONTHS[m.group(1).lower()[:3]]))
    for m in ISO.finditer(text):
        mo = int(m.group(2))
        if 1 <= mo <= 12:
            out.append((int(m.group(1)), mo))
    for m in DMY.finditer(text):
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        cands = [x for x, other in ((b, a), (a, b)) if 1 <= x <= 12 and 1 <= other <= 31]
        if cands:
            out.append((y, min(cands)))  # ambiguity never makes a line look later
    for m in MY.finditer(text):
        mo = int(m.group(1))
        if 1 <= mo <= 12:
            out.append((int(m.group(2)), mo))
    return sorted(set(out))

def line_month(text):
    """'YYYY-MM' of the latest stated month, or None."""
    ms = stated_months(text)
    return "%04d-%02d" % ms[-1] if ms else None

def year_only(text):
    return line_month(text) is None and bool(YEAR_ONLY.search(text))
