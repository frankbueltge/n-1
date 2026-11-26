"""Project 27, session 2: what stands before and after a rise in the lowest condition code with nothing recorded.

Usage: python3 count2.py DIR STATE FIRST LAST OUT.json RISES.json.gz
  Definitions: SESSION2.md. Inspections, rises and "recorded" exactly as count1.py. Standard library only.
"""
import gzip
import json
import os
import statistics
import sys
from collections import Counter

ITEMS = (("58", 259), ("59", 260), ("60", 261), ("62", 263))


def field(line, a, b):
    return line[a - 1:b]


def read_year(path):
    recs = {}
    vocab = {"41": Counter(), "75A": Counter(), "91": Counter()}
    with open(path, encoding="latin-1", newline="") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if not line.strip() or len(line) < 365 or field(line, 19, 19) != "1":
                continue
            vals = [field(line, c, c) for _, c in ITEMS]
            if any(not (v.isdigit() or v == "N") for v in vals):
                continue
            b = field(line, 4, 18).strip()
            if b in recs:
                continue
            ds = [int(v) for v in vals if v.isdigit()]
            r = {
                "L": min(ds) if ds else None,
                "items": [int(v) if v.isdigit() else None for v in vals],
                "open": field(line, 199, 199),
                "insp": field(line, 287, 290),
                "built": field(line, 157, 160),
                "recon": field(line, 362, 365),
                "w75": field(line, 278, 279),
                "f91": field(line, 291, 292),
            }
            for k, v in (("41", r["open"]), ("75A", r["w75"]), ("91", r["f91"])):
                vocab[k][v] += 1
            recs[b] = r
    return recs, vocab


def months(insp):
    """MMYY -> months since year 0, or None."""
    if not insp.isdigit():
        return None
    m, yy = int(insp[:2]), int(insp[2:])
    if not 1 <= m <= 12:
        return None
    y = 1900 + yy if yy >= 50 else 2000 + yy
    return y * 12 + m - 1


def inspections(series):
    out = []
    prev = None
    for y in sorted(series):
        r = series[y]
        if r["insp"] != prev:
            out.append((y, r))
            prev = r["insp"]
    return out


def work_proposed(r):
    return r["w75"].isdigit() and 31 <= int(r["w75"]) <= 38


