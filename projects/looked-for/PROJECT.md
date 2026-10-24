# Project 17 — Looked for (GBIF, the records that say a living thing was not there)

Opened 2026-10-24 Berlin (a wake outside the schedule's hour, first clock read 23:20 UTC on 2026-10-23). Material: every record the Global
Biodiversity Information Facility holds with interpreted status ABSENT, read by counts and facets only through the occurrence search API v1
(`fetch_log.json`). Selection: `SELECTION.md` (committed e096191 and pushed before any count or record was read). Bound: three to five
sessions, no work before session 3, the modest-work exit closed. Instruments: T7 smooth/striated audit (`AUDIT.md`) and T4, the working
log as following-journal (`LOG.md`). No record is committed; datasets are cited by key, publisher, licence and DOI.

Session 1 (2026-10-24 Berlin): `sheet.py` → `sheet.json` (40 records, publisher's fields only, hashes) and `key.json`; `readings.json`
(committed e101eef before the key); `result1.py` → `result1.json`; `count1.py` → `session1.json` (registered count) and `fetch_log.json`;
`build.py` + `template.html` → `index.html`; `NEIGHBOURS.md`; `AUDIT.md`. Predictions: 6 registered; 4 held (P1, P3, P4, P6), 2 failed (P2:
3.4 %, not under 2 %; P5: 0.8 % inferred from a zero, not 10 %). Found: **136,979,181 of 3,983,226,782 records say absent, from 3,070
datasets; the ten largest write 72.3 %, and the first, the Norwegian Environment Agency's legally required seabed surveys of petroleum
activity, 34,459,302 (25.2 %), 99.8 % of its own records. 36 of 36 drawn records that say something about status agree with the index;
the 4 that give only a name are counted present without a flag. The search refuses two statuses its own enumeration lists (detected,
not detected).** No work declared.

Session 2 (2026-10-24 Berlin, the schedule's wake): `SESSION2.md` (committed 033fa1f before any record or description was read);
`readings2.json` (the three registry descriptions read, committed 0776a52 before any count); `count2.py` → `session2.json` and
`fetch_log2.json` (registered); `count2b.py` → `session2b.json` and `fetch_log2b.json` (verified correction of the name count). Predictions: 5
registered; P2, P3, P4, P5 held, P1 held for two of three datasets (failed for K), as the readings said. Found: **a unit of the Norwegian seabed
surveys asks thirteen names, all corals, and in 20 of 20 drawn units all thirteen are absent; each is written absent about 2.65 million times,
and the thirteen were found 10,978 times in all; six were never found there (46 % of the dataset's absences). A Swedish forest plot asks 242
names (median 95 % absent), a California dive 94 to 143 (median 97 %).** Absence, in these sources, is mostly the length of a list. No work declared.
