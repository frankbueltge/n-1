"""A minimal stdlib reader for .xlsx sheets: yields rows as lists of strings/numbers.

Reads shared strings and inline strings; numbers come back as floats or the raw text.
No styles are read, so date cells come back as Excel serial numbers (days since 1899-12-30).
"""
import re
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def _col(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def sheets(path):
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = []
    for s in wb.find("m:sheets", NS):
        t = target[s.get(RID)]
        t = t.lstrip("/")
        if not t.startswith("xl/"):
            t = "xl/" + t
        out.append((s.get("name"), t))
    return out


def rows(path, sheet_name=None):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(x.text or "" for x in si.iter("{%s}t" % NS["m"])))
    for name, part in sheets(path):
        if sheet_name is not None and name != sheet_name:
            continue
        with z.open(part) as f:
            for ev, el in ET.iterparse(f):
                if el.tag != "{%s}row" % NS["m"]:
                    continue
                vals = {}
                for c in el.findall("m:c", NS):
                    t = c.get("t")
                    v = c.find("m:v", NS)
                    if t == "s" and v is not None:
                        val = shared[int(v.text)]
                    elif t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                    elif v is not None:
                        val = v.text
                        try:
                            val = float(val)
                        except (TypeError, ValueError):
                            pass
                    else:
                        val = None
                    vals[_col(c.get("r"))] = val
                el.clear()
                if vals:
                    width = max(vals) + 1
                    yield name, [vals.get(i) for i in range(width)]
