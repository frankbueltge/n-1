#!/usr/bin/env python3
"""Project 24 session 2, exploratory (not registered): for eight sequences everyone knows, which other sequences show their whole
shown run inside their own (grep -F on the decompressed file, not the count's code). Usage: python3 -I explore2c.py STRIPPED.txt NAMES.gz OUT.json"""
import json, sys, subprocess, gzip
txt = sys.argv[1]
names = {}
with gzip.open(sys.argv[2], 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        if line.startswith('A'):
            a, _, n = line.rstrip('\n').partition(' '); names[a] = n
rows = {}
for line in open(txt):
    if line.startswith('A'):
        a, _, b = line.rstrip('\n').partition(' '); rows[a] = b
out = []
for a in ('A000004', 'A000012', 'A000027', 'A000040', 'A000045', 'A000108', 'A000142', 'A000290'):
    run = rows[a]
    p = subprocess.run(['grep', '-F', '--', run, txt], capture_output=True, text=True)
    holders = [l.split(' ')[0] for l in p.stdout.splitlines() if not l.startswith(a + ' ')]
    twins = [h for h in holders if rows[h] == run]
    out.append({'a': a, 'name': names[a], 'shown': run.strip(',').count(',') + 1, 'held_by': len(holders), 'twins': len(twins),
                'first_holders': [[h, names.get(h, '')[:120]] for h in holders[:3]]})
json.dump(out, open(sys.argv[3], 'w'), indent=1); print(json.dumps(out, indent=1))
