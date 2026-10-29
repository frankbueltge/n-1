"""Project 20, session 1: exploration after the registered count (not registered; nothing here is a prediction's outcome).
The ring's offset (tenor's d) against the ring's inside (r), by the tenor's cast era; the bells named by a note that is not the nearest;
the record's pre-1600 years; the weight-pitch fit by era. Writes explore1.json."""
import csv, json, math, re, statistics as st, sys, collections as C
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from count1_lib import pc, dev

rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
def num(s):
    try:
        v = float(s); return v if v > 0 else None
    except ValueError:
        return None
def year(s):
    m = re.search(r'(\d{4})', s or ''); return int(m.group(1)) if m else None
for r in rows:
    f = num(r['Nominal (Hz)']); p = pc(r['Note'])
    r['_d'] = dev(f, p) if f and p is not None else None
    r['_y'] = year(r['Cast Date'])
out = {}
ds = [r['_d'] for r in rows if r['_d'] is not None]
out['signed_d_median'] = st.median(ds)
out['share_d_positive'] = sum(1 for d in ds if d > 0) / len(ds)

rings = C.defaultdict(list)
for r in rows:
    if r['Collection Type'] == 'full-circle ring':
        rings[r['Ring ID']].append(r)
era = lambda y: None if y is None else (y // 50) * 50
ten_d, rel = [], []
by_era = C.defaultdict(lambda: {'tenor_abs_d': [], 'abs_r': []})
far = C.Counter()
for rid, bs in rings.items():
    size = bs[0]['Ring Size'].split()[0] if bs[0]['Ring Size'] else ''
    ten = [x for x in bs if x['Bell Role'] == size]
    if len(ten) != 1 or ten[0]['_d'] is None:
        continue
    td = ten[0]['_d']; e = era(ten[0]['_y'])
    ten_d.append(td); by_era[e]['tenor_abs_d'].append(abs(td))
    for x in bs:
        if x is ten[0] or x['_d'] is None or not x['Bell Role'].isdigit():
            continue
        rd = ((x['_d'] - td + 600) % 1200) - 600
        rel.append(rd); by_era[era(x['_y'])]['abs_r'].append(abs(rd))
        if abs(x['_d']) > 50:
            far['ring_offset' if abs(rd) <= 50 else 'inside_ring'] += 1
out['rings_with_tenor_d'] = len(ten_d)
out['median_abs_tenor_d'] = st.median(abs(t) for t in ten_d)
out['median_abs_r'] = st.median(abs(t) for t in rel)
out['share_abs_tenor_d_gt_25'] = sum(1 for t in ten_d if abs(t) > 25) / len(ten_d)
out['bells_named_not_nearest_in_rings'] = dict(far)
out['by_50y_era'] = {str(k): {'rings_tenor_cast': len(v['tenor_abs_d']), 'median_abs_tenor_d': st.median(v['tenor_abs_d']) if v['tenor_abs_d'] else None,
                               'bells_r': len(v['abs_r']), 'median_abs_r': st.median(v['abs_r']) if v['abs_r'] else None}
                     for k, v in sorted(by_era.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))}
out['tenor_d_hist_10c'] = dict(sorted(C.Counter(int(math.floor(t / 10)) * 10 for t in ten_d).items()))
out['r_hist_5c'] = dict(sorted(C.Counter(int(math.floor(t / 5)) * 5 for t in rel if abs(t) < 100).items()))

pre = [r['_y'] for r in rows if r['_y'] and r['_y'] < 1600]
out['pre1600'] = {'n': len(pre), 'ending_99': sum(1 for y in pre if y % 100 == 99), 'ending_00_or_50': sum(1 for y in pre if y % 50 == 0),
                  'circa': sum(1 for r in rows if r['_y'] and r['_y'] < 1600 and r['Cast Date'].startswith('c'))}
yrs = C.Counter(r['_y'] for r in rows if r['_y'])
out['year_counts'] = dict(sorted(yrs.items()))

def fit(pairs):
    n = len(pairs); mx = sum(a for a, _ in pairs) / n; my = sum(b for _, b in pairs) / n
    sxx = sum((a - mx) ** 2 for a, _ in pairs); b = sum((a - mx) * (c - my) for a, c in pairs) / sxx
    sd = math.sqrt(sum((c - (my + b * (a - mx))) ** 2 for a, c in pairs) / (n - 2))
    return {'n': n, 'slope': b, 'resid_sd_octaves': sd / math.log10(2)}
grp = C.defaultdict(list)
for r in rows:
    f = num(r['Nominal (Hz)']); w = num(r['Weight (lbs)'])
    if f and w and r['Weight (approx)'] != 'Y' and r['_y']:
        k = 'before 1800' if r['_y'] < 1800 else ('1800-1899' if r['_y'] < 1900 else '1900 and after')
        grp[(k, r['Shape'])].append((math.log10(w), math.log10(f)))
out['fit_by_era_shape'] = {'%s / %s' % k: fit(v) for k, v in sorted(grp.items()) if len(v) > 30}
json.dump(out, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in out.items() if k not in ('year_counts', 'r_hist_5c', 'tenor_d_hist_10c')}, indent=1))
