"""Project 15 session 3: appends hand readings of the read set to readings3.json (my judgments only; no page wording).
Each reading: treaty, state, holds (common provisions held back, as 'article(para)'; empty if none), general (bool), remark."""
import json, os, sys
F = 'readings3.json'


def add(treaty, rows):
    d = json.load(open(F)) if os.path.exists(F) else {'read_by': 'Remainder, by hand, every entry of the read set; machine readings, estimates',
                                                      'estimate': True, 'items': []}
    for state, holds, general, remark in rows:
        d['items'].append({'treaty': treaty, 'state': state, 'holds': holds, 'general': general, 'remark': remark})
    json.dump(d, open(F, 'w'), indent=0)
    print(treaty, len([x for x in d['items'] if x['treaty'] == treaty]), 'read;', len(d['items']), 'in all')
