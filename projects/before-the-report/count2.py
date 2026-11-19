"""Project 25 session 2: whose word came first -- the firm's initial notice (public or consignees) per recall event, and how
long the register-first events waited. Definitions: SESSION2.md.

Usage: python3 -I count2.py <dir with food.json drug.json device.json> <out.json> <per-event out.json>
No firm or product name is read into the output.
"""
import json, sys, statistics, datetime, collections

CENTRES = ["food", "drug", "device"]
CLASSES = ["Class I", "Class II", "Class III"]
RANK = {"Class I": 0, "Class II": 1, "Class III": 2, "other": 3}
GROUPS = ["public", "listed-with-press", "ambiguous", "consignees", "unrecorded"]
AMBIG_PREFIX = "two or more of the following"


def d(s):
    if not isinstance(s, str) or len(s) != 8 or not s.isdigit():
        return None
    try:
        return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:]))
    except ValueError:
        return None


def group(s):
    if not isinstance(s, str) or not s.strip() or s.strip().lower() == "n/a":
        return "unrecorded"
    t = s.strip().lower()
    if t == "other":
        return "ambiguous"  # method not stated: may or may not have been public (JOURNAL.md, session 2, 02:05)
    if t == "press release":
        return "public"
    if t.startswith(AMBIG_PREFIX):
        return "ambiguous"
    if "press release" in t:
        return "listed-with-press"
    return "consignees"


def med(xs):
    return statistics.median(xs) if xs else None


def summ(ws):
    ws = sorted(ws)
    n = len(ws)
    if not n:
        return {"n": 0}
    q = lambda p: ws[min(n - 1, int(p * n))]
    return {"n": n, "median": med(ws), "p25": q(0.25), "p75": q(0.75), "p90": q(0.90), "max": ws[-1],
            "over90": sum(1 for w in ws if w > 90), "over365": sum(1 for w in ws if w > 365)}


def main(src, out, per_out):
    strings = collections.Counter()
    rec_groups = collections.Counter()
    E = collections.defaultdict(list)
    meta = {}
    for c in CENTRES:
        j = json.load(open(f"{src}/{c}.json"))
        meta[c] = {"meta_last_updated": j.get("meta", {}).get("last_updated"), "records": len(j["results"])}
        for r in j["results"]:
            s = r.get("initial_firm_notification")
            strings[(s or "").strip()] += 1
            g = group(s)
            rec_groups[(c, g)] += 1
            i, rp = d(r.get("recall_initiation_date")), d(r.get("report_date"))
            k = r.get("classification")
            E[(c, r.get("event_id"))].append({"g": g, "class": k if k in CLASSES else "other",
                                              "W": (rp - i).days if i and rp else None,
                                              "report": r.get("report_date") or "", "recall_number": r.get("recall_number")})
    events = []
    for (c, e), rs in E.items():
        gs = {x["g"] for x in rs}
        eg = next(g for g in GROUPS if g in gs)
        ws = [x["W"] for x in rs if x["W"] is not None]
        events.append({"centre": c, "event_id": e, "notice": eg, "class": min((x["class"] for x in rs), key=RANK.get),
                       "W": min(ws) if ws else None, "year": min(x["report"] for x in rs)[:4], "records": len(rs),
                       "mixed_notice": len(gs) > 1})
    res = {"meta": meta, "records": sum(m["records"] for m in meta.values()), "events": len(events)}
    res["top_strings"] = [[s, n] for s, n in strings.most_common(40)]
    res["distinct_strings"] = len(strings)
    res["record_groups"] = {c: {g: rec_groups[(c, g)] for g in GROUPS} for c in CENTRES}
    res["record_exact_press_release"] = {c: rec_groups[(c, "public")] for c in CENTRES}
    cnt = collections.Counter(x["notice"] for x in events)
    res["event_groups"] = {g: cnt[g] for g in GROUPS}
    res["event_group_share"] = {g: round(cnt[g] / len(events), 4) for g in GROUPS}
    res["events_mixed_notice"] = sum(1 for x in events if x["mixed_notice"])
    res["by_centre_class"] = {}
    for c in CENTRES:
        res["by_centre_class"][c] = {}
        for k in CLASSES:
            xs = [x for x in events if x["centre"] == c and x["class"] == k]
            gc = collections.Counter(x["notice"] for x in xs)
            res["by_centre_class"][c][k] = {
                "events": len(xs),
                "groups": {g: gc[g] for g in GROUPS},
                "share_public": round(gc["public"] / len(xs), 4) if xs else None,
                "W": {g: summ([x["W"] for x in xs if x["notice"] == g and x["W"] is not None]) for g in GROUPS}}
    yrs = sorted({x["year"] for x in events})
    res["by_year_centre_class1"] = {c: {y: {g: [len([x for x in events if x["centre"] == c and x["year"] == y and x["class"] == "Class I" and x["notice"] == g])]
                                            for g in ["public", "consignees"]} for y in yrs} for c in CENTRES}
    res["by_year_drug_consignees"] = {y: {k: summ([x["W"] for x in events if x["centre"] == "drug" and x["year"] == y and x["class"] == k
                                                   and x["notice"] == "consignees" and x["W"] is not None]).get("median")
                                          for k in ["Class I", "Class II"]} for y in yrs}
    reg = [x for x in events if x["notice"] == "consignees" and x["W"] is not None]
    res["register_first_all"] = summ([x["W"] for x in reg])
    res["longest_register_first_drug_class1"] = sorted(
        [x for x in reg if x["centre"] == "drug" and x["class"] == "Class I"], key=lambda x: -x["W"])[:3]
    json.dump(res, open(out, "w"), indent=1)
    json.dump(events, open(per_out, "w"))
    print(json.dumps({k: res[k] for k in ("records", "events", "event_groups", "event_group_share", "events_mixed_notice")}))
    print(res["top_strings"][:12])
    for c in CENTRES:
        for k in CLASSES:
            b = res["by_centre_class"][c][k]
            print(c, k, b["events"], b["share_public"], {g: b["W"][g].get("median") for g in ("public", "consignees")},
                  {g: b["groups"][g] for g in GROUPS})


if __name__ == "__main__":
    main(*sys.argv[1:4])