def main(d, state, first, last, out_path, rises_path):
    years = list(range(first, last + 1))
    by_bridge = {}
    vocab = {"41": Counter(), "75A": Counter(), "91": Counter()}
    for y in years:
        recs, v = read_year(os.path.join(d, f"{state}{y % 100:02d}.txt"))
        for k in vocab:
            vocab[k].update(v[k])
        for b, r in recs.items():
            by_bridge.setdefault(b, {})[y] = r

    pairs = 0
    pairs_wp = pairs_nwp = 0
    sil_wp = sil_nwp = 0
    rises = 0
    intervals_all = []
    pairs_by_int = Counter()
    sil_by_int = Counter()
    silent = []
    for b, series in by_bridge.items():
        ins = inspections(series)
        for i in range(len(ins) - 1):
            (y0, a), (y1, c) = ins[i], ins[i + 1]
            if a["L"] is None or c["L"] is None:
                continue
            pairs += 1
            wp = work_proposed(a)
            if wp:
                pairs_wp += 1
            else:
                pairs_nwp += 1
            m0, m1 = months(a["insp"]), months(c["insp"])
            iv = (m1 - m0) if (m0 is not None and m1 is not None) else None
            band = None
            if iv is not None:
                intervals_all.append(iv)
                band = "le12" if iv <= 12 else ("23to25" if 23 <= iv <= 25 else "other")
                pairs_by_int[band] += 1
            if c["L"] <= a["L"]:
                continue
            rises += 1
            if a["built"] != c["built"] or a["recon"] != c["recon"]:
                continue
            if wp:
                sil_wp += 1
            else:
                sil_nwp += 1
            if band:
                sil_by_int[band] += 1
            comps = [ITEMS[k][0] for k in range(4)
                     if a["items"][k] is not None and c["items"][k] is not None
                     and a["items"][k] == a["L"] and c["items"][k] > a["items"][k]]
            later = [r["L"] for _, r in ins[i + 2:]]
            later_rated = [x for x in later if x is not None]
            nxt = ins[i + 2][1]["L"] if i + 2 < len(ins) else None
            silent.append({
                "b": b, "y0": y0, "y1": y1, "L0": a["L"], "L1": c["L"],
                "open0": a["open"], "open1": c["open"], "w75": a["w75"], "interval": iv,
                "comps": comps,
                "has_next": i + 2 < len(ins),
                "next_L": nxt,
                "falls_back": (nxt is not None and nxt <= a["L"]),
                "n_later": len(later_rated),
                "holds": (len(later_rated) > 0 and all(x > a["L"] for x in later_rated)),
                "poor_exit": a["L"] <= 4 and c["L"] >= 5,
                "back_poor": any(x <= 4 for x in later_rated),
            })

    S = len(silent)
    with_next = [s for s in silent if s["has_next"] and s["next_L"] is not None]
    with_later = [s for s in silent if s["n_later"] > 0]
    comp = Counter(c for s in silent for c in s["comps"])
    posted = [s for s in silent if s["open0"] in ("P", "R")]
    lifted = [s for s in posted if s["open1"] == "A"]
    by_year = Counter(s["y1"] for s in silent)
    top_year, top_n = max(by_year.items(), key=lambda kv: (kv[1], -kv[0]))
    sil_iv = [s["interval"] for s in silent if s["interval"] is not None]
    pe = [s for s in silent if s["poor_exit"]]
    pe_later = [s for s in pe if s["n_later"] > 0]
    pe_back = [s for s in pe_later if s["back_poor"]]
    rate = lambda n, d: n / d if d else None

    res = {
        "state": state, "years": [first, last],
        "rated_pairs": pairs, "rises": rises, "silent_rises": S,
        "silent_with_next": len(with_next),
        "P1_share_falls_back_next": rate(sum(s["falls_back"] for s in with_next), len(with_next)),
        "silent_with_later": len(with_later),
        "P2_share_holds": rate(sum(s["holds"] for s in with_later), len(with_later)),
        "silent_last": S - len(with_later),
        "P3_component_counts": dict(comp),
        "silent_no_component": sum(1 for s in silent if not s["comps"]),
        "P4_rate_after_work_proposed": rate(sil_wp, pairs_wp), "pairs_work_proposed": pairs_wp, "silent_work_proposed": sil_wp,
        "P4_rate_after_no_work_proposed": rate(sil_nwp, pairs_nwp), "pairs_no_work_proposed": pairs_nwp, "silent_no_work_proposed": sil_nwp,
        "P5_silent_from_posted": len(posted), "P5_share_lifted": rate(len(lifted), len(posted)),
        "P6_by_year": {str(k): v for k, v in sorted(by_year.items())},
        "P6_top_year": top_year, "P6_top_share": rate(top_n, S),
        "P7_median_interval_silent": statistics.median(sil_iv) if sil_iv else None,
        "P7_median_interval_all": statistics.median(intervals_all) if intervals_all else None,
        "P8_poor_exits": len(pe), "P8_poor_exits_with_later": len(pe_later),
        "P8_share_back_poor": rate(len(pe_back), len(pe_later)),
        "P9_pairs_by_interval": dict(pairs_by_int), "P9_silent_by_interval": dict(sil_by_int),
        "P9_rate_le12": rate(sil_by_int["le12"], pairs_by_int["le12"]),
        "P9_rate_23to25": rate(sil_by_int["23to25"], pairs_by_int["23to25"]),
        "vocab": {k: dict(v.most_common()) for k, v in vocab.items()},
    }
    with open(out_path, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    with gzip.open(rises_path, "wt") as f:
        json.dump(silent, f, separators=(",", ":"))
    return res


if __name__ == "__main__":
    d, state, first, last, out_path, rises_path = sys.argv[1:7]
    r = main(d, state, int(first), int(last), out_path, rises_path)
    print(json.dumps({k: v for k, v in r.items() if k not in ("vocab", "P6_by_year")}, indent=1))
