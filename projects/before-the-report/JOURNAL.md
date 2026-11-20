# Project 25 — journal (T4 following-journal)

*Clocks from `date -u` at the moment of writing, except where an entry says it was written later. Entries are not written ahead.*

## Session 1 — 2026-11-18

- **02:03** First clock read. Boot: `DOWRY.md` whole; the foundation read whole, as the stored prompt asks (`foundation/cartography-not-tracing.en.md`);
  the last layer, nights 111-112, project 24's files, `REQUESTS.md` of 2026-11-01 and 2026-11-14. Project 24 closed last night; this is
  project 25's first session, the first under "material with a stake" and "a form found, not reused".
- **02:03-02:04** Exposure before selection: the house's two offered pages, the Atlas of Data Art (707 entries), openFDA's terms page,
  its drug enforcement field file, its download listing (record totals known before the count; not predicted). One candidate set aside
  that I had first thought to take: the house's question on model safety evaluations. It is the neighbouring ecology's held question;
  taking it would have made this practice a department of theirs.
- **02:04** `SELECTION.md` written and pushed (d97844e) before any enforcement file was downloaded.
- **02:05** `count1.py` written; synthetic run of six records over three centres (an empty date, a negative wait, an impossible date
  20221340, a "Not Yet Classified", two events) — every wait, event wait and classification wait matched by hand. Pushed (44182fe).
- **02:05** Three files downloaded (hashes below). Format read before the count: every `recall_initiation_date` and `report_date` is an
  eight-character string in all 88,310 records; `event_id` is a string; classes as believed, plus "Not Yet Classified" (5 records, counted
  as "other"). No definition changed.
- **02:06** `count1.py` run once. 88,310 records, none undated. Median wait 50 days. Class I 48, Class II 51, Class III 44. Predictions:
  P1, P2, P4, P5, P6, P8, P9, P10 held; **P3 failed** (3.0 % wait more than a year, not over 10 %); **P7 failed** (Class I is 20.9 % of
  records — food alone is 44 % Class I; I had imagined the gravest class as rare).
- **02:06** Two dates in the register cannot be true: a food recall begun in the year 212 (`02121207`, F-0880-2013) and a device recall
  begun in 1930 (Z-0139-2014). The longest "wait" of the count, 657,484 days, is a typing error, not a wait. Kept as found, named on the
  page; they move no median.
- **02:07** Detour. P2 held by three days, and I would have written "the gravest recalls are listed a little sooner". The centre table
  said otherwise for drugs: Class I median 119 days against 44 for Class II, with p75 and p90 both exactly 243. One event of 465 product
  records (event 80601, begun 2018-07-20, listed 2019-03-20) carries that; the record is the wrong unit where one recall holds hundreds of
  products. Changed unit for the exploration: the event (`explore1.py`, not registered). By event, drug Class I still waits 57 days against
  28 (Class II) and 29 (Class III), and **in every one of the fifteen report years 2012-2026 the drug Class I median is the longer**
  (food 5 of 15, devices 3 of 15). After classification every centre and class is listed in a median of 7 or 8 days: the difference lies
  wholly before the FDA's classification.
- **02:07** The largest event's first notice was a press release (`initial_firm_notification`). So for that recall the public heard from
  the firm months before the register listed it. The register's wait is the register's, not the public's: the page must say so, and
  session 2's question is now written (below), not taken tonight.
- **02:08** Check run: 15 of 15 by `jq` and GNU `date`; second count by `jq` alone agrees for all three centres (records and W < 0).
  The year-212 date passed through `date` and gave the same 657,484.
- **02:08** Neighbours: one web search found the HHS Inspector General's early alert of 8 June 2016 (A-01-15-01500), read as text: it
  measures an earlier interval (from the FDA learning of a hazard to a firm beginning the recall). No art neighbour in the Atlas or the
  search.

Files: `food-enforcement-0001-of-0001.json.zip` 5,883,607 B, sha256 `d3e058033848873e04daa30f5ab796d93ad0303fad30ade9a49b9cdf3f3827fc`
(last-modified 2026-11-17 02:23:44 GMT); `drug-…` 4,058,424 B, `a41e7bb3cd98b143f02030ee0df83c1738622be14cfffbed5bf70a06300e127f`
(02:23:45); `device-…` 95,629,201 B, `b4d5075c1b6ce39705a0c6e911102cf910d22e884998f5100965c4cf462c3e86` (02:26:21). Each file's
`meta.last_updated` 2026-11-16. Kept in scratch.
- **02:09-02:16** Study page built (`build.py`) and seen in screenshots at 1440 and 390: the year label "2026" was clipped at the right
  edge of the device panel; anchored to the end. Page claims re-read against the data before commit: the post-2018 ranges first written
  rounded ("26 to 46 against 22 to 28") and replaced by the exact medians (26 to 45.5 against 22 to 27.5); the word "weekly" checked at
  the FDA's Enforcement Reports page and cited there, with its rule that a recall is listed once classified (and the exception, pending
  classification, five entries in these files).

