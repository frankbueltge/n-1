"""Session 1, after the key: where each indirect loss happened, read with the bridge (writes bridges.json). A machine reading: an estimate.

'first'  = the loss is already in A -> B; 'second' = in B -> C; 'chain' = both links can be read as faithful, and the bridge carries
an ambiguity (a word or form with two readings) that the far end resolves the other way."""
import collections, json

LOCUS = {
    5: ("chain", "French 'vous' is plural or formal; Italian takes formal singular", "vous"),
    9: ("chain", "English 'you' carries no formality; Italian takes formal feminine", "you"),
    16: ("second", "Spanish keeps the informal 'te'; Turkish makes it formal or plural ('this' already lost in the first link)", None),
    18: ("chain", "English 'fair' is reasonable or considerable; Bulgarian takes 'satisfactory'", "fair"),
    23: ("chain", "English 'you' carries no formality; Hungarian takes informal singular", "you"),
    27: ("second", "French 'au fond du trou' is literal or 'at rock bottom'; the Kabyle reading is low-confidence", None),
    30: ("chain", "French 'arriver' is to arrive and to happen; Dutch takes 'happen'", "arrivé"),
    47: ("first", "'too many' becomes 'one too many' in the English", None),
    48: ("chain", "English 'a number of' is several or many; Japanese takes 'many'", "a number of"),
    50: ("first", "'trying to get extradited' becomes 'request' in the German", None),
    56: ("chain", "Esperanto 'rigardis' carries no aspect; Russian takes the perfective", "rigardis"),
    61: ("first", "'forged the weapons of' becomes 'made arms for' in the Latin", None),
    66: ("first", "the Berber idiom becomes 'tortured their minds' in the French (low confidence)", None),
    84: ("chain", "English 'you' carries no formality; Ukrainian takes informal", "you"),
    102: ("second", "English 'boy' becomes Tagalog 'bata' (child)", None),
    107: ("chain", "English 'you' carries no formality; Russian takes formal or plural", "you"),
    116: ("chain", "English 'they' is singular or plural; Volapük takes plural", "they"),
    118: ("second", "Esperanto 'li' (him) becomes French 'sa connaissance' (his or hers)", None),
    121: ("second", "English 'want' becomes Volapük 'need' (low confidence)", None),
    122: ("chain", "English 'I will' leaves the verb out; Portuguese supplies 'go'", "I will"),
    123: ("second", "Japanese 'gakusha baka' becomes the literal 'learned fool'", None),
    125: ("second", "the German anthem line becomes a different poetic line in Tatar", None),
    127: ("chain", "Italian 'la' is 'her' or formal 'you'; English takes 'her'", "la"),
    151: ("chain", "English 'you' is singular or plural; Dutch takes plural", "you"),
    162: ("first", "'foreign languages' becomes 'how many languages' in the Japanese", None),
    183: ("chain", "Turkish carries no gender and leaves the number of beds open; Esperanto takes 'he' and one bed", "yatak toplamazdı"),
    187: ("first", "'got irritated' becomes 'became frustrated' in the English", None),
    198: ("chain", "Italian 'Lei' is 'she' or formal 'you'; English takes 'you'", "Lei"),
    200: ("first", "'straight up' becomes 'in one gulp' in the Spanish", None),
}

KIND = {**{n: "address (who is spoken to)" for n in (5, 9, 16, 23, 84, 107, 127, 151, 198)},
        **{n: "measure or number" for n in (18, 47, 48, 116)}, **{n: "gender" for n in (102, 118, 183)}, 56: "aspect",
        **{n: "sense or idiom" for n in (27, 30, 50, 61, 66, 121, 122, 123, 125, 162, 187, 200)}}

if __name__ == "__main__":
    key = {x["n"]: x for x in json.load(open("key.json"))}
    rd = {x["n"]: x for x in json.load(open("readings.json"))["readings"]}
    lost = [n for n in rd if key[n]["kind"] == "indirect" and rd[n]["reading"] in ("shifted", "different")]
    assert sorted(lost) == sorted(LOCUS), set(lost) ^ set(LOCUS)
    rows = [{"n": n, "locus": LOCUS[n][0], "how": LOCUS[n][1], "hinge": LOCUS[n][2], "what": KIND[n], "bridge_lang": key[n]["bridge"]["lang"]} for n in sorted(LOCUS)]
    assert sorted(KIND) == sorted(LOCUS)
    c = collections.Counter(r["locus"] for r in rows)
    print(collections.Counter(r["what"] for r in rows))
    json.dump({"estimate": True, "counts": c, "rows": rows}, open("bridges.json", "w"), ensure_ascii=False, indent=1)
    print(c)
