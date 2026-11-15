#!/usr/bin/env python3
"""Project 24, session 3 check (registered in SESSION3.md). Shares no code with count3.py.

Usage: python3 -I check3.py STRIPPED NAMES PER.json OUT.json   (STRIPPED and NAMES decompressed)
Twelve never-found-alone sequences (seed 20261115): grep -c -F of the whole shown run == holders + 1.
Six of the 1,000 most named (same seed): grep -c -w of the A-number on NAMES, minus its own line if it names itself, == Named.
Separately: every link of the deepest chain by grep -F of the lower run in the upper line.
"""
import json, random, subprocess, sys

stripped, names, perp, outp = sys.argv[1:5]
per = json.load(open(perp))
rng = random.Random(20261115)
nv = sorted(per['never_found_alone'], key=lambda e: e['a'])
pick = rng.sample(nv, 12)
top = sorted(per['named_top1000'], key=lambda e: e[0])
pick2 = rng.sample(top, 6)
line_of = {}
for l in open(stripped, encoding='utf-8'):
    if l.startswith('A'):
        a, _, body = l.rstrip('\n').partition(' ')
        line_of[a] = body
def grepc(args, pat, f):
    r = subprocess.run(['grep', '-c'] + args + ['--', pat, f], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)
res = []
for e in pick:
    run = line_of[e['a']]
    c = grepc(['-F'], run, stripped)
    res.append({'a': e['a'], 'kind': 'holders', 'counted': e['holders'], 'grep_lines': c, 'ok': c == e['holders'] + 1})
for a, named, _ in pick2:
    c = grepc(['-w'], a, names)
    own = subprocess.run(['grep', '-m1', '^' + a + ' ', names], capture_output=True, text=True).stdout
    selfref = (own.count(a) > 1) if own else False   # its own line names it beyond the leading A-number
    v = c - (1 if own else 0)
    res.append({'a': a, 'kind': 'named', 'counted': named, 'grep_lines_minus_own': v, 'own_line_names_itself': selfref, 'ok': v == named})
out = {'checks': res, 'held': sum(r['ok'] for r in res), 'of': len(res)}
s3 = json.load(open(perp.replace('-per', '')))
chain = s3['deepest_chains'][0]
links = []
for lo, hi in zip(chain[1:], chain[:-1]):
    r = subprocess.run(['grep', '-c', '-F', '--', line_of[lo['a']], '-'], input=hi['a'] + ' ' + line_of[hi['a']] + '\n',
                       capture_output=True, text=True)
    links.append({'lower': lo['a'], 'upper': hi['a'], 'ok': r.stdout.strip() == '1'})
out['chain_links'] = links
json.dump(out, open(outp, 'w'), indent=1)
print(out['held'], 'of', out['of'], '; chain links', sum(l['ok'] for l in links), 'of', len(links))
