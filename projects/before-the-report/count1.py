"""Project 25 session 1: the wait between a recall's start and the FDA enforcement report that lists it.

Usage: python3 -I count1.py <dir with food.json drug.json device.json> <out.json> <per-record out.json>
Each input is the unzipped openFDA enforcement file ({"meta":..., "results":[...]}).
Definitions: SELECTION.md. No firm name is read into the output.
"""
import json, sys, statistics, datetime, collections

CENTRES = ["food", "drug", "device"]
CLASSES = ["Class I", "Class II", "Class III"]


def d(s):
    if not isinstance(s, str) or len(s) != 8 or not s.isdigit():
        return None
    try:
        return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:]))
    except ValueError:
        return None


def med(xs):
    return statistics.median(xs) if xs else None


def summ(ws):
    ws = sorted(ws)
    n = len(ws)
    if not n:
        return {"n": 0}
    q = lambda p: ws[min(n - 1, int(p * n))]
    return {"n": n, "median": med(ws), "p10": q(0.10), "p25": q(0.25), "p75": q(0.75), "p90": q(0.90),
            "max": ws[-1], "min": ws[0], "neg": sum(1 for w in ws if w < 0),
            "over365": sum(1 for w in ws if w > 365), "share_over365": round(sum(1 for w in ws if w > 365) / n, 4),
            "share_neg": round(sum(1 for w in ws if w < 0) / n, 4)}


def main(src, out, per_out):
    per = []
    meta = {}
    for c in CENTRES:
        j = json.load(open(f"{src}/{c}.json"))
        meta[c] = {"meta_last_updated": j.get("meta", {}).get("last_updated"), "records": len(j["results"])}
        for r in j["results"]:
            i, rp, cl = d(r.get("recall_initiation_date")), d(r.get("report_date")), d(r.get("center_classification_date"))
            k = r.get("classification")
            per.append({"centre": c, "recall_number": r.get("recall_number"), "event_id": r.get("event_id"),
                        "class": k if k in CLASSES else "other", "init": r.get("recall_initiation_date"),
                        "report": r.get("report_date"), "classified": r.get("center_classification_date"),
                        "W": (rp - i).days if i and rp else None, "C": (cl - i).days if i and cl else None,
                        "report_year": rp.year if rp else None})
    res = {"meta": meta, "records": len(per)}
    dated = [p for p in per if p["W"] is not None]
    res["undated_W"] = len(per) - len(dated)
    res["all"] = summ([p["W"] for p in dated])
    res["by_class"] = {k: summ([p["W"] for p in dated if p["class"] == k]) for k in CLASSES + ["other"]}
    res["class_counts"] = dict(collections.Counter(p["class"] for p in per))
    res["by_centre"] = {c: summ([p["W"] for p in dated if p["centre"] == c]) for c in CENTRES}
    res["by_centre_class"] = {c: {k: summ([p["W"] for p in dated if p["centre"] == c and p["class"] == k]) for k in CLASSES}
                              for c in CENTRES}
    yrs = sorted({p["report_year"] for p in dated})
    res["by_report_year"] = {y: summ([p["W"] for p in dated if p["report_year"] == y]) for y in yrs}
    res["by_report_year_class"] = {y: {k: summ([p["W"] for p in dated if p["report_year"] == y and p["class"] == k])
                                       for k in CLASSES} for y in yrs}
    reps = [p["report"] for p in per if d(p["report"])]
    res["report_date_range"] = [min(reps), max(reps)] if reps else None
    inits = [p["init"] for p in per if d(p["init"])]
    res["init_date_range"] = [min(inits), max(inits)] if inits else None
    cs = [p["C"] for p in per if p["C"] is not None]
    res["C_all"] = summ(cs)
    res["C_by_class"] = {k: summ([p["C"] for p in per if p["C"] is not None and p["class"] == k]) for k in CLASSES}
    res["undated_C"] = len(per) - len(cs)
    # events
    ev = collections.defaultdict(list)
    for p in per:
        if p["event_id"] not in (None, ""):
            ev[(p["centre"], p["event_id"])].append(p)
    rank = {"Class I": 0, "Class II": 1, "Class III": 2, "other": 3}
    ews, ecl = [], collections.Counter()
    eclass_w = collections.defaultdict(list)
    for key, ps in ev.items():
        ii = [d(p["init"]) for p in ps if d(p["init"])]
        rr = [d(p["report"]) for p in ps if d(p["report"])]
        g = min((p["class"] for p in ps), key=lambda k: rank[k])
        ecl[g] += 1
        if ii and rr:
            w = (min(rr) - min(ii)).days
            ews.append(w)
            eclass_w[g].append(w)
    res["events"] = {"n": len(ev), "records_without_event_id": sum(1 for p in per if p["event_id"] in (None, "")),
                     "W": summ(ews), "gravest_class_counts": dict(ecl),
                     "W_by_gravest_class": {k: summ(eclass_w[k]) for k in CLASSES}}
    longest = sorted(dated, key=lambda p: -p["W"])[:3]
    res["longest"] = [{k: p[k] for k in ("centre", "recall_number", "class", "init", "report", "W")} for p in longest]
    json.dump(res, open(out, "w"), indent=1)
    json.dump(per, open(per_out, "w"))
    print(json.dumps({k: res[k] for k in ("records", "undated_W", "all", "class_counts", "report_date_range")}, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
