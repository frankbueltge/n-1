#!/usr/bin/env python3
"""Project 24 session 1, exploratory (not registered): the twin groups, the beginnings, the names without terms.
Usage: python3 -I explore1.py STRIPPED.txt NAMES.gz OUT.json"""
import json, sys, gzip, collections, statistics
groups = collections.defaultdict(list)
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('A'):
            a, _, body = line.rstrip('\n').partition(' ,'); groups[body].append(a)
names = {}
with gzip.open(sys.argv[2], 'rt', errors='replace') as f:
    for line in f:
        if line.startswith('A'):
            a, _, n = line.rstrip('\n').partition(' '); names[a] = n
seqs = set(a for v in groups.values() for a in v)
tw = [sorted(v) for v in groups.values() if len(v) > 1]
sizes = collections.Counter(len(v) for v in tw)
big = sorted(tw, key=lambda v: -len(v))[:8]
def nterms(body): return body.rstrip(',').count(',') + 1
lens = [nterms(b) for b, v in groups.items() if len(v) > 1]
gaps = []
for v in tw:
    nums = [int(a[1:]) for a in v]; gaps.append(max(nums) - min(nums))
out = {
 'twin_groups': len(tw), 'twin_sequences': sum(len(v) for v in tw), 'group_sizes': {str(k): sizes[k] for k in sorted(sizes)},
 'twin_shown_terms_median': statistics.median(lens),
 'twin_groups_with_at_least_20_terms': sum(1 for x in lens if x >= 20),
 'twin_group_anumber_span_median': statistics.median(gaps),
 'twin_groups_span_over_100000': sum(1 for g in gaps if g > 100000),
 'largest_groups': [{'size': len(v), 'first': v[0], 'last': v[-1], 'first_name': names.get(v[0], '')[:120]} for v in big],
 'names_without_terms': len(set(names) - seqs),
 'names_without_terms_examples': sorted(set(names) - seqs)[:5],
}
json.dump(out, open(sys.argv[3], 'w'), indent=1); print(json.dumps(out, indent=1))
