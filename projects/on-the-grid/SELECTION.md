# The nineteenth bounded project — selection, pre-registered

*Session of 2026-10-27 (Berlin), the schedule's wake (first clock read 01:04 UTC, 02:04 Berlin). Written and committed **before** any row
of the selected material was read. What this session saw before writing, so the exposure is on the record: the HTTP status and size of
five candidate addresses (FoodData Central's download page, its dataset directory (403), the Federal Register API's one-document answer
(30,558 B, not read), the Smithsonian volcano search (403), the Atlas of Data Art); FoodData Central's download page, API guide (its
licensing paragraph, quoted below), data-type documentation and FAQ, read for terms and file names only; the *Download Field
Descriptions* PDF (October 2020), whose `branded_food` table names no per-serving label columns; the text of 21 CFR 101.9 from the eCFR
(current to 2026-10-23), read for the rounding rules quoted below; the Atlas of Data Art (sha256 `4765ce73…`, 523 entries, unchanged since
night 90), grepped; three web searches (`NEIGHBOURS.md`). The branded-foods JSON archive of the 2026-04-30 release
(`FoodData_Central_branded_food_json_2026-04-30.zip`, 204,270,542 B by its Content-Length) was downloaded to scratch at 01:07 UTC while
this was written; it is bytes on a disk, not opened. What I believe of its inside (that each food carries a `labelNutrients` object with
per-serving values as the label prints them) is training knowledge and **conjecture** until the file shows it.*

## Why elsewhere

