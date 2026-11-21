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
- **02:08-02:10** Format read before the count, by headers and first rows only. **Definition changes, logged before the count:** (1) the
  times carry a zone — every header says GMT, ISO strings end in `Z`; four XLSX files store Excel serial days, read as GMT. My belief
  "no zone" was wrong; nothing else changes. (2) Activations lying wholly outside 2025 are counted as their own row ("outside_2025") and
  not used; those crossing a year's edge are clipped, as registered. (3) The annual return's sheet "All WaSC" holds one row per overflow
  with `Total Duration (hh:mm:ss) all spills prior to processing through 12-24h count method` and `Counted spills using 12-24h count
  method`: the comparison uses that count; the duration is compared too, exploratory, unregistered. (4) Thames's file has a sixth
  column, "Data Correction" (48 rows "Amended"): read and ignored. Southern Water's sheet holds 1,048,042 rows, 534 short of a
  spreadsheet's row limit — noted; whether its file was cut cannot be told from the file.
- **02:11** `count1.py` written; synthetic run (a CSV with a quoted comma in a name, a reversed and an empty time, a row in 2024, one
  crossing New Year; an XLSX with an Excel serial; a three-row annual return with one count deliberately wrong) — every count, hour,
  match and the 4.5-day sequence as worked by hand.
