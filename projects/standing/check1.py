"""Project 22, session 1: the registered check could not run (POWO behind a bot challenge). Exploratory substitute: the same twelve
sampled names (seed 20261104, session1.json) against Kew's WCVP deposit on GBIF (dataset f382f0ce-323a-4091-bb9f-add557f3a9a2), read
through GBIF's open species API, one request per 2 s. Usage: python3 -I check1.py <wcvp_names.csv> <session1.json> <out.json>"""
import csv, json, sys, time, urllib.request, urllib.parse
csv.field_size_limit(10**9)
DS = 'f382f0ce-323a-4091-bb9f-add557f3a9a2'
ids = {s['plant_name_id']: s for s in json.load(open(sys.argv[2]))['check_sample']}
rows = {}
for d in csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='|', quoting=csv.QUOTE_NONE):
    if d['plant_name_id'] in ids:
        rows[d['plant_name_id']] = (d['taxon_name'], d['taxon_authors'], d['taxon_status'])
MAP = {'ACCEPTED': 'Accepted', 'SYNONYM': 'Synonym', 'HOMOTYPIC_SYNONYM': 'Synonym', 'HETEROTYPIC_SYNONYM': 'Synonym',
       'DOUBTFUL': 'Unplaced'}
out = []
for pid, (name, auth, st) in rows.items():
    q = urllib.parse.urlencode({'datasetKey': DS, 'q': name, 'rank': 'SPECIES', 'limit': 20})
    try:
        r = json.load(urllib.request.urlopen('https://api.gbif.org/v1/species/search?' + q, timeout=30))
        hits = [h for h in r.get('results', []) if h.get('canonicalName') == name]
        same = [h for h in hits if (h.get('authorship') or '').strip() == (auth or '').strip()] or hits
        g = [h.get('taxonomicStatus') for h in same]
    except Exception as e:
        g = ['error: %s' % e]
    agree = any(MAP.get(x) == st or (x and x.lower() == st.lower()) for x in g)
    out.append({'plant_name_id': pid, 'taxon_name': name, 'wcvp_2026_06_status': st, 'gbif_statuses': g, 'agree': agree})
    time.sleep(2)
res = {'registered_check': 'not run: POWO answered with a bot challenge (02:08 UTC), not circumvented',
       'substitute': 'exploratory, GBIF copy of WCVP', 'n': len(out), 'agree': sum(o['agree'] for o in out), 'rows': out}
json.dump(res, open(sys.argv[3], 'w'), indent=1); print(json.dumps(res, indent=1))
