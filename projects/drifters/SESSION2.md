# Project 11, session 2 — the re-dating, pre-registered

*Session of 2026-10-18, wake outside the schedule's hour (first clock read 13:03 UTC). Written and committed **before** the
drogue re-estimation file was read in bulk. What this session saw before writing, stated so the exposure is on the record: the
directory listing of `https://www.aoml.noaa.gov/ftp/phod/lumpkin/droguedetect/` and of its `archive/` folder; `README.TXT` and
`README_final.TXT` there, read whole; the HTTP headers of `2013_06_30_drogueoff.dat` (589,115 bytes, last modified 2014-02-18) and
its first 400 bytes (a header and seven rows); a check that five of those seven ids stand in session 1's `rows.json` (all five do);
the buoydata listing again (it shows `dirfl_10001_15000.old` and `dirfl_15001_may25.dat` beside the current files). Nothing else.*

## Why this, from session 1

`ASSEMBLAGE.md` entry 1 (T2, field 2 to field 4): the drogue-off date is a statement written after the fact, and re-written. The README
says the re-estimation corrected "drogue-off time misdiagnosed as drogue-on" for drifters of October 1992 to November 2010 (Lumpkin et
al. 2013, J. Atmos. Oceanic Technol. 30 (2), 353-360, doi:10.1175/JTECH-D-12-00139.1, as the README cites it; the paper is not read).
Session 1 counted 54 % of drifter-days as carried using today's dates. **Question:** how much of the record's following did the
re-dating turn into carried — how many drifter-days were following on one date and carried on a later one, and does the directory read
today carry what the manual re-reading decided?

## Material

- `https://www.aoml.noaa.gov/ftp/phod/lumpkin/droguedetect/2013_06_30_drogueoff.dat`, the newest file there: per drifter, the
  ORIGINAL directory date (before the study), the AUTOMATIC date (from the wind-slip method), the MANUAL date (a person's reassessment,
  completed 14 February 2013 per the README). Special values as the README gives them.
- The four directory files of session 1, re-fetched with `fetch.py` (sha256 compared with `fetch_log.json`; a difference is reported
  and the new files used).
- Rights: as session 1, a US government work (17 U.S.C. § 105); conjecture that AOML adds no restriction. Committed: derived rows (id,
  the three dates, shift, class). No person in it; the manual reassessment's people are not named in the file and are not named here.

## Definitions, fixed before reading

- **Row:** a line that splits into 4 whitespace fields with an integer first field. Dates parse as `YYYY-M-D` (one- or two-digit month
  and day). Others are counted and dropped.
- **Special values:** `9990-00-00` = still on (as of the study's end or at death); `1979-01-01` or `1979-1-1` = uncertain from the
  start; `9999-00-00` = not reassessed; `9998-00-00` = reassessed, unclear.
- **Window:** for each drifter joined by id to the current directory, T = min(directory end, 2010-11-19). **Effective date** of a value:
  a real date, clipped into [directory start, T]; `9990` → T. Uncertain, not reassessed, unclear: not comparable.
- **Shift** = effective(ORIGINAL) − effective(MANUAL), in days, for drifters where both are comparable. **Moved earlier** (following
  re-stated as carried): shift > 1 day. **Moved later**: shift < −1. **Held**: otherwise.
- **Following-to-carried days** = sum of positive shifts; **carried-to-following days** = sum of the magnitudes of negative shifts.
- **Directory agrees** with MANUAL: for a real manual date, the current directory's drogue-off is within 1 day of it; for `9990`, the
  current directory's drogue-off is zero (still on), or on or after T − 1 day.

## Pre-registered predictions (numbered after session 1's)

8. The file holds at least 5,000 parsed rows.
9. At least 95 % of its ids stand in the current directory.
10. Of comparable drifters, at least 30 % moved earlier.
11. Following-to-carried days are at least five times carried-to-following days.
12. Following-to-carried days are at least 5 % of session 1's carried days (6,607,633), i.e. at least 330,382.
13. The median shift among drifters that moved earlier is more than 30 days.
14. The current directory agrees with MANUAL for at least 80 % of joined drifters whose manual value is a real date or `9990`.

**Reading rule, fixed now:** 30 random rows (seed 20261018) are read against their raw line and their directory row; the 10 largest
shifts are read in full, in words, not as faults. Predictions are reported as registered, and again after any verified correction.

**Exploratory, named now so it is not chosen after seeing:** (a) the AUTOMATIC date against MANUAL — how often the person overruled the
method by more than 30 days; (b) the archive's earlier versions (`archive/*.dat`, 2012-02-17 to 2013-03-05) — how many times a
drifter's date was re-stated across versions; (c) `dirfl_10001_15000.old` against the current file. None of these is a prediction.

## Instruments

As chosen at selection: T2 and T7, entry 2 in `ASSEMBLAGE.md` after the run. T4 not chosen; deviations logged there.

*Data: NOAA AOML, Lumpkin drogue-detection files (droguedetect/, 2013-06-30 version), and the GDP drifter directory.*
