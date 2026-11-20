"""Project 25 session 3, exploratory (not registered): the registered predictions P2, P4, P5, P6 name 2025, but the registered rule
for the work's years (complete calendar years ending at least 365 days before the latest listing) excludes 2025. This computes 2025
with build3.py's definitions, unchanged, as a lower bound (events begun in 2025 and not listed by the export are not in the files).

Usage: python3 -I explore3.py <dir with food.json drug.json device.json> <out.json>
"""
import json, sys, os, datetime, collections, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from count2 import CENTRES, CLASSES, RANK, GROUPS, d, group  # noqa: E402


def main(src, out, y=2025):
    E = collections.defaultdict(list)
    for c in CENTRES:
        for r in json.load(open(f"{src}/{c}.json"))["results"]:
            k = r.get("classification")
            E[(c, r.get("event_id"))].append((group(r.get("initial_firm_notification")), d(r.get("recall_initiation_date")),
                                              d(r.get("report_date"))))
    ev = []
    for rs in E.values():
        ss = [x[1] for x in rs if x[1]]; ls = [x[2] for x in rs if x[2]]
        gs = {x[0] for x in rs}
        if ss and ls and min(ls) >= min(ss) and min(ss).year > 2000:
            ev.append((min(ss), min(ls), next(g for g in GROUPS if g in gs)))
    a, b = datetime.date(y, 1, 1), datetime.date(y, 12, 31)
    backlog = [sum(1 for s, l, _ in ev if s <= a + datetime.timedelta(days=i) < l) for i in range((b - a).days + 1)]
    listed = [e for e in ev if a <= e[1] <= b]; begun = [e for e in ev if a <= e[0] <= b]
    wd = collections.Counter(e[1].weekday() for e in listed)
    res = {"year": y, "backlog_median": statistics.median(backlog), "backlog_min": min(backlog), "backlog_max": max(backlog),
           "listed": len(listed), "begun": len(begun), "listing_weekdays": dict(wd),
           "begun_public": sum(1 for e in begun if e[2] == "public"),
           "begun_public_share": round(sum(1 for e in begun if e[2] == "public") / len(begun), 4)}
    json.dump(res, open(out, "w"), indent=1)
    print(res)


if __name__ == "__main__":
    main(*sys.argv[1:3])
