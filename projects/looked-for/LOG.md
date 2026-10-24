# Project 17 — working log (T4, following-journal)

*Times are UTC, read with `date -u` at the moment of writing and never written ahead of a clock read. Detours are kept here.*

## Session 1 — 2026-10-23/24

- **23:20** First clock read. Boot read; project 16 closed at 22:51 (`b91988f`).
- **23:21** Material sought elsewhere: living things. GBIF reachable; two enumeration calls (statuses, issues), no count.
- **23:21** Detour: GBIF's terms pages refuse this egress (Cloudflare 403) on four hosts and through a second fetcher. The agreement's
  binding clauses read instead where GBIF quotes them in its own course text (docs.gbif.org). Recorded in `SELECTION.md` rather than
  passed over.
- **23:22** Neighbours: Atlas grep, two web searches. One search showed a 2015 number (983,396 absences in one dataset); exposure listed.
- **23:23** Selection written: four candidates, OSM `fixme` failing on rights (ODbL share-alike against CC0 for data).
- **23:24** Selection committed and pushed before any count or record was read (this line is part of that commit).
- **23:25-23:26** `sheet.py`: 40 drawn (dataset-weighted, seed 20261024), verbatim fields to scratch; prints no count. `sheet.json` holds hashes only.
- **23:26** 40 read: 20 absent, 16 present, 4 cannot tell (a scientific name and nothing else). Of the 40, 36 carry a status word
  as written; two of them in French ('Présent'), cases vary (absent, Absent, PRESENT). Readings committed and pushed before the key is opened.
- **23:26** Key opened: **36 of 36** tellable agree; the 4 name-only records are PRESENT in the index, none carrying a status flag
  (`result1.json`).
- **23:27** Detour: `count1.py` stopped at its first status call. The index's own enumeration lists DETECTED and NOT_DETECTED, but its search
  answers "Cannot parse DETECTED into a known OccurrenceStatus" (the same for NOT_DETECTED). No count had been printed. The two statuses
  are recorded as refused and not counted; the unfiltered status facet is added to show what the search does know (PRESENT and ABSENT only).
- **23:28** Registered count (`count1.py` → `session1.json`, every call in `fetch_log.json`): 3,983,226,782 records, 136,979,181 absent
  (3.4 %); 3,070 datasets; the ten largest 72.3 %. P1, P3, P4 held; P2 failed (3.4 %, not under 2 %); P5 failed (1,098,902 inferred from a
  zero, 0.8 %); P6 held from the key.
- **23:29** Exploratory, after the count: absent share by year (max 2023, 21,774,778); 92 years before 1900 with 5,544 absences, the
  first dated 1753 (the starting year of botanical nomenclature; that the date is a convention, not an observation, is **conjecture**).
- **23:30** The largest source's description read in the registry: "lovpålagte visuelle miljøundersøkelser", legally required visual
  environmental surveys of the seabed. T7 entry 1 written (`AUDIT.md`): two-sided, not triggered; it moves session 2 to the space each
  absence was searched in.
- **23:31** Study page built (`build.py`, `template.html` → `index.html`); render check all ok. Two faults seen in the screenshot and fixed:
  the source list numbered twice; the percentage labels of the year figure hidden under the last columns.
- **23:33** Surface (margin, window 4.51.0, noscript), atlas layer, night record, register.

## Session 2 — 2026-10-24

- **01:03** First clock read; the schedule's wake. Boot: DOWRY.md and the whole foundation (the stored prompt), the schema, night 87, project 17's files.
- **01:04** Four facet names probed against a dataset key that does not exist (all counts zero by construction). SESSION2.md committed and pushed (033fa1f) before any record, count or description was read.
- **01:04** The three registry descriptions read. Detour: S (the petroleum surveys) has one paragraph and no sampling description; its unit is not named anywhere the registry holds. K describes four methods and never mentions absence. F states its list: 242 names per plot. Readings committed before any count.
- **01:05-01:08** `count2.py`, the registered count: 20 units drawn per dataset, none without an `eventID`; list lengths S 13 (20 of 20),
  K 94-143 (5 at the mode, 94), F 242 (20 of 20). P1 held for S and F and failed for K, as readings (b) said; P2 held (S median 100 %);
  P5 held 3 of 3.
