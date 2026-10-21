"""Project 14, session 2: the rule check read (SESSION2.md). The 80 sentences of check_sheet.json read by this session, the language model
itself, in one pass, with the rule's class withheld: who does each sentence address, by reading, not by the word lists?
T: a familiar singular addressee only; V: a plural or polite addressee only; both; neither. Machine readings: estimates.
Writes check_readings.json. Committed before check_key.json is opened."""

import json

R = {
 1: ("neither", "'we' only"), 2: ("both", "'Вы вегетарианка?' polite; 'а ты?' familiar"), 3: ("T", "'rendez-vous' is a noun"),
 4: ("T", ""), 5: ("neither", ""), 6: ("T", ""), 7: ("both", "'tu' addressed, 'vous' a group"), 8: ("V", ""), 9: ("T", ""),
 10: ("V", ""), 11: ("both", "'vous' with 'tes'"), 12: ("neither", ""), 13: ("neither", ""), 14: ("neither", ""),
 15: ("both", ""), 16: ("neither", ""), 17: ("neither", ""), 18: ("V", ""), 19: ("both", ""), 20: ("T", ""),
 21: ("neither", ""), 22: ("both", ""), 23: ("T", "'rendez-vous' is a noun"), 24: ("both", ""), 25: ("V", ""), 26: ("both", ""),
 27: ("T", ""), 28: ("V", ""), 29: ("V", ""), 30: ("V", ""), 31: ("neither", ""), 32: ("both", "several sentences in one"),
 33: ("V", ""), 34: ("T", ""), 35: ("T", ""), 36: ("V", ""), 37: ("both", ""), 38: ("neither", ""), 39: ("neither", ""),
 40: ("T", "imperative and 'парень', no pronoun"), 41: ("T", ""), 42: ("neither", ""), 43: ("T", ""), 44: ("T", ""),
 45: ("T", ""), 46: ("V", ""), 47: ("neither", ""), 48: ("neither", ""), 49: ("V", ""), 50: ("V", ""), 51: ("V", ""),
 52: ("both", "'s'il vous plaît' answers a 'tu'"), 53: ("V", "'ton' is 'tone'"), 54: ("both", ""), 55: ("T", ""), 56: ("T", ""),
 57: ("T", ""), 58: ("V", ""), 59: ("T", ""), 60: ("T", ""), 61: ("both", ""), 62: ("both", ""), 63: ("T", ""),
 64: ("neither", ""), 65: ("V", ""), 66: ("T", ""), 67: ("T", ""), 68: ("V", ""), 69: ("both", "'ты' addressed, 'вы' a group"),
 70: ("T", ""), 71: ("neither", ""), 72: ("neither", ""), 73: ("V", ""), 74: ("V", ""), 75: ("both", ""), 76: ("V", ""),
 77: ("V", "'Ух ты' is an interjection"), 78: ("neither", ""), 79: ("V", "plural imperatives, no pronoun"), 80: ("V", ""),
}

if __name__ == "__main__":
    sheet = json.load(open("check_sheet.json"))
    assert sorted(R) == [r["n"] for r in sorted(sheet, key=lambda r: r["n"])]
    out = {"estimate": True, "reader": "this session (a language model), one pass, class withheld",
           "readings": [{"n": n, "reading": R[n][0], "note": R[n][1]} for n in sorted(R)]}
    json.dump(out, open("check_readings.json", "w"), indent=1, ensure_ascii=False)
