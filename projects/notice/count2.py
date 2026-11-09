#!/usr/bin/env python3
"""Project 23 session 2: the registered count (SESSION2.md). Run once after the registration is pushed.

For every zone of the final release and every instant of the window, the offset the then-newest release showed against the
offset the final release gives; wrong runs joined into episodes, each episode given a kind (past rewritten, re-timed, news).

usage: python3 -I count2.py TARDIR WORKDIR OUT.json      (helper/ beside this file is put on PATH for zic)
       python3 -I count2.py --synthetic                  (hand-made releases, no files)
"""
import bisect, calendar, collections, json, os, re, struct, subprocess, sys, statistics, tarfile, time
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REGION = ["africa", "antarctica", "asia", "australasia", "europe", "northamerica", "southamerica", "etcetera"]
W0 = calendar.timegm((1997, 1, 1, 0, 0, 0))
W1 = calendar.timegm((2026, 11, 7, 0, 0, 0))
DAY = 86400


def norm(name):
    m = re.fullmatch(r"(\d{2}|\d{4})([a-z]?)", name)
    if not m:
        return name
    y = m.group(1)
    return ("19" + y if len(y) == 2 else y) + m.group(2)


def news_dates(path):
    out = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"Release (\S+) - (\d{4}-\d{2}-\d{2})", line)
        if not m:
            continue
        toks = m.group(1).split("-")
        data = [t[4:] for t in toks if t.startswith("data")]
        bare = [t for t in toks if not t.startswith("code") and not t.startswith("data")]
        for d in data + bare:
            out.setdefault(norm(d), m.group(2))
    return out


def read_tzif(path):
    """(initial offset, [(t, new offset)] at every change of offset), from the 64-bit block when present."""
    b = open(path, "rb").read()
    if b[:4] != b"TZif":
        return None

    def block(off, tsize):
        isut, isstd, leap, timecnt, typecnt, charcnt = struct.unpack(">6l", b[off + 20:off + 44])
        p = off + 44
        times = struct.unpack(">%d%s" % (timecnt, "q" if tsize == 8 else "l"), b[p:p + timecnt * tsize]); p += timecnt * tsize
        idx = b[p:p + timecnt]; p += timecnt
        types = []
        for i in range(typecnt):
            utoff, isdst, ai = struct.unpack(">lBB", b[p:p + 6]); p += 6
            types.append(utoff)
        p += charcnt + leap * (tsize + 4) + isstd + isut
        return times, idx, types, p

    times, idx, types, end = block(0, 4)
    if b[4:5] >= b"2":
        times, idx, types, _ = block(end, 8)
    init = types[0] if types else 0
    trans, prev = [], init
    for t, i in zip(times, idx):
        if types[i] != prev:
            trans.append((t, types[i]))
        prev = types[i]
    return init, trans


