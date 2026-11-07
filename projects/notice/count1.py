#!/usr/bin/env python3
"""Project 23 session 1: the registered count (SELECTION.md). Run once after the selection is pushed.

usage: python3 -I count1.py TARDIR WORKDIR OUT.json
TARDIR holds tzdata*.tar.gz; WORKDIR is scratch for unpacking and compiling.
"""
import calendar, json, os, re, struct, subprocess, sys, tarfile, statistics
from concurrent.futures import ProcessPoolExecutor

REGION = ["africa", "antarctica", "asia", "australasia", "europe", "northamerica", "southamerica", "etcetera"]
W0 = calendar.timegm((1997, 1, 1, 0, 0, 0))
W1 = calendar.timegm((2026, 11, 7, 0, 0, 0))


def norm(name):
    # 96i -> 1996i ; 93 -> 1993
    m = re.fullmatch(r"(\d{2}|\d{4})([a-z]?)", name)
    if not m:
        return name
    y = m.group(1)
    if len(y) == 2:
        y = "19" + y
    return y + m.group(2)


def news_dates(path):
    out = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"Release (\S+) - (\d{4}-\d{2}-\d{2})", line)
        if not m:
            continue
        label, date = m.group(1), m.group(2)
        toks = label.split("-")
        data = [t[4:] for t in toks if t.startswith("data")]
        bare = [t for t in toks if not t.startswith("code") and not t.startswith("data")]
        for d in data + bare:
            out.setdefault(norm(d), date)
    return out


def read_tzif(path):
    b = open(path, "rb").read()
    if b[:4] != b"TZif":
        return None
    ver = b[4:5]

    def block(off, tsize):
        isut, isstd, leap, timecnt, typecnt, charcnt = struct.unpack(">6l", b[off + 20:off + 44])
        p = off + 44
        fmt = ">%d%s" % (timecnt, "q" if tsize == 8 else "l")
        times = struct.unpack(fmt, b[p:p + timecnt * tsize]); p += timecnt * tsize
        idx = b[p:p + timecnt]; p += timecnt
        types = []
        for i in range(typecnt):
            utoff, isdst, ai = struct.unpack(">lBB", b[p:p + 6]); p += 6
            types.append(utoff)
        p += charcnt + leap * (tsize + 4) + isstd + isut
        return times, idx, types, p

    times, idx, types, end = block(0, 4)
    if ver >= b"2":
        times, idx, types, _ = block(end, 8)
    trans = []
    prev = types[0] if types else None
    for t, i in zip(times, idx):
        off = types[i]
        if off != prev:
            trans.append((t, off))
        prev = off
    return trans


