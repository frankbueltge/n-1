"""Project 20, session 1: the registered count (SELECTION.md). Run once, after the selection was pushed.
Reads bells.csv from scratch (Dove's Guide, CC BY-SA 4.0); writes session1.json (counts and fits only)."""
import csv, json, math, re, statistics as st, sys, collections as C

path = sys.argv[1]
rows = list(csv.DictReader(open(path, encoding='utf-8-sig')))

LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
ACC = {'♯': 1, '♭': -1, '𝄪': 2, '𝄫': -2, '#': 1, 'b': -1}

def pc(note):
    if not note or note[0] not in LET:
        return None
    p = LET[note[0]]
    for ch in note[1:]:
        if ch not in ACC:
            return None
        p += ACC[ch]
    return p % 12

def dev(f, p):
    c = 1200 * math.log2(f / 440) + 900
    return ((c - 100 * p + 600) % 1200) - 600

def num(s):
    try:
        v = float(s)
        return v if v > 0 else None
    except ValueError:
        return None

def year(s):
    m = re.search(r'(\d{4})', s or '')
    return int(m.group(1)) if m else None

out = {'bells': len(rows)}
hz = [num(r['Nominal (Hz)']) for r in rows]
out['with_nominal'] = sum(1 for v in hz if v)
out['share_with_nominal'] = out['with_nominal'] / len(rows)

# deviation from the named note
ds = []
for r, f in zip(rows, hz):
    p = pc(r['Note'])
    r['_d'] = dev(f, p) if (f and p is not None) else None
    if r['_d'] is not None:
        ds.append(r['_d'])
ad = [abs(d) for d in ds]
out['with_nominal_and_note'] = len(ds)
out['median_abs_dev_cents'] = st.median(ad)
out['share_abs_dev_le_50'] = sum(1 for a in ad if a <= 50) / len(ad)
out['abs_dev_hist_10c'] = dict(sorted(C.Counter(min(int(a // 10) * 10, 600) for a in ad).items()))
out['signed_dev_hist_5c'] = dict(sorted(C.Counter(int(math.floor(d / 5)) * 5 for d in ds).items()))

# weight
wts = [num(r['Weight (lbs)']) for r in rows]
out['with_weight'] = sum(1 for w in wts if w)
out['estimated_weight'] = sum(1 for r, w in zip(rows, wts) if w and r['Weight (approx)'] == 'Y')
out['share_estimated'] = out['estimated_weight'] / out['with_weight']
xs, ys = [], []
for r, f, w in zip(rows, hz, wts):
    if f and w and r['Weight (approx)'] != 'Y':
        xs.append(math.log10(w)); ys.append(math.log10(f))
n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
b = sxy / sxx; a = my - b * mx
res = [y - (a + b * x) for x, y in zip(xs, ys)]
sd = math.sqrt(sum(e * e for e in res) / (n - 2))
out['fit'] = {'n': n, 'slope': b, 'intercept': a, 'resid_sd_log10': sd, 'resid_sd_octaves': sd / math.log10(2)}

# cast years before 1600
yrs = [year(r['Cast Date']) for r in rows]
pre = C.Counter(y for y in yrs if y and y < 1600)
out['cast_before_1600'] = sum(pre.values())
out['modal_years_before_1600'] = pre.most_common(10)

# relative deviation in full-circle rings; trebles of eight by era
rings = C.defaultdict(list)
for r in rows:
    if r['Collection Type'] == 'full-circle ring':
        rings[r['Ring ID']].append(r)
rel = []
for rid, bs in rings.items():
    size = bs[0]['Ring Size'].split()[0] if bs[0]['Ring Size'] else ''
    ten = [x for x in bs if x['Bell Role'] == size]
    if len(ten) != 1 or ten[0]['_d'] is None:
        continue
    td = ten[0]['_d']
    for x in bs:
        if x['_d'] is not None and x['Bell Role'].isdigit():
            rd = ((x['_d'] - td + 600) % 1200) - 600
            rel.append((size, x['Bell Role'], year(x['Cast Date']), rd, x['Ring Size']))
out['bells_with_r'] = len(rel)
tre = [t for t in rel if t[4] == '8' and t[1] == '1' and t[2]]
old = [t[3] for t in tre if t[2] < 1880]
new = [t[3] for t in tre if t[2] >= 1950]
out['trebles_of_8'] = {'old_n': len(old), 'old_median_r': st.median(old) if old else None,
                       'new_n': len(new), 'new_median_r': st.median(new) if new else None}

P = {}
P['P1'] = out['bells'] >= 40000
P['P2'] = out['share_with_nominal'] >= 0.25
P['P3'] = out['median_abs_dev_cents'] <= 20
P['P4'] = out['share_abs_dev_le_50'] >= 0.90
P['P5'] = -0.40 <= b <= -0.27
P['P6'] = out['fit']['resid_sd_octaves'] <= 0.25
P['P7'] = bool(pre) and pre.most_common(1)[0][0] in (1499, 1599)
P['P8'] = out['share_estimated'] >= 0.20
P['P9'] = (old and new and st.median(old) >= 10 and abs(st.median(new)) <= 5) or False
out['predictions'] = {k: bool(v) for k, v in P.items()}
json.dump(out, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: out[k] for k in out if 'hist' not in k}, indent=1, ensure_ascii=False))
