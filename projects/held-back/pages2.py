"""Project 15, session 2: parses the UN depositary pages fetched to scratch (personal use; nothing of a page is committed).
For each treaty page: the participants table (name, date of joining, note numbers) and each state's entry (text, note numbers),
and the footnotes by number."""
import html, os, re

D = os.environ.get('HELD_BACK_PAGES', '/tmp/claude-0/-home-user-n-1/0b77fdd6-0f75-5d4b-be0f-3a5a56bf2ec0/scratchpad/pages')
NO = {'CERD': 'IV-2', 'ICESCR': 'IV-3', 'ICCPR': 'IV-4', 'CEDAW': 'IV-8', 'CAT': 'IV-9', 'CRC': 'IV-11', 'CRMW': 'IV-13',
      'CRPD': 'IV-15', 'CED': 'IV-16'}
MONTHS = 'January February March April May June July August September October November December'.split()
MON = {m[:3]: i + 1 for i, m in enumerate(MONTHS)}
DATE = re.compile(r'\b(\d{1,2})\s+(' + '|'.join(MONTHS) + r')\s+(\d{4})\b')


def clean(s):
    s = re.sub(r'<script.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<br\s*/?>|</p>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'[ \t\xa0]+', ' ', html.unescape(s)).strip()


def name_of(cell):
    return clean(re.sub(r'<SUP>.*?</SUP>', '', cell, flags=re.S | re.I)).strip(' ,')


def parse(treaty):
    t = open(os.path.join(D, NO[treaty] + '.html'), encoding='utf-8', errors='replace').read()
    parts = {}
    for row in re.findall(r'<tr class="trB[^"]*">(.*?)</tr>', t, flags=re.S):
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, flags=re.S)
        if len(cells) < 2:
            continue
        name = name_of(cells[0])
        last = clean(cells[-1])
        m = re.match(r'(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})\s*([a-zA-Z]?)', last)
        if not name or not m:
            continue
        parts[name] = {'joined': (int(m.group(3)), MON[m.group(2)], int(m.group(1))), 'how': m.group(4) or 'r',
                       'notes': re.findall(r"href='#(\d+)'", cells[0])}
    entries = {}
    for m in re.finditer(r'divParticipant" class="heading-two">(.*?)</div>\s*<div id="[^"]*divText" class="content-two">(.*?)</div>\s*</td>', t, flags=re.S):
        name = name_of(m.group(1))
        e = entries.setdefault(name, {'text': '', 'notes': []})
        e['text'] += clean(m.group(2)) + '\n'
        e['notes'] += re.findall(r"href='#(\d+)'", m.group(1)) + re.findall(r"href='#(\d+)'", m.group(2))
    notes = {}
    for m in re.finditer(r"<a name='(\d+)'>(.*?)(?=<a name='\d+'>|</table>\s*</div>\s*$)", t, flags=re.S):
        notes[m.group(1)] = clean(m.group(2))
    return parts, entries, notes


def footnotes(name, parts, entries, notes):
    ns = list(parts.get(name, {}).get('notes', [])) + list(entries.get(name, {}).get('notes', []))
    seen = []
    for n in ns:
        if n not in seen:
            seen.append(n)
    return [(n, notes.get(n, '')) for n in seen]


def late_sentences(text):
    """Sentences that withdraw a reservation or declaration (not an objection) with a date in 2015 or later."""
    out = []
    for s in re.split(r'(?<=[.;])\s+(?=[A-Z0-9])', text):
        low = s.lower()
        if 'withdr' in low and ('reserv' in low or 'declar' in low) and 'objection' not in low:
            yrs = [int(y) for _, _, y in DATE.findall(s)]
            if any(y >= 2015 for y in yrs):
                out.append((max(yrs), s))
    return out
