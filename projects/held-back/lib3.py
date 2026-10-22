"""Project 15, session 3: the clauses the file leaves out, read from the UN depositary pages fetched to scratch (personal use; nothing
of a page is committed). Separation rule, read when the pages were fetched: a state's own reservations-and-declarations entry is a
block whose text div id contains '_dgDec_'; objections are '_dgObj_', competence declarations '_dgDecUnderArticle_'."""
import os, re
import pages2

pages2.D = os.environ.get('HELD_BACK_PAGES', '/tmp/claude-0/-home-user-n-1/515a6970-2dd1-537a-882b-5550e799735f/scratchpad/pages')
TREATIES = ['CERD', 'CEDAW', 'CAT', 'CRMW', 'CED']
CLAUSE = {'CERD': 22, 'CEDAW': 29, 'CAT': 30, 'CRMW': 92, 'CED': 42}
MAXART = {'CERD': 25, 'CEDAW': 30, 'CAT': 33, 'CRMW': 93, 'CED': 45}
ALIAS = {('CAT', 28): 20}  # a refusal of CAT 20 is made under CAT 28


def sections(treaty):
    t = open(os.path.join(pages2.D, pages2.NO[treaty] + '.html'), encoding='utf-8', errors='replace').read()
    out, other = {}, 0
    for m in re.finditer(r'divParticipant" class="heading-two">(.*?)</div>\s*<div id="([^"]*)divText" class="content-two">(.*?)</div>\s*</td>', t, flags=re.S):
        if '_dgDec_' not in m.group(2):
            if '_dgObj_' not in m.group(2) and '_dgDecUnderArticle_' not in m.group(2):
                other += 1
            continue
        name = pages2.name_of(m.group(1))
        e = out.setdefault(name, {'text': '', 'notes': []})
        e['text'] += pages2.clean(m.group(3)) + '\n'
        e['notes'] += re.findall(r"href='#(\d+)'", m.group(1)) + re.findall(r"href='#(\d+)'", m.group(3))
    return out, other


def named(text, treaty):
    """Article numbers the text names: 'article N' (so also 'paragraph .. of article N'), or 'articles' followed within the same
    sentence and 80 characters by N as a whole number in a list (parenthesised paragraph marks removed first)."""
    found = set()
    for m in re.finditer(r'\barticle(s|\(s\))?\b', text, flags=re.I):
        rest = text[m.end():]
        if not m.group(1):
            n = re.match(r'\s*(\d+)\b', rest)
            if n:
                found.add(int(n.group(1)))
            continue
        chunk = re.split(r'\.\s|;|\n', rest[:80])[0]
        chunk = re.sub(r'\([^)]*\)', ' ', chunk)
        found |= {int(x) for x in re.findall(r'\b(\d+)\b', chunk)}
    found = {ALIAS.get((treaty, n), n) for n in found}
    return {n for n in found if 1 <= n <= MAXART[treaty]}


def verdicts(treaty):
    """party -> {article: 'now' | 'withdrawn'}; plus parties, sections not assigned."""
    parts, _, notes = pages2.parse(treaty)
    secs, other = sections(treaty)
    out = {}
    for name in parts:
        sec = secs.get(name, {'text': '', 'notes': []})
        now = named(sec['text'], treaty)
        wd = set()
        ns = []
        for n in parts[name]['notes'] + sec['notes']:
            if n not in ns:
                ns.append(n)
        for n in ns:
            txt = notes.get(n, '')
            for s in re.split(r'(?<=[.;])\s+(?=[A-Z0-9])', txt):
                low = s.lower()
                if 'withdr' in low and 'objection' not in low:
                    wd |= named(s, treaty)
        v = {a: 'withdrawn' for a in wd}
        v.update({a: 'now' for a in now - wd})
        out[name] = v
    unassigned = sorted(set(secs) - set(parts))
    return out, parts, secs, unassigned, other
