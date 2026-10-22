"""Project 15 session 3: the common treaty from the file, year by year (SESSION3.md, definitions). Writes common3.json."""
import json
from lib import load, SHA256

df, labels = load()
out = {'file_sha256': SHA256, 'last_year': 2014, 'min_parties_shown': 20, 'treaties': {}}
out['rows_missing_rat_yr'] = int(df['rat_yr'].isna().sum())
held = df[df['held']]
out['held_rows_missing_resdec_yr'] = int(held['resdec_yr'].isna().sum())
out['withdrawn_rows_missing_wdraw_yr'] = int(((held['withdrawal'] == 1) & held['wdraw_yr'].isna()).sum())
for t, g in df.groupby('treaty'):
    provs = g[['provision_id', 'article', 'para']].drop_duplicates('provision_id').sort_values(['article', 'para'])
    plist = [(int(p), int(a), int(q)) for p, a, q in provs.itertuples(index=False)]
    joined = g.groupby('country')['rat_yr'].min()
    h = g[g['held']].copy()
    h['from'] = h['resdec_yr'].fillna(h['rat_yr'])
    h['until'] = h['wdraw_yr'].where(h['withdrawal'] == 1)
    first = int(joined.min())
    years, n20 = {}, None
    for y in range(first, 2015):
        parties = set(joined[joined <= y].index)
        if n20 is None and len(parties) >= 20:
            n20 = y
        live = h[(h['from'] <= y) & ~(h['until'] <= y) & h['country'].isin(parties)]
        broken = set(int(p) for p in live['provision_id'])
        common = [p for p, _, _ in plist if p not in broken]
        holders = live.groupby('provision_id')['country'].nunique()
        years[y] = {'parties': len(parties), 'common': common,
                    'holders': {int(p): int(n) for p, n in holders.items()}}
    out['treaties'][t] = {'provisions': [{'id': p, 'article': a, 'para': q} for p, a, q in plist],
                          'first_party_year': first, 'year_20': n20, 'years': years}
json.dump(out, open('common3.json', 'w'), indent=0)
for t, v in out['treaties'].items():
    y20 = v['year_20']
    seq = [(y, len(v['years'][y]['common'])) for y in range(y20, 2015)]
    grow = [y for (y0, a), (y, b) in zip(seq, seq[1:]) if b > a]
    print(t, 'n', len(v['provisions']), 'y20', y20, 'at y20', seq[0][1], 'max', max(b for _, b in seq), 'min', min(b for _, b in seq),
          '2014', seq[-1][1], 'parties2014', v['years'][2014]['parties'], 'grows in', grow)
print({k: out[k] for k in ('rows_missing_rat_yr', 'held_rows_missing_resdec_yr', 'withdrawn_rows_missing_wdraw_yr')})
