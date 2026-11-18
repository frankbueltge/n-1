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
