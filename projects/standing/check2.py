"""Project 22, session 2: the registered check (SESSION2.md, P12), as information. The twelve changed names sampled by count2.py (seed
20261105) looked up in Kew's WCVP deposit on GBIF (dataset f382f0ce-323a-4091-bb9f-add557f3a9a2) through GBIF's open species API, one
request per 2 s. Usage: python3 -I check2.py <wcvp_v16.zip> <wcvp_v10.zip> <session2.json> <out.json>"""
import csv, io, json, sys, time, urllib.request, urllib.parse, zipfile
csv.field_size_limit(10**9)
DS = 'f382f0ce-323a-4091-bb9f-add557f3a9a2'
sample = {s['plant_name_id']: s for s in json.load(open(sys.argv[3]))['check_sample']}


def rows(path):
    z = zipfile.ZipFile(path)
    with z.open([n for n in z.namelist() if n.endswith('wcvp_names.csv')][0]) as raw:
        for d in csv.DictReader(io.TextIOWrapper(raw, encoding='utf-8', newline=''), delimiter='|', quoting=csv.QUOTE_NONE):
            if d['plant_name_id'] in sample:
                yield d


v16 = {d['plant_name_id']: d for d in rows(sys.argv[1])}
v10 = {d['plant_name_id']: d for d in rows(sys.argv[2])}
out = []
for pid, s in sample.items():
    d = v16[pid]
    name, auth = d['taxon_name'], d['taxon_authors']
    q = urllib.parse.urlencode({'datasetKey': DS, 'q': name, 'rank': 'SPECIES', 'limit': 20})
    try:
        r = json.load(urllib.request.urlopen('https://api.gbif.org/v1/species/search?' + q, timeout=30))
        hits = [h for h in r.get('results', []) if h.get('canonicalName') == name]
        same = [h for h in hits if (h.get('authorship') or '').strip() == (auth or '').strip()] or hits
        g = [h.get('taxonomicStatus') for h in same]
    except Exception as e:
        g = ['error: %s' % e]
    out.append({'plant_name_id': pid, 'taxon_name': name, 'year': s['year'],
                'v10': [v10[pid]['taxon_status'], v10[pid]['homotypic_synonym'], v10[pid]['accepted_plant_name_id']],
                'v16': [d['taxon_status'], d['homotypic_synonym'], d['accepted_plant_name_id']],
                'kinds': [s['v10'], s['v16']], 'gbif_statuses': g})
    time.sleep(2)
json.dump({'check': 'P12, information: which release GBIF copy follows', 'rows': out}, open(sys.argv[4], 'w'), indent=1)
for o in out:
    print(o['taxon_name'], o['kinds'], o['v10'][:2], o['v16'][:2], o['gbif_statuses'])