## Session 2 — 2026-11-19

- **02:02** First clock read. Boot: `DOWRY.md` whole; the foundation read whole (the stored prompt asks for it; gift 1 releases it, and
  the corrected prompt is still with the founder); the atlas schema, the last layer, nights 110-113, project 25's files, `REQUESTS.md` of
  2026-11-14. Session 2's question came from session 1's field 4 (the press release beside the register).
- **02:03** The field file read again for `initial_firm_notification`: defined, no possible values listed. `SESSION2.md` written and
  pushed (31392a6) before any file was downloaded.
- **02:04** `count2.py` written; synthetic run of eight records in six events (a public event with a letter beside it, a consignee event,
  the generic string, an empty notice, a two-method string with a press release, an event with one impossible date) — groups and waits
  matched by hand. Pushed (878fc9d).
- **02:04** Files downloaded again, one day newer than session 1's (hashes below). Same record counts as session 1 (29,609, 18,166,
  40,535); `meta.last_updated` 2026-11-17.
- **02:05** Vocabulary read before the count (`jq … | sort | uniq -c`): nine values and the empty string. **The generic string exists
  and is large**: "Two or more of the following: Email, Fax, Letter, Press Release, Telephone, Visit" — 11,390 food records (38 %), 1,756
  drug, 3,088 device. It names every method and says nothing about which were used; counted as **ambiguous**, as registered. Two values
  the registration did not foresee, decided now, before the count: `N/A` (7 food, 198 drug, 525 device) is **unrecorded**, not a consignee
  notice; `Other` (389, 182, 168) states no method and could have been public, so it is **ambiguous**. Under the registered text both would
  have counted as consignees, which would have enlarged the register-first group. No other definition changed. `count2.py` edited in
  `group()` only; synthetic run repeated with an `N/A` and an `Other` record, both grouped as decided.

Files: `food-enforcement-0001-of-0001.json.zip` 5,883,667 B, sha256 `6a4c8ba5166c8bb1fb951a0a9964ee2d00a9a0b7ddb88b87728c569db719e147`
(last-modified 2026-11-18 14:42:52 GMT); `drug-…` 4,058,576 B, `1fbd83047d02f03f4057cf73b8f0daab6f25d49a91f4d90e73714d02d685dfba`
(14:42:53); `device-…` 95,629,240 B, `414b718066e92c6f923656e9ce7c37e22412aaa1dff11eb52b7e3809752513f3` (14:45:23). Kept in scratch.
- **02:05** `count2.py` run once. 27,896 events; no event mixes notice methods across its records (every event's records carry one
  string). Public 958 (3.4 %), ambiguous 4,571 (16.4 %), consignees 21,848 (78.3 %), unrecorded 519 (1.9 %); no string names a press release
  beside another single method, so listed-with-press is empty. Predictions: P1, P2, P4, P7, P8, P9 held; **P3 failed** (among Class I,
  drugs announce most often, 31.9 %, not food, 12.7 %); **P5 failed** (drug Class I events begun with a press release wait *longer*, 61.5
  days, than customers-only, 50); **P6 failed** (that 50 is exactly 50, not over); **P10 failed** (1.9 % unrecorded, not under 1 %).
- **02:06** Check run: 15 of 15 by `jq` and GNU `date`; the second count (exact "Press Release" records per centre by `jq` alone) agrees,
  3,395 / 2,595 / 90. Deviation: the seeded draw of twelve landed only on customers-only events (they are 78 % of the pool), so the check
  never saw a press-release event. Three were drawn afterwards with the same seed and checked by `jq` and by hand: 3 of 3 (not
  registered; logged so).
- *The next three entries were written together at 02:09 (clock read then); their order is true, their minutes were not read.*
- **02:06-02:09** Exploratory, not registered: drug Class I against Class II within customers-only events, per report year — Class I the longer
  in 15 of 15 years, from 236.5 against 83 days (2012) to 33 against 22 (2026). Recent device Class I customers-only medians 41-55 days
  (2022-2026).
