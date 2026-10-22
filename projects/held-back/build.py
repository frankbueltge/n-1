"""Project 15: the study page, index.html, drawn from the file (via lib.py), session1.json and result1.json; from session 2 also
session2.json, result2.json and newreadings2.json (the years after the file's last); from session 3 also session3.json and
result3.json (the clauses the file leaves out, read from the pages)."""
import json, html
from lib import load

df, labels = load()
s = json.load(open('session1.json'))
r = json.load(open('result1.json'))
ORDER = ['ICCPR', 'ICESCR', 'CERD', 'CEDAW', 'CAT', 'CRC', 'CRMW', 'CRPD', 'CED']
# years: the date each treaty was opened for signature, as the UN's chapter IV list gives it (New York, 1966-2006)
NAME = {'ICCPR': 'Civil and Political Rights (1966)', 'ICESCR': 'Economic, Social and Cultural Rights (1966)',
        'CERD': 'Racial Discrimination (1966)', 'CEDAW': 'Discrimination against Women (1979)', 'CAT': 'Torture (1984)',
        'CRC': 'Rights of the Child (1989)', 'CRMW': 'Migrant Workers (1990)', 'CRPD': 'Persons with Disabilities (2006)',
        'CED': 'Enforced Disappearance (2006)'}
fig = {}
for t in ORDER:
    g = df[df['treaty'] == t]
    rows = []
    for p, x in g.groupby('provision_id', sort=True):
        h = x[x['held']]
        para = int(x['para'].iloc[0])
        lab = '%d' % int(x['article'].iloc[0]) + ('' if para == 0 else (' (%s)' % 'abcdefghi'[para - 901] if para > 900 else ' (%d)' % para))
        rows.append({'p': lab, 'held': int(h['country'].nunique()), 'withdrawn': int(h.loc[h['withdrawal'] == 1, 'country'].nunique())})
    fig[t] = {'parties': s['treaties'][t]['parties'], 'cells': rows}
json.dump(fig, open('figure1.json', 'w'), indent=0)

W, CELL, GAP = 1008, 6, 1
parts = []
for t in ORDER:
    f = fig[t]
    cells = f['cells']
    svg, x, y = [], 0, 0
    for c in cells:
        if x + CELL > W:
            x = 0; y += 34
        held_still = c['held'] - c['withdrawn']
        # height: share of parties holding back, scaled so one party in five fills the cell's 30 px
        hh = min(30, 30 * c['held'] / f['parties'] / .20)
        hs = min(30, 30 * held_still / f['parties'] / .20)
        svg.append('<g><title>Article %s: held back by %d of %d parties, %d of them since withdrawn</title>'
                   '<rect x="%d" y="%d" width="%d" height="30" class="bg"/>'
                   '<rect x="%d" y="%.1f" width="%d" height="%.1f" class="wd"/>'
                   '<rect x="%d" y="%.1f" width="%d" height="%.1f" class="hb"/></g>' % (
                       c['p'], c['held'], f['parties'], c['withdrawn'], x, y, CELL, x, y + 30 - hh, CELL, hh, x, y + 30 - hs, CELL, hs))
        x += CELL + GAP
    parts.append('<h3 class="tt">%s <span class="sm mut">%d parties · %d provisions</span></h3>'
                 '<svg class="ch" viewBox="0 0 %d %d" role="img" aria-label="%s: %d provisions as columns">%s</svg>' % (
                     html.escape(NAME[t]), f['parties'], len(cells), W, y + 31, html.escape(NAME[t]), len(cells), ''.join(svg)))
svg_s = '<div class="fig">' + ''.join(parts) + '</div>'

