"""Rules tried on an invented graph before the export is read. Run: python3 test_lib.py"""

import random

import numpy as np

import lib

# ids 1..9; languages: 0 eng, 1 deu, 2 fra, 3 jpn
LANG = np.array([-1, 0, 1, 2, 3, 0, 1, 2, -1, 3], dtype=np.int32)
LINKS = np.array([
    (1, 2), (2, 1),      # eng-deu
    (2, 3), (3, 2),      # deu-fra  -> chain 1-2-3
    (2, 4),              # deu-jpn (one direction only; still a link) -> chain 1-2-4, chain 3-2-4
    (1, 4), (4, 1),      # eng-jpn: 1 and 4 are directly linked, so 1-2-4 is not a chain
    (1, 5),              # eng-eng: same language, kept out
    (5, 6), (6, 7),      # eng-deu, deu-fra -> chain 5-6-7
    (7, 7),              # self link
    (6, 8),              # 8 has no sentence
    (6, 9), (9, 1),      # deu-jpn, jpn-eng -> chains 5-6-9; 7-6-9; 6-9-1; 9-1-2? 9(jpn)-1(eng)-2(deu): chain unless 9-2 linked (no)
], dtype=np.int64)


def test():
    g, counts, pairs = lib.build_graph(LINKS, LANG)
    assert counts["undirected_links_same_language"] == 1, counts
    assert counts["link_rows_missing_or_unknown_end"] == 1, counts
    # direct cross-language pairs: 1-2, 2-3, 2-4, 1-4, 5-6, 6-7, 6-9, 1-9
    assert counts["direct_pairs"] == 8, counts
    n_ind, is_end = lib.count_indirect(g, LANG, budget=3)
    # enumerate by hand: chains (unordered ends)
    expect = set()
    for a in range(1, 10):
        for b in lib.nbrs(g, a).tolist():
            for c in lib.far_ends(g, LANG, a, b):
                expect.add(frozenset((a, c)))
    assert n_ind == len(expect), (n_ind, expect)
    # by hand: 1-3 (via 2), 3-4 (via 2), 5-7 (6), 5-9 (6), 7-9 (6), 6-1 (via 9), 9-2 (via 1), 3-1? already, 4-9 (via 1: 4 jpn, 1 eng, 9 jpn -> same lang, no)
    hand = {frozenset(p) for p in [(1, 3), (3, 4), (5, 7), (5, 9), (7, 9), (6, 1), (9, 2)]}
    assert expect == hand, expect ^ hand
    assert frozenset((1, 4)) not in expect  # linked directly
    assert is_end[1] and is_end[3] and not is_end[8]
    rng = random.Random(1)
    for a, b, c in lib.sample_chains(g, LANG, is_end, 50, rng):
        assert len({LANG[a], LANG[b], LANG[c]}) == 3
        assert c not in lib.nbrs(g, a).tolist()
    d = lib.sample_direct(pairs, 8, random.Random(2))
    assert len(set(d)) == 8
    print("ok", counts, n_ind)


if __name__ == "__main__":
    test()
