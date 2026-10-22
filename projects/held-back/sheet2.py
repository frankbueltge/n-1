"""Project 15, session 2: draws the 20 checked pairs, stratified by the machine flag, and writes the sheet (state, treaty) and the
key (flags) separately. Prints the sheet only."""
import json, random
import lib2

f = lib2.flags()
matched = sorted(k for k, v in f.items() if v is not None)
flagged = [k for k in matched if f[k]]
unflagged = [k for k in matched if not f[k]]
rng = random.Random(20261023)
a = rng.sample(flagged, min(10, len(flagged)))
b = rng.sample(unflagged, 20 - len(a))
items = a + b
rng.shuffle(items)
sheet = [{'item': i + 1, 'state': c, 'treaty': t} for i, (c, t) in enumerate(items)]
key = [{'item': i + 1, 'state': c, 'treaty': t, 'flag': bool(f[(c, t)]), 'years': sorted({y for y, _ in f[(c, t)]})}
       for i, (c, t) in enumerate(items)]
json.dump({'seed': 20261023, 'items': sheet}, open('sheet2.json', 'w'), indent=1, ensure_ascii=False)
json.dump({'seed': 20261023, 'items': key}, open('key2.json', 'w'), indent=1, ensure_ascii=False)
for s in sheet:
    print(s['item'], s['state'], '|', s['treaty'])
