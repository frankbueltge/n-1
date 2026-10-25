"""Project 18, session 2, exploratory (not registered; written after count2.py had run and its top release groups were seen).
For discs whose lead-out sits at exactly 333,000 frames (74:00:00), at exactly 333,150 (74:02:00), elsewhere in A74, and in C70:
the share carrying the release-group secondary type "Audiobook", the share whose primary type is "Other", the share on CD-R,
the median track count and the median year. Writes explore2.json.
Usage: python3 -I explore2.py <path to mbdump/>
"""
import json, statistics, sys
from collections import defaultdict

def rows(d, t):
    for line in open(d + "/" + t, encoding="utf-8"):
        yield line.rstrip("\n").split("\t")

def group(leadout):
    if leadout == 333000: return "frame 333,000 (74:00:00)"
    if leadout == 333150: return "frame 333,150 (74:02:00)"
    if leadout // 75 == 4440: return "rest of 74:00 second"
    if 4200 <= leadout // 75 <= 4379: return "C70 (70:00-72:59)"
    if 4795 <= leadout // 75 <= 4799: return "B80 (79:55-79:59)"
    return None

def main(d):
    grp, tracks = {}, {}
    for f in rows(d, "cdtoc"):
        g = group(int(f[4]))
        if g:
            grp[int(f[0])] = g; tracks[int(f[0])] = int(f[3])
    media = defaultdict(list)
    for f in rows(d, "medium_cdtoc"):
        if int(f[2]) in grp: media[int(f[2])].append(int(f[1]))
    need = {m for v in media.values() for m in v}
    med = {}
    for f in rows(d, "medium"):
        if int(f[0]) in need: med[int(f[0])] = (int(f[1]), None if f[3] == "\\N" else int(f[3]))
    fmt = {int(f[0]): f[1] for f in rows(d, "medium_format")}
    rels = {r for r, _ in med.values()}
    rg = {}
    for f in rows(d, "release"):
        if int(f[0]) in rels: rg[int(f[0])] = int(f[4])
    year = {}
    for t, yi in (("release_country", 2), ("release_unknown_country", 1)):
        for f in rows(d, t):
            r = int(f[0])
            if r in rels and f[yi] != "\\N": year[r] = min(int(f[yi]), year.get(r, 9999))
    groups = set(rg.values())
    ptn = {int(f[0]): f[1] for f in rows(d, "release_group_primary_type")}
    stn = {int(f[0]): f[1] for f in rows(d, "release_group_secondary_type")}
    ab = [k for k, v in stn.items() if v == "Audiobook"][0]
    ptype = {}
    for f in rows(d, "release_group"):
        if int(f[0]) in groups: ptype[int(f[0])] = ptn.get(int(f[4])) if f[4] != "\\N" else None
    abg = {int(f[0]) for f in rows(d, "release_group_secondary_type_join") if int(f[1]) == ab and int(f[0]) in groups}
    acc = defaultdict(lambda: {"discs": 0, "attached": 0, "audiobook": 0, "other": 0, "cdr": 0, "tracks": [], "years": []})
    for c, g in grp.items():
        a = acc[g]; a["discs"] += 1; a["tracks"].append(tracks[c])
        ms = [m for m in media.get(c, []) if m in med]
        if not ms: continue
        a["attached"] += 1
        rr = {med[m][0] for m in ms}; gs = {rg[r] for r in rr if r in rg}
        if gs & abg: a["audiobook"] += 1
        if any(ptype.get(x) == "Other" for x in gs): a["other"] += 1
        if any(fmt.get(med[m][1]) == "CD-R" for m in ms): a["cdr"] += 1
        ys = [year[r] for r in rr if r in year]
        if ys: a["years"].append(min(ys))
    out = {}
    for g, a in acc.items():
        n = a["attached"]
        out[g] = {"discs": a["discs"], "attached": n, "audiobook_share": a["audiobook"] / n, "other_share": a["other"] / n,
                  "cd_r_share": a["cdr"] / n, "median_tracks": statistics.median(a["tracks"]),
                  "median_year": statistics.median(a["years"]) if a["years"] else None}
    json.dump(out, open("explore2.json", "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main(sys.argv[1].rstrip("/"))
