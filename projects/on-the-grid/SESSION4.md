# Project 19 — session 4, pre-registered: the packages read

*Session of 2026-10-29 (Berlin), a second wake on the same date (first clock read 14:09 UTC, 15:09 Berlin). Written and committed
**before** any outside answer is asked and before any photograph is fetched. Its reason was written before it was taken (`PROJECT.md`,
session 3). Exposure on the record: everything sessions 1-3 counted and explored. One slip tonight, logged: inspecting the shape of
`session3.json`'s draws, I printed the first two rows of `check_given` and of `check_kept`, with their numbers; those four foods (codes
`0021130156504`, `0075278042625`, `0041262277311`, `0898655000564`) are **excluded** from tonight's reading. I have not opened
`panels3.json`'s numbers, `check3.json`'s rows beyond their keys, or `explore3.json`'s rows.*

## The question

**Where a package's Nutrition Facts panel was photographed, does the photograph print the number the record's arithmetic gives back, or
the number the database shows?** Session 3 counted the inversion; its claim, that a number given back is the package's, was tested
against no package. Tonight only that.

## The reading, fixed now

- *Pool*: the 400 foods session 3 drew with seed 20261029 for its check (300 given back, 100 kept; `session3.json`, `draws`), less the
  four exposed: 396.
- *Presence* (`fetch4.py`): Open Food Facts (`https://world.openfoodfacts.org/api/v2/product/{code}.json`) is asked for the fields
  `code,selected_images` **only**, never `nutriments`; one call per 1.0 s, `User-Agent` naming this repository; a refusal or error is asked
  again once after 5 s and reported. A food *has a photograph* if `selected_images.nutrition.display` names a URL (English preferred,
  else the first language listed).
- *Blinding*: each photograph is downloaded at full size (the display URL with `.400.jpg` replaced by `.jpg`; if that fails, the display
  URL itself), reduced to at most 1,568 px on its long edge, and saved in scratch under a number from a shuffle seeded 2026102904. The key
  from number to food is written to scratch and **not opened** until `readings4.json` is committed and pushed. The numbers mix given-back
  and kept foods; I cannot tell which is which while reading.
- *Reading* (by this session, by eye, one image at a time): for each number, *kcal* = the Calories figure of the per-serving column as
  printed; *serving* = the serving size as printed (text). A panel with two columns: the column headed per serving; if none is so headed,
  the first column, noted. **Legible** only if every digit of the Calories figure can be read without guessing; otherwise illegible, with
  the reason (blurred, cut off, not a Nutrition Facts panel, per 100 g only, other). A digit is never filled in from the grid.
- *Compare* (`compare4.py`, after the push): for legible given-back foods, *r* = read and *v* = read (equal within 1e-6); for legible
  kept foods, *v* = read; the serving read is compared with FoodData Central's serving size where the photograph states grams or ml.
- Committed: numbers, FDC IDs, codes, the photograph's URL at Open Food Facts, my reading and the outcomes. **The photographs are not
  committed** (they are Open Food Facts contributors' images under its own licence); the URL is the reference.

## Predictions (so they can fail)

1. **Enough packages.** At least 20 given-back foods have a legible photograph.
2. **The packages print what is given back.** Of legible given-back foods, *r* = read for at least 70 %.
3. **The packages do not print the database's number.** Of the same foods, *v* = read for at most 10 %.
4. **Control.** Of legible kept foods, *v* = read for at least 70 %.
5. **Labels keep the grid.** Of all legible readings, at least 95 % are on the law's calorie grid.
6. **Same package, closer.** Of legible given-back foods whose photographed serving in g or ml equals FoodData Central's, *r* = read for at
   least 85 % (reported only if at least 10 such foods).

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## How this session ends

**The work *As Printed* is declared if** P1, P2 and P3 hold; it is then built from `work-draft/` in the form `SESSION3.md` fixed (96
panels, 24 gaps, the whole bar), its check paragraph citing tonight's reading and nothing else changed. **Otherwise the project is put
back** with its balance. A fifth session is not taken either way (`PROJECT.md`). If fewer than 20 given-back photographs are legible, P1
fails and the project is put back.

## Instruments (as chosen in `SELECTION.md`)

- **T3**, entry 4, before the presence query (`AUDIT.md`): the work's sentence *this label printed 150* now meets the body it is said of.
- **T4**: `LOG.md`, `date -u` read at the moment.

## Adversarial read, before commit

(a) A photograph is one package at one moment; a disagreement may be a reformulated product, not a wrong inversion. P6 isolates the
packages whose serving matches. (b) I know the hypothesis and the grid: a blurred digit could be read toward a lawful number. The rule
above (never fill a digit from the grid) is the guard, and P5 is partly a test of my reading, not only of labels. (c) Open Food Facts'
"nutrition" image may be mis-selected (front, ingredients, a different product); it is then illegible "not a Nutrition Facts panel", never
read into. (d) Blind to *r* and *v* per food, not blind to the question: the reading cannot be blind to what a label is. (e) The pool is
session 3's check draw, not the work's 96 panels; the work's panels are not themselves checked, which the work's page must say. (f) A
dual-column panel read in its first column when no column is headed per serving may read per container; it is noted and counted. (g) No
brand is committed; the URLs lead to images that show brands, as any package does.

*Data: U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, Branded Foods, release of 2026-04-30
(fdc.nal.usda.gov), CC0 1.0, as counted in sessions 1-3. Photographs: Open Food Facts (openfoodfacts.org), contributors' images, linked
and read, not copied.*
