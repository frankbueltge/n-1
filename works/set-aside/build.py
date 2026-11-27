"""Build works/set-aside/index.html (project 27, session 3) from template.html, with the figures taken from
projects/the-lowest-code/session3.json, session2.json, session1.json and explore3.json. data.json is written by
projects/the-lowest-code/build5.py. Nothing is fetched at runtime from anywhere but this directory. Usage: python3 build.py"""
import json, os

H = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(H, '..', '..', 'projects', 'the-lowest-code')
S3 = json.load(open(os.path.join(P, 'session3.json')))
S2 = json.load(open(os.path.join(P, 'session2.json')))
E3 = json.load(open(os.path.join(P, 'explore3.json')))
D = json.load(open(os.path.join(H, 'data.json')))
assert len(D['strokes']) == S3['P1_strokes']
rep = {'{{N}}': f"{S3['P1_strokes']:,}", '{{RISES}}': f"{S2['rises']:,}", '{{H}}': f"{S3['held']:,}", '{{F}}': f"{S3['fell_back']:,}",
       '{{O}}': f"{S3['other']:,}", '{{FPCT}}': f"{100 * S2['P1_share_falls_back_next']:.1f}", '{{HPCT}}': f"{100 * S2['P2_share_holds']:.1f}",
       '{{R95}}': f"{100 * E3['by_year']['1995']['silent_rate']:.1f}", '{{R24}}': f"{100 * E3['by_year']['2024']['silent_rate']:.1f}"}
t = open(os.path.join(H, 'template.html')).read()
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', rep)
