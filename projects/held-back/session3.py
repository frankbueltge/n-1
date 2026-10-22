"""Project 15, session 3: the registered count of the clauses the file leaves out (SESSION3.md). Writes session3.json."""
import collections, hashlib, json, os, re
import lib3, pages2

out = {'pages_fetched': '2026-10-22 16:55 UTC', 'pages_sha256': {}, 'treaties': {}}
for t in lib3.TREATIES:
    p = os.path.join(pages2.D, pages2.NO[t] + '.html')
    out['pages_sha256'][pages2.NO[t]] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    v, parts, secs, unassigned, other = lib3.verdicts(t)
    now = collections.Counter(a for x in v.values() for a, s in x.items() if s == 'now')
    wd = collections.Counter(a for x in v.values() for a, s in x.items() if s == 'withdrawn')
    c = lib3.CLAUSE[t]
    others = {a: n for a, n in now.items() if a != c and not (t == 'CAT' and a == 20)}
    top_other = max(others.items(), key=lambda x: (x[1], -x[0])) if others else (None, 0)
    # sensitivity, not registered: sections that name the clause in a sentence accepting the Court or recording a withdrawal
    sens = {'accepts': [], 'withdraws_in_section': []}
    for name, x in v.items():
        if x.get(c) != 'now':
            continue
        for s in re.split(r'(?<=[.;])\s+(?=[A-Z0-9“"])', secs.get(name, {}).get('text', '')):
            if c in lib3.named(s, t):
                low = s.lower()
                if re.search(r'recogni[sz]es?|accepts?', low) and 'not' not in low.split():
                    sens['accepts'].append(name)
                if 'withdr' in low:
                    sens['withdraws_in_section'].append(name)
    out['treaties'][t] = {
        'parties': len(parts), 'sections': len(secs), 'sections_of_non_parties': unassigned,
        'clause': c, 'clause_now': now[c], 'clause_withdrawn': wd[c], 'clause_share': round(now[c] / len(parts), 4),
        'top_other_article': top_other[0], 'top_other_now': top_other[1],
        'cat20_now': now[20] if t == 'CAT' else None, 'cat20_withdrawn': wd[20] if t == 'CAT' else None,
        'now_by_article': dict(sorted(now.items())), 'withdrawn_by_article': dict(sorted(wd.items())),
        'clause_now_parties': sorted(n for n, x in v.items() if x.get(c) == 'now'),
        'sensitivity_not_registered': {k: sorted(set(x)) for k, x in sens.items()},
    }
T = out['treaties']
out['predictions'] = [
    {'n': 1, 'held': T['CEDAW']['now_by_article'].get(29, 0) > T['CEDAW']['now_by_article'].get(16, 0),
     'found': 'CEDAW 29: %d, CEDAW 16: %d' % (T['CEDAW']['now_by_article'].get(29, 0), T['CEDAW']['now_by_article'].get(16, 0))},
    {'n': 2, 'held': sum(T[t]['clause_now'] > T[t]['top_other_now'] for t in T) >= 4,
     'found': '; '.join('%s %d: %d against article %s: %d' % (t, T[t]['clause'], T[t]['clause_now'], T[t]['top_other_article'], T[t]['top_other_now']) for t in T)},
    {'n': 3, 'held': T['CAT']['cat20_now'] < T['CAT']['clause_now'], 'found': 'CAT 20: %d, CAT 30: %d' % (T['CAT']['cat20_now'], T['CAT']['clause_now'])},
    {'n': 5, 'held': any(T[t]['clause_share'] > .25 for t in T), 'found': '; '.join('%s %d: %d of %d (%.1f %%)' % (t, T[t]['clause'], T[t]['clause_now'], T[t]['parties'], 100 * T[t]['clause_share']) for t in T)},
]
json.dump(out, open('session3.json', 'w'), indent=1, ensure_ascii=False)
for t in T:
    print(t, {k: T[t][k] for k in ('parties', 'clause', 'clause_now', 'clause_withdrawn', 'clause_share', 'top_other_article', 'top_other_now', 'cat20_now', 'cat20_withdrawn')})
    print('   sens', T[t]['sensitivity_not_registered'])
    print('   now', T[t]['now_by_article'])
for p in out['predictions']:
    print(p)
