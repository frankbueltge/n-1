"""Build works/between-the-keys/index.html from template.html and two committed files of project 20, session 3
(projects/the-nominal/session3.json, explore3.json). Usage: python3 build.py"""
import json, math, os

H = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(H, '..', '..', 'projects', 'the-nominal')
S = json.load(open(os.path.join(P, 'session3.json')))
E = json.load(open(os.path.join(P, 'explore3.json')))

rows = []
for k, v in S['decades'].items():
    rows.append({'label': k + 's', 'n': v['n'], 'cells': v['cells'], 'at440': v['at_440'], 'at435': v['at_435'],
                 'beat': v['median_beat_hz'], 'R': v['R']})
ny = S['no_year']
if ny['n']:
    rows.append({'label': 'no year', 'n': ny['n'], 'cells': ny['cells'], 'at440': ny['at_440'], 'at435': ny['at_435'],
                 'beat': ny['median_beat_hz'], 'R': ny['R']})

data = [{'label': r['label'], 'n': r['n'], 'at440': r['at440'],
         'cells': {str(i): c for i, c in enumerate(r['cells']) if c}} for r in rows]

# the raster: one row per decade, one column per cent
cw, rh, lx = 6, 6, 44
W, Hh = lx + 100 * cw + 4, 14 + len(rows) * rh + 4
mx = max(max(r['cells']) for r in rows)
out = [f'<svg class="raster" viewBox="0 0 {W} {Hh}" role="img" aria-label="Rings by decade and by cent between two keys">']
for i, r in enumerate(rows):
    y = 14 + i * rh
    out.append(f'<rect class="rb" data-i="{i}" x="0" y="{y}" width="{W}" height="{rh}"><title>{r["label"]}: {r["n"]} rings, '
               f'{r["at440"]} on A = 440</title></rect>')
    for c, n in enumerate(r['cells']):
        if n:
            op = 0.12 + 0.88 * math.sqrt(n / mx)
            out.append(f'<rect class="c" x="{lx + c * cw}" y="{y + .5}" width="{cw - .6:.1f}" height="{rh - 1}" opacity="{op:.2f}" pointer-events="none"/>')
    lab = r['label']
    if lab == 'no year' or (lab[:-1].isdigit() and int(lab[:-1]) % 50 == 0):
        out.append(f'<text class="lab" x="{lx - 4}" y="{y + rh - .5}" text-anchor="end">{lab}</text>')
for x, t, dash in [(lx + 50 * cw, 'A = 440', ''), (lx + (50 - 19.8) * cw, '435', ' stroke-dasharray="1.5 1.5"')]:
    out.append(f'<line class="mk" x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="{Hh - 2}"{dash} pointer-events="none"/>')
    out.append(f'<text class="mkl" x="{x:.1f}" y="8" text-anchor="middle">{t}</text>')
out.append(f'<text class="lab" x="{lx}" y="8">−50 cents</text><text class="lab" x="{lx + 100 * cw}" y="8" text-anchor="end">+50</text>')
out.append('</svg>')
raster = '\n'.join(out)

tr = ['<table><thead><tr><th>Decade</th><th>Rings</th><th>On A = 440</th><th>On A = 435</th><th>Median beat (per second)</th></tr></thead><tbody>']
for r in rows:
    tr.append(f'<tr><td>{r["label"]}</td><td>{r["n"]:,}</td><td>{r["at440"]}</td><td>{r["at435"]}</td><td>{r["beat"]:.1f}</td></tr>')
tr.append('</tbody></table><p class="aside">“On” a pitch: within 1.5 cents of it. Beat: the difference in vibrations a second between the '
          'ring, moved next to A, and A = 440.</p>')
table = '\n'.join(tr)

D = S['decades']
pct = lambda v: f'{100 * v["share_440"]:.0f} %'
late = E['1990-2029']
rep = {'{{RINGS}}': f'{S["rings"]:,}', '{{BEAT1900}}': f'{S["median_beat_before_1900"]:.1f}',
       '{{S1970}}': pct(D['1970']), '{{S1980}}': pct(D['1980']),
       '{{OLD1990}}': str(late['tenor_50y_older_than_tuning']['n']), '{{N1990}}': str(late['all']['n']),
       '{{BEATOLD}}': f'{late["tenor_50y_older_than_tuning"]["median_beat_hz"]:.1f}',
       '{{BEATNEW}}': f'{late["tenor_new_when_sounded"]["median_beat_hz"]:.1f}',
       '{{RASTER}}': raster, '{{TABLE}}': table, '{{DATA}}': json.dumps(data, separators=(',', ':'))}
t = open(os.path.join(H, 'template.html')).read()
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t
open(os.path.join(H, 'index.html'), 'w').write(t)
print('ok', len(t), 'bytes', len(rows), 'rows')
