# Project 19 — session 2, pre-registered: does the serving size decide which lawful numbers survive the record?

*Session of 2026-10-28 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin, winter time). Written and committed
**before** any row of this session's count was read. Exposure on the record: everything session 1 counted and explored
(`session1b.json`, `explore1.json`, `explore1b.json`, `explore1c.json`): among them the on-grid rates by data source (LI 72.7 %, GDSN
58.5 %, NZGDSN 10.8 %, Euromonitor 13.0 %), the categories with the highest off-grid calorie rates (honey 88.9 %, tomatoes 87.1 %, milk and
milk substitutes 86.2 %), and the three-digit round-trip classes. The archive was downloaded again to scratch (session 1's scratch did not
survive): 204,270,542 B, sha256 `57b0f122e61cf2840f03c11e9520275d0d2018dc036e16273fcd3cd370db2256`, equal to the prefix session 1 logged;
unzipped, not read. `count2.py` was run once on a synthetic table of 200 made-up foods to check it runs; that output was discarded.*

## Where session 1 left the question

Session 1 found that the record does not keep the panel: most off-grid calorie values are a lawful number sent to per 100 g (kept whole)
and back with three significant digits kept. That reading was found after the count and is a fit, not documentation. If it is the
record's one operation, then **whether a label's lawful number survives into the record is decided before any firm or law speaks, by
the arithmetic of the serving size alone**: 150 kcal on 100 g returns 150; 150 kcal on 145 g goes to 103 per 100 g and comes back as
149. That is testable on every food without looking at its declared value, and it is what this session tests.

## The question

**Does the serving size alone predict, food by food, whether a declared calorie value is on the law's grid; and where it does not,
which records are not the round trip's?**

## Definitions, fixed now

For every food with a declared calorie value *v* (`labelNutrients.calories.value`), an energy amount *a* per 100 g (`foodNutrients`,
nutrient number 208, kcal) and a serving size *s* > 0 whose unit is g or ml (`g`, `ml`, `grm`, `mlt`, any case): a *testable food*.
*Source* = `dataSource`, read as LI or other.

- *on*: *v* is on the grid of `count1.py` (`grid_cal`).
- *consistent*: *v* = sig3(*a* · *s* / 100), sig3 as in `explore1c.py` (three significant digits).
- *g*: *v* if on, else the grid number nearest *v* (`explore1.py`, `grid_points`).
- *ghost*: *g* reproduces the stored *a*: |*g* · 100 / *s* − *a*| ≤ half of *a*'s last decimal unit.
- *predicted*: from *g* and *s* only, never *v* or *a*: *a′* = *g* · 100 / *s* rounded half up to a whole number; predicted on if
  sig3(*a′* · *s* / 100) = *g* (and always if *g* = 0).
- *Class D* = off, consistent, no ghost: a value the record computed from a per-100 g amount that no lawful number explains.
- Total fat (204) and sodium (307) get *on*, *consistent* and *ghost* the same way, with their own grids.
- Every count by `count2.py`, run once, after this file is pushed.

## The check, fixed now

Twenty testable LI foods drawn with seed 20261028 from the parsed archive; for each, FoodData Central's live API (`DEMO_KEY`, one call per
4 s) is asked for the food; declared calories, serving size and the 208 amount are compared with the archive's (`check2.py`).
Agreement: all three equal after rounding both sides to one decimal (session 1 saw the live service give 8.0 where the archive holds
8.01, a difference that may be the service's output; conjecture); exact equality reported beside. Refusals for rate are reported as
refusals, not as disagreement, and are not re-asked inside the registration.

## Predictions (so they can fail)

1. **The arithmetic decides.** Among testable LI foods, *predicted* agrees with *on* for at least 97 %.
2. **On the grid by luck, not by keeping.** Among testable LI foods on the grid, at least 95 % are consistent.
3. **Where the arithmetic cannot displace.** Among testable LI foods with *g* ≥ 100 and *s* ≤ 100, at least 97 % are on the grid.
4. **Where three digits show a tenth.** Among testable LI foods with 10 ≤ *g* < 100, at most 60 % are on the grid.
5. **Class D is the other sources'.** Of class D, at least 25 % is from sources other than LI (they hold 6.0 % of declared calories).
6. **Fat the same.** Among testable LI foods with total fat on the grid, at least 95 % are consistent.
7. **Sodium the same.** Among testable LI foods with sodium on the grid, at least 95 % are consistent.
8. **The check agrees** on at least 19 of 20.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Instruments (as chosen in `SELECTION.md`)

- **T3** entry 2 is written before the count (`AUDIT.md`).
- **T4**: the log is written in session, `date -u` read at the moment.

## Adversarial read, before commit

(a) P1 is close to circular where *v* is consistent and ghosted: *predicted* then recomputes what the record computed. It is not circular
where the record holds a panel number it did not compute (on but not consistent) or a per-100 g amount no lawful number explains
(class D): those are exactly the records P1 can fail on, and they are counted separately. (b) "Rounded half up" for *a′* is my reading;
the database may round half to even or truncate. Half-way cases are rare (*g* · 100 / *s* exactly *k* + 0.5) and the disagreements are
listed by example, so a rounding-mode effect would show as a pattern in them. (c) *s* in ml is treated as if 100 ml were the per-100
base, which I believe but have not read; liquids could carry their energy per 100 g with a density. If so, beverages will fail P1 and
show in the serving-size table. (d) P5 leans on a conjecture: that other sources supply per-100 g values from labels written under other
laws. The count can only say where class D sits, not why. (e) A food is a record; the record may have been updated after the label was
read, and nothing here judges a firm.

*Data: U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, Branded Foods, release of 2026-04-30
(fdc.nal.usda.gov), CC0 1.0; read 2026-10-28 UTC. Modifications: counts computed from the declared values as defined above.*
