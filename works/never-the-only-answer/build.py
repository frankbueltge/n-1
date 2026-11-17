"""Build works/never-the-only-answer/ from the data file written by projects/first-terms/build4.py (session 4 of project 24).

Usage: python3 build.py DATA.json

Writes data/entries.json (every never-found-alone entry: A-number, name, shown run, number of holders, shard) and
data/h-NN.json (the holders of the entries in shard NN, each with its A-number, name, the run's position and up to three
shown terms on either side, and its number of shown terms), then index.html from template.html. Nothing is fetched at
runtime from anywhere but this directory. Derived from The On-Line Encyclopedia of Integer Sequences, CC BY-SA 4.0.
"""
import json, os, sys, glob

H = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(H, 'data')
PER = 128
NAMED = [('A000045', 'Fibonacci numbers'), ('A000040', 'primes'), ('A000290', 'squares'), ('A000142', 'factorials'),
         ('A000027', 'counting numbers'), ('A146968', "Brocard's problem"), ('A222011', 'division algebras')]

data = json.load(open(sys.argv[1]))
T, E = data['seqs'], data['entries']
S = json.load(open(os.path.join(H, '..', '..', 'projects', 'first-terms', 'session4.json')))
assert len(E) == S['never_found_alone'] and sum(len(e[2]) for e in E) == S['holdings']
os.makedirs(D, exist_ok=True)
for f in glob.glob(os.path.join(D, 'h-*.json')):
    os.remove(f)
entries, shard = [], {}
for i, (s, run, hs) in enumerate(E):
    entries.append([T[s][0], T[s][1], run, len(hs), i // PER])
    shard.setdefault(i // PER, {})[str(i)] = [[T[t][0], T[t][1], k, b, a, L] for t, k, b, a, L in hs]
json.dump(entries, open(os.path.join(D, 'entries.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
for n, v in shard.items():
    json.dump(v, open(os.path.join(D, f'h-{n:02d}.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
sizes = [os.path.getsize(f) for f in glob.glob(os.path.join(D, '*.json'))]
assert max(sizes) <= 25 * 10**6
ix = {e[0]: e for e in entries}
named = []
for a, label in NAMED:
    named.append(f'<li><button type="button" data-a="{a}">{label}</button> <span>{ix[a][3] + 1:,} answers</span></li>')
f = lambda n: f'{n:,}'
rep = {'{{SEQS}}': f(S['sequences']), '{{NFA}}': f(S['never_found_alone']), '{{HOLD}}': f(S['holdings']),
       '{{BROC}}': f(ix['A146968'][3] + 1), '{{NAMED}}': '\n    '.join(named)}
t = open(os.path.join(H, 'template.html')).read()
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', len(entries), 'entries', len(shard), 'shards', 'largest', max(sizes), 'total', sum(sizes))
