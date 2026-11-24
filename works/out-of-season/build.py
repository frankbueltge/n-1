"""Build works/out-of-season/ (project 26, session 3) from the data file written by projects/counted-as-one/build4.py.

Usage: python3 build.py WORK-DATA.json
Writes data.json (per overflow in U: identifier, receiving water, bathing and shellfish names, count, hours, 365 daily
hours at 0.1 h, the days counted spills begin, and the exact season hours from session2-per.json.gz; no start/stop row) and writes index.html from template.html with the figures taken
from projects/counted-as-one/session3.json. Nothing is fetched at runtime from anywhere but this directory.
"""
import gzip, json, os, sys

H = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]
D = json.load(open(src))
S = json.load(open(os.path.join(H, '..', '..', 'projects', 'counted-as-one', 'session3.json')))
assert len(D['overflows']) == S['U']
o = D['overflows']
# exact season hours from session 2's per-overflow file (the 0.1 h rounding of data.json would turn 3 short discharges into none)
P2 = {r['uid']: r for r in json.load(gzip.open(os.path.join(H, '..', '..', 'projects', 'counted-as-one', 'session2-per.json.gz'), 'rt'))}
none = sum(1 for r in o if P2[r['id']]['season_h'] == 0)
for r in o:  # exact season hours (session 2, summed durations clipped to the season) added beside the rounded days
    r['season'] = round(P2[r['id']]['season_h'], 2)
json.dump(D, open(os.path.join(H, 'data.json'), 'w'), separators=(',', ':'))
rounded_none = sum(1 for r in o if sum(r['days'][S['season_days'][0]:S['season_days'][1] + 1]) == 0)
f = lambda n: f'{round(n):,}'
rep = {'{{U}}': str(S['U']), '{{UHOURS}}': f(S['U_union_hours']), '{{USEASON}}': f(S['together_season_hours']),
       '{{USEASONPCT}}': f"{100 * S['together_season_hours'] / S['U_union_hours']:.1f}", '{{NONE}}': str(none),
       '{{UBATH}}': str(S['U_bathing']), '{{USHELL}}': str(S['U_shellfish'])}
t = open(os.path.join(H, 'template.html')).read()
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', len(o), 'overflows; none in season:', none, '(by the rounded days:', rounded_none, ')')
