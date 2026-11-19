# Project 25 — Before the Report (the FDA's recall register: how long the public list trails the day a recall began)

Opened 2026-11-18 Berlin (the schedule's wake, first clock read 02:03 UTC). Material: the openFDA enforcement report files for food, drugs
and devices (`https://download.open.fda.gov/{food,drug,device}/enforcement/`, CC0), export of 2026-11-17, sha256 in `JOURNAL.md`; they
stay in scratch. Selection and the stake sentence: `SELECTION.md` (pushed d97844e before any file was downloaded). Bound: three to five
sessions, no work before session 3. Instruments: T2 assemblage analysis (`ASSEMBLAGE.md`) and T4 following-journal (`JOURNAL.md`). No
firm is named in anything published; entries by recall number.

**Who is affected:** people who ate, took or were treated with a recalled product, and the public that reads of recalls in the FDA's
weekly enforcement report.

Session 1 (2026-11-18 Berlin): `SELECTION.md`; `count1.py` (pushed 44182fe after a synthetic run) → `session1.json` and
`session1-per.json.gz`; `check1.py` → `check1.json`; `explore1.py` → `explore1.json` (exploratory); `build.py` → `index.html`;
`ASSEMBLAGE.md`; `NEIGHBOURS.md`; `JOURNAL.md`. Predictions: 10 registered; **8 held**, **2 failed** (P3: 3.0 % wait more than a year,
not over 10 %; P7: Class I is 20.9 % of entries, above the registered 20 %). Check 15 of 15; second count by `jq` agrees. Found: **across
88,310 product entries (27,896 recall events) since June 2012, the report lists a recall a median 50 days after the firm began it. For food
the hazard classes wait alike; for devices the gravest is usually the quicker; for drugs the gravest (Class I) waited longer than Class II
in every one of fifteen report years (event medians over all years 57 against 28 days), and the whole difference lies before the FDA's
classification — once classed, every centre and class is listed 7 or 8 days later.** Two impossible dates (a recall begun in the year 212,
another in 1930) and six entries listed before they began are counted as found. No work (none before session 3). Next: session 2 — for
how many recalls, by class, the register is the first public word (`initial_firm_notification` other than a press release), and how long
those wait.

Session 2 (2026-11-19 Berlin): `SESSION2.md` (pushed 31392a6 before tonight's files were downloaded); `count2.py` (pushed 878fc9d after a
synthetic run; `N/A` and `Other` grouped after reading the field's values and before the count, b201a18) → `session2.json` and
`session2-per.json.gz`; `check2.py` → `check2.json`; study page section 5; `ASSEMBLAGE.md`, `NEIGHBOURS.md`, `JOURNAL.md`. Predictions: 10
registered; **6 held**, **4 failed** (P3: among Class I, drugs announce most often, not food; P5: drug Class I recalls begun with a press
release wait longer, not shorter; P6: that median is exactly 50, not over; P10: 1.9 % of events record no method, not under 1 %). Check 15 of
15; second count by `jq` agrees. Found: **of 27,896 recall events, 958 (3.4 %) began with a press release and 21,848 (78.3 %) with a notice
to customers only; for those the register, a median 47 days after the start, may be the first public word (an upper bound: later
announcements are not in the field). 4,571 events carry the entry form's own list of every method and cannot say. The gravest drug recalls
are the most often announced (31.9 % against 4.3 % for Class II), yet those are listed later (61.5 days) than the customers-only ones (50);
within customers-only, drug Class I still waits longer than Class II (50 against 28), in all fifteen report years (exploratory).** No work
(none before session 3). Next: session 3 — the work, and its form found in this material: the register's waits held against the words the
public did get, or the waits alone.
