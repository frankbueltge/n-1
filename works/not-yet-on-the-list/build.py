"""Build works/not-yet-on-the-list/ from the data file written by projects/before-the-report/build3.py (session 3 of project 25).

Usage: python3 build.py WORK-DATA.json

Writes data.json (every recall event's start and listing day, centre, gravest class and notice group; no event id, no firm, no
product) and index.html from template.html, with the figures taken from projects/before-the-report/session3.json. Nothing is
fetched at runtime from anywhere but this directory. openFDA data is public domain / CC0.
"""
import json, os, sys

H = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(sys.argv[1]))
S = json.load(open(os.path.join(H, '..', '..', 'projects', 'before-the-report', 'session3.json')))
assert len(src['rows']) == S['events']
rows = [r[:5] for r in src['rows']]
out = {'epoch': src['epoch'], 'fields': src['fields'][:5], 'centre': src['centre'], 'class': src['class'], 'notice': src['notice'],
       'years': src['years'], 'backlog': src['backlog'], 'rows': rows}
json.dump(out, open(os.path.join(H, 'data.json'), 'w'), separators=(',', ':'))
Y = S['by_year']
last = str(src['years'][-1])
f = lambda n: f'{n:,}'
rep = {'{{EVENTS}}': f(S['events']), '{{LAST}}': last, '{{FIRST}}': str(src['years'][0]),
       '{{MED}}': f(int(Y[last]['backlog_median'])), '{{MIN}}': f(Y[last]['backlog_min']), '{{MAX}}': f(Y[last]['backlog_max']),
       '{{MED13}}': f(int(Y['2013']['backlog_median'])),
       '{{BEGUN}}': f(Y[last]['begun']), '{{PUB}}': f(Y[last]['begun_public']),
       '{{PUBPCT}}': f"{100 * Y[last]['begun_public'] / Y[last]['begun']:.1f}"}
t = open(os.path.join(H, 'template.html')).read()
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', len(rows), 'events', os.path.getsize(os.path.join(H, 'data.json')), 'bytes')
