"""Project 18, session 2: the registered count (SESSION2.md, pushed e49436e before any row was read).

Reads tables extracted from MusicBrainz's core export 20261024-102842 (PostgreSQL COPY text format; columns per
admin/sql/CreateTables.sql) and writes session2.json. No person field is opened; release-group names are read only for the
top release groups of band A74, as SESSION2.md allows.
Usage: python3 -I count2.py <path to mbdump/>
"""
import json, random, statistics, sys
from collections import Counter, defaultdict

def rows(d, table):
    for line in open(d + "/" + table, encoding="utf-8"):
        yield line.rstrip("\n").split("\t")

def band(sec):
    if sec == 4440: return "A74"
    if 4795 <= sec <= 4799: return "B80"
    if 4200 <= sec <= 4379: return "C70"
    if 4560 <= sec <= 4739: return "C76"
    return None

def main(d):
    # cdtoc: id, discid, freedb_id, track_count, leadout_offset, track_offset[], created
    addr_sec = Counter(); play_sec = Counter(); frames = Counter()
    disc_band = {}; discid_of = {}
    for f in rows(d, "cdtoc"):
        cid, discid, leadout, offs = int(f[0]), f[1], int(f[4]), f[5]
        first = int(offs.strip("{}").split(",")[0])
        a = leadout // 75
        addr_sec[a] += 1
        play_sec[(leadout - first) // 75] += 1
        if 330000 <= leadout <= 336000 or 357000 <= leadout <= 361000:
            frames[leadout] += 1
        b = band(a)
        if b:
            disc_band[cid] = b; discid_of[cid] = discid
    # medium_cdtoc: id, medium, cdtoc, ...
    media_of = defaultdict(list)
    for f in rows(d, "medium_cdtoc"):
        c = int(f[2])
        if c in disc_band:
            media_of[c].append(int(f[1]))
    need_media = {m for ms in media_of.values() for m in ms}
    # medium: id, release, position, format, ...
    medium = {}
    for f in rows(d, "medium"):
        m = int(f[0])
        if m in need_media:
            medium[m] = (int(f[1]), None if f[3] == "\\N" else int(f[3]))
    fmt_name = {int(f[0]): f[1] for f in rows(d, "medium_format")}
    need_rel = {r for r, _ in medium.values()}
    # release: id, gid, name, artist_credit, release_group, ...
    rel_rg = {}; rel_gid = {}
    for f in rows(d, "release"):
        r = int(f[0])
        if r in need_rel:
            rel_rg[r] = int(f[4]); rel_gid[r] = f[1]
    year = {}
    for t in ("release_country", "release_unknown_country"):
        yi = 2 if t == "release_country" else 1
        for f in rows(d, t):
            r = int(f[0])
            if r in need_rel and f[yi] != "\\N":
                y = int(f[yi]); year[r] = min(y, year.get(r, 9999))
    need_rg = set(rel_rg.values())
    ptype_name = {int(f[0]): f[1] for f in rows(d, "release_group_primary_type")}
    stype_name = {int(f[0]): f[1] for f in rows(d, "release_group_secondary_type")}
    comp_id = [k for k, v in stype_name.items() if v == "Compilation"][0]
    rg_type = {}; rg_name = {}
    for f in rows(d, "release_group"):
        g = int(f[0])
        if g in need_rg:
            rg_type[g] = None if f[4] == "\\N" else int(f[4]); rg_name[g] = f[2]
    comp_rg = set()
    for f in rows(d, "release_group_secondary_type_join"):
        if int(f[1]) == comp_id and int(f[0]) in need_rg:
            comp_rg.add(int(f[0]))
    # per band
    out_b = {}
    per = defaultdict(lambda: {"discs": 0, "orphan": 0, "fmt": Counter(), "ptype": Counter(), "comp": 0, "years": [],
                               "rg": Counter()})
    for c, b in disc_band.items():
        p = per[b]; p["discs"] += 1
        ms = [m for m in media_of.get(c, []) if m in medium]
        if not ms:
            p["orphan"] += 1; continue
        rels = {medium[m][0] for m in ms}
        fmts = {fmt_name.get(medium[m][1], "none") if medium[m][1] else "none" for m in ms}
        p["fmt"][fmts.pop() if len(fmts) == 1 else "mixed"] += 1
        rgs = {rel_rg[r] for r in rels if r in rel_rg}
        pts = {ptype_name.get(rg_type.get(g), "none") if rg_type.get(g) else "none" for g in rgs}
        p["ptype"][pts.pop() if len(pts) == 1 else "mixed"] += 1
        if rgs & comp_rg: p["comp"] += 1
        ys = [year[r] for r in rels if r in year]
        if ys: p["years"].append(min(ys))
        for g in rgs: p["rg"][g] += 1
    for b in ("A74", "B80", "C70", "C76"):
        p = per[b]; att = p["discs"] - p["orphan"]
        one_fmt = sum(v for k, v in p["fmt"].items() if k != "mixed")
        out_b[b] = {
            "discs": p["discs"], "orphan": p["orphan"], "attached": att,
            "format": dict(p["fmt"].most_common()), "share_CD_of_one_format": p["fmt"]["CD"] / one_fmt if one_fmt else None,
            "primary_type": dict(p["ptype"].most_common()),
            "compilation": p["comp"], "compilation_share": p["comp"] / att if att else None,
            "with_year": len(p["years"]), "median_year": statistics.median(p["years"]) if p["years"] else None,
            "years": dict(sorted(Counter(p["years"]).items())),
            "distinct_release_groups": len(p["rg"]),
        }
    out_b["A74"]["top_release_groups"] = [{"release_group": rg_name[g], "discs": n} for g, n in per["A74"]["rg"].most_common(15)]
    out_b["B80"]["top_release_groups"] = [{"release_group": rg_name[g], "discs": n} for g, n in per["B80"]["rg"].most_common(15)]
    # falls
    falls = []
    for s in range(4300, 4900):
        if addr_sec[s + 1] >= 1:
            falls.append((addr_sec[s] / addr_sec[s + 1], s))
    falls.sort(reverse=True)
    top74 = max(range(4380, 4500), key=lambda s: addr_sec[s])
    f74 = max(range(330000, 336001), key=lambda x: frames[x])
    ratio_addr = addr_sec[4799] / addr_sec[4800] if addr_sec[4800] else None
    # draw for the check
    pool = sorted(c for c, b in disc_band.items() if b in ("A74", "B80"))
    drawn = random.Random(20261025).sample(pool, 20)
    draw = []
    for c in drawn:
        rels = sorted({rel_gid[medium[m][0]] for m in media_of.get(c, []) if m in medium and medium[m][0] in rel_gid})
        draw.append({"discid": discid_of[c], "band": disc_band[c], "releases": rels})
    out = {
        "source": "MusicBrainz core export 20261024-102842; TIMESTAMP " + open(d + "/../TIMESTAMP").read().strip(),
        "address_seconds": {str(k): addr_sec[k] for k in sorted(addr_sec) if k <= 6000},
        "playing_seconds_4380_4899": {str(k): play_sec[k] for k in range(4380, 4900)},
        "frames_330000_336000": {str(k): frames[k] for k in range(330000, 336001) if frames[k]},
        "frames_357000_361000": {str(k): frames[k] for k in range(357000, 361001) if frames[k]},
        "largest_falls_4300_4899": [{"from": s, "to": s + 1, "ratio": r, "counts": [addr_sec[s], addr_sec[s + 1]]} for r, s in falls[:10]],
        "commonest_second_4380_4499": top74, "commonest_frame_330000_336000": f74, "commonest_frame_count": frames[f74],
        "fall_4799_4800_address": ratio_addr,
        "bands": out_b,
        "check_draw": draw,
    }
    a, b80, c76 = out_b["A74"], out_b["B80"], out_b["C76"]
    out["predictions"] = {
        "P1 largest fall 4300-4899 is 4799->4800": falls[0][1] == 4799,
        "P2 address fall 4799/4800 exceeds 498/167": ratio_addr is not None and ratio_addr > 498 / 167,
        "P3 commonest second 4380-4499 is 4440": top74 == 4440,
        "P4 commonest frame 330000-336000 is 333000": f74 == 333000,
        "P5 B80 compilation share at least 1.5 x C76": b80["compilation_share"] >= 1.5 * c76["compilation_share"],
        "P6 A74 median year at least 3 earlier than B80": a["median_year"] is not None and b80["median_year"] - a["median_year"] >= 3,
        "P7 CD at least 90 % of one-format discs in A74 and B80": a["share_CD_of_one_format"] >= 0.9 and b80["share_CD_of_one_format"] >= 0.9,
    }
    json.dump(out, open("session2.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k not in ("address_seconds", "playing_seconds_4380_4899",
                      "frames_330000_336000", "frames_357000_361000", "check_draw")}, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1].rstrip("/"))
