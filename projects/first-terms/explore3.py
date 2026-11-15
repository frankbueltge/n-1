#!/usr/bin/env python3
"""Project 24, session 3, exploratory (not registered): who is held, by length and by name.
Usage: python3 -I explore3.py session3.json session3-per.json NAMES STRIPPED OUT.json"""
import json, sys, collections
s3, per, namesf, strippedf, outp = sys.argv[1:6]
terms = {}
for l in open(strippedf, encoding='utf-8'):
    if l.startswith('A'):
        a, _, b = l.rstrip('\n').partition(' '); terms[a] = b.strip(',')
o = json.load(open(s3)); p = json.load(open(per))
names = {}
for l in open(namesf, encoding='utf-8', errors='replace'):
    if l.startswith('A'):
        a, _, n = l.rstrip('\n').partition(' '); names[a] = n
nv = p['never_found_alone']
bylen = collections.Counter(min(e['n'], 11) for e in nv)
heavy = [e for e in nv if e['holders'] > 100]
dup = [e for e in nv if names.get(e['a'], '').lower().startswith(('duplicate', 'erroneous', 'incorrect', 'a variant of', 'erroneous version'))]
heavy_len = collections.Counter(min(e['n'], 11) for e in heavy)
words = collections.Counter()
for e in heavy:
    for w in ('prime', 'factorial', 'square', 'Fibonacci', 'problem', 'only', 'known', 'conjecture', 'all', 'complete', 'finite'):
        if w.lower() in names.get(e['a'], '').lower(): words[w] += 1
out = {'never_by_length_capped_11': dict(sorted(bylen.items())), 'held_by_over_100': len(heavy),
       'held_by_over_100_by_length': dict(sorted(heavy_len.items())),
       'held_by_over_100_name_words': dict(words.most_common()),
       'never_named_duplicate_or_erroneous': len(dup),
       'heaviest_30': [{'a': e['a'], 'n': e['n'], 'holders': e['holders'], 'name': names.get(e['a'], ''), 'terms': terms[e['a']]} for e in
                       sorted(nv, key=lambda e: (-e['holders'], e['a']))[:30]]}
json.dump(out, open(outp, 'w'), indent=1)
print({k: v for k, v in out.items() if k != 'heaviest_30'})
for e in out['heaviest_30']: print(e['a'], e['n'], e['holders'], e['name'][:100])