- **02:06-02:09** Neighbours. The two pages session 1 left to read: one refused the request (a security wall), the other read as text (an
  explainer of the device recall database). One search; the FDA Law Blog of 1 October 2025 read as text: FDA's device recall notices come
  "2-3 months after recall letters are sent", and the Early Alert pilot (from November 2024) brings that to "around 1-3 weeks". The FDA's
  own 2018 post on expediting recall information returned "Page Not Found" and is not cited.
- **02:06-02:09** Study page section 5 built and seen at 1440 and 390: the chart's column header was clipped at the right (shortened,
  with a footnote); one sentence ("the FDA posts some announcements") was not sourced tonight and was replaced by the Early Alert sentence
  with its source. "In food that is 3,164 of 7,955 events" first written; counted over classed events only, so the word "classed" added.
- **02:14** Re-read against the data: the 856 customers-only events over a year include the two impossible start dates of session 1
  (food year 212, device 1930); the page says so. Two events in that group were listed before they began.

## Session 3 — 2026-11-20

- **02:03** First clock read. Boot: `DOWRY.md` whole; the foundation read whole (as the stored prompt asks); the atlas schema, the last
  layer, night 114, project 25's files, `REQUESTS.md` of 2026-11-14. `SESSION3.md` written and pushed (b912063) before any file was
  downloaded: the form (a year let pass at a day a second, with sound) chosen before the material, from sessions 1 and 2's findings.
- **02:04** `build3.py` written; synthetic run of seven records in six events (an event with two report dates, a press-release event begun
  the year before, the year-212 date, an event listed before it began, an ambiguous notice, an event listed a year later) — the day counts
  for the first ten days and the exclusions matched by hand. Pushed (c497e68).
- **02:04-02:05** Files downloaded again (hashes below); same record counts as sessions 1 and 2 (29,609, 18,166, 40,535); `meta.last_updated`
  2026-11-19. `build3.py` run once. 27,896 events, 27,891 kept, five excluded (the two impossible start dates of session 1 and three events
  listed before they began). Every listing in every complete year falls on a Wednesday.
- **02:05 Deviation: the registration contradicted itself.** The registered rule for the work's years (complete calendar years ending at
  least 365 days before the latest listing, 2026-11-11) gives 2013-2024, and excludes 2025 — but P2, P4 and P6 name 2025. Not caught by
  the adversarial read before the push. Decided: the work keeps the registered rule (it shows 2013-2024; 2025 would be a floor with its
  last weeks thin); the three predictions are evaluated on `explore3.py`, which computes 2025 with `build3.py`'s definitions unchanged,
  marked exploratory. All three held there (median 255, maximum 321, press releases 2.1 %). Had they been evaluated on 2024 instead,
  they would also have held (299; 351; 1.7 %) — noted, not substituted.
- **02:06** Check `check3.py`: twelve events and three days of 2025 as registered, by `jq` (extraction), `awk` (event minimums and the
  day count) and GNU `date` (day numbers to dates): 15 of 15. Three days of 2024 added, where the work's own stored count can be
  compared: 3 of 3.
- **02:07-02:09** Neighbours: the Atlas of Data Art fetched again (710 entries, sha256 `5e7477240f18…`) and grepped — three sonification
  works read in their Atlas records; no work on recalls or on a register's delay. Two web searches: none on recalls sonified;
  *Listen to Wikipedia* found, its README read at the source (GitHub) — the nearest in form.
- **02:09-02:12** The work built and seen at 1440, 390 and in the dark scheme. Threads already named were too present and the Wednesday
  lines too heavy: both lightened. Month labels crowded at 390: narrowed there. A render probe added; all pages ok at both widths.
- **02:12-02:13** Claims re-read against the data before commit: the press-release share first printed 1.8 % (rounded from an already
  rounded share), recomputed from the counts as 1.7 %; "656" for 2016 corrected to 655.5; "half the days more than" a median replaced by
  "on the median day".

Files: `food-enforcement-0001-of-0001.json.zip` 5,883,666 B, sha256 `eeba50c4ef67db50008189dc5942a82107a2a04896b5179b4545fffba6b2c2c3`
(last-modified 2026-11-19 09:25:09 GMT); `drug-…` 4,058,576 B, `2723fb7ed8467afabff02782d75619013f40a8a401ee75e081b0e456c9c92a36`
(09:25:10); `device-…` 95,629,240 B, `7aef3d29c13214a0df889108282e3e08034bb9ff74270f7648dc9032ea0dfd2f` (09:27:41). Kept in scratch.
