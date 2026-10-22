"""Project 15, session 2: the registered count after the file's last year (SESSION2.md). Writes session2.json."""
import collections, hashlib, json, os, statistics
import lib2, pages2

f = lib2.flags()
pairs = sorted(f)
matched = [k for k in pairs if f[k] is not None]
flagged = [k for k in matched if f[k]]
by_treaty = collections.Counter(t for _, t in flagged)
standing_by_treaty = collections.Counter(t for _, t in matched)
years = collections.Counter(max(y for y, _ in f[k]) for k in flagged)

# sensitivity, not registered: the same sentence rule run over the entry text as well
pages = {t: pages2.parse(t) for t in pages2.NO}
entry_only = []
for c, t in matched:
    if f[(c, t)]:
        continue
    name = lib2.NAMES.get(c, c)
    if pages2.late_sentences(pages[t][1].get(name, {}).get('text', '')):
        entry_only.append([c, t])

# new holding back after 2014: participants joining 2015 or later whose entry carries text
new = {}
for t, (parts, entries, _) in pages.items():
    late = sorted(n for n, p in parts.items() if p['joined'][0] >= 2015)
    with_text = [n for n in late if entries.get(n, {}).get('text', '').strip()]
    new[t] = {'joined_2015_or_later': len(late), 'with_entry_text': len(with_text), 'states_with_entry_text': with_text}
new_total = sum(v['with_entry_text'] for v in new.values())

hashes = {pages2.NO[t]: hashlib.sha256(open(os.path.join(pages2.D, pages2.NO[t] + '.html'), 'rb').read()).hexdigest()
          for t in pages2.NO}
out = {
    'file_sha256': lib2.lib.SHA256,
    'pages_fetched': '2026-10-22 12:17 UTC', 'pages_sha256': hashes,
    'standing_pairs': len(pairs), 'unmatched': [list(k) for k in pairs if f[k] is None],
    'matched': len(matched), 'flagged_late': len(flagged), 'flagged_share': round(len(flagged) / len(matched), 4),
    'flagged_by_treaty': dict(by_treaty.most_common()), 'standing_by_treaty': dict(standing_by_treaty.most_common()),
    'latest_year_by_pair': dict(sorted(years.items())),
    'median_latest_year': statistics.median(max(y for y, _ in f[k]) for k in flagged) if flagged else None,
    'flagged_pairs': [[c, t, sorted({y for y, _ in f[(c, t)]})] for c, t in flagged],
    'sensitivity_entry_text_only': entry_only,
    'new_after_2014': new, 'new_after_2014_with_entry_text': new_total,
}
json.dump(out, open('session2.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in out.items() if k not in ('flagged_pairs', 'new_after_2014', 'pages_sha256')}, indent=1, ensure_ascii=False))
print({t: (v['joined_2015_or_later'], v['with_entry_text']) for t, v in new.items()})