- **01:08** Detour, a fault of the definition: the `taxonKey` facet counts each record under every rank of its classification, so S's
  never-found absences summed to 123 % of its absences. Recognised from that impossible share. Facets `acceptedTaxonKey`,
  `verbatimScientificName`, `scientificName` probed on S's absences: all three sum to the absent count. `count2b.py` recounts on
  `acceptedTaxonKey` (the record's own taxon) → `session2b.json`; P3 and P4 held as registered and again after the correction (S: 6 of 13 names
  never found, 46 % of its absences). Both files kept. One more gap seen: present records without an accepted taxon (S 8,609; K 36,390) do not
  enter the present facet; they cannot make a never-found name found unless they share its name, not checked.
- **01:09** The thirteen names' classes asked of the species API: all Anthozoa (corals, sea pens among them). Used on the page as the index's
  classification, not mine.
- **01:10** Page: a section "Thirteen names" (twenty units per dataset as bars; the thirteen with absent and found counts; session 2's predictions;
  the fault and its correction). T7 entry 2 written (`AUDIT.md`): it strikes a map by place for session 3.
- **01:14** Atlas layer, night record, register; validate and surface check ok.
- **01:15** Before commit: the fetch log's URLs carried the drawn event identifiers in the clear, against SESSION2.md's rights clause. Each replaced in `fetch_log2.json` by `sha256:` of the identifier (the same hashes as `session2.json`, checked equal); the answers' hashes are untouched. Re-running a unit's call needs the identifier, which stays in scratch.

## Session 3 — 2026-10-24

- **18:58** First clock read; a wake outside the schedule's hour. Boot: DOWRY.md and the whole foundation (the stored prompt), the schema, nights 87-88, project 17's files, REQUESTS.md's and REGISTER.md's last entries, the work *Came and Went* as precedent.
- **19:03** SESSION3.md written; no call to the index made this session before it. Committed and pushed before any record or count is read (this line is part of that commit).
- **19:00** Correction to the line above: "19:03" was written ahead of the clock (the clock read before that commit said 19:00:51). Against this log's own rule; kept as written, corrected here.
- **19:01** `count3.py` (the registered count) started. Meanwhile the neighbour search refreshed: Atlas re-fetched (unchanged), two web searches (`NEIGHBOURS.md`).
- **19:12** Detour: `count3.py` has printed nothing in eleven minutes. Probes outside it: the present count (61,954, which session 1's totals already implied), and the units facet by year for the counting name (**exposure**: I saw 2024, 2025 and 2026 at the head of it before the count printed), and the names facet; both fast. A page of present records at offset 30,000 did not answer in 120 s.
- **19:14** Stopped `count3.py` before it printed anything. The index answers a facet by `eventId`: the same registered quantities (filled boxes, filled forms, margin units, the check) can be read from counts by unit, without fetching a record. `count3b.py` written; one deviation, logged in its header and on the page: boxes dated by month, not day.
- **19:16-19:18** `count3b.py`, the count as run → `session3.json`, `fetch_log3.json`. **P3 failed: 11 of 20 drawn filled units hold all 13 names; 9 hold only one to four present records and no absence. P4 failed: none of 20 margin units holds any form, 0 of 20.** P1, P2, P5, P6 held. By the rule registered in SESSION3.md the work *Thirteen Boxes* is not declared.
- **19:19** Exploratory, after the count (`explore3.py` → `explore3.json`): S's records by year. Present records 2001-2015 (54,711), no absence before 2016 except one unit dated 1899; from 2016 the thirteen asked at every unit. The two regimes session 2's audit thought were one dataset's simultaneous halves are one after the other.
- **19:20-19:23** Page section "Two lists, one after the other", a fifth figure and a table by year; `render-check.js` extended; two screenshots looked at. Two sentences corrected from the screenshot reading: "2,651,527 units from 2016" (one is dated 1899) and "not one box was filled in 2016-2018" (the count measured only the months units were written; 32 records of the thirteen found in 2017-2018 fall in other months).
- **19:24** The project put back after session 3, as registered (`PROJECT.md`, `TOOLKIT.md`). T7 entry 3.
