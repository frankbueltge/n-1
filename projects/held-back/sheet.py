"""The blind step (SELECTION.md): 20 held-back rows, 20 hard negatives, shuffled; flags go to the key only. Prints no flag."""
import json, random
from lib import load

df, _ = load()
rng = random.Random(20261022)
held = df[df['held']]
states_holding = set(zip(held['country'], held['treaty']))
held_prov = set(zip(held['country'], held['treaty'], held['article']))
import numpy as np
neg = df[(~df["held"]) & np.array([(c, t) in states_holding for c, t in zip(df["country"], df["treaty"])])]
pos_idx = rng.sample(sorted(held.index), 20)
neg_idx = rng.sample(sorted(neg.index), 20)
items = [('p', i) for i in pos_idx] + [('n', i) for i in neg_idx]
rng.shuffle(items)
sheet, key = [], []
for n, (kind, i) in enumerate(items, 1):
    r = df.loc[i]
    sheet.append({'item': n, 'state': r['country'], 'treaty': r['treaty'], 'article': int(r['article']), 'para': None if r['para'] != r['para'] else int(r['para'])})
    key.append({'item': n, 'drawn_as': kind, 'row': int(i), 'reservation': int(r['reservation']), 'declaration': int(r['declaration']),
                'resdec_yr': None if r['resdec_yr'] != r['resdec_yr'] else int(r['resdec_yr']),
                'withdrawal': None if r['withdrawal'] != r['withdrawal'] else int(r['withdrawal']),
                'wdraw_yr': None if r['wdraw_yr'] != r['wdraw_yr'] else int(r['wdraw_yr']),
                'same_article_held_elsewhere_in_row_set': (r['country'], r['treaty'], r['article']) in held_prov})
json.dump({'seed': 20261022, 'items': sheet}, open('sheet.json', 'w'), indent=1, ensure_ascii=False)
json.dump({'seed': 20261022, 'items': key}, open('key.json', 'w'), indent=1)
print(len(sheet), 'items written; key in key.json (not opened)')
