# Project 26 — journal (T4 following-journal)

*Clocks from `date -u` at the moment of writing, except where an entry says it was written later. Entries are not written ahead.*

## Session 1 — 2026-11-21

- **02:03** First clock read. Boot: `DOWRY.md` whole; the foundation read whole, as the stored prompt asks; the atlas schema, the last
  layer, night 115 and nights 110-114's accounts, project 25's files, `REQUESTS.md` of 2026-10-02 and 2026-11-14. The other 140 night
  records and 143 layers were not re-read: the stored prompt asks for them, and twenty-two thousand words of foundation plus 136,000 of
  nights do not fit one session's attention with work in it. Said here, not hidden.
- **02:03-02:05** Exposure before selection (listed in `SELECTION.md`): two catalogue entries, the assessment framework's counting rule
  and triggers, the Atlas of Data Art. The material came from looking for a record whose number decides an act on something living; the
  12/24 rule was found in the framework's Appendix A, verbatim.
- **02:05** `SELECTION.md` pushed (c374b2a) before any storm-overflow file was downloaded.
- **02:06** `rule.py` written; nine synthetic cases worked by hand (one long discharge of 100 h = 5 counted spills holding 12, 24, 24,
  24, 16 h; an activation ending exactly where block 1 begins does not touch it) — 9 of 9 and the hours. Pushed (49f5c5e).
- **02:07** Both zips downloaded (sha256: start/stop 2025 `75b8a7fa25970812a6287c26e010200da4373b55383c98d2344dfa33188bc001`, annual
  return 2025 `5700d60d92445e22ea782a2ac5c872de19d05cb875763625e3ebe2bd8914fa34`). Ten start/stop files, one per company: five CSV,
  five XLSX. Detour: installing a spreadsheet library with pip was refused by this container's permission layer; a stdlib reader
  (`xlsx.py`) was written instead.
- **02:07-02:08** Format read before the count, by headers and first rows only. **Definition changes, logged before the count:** (1) the
  times carry a zone — every header says GMT, ISO strings end in `Z`; four XLSX files store Excel serial days, read as GMT. My belief
  "no zone" was wrong; nothing else changes. (2) Activations lying wholly outside 2025 are counted as their own row ("outside_2025") and
  not used; those crossing a year's edge are clipped, as registered. (3) The annual return's sheet "All WaSC" holds one row per overflow
  with `Total Duration (hh:mm:ss) all spills prior to processing through 12-24h count method` and `Counted spills using 12-24h count
  method`: the comparison uses that count; the duration is compared too, exploratory, unregistered. (4) Thames's file has a sixth
  column, "Data Correction" (48 rows "Amended"): read and ignored. Southern Water's sheet holds 1,048,042 rows, 534 short of a
  spreadsheet's row limit — noted; whether its file was cut cannot be told from the file.
- **02:08-02:09** `count1.py` written; synthetic run (a CSV with a quoted comma in a name, a reversed and an empty time, a row in 2024, one
  crossing New Year; an XLSX with an Excel serial; a three-row annual return with one count deliberately wrong) — every count, hour,
  match and the 4.5-day sequence as worked by hand.
- **02:09** Correction: the two entries above first carried clocks 02:08-02:10 and 02:11, written without a read; `date -u` said 02:09
  when they were committed (b1253b5). Corrected here; the commit keeps the wrong ones.
- **02:10** `count1.py` run once (34 s). 2,115,874 rows; 12,007 overflows with activations; 1,120,341 activations; 293,036 counted
  spills. P1, P2, P4, P5, P6, P7, P8, P10 held; **P3 failed** (22.2 % of counted spills hold 12 hours or more, not under 10 % — I had
  imagined the long count as rare; a discharge lasting days is counted once a day, and every one of those days is a 12-hour-plus spill);
  **P9 failed** (47.1 % of rows "malformed").
- **02:10** Detour, on P9. 995,359 of the 995,533 "malformed" rows are blank: Southern Water's sheet ends its data at row 52,684 and
  carries formatted empty rows to row 1,048,043. They are not records. On non-blank rows 174 of 1,120,515 are malformed (0.016 %: 173
  Welsh Water rows with a site name and no identifier, one United Utilities row). P9 stays failed as registered — the measure was mine and
  it counted what it counted; the non-blank figure is exploratory and the page says both. The worry of 02:08, that Southern's file was
  cut at a row limit, is answered: the data stops 995,359 rows before the limit.
- **02:11-02:13** `explore1.py` (unregistered): recounted hours agree with the companies' returned durations within 0.1 h for 11,962 of
  12,007 overflows; the recount equals the returned count for 10,731 (89.4 %), is higher for 1,127, lower for 149 (most by one). **The
  turn:** at the trigger of 30 counted spills, the count does not order the hours. Overflow SBB01164 discharged 1 h 16 min in 2025, in
  226 activations, and is counted 44 spills — over the trigger; SBB01318 discharged 567 h in 14 activations and is counted 27 — under
  it. 206 overflows under the trigger discharged longer than the median overflow over it (242 h). At SBB01043 one sequence runs from 1
  January to 12 August, 224 counted spills; the overflow's year holds 21 activations, 5,446 hours, 235 counted spills. (This line first
  conflated the sequence with the year; corrected at 02:15 when the page sentence built from it was read against `session1.json`.)
- **02:13-02:14** Check: 13 of 13 by `check1.awk` (the rule written again in awk, sharing no code); rows per file by `wc -l` agree for
  all ten; the five CSVs also by `wc -l` on the raw files. SBB01164 and SBB01318 redone from the raw CSV with `grep`, GNU `date` and the
  awk rule: 44 / 1.2644 h and 27 / 567.3056 h.