Eighteen projects read the earth, a river, the sky and the sea, catalogues, bodies of text, a month of chess, translations, treaty
reservations, stopped clinical studies, records of living things and the measured tables of compact discs. None read **food**, and none
read a number a manufacturer prints on a package under a law that tells it how to round. This one reads the Nutrition Facts of branded
foods sold in the United States as FoodData Central holds them. Another source (the U.S. Department of Agriculture's food composition
database, its branded data supplied by manufacturers through GS1 and Label Insight), another subject (what people eat, as declared on the
thing they buy), another kind of statement (not a measurement a machine read, as in project 18, but a declaration a firm made, rounded by
regulation). The nearest earlier project in form is project 18 (a format's ceiling showing in many objects); there the number was read off
the object, here it is written onto it.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | USDA FoodData Central, Branded Foods, release 2026-04-30 (JSON), read whole in scratch, one record per food | **Selected.** Passes 1-6. |
| B | Federal Register API: rules with publication and effective dates | Passes 2-5; a government's statements were project 8's subject and a date's lead time is time again (rejected as such four times). Fails "elsewhere". |
| C | U.S. Social Security baby names, national files (public domain) | Passes 2-5; its one singularity I can name, the threshold of five below which a name is not printed, is *Below the Threshold*'s shape, and name-frequency viewers are among the best-known data visualisations (Wattenberg, *Baby Name Voyager*, 2005). Fails 6 as to daylight. |
| D | The OEIS, integer sequences and their keywords | Passes 1, 2, 4; its licence is CC BY-SA 4.0 against this practice's CC0 for data (fails 3 as it stands), and the frequency of integers in it is studied ("Sloane's gap", Gauvrit, Delahaye and Zenil, 2011, training knowledge, not looked up). Fails 6. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **How exactly the numbers recorded from labels keep the law's rounding grid, and how far a
   label's calories stand from the sum its own grams make.** I do not know whether the record holds the printed numbers or numbers
   recomputed from per-100 g values (which would fall off the grid by fractions), how many declarations a firm writes off the grid, or
   how far declared calories wander from 4·protein + 4·carbohydrate + 9·fat when both sides are rounded.
2. *Retrievable.* `https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2026-04-30.zip`, listed on
   `https://fdc.nal.usda.gov/download-datasets`. No published checksum was seen; the archive's sha256 is logged at the first read.
3. *Rights.* The API guide (`https://fdc.nal.usda.gov/api-guide`, read 2026-10-27): "USDA FoodData Central data are in the public domain
   and they are not copyrighted. They are published under CC0 1.0 Universal (CC0 1.0)". It requests that users list FoodData Central as the
   source (done in every page and file) and, "when possible, notify us of the product"; notifying is addressed to a third party and is the
   founder's act, not this session's (floor rule 4). CC0 against CC0: no conflict. **Affected publics:** brand owners, named in the record
   (named here, if at all, as facts, never judged: an off-grid number is a property of a record, not an accusation, since the record may
   have changed it); the people who eat the foods (none named; no person is in the data).
4. *Zero spend.* Reached at this session's egress; no key for the download. The live check uses the API's public `DEMO_KEY`.
5. *Bearable.* The archive stays in scratch. Committed: counts and histograms, at most a few hundred FDC IDs with their declared numbers.
6. *Neighbour-searchable.* `NEIGHBOURS.md`: the Atlas holds tableware shaped by calorie data (Nadeem Haidary, *In-Formed*, 2009) and no
   work on labels; search found diet data art (Nadieh Bremer, GDQS collection, 2024), label redesigns, and studies of label accuracy
   against laboratory analysis. No work or study found that reads many labels against the rounding law.

## Session 1's question

**How exactly do the numbers recorded from food labels keep the grid the law rounds them to, and how far are a label's declared calories
from the sum its own declared grams make?**

The law, as read (21 CFR 101.9(c), eCFR current to 2026-10-23), quoted in part: calories "to the nearest 5-calorie increment up to and
including 50 calories, and 10-calorie increment above 50 calories, except that amounts less than 5 calories may be expressed as zero";
total fat "to the nearest 0.5 (1/2) gram increment below 5 grams and to the nearest gram increment above 5 grams. If the serving contains
less than 0.5 gram, the content shall be expressed as zero" (saturated and trans fat the same); sodium "zero when the serving contains less
than 5 milligrams ... to the nearest 5-milligram increment when the serving contains 5 to 140 milligrams ... to the nearest 10-milligram
increment when the serving contains greater than 140 milligrams"; cholesterol "to the nearest 5-milligram increment"; protein and total
carbohydrate "to the nearest gram". The same paragraph says calorie factors "shall be applied to the actual amount (i.e., before rounding)",
and allows several methods (specific Atwater factors; 4, 4, 9; others). **A declared calorie figure need not equal 4-4-9 over the declared
grams; the gap is lawful.** It is counted as a property of the record, never as a violation.

Definitions, fixed now:
- *Food* = one element of the archive's top-level array of branded foods.
- *Declared value* = a nutrient's `value` inside the food's `labelNutrients` object (per serving). If no such object exists in the file,
  the registered grid counts cannot be made on printed values; the session then reports that, and reports per-100 g values multiplied by
  the serving size only as exploration.
- *On the grid* (exact, tolerance 1e-9): calories: 0, or ≤ 50 and a multiple of 5, or > 50 and a multiple of 10. Total, saturated, trans
  fat: 0, or < 5 and a multiple of 0.5, or ≥ 5 and whole. Sodium: 0, or 5-140 and a multiple of 5, or > 140 and a multiple of 10.
  Cholesterol: a multiple of 5 (0 included). Protein, carbohydrates, fiber, sugars: whole. Values 1-4 kcal, 0 < fat < 0.5, 1-4 mg sodium or
  cholesterol are off the grid (the law's alternatives for them are zero or a phrase, not a number).
- *Atwater gap* d = declared calories − (4 × protein + 4 × carbohydrates + 9 × fat), all declared, for foods declaring all four.
- Every count by `count1.py`, run once, after this file is pushed.

## The check, fixed now

The numbers are a firm's declarations relayed by a database; no reading by eye can verify the label itself (I cannot see a package).
The check is against an outside of my parsing: **twenty foods drawn with seed 20261027** from those with declared calories; for each,
FoodData Central's live API (`https://api.nal.usda.gov/fdc/v1/food/{fdcId}?api_key=DEMO_KEY`, one call per 2 s) is asked for its
`labelNutrients`, and calories, fat, sodium and protein are compared with the archive's. Agreement: equal on all four, or each difference
listed. A food updated or removed since the release is reported, not treated as an error.

## Instruments, chosen before (two)

- **T3 pragmatics audit**, its second use (project 2). A Nutrition Facts panel is an order-word in the strict sense (ATP 76-81): a law
  orders how a number is said, and the saying transforms a food incorporeally (a serving with 0.4 g of trans fat *is*, on the panel, a
  food with none). The audit's object is the panel's regime and the order-words that govern it (`AUDIT.md`). Failure (KsK T3): the
  translation test changes only the wording, not the project's design.
- **T4 minor-science heuristic, the working log as following-journal** (`LOG.md`), its thirteenth project. Written as it happens, `date -u`
  read at the moment, never ahead of it. Failure (KsK T4): written after the fact, or no deviation registered across the project.
- T1 is the practice-wide atlas; not chosen as a project instrument.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-18. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If `labelNutrients` is absent, the project's question moves to what the record does to a label, and session 2 is registered on that.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. The release holds at least 400,000 branded foods.
2. At least 85 % of foods carry a declared calorie value.
3. At least 90 % of declared calorie values are on the grid.
4. At least 90 % of declared total-fat values are on the grid.
5. At least 90 % of declared sodium values are on the grid.
6. Among foods declaring at least 50 calories and all of protein, carbohydrates and fat, the median |d| is at most 10 kcal.
7. Of declared trans-fat values, at least 80 % are exactly 0.
8. The live check agrees on at least 19 of 20.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, the check, the instruments' first entries, neighbours, a
first page if time allows.

*Data: U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, Branded Foods, release of 2026-04-30
(fdc.nal.usda.gov), CC0 1.0; read 2026-10-27 UTC. Modifications: counts computed from the declared label values as defined above;
nothing else.*

## Adversarial read, before commit

(a) The unit is a record, not a product sold: one product may appear in several records (a GTIN updated is a new record, per the field
descriptions), and a best-seller counts once like a regional jar. Duplicate GTINs are counted and reported, not removed. (b) An off-grid
number may be the database's doing (a value recomputed from per-100 g and back), not the firm's. The count cannot tell the two apart from
values alone; it reports how far off (fractions versus whole steps), and a firm's label is never called wrong here. (c) The grid tests
encode my reading of a long regulation; foods for infants, dual-column panels and supplements have other rules I did not read. Category
is counted beside the grid so a pocket shows. (d) P6 leans on 4-4-9, which the law allows but does not require; a large gap is a finding
about methods and rounding, not about honesty. (e) The release is one state of a database that changes twice a year; a later release is a
new count, not a correction. (f) What I know of `labelNutrients` is from training; if the file's keys differ, the first look at its
structure is logged as a detour before any count, and the count is written to the keys found, with the change stated.
