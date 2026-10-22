"""Project 15 session 3: candidates for return (SESSION3.md, definitions): provisions not common in 2014 whose every 2014 holder is among
session 2's 27 late-withdrawal pairs. Writes returns3_candidates.json (provisions and holders; no page text)."""
import json
import lib

C = json.load(open('common3.json'))
flagged = {(c, t) for c, t, _ in json.load(open('session2.json'))['flagged_pairs']}
df, _ = lib.load()
h = df[df['held']].copy()
h['from'] = h['resdec_yr'].fillna(h['rat_yr'])
live = h[(h['from'] <= 2014) & ~((h['withdrawal'] == 1) & (h['wdraw_yr'] <= 2014))]
out = []
for (t, p), g in live.groupby(['treaty', 'provision_id']):
    holders = sorted(set(g['country']))
    if holders and all((c, t) in flagged for c in holders):
        a, q = int(g['article'].iloc[0]), int(g['para'].iloc[0])
        out.append({'treaty': t, 'provision': '%d(%d)' % (a, q), 'holders_2014': holders})
json.dump(out, open('returns3_candidates.json', 'w'), indent=1)
print(len(out)); [print(x) for x in out]
