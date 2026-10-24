"""Project 18, session 1: exploratory, after the registered count (not registered; reported as exploration).
First-track offsets (the pregap), and tables whose lead-out lies past 99:59.74 (449,999 frames), the largest address a
minutes:seconds:frames field of two digits each can hold (conjecture as to drives; stated as arithmetic). Writes explore1.json.
Usage: python3 -I explore1.py <path to mbdump/cdtoc>
"""
import json, sys
from collections import Counter

first = Counter()
past = []
over80 = Counter()
for line in open(sys.argv[1], encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    tc, leadout = int(f[3]), int(f[4])
    offs = [int(x) for x in f[5].strip("{}").split(",")]
    first[offs[0]] += 1
    L = leadout - offs[0]
    if leadout > 449999:
        past.append({"discid": f[1], "tracks": tc, "leadout": leadout, "seconds": round(L / 75, 2)})
    if L >= 4800 * 75:
        over80[min((L // 75) // 60, 100)] += 1
n = sum(first.values())
out = {
    "first_offset_top20": [{"frames": k, "discs": v} for k, v in first.most_common(20)],
    "first_offset_150": first[150],
    "first_offset_under_150": sum(v for k, v in first.items() if k < 150),
    "first_offset_151_to_224": sum(v for k, v in first.items() if 150 < k < 225),
    "first_offset_225_or_more": sum(v for k, v in first.items() if k >= 225),
    "first_offset_225_or_more_median_seconds": None,
    "leadout_past_99_59_74": len(past),
    "leadout_past_examples": sorted(past, key=lambda r: -r["leadout"])[:10],
    "over_80_by_minute": {str(k): over80[k] for k in sorted(over80)},
    "n": n,
}
big = sorted(k for k, v in first.items() if k >= 225 for _ in range(v))
if big:
    out["first_offset_225_or_more_median_seconds"] = round((big[len(big) // 2] - 150) / 75, 2)
json.dump(out, open("explore1.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "leadout_past_examples"}, indent=1))
