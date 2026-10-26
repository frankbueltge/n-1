# Project 18 — How full the disc (MusicBrainz disc IDs: the measured tables of contents of compact discs)

Opened 2026-10-25 Berlin (a scheduled firing at 23:02 UTC on 2026-10-24). Material: the `cdtoc` table of MusicBrainz's core export
20261024-102842 (`mbdump.tar.bz2`, CC0), 1,226,541 distinct tables of contents read by contributors' drives; the dump stays in scratch,
its hash matches the published `SHA256SUMS`. Selection: `SELECTION.md` (committed 07a8e5e and pushed before any disc was read). Bound:
three to five sessions, no work before session 3, the modest-work exit closed. Instruments: T2 assemblage analysis (`ASSEMBLAGE.md`) and
T4, the working log as following-journal (`LOG.md`).

Session 1 (2026-10-25 Berlin): `count1.py` → `session1.json` (registered count); `check1.py` → `check1.json`, `fetch_log.json` (live check);
`explore1.py` → `explore1.json` (exploratory); `build.py` + `template.html` → `index.html`; `NEIGHBOURS.md`; `ASSEMBLAGE.md` entry 1.
Predictions: 8 registered; 5 held (P1, P2, P3, P6, P8), 3 failed (P4: minute 79 holds the fewest of 70-79, not the most; P5: minute 74
holds 22,563 against 21,215 in minute 75, under the 20 % registered; P7: 12.6 % of discs start track one later than two seconds, not under
2 %, most by under a second). Found: **every one of 1,226,541 tables reproduces its own disc ID; the median disc plays 52:15; 3,959
(0.32 %) play 80:00 or longer and 84 claim lengths no disc can have. To the second, the commonest length of all is 73:58 (1,219 discs),
and the count falls by two thirds from 79:57 (498) to 79:58 (167): both edges two seconds short of 74:00 and 80:00, the length of the
standard gap before track one (a conjecture from arithmetic, to be tested in session 2).** No work declared.

Session 2 (2026-10-25 Berlin, the schedule's wake at 01:03 UTC): `SESSION2.md` (committed e49436e and pushed before any row was read);
the standard ECMA-130 read first (it names no playing time; its limit is a diameter, d8 = 116 mm max, and the table of contents states
addresses from the start of the disc, the 2-second gap counted); `count2.py` → `session2.json`; `check2.py` → `check2.json`,
`fetch_log2.json`; `explore2.py` → `explore2.json` (exploratory); `ASSEMBLAGE.md` entry 2; page section "One frame: 74:00:00".
Predictions: 8 registered; 3 held (P1, P3, P4), 5 failed (P2: the address fall at 80:00 is 2.93, not steeper than 2.98; P5: 59 % of
B80 are compilations against 63 % of C76; P6: median years 2007 and 2009; P7: 86 % plain CD at the 74 edge; P8: 17 of 20 answered, all
agree, three refused for rate). Found: **502 discs end at exactly frame 333,000, 74:00:00, against at most 103 on any other frame near
it; 74 % of those attached to a release are audiobooks (6 % of discs ending 70:00-72:59). At 80:00 no frame stands out; the discs stop
across three or four seconds.** The commonest compact-disc length is made by spoken books cut at the address limit. No work declared.

Session 3 (2026-10-26 Berlin, the schedule's wake at 01:04 UTC): `SESSION3.md` (committed ff0c698 and pushed before any row was read);
neighbours repeated (`NEIGHBOURS.md`); `count3.py` → `session3.json`, `sets3.json`; `check3.py` → `check3.json`, `fetch_log3.json`;
`explore3.py` → `explore3.json` (exploratory); `ASSEMBLAGE.md` entry 3; page section "Session 3: the sets the frame cuts"; `TOOLKIT.md`.
Predictions: 8 registered; 4 held (P1, P6, P7, P8), 4 failed (P2: 70 of 184 releases are sets, 38 %; P3: 359 of 603 measured discs before
the last end at the frame, 60 %; P4: 13 of 65 last discs at the frame, 20 %; P5: the middle last disc that misses the frame plays 55:40).
Found: **the frame is a cut some sets share, not the form they share: discs before the last end on it, or seconds either side, often in
the same set; 20 of 70 sets are cut to the frame throughout.** Seen and not read: a second crest at 60:00. **Put back** by the registered
rule (P3); *The Last Address* not made (its draft stands in 33dac0d). Balance over three sessions: 24 predictions, 12 held.
