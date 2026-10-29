"""Project 20, session 1: the registered check. Twenty bells with a nominal, drawn with seed 20261029; each tower's Dove page read
(one request per 3 s), the bell's own table row found by its id (bell-<Bell ID>), and weight, nominal and note compared with the CSV.
Also read: the page's own cents figure for the bell (the frequency's tooltip), compared with this practice's d (SELECTION.md).
Writes check1.json (the twenty bells' fields and the comparison)."""
import csv, json, math, random, re, sys, time, html, urllib.request
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from count1_lib import pc, dev

rows = [r for r in csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')) if r['Nominal (Hz)'].strip()]
rows.sort(key=lambda r: int(r['Bell ID']))
draw = random.Random(20261029).sample(rows, 20)
out = []
for r in draw:
    url = 'https://dove.cccbr.org.uk/tower/%s' % r['Tower ID']
    rec = {'bell_id': r['Bell ID'], 'tower': url, 'role': r['Bell Role'], 'csv': {'weight_lbs': r['Weight (lbs)'],
           'approx': r['Weight (approx)'], 'nominal_hz': r['Nominal (Hz)'], 'note': r['Note']}}
    try:
        page = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'n-1 research (remainder@n-1.invalid)'}), timeout=30).read().decode('utf-8', 'replace')
        m = re.search(r'<tr id="bell-%s".*?</tr>' % re.escape(r['Bell ID']), page, re.S)
        if not m:
            rec['status'] = 'row not found'
        else:
            row = m.group(0)
            cells = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)]
            wt = re.search(r'title="([\d.]+) lb', row)
            fq = re.search(r'title="([^"]*)" class="bell-pitch">([\d.]+)<', row)
            rec['page'] = {'cells': cells[:6], 'weight_lbs': wt.group(1) if wt else None,
                           'nominal_hz': fq.group(2) if fq else None, 'pitch_title': html.unescape(fq.group(1)) if fq else None}
            rec['status'] = 'ok'
            p = pc(r['Note'])
            rec['d_ours'] = round(dev(float(r['Nominal (Hz)']), p), 1) if p is not None else None
    except Exception as e:
        rec['status'] = 'error: %s' % e
    out.append(rec)
    time.sleep(3)
json.dump(out, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
for o in out:
    print(o['bell_id'], o['csv'], o.get('page'), o.get('d_ours'), o['status'])
