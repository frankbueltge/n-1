"""Project 20, session 3, sound check (SESSION3.md, P8), step 2: measure the frequency of each rendered strike from its samples
(upward zero crossings between 0.05 s and 1.05 s, linearly interpolated), without importing the synthesis.
Usage: sound3.py samples.json out.json"""
import json, math, sys
S = json.load(open(sys.argv[1])); out = {}
for o, v in S.items():
    x, sr = v['samples'], v['sr']
    a, b = int(0.05 * sr), int(1.05 * sr)
    z = [i - 1 + x[i - 1] / (x[i - 1] - x[i]) for i in range(a + 1, b) if x[i - 1] < 0 <= x[i]]
    f = (len(z) - 1) / ((z[-1] - z[0]) / sr)
    want = 440 * 2 ** (float(o) / 1200)
    out[o] = {'asked_hz': want, 'measured_hz': f, 'cents_off': 1200 * math.log2(f / want), 'crossings': len(z)}
P8 = all(abs(v['cents_off']) <= 0.5 for v in out.values())
out['P8'] = P8
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out, indent=1))
