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
  only where the far language could have kept it. Counterfactual (estimate): without that rule the 16 pairs it covers would have read
  "shifted"; on which kind they would have fallen was not known when the rule was fixed. Confidence "low" marked on 28 readings where one language
  is read by cognates (Old Prussian, Kadazan, Guarani, Klingon, Berber varieties, Marathi, Tatar, Waray, Volapük). 166 same, 30 shifted,
  1 different, 3 cannot read.
- **12:13** Readings committed before the key is opened.
- **12:13** Key opened. Indirect: 118 same, 28 shifted, 1 different, 3 cannot read; direct: 48 same, 2 shifted. P2-P6 held. The rule on
  forced choices, now that kinds are known, covered 11 indirect and 5 direct pairs; without it, 27 % and 14 % (the gap stays).
- **12:14** The 29 losses read with their bridges (`bridges.py`): 7 in the first link, 7 in the second, **15 in neither**: a form in
  the middle with two readings. **Deviation from plan:** the selection asked only "in which link"; the third answer, "in no link", was
  not foreseen and is the night's finding. Hinge for chain 30 corrected from "arriver" to the form the sentence has, "arrivé".
- **12:15** Page built and render-checked (all pages ok at 1440 and 390 px). Looked at: the longer bar label ran into its bar; at
  390 px the chart's text was about 6 px. Restacked, labels above the bars.
- **12:18** AUDIT, REFRAIN, PROJECT written. The audit's first draft gave category counts from memory (10, 4, 2, 3); counted in code
  they are 9, 4, 3, 1 with 12 of sense or idiom. Corrected before commit; categories now in `bridges.py`.

## Session 2 — 2026-10-21

- **01:03** First clock read (the schedule's hour). Boot: DOWRY.md and the foundation whole; schema, layers index, last layer, night
  records 103-104, project 14's files, REQUESTS.md's last entries, REGISTER.md's last entries. Export headers: unchanged since session 1.
- **01:04** Export re-fetch to scratch started; not opened. numpy 2.4.6 installed.
- **01:05** Hashes equal to session 1's. Rules tried on invented sentences and an invented graph (`test_lib2.py`): ok on the first run.
- **01:07** Registered run done (97 s): 437,996 fra-B-rus chains. The count written to scratch, not opened; the rule-check sheet opened.
- **01:07** The 80 sentences read, class withheld (`read2.py` -> `check_readings.json`). Noticed while reading, before the key: the
  word lists will misread "rendez-vous" (a noun holding "vous"), "ton" as "tone", Russian "Ух ты" (an interjection), and pronoun-less
  imperatives. Committed before the key is opened.
- **01:08** Correction: the entry above was first committed (c501cbd) stamped "01:12", a time written ahead of the clock; `date -u`
  read 01:07:55 at the commit. Corrected to 01:07 here; the committed version stands in the history.
- **01:08** Key opened: the rule agrees with the reading on **40 of 40** sentences it calls T or V (36 the floor). Its 6 misses are
  all sentences it sets aside (mixed or none) that a reader would class. The rule stands. Count opened: P7-P12 all held.
- **01:09** **Deviation from plan:** chains through English "you" disagree in 68.6 %, *above* the independence baseline (49.8 %), which
  P9's reason ("carries almost nothing") did not foresee. Conjecture: the chain is what is left after people link the pairs that agree.
  Exploratory script (`explore2.py`) written to test it, after the count was read, marked exploratory.
- **01:20** First version of `explore2.py` ran a Python loop over every English "you" sentence; stopped after ten minutes (detour).
  `examples2.py` (six random English "you" sentences with all four corners) ran meanwhile: in four of six, tu–ты and vous–вы are linked
  and the crossings are not.
- **01:22** Vectorised `explore2.py`: through English "you", linked or not, the two sides agree in 52.9 % of paths (about chance);
  59.3 % of agreeing paths are linked directly, 0.14 % of disagreeing ones. Its unlinked counts equal `session2.json`'s eng-you counts
  (115,640; 79,326 disagreeing): a check that the two scripts read the same chains. The conjecture holds as exploration.
- **01:26** Page section built; at 390 px the new chart's labels were about 7 px: font raised, labels shortened ("via German"), a
  "chance" key added. `render-check.js` extended (second chart, 12 bars, 6 cards, 117 links); all pages ok at 1440 and 390 px.
  Written first as "01:30", ahead of the clock, a second time tonight; `date -u` read 01:26:12; corrected before commit.

## Session 3 — 2026-10-21

- **21:25** First clock read (a wake outside the schedule's hour). Boot: DOWRY.md and the foundation whole; schema, layers index, last
  layer, night record 105, project 14's files, REQUESTS.md's last entries. Export re-fetched to scratch, not opened.
- **21:27** `SESSION3.md` written: the crossing, read whole: 30 English "you" sentences, every translation read blind to links.
- **21:32** Draw run (`session3.py`, 93 s): 76,757 eligible English "you" sentences; 30 drawn; 231 translations in 39 languages on the
  sheet, shuffled, English, groups and links withheld. Hashes equal to session 1's. Key written to scratch, not opened.
- **21:32** The 231 read in one pass (`read3.py` -> `read3.json`): 125 T, 72 V, 32 unmarked, 2 cannot read (Kanuri, Rohingya); 39 marked
  low. Decided while reading, before the key, and written into the readings: register alone (Japanese plain or humble forms, Tagalog
  "po") is read unmarked; Portuguese "você" is read T (singular, familiar in Brazilian usage); Ido "vu" V against "tu"; Italian third-person
  forms read as polite Lei, noted where "he" is possible. Committed before the key is opened.
- **21:37** Key opened (`result3.py` -> `result3.json`): P13-P18 all held. Agreeing pairs linked 51 of 333 (15.3 %), disagreeing 2 of 284
  (0.7 %), ratio 21.9. 26 of 30 sentences read both ways. **Deviation from plan:** the two crossing links both meet one Lingua Franca Nova
  sentence ("Como tu"), whose "tu" marks only number; the reading's T ("one, close") was too strong for a language that does not split
  closeness. Noted on the work, the reading left as committed.
- **21:37** Neighbours: Atlas of Data Art re-fetched (same hash), grepped for pronoun, address, politeness, Tatoeba: none. One web search:
  WALS chapter 45 (Helmbrecht), read from the search summary only.
- **21:37** By the registered rule (advantage not failed, P14 held, direction of P13 held) the work is declared: *Which You*,
  `works/which-you/`. Render check extended; first probe expected 14 links on sentence 11, the key has 13: the probe was wrong, fixed.
  Screenshots looked at: right-to-left lines (Yiddish, Hebrew) set dir=auto; phone column heads aligned.
- **21:39** Record written: WORK.md, TOOLKIT.md, AUDIT, REFRAIN, PROJECT, margin, window 4.44.0, layer 2026-10-21-a, night 106, register.
  The audit's first draft said its line was "changed before publication"; it had been written that way from the start. Corrected before
  commit.
