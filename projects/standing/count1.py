"""Project 22, session 1: the registered count (SELECTION.md). Run once, after this file is pushed.

Usage: python3 -I count1.py <wcvp_names.csv> <out.json>
"""
import csv, json, re, sys, statistics, random
from collections import Counter, defaultdict

csv.field_size_limit(10**9)
YEAR = re.compile(r'(?<!\d)(\d{4})(?!\d)')
VOID = {'Illegitimate', 'Invalid', 'Orthographic', 'Misapplied'}


def year_of(s):
    for m in YEAR.finditer(s or ''):
        y = int(m.group(1))
        if 1753 <= y <= 2026:
            return y
    return None


def kind(status, homo):
    if status == 'Accepted':
        return 'standing'
    if status == 'Synonym':
        return 'moved' if homo.strip().upper() == 'TRUE' else 'merged'
    if status in VOID:
        return 'void'
    if status == 'Unplaced':
        return 'unjudged'
    return 'other:' + status


def main(src, out):
    rows = 0
    year_by_id = {}
    sp = []  # (id, year, kind, basionym_id)
    with open(src, encoding='utf-8', newline='') as f:
        r = csv.DictReader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        for d in r:
            rows += 1
            y = year_of(d['first_published'])
            if y is not None:
                year_by_id[d['plant_name_id']] = y
            if d['taxon_rank'] == 'Species':
                sp.append((d['plant_name_id'], y, kind(d['taxon_status'], d['homotypic_synonym'] or ''),
                           d['basionym_plant_name_id'] or '', d['first_published']))
    n_sp = len(sp)
    with_year = [s for s in sp if s[1] is not None]
    kinds_all = Counter(s[2] for s in sp)
    kinds_y = Counter(s[2] for s in with_year)
    by_year = defaultdict(Counter)
    by_dec = defaultdict(Counter)
    for _, y, k, _, _ in with_year:
        by_year[y][k] += 1
        by_dec[min(y // 10 * 10, 2020)][k] += 1

    def share(c):
        t = sum(c.values())
        return round(c['standing'] / t, 4) if t else None

    dec_tab = {str(d): {'n': sum(c.values()), 'share_standing': share(c), **dict(c)} for d, c in sorted(by_dec.items())}
    big = {d: v for d, v in dec_tab.items() if v['n'] >= 1000}
    top = max(big, key=lambda d: big[d]['share_standing'])
    low = min(big, key=lambda d: big[d]['share_standing'])

    def moved_share(lo, hi):
        c = Counter(k for _, y, k, _, _ in with_year if lo <= y <= hi and k in ('moved', 'merged'))
        t = c['moved'] + c['merged']
        return round(c['moved'] / t, 4) if t else None, t

    standing = [s for s in sp if s[2] == 'standing']
    with_bas = [s for s in standing if s[3]]
    waits = [s[1] - year_by_id[s[3]] for s in with_bas if s[1] is not None and s[3] in year_by_id]
    syn = kinds_all['moved'] + kinds_all['merged']
    ms_early, n_early = moved_share(1753, 1799)
    ms_20c, n_20c = moved_share(1900, 1999)
    overall = share(kinds_y)

    rnd = random.Random(20261104)
    sample = rnd.sample(with_year, 12)
    raw20 = [s[4] for s in random.Random(1).sample(sp, 20)]

    res = {
        'rows': rows, 'species_names': n_sp, 'species_with_year': len(with_year),
        'share_with_year': round(len(with_year) / n_sp, 4),
        'kinds_all_species': dict(kinds_all), 'kinds_species_with_year': dict(kinds_y),
        'share_standing_overall': overall,
        'decades': dec_tab, 'top_decade': top, 'low_decade': low,
        'moved_share_1753_1799': ms_early, 'synonyms_1753_1799': n_early,
        'moved_share_1900_1999': ms_20c, 'synonyms_1900_1999': n_20c,
        'standing_n': len(standing), 'standing_with_basionym': len(with_bas),
        'share_standing_with_basionym': round(len(with_bas) / len(standing), 4),
        'waits_n': len(waits), 'wait_median': statistics.median(waits) if waits else None,
        'wait_quartiles': statistics.quantiles(waits, n=4) if len(waits) > 3 else None,
        'years': {str(y): dict(c) for y, c in sorted(by_year.items())},
        'check_sample': [{'plant_name_id': s[0], 'year': s[1], 'kind': s[2]} for s in sample],
        'raw_first_published_20': raw20,
    }
    p = {
        'P1': 1_300_000 <= rows <= 1_700_000,
        'P2': res['share_with_year'] >= 0.95,
        'P3': 0.30 <= overall <= 0.45,
        'P4': top in ('2010', '2020') and big[top]['share_standing'] >= 0.75,
        'P5': 1800 <= int(low) <= 1899,
        'P6': kinds_all['merged'] > kinds_all['moved'],
        'P7': (ms_early is not None and ms_20c is not None and ms_early > ms_20c),
        'P8': res['share_standing_with_basionym'] >= 0.35,
        'P9': (res['wait_median'] is not None and res['wait_median'] >= 50),
        'P10': kinds_all['unjudged'] / n_sp <= 0.05,
    }
    res['predictions'] = {k: bool(v) for k, v in p.items()}
    res['P11'] = 'checked separately (check1.py)'
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ('years', 'decades')}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
