"""Project 15 session 1: the registered count (SELECTION.md, definitions). Writes session1.json."""
import json
import numpy as np
from lib import load, SHA256

df, labels = load()
F = labels['art_function']
out = {'file_sha256': SHA256, 'rows_with_treaty': int(len(df)), 'rows_without_treaty': df.attrs['rows_without_treaty']}
yrs = [df[c].max() for c in ('rat_yr', 'resdec_yr', 'wdraw_yr')]
last = int(np.nanmax(yrs))
out['last_year'] = last
out['last_year_by_column'] = {c: (None if v != v else int(v)) for c, v in zip(('rat_yr', 'resdec_yr', 'wdraw_yr'), yrs)}
held = df[df['held']]
out['held_rows'] = int(len(held))
out['reserved_rows'] = int((df['reservation'] == 1).sum())
out['declared_rows'] = int((df['declaration'] == 1).sum())
out['held_rows_missing_resdec_yr'] = int(held['resdec_yr'].isna().sum())
wd = held[held['withdrawal'] == 1]
out['withdrawn_rows'] = int(len(wd))
out['withdrawn_share'] = round(len(wd) / len(held), 4)
st = (wd['wdraw_yr'] - wd['resdec_yr']).dropna()
out['withdrawn_missing_years'] = int(len(wd) - len(st))
out['standing_withdrawn'] = {'n': int(len(st)), 'median': float(st.median()), 'q1': float(st.quantile(.25)), 'q3': float(st.quantile(.75)),
                             'negative': int((st < 0).sum()), 'zero': int((st == 0).sum())}
still = held[held['withdrawal'] != 1]
s2 = (last - still['resdec_yr']).dropna()
out['standing_still_to_last_year'] = {'n': int(len(s2)), 'median': float(s2.median())}
# how states hold back: provisions held per (state, treaty) against provisions of the treaty
per = {}
for t, g in df.groupby('treaty'):
    parties = g['country'].nunique()
    provs = g.groupby('provision_id')
    hb = provs.apply(lambda x: int(x.loc[x['held'], 'country'].nunique()), include_groups=False)
    n_prov = int(len(hb))
    st_held = g[g['held']].groupby('country')['provision_id'].nunique()
    top = hb.sort_values(ascending=False).head(3)
    per[t] = {'parties': int(parties), 'provisions': n_prov, 'rows': int(len(g)),
              'parties_holding_back_any': int(len(st_held)),
              'provisions_held_by_all': int((hb == 0).sum()), 'share_held_by_all': round(float((hb == 0).mean()), 4),
              'max_states_on_one_provision': int(hb.max()), 'max_share_of_parties': round(float(hb.max() / parties), 4),
              'states_holding_back_every_provision': int((st_held == n_prov).sum()),
              'top': [{'provision_id': int(p), 'article': int(g.loc[g['provision_id'] == p, 'article'].iloc[0]),
                       'para': int(g.loc[g['provision_id'] == p, 'para'].iloc[0]),
                       'function': F.get(int(g.loc[g['provision_id'] == p, 'art_function'].iloc[0]), None), 'states': int(n)} for p, n in top.items()]}
out['treaties'] = per
# across treaties: top five provisions by number of states
allp = []
for t, v in per.items():
    for x in v['top']:
        allp.append(dict(x, treaty=t))
allp.sort(key=lambda x: -x['states'])
out['top5_across'] = allp[:5]
# withdrawal share by function (obligation vs mechanics), reported, not predicted
byf = {}
for f, g in held.groupby('art_function'):
    byf[F.get(int(f), str(f))] = {'held': int(len(g)), 'withdrawn': int((g['withdrawal'] == 1).sum())}
out['by_function'] = byf
# withdrawals by decade of withdrawal
out['withdrawals_by_decade'] = {str(int(d)): int(n) for d, n in (wd['wdraw_yr'] // 10 * 10).value_counts().sort_index().items()}
json.dump(out, open('session1.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
