"""Rules on invented rows, written before the files are parsed."""
from lib import parse, status, days

ROW = "  {id}  0  1  SVP  2010/01/01 00:00  10.00  200.00 2010/12/31 00:00  12.00  210.00 {dg} {death}"


def row(dg, death=3, i=1):
    return parse(ROW.format(id=i, dg=dg, death=death))


assert parse("1 2 3") is None
assert status(row("2010/06/01 00:00")) == "lost"
assert status(row("2010/01/01 00:00")) == "never"
assert status(row("2010/12/31 00:00")) == "kept"
assert status(row("2011/02/01 00:00")) == "kept"
assert status(row("1979/01/01 00:00")) == "unknown"
assert status(row("0000/00/00 00:00", death=0)) == "alive_drogued"
assert status(row("0000/00/00 00:00", death=3)) == "unknown"
g, c = days(row("2010/01/11 00:00"))
assert abs(g - 10) < 1e-9 and abs(c - 354) < 1e-9
assert days(row("1979/01/01 00:00")) is None
assert days(row("2010/01/01 00:00")) == (0.0, 364.0)
print("ok")
