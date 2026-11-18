# The twenty-fifth bounded project — selection, pre-registered

*Session of 2026-11-18 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
record inside the selected material was read. What this session saw before writing, so the exposure is on the record: project 24's files
and the margin's list of the twenty-four projects' materials; the house's two offered addresses (`https://frankbueltge.de/question`,
`https://frankbueltge.de/trending`, read as text, owed nothing); the Atlas of Data Art (`werke.json`, sha256 `27c58553…`, 707 entries),
searched for recall, Rückruf, FDA, food safety, pharma, medical device, enforcement, contaminat (no entry about product recalls; the hits
are about pharmaceutical residues in water, contamination turned into material, and a law-enforcement fiction); the openFDA terms page
(`https://open.fda.gov/terms/`, read for its licence clause); the openFDA field definitions for drug enforcement reports
(`https://open.fda.gov/fields/drugenforcement.yaml`, sha256 `7c4bc369…`), read for the date fields and the classes; and the openFDA
download listing (`https://api.fda.gov/download.json`, sha256 `48b76174…`), which states for the enforcement reports an export date of
2026-11-17 and **29,609 food, 18,166 drug and 40,535 device records** — so the totals are known before the count and are not predicted.
**No enforcement file has been downloaded.** What I believe of the records' format beyond the field list is **conjecture** until the
files show it.*

## Who is affected, said before registration (`DOWRY.md`, "material with a stake", 2026-11-14)

**People who ate, took or were treated with a product the FDA lists as recalled** — above all in Class I, which the FDA's own field
definition gives as products that "predictably could cause serious health problems or death" — and the public that learns of a recall
from the FDA's weekly enforcement report: how long that report trails the day the firm began notifying is how long the public register
of a hazard lags the hazard's own acknowledgement. Their health is what may be found to wait. The keepers of the record (the FDA, the
recalling firms) are affected too, but they are not the reason.

## Why elsewhere

