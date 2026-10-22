"""Project 15 session 1: predictions against the count and the check. Writes result1.json."""
import json
s = json.load(open('session1.json'))
k = {x['item']: x for x in json.load(open('key.json'))['items']}
r = json.load(open('readings.json'))['readings']
told = [x for x in r if x['reading'] != 'cannot']
coded = lambda c: 'held' if (c['reservation'] == 1 or c['declaration'] == 1) else 'not'
agree = [x['item'] for x in told if x['reading'] == coded(k[x['item']])]
dis = [x['item'] for x in told if x['reading'] != coded(k[x['item']])]
T = s['treaties']
res = {
 'check': {'told': len(told), 'agree': len(agree), 'disagree': dis, 'cannot': [x['item'] for x in r if x['reading'] == 'cannot'],
           'disagreements_read_again_after_the_key': {
             '3': 'the page names article 22 paragraph 4; the file codes paragraph by paragraph and has 22 (6) not held: agreement at paragraph level',
             '6': 'the page names article 9 paragraph 2 and a general reservation; the file codes 9 (1) not held: the general reservation is not spread over provisions here',
             '19': 'the page names article 12 paragraph 4; the file has 12 (2) not held: agreement at paragraph level',
             '33': 'the page names article 2 (f) and (g); the file has 2 (d) not held: agreement at paragraph level',
             '8': 'my miss: note 36 on the page records Norway\'s reservation to article 6 (4), withdrawn 12 December 1979, as the file codes it (1972, 1979)'},
           'at_paragraph_level_exploratory': '36 of 37: the four granularity cases agree and my miss is mine',
           'also_seen': 'item 40: the file codes a declaration by Kuwait on ICCPR 2 (1) in 1966; Kuwait acceded on 21 May 1996 (the participants table of the UN page), and the page does not carry the declaration\'s text'},
 'predictions': [
  {'n': 1, 'text': 'the provision held back by most states is a dispute-settlement clause', 'held': False,
   'found': 'CEDAW 16 (1), 33 states; then CEDAW 9 (2), 25; CERD 4 (a)-(c), 20-21. The file codes only provisions of function "obligation" (all 72,396 rows); no dispute clause is in it, so the prediction could not hold here, and says nothing of the record itself.'},
  {'n': 2, 'text': 'at most 25 % of held-back rows withdrawn by the last year', 'held': s['withdrawn_share'] <= .25, 'found': '%d of %d (%.1f %%), last year %d' % (s['withdrawn_rows'], s['held_rows'], 100 * s['withdrawn_share'], s['last_year'])},
  {'n': 3, 'text': 'median standing time of withdrawn rows at least 10 years', 'held': s['standing_withdrawn']['median'] >= 10, 'found': 'median %g years (quartiles %g and %g), n %d' % (s['standing_withdrawn']['median'], s['standing_withdrawn']['q1'], s['standing_withdrawn']['q3'], s['standing_withdrawn']['n'])},
  {'n': 4, 'text': 'in every treaty at least half of the provisions held by all parties', 'held': all(v['share_held_by_all'] >= .5 for v in T.values()),
   'found': '; '.join('%s %d of %d' % (t, v['provisions_held_by_all'], v['provisions']) for t, v in T.items())},
  {'n': 5, 'text': 'in at least one treaty a provision held back by more than a quarter of its parties', 'held': any(v['max_share_of_parties'] > .25 for v in T.values()),
   'found': 'largest: CEDAW 16 (1), %d of %d parties (%.1f %%)' % (T['CEDAW']['max_states_on_one_provision'], T['CEDAW']['parties'], 100 * T['CEDAW']['max_share_of_parties'])},
  {'n': 6, 'text': 'the check agrees at at least 30 of the rows it can tell', 'held': len(agree) >= 30, 'found': '%d of %d' % (len(agree), len(told))},
 ]}
res['held'] = sum(p['held'] for p in res['predictions'])
json.dump(res, open('result1.json', 'w'), indent=1, ensure_ascii=False)
for p in res['predictions']: print(p['n'], p['held'], p['found'])
print(res['check']['agree'], res['check']['disagree'])
