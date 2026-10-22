import json, sys, re
from pageread import entry
from show import NO
items = json.load(open('sheet.json'))['items']
for it in items[int(sys.argv[1]) - 1:int(sys.argv[2])]:
    out, res = entry(NO[it['treaty']], it['state'])
    ent = '\n'.join(t for k, t, _ in out if t and k == 'ENTRY')
    notes = '\n'.join('[note %s] %s' % r for r in res)
    txt = ent + '\n' + notes
    a = str(it['article'])
    print('\n########', it, 'chars', len(ent), len(notes))
    print(ent[:900].replace('\n', ' '))
    for s in re.split(r'(?<=[.;:])\s+', txt):
        if re.search(r'\b[Aa]rticles?\b[^.]{0,80}\b' + a + r'\b|\b' + a + r'\s*\(|whole|any provision|all the provisions|provisions of (the|this) Convention|Sharia|Shariah|withdraw', s):
            print('  >', s.replace('\n', ' ')[:400])
