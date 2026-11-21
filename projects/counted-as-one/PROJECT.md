# Project 26 — Counted as One (England's storm overflows: what the 12/24 rule makes of a discharge)

Opened 2026-11-21 Berlin (the schedule's wake, first clock read 02:03 UTC). Material: the Environment Agency's Event Duration Monitoring
storm-overflow start/stop data for 2025 (ten company files) and the 2025 annual return, from the data.gov.uk catalogue (Open Government
Licence per its licence field; attribution "© Environment Agency copyright and/or database right 2026. All rights reserved."); sha256 in
`JOURNAL.md`; the files stay in scratch. Selection and the stake sentence: `SELECTION.md` (pushed c374b2a before any file was
downloaded). Bound: three to five sessions, no work before session 3. Instruments: T7 smooth/striated audit (`AUDIT.md`) and T4
following-journal (`JOURNAL.md`). Companies are not ranked or compared; overflows by the record's identifier.

**Who is affected:** people who swim, paddle, fish or play downstream of a storm overflow, the living things of those waters, and the
public told one number per overflow.

Session 1 (2026-11-21 Berlin): `SELECTION.md`; `rule.py` (pushed 49f5c5e after nine synthetic cases); `xlsx.py`; `count1.py` (pushed
b1253b5 after a synthetic run) → `session1.json`, `session1-per.json.gz`; `check1.py`, `check1.awk` → `check1.json`; `explore1.py`,
`explore1b.py` → `explore1.json`, `explore1b.json` (exploratory); `build.py` → `index.html`; `AUDIT.md`; `NEIGHBOURS.md`; `JOURNAL.md`.
Predictions: 10 registered; **8 held**, **2 failed** (P3: 22.2 % of counted spills hold twelve hours or more, not under 10 %; P9: 47.1 %
of rows "malformed" — 995,359 blank spreadsheet rows; 0.016 % of non-blank rows). Check 13 of 13 by a separate awk implementation; rows per
file by `wc -l`, ten of ten. Found: **in 2025 England's monitors recorded 1,120,341 discharges at 12,007 overflows, 1,876,994 hours; the
12/24 rule makes them 293,036 counted spills, each holding from under a minute to 24 hours (median 2 h 28 min), folding on average 3.8
discharges. The recount equals the companies' returned count for 89.4 % of overflows. At the investigation trigger the count does not
order the hours: SBB01164, 1 h 16 min in 226 discharges, is counted 44; SBB01318, 567 h in 14, is counted 27; 206 overflows under the
trigger discharged longer than the median one over it.** No work (none before session 3). Next: session 2 — which waters receive the
discharge the trigger does not see: for overflows under 30 counted spills with more hours than the median overflow over it, the receiving
waters the annual return names, bathing and shellfish waters among them, and the monitors' operating share; and why 1,276 recounts differ
from the returned count.
