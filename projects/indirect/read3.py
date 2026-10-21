"""Project 14, session 3: the sheet read (SESSION3.md). Every translation of sheet3.json read by this session, the language model itself,
in one pass, blind to the English sentence, to which sentence each belongs, and to every link: who does each address?
T: one addressee, familiar. V: polite, or several. both. unmarked: the form does not tell (register alone, without a second-person form,
is read unmarked). cannot: the reader cannot judge the language. Machine readings: estimates; "low" marks a reading made with little
confidence in the language. Writes read3.json. Committed before key3.json is opened."""

import json
import sys

LOW = "low"
R = {
 1: ("V", ""), 2: ("T", ""), 3: ("V", "imperative 'comptez', a proverb"), 4: ("V", "plural imperative and 'tzemrem'", LOW),
 5: ("V", "'fa': polite Lei, or 'he'"), 6: ("cannot", "Kanuri"), 7: ("V", "'uw'"), 8: ("V", "'fate'"), 9: ("T", ""), 10: ("T", ""),
 11: ("T", ""), 12: ("V", ""), 13: ("T", "'biliyorsun'"), 14: ("V", "'tettarumt': plural feminine", LOW), 15: ("T", ""), 16: ("T", ""),
 17: ("V", "'misiniz'"), 18: ("T", ""), 19: ("T", ""), 20: ("T", "'contes'"), 21: ("T", ""), 22: ("unmarked", "'man': generic"),
 23: ("V", "'ձեզ'"), 24: ("T", "'tua'"), 25: ("unmarked", "a proverb, plain prohibitive"), 26: ("V", "'Sizi'"), 27: ("V", "'avete'"),
 28: ("V", "'riuscite'"), 29: ("T", "'je'"), 30: ("T", "'txeddmeḍ'", LOW), 31: ("V", ""), 32: ("T", "'tua'"), 33: ("V", "'Sie' mid-sentence"),
 34: ("T", ""), 35: ("T", ""), 36: ("T", "'jij'"), 37: ("T", ""), 38: ("T", ""), 39: ("T", "'senin'"), 40: ("T", "'ту'", LOW),
 41: ("V", "'jullie'"), 42: ("V", ""), 43: ("T", ""), 44: ("V", ""), 45: ("T", ""), 46: ("T", "'Tzemreḍ'", LOW),
 47: ("V", "'sua': polite Lei, or his/her"), 48: ("V", "'Ustedes'"), 49: ("V", ""), 50: ("T", "'deine'"), 51: ("V", "'ha': polite Lei"),
 52: ("V", "'ihr'"), 53: ("T", "'tuoi'"), 54: ("V", ""), 55: ("T", "'edersin'"), 56: ("T", "'bacağın'"), 57: ("T", "'je'"),
 58: ("V", "'tettarum': plural", LOW), 59: ("unmarked", "plain form, no pronoun"), 60: ("T", ""), 61: ("V", ""), 62: ("T", ""),
 63: ("V", "'jūsu'", LOW), 64: ("V", "'ihr'"), 65: ("T", "'tzemred'", LOW), 66: ("V", "'tzemrem'", LOW), 67: ("cannot", "Rohingya"),
 68: ("unmarked", ""), 69: ("T", "'tavas'", LOW), 70: ("T", "'você': singular, familiar in Brazilian usage"), 71: ("V", "'Ihre'"),
 72: ("T", ""), 73: ("T", ""), 74: ("T", ""), 75: ("V", "'Duermen': ustedes, or 'they'"), 76: ("T", "'דו'"), 77: ("V", "'veros': vosotros"),
 78: ("T", "'lábadat'"), 79: ("unmarked", "'I'm not joking': no 'you'"), 80: ("T", "'tettarud'", LOW), 81: ("unmarked", "'po' is polite register; no 'you'"),
 82: ("unmarked", "generic"), 83: ("V", "'tettarum'", LOW), 84: ("T", ""), 85: ("T", "'musun'"), 86: ("T", "'Ti'"), 87: ("V", "'Sie'"),
 88: ("T", ""), 89: ("T", "'tuas'"), 90: ("unmarked", "a proverb, impersonal"), 91: ("V", ""), 92: ("V", ""), 93: ("T", ""), 94: ("T", ""),
 95: ("unmarked", "'po' is polite register; no 'you'"), 96: ("T", ""), 97: ("T", "'νομίζεις'"), 98: ("T", "Ido 'tu', the familiar", LOW),
 99: ("unmarked", "3sg verb: você or o senhor"), 100: ("T", "'tettarud'", LOW), 101: ("T", ""), 102: ("T", "'Te', 'tudod'"),
 103: ("T", "'maka'", LOW), 104: ("V", "'votre'"), 105: ("T", "'nnem': singular feminine", LOW), 106: ("V", ""), 107: ("unmarked", "generic"),
 108: ("T", "'uyursun'"), 109: ("V", "'uw'"), 110: ("V", "'txeddmem'", LOW), 111: ("V", "plural feminine", LOW),
 112: ("unmarked", "'sina': one or several"), 113: ("T", ""), 114: ("T", "singular imperative"), 115: ("T", "'riesci'"), 116: ("V", ""),
 117: ("unmarked", "polite register, no pronoun"), 118: ("T", "'tu'", LOW), 119: ("T", "'tzemred'", LOW), 120: ("unmarked", "generic"),
 121: ("V", "'tettarumt'", LOW), 122: ("T", "'-ku-': you, singular", LOW), 123: ("V", "'আপুনি': polite", LOW), 124: ("V", "'vám'"),
 125: ("unmarked", "a proverb"), 126: ("T", "'ihtiyacın'"), 127: ("T", "'քեզ'"), 128: ("V", "'Potreste'"),
 129: ("unmarked", "'değiştiremeyeceğini': yours or his"), 130: ("V", "'riesce': polite Lei, or 'he'"), 131: ("V", "'איר'"), 132: ("T", ""),
 133: ("V", "'Sie'"), 134: ("V", ""), 135: ("T", "'Te'"), 136: ("unmarked", "'a person': generic", LOW), 137: ("unmarked", "a proverb"),
 138: ("T", "'fai'"), 139: ("V", ""), 140: ("T", "'Yazdığın'"), 141: ("T", "'senin'"), 142: ("T", ""), 143: ("T", ""), 144: ("V", "'Sie'"),
 145: ("unmarked", "generic"), 146: ("T", ""), 147: ("T", "'tu'", LOW), 148: ("T", "'piszesz'"), 149: ("T", "'Sence'"),
 150: ("unmarked", "humble register, no pronoun"), 151: ("V", "'Potrebbe': Lei"), 152: ("T", ""), 153: ("V", "'orik' read as the polite 'your'", LOW),
 154: ("T", "singular imperative, a proverb"), 155: ("T", ""), 156: ("T", "'לך': singular"), 157: ("V", "'alın': plural imperative"),
 158: ("unmarked", "'sina': one or several"), 159: ("T", ""), 160: ("unmarked", "'po' is polite register; no 'you'"), 161: ("V", "'Le'"),
 162: ("T", ""), 163: ("T", "'doe'", LOW), 164: ("T", "'tua'"), 165: ("T", "'sinulle'"), 166: ("T", "'te'"), 167: ("V", "'txeddmemt'", LOW),
 168: ("T", "'u-': you, singular", LOW), 169: ("T", ""), 170: ("V", ""), 171: ("unmarked", "plain form, no pronoun"), 172: ("V", "Ido 'vu', the ordinary singular against 'tu'", LOW),
 173: ("T", "'te'"), 174: ("T", "'-si'"), 175: ("V", "Ido 'vua'", LOW), 176: ("T", ""), 177: ("unmarked", "'I'm not joking': no 'you'", LOW),
 178: ("V", ""), 179: ("T", ""), 180: ("T", "'Potresti'"), 181: ("T", "'sana'"), 182: ("T", "'widzisz'"), 183: ("unmarked", "'I'm not joking': no 'you'"),
 184: ("T", "'misin'"), 185: ("T", "'Você'"), 186: ("T", ""), 187: ("unmarked", "a proverb"), 188: ("T", ""), 189: ("V", ""),
 190: ("unmarked", "a proverb"), 191: ("T", ""), 192: ("T", ""), 193: ("T", "'hai'"), 194: ("T", "'tu'", LOW),
 195: ("unmarked", "'what I meant': no 'you'"), 196: ("T", "'você'"), 197: ("V", ""), 198: ("V", "'Vi'"), 199: ("T", ""), 200: ("T", "'Duermes'"),
 201: ("V", ""), 202: ("T", "'ти'"), 203: ("V", ""), 204: ("T", ""), 205: ("T", "'Ağrına'"), 206: ("unmarked", "'man': generic"),
 207: ("V", "'ihr'"), 208: ("unmarked", "'I'm not joking': no 'you'"), 209: ("T", "'nnek'", LOW), 210: ("V", ""), 211: ("T", ""),
 212: ("T", ""), 213: ("T", ""), 214: ("T", ""), 215: ("V", ""), 216: ("T", ""), 217: ("V", "'Ihren'"), 218: ("T", "'Ti'"),
 219: ("unmarked", "infinitive, a proverb", LOW), 220: ("T", "'по-твоему'"), 221: ("V", "'あなた' with a humble verb"), 222: ("T", "'sua': você"),
 223: ("T", ""), 224: ("T", "'你', not '您'"), 225: ("T", ""), 226: ("T", "'k-'", LOW), 227: ("V", "plural feminine", LOW),
 228: ("unmarked", "generic"), 229: ("T", "'-ካ': you, singular", LOW), 230: ("T", "'ти'"), 231: ("T", "'-lIj': your, singular", LOW),
}

if __name__ == "__main__":
    sheet = json.load(open(sys.argv[1]))
    assert sorted(R) == [r["n"] for r in sheet], "every row read once"
    rows = []
    for n in sorted(R):
        r = R[n]
        rows.append({"n": n, "reading": r[0], "note": r[1], "confidence": r[2] if len(r) > 2 else "ordinary"})
    out = {"estimate": True, "reader": "this session (a language model), one pass, blind to the English sentence, the groups and the links",
           "readings": rows}
    json.dump(out, open("read3.json", "w"), indent=0, ensure_ascii=False)
    import collections
    print(collections.Counter(r["reading"] for r in rows), sum(r["confidence"] == LOW for r in rows))
