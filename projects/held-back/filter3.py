"""Project 15 session 3: the pre-filter (SESSION3.md). For each treaty page, every participant whose entry or footnotes carry text is
sent to be read if the text names an article of a 2014-common provision or names no article; otherwise cleared. Writes filter3.json
(state, treaty, verdict, the article numbers found; no page text)."""
import json, re
import pages2

C = json.load(open('common3.json'))
ART = re.compile(r'\b(?:[Aa]rticles?|[Aa]rts?\.)\s+((?:[\dIVXivx]+\s*(?:\([^)]{1,6}\)\s*)*(?:,|and|or|to|through|-|–|&)?\s*)+)')
NUM = re.compile(r'\b(\d{1,3})\b')


def articles(text):
    found = set()
    for m in ART.finditer(text):
        found |= {int(n) for n in NUM.findall(re.sub(r'\([^)]*\)', ' ', m.group(1)))}
    return found


def run():
    out = []
    for t in pages2.NO:
        parts, entries, notes = pages2.parse(t)
        common = set(C['treaties'][t]['years']['2014']['common'])
        arts = {p['article'] for p in C['treaties'][t]['provisions'] if p['id'] in common}
        for name in sorted(set(parts) | set(entries)):
            text = entries.get(name, {}).get('text', '').strip()
            fn = ' '.join(x for _, x in pages2.footnotes(name, parts, entries, notes))
            if not text and not fn.strip():
                continue
            found = articles(text + ' ' + fn)
            hit = sorted(found & arts)
            verdict = 'read' if (hit or not found) else 'cleared'
            out.append({'treaty': t, 'state': name, 'verdict': verdict, 'common_articles_named': hit,
                        'names_no_article': not found, 'in_entries': name in entries,
                        'chars': len(text) + len(fn)})
    return out


if __name__ == '__main__':
    out = run()
    json.dump(out, open('filter3.json', 'w'), indent=0)
    from collections import Counter
    print(Counter((o['treaty'], o['verdict']) for o in out))
    print('read', sum(o['verdict'] == 'read' for o in out), 'cleared', sum(o['verdict'] == 'cleared' for o in out),
          'chars to read', sum(o['chars'] for o in out if o['verdict'] == 'read'))
