"""Build works/the-court-still-sits/index.html from template.html and one committed file of project 22, session 3
(projects/standing/session3.json): counts per (interval, year, class) only; no name or id leaves that file. Usage: python3 build.py"""
import json, os

H = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(H, '..', '..', 'projects', 'standing', 'session3.json')))
STEPS = ['v10-v11', 'v11-v12', 'v12-v13', 'v13-v14', 'v14-v15', 'v15-v16']
# release dates: Kew's archive listing (read 2026-11-05 02:03 UTC, SESSION2.md) and the current file's version date (PROJECT.md)
LABELS = ['Dec 2022 → Oct 2023', 'Oct 2023 → Oct 2023 (files posted 18 minutes apart)', 'Oct 2023 → May 2025',
          'May 2025 → Jul 2025', 'Jul 2025 → Jan 2026', 'Jan 2026 → Jun 2026']
CL = ['condemned', 'acquitted', 'sent', 'judged', 'withdrawn', 're-described']
cells = {}
for s in STEPS:
    rows = {}
    for y, cl, n in S['cells'][s]:
        if cl in CL:
            rows.setdefault(str(y), [0] * len(CL))[CL.index(cl)] = n
    cells[s] = rows
names = dict(S['v16_names_per_year'])
stand = dict(S['v16_standing_per_year'])
assert set(cells) == set(STEPS)
data = {'steps': STEPS, 'labels': LABELS, 'classes': CL, 'cells': cells,
        'names': {str(k): v for k, v in names.items()}, 'standing': {str(k): v for k, v in stand.items()}}

def f(n): return f'{n:,}'
T = S['totals']
trs = []
for s, lab in zip(STEPS, LABELS):
    c = S['steps'][s]['classes']
    trs.append('<tr><td>' + lab + '</td>' + ''.join(f'<td>{f(c[k])}</td>' for k in CL + ['other']) + '</tr>')
trs.append('<tr class="sum"><td>all six</td>' + ''.join(f'<td>{f(T[k])}</td>' for k in CL + ['other']) + '</tr>')
total_names = sum(names.values())
t = open(os.path.join(H, 'template.html')).read()
rep = {
    '{{NAMES}}': f(total_names), '{{STAND}}': f(sum(stand.values())), '{{EVENTS}}': f(S['all_events']), '{{DRAWN}}': f(S['drawn']),
    '{{COND}}': f(T['condemned']), '{{ACQ}}': f(T['acquitted']), '{{SENT}}': f(T['sent']), '{{JUDGED}}': f(T['judged']),
    '{{WITHDRAWN}}': f(T['withdrawn']), '{{REDESC}}': f(T['re-described']), '{{OTHER}}': f(T['other']),
    '{{REDESC_PC}}': f"{100 * T['re-described'] / S['all_events']:.0f}", '{{Y1753}}': str(S['steps_with_1753_drawn']),
    '{{TOPYEAR}}': str(S['top_year_drawn'][0]), '{{TOPYEAR_N}}': f(S['top_year_drawn'][1]),
    '{{RATE_NEW}}': f"{S['rate_2000_2026'][0]:.0f}", '{{RATE_OLD}}': f"{S['rate_1753_1799'][0]:.0f}",
    '{{ROWS}}': '\n'.join(trs), '{{DATA}}': json.dumps(data, separators=(',', ':')),
}
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t
# rights: no plant_name_id from the sample may appear on the page
for e in S['check_sample']:
    assert '"' + e['plant_name_id'] + '"' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', len(t))
