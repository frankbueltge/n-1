"""Project 18, session 1: the registered count (SELECTION.md, pushed 07a8e5e before any disc was read).

Reads the `cdtoc` table extracted from MusicBrainz's core export 20261024-102842 (PostgreSQL COPY text format; columns per
admin/sql/CreateTables.sql: id, discid, freedb_id, track_count, leadout_offset, track_offset[], created) and writes session1.json.
Usage: python3 -I count1.py <path to mbdump/cdtoc> <path to mbdump/TIMESTAMP>
"""
import base64, hashlib, json, statistics, sys
from collections import Counter

def disc_id(first, last, leadout, offsets):
    # MusicBrainz disc ID: SHA-1 over hex first, last, then 100 offsets (lead-out first, 0-padded), base64 with ._- for +/=
    s = "%02X%02X" % (first, last) + "%08X" % leadout
    offs = list(offsets) + [0] * (99 - len(offsets))
    s += "".join("%08X" % o for o in offs)
    b = base64.b64encode(hashlib.sha1(s.encode("ascii")).digest()).decode("ascii")
    return b.replace("+", ".").replace("/", "_").replace("=", "-")

def main(path, tspath):
    n = bad = reproduced = 0
    lengths = []          # playing length in frames
    pregap = 0
    pregap_lengths = []
    tracks = Counter()
    created_year = Counter()
    unreproduced = []
    longest = []
    for line in open(path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) != 7:
            bad += 1
            continue
        _id, discid, _freedb, tc, leadout, offs, created = f
        try:
            tc = int(tc); leadout = int(leadout)
            offs = [int(x) for x in offs.strip("{}").split(",")]
        except ValueError:
            bad += 1
            continue
        n += 1
        if disc_id(1, tc, leadout, offs) == discid:
            reproduced += 1
        elif len(unreproduced) < 50:
            unreproduced.append({"discid": discid, "track_count": tc, "leadout": leadout, "first_offset": offs[0], "n_offsets": len(offs)})
        L = leadout - offs[0]
        lengths.append(L)
        if offs[0] > 150:
            pregap += 1
            pregap_lengths.append(offs[0] - 150)
        tracks[tc] += 1
        created_year[created[:4] if created != "\\N" else "none"] += 1
        longest.append((L, discid, tc))
    lengths.sort()
    sec = [l // 75 for l in lengths]
    by_minute = Counter(s // 60 for s in sec)
    by_second = Counter(sec)
    q = statistics.quantiles(sec, n=4)
    over74 = sum(1 for s in sec if s >= 4440)
    over80 = sum(1 for s in sec if s >= 4800)
    bins70_78 = {m: by_minute.get(m, 0) for m in range(70, 79)}
    longest.sort(reverse=True)
    out = {
        "source": "MusicBrainz core export 20261024-102842, mbdump/cdtoc; TIMESTAMP " + open(tspath).read().strip(),
        "rows_parsed": n, "rows_unparsed": bad,
        "reproduced_ids": reproduced, "reproduced_share": reproduced / n,
        "unreproduced_examples": unreproduced,
        "length_seconds": {"min": sec[0], "q1": q[0], "median": q[1], "q3": q[2], "max": sec[-1], "mean": sum(sec) / n},
        "at_or_over_74_00": over74, "at_or_over_80_00": over80, "share_at_or_over_80_00": over80 / n,
        "by_minute": {str(k): by_minute[k] for k in sorted(by_minute)},
        "by_second": {str(k): by_second[k] for k in sorted(by_second)},
        "pregap_over_zero": pregap, "pregap_share": pregap / n,
        "pregap_seconds_median": statistics.median(pregap_lengths) / 75 if pregap_lengths else None,
        "track_count": {str(k): tracks[k] for k in sorted(tracks)},
        "created_year": dict(sorted(created_year.items())),
        "longest_30": [{"seconds": l / 75, "discid": d, "tracks": t} for l, d, t in longest[:30]],
    }
    m79 = by_minute.get(79, 0)
    out["predictions"] = {
        "P1 at least 1,000,000 discs": n >= 1_000_000,
        "P2 median between 40:00 and 55:00": 2400 <= q[1] <= 3300,
        "P3 under 1 % at or over 80:00": over80 / n < 0.01,
        "P4 bin 79 above every bin 70-78": all(m79 > v for v in bins70_78.values()),
        "P5 bin 74 at least 1.2 x bin 75": by_minute.get(74, 0) >= 1.2 * by_minute.get(75, 0),
        "P6 at least 99.9 % reproduced": reproduced / n >= 0.999,
        "P7 under 2 % pregap": pregap / n < 0.02,
    }
    json.dump(out, open("session1.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("by_second", "by_minute", "unreproduced_examples", "longest_30")}, indent=1))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
