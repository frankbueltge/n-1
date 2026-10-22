"""Project 15, session 2: the standing pairs of the file, joined to the pages. The name mapping is written as mismatches are met."""
import lib, pages2

# file name -> page name; met on 2026-10-22, session 2
NAMES = {'Bahamas': 'Bahamas (The)', 'Netherlands': 'Netherlands (Kingdom of the)', 'Turkey': 'Türkiye'}
# no entry of their own on any page (their holding back stands under China's entry); left unmatched, counted
UNMATCHED = {'China, Hong Kong Special Administrative Region', 'China, Macao Special Administrative Region'}


def standing_pairs():
    df, _ = lib.load()
    st = df[df['held'] & (df['withdrawal'] != 1)]
    return sorted(st.groupby(['country', 'treaty']).size().index)


def flags():
    """(country, treaty) -> list of (year, sentence) late-withdrawal sentences, or None if unmatched."""
    pages = {t: pages2.parse(t) for t in pages2.NO}
    out = {}
    for c, t in standing_pairs():
        if c in UNMATCHED:
            out[(c, t)] = None
            continue
        name = NAMES.get(c, c)
        parts, entries, notes = pages[t]
        if name not in parts and name not in entries:
            out[(c, t)] = None
            continue
        sents = []
        for _, text in pages2.footnotes(name, parts, entries, notes):
            sents += pages2.late_sentences(text)
        out[(c, t)] = sents
    return out
