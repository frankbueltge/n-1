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
