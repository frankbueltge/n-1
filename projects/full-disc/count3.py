"""Project 18, session 3: the registered count (SESSION3.md, pushed ff0c698 before any row was read).

Reads tables extracted from MusicBrainz's core export 20261024-102842 (PostgreSQL COPY text format; columns per
admin/sql/CreateTables.sql) and writes session3.json. No title, artist or person field is opened: release gid and
release_group id only.
Usage: python3 -I count3.py <path to mbdump/>
"""
import json, random, statistics, sys
from collections import Counter, defaultdict

FRAME = 333000

def rows(d, table):
    for line in open(d + "/" + table, encoding="utf-8"):
        yield line.rstrip("\n").split("\t")

def main(d):
    # cdtoc: id, discid, freedb_id, track_count, leadout_offset, track_offset[], created
    leadout = {}; discid = {}; frame_discs = set(); long_frames = Counter()
    for f in rows(d, "cdtoc"):
        c, lo = int(f[0]), int(f[4])
        leadout[c] = lo; discid[c] = f[1]
        if lo == FRAME: frame_discs.add(c)
        if lo >= 270000: long_frames[lo] += 1
    # medium_cdtoc: id, medium, cdtoc, ...
    tocs_of = defaultdict(list)
    for f in rows(d, "medium_cdtoc"):
        tocs_of[int(f[1])].append(int(f[2]))
    frame_media = {m for m, cs in tocs_of.items() if any(c in frame_discs for c in cs)}
    # medium: id, release, position, format, name, edits_pending, last_updated, track_count, gid
    rel_of = {}
    for f in rows(d, "medium"):
        if int(f[0]) in frame_media: rel_of[int(f[0])] = int(f[1])
    R = set(rel_of.values())
    media = defaultdict(list)
    for f in rows(d, "medium"):
        r = int(f[1])
        if r in R:
            media[r].append((int(f[2]), int(f[0]), None if f[3] == "\\N" else int(f[3])))
    fmt_name = {int(f[0]): f[1] for f in rows(d, "medium_format")}
    gid = {}; rg = {}
    for f in rows(d, "release"):
        r = int(f[0])
        if r in R: gid[r] = f[1]; rg[r] = int(f[4])

    def address(m):
        cs = tocs_of.get(m, [])
        if not cs: return None
        if any(c in frame_discs for c in cs): return FRAME
        return max(leadout[c] for c in cs)

    sets, singles = [], []
    nonlast = Counter(); last = Counter(); last_addr = []; last_not_frame = []
    for r in sorted(R):
        ms = sorted(media[r])
        row = {"release": gid[r], "release_group": rg[r],
               "media": [{"position": p, "address": address(m), "format": fmt_name.get(fm) if fm else None,
                          "discids": sorted(discid[c] for c in tocs_of.get(m, []))} for p, m, fm in ms]}
        if len(ms) < 2:
            singles.append(row); continue
        sets.append(row)
        for i, x in enumerate(row["media"]):
            a = x["address"]
            k = "unmeasured" if a is None else ("frame" if a == FRAME else "other")
            if i < len(ms) - 1:
                nonlast[k] += 1
            else:
                last[k] += 1
                if a is not None:
                    last_addr.append(a)
                    if a != FRAME: last_not_frame.append(a)
    nl_meas = nonlast["frame"] + nonlast["other"]
    l_meas = last["frame"] + last["other"]
    med_last = statistics.median(last_not_frame) if last_not_frame else None
    top_long = long_frames.most_common(15)
    # draw for the check
    drawn = random.Random(20261026).sample(sorted(R), 20)
    draw = []
    for r in drawn:
        draw.append({"release": gid[r], "media": [{"position": p, "discids": sorted(discid[c] for c in tocs_of.get(m, []))}
                                                  for p, m, _ in sorted(media[r])]})
    out = {
        "source": "MusicBrainz core export 20261024-102842; TIMESTAMP " + open(d + "/../TIMESTAMP").read().strip(),
        "frame_discs": len(frame_discs), "frame_media": len(frame_media),
        "R": len(R), "sets": len(sets), "singles": len(singles), "set_share": len(sets) / len(R),
        "nonlast": dict(nonlast), "nonlast_frame_share_of_measured": nonlast["frame"] / nl_meas if nl_meas else None,
        "last": dict(last), "last_frame_share_of_measured": last["frame"] / l_meas if l_meas else None,
        "last_not_frame_median_frames": med_last,
        "last_at_most_frame_share": sum(1 for a in last_addr if a <= FRAME) / len(last_addr) if last_addr else None,
        "last_addresses": sorted(last_addr),
        "commonest_leadouts_ge_270000": [{"frame": k, "discs": v} for k, v in top_long],
        "media_count_of_sets": dict(sorted(Counter(len(s["media"]) for s in sets).items())),
        "check_draw": draw,
    }
    out["predictions"] = {
        "P1 R at least 100 releases": len(R) >= 100,
        "P2 at least 80 % of R are sets": out["set_share"] >= 0.8,
        "P3 at least 70 % of measured non-last media at the frame": (out["nonlast_frame_share_of_measured"] or 0) >= 0.7,
        "P4 at most 10 % of measured last media at the frame": out["last_frame_share_of_measured"] is not None and out["last_frame_share_of_measured"] <= 0.1,
        "P5 median of last media not at frame in 112500-225000": med_last is not None and 112500 <= med_last <= 225000,
        "P6 at least 95 % of measured last media at most 333000": (out["last_at_most_frame_share"] or 0) >= 0.95,
        "P7 333000 commonest leadout >= 270000": top_long[0][0] == FRAME,
    }
    json.dump(out, open("session3.json", "w"), indent=1)
    rowsfile = {"sets": sets, "singles": singles}
    json.dump(rowsfile, open("sets3.json", "w"), indent=0)
    print(json.dumps({k: v for k, v in out.items() if k not in ("last_addresses", "check_draw")}, indent=1))

if __name__ == "__main__":
    main(sys.argv[1].rstrip("/"))
