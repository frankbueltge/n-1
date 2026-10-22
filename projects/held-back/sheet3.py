"""Project 15, session 3: draws the 24 checked items (SESSION3.md) and writes the sheet (state, treaty, article) and the key (machine
verdicts) separately. Prints the sheet only."""
import json, random
import lib3

pos, neg, c16 = [], [], {'now': [], 'not': []}
for t in lib3.TREATIES:
    v, parts, secs, _, _ = lib3.verdicts(t)
    arts = [lib3.CLAUSE[t]] + ([20] if t == 'CAT' else [])
    for name in sorted(parts):
        for a in arts:
            verdict = v[name].get(a, 'not')
            if verdict == 'now':
                pos.append((name, t, a, verdict))
            elif verdict == 'not' and secs.get(name, {}).get('text', '').strip():
                neg.append((name, t, a, verdict))
        if t == 'CEDAW':
            verdict = v[name].get(16, 'not')
            if verdict in c16:
                c16[verdict].append((name, t, 16, verdict))
rng = random.Random(20261024)
items = rng.sample(pos, 12) + rng.sample(neg, 6) + rng.sample(c16['now'], 3) + rng.sample(c16['not'], 3)
rng.shuffle(items)
sheet = [{'item': i + 1, 'state': s, 'treaty': t, 'article': a} for i, (s, t, a, _) in enumerate(items)]
key = [{'item': i + 1, 'state': s, 'treaty': t, 'article': a, 'machine': v} for i, (s, t, a, v) in enumerate(items)]
json.dump({'seed': 20261024, 'items': sheet}, open('sheet3.json', 'w'), indent=1, ensure_ascii=False)
json.dump({'seed': 20261024, 'items': key}, open('key3.json', 'w'), indent=1, ensure_ascii=False)
for s in sheet:
    print(s['item'], s['state'], '|', s['treaty'], s['article'])
