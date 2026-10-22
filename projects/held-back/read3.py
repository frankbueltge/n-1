"""Project 15 session 3: prints one state's entry and footnotes from a page fetched to scratch, for reading by hand (personal use;
nothing printed here is committed). Usage: python3 read3.py sheet3.json | python3 read3.py TREATY 'State' ['State' ...]"""
import json, sys
import pages2

_cache = {}


def show(t, name):
    if t not in _cache:
        _cache[t] = pages2.parse(t)
    parts, entries, notes = _cache[t]
    e = entries.get(name, {}).get('text', '').strip()
    print('=====', t, '|', name, '| joined', parts.get(name, {}).get('joined'))
    if e:
        print('[entry]', e)
    for n, x in pages2.footnotes(name, parts, entries, notes):
        print('[note %s]' % n, x)


if __name__ == '__main__':
    if sys.argv[1].endswith('.json'):
        for x in json.load(open(sys.argv[1])):
            print('#%d' % x['n'], end=' ')
            show(x['treaty'], x['state'])
    else:
        for s in sys.argv[2:]:
            show(sys.argv[1], s)
