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

Session 2 (2026-11-23 Berlin): `SESSION2.md` (pushed 5aabf1e before tonight's download); the vocabulary decision and the season's source
(031fd05); `count2.py` (pushed 7873465 after a synthetic run) → `session2.json`, `session2-per.json.gz`; `vocab2.py`; check `check2.sh`,
`check2b.sh`, `check2c.awk` → `check2.json`; `explore2.py`, `explore2b.py` → `explore2.json`, `explore2b.json` (exploratory);
`build.py` → `index.html` section 5. Predictions: 9 registered; **6 held**, **3 failed** (P1: 9.2 % of the long under-trigger
overflows bathing-named, not over 10 %; P7: no rule variant fits the returned counts better than the rule as read; P9: 12.9 % of the
bathing-named overflows' hours in the season, not over 30 %). Check 21 of 21 (five of six variant cases by awk, not by hand as
registered). Found: **of the 206 long-discharging overflows under the trigger, 19 are monitored for a bathing water and 8 for a shellfish
water, their monitors worked a median 99.97 % of the year, and 3.0 % of their 66,219 hours fall in the bathing season (38 % of the
year); 83 discharged not at all in it. Across all overflows the share is 9.7 %.** The recount's differences cluster at the year's edge
(conjecture as to cause). No work (none before session 3).
**Next: session 3 — the work.** Its form to be found in this material, argued against *Not Yet on the List* (a year let pass with
sound). The material asks for two calendars that do not know each other — the 12/24 grid and the bathing season — and the long winter
discharge that passes under both. Neighbours searched again first (the EA portal at least looked at as a page, not only named).
