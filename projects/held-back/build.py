"""Project 15: the study page, index.html, drawn from the file (via lib.py), session1.json and result1.json."""
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
}
for k, v in rep.items():
    page = page.replace(k, v)
assert '{{' not in page
open('index.html', 'w').write(page)
print('ok', len(page))
