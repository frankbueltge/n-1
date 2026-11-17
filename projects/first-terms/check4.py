#!/usr/bin/env python3
"""Project 24 session 4, check P7 (registered in SESSION4.md). Shares no code with build4.py or the work's build:
twelve entries drawn from works/never-the-only-answer/data/entries.json with seed 20261117; for each, `grep -c -F`
of ",t1,...,tn," on the decompressed stripped file must equal the entry's listed answers (holders + 1).
Usage: python3 check4.py STRIPPED_DECOMPRESSED OUT.json"""
import json, random, subprocess, sys
E = json.load(open('../../works/never-the-only-answer/data/entries.json'))
rows = []
for e in random.Random(20261117).sample(E, 12):
    g = int(subprocess.run(['grep', '-c', '-F', ',' + e[2] + ',', sys.argv[1]], capture_output=True, text=True).stdout.strip() or 0)
    rows.append({'a': e[0], 'terms': len(e[2].split(',')), 'answers_listed': e[3] + 1, 'grep_lines': g, 'agree': g == e[3] + 1})
out = {'drawn': 12, 'agree': sum(r['agree'] for r in rows), 'rows': rows}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps(out, indent=1))
