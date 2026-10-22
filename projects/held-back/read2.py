"""Project 15, session 2: prints one pair's page entry and every footnote it references, for the hand reading (no flag shown).
Usage: python3 read2.py ITEM [ITEM ...] (items from sheet2.json)."""
import json, sys
import lib2, pages2

sheet = {s['item']: s for s in json.load(open('sheet2.json'))['items']}
for i in map(int, sys.argv[1:]):
    s = sheet[i]
    name = lib2.NAMES.get(s['state'], s['state'])
    parts, entries, notes = pages2.parse(s['treaty'])
    print('=' * 20, i, name, s['treaty'], 'joined', parts.get(name, {}).get('joined'))
    print('ENTRY:', entries.get(name, {}).get('text', '(none)').strip())
    for n, text in pages2.footnotes(name, parts, entries, notes):
        print('-- note', n, f'({len(text)} chars)'); print(text)
