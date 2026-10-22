"""Shared parsing for project 16: stopped studies, stated reasons, stop months, the registered rule."""
import glob, json, re

RULE = re.compile(r"covid|coronavirus|corona virus|sars-?cov|2019-ncov|pandemic|lockdown", re.I)

def month(dstruct):
    """'YYYY-MM' from a date struct {'date': 'YYYY-MM[-DD]', 'type': ...}."""
    return dstruct["date"][:7] if dstruct and dstruct.get("date") else None

def load(rawdir):
    rows = []
    for p in sorted(glob.glob(rawdir + "/page_*.json")):
        for s in json.load(open(p)).get("studies", []):
            ps = s.get("protocolSection", {})
            ident = ps.get("identificationModule", {})
            st = ps.get("statusModule", {})
            design = ps.get("designModule", {})
            why = (st.get("whyStopped") or "").strip()
            status = st.get("overallStatus")
            comp, prim = st.get("completionDateStruct"), st.get("primaryCompletionDateStruct")
            stop = None
            if status in ("TERMINATED", "WITHDRAWN"):
                if comp and comp.get("type") == "ACTUAL":
                    stop = month(comp)
                elif prim and prim.get("type") == "ACTUAL":
                    stop = month(prim)
            rows.append({"nct": ident.get("nctId"), "status": status, "why": why,
                         "type": design.get("studyType"), "stop": stop,
                         "start": month(st.get("startDateStruct")),
                         "lastupd": month(st.get("lastUpdatePostDateStruct")),
                         "flag": bool(RULE.search(why)) if why else False})
    return rows
