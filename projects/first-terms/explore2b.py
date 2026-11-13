#!/usr/bin/env python3
"""Project 24 session 2, exploratory (not registered): share never found alone by A-number band; M = 1 by band.
Usage: python3 -I explore2b.py SESSION2-PER.json OUT.json"""
import json, sys
per = json.load(open(sys.argv[1]))
bands = [(1, 1000), (1001, 10000), (10001, 100000), (100001, 200000), (200001, 300000), (300001, 500000)]
out = []
for lo, hi in bands:
    rs = [r for r in per if lo <= int(r[0][1:]) <= hi]
    al = [r for r in rs if r[3] > 0]
    out.append({'from': f'A{lo:06d}', 'to': f'A{hi:06d}', 'sequences': len(rs),
                'never_found_alone': sum(1 for r in rs if r[3] == 0),
                'never_share': sum(1 for r in rs if r[3] == 0) / len(rs),
                'M_eq_1_share_of_alone': sum(1 for r in al if r[4] == 1) / len(al),
                'B_median': sorted(r[3] for r in al)[len(al) // 2]})
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out, indent=1))
