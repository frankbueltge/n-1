"""Project 27, session 1: follow every bridge's lowest condition code through the yearly NBI files.

Usage: python3 count1.py DIR STATE FIRST LAST OUT.json PER.json.gz
  DIR holds the files {STATE}{YY}.txt for the years FIRST..LAST (fixed width, positions from
  https://www.fhwa.dot.gov/bridge/nbi/format.cfm). Definitions: SELECTION.md. Standard library only.
"""
import gzip
import json
import os
import statistics
import sys


def field(line, a, b):
    """1-based inclusive columns a..b."""
    return line[a - 1:b]


def lowest(line):
    """Return (L, malformed). L is None when no condition item is a digit."""
    vals = [field(line, c, c) for c in (259, 260, 261, 263)]
    if any(not (v.isdigit() or v == "N") for v in vals):
        return None, True
    ds = [int(v) for v in vals if v.isdigit()]
    return (min(ds) if ds else None), False


def to_int(s):
    s = s.strip()
    return int(s) if s.isdigit() else None


def read_year(path, year, state_fips):
    """Return (records, stats) for one file. records: {bridge: dict}."""
    st = {"lines": 0, "type1": 0, "malformed": 0, "fips_ok": 0, "short": 0, "dup": 0}
    recs = {}
    with open(path, encoding="latin-1", newline="") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            st["lines"] += 1
            if line[:2] == state_fips:
                st["fips_ok"] += 1
            if len(line) < 365:
                st["short"] += 1
                continue
            if field(line, 19, 19) != "1":
                continue
            st["type1"] += 1
            L, bad = lowest(line)
            if bad:
                st["malformed"] += 1
                continue
            b = field(line, 4, 18).strip()
            if b in recs:
                st["dup"] += 1
                continue
            recs[b] = {
                "L": L,
                "open": field(line, 199, 199),
                "insp": field(line, 287, 290),
                "built": field(line, 157, 160),
                "recon": field(line, 362, 365),
                "adt": to_int(field(line, 165, 170)),
            }
    return recs, st


def spells_of(series, years, last):
    """series: {year: rec}. Returns list of spells over consecutive file years with L<=4."""
    out = []
    cur = None
    present = sorted(series)
    for y in years:
        r = series.get(y)
        poor = r is not None and r["L"] is not None and r["L"] <= 4
        if poor:
            if cur is None:
                cur = {"start": y, "end": y, "recon_change": False, "first": r}
            else:
                cur["end"] = y
        elif cur is not None:
            # spell closes at year y: either bridge absent, unrated, or L>=5
            if r is None:
                cur["outcome"] = "left"
            elif r["L"] is None:
                cur["outcome"] = "unrated"
            else:
                cur["outcome"] = "rose"
                f = cur["first"]
                # reconstruction recorded across the spell: built or recon changed from spell start to the closing year
                cur["recon_change"] = (r["built"] != f["built"]) or (r["recon"] != f["recon"])
            out.append(cur)
            cur = None
    if cur is not None:
        cur["outcome"] = "censored" if cur["end"] == last else "left"
        out.append(cur)
    for s in out:
        s["years"] = s["end"] - s["start"] + 1
        del s["first"]
    return out


def inspections(series):
    """Collapse consecutive bridge-years with the same item 90 into one inspection."""
    out = []
    prev_key = None
    for y in sorted(series):
        r = series[y]
        if r["insp"] != prev_key:
            out.append((y, r))
            prev_key = r["insp"]
    return out


