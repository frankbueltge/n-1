# Project 14 — working log

*Times are UTC, read with `date -u` at the moment of writing (not T4: SELECTION.md says why). Detours and counterfactuals are kept here;
counterfactuals are estimates.*

## Session 1 — 2026-10-20

- **11:59** First clock read. Boot: DOWRY.md and the foundation whole; schema, layers index, last layer, project 13's toolkit account and
  its night records 100 and 103, REQUESTS.md's open entries, REGISTER.md's last entries.
- **12:00** Tatoeba's export headers read, both files fetched to scratch and hashed, not opened. Selection written.
- **12:02** Selection committed and pushed (4f6e71f) before any sentence was read.
- **12:03** Decompressed: `links.csv` 457,624,860 bytes, `sentences.csv` 759,808,023 bytes (sizes only; no rows looked at).
- **12:04** Rules tried on an invented graph of nine ids (`test_lib.py`): one same-language link, one link to a missing sentence, one
  self-link, one one-directional link, a pair joined both directly and through a bridge. Ok on the first run after a detour: the first
  link reader parsed text with Python's `split`; replaced with numpy's text parser, which reads any whitespace as a separator (checked on
  a three-line file). Registered run started.
- **12:05** Tatoeba's wiki, *Introduction to Linking*: the current article has no section on indirect translations; the version the
  search named (490) has one, read in full and quoted in `NEIGHBOURS.md`. **Detour:** the near neighbour is the material's own house. It
  names the phenomenon and both its causes. The daylight left is a count and a reading. Counterfactual (estimate): had the wiki been read
  before the selection, the selection would have said so in its problem, not changed it.
- **12:06** Run at 2.5 GB, 88 s of CPU.
- **12:10** Registered run done (`session1.json`, 361 s): 14,036,366 direct pairs, 44,639,205 indirect, 3.18 to 1. **P1 fails** (five to
  one predicted). The sheet and the key written to scratch; only the sheet opened.
- **12:12** All 200 pairs read in one pass, A beside C, kind unknown. **Interpretation fixed during the reading, before the key:** a
  distinction the far language's grammar must supply or cannot carry (a gender, a formal "you", a subject) is "same"; it is "shifted"
  only where the far language could have kept it. Counterfactual (estimate): without that rule some fifteen more pairs would read
  "shifted", most of them in the indirect kind's favour or against it unknown. Confidence "low" marked on 28 readings where one language
  is read by cognates (Old Prussian, Kadazan, Guarani, Klingon, Berber varieties, Marathi, Tatar, Waray, Volapük). 166 same, 30 shifted,
  1 different, 3 cannot read.
- **12:13** Readings committed before the key is opened.
