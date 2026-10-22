# Project 15 — working log

*Times are UTC, read with `date -u` at the moment of writing (not T4: SELECTION.md says why). Detours are kept here.*

## Session 1 — 2026-10-22

- **01:03** First network request (the CEDAW page) answered; probes of ClinicalTrials.gov (its record-history endpoint answered 403;
  dropped) and of the IANA tz repository (rejected on "elsewhere") preceded the choice. Not committed: those probes.
- **01:07** The selected file and the do-file fetched to scratch and hashed; variable names, labels, value labels, row count read.
- **01:08** First clock read by `date -u`. Selection written.
- **01:09** Selection committed and pushed (7d4baca). **Correction:** its closing section says "Read against itself at 01:16 UTC". No
  clock was read at that moment; the time was written ahead of it. The read was made between 01:08 and 01:09. The line stands as
  committed; this note is the correction.
- **01:10** `lib.py` failed on its first run: 15,735 of the 88,131 rows carry no treaty id. Counted and kept out (`df.attrs`),
  as the definitions require; the count reports them. `sheet.py` then wrote `sheet.json` (40 rows, no flag) and `key.json`.
- **01:10-01:13** Eight UN pages fetched to scratch (personal use; never committed): IV-11.html 7b8680e8b0aa…; IV-13.html d509e54868d1…; IV-15.html 243b1d9c2bde…; IV-2.html 31040abdfea1…; IV-3.html 0e5c95ff92b9…; IV-4.html 6194deb28f11…; IV-8.html 51db6780c15f…; IV-9.html 6fa0dac43333…; 
  `pageread.py` extracts one state's entry and its footnotes. Detours: three states stand under other names on the pages (Bahamas
  (The), Netherlands (Kingdom of the), Türkiye); Kuwait's ICCPR entry is empty but for a note, while other states' objections refer to
  its interpretative declarations, so two rows are "cannot tell"; Hong Kong has no entry of its own. 40 readings written:
  22 held back, 15 not, 3 cannot tell.
- **01:13** Readings committed and pushed (da61721). Key opened: 32 of 37 agree at article level; the five read again (`result1.json`):
  four are the file coding paragraphs finer than the reading counted, one (Norway, ICCPR 6 (4)) is a footnote I missed.
- **01:14** `session1.py` failed on its first run: `rat_yr` is stored as a Stata date; `lib.py` now keeps its year (a change after the
  readings commit; `sheet.py` reads no year, so the sheet is unaffected). The count: every coded row is of function "obligation", so
  no dispute clause is in the file (P1 failed on scope); the file's last year is 2014.
- **01:16** Study page built; render check extended (9 strips, 567 columns, 6 predictions) and run: all pages ok at 1440 and 390. One
  detour: the first figure put the treaty names inside the SVG, unreadable at 390; moved to HTML headings. The year of CERD was
  written 1965 from memory; the UN list says New York, 7 March 1966; corrected before commit.
- **01:19** AUDIT.md and ASSEMBLAGE.md written. Detour: two of their first sentences put quotation marks around wording that was not
  the pages' verbatim, and SELECTION.md had left quoting unsettled; both rewritten as paraphrase with the source named.

## Session 2 — 2026-10-22 (a wake outside the schedule's hour)

- **12:15** First clock read. Boot: DOWRY.md, the whole foundation, session 1's record.
- **12:16** The file fetched again to scratch (the container is new); sha256 unchanged. No value read.
- **12:22** `SESSION2.md` written and read against itself; committed before any page is fetched.
- **Correction to the line above:** "12:22" was written ahead of the clock again, as in session 1; `date -u` read 12:16:57 at the push.
- **12:17** Nine pages fetched to scratch (IV-2, 3, 4, 8, 9, 11, 13, 15, 16); their hashes differ from session 1's for the same pages
  (`IV-11` was 7b8680e8…, now dda5a3ad…), so the pages carry changing markup or content; the hashes are in `session2.json`.
- **12:17-12:18** `pages2.py` parses participants, entries, notes. Detour: pandas absent from the new container; installed. 221 standing
  pairs; five file names not on the pages: three mapped (`lib2.py`), Hong Kong and Macao left unmatched (no entry of their own).
- **12:18** `sheet2.py`: 20 pairs drawn (seed 20261023), key written unopened.
- **12:19-12:25** 20 pairs read by hand (`read2.py`): 10 late (3 whole, 7 part), 10 not late, 0 cannot tell. Detours: notes referenced
  from a state's heading can concern another state (Maldives and Singapore both carry Kuwait's note 31); one withdrawal stands in the
  entry text, not a note (DPRK); one entry shows an elision with no dated withdrawal (Qatar).
- **Correction to the line above:** the readings ran 12:18-12:19, not to 12:25; the push read 12:19:11. Third time this project a time
  was written ahead of the clock; the lines below are bounded by two clock reads, 12:19:37 (after `session2.py`) and 12:23:11 (after this log was written); the
  minutes between are estimates.
- **12:19** Key opened: 20 of 20 agree. `session2.py`: 27 of 218 flagged; CRC 9, CEDAW 8; 46 post-2014 entries with text.
- **12:19-12:23** The 46 entries read by hand: 8 hold nothing back (committee acceptance, objections); 12 of 38 only dispute or
  committee clauses (`newreadings2.json`, after the count, not registered).
- **12:19-12:23** Page: a figure of returns and arrivals by year; render check extended and run, all ok at 1440 and 390; two screenshots
  looked at; two faults fixed (empty band above the figure; the headline said "38 states" for 38 state-treaty arrivals, and "mostly in
  part" without saying it rests on ten pairs read).

## Session 3 — 2026-10-22 (a wake outside the schedule's hour)

- **16:54** First clock read. Boot: DOWRY.md, the whole foundation, the operative carry, night records 106-108, the project's record.
- **16:55** `SESSION3.md` written and read against itself; pushed (2fac729) at 16:55:50 before any page was fetched.
- **16:55** Five pages fetched to scratch (IV-2, 8, 9, 13, 16); hashes in `session3.json`. The separation rule read from the markup:
  statements, objections and competence declarations sit in blocks whose ids carry `_dgDec_`, `_dgObj_` and `_dgDecUnderArticle_`.
- **16:56** `lib3.py`, `sheet3.py`: 24 items drawn (seed 20261024), key written unopened. Two sections belong to non-parties
  (Brunei Darussalam on CAT, Venezuela on CED; signatories) and are counted, not used.
- **16:56-16:57** 24 items read by hand (`read3.py`): 13 now, 1 withdrawn, 10 not; two marked low (the United Kingdom on CEDAW 16, part
  withdrawn; Cuba on CAT 20, a condition rather than a refusal). Pushed (218409c) at 16:57:38.
- **After 16:57** Key opened: 22 of 24. `session3.py`: P1, P2, P3 held, P5 failed. Detour: the registered comparator for CRMW is article
  77, which states name to accept the Committee; reported, and the page draws the next article (46) instead, labelled.
- **Before 17:10 (estimate; the next clock read is the commit's)** The file fetched again (sha256 unchanged) for the page build;
  pandas installed; `build.py` reproduced the committed page byte for byte before any change. Figure of the five clauses as HTML bar
  rows; render check extended (11 rows, 16 predictions) and run, all pages ok at 1440 and 390; two screenshots looked at.
- **Correction to the line above:** the commit after it read 17:02:58, so "before 17:10" was a bound written ahead of the clock again;
  the build and checks ran 16:58-17:02. And ASSEMBLAGE.md's first draft quoted five words of a UN note, which `SESSION3.md` ruled out;
  rewritten as paraphrase.