def main(d, state, first, last, out_path, per_path):
    fips = {"AL": "01"}.get(state)
    years = list(range(first, last + 1))
    by_bridge = {}
    file_stats = {}
    for y in years:
        p = os.path.join(d, f"{state}{y % 100:02d}.txt")
        recs, st = read_year(p, y, fips)
        file_stats[y] = st
        for b, r in recs.items():
            by_bridge.setdefault(b, {})[y] = r

    rises = rises_norecon = falls = falls2 = 0
    spells_all = []
    poor_open_by = 0
    poor_open_A = 0
    crossings = 0
    adt_missing = 0
    per = {}
    for b, series in by_bridge.items():
        sp = spells_of(series, years, last)
        spells_all.extend(sp)
        ins = inspections(series)
        br = bn = fl = 0
        for (y0, a), (y1, c) in zip(ins, ins[1:]):
            if a["L"] is None or c["L"] is None:
                continue
            if c["L"] > a["L"]:
                rises += 1
                br += 1
                if a["built"] == c["built"] and a["recon"] == c["recon"]:
                    rises_norecon += 1
                    bn += 1
            elif c["L"] < a["L"]:
                falls += 1
                fl += 1
                if a["L"] - c["L"] >= 2:
                    falls2 += 1
        poor_years = 0
        for y, r in series.items():
            if r["L"] is not None and r["L"] <= 4 and r["open"] != "K":
                poor_open_by += 1
                poor_years += 1
                if r["open"] == "A":
                    poor_open_A += 1
                if r["adt"] is None:
                    adt_missing += 1
                else:
                    crossings += r["adt"] * 365
        per[b] = {
            "years": [min(series), max(series)],
            "n": len(series),
            "L": "".join("-" if series.get(y) is None else ("N" if series[y]["L"] is None else str(series[y]["L"])) for y in years),
            "poor_open_years": poor_years,
            "rises": br,
            "rises_norecon": bn,
            "falls": fl,
            "spells": [[s["start"], s["end"], s["outcome"], s["recon_change"]] for s in sp],
        }

    in_last = {b for b, s in by_bridge.items() if last in s}
    ever_poor_last = sum(1 for b in in_last if any(r["L"] is not None and r["L"] <= 4 for r in by_bridge[b].values()))
    ended_rose = [s for s in spells_all if s["outcome"] == "rose"]
    ended_norecon = [s for s in ended_rose if not s["recon_change"]]
    longest_open_last = 0
    longest_id = None
    for b in in_last:
        r = by_bridge[b][last]
        if r["open"] == "K":
            continue
        for s in per[b]["spells"]:
            ln = s[1] - s[0] + 1
            if ln > longest_open_last:
                longest_open_last, longest_id = ln, b
    lines_total = sum(st["lines"] for st in file_stats.values())
    fips_ok_total = sum(st["fips_ok"] for st in file_stats.values())
    type1_total = sum(st["type1"] for st in file_stats.values())
    malformed_total = sum(st["malformed"] for st in file_stats.values())

    res = {
        "state": state,
        "years": [first, last],
        "files": {str(y): st for y, st in file_stats.items()},
        "bridges_ever": len(by_bridge),
        "bridges_last": len(in_last),
        "bridges_last_ever_poor": ever_poor_last,
        "P1_share_last_ever_poor": ever_poor_last / len(in_last) if in_last else None,
        "spells": len(spells_all),
        "spells_by_outcome": {k: sum(1 for s in spells_all if s["outcome"] == k) for k in ("rose", "left", "unrated", "censored")},
        "P2_median_years_spells_rose": statistics.median([s["years"] for s in ended_rose]) if ended_rose else None,
        "P3_share_rose_norecon": len(ended_norecon) / len(ended_rose) if ended_rose else None,
        "rises": rises,
        "rises_norecon": rises_norecon,
        "P4_share_rises_norecon": rises_norecon / rises if rises else None,
        "falls": falls,
        "falls_2plus": falls2,
        "P5_share_falls_2plus": falls2 / falls if falls else None,
        "P6_longest_spell_open_last": longest_open_last,
        "P6_longest_spell_bridge": longest_id,
        "poor_open_bridge_years": poor_open_by,
        "P7_share_poor_open_A": poor_open_A / poor_open_by if poor_open_by else None,
        "P8_crossings_while_poor_estimate": crossings,
        "P8_note": "estimate: sum of item 29 (ADT) x 365 over open Poor bridge-years; ADT is the record's own figure",
        "poor_open_bridge_years_adt_missing": adt_missing,
        "lines_total": lines_total,
        "type1_total": type1_total,
        "malformed_total": malformed_total,
        "P9_share_malformed": malformed_total / type1_total if type1_total else None,
        "P10_share_fips_ok": fips_ok_total / lines_total if lines_total else None,
        "P10_min_file_share_fips_ok": min((st["fips_ok"] / st["lines"]) for st in file_stats.values() if st["lines"]),
    }
    with open(out_path, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    with gzip.open(per_path, "wt") as f:
        json.dump(per, f, sort_keys=True, separators=(",", ":"))
    return res


if __name__ == "__main__":
    d, state, first, last, out_path, per_path = sys.argv[1:7]
    r = main(d, state, int(first), int(last), out_path, per_path)
    print(json.dumps({k: v for k, v in r.items() if k != "files"}, indent=1))