def compile_release(args):
    name, tarpath, work = args
    src, out = os.path.join(work, "src", name), os.path.join(work, "out", name)
    os.makedirs(src, exist_ok=True); os.makedirs(out, exist_ok=True)
    with tarfile.open(tarpath) as tf:
        tf.extractall(src, filter="data")
    files = [f for f in REGION if os.path.exists(os.path.join(src, f))]
    env = dict(os.environ, PATH=os.path.join(HERE, "helper") + os.pathsep + os.environ.get("PATH", ""))
    r = subprocess.run(["zic", "-b", "fat", "-d", out] + files, cwd=src, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        return name, {"ok": False, "err": r.stderr[-300:], "zones": {}}
    zones = {}
    for f in files:
        for line in open(os.path.join(src, f), encoding="latin-1"):
            m = re.match(r"Zone\s+(\S+)", line)
            if m and not m.group(1).startswith("Etc/"):
                p = os.path.join(out, m.group(1))
                if os.path.exists(p):
                    zones[m.group(1)] = read_tzif(p)
    return name, {"ok": True, "zones": zones}


class Z:
    """one zone's offsets as a step function"""
    def __init__(self, init, trans):
        self.init, self.trans = init, trans
        self.ts = [t for t, _ in trans]

    def at(self, t):
        i = bisect.bisect_right(self.ts, t)
        return self.init if i == 0 else self.trans[i - 1][1]

    def breaks(self, a, b):
        return [t for t in self.ts[bisect.bisect_right(self.ts, a):bisect.bisect_left(self.ts, b)]]


def analyse(order, dates, zones_by_rel):
    """order: release names (final last); dates: name -> unix day start; zones_by_rel: name -> {zone: (init, trans)}"""
    final = order[-1]
    F = {z: Z(*v) for z, v in zones_by_rel[final].items()}
    lives = []
    for i, n in enumerate(order[:-1]):
        a, b = max(dates[n], W0), min(dates[order[i + 1]], W1)
        if a < b:
            lives.append((i, a, b))
    starts = [a for _, a, _ in lives]
    cache = {}

    def zr(i, z):
        k = (i, z)
        if k not in cache:
            v = zones_by_rel[order[i]].get(z)
            cache[k] = Z(*v) if v else None
        return cache[k]

    episodes, exposure, absent = [], 0, 0
    for z, fz in F.items():
        runs = []
        for i, a, b in lives:
            rz = zr(i, z)
            if rz is None:
                absent += b - a
                continue
            exposure += b - a
            cuts = sorted(set([a, b] + rz.breaks(a, b) + fz.breaks(a, b)))
            for s, e in zip(cuts, cuts[1:]):
                ro, fo = rz.at(s), fz.at(s)
                if ro != fo:
                    err = abs(ro - fo)
                    if runs and runs[-1]["t1"] == s:
                        runs[-1]["t1"] = e; runs[-1]["err"] = max(runs[-1]["err"], err)
                        runs[-1]["err_hours"][err] = runs[-1]["err_hours"].get(err, 0) + (e - s)
                    else:
                        runs.append({"zone": z, "t0": s, "t1": e, "rel": i, "err": err, "err_hours": {err: e - s},
                                     "shown": ro, "final": fo})
        for r in runs:
            i0, t0, t1 = r["rel"], r["t0"], r["t1"]
            corr = None
            for j in range(i0 + 1, len(order)):
                cz = zr(j, z) if j < len(order) - 1 else fz
                if cz is not None and cz.at(t0) == fz.at(t0):
                    corr = j
                    break
            lag = (dates[order[corr]] - t0) / DAY
            rz = zr(i0, z)
            retimed = False
            for tr, orr in rz.trans:
                if abs(tr - t0) > 62 * DAY and abs(tr - t1) > 62 * DAY:
                    continue
                for tf, of in fz.trans:
                    if of == orr and abs(tr - tf) <= 31 * DAY and min(tr, tf) <= t0 and t1 <= max(tr, tf):
                        retimed = True
                        break
                if retimed:
                    break
            kind = "past" if lag > 365 else ("retimed" if retimed else "news")
            episodes.append({"zone": z, "t0": t0, "t1": t1, "hours": round((t1 - t0) / 3600, 3), "rel": order[i0],
                             "corr": order[corr], "lag_days": round(lag, 3), "kind": kind, "err_s": r["err"],
                             "err_hours": {str(k): round(v / 3600, 3) for k, v in r["err_hours"].items()},
                             "shown": r["shown"], "final": r["final"]})
    return episodes, exposure / 3600, absent / 3600


def summarise(episodes, exposure_h, absent_h):
    K = ("past", "retimed", "news")
    hours = {k: round(sum(e["hours"] for e in episodes if e["kind"] == k), 1) for k in K}
    total = round(sum(hours.values()), 1)
    n = {k: sum(1 for e in episodes if e["kind"] == k) for k in K}
    zones = {k: len({e["zone"] for e in episodes if e["kind"] == k}) for k in K}
    yr = lambda e: time.gmtime(e["t0"]).tm_year
    by_year = {}
    for e in episodes:
        a = by_year.setdefault(yr(e), {k: 0.0 for k in K})
        a[e["kind"]] = round(a[e["kind"]] + e["hours"], 1)
    err = collections.Counter()
    for e in episodes:
        for k, v in e["err_hours"].items():
            err[int(k)] += v
    news = sorted((e for e in episodes if e["kind"] == "news"), key=lambda e: (e["corr"], e["t0"]))
    events = []
    for e in news:
        g = events[-1] if events else None
        if g and g["corr"] == e["corr"] and e["t0"] - g["t0_max"] <= 2 * DAY:
            g["zones"].append(e["zone"]); g["t0_max"] = max(g["t0_max"], e["t0"]); g["hours"] += e["hours"]
            g["max_days"] = max(g["max_days"], e["hours"] / 24)
        else:
            events.append({"corr": e["corr"], "when": time.strftime("%Y-%m-%d %H:%M", time.gmtime(e["t0"])), "t0_max": e["t0"],
                           "zones": [e["zone"]], "hours": e["hours"], "max_days": e["hours"] / 24})
    for g in events:
        del g["t0_max"]; g["hours"] = round(g["hours"], 1); g["max_days"] = round(g["max_days"], 2); g["n"] = len(g["zones"])
    news_days = [e["hours"] / 24 for e in news]
    longest = max(episodes, key=lambda e: e["hours"]) if episodes else None
    recent_news = sum(e["hours"] for e in news if yr(e) >= 2017)
    one_hour = err.get(3600, 0)
    res = {
        "zone_hours_wrong": total, "by_kind_hours": hours, "episodes": n, "episodes_total": len(episodes),
        "zones_with_episode": len({e["zone"] for e in episodes}), "zones_by_kind": zones,
        "exposure_zone_hours": round(exposure_h, 1), "absent_zone_hours": round(absent_h, 1),
        "share_of_exposure": total / exposure_h if exposure_h else None,
        "news_median_days": statistics.median(news_days) if news_days else None,
        "longest": longest, "news_hours_2017_on": round(recent_news, 1),
        "error_hours_by_seconds": {str(k): round(v, 1) for k, v in sorted(err.items())},
        "share_one_hour": one_hour / total if total else None,
        "by_year": {y: by_year[y] for y in sorted(by_year)},
        "news_events": events,
    }
    res["predictions_2_10"] = {
        "P2": 200000 <= total <= 5000000,
        "P3": total > 0 and hours["past"] / total > 0.70,
        "P4": hours["retimed"] < hours["news"],
        "P5": 60 <= res["zones_with_episode"] <= 200,
        "P6": res["share_of_exposure"] is not None and 0.001 <= res["share_of_exposure"] <= 0.03,
        "P7": res["news_median_days"] is not None and 1 <= res["news_median_days"] <= 30,
        "P8": longest is not None and longest["hours"] > 365 * 24,
        "P9": hours["news"] > 0 and recent_news / hours["news"] < 0.10,
        "P10": res["share_one_hour"] is not None and res["share_one_hour"] >= 0.90,
    }
    return res


def synthetic():
    d = lambda *a: calendar.timegm(a + (0, 0, 0)) if len(a) == 3 else calendar.timegm(a)
    # zone A: final has DST 2005-03-27 -> 2005-10-30 (+3600). R1 lacks it (news), R2 (from 2005-04-10) has it.
    # zone B: final ends DST 2006-10-29; R0-R2 end it 2006-11-05, R3 (2007-01-15) corrects it (re-timed, a week).
    # zone C: final says +7200 from 1999-06-01 to 2000-06-01; every release but the final says 0 (past rewritten).
    A = (0, [(d(2005, 3, 27, 1, 0, 0), 3600), (d(2005, 10, 30, 1, 0, 0), 0)])
    Bf = (0, [(d(2006, 3, 26, 1, 0, 0), 3600), (d(2006, 10, 29, 1, 0, 0), 0)])
    Br = (0, [(d(2006, 3, 26, 1, 0, 0), 3600), (d(2006, 11, 5, 1, 0, 0), 0)])
    Cf = (0, [(d(1999, 6, 1), 7200), (d(2000, 6, 1), 0)])
    rels = {
        "r0": {"A": (0, []), "B": Br, "C": (0, [])},
        "r1": {"A": (0, []), "B": Br, "C": (0, [])},
        "r2": {"A": A, "B": Br, "C": (0, [])},
        "r3": {"A": A, "B": Bf, "C": (0, [])},
        "fin": {"A": A, "B": Bf, "C": Cf},
    }
    dates = {"r0": d(1998, 1, 1), "r1": d(2004, 1, 1), "r2": d(2005, 4, 10), "r3": d(2007, 1, 15), "fin": d(2026, 10, 27)}
    eps, ex, ab = analyse(["r0", "r1", "r2", "r3", "fin"], dates, rels)
    for e in eps:
        print(e["zone"], e["kind"], e["hours"], e["rel"], "->", e["corr"], e["lag_days"])
    k = {(e["zone"], e["kind"]) for e in eps}
    assert ("A", "news") in k and ("B", "retimed") in k and ("C", "past") in k and len(eps) == 3, eps
    a = [e for e in eps if e["zone"] == "A"][0]
    assert a["hours"] == (d(2005, 4, 10) - d(2005, 3, 27, 1, 0, 0)) / 3600
    print("synthetic ok; exposure h", ex)


def main():
    if sys.argv[1:] == ["--synthetic"]:
        return synthetic()
    tardir, work, outpath = sys.argv[1:4]
    tars = sorted(f for f in os.listdir(tardir) if f.startswith("tzdata") and f.endswith(".tar.gz") and f != "tzdatabeta.tar.gz")
    jobs = [(norm(f[6:-7]), os.path.join(tardir, f), work) for f in tars]
    with ProcessPoolExecutor(8) as ex:
        rel = dict(ex.map(compile_release, jobs))
    newest = max(rel, key=lambda n: (n[:4], n[4:]))
    news = news_dates(os.path.join(work, "src", newest, "NEWS"))
    ok = [n for n in rel if rel[n]["ok"] and n in news]
    ts = lambda s: calendar.timegm(tuple(map(int, s.split("-"))) + (0, 0, 0))
    order = sorted(ok, key=lambda n: (news[n], n))
    assert order[-1] == newest, order[-3:]
    dates = {n: ts(news[n]) for n in order}
    episodes, exposure_h, absent_h = analyse(order, dates, {n: rel[n]["zones"] for n in order})
    res = {"releases_total": len(rel), "releases_compiled": sum(1 for n in rel if rel[n]["ok"]),
           "failed": sorted(n for n in rel if not rel[n]["ok"]), "undated": sorted(n for n in rel if n not in news),
           "newest": newest, "first_life": order[0], "zones_final": len(rel[newest]["zones"])}
    res.update(summarise(episodes, exposure_h, absent_h))
    res["predictions"] = dict({"P1": res["releases_compiled"] == 252}, **res.pop("predictions_2_10"))
    res["release_dates"] = {n: news[n] for n in order}
    res["episodes_rows"] = episodes
    json.dump(res, open(outpath, "w"), indent=0)
    print(json.dumps({k: v for k, v in res.items() if k not in ("episodes_rows", "release_dates", "by_year", "news_events", "failed")},
                     indent=1))


if __name__ == "__main__":
    main()