# session 2: after 2014, returns (a standing pair's latest withdrawal year) above the line, arrivals (a state joining with something
# held back, by year joined) below; an arrival holding back only clauses the file does not code is drawn hollow
s2 = json.load(open('session2.json'))
r2 = json.load(open('result2.json'))
arr = [x for x in json.load(open('newreadings2.json'))['items'] if x['reading'] == 'holds back']
YW, U, MID = 84, 13, 72
g2 = []
for i, yr in enumerate(range(2015, 2027)):
    x0 = 8 + i * YW
    g2.append('<text x="%d" y="%d" class="yr">%d</text>' % (x0 + YW // 2, MID + 5, yr))
    for j in range(s2['latest_year_by_pair'].get(str(yr), 0)):
        g2.append('<rect x="%d" y="%d" width="%d" height="%d" class="rt"/>' % (x0 + 6 + (j % 5) * U, MID - 20 - (j // 5 + 1) * U, U - 3, U - 3))
    a = sorted((x for x in arr if x['joined'] == yr), key=lambda x: x['only_dispute_or_committee_clauses'])
    for j, x in enumerate(a):
        g2.append('<g><title>%s, %s</title><rect x="%d" y="%d" width="%d" height="%d" class="%s"/></g>' % (
            html.escape(x['state']), x['treaty'], x0 + 6 + (j % 5) * U + 1, MID + 16 + (j // 5) * U + 1, U - 5, U - 5,
            'ao' if x['only_dispute_or_committee_clauses'] else 'ar'))
svg2 = ('<svg class="ch" viewBox="0 0 1024 %d" role="img" aria-label="Withdrawals and new reservations by year, 2015 to 2026">%s'
        '<line x1="8" x2="1016" y1="%d" y2="%d" class="ax"/></svg>' % (MID + 60, ''.join(g2), MID - 14, MID - 14))

# session 3: the clauses the file leaves out, read on the pages; per treaty, the dispute clause (and CAT 20) beside the most
# held-back other article, each as a bar of parties holding it back now and since withdrawn; scale 50 parties = full width
s3 = json.load(open('session3.json'))
r3 = json.load(open('result3.json'))
CL = {'CERD': ('22', 'disputes go to the International Court of Justice'), 'CEDAW': ('29 (1)', 'disputes go to arbitration or the Court'),
      'CAT': ('30 (1)', 'disputes go to arbitration or the Court'), 'CRMW': ('92 (1)', 'disputes go to arbitration or the Court'),
      'CED': ('42 (1)', 'disputes go to arbitration or the Court')}
OTHER = {'CERD': 'on racist propaganda and organisations', 'CEDAW': 'on marriage and family', 'CAT': 'the definition of torture'}


def bar(label, now, wd, cls):
    return ('<div class="br %s"><div class="bl">%s</div><div class="bt"><span class="bn" style="width:%.1f%%"></span>'
            '<span class="bw" style="width:%.1f%%"></span></div><div class="bc">%d now · %d withdrawn</div></div>' % (
                cls, label, 100 * now / 50, 100 * wd / 50, now, wd))


rows3 = []
for t in ['CERD', 'CEDAW', 'CAT', 'CRMW', 'CED']:
    d, c = s3['treaties'][t], r3['comparator_without_opt_ins'][t]
    rows3.append('<h3 class="tt">%s <span class="sm mut">%d parties</span></h3>' % (html.escape(NAME[t]), d['parties']))
    rows3.append(bar('Article %s · %s' % CL[t], d['clause_now'], d['clause_withdrawn'], 'cl'))
    if t == 'CAT':
        rows3.append(bar('Article 20 · the Committee may inquire', d['cat20_now'], d['cat20_withdrawn'], 'cl'))
    rows3.append(bar('Article %d%s' % (c['article'], ' · ' + OTHER[t] if t in OTHER else ''), c['now'], c['withdrawn'], 'ob'))
fig3 = '<div class="bars">' + ''.join(rows3) + '</div>'

P = {p['n']: p for p in r['predictions']}
T = s['treaties']
page = open('template.html').read()
rep = {
 '{{FIG}}': svg_s,
 '{{HELD}}': '{:,}'.format(s['held_rows']), '{{ROWS}}': '{:,}'.format(s['rows_with_treaty']),
 '{{WD}}': '{:,}'.format(s['withdrawn_rows']), '{{WDP}}': '%.0f %%' % (100 * s['withdrawn_share']),
 '{{MED}}': '%g' % s['standing_withdrawn']['median'], '{{Q1}}': '%g' % s['standing_withdrawn']['q1'], '{{Q3}}': '%g' % s['standing_withdrawn']['q3'],
 '{{STILLMED}}': '%g' % s['standing_still_to_last_year']['median'], '{{LAST}}': str(s['last_year']),
 '{{CEDAWP}}': str(T['CEDAW']['parties']), '{{C161}}': str(T['CEDAW']['max_states_on_one_provision']),
 '{{CATANY}}': str(T['CAT']['parties_holding_back_any']), '{{CATP}}': str(T['CAT']['parties']), '{{CATALL}}': str(T['CAT']['provisions_held_by_all']), '{{CATN}}': str(T['CAT']['provisions']),
 '{{AGREE}}': str(r['check']['agree']), '{{TOLD}}': str(r['check']['told']),
 '{{PRED}}': ''.join('<li>%s: <b>%s</b>. %s</li>' % (html.escape(p['text']), 'held' if p['held'] else 'failed', html.escape(p['found'])) for p in r['predictions']),
 '{{NHELD}}': str(r['held']),
 '{{FIG2}}': svg2, '{{STAND}}': str(s2['matched']), '{{RET}}': str(s2['flagged_late']), '{{RETP}}': '%.0f %%' % (100 * s2['flagged_share']),
 '{{ARR}}': str(r2['arrivals']['holding_back']), '{{ARRO}}': str(r2['arrivals']['only_clauses_the_file_does_not_code']),
 '{{AGREE2}}': str(r2['check']['agree']),
 '{{PRED2}}': ''.join('<li>%s: <b>%s</b>. %s</li>' % (html.escape(p['text']), 'held' if p['held'] else 'failed', html.escape(p['found'])) for p in r2['predictions']),
 '{{NHELD2}}': str(r2['held']),
 '{{FIG3}}': fig3, '{{CLNOW}}': str(r3['totals']['clause_now']), '{{C29}}': str(s3['treaties']['CEDAW']['clause_now']),
 '{{C16}}': str(s3['treaties']['CEDAW']['now_by_article']['16']), '{{AGREE3}}': str(r3['check']['agree']),
 '{{PRED3}}': ''.join('<li>%s: <b>%s</b>. %s</li>' % (html.escape(p['text']), 'held' if p['held'] else 'failed', html.escape(p['found'])) for p in r3['predictions']),
 '{{NHELD3}}': str(r3['held']),
}
for k, v in rep.items():
    page = page.replace(k, v)
assert '{{' not in page
open('index.html', 'w').write(page)
print('ok', len(page))
