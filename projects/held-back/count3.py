"""Project 15 session 3: the registered 2026 count (SESSION3.md) from common3.json, readings3.json, readings_check3.json and the returns
read by hand (RETURNS below, with the reason each was decided). Writes session3.json. No page text."""
import json
import pages2

C = json.load(open('common3.json'))
R = json.load(open('readings3.json'))['items']
CHECK = json.load(open('readings_check3.json'))['items']
CAND = json.load(open('returns3_candidates.json'))
# returns, read by hand after the candidates were drawn (footnotes of the holder on the current page)
RETURNS = {
    ('CEDAW', '10(903)'): (True, 'United Kingdom: its reservation on 10 (c) is among those withdrawn on 22 March 1996 (note 63); the file still codes it '
                                 'held in 2014; the dependent territories keep reservations on 1, 2, 9, 11, 13, 15, 16, not 10'),
    ('CRC', '9(4)'): (True, 'Oman: reservation on 9 (4) withdrawn, notified 9 December 2014, effective 14 January 2011 by its own account (note 50)'),
    ('ICCPR', '24(3)'): (False, 'United Kingdom: nationality legislation reservation naming 24 (3) still stands on the page'),
}
SIGNATURE_ONLY = {('CRC', 'Ecuador')}
RANGE = {('ICCPR', 'United States of America')}
joined = {t: {n: (p['joined'][0] if p.get('joined') else None) for n, p in pages2.parse(t)[0].items()} for t in pages2.NO}

out = {'treaties': {}, 'predictions': {}}
tot14 = tot26 = 0
for t, v in C['treaties'].items():
    prov = {p['id']: p for p in v['provisions']}
    lab = {pid: '%d(%d)' % (p['article'], p['para']) for pid, p in prov.items()}
    arts_split = {p['article'] for p in v['provisions'] if p['para'] != 0}
    c14 = [lab[pid] for pid in v['years']['2014']['common']]
    holders = {}
    for x in R:
        if x['treaty'] != t:
            continue
        for h in x['holds']:
            holders.setdefault(h, []).append(x['state'])
    broken = {}
    for h, sts in holders.items():
        kinds = []
        for s in sts:
            j = joined[t].get(s)
            if (t, s) in RANGE:
                k = 'a range of articles declared not self-executing'
            elif (t, s) in SIGNATURE_ONLY:
                k = 'a statement made upon signature only'
            elif j and j >= 2015:
                k = 'a party that joined after 2014'
            elif h.endswith('(0)') and int(h.split('(')[0]) in arts_split:
                k = 'a whole article named, where the file codes its subparagraphs apart'
            else:
                k = 'a statement standing before or after 2014 that the file does not code at this provision'
            kinds.append({'state': s, 'joined': j, 'kind': k})
        broken[h] = kinds
    c26 = [p for p in c14 if p not in broken]
    ret = [p for (tt, p), (ok, why) in RETURNS.items() if tt == t and ok]
    gen = sorted({x['state'] for x in R if x['treaty'] == t and x['general']})
    gen_sig = sorted({x['state'] for x in R if x['treaty'] == t and x['general'] and 'upon signature only' in x['general']})
    out['treaties'][t] = {'provisions': len(prov), 'common_2014': c14, 'common_2026_articled': c26 + ret, 'returned': ret,
                          'broken': broken, 'general_parties': gen, 'general_upon_signature_only': gen_sig,
                          'parties_2014': v['years']['2014']['parties'], 'read': sum(1 for x in R if x['treaty'] == t)}
    tot14 += len(c14)
    tot26 += len([p for p in c14 if p not in broken])
# strict variants for the report: without the US range declaration, without signature-only, without chapeau splits
def still(strip):
    n = 0
    for t, v in out['treaties'].items():
        for p in v['common_2014']:
            ks = [k['kind'] for k in v['broken'].get(p, [])]
            ks = [k for k in ks if k not in strip]
            if not ks:
                n += 1
    return n
out['totals'] = {'common_2014': tot14, 'still_common_2026_articled': tot26,
                 'share': round(tot26 / tot14, 4),
                 'still_common_without_range_signature_chapeau': still({'a range of articles declared not self-executing',
                                                                        'a statement made upon signature only',
                                                                        'a whole article named, where the file codes its subparagraphs apart'}),
                 'returned': sum(len(v['returned']) for v in out['treaties'].values()),
                 'treaties_with_general': sum(1 for v in out['treaties'].values() if v['general_parties']),
                 'treaties_with_general_excluding_signature_only': sum(1 for v in out['treaties'].values()
                                                                       if set(v['general_parties']) - set(v['general_upon_signature_only'])),
                 'parties_with_general': sum(len(v['general_parties']) for v in out['treaties'].values())}
out['returns_read'] = [{'treaty': t, 'provision': p, 'returned': ok, 'reading': why} for (t, p), (ok, why) in RETURNS.items()]
assert {(x['treaty'], x['provision']) for x in CAND} == set(RETURNS)
# predictions
yrs = lambda t: C['treaties'][t]['years']
p1 = {t: (len(yrs(t)['2014']['common']), len(yrs(t)[str(v['year_20'])]['common'])) for t, v in C['treaties'].items()}
p2 = {}
for t, v in C['treaties'].items():
    seq = [len(yrs(t)[str(y)]['common']) for y in range(v['year_20'], 2015)]
    p2[t] = [v['year_20'] + i + 1 for i, (a, b) in enumerate(zip(seq, seq[1:])) if b > a]
agree = sum(1 for x in CHECK if x['reading'] == 'does not')
out['predictions'] = [
    {'n': 1, 'text': 'in every treaty the common treaty in 2014 is smaller than in the first year with 20 parties',
     'held': all(a < b for a, b in p1.values()), 'found': {t: {'at_20_parties': b, '2014': a} for t, (a, b) in p1.items()}},
    {'n': 2, 'text': 'in at least three treaties the common treaty grows in at least one year', 'held': sum(1 for g in p2.values() if g) >= 3,
     'found': p2},
    {'n': 3, 'text': 'at least 90 % of the 2014-common provisions still common on the October 2026 pages (articled reading)',
     'held': tot26 / tot14 >= .9, 'found': '%d of %d (%.1f %%)' % (tot26, tot14, 100 * tot26 / tot14)},
    {'n': 4, 'text': 'at least five treaties with a party holding a standing general reservation in 2026',
     'held': out['totals']['treaties_with_general'] >= 5, 'found': {t: v['general_parties'] for t, v in out['treaties'].items()}},
    {'n': 5, 'text': 'machine clearance agrees with the hand reading on at least 19 of 20', 'held': agree >= 19, 'found': '%d of %d' % (agree, len(CHECK))},
    {'n': 6, 'text': 'at most 3 provisions not common in 2014 are common in 2026', 'held': out['totals']['returned'] <= 3,
     'found': '%d returned of %d candidates' % (out['totals']['returned'], len(CAND))},
]
out['held'] = sum(p['held'] for p in out['predictions'])
json.dump(out, open('session3.json', 'w'), indent=1)
for t, v in out['treaties'].items():
    print(t, 'n', v['provisions'], '2014', len(v['common_2014']), '2026', len(v['common_2026_articled']), 'broken', {k: [x['state'] for x in s] for k, s in v['broken'].items()}, 'general', len(v['general_parties']))
print(out['totals']); print([(p['n'], p['held']) for p in out['predictions']])
