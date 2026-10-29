"""Project 19, session 4: presence and blinding (SESSION4.md). For the 396 foods of session 3's check draw (less four exposed),
Open Food Facts is asked for code and selected_images only (never nutriments), one call per 1.0 s. Each nutrition photograph found is
downloaded full size, reduced (ImageMagick convert; the installed PIL does not load) to at most 1,568 px on its long edge and saved as <out>/blind/NNN.jpg, NNN from a shuffle seeded
2026102904. The key (NNN -> food) and the presence rows go to <out>/key4.json, which stays unopened until readings4.json is pushed.
Only aggregate counts are printed.
Usage: python3 -I fetch4.py <session3.json> <outdir>
"""
import json, os, random, subprocess, sys, time, urllib.request

UA = 'n-1 research practice (github.com/frankbueltge/n-1)'
EXPOSED = {'0021130156504', '0075278042625', '0041262277311', '0898655000564'}

def get(url, raw=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            b = resp.read()
            return 200, (b if raw else json.loads(b))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return str(e)[:80], None

def photo_url(p):
    disp = (((p or {}).get('selected_images') or {}).get('nutrition') or {}).get('display') or {}
    if not disp:
        return None, None
    lang = 'en' if 'en' in disp else sorted(disp)[0]
    return disp[lang], lang

def main(sess, out):
    d = json.load(open(sess))['draws']
    foods = [(k, fid, code) for k in ('check_given', 'check_kept') for fid, code, v, r in d[k] if code not in EXPOSED]
    rows = []
    for kind, fid, code in foods:
        st, j = get(f'https://world.openfoodfacts.org/api/v2/product/{code}.json?fields=code,selected_images')
        if j is None and st != 404:
            time.sleep(5); st, j = get(f'https://world.openfoodfacts.org/api/v2/product/{code}.json?fields=code,selected_images')
        p = (j or {}).get('product') if isinstance(j, dict) else None
        url, lang = photo_url(p)
        rows.append({'kind': kind, 'fdcId': fid, 'code': code, 'status': st, 'found': bool(p), 'photo': url, 'lang': lang,
                     'clock_utc': time.strftime('%H:%M:%S', time.gmtime())})
        time.sleep(1.0)
    with_photo = [x for x in rows if x['photo']]
    rng = random.Random(2026102904)
    order = list(range(len(with_photo))); rng.shuffle(order)
    os.makedirs(os.path.join(out, 'blind'), exist_ok=True)
    key = {}
    for n, i in enumerate(order, 1):
        x = with_photo[i]; nnn = '%03d' % n
        full = x['photo'].replace('.400.jpg', '.jpg')
        st, b = get(full, raw=True)
        x['fetched'] = full
        if b is None:
            st, b = get(x['photo'], raw=True); x['fetched'] = x['photo']
        if b is None:
            x['download'] = 'failed %s' % st
        else:
            raw = os.path.join(out, 'raw.bin'); open(raw, 'wb').write(b)
            dst = os.path.join(out, 'blind', nnn + '.jpg')
            cp = subprocess.run(['convert', raw, '-auto-orient', '-resize', '1568x1568>', '-quality', '90', dst], capture_output=True)
            x['download'] = 'ok' if cp.returncode == 0 and os.path.exists(dst) else 'convert failed'
        x['blind'] = nnn; key[nnn] = x['fdcId']
        time.sleep(0.5)
    json.dump({'rows': rows, 'key': key}, open(os.path.join(out, 'key4.json'), 'w'), indent=1)
    print('asked', len(rows), '| found', sum(x['found'] for x in rows), '| with photograph', len(with_photo),
          '| downloaded', sum(x.get('download') == 'ok' for x in with_photo),
          '| statuses', sorted({str(x['status']) for x in rows}))
    print('with photograph by kind (count only):', {k: sum(1 for x in with_photo if x['kind'] == k) for k in ('check_given', 'check_kept')})

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
