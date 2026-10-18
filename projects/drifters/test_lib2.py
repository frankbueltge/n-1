"""Rules of lib2 on invented rows, written before parsing the real file."""
from datetime import datetime as D
from lib2 import parse, value, effective, shift, klass, agrees

assert parse(" ID  ORIGINAL AUTOMATIC MANUAL") is None
r = parse(" 1831\t2001-08-20\t2001-01-11\t  2001-01-09\t")
assert r["id"] == "1831" and r["orig"] == D(2001, 8, 20) and r["manual"] == D(2001, 1, 9)
assert value("1979-1-1") == "uncertain" and value("1979-01-01") == "uncertain"
assert value("9990-00-00") == "still_on" and value("9999-00-00") == "not_reassessed" and value("9998-00-00") == "unclear"
assert value("2001-02-30") == "bad"
s, e = D(2000, 1, 1), D(2012, 1, 1)
assert effective("still_on", s, e) == D(2010, 11, 19)
assert effective(D(1999, 1, 1), s, e) == s
assert effective("unclear", s, e) is None
assert shift(D(2001, 8, 20), D(2001, 1, 9), s, e) == 223
assert shift("still_on", D(2010, 11, 9), s, e) == 10
assert klass(223) == "earlier" and klass(-5) == "later" and klass(0.5) == "held" and klass(None) == "not_comparable"
assert agrees(D(2001, 1, 9), D(2001, 1, 10), False, e) is True
assert agrees(D(2001, 1, 9), D(2001, 1, 12), False, e) is False
assert agrees("still_on", None, True, e) is True
assert agrees("still_on", D(2010, 11, 18, 12), False, e) is True
assert agrees("unclear", None, True, e) is None
assert value("NNNN-NN-NN") == "none"
print("ok")
