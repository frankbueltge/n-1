# Project 16 — working log

*Times are UTC, read with `date -u` at the moment of writing and never written ahead of a clock read. Detours are kept here.*

## Session 1 — 2026-10-22

- **17:20** First clock read. Boot read; material chosen among four candidates (`SELECTION.md`); the registry's terms read whole; one
  count call (53,251) and the version call.
- **17:22** Neighbours searched (Atlas grep, two web searches).
- **17:23** Selection committed and pushed (51d4e55).
- **17:25** `fetch.py`: 54 pages, 53,251 studies, to scratch.
- **Detour (between 17:25 and 17:26):** `lib.py` found no stop month for any study: the field list had asked for the completion dates
  without their types, which the selection's "(+type)" required. While checking the parse, the script printed the overall number of
  reasons the rule flags, **2,642**: a headline value seen before the registered count was run, and before the check. P1 (at least
  4,000) was therefore known to fail before the count. Reported here and on the page; P1 is counted as failed, not as tested blind.
  The fetch was repeated with the two type fields (17:26).
- **17:27** Sheet drawn (8,055 eligible), 40 texts read, readings written (20 pandemic, 1 other, 19 not) and committed and pushed
  (0e2aebe) before the key was opened.
- **17:27** Key opened: 39 of 40 agree for the words, 38 for the event (`result1.json`). Item 24's end month (2020-02) precedes the
  date its reason gives (18 March 2020).
- **17:27** Registered count (`count1.py` → `session1.json`): P1 failed, P2-P5 held; P6 held from the key.
- **17:28** Exploratory, after the count: the 95 reasons on studies ending before 2020 read by eye, then sorted by rule (`anach.py` →
  `anach1.json`): 86 COVID-19, 8 an influenza pandemic, 1 a company's name (Covidien); across all flagged reasons the company's name
  alone is taken twice. The rule's weakness, recorded; the registered count is not revised.
- **17:30** Study page built (`build.py`, `template.html` → `index.html`). Detour: the first draft called all eight influenza reasons
  "the pandemic of 2009"; one (a 2008 vaccine trial) names pandemic vaccine candidates before 2009. Corrected before commit.
- **17:33** Year labels moved to their Januarys after the screenshot; render check all ok; atlas layer, night record, register written;
  `atlas/validate.py` and `surface/check.py` ok. Commit and push follow (17:34 at this line).
