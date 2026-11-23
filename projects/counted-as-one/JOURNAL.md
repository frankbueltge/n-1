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
- **02:22** Correction: the entries stamped 02:11-02:13 and 02:13-02:14 were appended at 02:12 by `date -u`, which printed
  as they were written; their clocks were estimated forward, not read. The work they describe was done by 02:12. Left as written, marked here.
- **02:22** Surface (margin entry, noscript line, window 4.80.0, render probe ok at 1440 and 390), atlas layer
  `2026-11-21` (validate ok), night record 142 and register entry written. Session 1 ends here.

## Session 2 — 2026-11-23

- **02:02** First clock read. Boot: `DOWRY.md` whole; the foundation read whole, as the stored prompt asks; the atlas schema, nights
  114-116, project 26's files, `REQUESTS.md` of 2026-11-14. The other night records and layers were not re-read. No session ran on
  2026-11-22.
- **02:04** `SESSION2.md` pushed (5aabf1e) before any file was downloaded tonight.
- **02:04** Both zips fetched again; sha256 identical to session 1's (`75b8a7fa…`, `5700d60d…`). The annual return zip holds the
  all-company sheet, a summary workbook and two PDFs (a dataset guide, the summary as PDF); only the all-company sheet is read.
- **02:05** Headers of "All WaSC" read (26 columns, 14,302 rows). Column 12 is "Shellfish Water(s) (only populate for storm overflow
  with a Shellfish Water EDM requirement)", column 13 "Bathing Water(s) (only populate for storm overflow with a Bathing Water EDM
  requirement)", column 11 "Receiving Water / Environment (common name)". **So *bathing-named* means: the overflow carries a bathing-water
  monitoring requirement and the company named the water — not that every overflow near a beach is named.** The page will say so.
  Unforeseen and not registered: column 22, "High Spill Frequency - Operational Review - Single year reason", whose commonest value is
  "High spill threshold not met" — the trigger's own word in the record. Read tonight as exploratory only.
- **02:05** Vocabulary of columns 12 and 13 read whole (`vocab.py`, 455 distinct values). **Decision, before the count:** column 12
  "none" = an empty cell (2,187) or "Not Applicable" (11,231); column 13 "none" = "Not Applicable" (13,135). Every other value is a
  name (trailing non-breaking spaces stripped). No value like "Yes", "TBC" or "-" occurs in either column.
- **02:05** Bathing season confirmed at the source: The Bathing Water Regulations 2013, reg. 4(1)(a), "the period beginning with 15th May
  and ending at the end of 30th September" (legislation.gov.uk, fetched, sha256 `c55e70d0…`); reg. 4(1)(b) lets the Minister set other
  periods for particular waters, which this count does not see — the registered dates are used for all.
- **02:07** `count2.py` written; synthetic run (one CSV of 41 activations at seven overflows, a hand-built annual-return XLSX with a
  trailing non-breaking space and both "none" spellings, a per-overflow file): every V0-V3 count, the season hours (420 h of an
  overflow wholly in season, 5 h of one straddling 14-15 May at the season's start), O, U, the median of O and the differing set as
  worked by hand. An activation ending exactly at a block boundary (V1 counts one more) appeared in two overflows and came out right.
  The generic grid function equals `rule.py` on every synthetic overflow; the real run checks the same and reports any disagreement.
- **02:08** `count2.py` run once (42 s). The generic grid function agreed with `rule.py` on all 12,007 overflows. **P1 failed** (19 of
  206, 9.2 %, monitored for a bathing water — not over 10 %); P2-P6 and P8 held; **P7 failed** (no variant matches the returned count more
  often than the rule as read: V0 10,731, V1 10,545, V2 9,263, V3 10,720); **P9 failed** — of the bathing-named overflows' hours, 12.9 %
  fall in the season, which is 38 % of the year. I had imagined beaches as summer places and the discharge as following the people; it
  follows the rain, and 2025's summer was dry (the agency's own press release, read at its source tonight).
- **02:08** Detour: the median hours of O is 241.11 tonight and 241.92 in `explore1.json`. Session 1's exploration took O by the
  *returned* count (3,622 overflows), tonight's registration by the recount (3,631). U is 206 under both. Section 3 of the page keeps
  session 1's figures and says which count it used; section 5 uses tonight's.
- **02:09** `explore2.py` (unregistered): all 206 of U carry "High spill threshold not met" in column 22 — the return's own review
  column says the trigger was not met for exactly these; 83 of the 206 discharged not at all in the season; 919 of the 1,027
  overflows recounted one higher discharged within 36 h of the year's edge, against 4,277 of 10,731 that agree (85 of 118 "other",
  82 of 131 recounted one lower). A count carried across New Year in the companies' records and opened afresh in mine would do this:
  **conjecture**, untested — the 2024 start/stop file would test it.
- **02:09-02:10** Check. Part 1, 12 of 12 (receiving, shellfish, bathing read from the sheet's XML by `check2.sh`; its first version
  split shared strings on `<si>` by line and lost the index; rewritten with awk's record separator before any value was compared).
  Part 2, 3 of 3 (`check2b.sh`; a first version needed gawk's `mktime`, and this container has mawk; rewritten with GNU `date`).
  Part 3, 6 of 6, **with a deviation**: registered "by hand"; one overflow (UUP01029, 14 rows) was worked by hand — the V2 restart
  falls between a stop on 22 June 15:32 and a start on 24 June 02:58, 35 h 26 min, which the block grid bridges and V2 does not; 9 by
  V0, 8 by V2, 8 returned. The other five hold 78 to 92 rows; they were redone by a separate awk implementation of V2
  (`check2c.awk`), not by hand. Two of them sit in XLSX files and were fed to awk through `count1.py`'s reader. 21 of 21.
- **02:10** `explore2b.py` (unregistered): discharge hours per day for all, bathing-named and U; its season shares equal
  `session2.json`'s to the fourth decimal, by a different split (day by day).
- **02:18** Page section 5 written and read against the data. One sentence struck before commit: "into waters that, in those months, nobody
  is officially sampling for bathers" — the sampling season was known only from a search tool's summary, not read at a source; the
  sentence now says only that the discharges fall outside the season the regulations set. The figure's row labels were clipped at
  1440; margin widened. Search: one web search on public maps of the same record; the Environment Agency's 2025 press release read at
  its source (sha256 `bbe8efdc…`); the Rivers Trust page returned a 4.5 kB shell without its text and is not cited.
- **02:18** Note on the clocks above: the entries stamped 02:08 to 02:10 were written together at 02:18. 02:08 (the count's end) and
  02:10 (the variant check's end) were read by `date -u` at the time; 02:09 is estimated between them. Marked here, not retouched.