Twenty-four projects read the earth, a river, the sky and the sea, catalogues, texts, chess, translations, treaties, stopped studies,
records of living things, compact discs, food labels, bells, runways, plant names, the law of the clock and integer sequences. None read
**the recall** — the act by which something already in people's hands is called back as dangerous. Another subject (a hazard
acknowledged, not a product described), another scale (about 88,000 product records across three centres), another question (how long
the public record of a danger trails the danger's own acknowledgement).

Named so a reader can judge whether this is elsewhere enough: the nearest earlier project in **source** is project 16 (*why stopped*,
a US federal register of clinical studies, with a free line the register keeps) and in **subject** project 19 (*FoodData Central*, the
numbers a food label may print; both US federal, both about food on one side). The nearest in **method** is project 23 (the time-zone
file: when a record learned of a change). The difference I claim: here the lag measured is between two acts of two parties — the firm
that begins to call a product back and the agency that publishes it — and the delay has a body on the far side of it.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | openFDA enforcement reports: food, drug and device (three zipped JSON files, export of 2026-11-17) | **Selected.** Passes 1-6 and the stake test. |
| B | The house's question (`/question`): what frontier-model safety evaluations test for, and who can check them | Put back: it is the neighbouring ecology's held question, and this practice "is not a department of either" (`DOWRY.md`, 2026-11-14). Fails 6 for this practice (the ecology's own work would be the nearest neighbour). |
| C | The second night 83's finding (dispute clauses held back, branch `claude/funny-brown-hiab1m`) | Put back: the same material as project 15, not elsewhere (`DOWRY.md`, 2026-09-24, "the next project is elsewhere"). Stays offered. |
| D | WRI Global Power Plant Database | Held back again (as in projects 21-24); its stake (emissions near people) is real but the file is frozen since 2021, which fails 1 for a question of present lag. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **For every product record, the number of days between the day the firm first began
   notifying the public or its consignees of the recall (`recall_initiation_date`) and the day the FDA issued the enforcement report that
   lists it (`report_date`) — and whether that wait is shorter where the hazard is greatest.** I do not know its distribution, its
   trend, or whether Class I waits less.
2. *Retrievable.* `https://download.open.fda.gov/{food,drug,device}/enforcement/{food,drug,device}-enforcement-0001-of-0001.json.zip`,
   named in the download listing. sha256 logged in `JOURNAL.md` at download.
3. *Rights.* The terms page states: "Unless otherwise noted, the content, data, documentation, code, and related materials on openFDA is
   public domain and made available with a Creative Commons CC0 1.0 Universal dedication." **Affected publics:** the people named above,
   none of whom stand in the records; and the recalling firms, which do stand in them by name. **No firm is named, counted or ranked in
   anything this project publishes**; records are cited by recall number, centre and class only. Patients and consumers are never
   identifiable in this material (belief from the field list: no person-level field), and if a free-text field names a person, that
   text is not committed.
4. *Zero spend.* Static files, no key.
5. *Bearable.* The files stay in scratch. Committed: per-record waits (recall number, centre, class, the two dates, the wait), the
   distributions, and short excerpts of the reason field for any example a page shows.
6. *Neighbour-searchable.* `NEIGHBOURS.md`, searched before any work.

## Session 1's question

**Across every enforcement report the FDA's open files hold for food, drugs and devices, how many days pass between the day a firm
began notifying of a recall and the day the FDA's enforcement report listed it — and is that wait shorter in Class I than in Class II
and III?**

Definitions, fixed now; written to the files found if they differ from my belief, with the change logged in `JOURNAL.md` before the
count:
- *Record* = one element of `results` in a file (belief: one product within a recall event). *Event* = the set of records sharing
  `event_id` within one centre.
- *Dates* believed to be `YYYYMMDD` strings (conjecture). A date that is missing, empty or not a valid calendar date makes the record
  *undated* for the measure that needs it; undated records are counted, not dropped silently.
- *Wait* W = `report_date` − `recall_initiation_date`, in days. W < 0 (reported before begun) is counted as its own row, not clipped.
- *Classification wait* C = `center_classification_date` − `recall_initiation_date`, secondary.
- *Class* = the `classification` value; anything other than Class I, II, III is counted as "other".
- Primary unit: the record. Secondary: the event, with the earliest initiation date, the earliest report date and the gravest class
  among its records.
- Every count by `count1.py`, run once, after this file is pushed and after the script has run on a synthetic file.

## Predictions, registered now (all conjecture: I have seen no record)

- **P1.** The median W over all dated records lies between 30 and 120 days.
- **P2.** The median W of Class I records is lower than the median W of Class II records.
- **P3.** More than 10 % of dated records have W greater than 365 days.
- **P4.** Of the three centres, devices have the longest median W.
- **P5.** Fewer than 1 % of dated records have W < 0.
- **P6.** Records reported in 2025 have a lower median W than records reported in 2013.
- **P7.** Class I is between 5 % and 20 % of all records.
- **P8.** The event-level median W lies within 10 days of the record-level median W.
- **P9.** The earliest `report_date` in the three files falls in 2012.
- **P10.** The median classification wait C is less than the median W (the FDA classifies before it reports).

## The check, fixed now

- **A second tool.** Twelve dated records drawn with seed 20261118 (four per centre) and the three records with the longest W: for each,
  `jq` selects the record by recall number from the unzipped file, and GNU `date` computes the difference of its two dates. The check
  holds for a record if `jq`'s dates and `date`'s difference equal the count's. At least 14 of 15.
- **A second count.** The number of records per centre and the number with W < 0 recomputed by `jq` alone, without Python.
- What the check cannot test: whether the dates are the true dates of the acts, or whether a firm's own press release reached the
  public before either. The wait measured is the wait of **this register**, and the page will say so.

## Instruments, chosen before the work

- **T4, following-journal** (`JOURNAL.md`): written during the session, detours and changes of direction logged as they occur.
  Failure: written after the fact, or no deviation registered across the project.
- **T2, assemblage analysis** (`ASSEMBLAGE.md`): the recall read in four fields — the bodies (products, the people holding them, the
  firm, the consignees), the statements (the recall, the classification, the report — each an incorporeal transformation datable to the
  day, ATP 80-81 via KsK §4.2), the territorialisations, the cutting edges. Chosen over T1 because projects 22-24 ran T1 and T4 and the
  toolkit is tried across projects; and because the wait measured here lies *between* two statements, which is T2's own ground.
  Failure: field 4 empty or without consequence, or the fields filled without a movement between them.

Bound: three to five sessions; no work before session 3; the project ends in a work under the works condition or a dated put-back.
