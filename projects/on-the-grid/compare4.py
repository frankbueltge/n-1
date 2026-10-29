"""Project 19, session 4: compare (SESSION4.md). Run only after readings4.json is committed and pushed. Joins the blind readings with
the key and session 3's draws; writes session4.json (outcomes, P1-P6) with FDC IDs, codes, photograph URLs, readings and outcomes.
Usage: python3 -I compare4.py <session3.json> <key4.json> <readings4.json> <fdc_servings.json> <session4.json>
fdc_servings.json: {fdcId: [servingSize, unit]} for the pool, written by servings4.py from the archive.
"""
import json, re, sys

def on_grid(c):
    return c == 0 or (c <= 50 and c % 5 == 0) or (c > 50 and c % 10 == 0)

def grams(text):
    m = re.findall(r'(\d+(?:\.\d+)?)\s*(g|ml|mL)\b', text or '')
    return float(m[-1][0]) if m else None

def main(sess, keyf, readf, servf, out):
    d = json.load(open(sess))['draws']
    num = {fid: (kind, code, v, r) for kind in ('check_given', 'check_kept') for fid, code, v, r in d[kind]}
    key = json.load(open(keyf)); rows = {x['fdcId']: x for x in key['rows']}
    reads = json.load(open(readf))['readings']
    serv = json.load(open(servf))
    res = []
    for nnn, fid in sorted(key['key'].items()):
        kind, code, v, r = num[fid]; rd = reads.get(nnn, {'legible': False, 'why': 'not read'})
        x = {'blind': nnn, 'kind': kind, 'fdcId': fid, 'code': code, 'photo': rows[fid]['fetched'], 'v': v, 'r': r,
             'legible': rd['legible'], 'read': rd.get('kcal'), 'serving_read': rd.get('serving'), 'why': rd.get('why'),
             'note': rd.get('note')}
        if rd['legible']:
            k = float(rd['kcal'])
            x['r_eq'] = abs(r - k) < 1e-6; x['v_eq'] = abs(v - k) < 1e-6; x['read_on_grid'] = on_grid(k)
            s = serv.get(str(fid)); g = grams(rd.get('serving'))
            x['fdc_serving'] = s; x['serving_match'] = bool(s and g is not None and abs(s[0] - g) < 1e-6)
        res.append(x)
    G = [x for x in res if x['kind'] == 'check_given' and x['legible']]
    K = [x for x in res if x['kind'] == 'check_kept' and x['legible']]
    L = [x for x in res if x['legible']]
    pct = lambda a, b: round(100.0 * a / b, 2) if b else None
    GS = [x for x in G if x['serving_match']]
    agg = {
        'pool': 396, 'with_photograph': len(res), 'legible': len(L), 'legible_given': len(G), 'legible_kept': len(K),
        'illegible_reasons': {w: sum(1 for x in res if not x['legible'] and x['why'] == w) for w in sorted({x['why'] for x in res if not x['legible']})},
        'given_r_eq': sum(x['r_eq'] for x in G), 'given_v_eq': sum(x['v_eq'] for x in G),
        'given_neither': sum(not x['r_eq'] and not x['v_eq'] for x in G),
        'kept_v_eq': sum(x['v_eq'] for x in K), 'read_on_grid': sum(x['read_on_grid'] for x in L),
        'given_serving_match': len(GS), 'given_serving_match_r_eq': sum(x['r_eq'] for x in GS),
    }
    P = {
        'P1 >= 20 given back legible': len(G) >= 20,
        'P2 r == read >= 70 %': (pct(agg['given_r_eq'], len(G)), (pct(agg['given_r_eq'], len(G)) or 0) >= 70),
        'P3 v == read <= 10 %': (pct(agg['given_v_eq'], len(G)), G and pct(agg['given_v_eq'], len(G)) <= 10),
        'P4 kept v == read >= 70 %': (pct(agg['kept_v_eq'], len(K)), (pct(agg['kept_v_eq'], len(K)) or 0) >= 70),
        'P5 read on grid >= 95 %': (pct(agg['read_on_grid'], len(L)), (pct(agg['read_on_grid'], len(L)) or 0) >= 95),
        'P6 serving match r == read >= 85 %': ('not reported, fewer than 10' if len(GS) < 10 else
                                              (pct(agg['given_serving_match_r_eq'], len(GS)), pct(agg['given_serving_match_r_eq'], len(GS)) >= 85)),
    }
    json.dump({'agg': agg, 'predictions': P, 'rows': res}, open(out, 'w'), indent=1)
    print(json.dumps(agg, indent=1)); print(json.dumps(P, indent=1))

if __name__ == '__main__':
    main(*sys.argv[1:6])
