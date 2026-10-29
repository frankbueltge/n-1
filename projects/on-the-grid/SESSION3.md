# Project 19 — session 3, pre-registered: the panels restored

*Session of 2026-10-29 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
row of this session's count is read and before any outside answer is asked. Exposure on the record: everything sessions 1 and 2 counted
and explored (`session1b.json`, `session2.json`, `session2_cells.json`, `explore1*.json`, `explore2.json`), among them that all but 116 of
416,781 LI calorie values are the per-100 g amount sent back to the serving (decimal, half to even), and that 21,036 calorie values come
from a per-100 g amount no lawful number produces (class D). The archive was downloaded again to scratch (sha256 `57b0f122…`, equal to
sessions 1 and 2) and unzipped, not read. One Open Food Facts product was fetched to learn the API's field names (`0038000138416`): its
`data_sources_tags` include `database-usda` and its `nutrition_data_per` is `100g`; I did not look at whether its numbers agree with
FoodData Central's. That one record is why the check below excludes Open Food Facts entries imported from USDA.*

## Where session 2 left the question

The database keeps no Nutrition Facts panel. It keeps a per-100 g amount and says the panel's number again from it, and the portion
decides whether the lawful number comes back as itself (80) or a hair beside it (80.1). `AUDIT.md` entry 2 fixed, before session 2's
count, the rule for tonight: if the arithmetic decides (it did, under the record's rounding), session 3 asks **whether a work restores
the panels**: inverts the record, rather than showing the displacement once more. The inversion is now possible to state exactly, and so
is what it cannot reach.

## The question

**From what the record holds (a per-100 g amount and a serving size), can the number printed on each label be given back, uniquely; and
do the numbers given back agree with the packages where someone outside the database has read them?**

## Definitions, fixed now

For every *testable food* as in `SESSION2.md` (declared calorie value *v*, energy amount *a* per 100 g, nutrient 208, serving size *s* > 0
in g or ml; source read as LI or other):

- *Preimage* P(*a*, *s*) = every number *g* on the law's calorie grid (0, 5-50 by 5, 60 and above by 10, up to 9,990) with
  |*g* · 100 / *s* − *a*| ≤ half of *a*'s last decimal unit (`decimals_unit`, as in sessions 1 and 2), computed in decimal.
- *Restored*: P has exactly one member, *r*. *Ambiguous*: two or more. *Unrestorable*: none.
- *Kept*: restored and *r* = *v*. *Given back*: restored and *r* ≠ *v* (the record's number is not the label's, and the label's is
  recoverable). Unrestorable is session 2's class D read from the other side (class D also required *v* consistent; unrestorable does
  not).
- Total fat (204, grid of `count1.py`, up to 299 g) and sodium (307, up to 99,990 mg) get P, restored, ambiguous, unrestorable the same way.
- Every count by `count3.py`, run once, after this file is pushed.

## The check, fixed now: the packages as people copied them

FoodData Central's own live service cannot check this (it holds the same record; `DEMO_KEY` refused 19 of 20 in session 2). The outside
reading is **Open Food Facts** (`https://world.openfoodfacts.org/api/v2/product/{code}.json`, ODbL), where people and apps type a
package's panel from the package or its photograph. Its USDA import is the same record and is excluded.

- *Pool*: testable LI foods with a `gtinUpc` of 8-14 digits. Drawn with seed 20261029 (`count3.py` writes the lists): **300 given back**
  and **100 kept** (*v* on the grid). *Code* = `gtinUpc` without leading zeros, left-padded with zeros to 13 digits (to 8 if it has 8 or
  fewer digits).
- One call per 1.0 s, `User-Agent` naming this repository, fields `code,nutriments,nutrition_data_per,data_sources_tags` only; a refusal
  or error is reported, asked again once after 5 s, never counted as disagreement.
- *Answered*: the product exists, `nutrition_data_per` is `serving`, `energy-kcal_serving` is a number, and no tag in
  `data_sources_tags` contains `usda`. Only answered foods are compared.
- *Agree*: equal within 1e-6. For given-back foods, both *r* = OFF and *v* = OFF are counted; for kept foods, *v* = OFF.
- Committed: FDC IDs, codes, the three outcomes (answered, *r* = OFF, *v* = OFF) and the reason a food was not answered. **Open Food
  Facts' own values are not committed** (ODbL against this practice's CC0 for data; they are re-retrievable at the code).

## Predictions (so they can fail)

