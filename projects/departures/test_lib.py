"""Rules tried on invented games before any real game is read."""
from lib import departures, position_departures, san_tokens, parse_pgn


def test_departures():
    g = [["e4", "e5", "Nf3"], ["e4", "e5", "Nc3"], ["e4", "c5"], ["e4", "e5"], ["d4"], ["d4"]]
    d = departures(g)
    assert d[0] == (3, 2) and d[1] == (3, 2)
    assert d[2] == (2, 1)
    assert d[3] == (None, 2)       # a prefix of games 0 and 1: never departs
    assert d[4] == (None, 1) and d[5] == (None, 1)  # identical: never departs
    assert departures([["a"]]) == [(1, 0)]  # alone from the first ply


def test_positions():
    # game 0 and 1 transpose: different order, same position at ply 3
    keys = [[1, 2, 9, 4], [1, 3, 9, 5], [1, 2, 6]]
    p = position_departures(keys)
    assert p == [4, 2, 3]


def test_tokens():
    t = san_tokens("1. e4 e5 2. Nf3?! {a comment} Nc6 3... Bb5 $1 1-0")
    assert t == ["e4", "e5", "Nf3", "Nc6", "Bb5"], t
    t = san_tokens("1.e4 1-0")
    assert t == ["e4"], t
    games = list(parse_pgn(['[Event "x"]\n', '[WhiteElo "1500"]\n', '\n', '1. e4 e5 1-0\n', '\n', '[Event "y"]\n', '\n', '1. d4 0-1\n']))
    assert len(games) == 2 and games[0][0]["WhiteElo"] == "1500" and san_tokens(games[1][1]) == ["d4"]


if __name__ == "__main__":
    test_departures(); test_positions(); test_tokens(); print("ok")
