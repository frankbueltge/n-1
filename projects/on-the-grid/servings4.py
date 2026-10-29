"""Project 19, session 4: FoodData Central's serving size for the 400 foods of session 3's check draw, read from the archive, for
compare4.py's serving comparison (SESSION4.md, P6). Writes {fdcId: [servingSize, servingSizeUnit, householdServingFullText]}.
Usage: python3 -I servings4.py <session3.json> <branded_food_json> <out.json>
"""
import json, sys

def main(sess, path, out):
    d = json.load(open(sess))['draws']
    want = {fid for k in ('check_given', 'check_kept') for fid, code, v, r in d[k]}
    DEC = json.JSONDecoder(); got = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            s_ = line.strip().rstrip(',')
            if not s_.startswith('{') or '"fdcId"' not in s_:
                continue
            try:
                r = DEC.raw_decode(s_)[0]
            except ValueError:
                continue
            if r.get('fdcId') in want:
                got[r['fdcId']] = [r.get('servingSize'), r.get('servingSizeUnit'), r.get('householdServingFullText')]
    json.dump(got, open(out, 'w'), indent=0)
    print('found', len(got), 'of', len(want))

if __name__ == '__main__':
    main(*sys.argv[1:4])
