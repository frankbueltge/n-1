"""Build works/the-hours-shown-wrong/index.html from template.html and two committed files of project 23 (projects/notice/session2.json,
the 505 episodes; projects/notice/session3.json, the registered count of session 3). Usage: python3 build.py"""
import calendar, json, os
H = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(H, '..', '..', 'projects', 'notice')
R = json.load(open(os.path.join(P, 'session2.json'))); S = json.load(open(os.path.join(P, 'session3.json')))
D = R['release_dates']
ts = lambda s: calendar.timegm(tuple(map(int, s.split('-'))) + (0, 0, 0))
K = {'news': 0, 'retimed': 1, 'past': 2}
eps = [[e['zone'], e['t0'], e['t1'], ts(D[e['corr']]), K[e['kind']], e['shown'], e['final'], e['rel'], e['corr'], e['hours']]
       for e in R['episodes_rows']]
assert len(eps) == S['episodes'] == 505
data = {'eps': eps, 'hidden': S['hidden_weekly']}
f = lambda n: f'{round(n):,}'
years = sorted(set(R['by_year']) | set(S['by_fixed_year']))
trs = []
for y in years:
    b = R['by_year'].get(y, {})
    trs.append(f"<tr><td>{y}</td><td>{f(b.get('news', 0))}</td><td>{f(b.get('retimed', 0))}</td><td>{f(b.get('past', 0))}</td>"
               f"<td>{f(S['by_fixed_year'].get(y, 0))}</td></tr>")
trs.append(f"<tr class=\"sum\"><td>all</td><td>{f(R['by_kind_hours']['news'])}</td><td>{f(R['by_kind_hours']['retimed'])}</td>"
           f"<td>{f(R['by_kind_hours']['past'])}</td><td>{f(S['hours'])}</td></tr>")
hm = S['hidden_max']
rep = {'{{HOURS}}': f(S['hours']), '{{EPS}}': str(S['episodes']), '{{REGIONS}}': str(S['regions']), '{{ZONES}}': str(R['zones_final']),
       '{{RELS}}': str(S['distinct_corr']), '{{MEDLAG}}': f"{S['median_lag_days_weighted'] / 365.25:.1f}",
       '{{W90}}': f"{100 * S['share_within_90d']:.1f}", '{{HMAX}}': f(hm['hours']),
       '{{HMAXDATE}}': '1 August 2012', '{{H2016}}': f(S['hidden_2016']),
       '{{ROWS}}': '\n'.join(trs), '{{DATA}}': json.dumps(data, separators=(',', ':'))}
assert hm['date'] == ts('2012-08-01')
t = open(os.path.join(H, 'template.html')).read()
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', len(t))
