"""Project 25 session 3: the work's data -- every recall event's start S and listing L, and, per day, the number of events begun and
not yet on the list. Definitions: SESSION3.md. Notice group and gravest class from count2.py, imported unchanged.

Usage: python3 -I build3.py <dir with food.json drug.json device.json> <summary out.json> <work data out.json>
No firm or product name, and no reason text, is read into either output.
"""
import json, sys, os, datetime, collections, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from count2 import CENTRES, CLASSES, RANK, GROUPS, d, group  # noqa: E402

EPOCH = datetime.date(2012, 1, 1)
CENTRE_CODE = {"food": 0, "drug": 1, "device": 2}
CLASS_CODE = {"Class I": 1, "Class II": 2, "Class III": 3, "other": 0}
GROUP_CODE = {g: i for i, g in enumerate(GROUPS)}


def main(src, out, data_out):
    E = collections.defaultdict(list)
    meta = {}
    for c in CENTRES:
        j = json.load(open(f"{src}/{c}.json"))
        meta[c] = {"meta_last_updated": j.get("meta", {}).get("last_updated"), "records": len(j["results"])}
        for r in j["results"]:
            k = r.get("classification")
            E[(c, r.get("event_id"))].append({"g": group(r.get("initial_firm_notification")),
                                              "class": k if k in CLASSES else "other",
                                              "S": d(r.get("recall_initiation_date")), "L": d(r.get("report_date"))})
    events, excluded = [], []
    for (c, e), rs in E.items():
        gs = {x["g"] for x in rs}
        ss = [x["S"] for x in rs if x["S"]]
        ls = [x["L"] for x in rs if x["L"]]
        ev = {"centre": c, "event_id": e, "notice": next(g for g in GROUPS if g in gs),
              "class": min((x["class"] for x in rs), key=RANK.get),
              "S": min(ss) if ss else None, "L": min(ls) if ls else None}
        if not ev["S"] or not ev["L"] or ev["L"] < ev["S"] or ev["S"] < EPOCH - datetime.timedelta(days=3650):
            excluded.append({"centre": c, "event_id": e, "S": str(ev["S"]), "L": str(ev["L"])})
            continue
        events.append(ev)
    last_export = max(ev["L"] for ev in events)
    years = [y for y in range(2013, last_export.year + 1) if datetime.date(y, 12, 31) <= last_export - datetime.timedelta(days=365)]
    res = {"meta": meta, "events_all": len(E), "events": len(events), "excluded": excluded, "last_listing": str(last_export),
           "years": years, "by_year": {}}
    # day-by-day counts for every complete year
    for y in years:
        a, b = datetime.date(y, 1, 1), datetime.date(y, 12, 31)
        days = (b - a).days + 1
        diff = [0] * (days + 1)
        base = 0
        for ev in events:
            s, l = ev["S"], ev["L"]  # active on [s, l)
            if l <= a or s > b:
                continue
            i = max(0, (s - a).days)
            j = min(days, (l - a).days)
            if i < j:
                diff[i] += 1
                diff[j] -= 1
        backlog, run = [], 0
        for i in range(days):
            run += diff[i]
            backlog.append(run)
        listed = [ev for ev in events if a <= ev["L"] <= b]
        begun = [ev for ev in events if a <= ev["S"] <= b]
        wd = collections.Counter(ev["L"].weekday() for ev in listed)
        top_wd, top_n = wd.most_common(1)[0] if wd else (None, 0)
        res["by_year"][y] = {
            "backlog_median": statistics.median(backlog), "backlog_min": min(backlog), "backlog_max": max(backlog),
            "backlog_max_day": str(a + datetime.timedelta(days=backlog.index(max(backlog)))),
            "backlog_min_day": str(a + datetime.timedelta(days=backlog.index(min(backlog)))),
            "listed": len(listed), "begun": len(begun),
            "listing_weekday_top": top_wd, "listing_weekday_share": round(top_n / len(listed), 4) if listed else None,
            "listing_days": len({ev["L"] for ev in listed}),
            "begun_public": sum(1 for ev in begun if ev["notice"] == "public"),
            "begun_public_share": round(sum(1 for ev in begun if ev["notice"] == "public") / len(begun), 4) if begun else None,
            "backlog": backlog}
    # the work's data: one row per event, day numbers from EPOCH
    rows = sorted(([(ev["S"] - EPOCH).days, (ev["L"] - EPOCH).days, CENTRE_CODE[ev["centre"]], CLASS_CODE[ev["class"]],
                    GROUP_CODE[ev["notice"]], ev["event_id"]] for ev in events))
    data = {"epoch": str(EPOCH), "fields": ["S", "L", "centre", "class", "notice", "event_id"],
            "centre": list(CENTRE_CODE), "class": ["other", "Class I", "Class II", "Class III"], "notice": GROUPS,
            "years": years, "backlog": {str(y): res["by_year"][y]["backlog"] for y in years}, "rows": rows}
    with open(data_out, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    res["data_bytes"] = os.path.getsize(data_out)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("events_all", "events", "last_listing", "years", "data_bytes")}))
    print("excluded", len(excluded), excluded[:5])
    for y in years:
        b = {k: v for k, v in res["by_year"][y].items() if k != "backlog"}
        print(y, b)


if __name__ == "__main__":
    main(*sys.argv[1:4])
