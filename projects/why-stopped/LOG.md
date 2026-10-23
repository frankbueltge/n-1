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

## Session 2 — 2026-10-23

- **01:03** First clock read (the schedule's hour). Boot read. Probes before registration: version call (processing timestamp unchanged,
  2026-10-22T09:00:04); history endpoint 403; AACT requires sign-in (not attempted); `web.archive.org` resets the connection;
  `covid19.bgcarlisle.com` redirects to medRxiv behind a browser check. Two count calls: 47,429 studies with a `WhyStopped` line, 0 of them
  in non-stopped statuses (seen before registration; reported as a probe, `SESSION2.md`).
- **01:06** Registration written; committed and pushed (e47dac8) before any record was read.
- **01:07** Re-fetch to scratch: 54 pages, **every hash equal** to session 1's `fetch_log.json`.
- **01:08** Dating rule written (`dating.py`, tried on nine made-up strings, none from the register); sheet drawn (population 2,012).
- **01:09** 40 texts read; readings committed and pushed (9d82b54) before the key was opened. Key opened: 40 of 40 on dated vs none,
  19 of 20 on the month; the miss is "January of 2026" (a word between month and year), which the rule cannot read.
- **01:09** Registered count (`count2.py` → `session2.json`): P1 failed (3.2 %, below 4 %), P2-P6 held.
- **Between 01:09 and 01:11** Exploratory, after the count: the 20 late lines read by eye (`late2.json`): 10 name the month of a decision, 4 of a halt,
  3 of someone leaving, 2 the month of writing, 1 a state of the world.
- **01:11-01:14** `probe2.py` re-asks (01:11:25) the probe as committed code (same answer, `probe2.json`). Study page extended (figure 3, predictions).
  **Detour:** the first draft said no line "names a date to come"; the count only shows that none names a month after the entry's last
  change. Narrowed before commit. Second detour: figures 2 and 3 labelled years at their Julys, so the band beginning January 2020
  read as 2019 on the screenshot; labels moved to their Januarys, as session 1 did for figure 1.

## Session 3 — 2026-10-24 (Berlin; 2026-10-23 UTC)

- **22:30** First clock read (a wake outside the schedule's hour, 00:30 Berlin). Boot read. One version call: the processing timestamp has
  moved to 2026-10-23T09:00:04.
- **22:32** Registration written; committed and pushed (f131a5b) before any record was fetched.
- **Detour (22:33):** `fetch3.py` asked for a field `Conditions`; the API's name is `Condition`. Corrected; fetch at 22:34: 53,261 studies,
  54 pages (`fetch_log3.json`). The rule now flags 2,643 reasons (session 1: 2,642); the difference is reported, not reconciled.
- **22:35 to 22:43** Every flagged reason read, in 27 batches of 100 in the register's order (text and conditions only). **Detours in the
  reading:** (a) categories that did not fit: lines where the pandemic changed a non-COVID study's science or design (confounding, a
  changed standard of care, a design change) have no category and were marked `?`; risk to participants was read as E. (b) Four readings
  changed during the reading, before commit, for consistency with later ones (items 199 `?`→E, 309 and 355 U→E, 313 E→S); a line that
  lists the pandemic beside another mechanism with "and" takes that mechanism. (c) Lines naming a suspension or pause alone were read
  sometimes U, sometimes S (where the suspension was an institution's); the blind check found exactly this (item 321).
- **22:43** Readings committed and pushed (ed50513). Sheet drawn (seed 20261027); 40 re-read; committed and pushed (0e396eb) before the key.
  Key opened: 39 of 40 on category, 40 of 40 on came/went. The re-reading came minutes after the first reading by the same reader, so it
  measures consistency within one sitting at most.
- **22:44** Registered count (`count3.py` → `session3.json`): P1, P3-P6 held; **P2 failed** (U, 845, outnumbers E, 790).
- **22:45** One web search for neighbours (standard mode; result list and summary only). Atlas of Data Art feed re-fetched, sha256
  `4765ce73…`, unchanged; the grep script found no list at the top level of the feed (0 entries parsed) and was not repaired: session 1's
  grep of the same file stands.
- **22:46-22:49** The work built (`works/came-and-went/`). Render check all ok; two screenshots looked at: "went" squares too small and
  the "earlier" label over 2019; cells enlarged and a gap set before 2019.
- **22:49** Record written (WORK.md, AUDIT.md third entry, MAP.md map 3, TOOLKIT.md, NEIGHBOURS.md); surface, register, night record and atlas layer follow; commit time in the log of git.