1. **Restorable.** Among testable LI calorie values, at least 93 % are restored (one lawful number exactly).
2. **Not ambiguous.** At most 0.5 % are ambiguous.
3. **The work's share.** Among restored LI calorie values, at least 20 % are given back (*r* ≠ *v*).
4. **The restoration does not move what was kept.** Among restored LI calorie values with *v* on the grid, at least 99 % have *r* = *v*.
5. **Sodium the same.** Among testable LI sodium values, at least 90 % are restored.
6. **The packages agree with the restoration.** Of answered given-back foods, *r* equals Open Food Facts' number for at least 70 %.
7. **The packages disagree with the record.** Of the same foods, *v* equals Open Food Facts' number for at most 10 %.
8. **Control.** Of answered kept foods, *v* equals Open Food Facts' number for at least 70 %.

Predictions are reported as registered, and again after any verified correction. Any failing is a result. Fat is counted and reported
without a prediction (I do not know how its per-100 g amounts are stored).

## How this session ends (rule 1 of `SELECTION.md`: work or put-back)

**The work is declared if** P1 holds, at least 20 given-back foods are answered, and P6 and P7 both hold. Otherwise the project is put
back with its balance; the form below is not redesigned after seeing. Session 4 is not taken for this project either way, unless the
check could not be made (fewer than 20 answered), in which case its reason is written before it is taken.

**The work, if declared — *As Printed*** (`works/as-printed/`): one page.
- *The panels.* 96 foods drawn with seed 20261029 from the given-back LI foods, each drawn as a small Nutrition Facts panel in the
  panel's own typography (rule, title, serving, Calories, Total Fat, Sodium), every number the restored lawful one where it is restored;
  beneath each number the database's own, small and grey, where it differs ("database: 149"). Then 24 unrestorable foods, drawn by the
  same seed, with the calorie line left as a gap and the database's number beneath it ("no number the law allows gives this"). Each
  panel names the food as the database describes it (`description`, never the brand) and links to its FoodData Central page.
- *The whole.* One bar of all testable calorie values, LI and other: kept, given back, ambiguous, unrestorable; the check's result; a
  table readable without the picture.
- Nothing is fetched while it is looked at except a FoodData Central page a visitor opens.

**The advantage, stated so it can fail.** A shopper reads one panel; a nutrition database keeps none. The work inverts the database's
own arithmetic, at its own decimal rounding, for every label it holds, and gives back the number that was printed; it names exactly the
labels it cannot give back. A person with time, the archive and the rounding rule could do the same; the claim is that the inversion is
whole and exact, and it is small. It **fails** if P6 or P7 fails: then the numbers given back are not the packages', and the page would
be a second rounding laid over the first.

## Instruments (as chosen in `SELECTION.md`)

- **T3** entry 3 is written before the count (`AUDIT.md`); it judges entry 2's failure criterion: did the rule "restore rather than
  show" change session 3's design, or only its wording?
- **T4**: `LOG.md`, `date -u` read at the moment.

## Adversarial read, before commit

(a) Open Food Facts is not the package: a contributor may type the database's number, or a number from a newer package; agreement with
*r* over *v* is evidence, not proof, and disagreement may be the package changed. (b) Excluding `usda`-tagged entries may not exclude every
copy of FDC's numbers (an app may have taken them from FDC); if so, *v* = OFF rises and P7 can fail for that reason; the tags of answered
foods are summarised so the reason shows. (c) `nutrition_data_per = serving` is the last state of the product, and Open Food Facts may
store a per-serving number it computed; if its `energy-kcal_serving` carries decimals, that is reported. (d) The pool is LI foods only
because the work's claim is about the main source's arithmetic; other sources are counted, not checked. (e) P1 is close to certain if P(*a*,
*s*) is the inverse of session 2's arithmetic; it can fail on the per-100 g amounts stored with decimals, where the tolerance is narrow and
a lawful number may miss it. (f) A label printed under another rule (dual columns, infant food) has another grid; it shows as
unrestorable, not as wrong. (g) No firm is named on the page; a given-back number says what the database did, not what a firm did.

*Data: U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, Branded Foods, release of 2026-04-30
(fdc.nal.usda.gov), CC0 1.0; read 2026-10-29 UTC. Check: Open Food Facts (openfoodfacts.org), ODbL 1.0, asked live; its values are
compared, not kept. Modifications: counts computed from the declared values as defined above.*
