"""Project 14, session 2: the address rules of SESSION2.md, and the chains between two languages.

Address classes: 0 none, 1 T (familiar singular), 2 V (plural or polite), 3 mixed. Bridge forms: whether an English or Esperanto
sentence holds a second-person form that makes no T/V split."""

import re

import numpy as np

NONE, T, V, MIXED = 0, 1, 2, 3
WORD = re.compile(r"[^\W\d_]+'?")

ADDRESS = {
    "fra": ({"tu", "te", "t'", "toi", "ton", "ta", "tes"}, {"vous", "votre", "vos", "vôtre", "vôtres"}),
    "rus": ({"ты", "тебя", "тебе", "тобой", "тобою", "твой", "твоя", "твоё", "твое", "твои", "твоего", "твоей", "твоему", "твоим",
             "твоих", "твоими", "твою", "твоею"},
            {"вы", "вас", "вам", "вами", "ваш", "ваша", "ваше", "ваши", "вашего", "вашей", "вашему", "вашим", "ваших", "вашими", "вашу",
             "вашею"}),
}
BRIDGE_FORMS = {
    "eng": {"you", "your", "yours", "yourself", "yourselves"},
    "epo": {"vi", "vin", "via", "viaj", "vian", "viajn"},
}


def tokens(text):
    return WORD.findall(text.lower().replace("’", "'"))


def address(lang, text):
    t_set, v_set = ADDRESS[lang]
    toks = set(tokens(text))
    t, v = bool(toks & t_set), bool(toks & v_set)
    return MIXED if t and v else T if t else V if v else NONE


def has_bridge_form(lang, text):
    return bool(set(tokens(text)) & BRIDGE_FORMS[lang])


def chains_between(g, lang, la, lc, a_ids, block=20000):
    """Every chain A-B-C with lang A == la, lang C == lc, lang B neither, and no A-C link. Returns arrays (A, B, C)."""
    indptr, nbr = g
    outA, outB, outC = [], [], []
    for s in range(0, len(a_ids), block):
        A = a_ids[s:s + block]
        deg = indptr[A + 1] - indptr[A]
        A1 = np.repeat(A, deg)
        starts = np.repeat(indptr[A], deg)
        offs = np.arange(len(A1), dtype=np.int64) - np.repeat(np.cumsum(deg) - deg, deg)
        B1 = nbr[starts + offs]
        lb = lang[B1]
        keep = (lb != la) & (lb != lc)
        # direct A-C links of these A, to exclude
        direct = set((A1[lang[B1] == lc] * len(lang) + B1[lang[B1] == lc]).tolist())
        A1, B1 = A1[keep], B1[keep]
        dB = indptr[B1 + 1] - indptr[B1]
        A2 = np.repeat(A1, dB)
        B2 = np.repeat(B1, dB)
        starts = np.repeat(indptr[B1], dB)
        offs = np.arange(len(A2), dtype=np.int64) - np.repeat(np.cumsum(dB) - dB, dB)
        C2 = nbr[starts + offs]
        k = lang[C2] == lc
        A2, B2, C2 = A2[k], B2[k], C2[k]
        if direct:
            d = np.fromiter(direct, dtype=np.int64)
            k = ~np.isin(A2 * len(lang) + C2, d)
            A2, B2, C2 = A2[k], B2[k], C2[k]
        outA.append(A2); outB.append(B2); outC.append(C2)
    return np.concatenate(outA), np.concatenate(outB), np.concatenate(outC)


def disagreement(ca, cc):
    """ca, cc: address classes of paired ends. Returns counts and shares over pairs with both classified."""
    both = np.isin(ca, (T, V)) & np.isin(cc, (T, V))
    a, c = ca[both], cc[both]
    n = int(both.sum())
    out = {"n": int(len(ca)), "both_classified": n}
    if n == 0:
        return out
    tt = int(((a == T) & (c == T)).sum()); tv = int(((a == T) & (c == V)).sum())
    vt = int(((a == V) & (c == T)).sum()); vv = int(((a == V) & (c == V)).sum())
    ta, tc = (tt + tv) / n, (tt + vt) / n
    base = 1 - (ta * tc + (1 - ta) * (1 - tc))
    out.update({"TT": tt, "TV": tv, "VT": vt, "VV": vv, "disagree": tv + vt, "disagree_share": round((tv + vt) / n, 4),
                "T_share_fra": round(ta, 4), "T_share_rus": round(tc, 4), "independence_baseline": round(base, 4),
                "observed_over_baseline": round(((tv + vt) / n) / base, 4) if base else None})
    return out
