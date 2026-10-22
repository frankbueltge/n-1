"""Reads one state's entry and its footnotes from a UN depositary page fetched to scratch (personal use; nothing of the page is
committed). Usage: python3 pageread.py MTDSG_NO 'State name'."""
import html, re, sys, os
D = '/tmp/claude-0/-home-user-n-1/fc2cde3e-6a77-59a1-af4d-cbfbcd3e8cb5/scratchpad/probe'


def clean(s):
    s = re.sub(r'<script.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<br\s*/?>|</p>', '\n', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'[ \t\xa0]+', ' ', html.unescape(s)).strip()


def entry(no, state):
    t = open(os.path.join(D, no + '.html'), encoding='utf-8', errors='replace').read()
    out = []
    for m in re.finditer(r'divParticipant" class="heading-two">(.*?)</div>\s*<div id="[^"]*divText" class="content-two">(.*?)</div>\s*</td>', t, flags=re.S):
        name = clean(re.sub(r'<SUP>.*?</SUP>', '', m.group(1), flags=re.S))
        if name == state:
            notes = re.findall(r"href='#(\d+)'", m.group(1))
            out.append(('ENTRY', clean(m.group(2)), notes))
    # participant table footnotes too (state name in status table)
    for m in re.finditer(r'>\s*' + re.escape(state) + r'\s*(<SUP>.*?</SUP>)', t, flags=re.S):
        out.append(('NAME-NOTES', '', re.findall(r"href='#(\d+)'", m.group(1))))
    notes = sorted({n for _, _, ns in out for n in ns}, key=int)
    res = []
    for n in notes:
        m = re.search(r"<a name='" + n + r"'>(.*?)(?=<a name='\d+'>|$)", t, flags=re.S)
        if m:
            res.append((n, clean(m.group(1))[:6000]))
    return out, res


if __name__ == '__main__':
    out, res = entry(sys.argv[1], sys.argv[2])
    for kind, text, ns in out:
        if text or kind == 'ENTRY':
            print('==', kind, ns); print(text)
    for n, text in res:
        print('-- note', n); print(text)
