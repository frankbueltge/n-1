"""Project 22, session 1: exploratory, after the registered count (not registered; findings marked so).
Usage: python3 -I explore1.py <wcvp_names.csv> <out.json>"""
import csv, json, re, sys
from collections import Counter, defaultdict
csv.field_size_limit(10**9)
Y = re.compile(r'(?<!\d)(\d{4})(?!\d)')
def year_of(s):
    for m in Y.finditer(s or ''):
        y = int(m.group(1))
        if 1753 <= y <= 2026: return y
by_dec = defaultdict(Counter); by_year = defaultdict(Counter); book = Counter(); dec_nobook = defaultdict(Counter)
for d in csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='|', quoting=csv.QUOTE_NONE):
    if d['taxon_rank'] != 'Species': continue
    y = year_of(d['first_published'])
    if y is None: continue
    st = d['taxon_status']; homo = d['homotypic_synonym'] == 'T'
    k = 'standing' if st == 'Accepted' else ('moved' if homo else 'merged') if st == 'Synonym' else st
    dec = min(y // 10 * 10, 2020)
    by_dec[dec][k] += 1; by_year[y][k] += 1
    if d['place_of_publication'] == 'Revis. Gen. Pl.' and y == 1891: book[k] += 1
    else: dec_nobook[dec][k] += 1
def tab(c):
    n = sum(c.values()); syn = c['moved'] + c['merged']
    return {'n': n, 'share_standing': round(c['standing'] / n, 4) if n else None,
            'moved_share_of_synonyms': round(c['moved'] / syn, 4) if syn else None, **dict(c)}
years = {y: tab(c) for y, c in by_year.items()}
big = [(y, t) for y, t in years.items() if t['n'] >= 1000]
out = {
  'note': 'exploratory; homotypic flag found coded "T" (registered belief was TRUE), so moved/merged here are not the registered P6/P7',
  'decades_with_moved': {str(d): tab(c) for d, c in sorted(by_dec.items())},
  'revis_gen_pl_1891': tab(book),
  'decades_without_that_book': {str(d): tab(c) for d, c in sorted(dec_nobook.items())},
  'years_n_ge_1000_lowest_share': sorted(([y, t['n'], t['share_standing']] for y, t in big), key=lambda r: r[2])[:10],
  'years_largest': sorted(([y, t['n'], t['share_standing']] for y, t in years.items()), key=lambda r: -r[1])[:10],
  'year_1753': years.get(1753),
  'years_share': {str(y): [t['n'], t['share_standing']] for y, t in sorted(years.items())},
  'years_kinds': {str(y): dict(c) for y, c in sorted(by_year.items())},
}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('years_share', 'decades_without_that_book')}, indent=1)[:6000])
