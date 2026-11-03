"""Build works/the-year-on-the-concrete/index.html from template.html and two committed files of project 21, session 3
(projects/the-number-on-the-concrete/cells3.json, session3.json). Usage: python3 build.py"""
import json, math, os

H = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(H, '..', '..', 'projects', 'the-number-on-the-concrete')
C = json.load(open(os.path.join(P, 'cells3.json')))
S = json.load(open(os.path.join(P, 'session3.json')))
cells = C['cells']
assert all(c['n'] >= C['min_cell'] >= 10 for c in cells)
Y0, Y1 = C['years']
N = C['world_n']

# the map: equal-angle, 75N to 60S, 5-degree squares, 10 units each
LAT_TOP, LAT_BOT = 80, -60
u = 10
W, Hh = 360 // 5 * u, (LAT_TOP - LAT_BOT) // 5 * u
m = [f'<svg id="map" viewBox="0 0 {W} {Hh}" role="img" aria-label="Squares of five degrees where ten or more runways stand">']
y_eq = (LAT_TOP - 0) / 5 * u
m.append(f'<line class="eq" x1="0" y1="{y_eq}" x2="{W}" y2="{y_eq}"/><text class="lab" x="3" y="{y_eq - 3}">equator</text>')
for c in cells:
    assert LAT_BOT <= c['lat'] < LAT_TOP
    x = (c['lon'] + 180) / 5 * u
    y = (LAT_TOP - c['lat'] - 5) / 5 * u
    m.append(f'<rect class="cell" x="{x:.0f}" y="{y:.0f}" width="{u}" height="{u}"/>')
m.append('</svg>')

# the line: world share by year
lx, rx, ty, by_ = 34, 700, 10, 150
dx = (rx - lx) / (Y1 - Y0)
sh = [a / N for a in C['world_agree']]
def py(s): return by_ - (s - 0.4) / 0.5 * (by_ - ty)
pts = [(lx + i * dx, py(s)) for i, s in enumerate(sh)]
k26 = 2026 - Y0
L = [f'<svg viewBox="0 0 720 172" role="img" aria-label="Share of runways whose number is right, by year">']
for v in (0.5, 0.6, 0.7, 0.8, 0.9):
    L.append(f'<line class="ax" x1="{lx}" y1="{py(v):.1f}" x2="{rx}" y2="{py(v):.1f}"/><text class="lab" x="{lx - 4}" y="{py(v) + 3:.1f}" text-anchor="end">{int(v * 100)} %</text>')
for yr in range(1900, 2031, 20):
    L.append(f'<text class="lab" x="{lx + (yr - Y0) * dx:.1f}" y="166" text-anchor="middle">{yr}</text>')
L.append('<polyline class="ln" points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts[:k26 + 1]) + '"/>')
L.append('<polyline class="fc" points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts[k26:]) + '"/>')
b = S['world_best_year_1900_2026'] - Y0
L.append(f'<circle class="pk" cx="{pts[b][0]:.1f}" cy="{pts[b][1]:.1f}" r="3"/><text class="lab" x="{pts[b][0]:.1f}" y="{pts[b][1] - 7:.1f}" text-anchor="middle">{Y0 + b}</text>')
L.append(f'<line id="nowline" class="now" data-x0="{lx}" data-dx="{dx:.4f}" x1="0" y1="{ty}" x2="0" y2="{by_}"/>')
L.append('</svg>')

dated = [c for c in cells if c['best'] is not None]
rows = ['<table><tr><th>The year they say</th><th>squares</th><th>runways in them</th></tr>']
for d in range(1900, 2030, 10):
    cs = [c for c in dated if d <= c['best'] < d + 10]
    rows.append(f'<tr><td>{d}s</td><td>{len(cs)}</td><td>{sum(c["n"] for c in cs)}</td></tr>')
und = [c for c in cells if c['best'] is None]
rows.append(f'<tr><td>no year (grey)</td><td>{len(und)}</td><td>{sum(c["n"] for c in und)}</td></tr></table>')

def pc(x): return f'{x * 100:.0f} %'
words = {0: 'none', 1: 'one', 2: 'two', 3: 'three'}
late = sum(1 for c in dated if c['best'] >= 2025)
data = {'years': C['years'], 'world_n': N, 'world_agree': C['world_agree'],
        'cells': [{'lat': c['lat'], 'lon': c['lon'], 'n': c['n'], 'agree': c['agree'], 'best': c['best'], 'range': c['range']} for c in cells]}
t = open(os.path.join(H, 'template.html')).read()
rep = {'{{N}}': f'{N:,}', '{{MAP}}': '\n'.join(m), '{{LINE}}': '\n'.join(L), '{{TABLE}}': '\n'.join(rows),
       '{{S1900}}': pc(sh[0]), '{{BEST}}': str(S['world_best_year_1900_2026']), '{{SBEST}}': pc(S['world_share_at_best']),
       '{{S2026}}': pc(sh[k26]), '{{S2030}}': pc(sh[-1]), '{{SHOWN}}': str(len(cells)), '{{DATED}}': str(len(dated)),
       '{{MEDB}}': str(int(math.floor(S['dated_median_best']))), '{{LATE}}': words.get(late, str(late)),
       '{{DATA}}': json.dumps(data, separators=(',', ':'))}
for k, v in rep.items():
    assert k in t, k
    t = t.replace(k, v)
assert '{{' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', len(t), 'bytes; cells', len(cells), 'dated', len(dated), 'late', late)
