"""Rules of lib3 on invented rows, written before any of the 1,022 is classified."""
from lib import parse as pd
from lib2 import parse as pr
from lib3 import dclass, direction

DIR = "1 0 0 SVP {d} 00:00 10.0 20.0 2005/01/01 00:00 11.0 21.0 {o} 00:00 3"


def row(o):
    return pd(DIR.format(d="2004/01/01", o=o))


r = pr("1 2004-6-1 2004-3-1 2004-2-1")
assert dclass(r, row("1979/01/01")) == "unknown"
assert dclass(r, row("0000/00/00")) == "still_on"
assert dclass(r, row("2004/06/01")) == "original"
assert dclass(r, row("2004/06/02")) == "original"
assert dclass(r, row("2004/03/01")) == "automatic"
assert dclass(r, row("2004/09/01")) == "other"
assert dclass(r, row("2004/02/01")) == "other"  # the manual date itself; such rows agree and are not in the population
assert direction(r, row("2004/06/01"), "original") == 121  # directory counts 121 more days following than the person decided
assert direction(r, row("2004/01/01"), "other") == -31
assert direction(r, row("1979/01/01"), "unknown") is None
d = direction(r, row("0000/00/00"), "still_on")
assert d == (366 - 31), d  # still on -> the end of the window, 2005-01-01, against 2004-02-01
s = pr("2 9990-00-00 2004-3-1 1979-01-01")
assert direction(s, row("2004/06/01"), "original") is None  # manual uncertain: not comparable
print("ok")
