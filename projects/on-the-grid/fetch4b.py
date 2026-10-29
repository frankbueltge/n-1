"""Project 19, session 4: the full-size photographs (correction to fetch4.py). Open Food Facts serves a selected image's full size at
`.full.jpg`, not at `.jpg` as SESSION4.md assumed; fetch4.py's first try therefore failed for every image and took the registered fallback
(the 400 px display image), too small to read many panels. This script fetches `.full.jpg` for each photograph fetch4.py found, reduces it
as registered (at most 1,568 px), and saves it under the same blind number in <out>/blind_full/. It reads key4.json without printing it.
Usage: python3 -I fetch4b.py <outdir>
"""
import json, os, subprocess, sys, time, urllib.request

UA = 'n-1 research practice (github.com/frankbueltge/n-1)'

def main(out):
    k = json.load(open(os.path.join(out, 'key4.json')))
    os.makedirs(os.path.join(out, 'blind_full'), exist_ok=True)
    ok = fail = 0
    for x in k['rows']:
        if not x.get('photo'):
            continue
        url = x['photo'].replace('.400.jpg', '.full.jpg')
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
                b = r.read()
            raw = os.path.join(out, 'rawf.bin'); open(raw, 'wb').write(b)
            dst = os.path.join(out, 'blind_full', x['blind'] + '.jpg')
            cp = subprocess.run(['convert', raw, '-auto-orient', '-resize', '1568x1568>', '-quality', '90', dst], capture_output=True)
            if cp.returncode == 0:
                x['fetched_full'] = url; ok += 1
            else:
                fail += 1
        except Exception:
            fail += 1
        time.sleep(0.5)
    json.dump(k, open(os.path.join(out, 'key4.json'), 'w'), indent=1)
    print('full size ok', ok, '| failed', fail)

if __name__ == '__main__':
    main(sys.argv[1])
