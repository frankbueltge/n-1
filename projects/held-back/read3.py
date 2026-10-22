"""Project 15, session 3: prints one item's section and every footnote it references, for the hand reading (no verdict shown).
Usage: python3 read3.py ITEM [ITEM ...] (items from sheet3.json)."""
import json, sys
import lib3, pages2

sheet = {s['item']: s for s in json.load(open('sheet3.json'))['items']}
for i in map(int, sys.argv[1:]):
    s = sheet[i]
    parts, _, notes = pages2.parse(s['treaty'])
    secs, _ = lib3.sections(s['treaty'])
    sec = secs.get(s['state'], {'text': '(none)', 'notes': []})
    print('=' * 20, i, s['state'], s['treaty'], 'article', s['article'], 'joined', parts.get(s['state'], {}).get('joined'))
    print('SECTION:', sec['text'].strip())
    ns = []
    for n in parts.get(s['state'], {}).get('notes', []) + sec['notes']:
        if n not in ns:
            ns.append(n)
    for n in ns:
        print('-- note', n); print(notes.get(n, ''))
