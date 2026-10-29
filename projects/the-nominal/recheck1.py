"""Project 20, session 1: compares check1.json's two sides field by field (the weight read as cwt-qr-lb or as an estimate in cwt,
converted to lb; nominal; note; this practice's d against Dove's own cents figure). Writes check1_compare.json."""
import json, re
FR = {'¼': .25, '½': .5, '¾': .75}
def lbs(cell):
    m = re.fullmatch(r'(\d+)–(\d)–(\d+)', cell)
    if m:
        return int(m.group(1)) * 112 + int(m.group(2)) * 28 + int(m.group(3))
    m = re.fullmatch(r'(\d+)([¼½¾]?)\s*cwt', cell.replace(' ', ' '))
    if m:
        return round((int(m.group(1)) + FR.get(m.group(2), 0)) * 112)
    return None
out = []
for o in json.load(open('check1.json')):
    p = o.get('page') or {}
    cells = p.get('cells', [])
    w = lbs(cells[2]) if len(cells) > 2 else None
    m = re.search(r'([+−-]\d+)\s*cents', p.get('pitch_title') or '')
    dove_c = int(m.group(1).replace('−', '-')) if m else None
    out.append({'bell_id': o['bell_id'], 'weight_equal': w == int(o['csv']['weight_lbs']),
                'nominal_equal': p.get('nominal_hz') == o['csv']['nominal_hz'], 'note_equal': cells[4] == o['csv']['note'] if len(cells) > 4 else False,
                'd_ours': o['d_ours'], 'dove_cents': dove_c, 'diff': None if dove_c is None else round(o['d_ours'] - dove_c, 1)})
agree = sum(1 for x in out if x['weight_equal'] and x['nominal_equal'] and x['note_equal'])
res = {'agree_all_three': agree, 'of': len(out), 'max_abs_diff_cents_vs_dove': max(abs(x['diff']) for x in out), 'bells': out}
json.dump(res, open('check1_compare.json', 'w'), indent=1, ensure_ascii=False)
print(agree, len(out), res['max_abs_diff_cents_vs_dove'], [x['diff'] for x in out])