def compile_release(args):
    name, tarpath, work = args
    src = os.path.join(work, "src", name)
    out = os.path.join(work, "out", name)
    os.makedirs(src, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    with tarfile.open(tarpath) as tf:
        members = tf.getmembers()
        mtime = max(m.mtime for m in members if m.isfile())
        tf.extractall(src, filter="data")
    files = [f for f in REGION if os.path.exists(os.path.join(src, f))]
    r = subprocess.run(["zic", "-b", "fat", "-d", out] + files, cwd=src, capture_output=True, text=True)
    zones = {}
    for f in files:
        for line in open(os.path.join(src, f), encoding="latin-1"):
            m = re.match(r"Zone\s+(\S+)", line)
            if m and not m.group(1).startswith("Etc/"):
                zones[m.group(1)] = None
    if r.returncode != 0:
        return name, {"ok": False, "mtime": mtime, "err": r.stderr[-400:], "zones": {}}
    for z in zones:
        p = os.path.join(out, z)
        if os.path.exists(p):
            zones[z] = [(t, o) for t, o in read_tzif(p) if W0 <= t < W1]
    zones = {z: v for z, v in zones.items() if v is not None}
    return name, {"ok": True, "mtime": mtime, "zones": zones, "files": files}


def main():
    tardir, work, outpath = sys.argv[1:4]
    tars = sorted(f for f in os.listdir(tardir) if f.startswith("tzdata") and f.endswith(".tar.gz") and f != "tzdatabeta.tar.gz")
    jobs = [(norm(f[6:-7]), os.path.join(tardir, f), work) for f in tars]
    with ProcessPoolExecutor(8) as ex:
        rel = dict(ex.map(compile_release, jobs))
    newest = max(rel, key=lambda n: (n[:4], n[4:]))
    news = news_dates(os.path.join(work, "src", newest, "NEWS"))
    dates = {}
    for n, d in rel.items():
        if n in news:
            dates[n] = (news[n], "news")
        else:
            import datetime
            dates[n] = (datetime.datetime.utcfromtimestamp(d["mtime"]).strftime("%Y-%m-%d"), "mtime")
    ok = [n for n in rel if rel[n]["ok"]]
    order = sorted(ok, key=lambda n: (dates[n][0], n))
    def ts(d):
        return calendar.timegm(tuple(map(int, d.split("-"))) + (0, 0, 0))
    final = rel[newest]["zones"]
    sets = {n: {z: set(v) for z, v in rel[n]["zones"].items()} for n in order}
    rows = []
    for z, trs in final.items():
        for t, off in trs:
            first = None
            for i, n in enumerate(order):
                if z in sets[n] and (t, off) in sets[n][z]:
                    first = i
                    break
            settled = None
            for i in range(len(order) - 1, -1, -1):
                n = order[i]
                if z in sets[n] and (t, off) in sets[n][z]:
                    settled = i
                else:
                    break
            fn = order[first]
            with_zone = first > 0 and z not in sets[order[first - 1]]
            rows.append({
                "zone": z, "t": t, "offset": off, "first": fn, "first_date": dates[fn][0], "first_date_src": dates[fn][1],
                "lead_days": round((t - ts(dates[fn][0])) / 86400, 3),
                "settled": order[settled], "settled_lead_days": round((t - ts(dates[order[settled]][0])) / 86400, 3),
                "with_zone": with_zone, "censored": first == 0,
            })
    core = [r for r in rows if not r["with_zone"] and not r["censored"]]
    late = [r for r in core if r["lead_days"] < 0]
    lt30 = [r for r in core if r["lead_days"] < 30]
    def year(r):
        return int(__import__("time").strftime("%Y", __import__("time").gmtime(r["t"])))
    by_year = {}
    for r in core:
        y = year(r)
        a = by_year.setdefault(y, [0, 0])
        a[0] += 1
        a[1] += r["lead_days"] < 0
    early = [r for r in core if year(r) < 2010]
    recent = [r for r in core if year(r) >= 2010]
    share = lambda xs: (sum(r["lead_days"] < 0 for r in xs) / len(xs)) if xs else None
    zone_counts = {n: len(rel[n]["zones"]) for n in order}
    drops = []
    for i in range(1, len(order) - 1):
        a, b, c = zone_counts[order[i - 1]], zone_counts[order[i]], zone_counts[order[i + 1]]
        if b < 0.9 * min(a, c):
            drops.append([order[i], a, b, c])
    peak_year = max(by_year, key=lambda y: by_year[y][1]) if late else None
    res = {
        "releases_total": len(rel), "releases_compiled": len(ok),
        "failed": {n: rel[n]["err"] for n in rel if not rel[n]["ok"]},
        "dated_news": sum(1 for n in rel if dates[n][1] == "news"),
        "dated_mtime": sorted(n for n in rel if dates[n][1] == "mtime"),
        "newest": newest, "earliest_dated_compiled": order[0], "zones_newest": len(final),
        "zone_count_drops": drops,
        "final_transitions": len(rows), "with_zone": sum(r["with_zone"] for r in rows),
        "censored": sum(r["censored"] for r in rows), "core": len(core),
        "late": len(late), "late_share": len(late) / len(core) if core else None,
        "lt30": len(lt30), "lt30_share": len(lt30) / len(core) if core else None,
        "median_lead_days": statistics.median(r["lead_days"] for r in core) if core else None,
        "late_by_year": {y: by_year[y] for y in sorted(by_year)}, "peak_late_year": peak_year,
        "max_late_days": -min(r["lead_days"] for r in core) if core else None,
        "late_share_1997_2009": share(early), "late_share_2010_2026": share(recent),
        "settled_late": sum(1 for r in core if r["settled_lead_days"] < 0),
        "release_dates": {n: dates[n] for n in order}, "zone_counts": zone_counts,
        "rows": rows,
    }
    yrs = res["late_by_year"]
    res["predictions"] = {
        "P1": len(ok) >= 260, "P2": res["dated_news"] >= 200, "P3": 300 <= len(final) <= 380,
        "P4": 7000 <= len(rows) <= 20000,
        "P5": res["late_share"] is not None and 0.005 <= res["late_share"] <= 0.05,
        "P6": res["lt30_share"] is not None and 0.02 <= res["lt30_share"] <= 0.10,
        "P7": res["median_lead_days"] is not None and res["median_lead_days"] >= 3 * 365.25,
        "P8": peak_year is not None and 2011 <= peak_year <= 2016,
        "P9": res["max_late_days"] is not None and res["max_late_days"] > 365,
        "P10": (res["late_share_2010_2026"] or 0) > (res["late_share_1997_2009"] or 0),
    }
    json.dump(res, open(outpath, "w"), indent=0)
    print(json.dumps({k: v for k, v in res.items() if k not in ("rows", "release_dates", "zone_counts", "late_by_year")}, indent=1))


if __name__ == "__main__":
    main()
