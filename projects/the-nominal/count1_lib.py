"""Shared arithmetic of count1.py (pitch class, deviation in cents), imported by check1.py."""
import math

LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
ACC = {'♯': 1, '♭': -1, '𝄪': 2, '𝄫': -2, '#': 1, 'b': -1}

def pc(note):
    if not note or note[0] not in LET:
        return None
    p = LET[note[0]]
    for ch in note[1:]:
        if ch not in ACC:
            return None
        p += ACC[ch]
    return p % 12

def dev(f, p):
    c = 1200 * math.log2(f / 440) + 900
    return ((c - 100 * p + 600) % 1200) - 600

