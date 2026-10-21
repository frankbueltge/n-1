"""Session 2's rules tried on invented sentences and an invented graph before the export is read. Run: python3 test_lib2.py"""

import numpy as np

import lib
import lib2

def test_address():
    A = lib2.address
    assert A("fra", "Je t'aime.") == lib2.T
    assert A("fra", "Je t’aime.") == lib2.T
    assert A("fra", "Va-t'en !") == lib2.T
    assert A("fra", "A-t-il mangé ?") == lib2.NONE
    assert A("fra", "Vous êtes là ?") == lib2.V
    assert A("fra", "Tu as vu votre mère ?") == lib2.MIXED
    assert A("fra", "Je tiens ta main.") == lib2.T
    assert A("fra", "Il est là.") == lib2.NONE
    assert A("rus", "Ты где?") == lib2.T
    assert A("rus", "Где твоё пальто?") == lib2.T
    assert A("rus", "Вы готовы?") == lib2.V
    assert A("rus", "Это ваша книга, а не твоя.") == lib2.MIXED
    assert A("rus", "Иди домой!") == lib2.NONE
    assert lib2.has_bridge_form("eng", "Are YOU sure?")
    assert not lib2.has_bridge_form("eng", "Youth is wasted.")
    assert lib2.has_bridge_form("epo", "Kie estas via domo?")
    assert not lib2.has_bridge_form("epo", "Vidu!")


def test_chains():
    # languages: 0 fra, 1 rus, 2 eng, 3 epo; ids 1..8
    lang = np.array([-1, 0, 1, 2, 0, 1, 3, 1, 2], dtype=np.int32)
    links = np.array([(1, 3), (3, 2), (3, 5), (1, 5),   # 1-3-2 chain; 1-3-5 not (1-5 direct)
                      (4, 6), (6, 7), (4, 8), (8, 7)],    # 4-6-7 and 4-8-7: one pair, two bridges
                     dtype=np.int64)
    g, _, _ = lib.build_graph(links, lang)
    A, B, C = lib2.chains_between(g, lang, 0, 1, np.array([1, 4], dtype=np.int64), block=1)
    got = sorted(zip(A.tolist(), B.tolist(), C.tolist()))
    assert got == [(1, 3, 2), (4, 6, 7), (4, 8, 7)], got
    d = lib2.disagreement(np.array([1, 1, 2, 0]), np.array([2, 1, 2, 1]))
    assert d["both_classified"] == 3 and d["disagree"] == 1 and d["TV"] == 1, d


if __name__ == "__main__":
    test_address(); test_chains(); print("ok")
