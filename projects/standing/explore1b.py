"""Project 22, session 1, exploratory: which publications hold the species names of a given year, with their statuses.
Usage: python3 -I explore1b.py <wcvp_names.csv> <year> <out.json>"""
import csv, json, sys
from collections import Counter, defaultdict
csv.field_size_limit(10**9)
p = Counter(); s = defaultdict(Counter)
for d in csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='|', quoting=csv.QUOTE_NONE):
    if d['taxon_rank'] == 'Species' and (d['first_published'] or '').startswith('(' + sys.argv[2]):
        p[d['place_of_publication']] += 1; s[d['place_of_publication']][d['taxon_status']] += 1
out = {'year': sys.argv[2], 'top': [[k, n, dict(s[k])] for k, n in p.most_common(5)]}
json.dump(out, open(sys.argv[3], 'w'), indent=1); print(json.dumps(out))
