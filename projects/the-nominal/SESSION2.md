# Project 20 — session 2, pre-registered: where between the keys do rings stand, and what holds them there?

*Session of 2026-10-30 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
row of this session's count was read. Exposure on the record: everything session 1 counted and explored (`session1.json`,
`explore1.json`), among them the tenor's distance from its named note by casting era (22-29 cents from the 1350s to the 1900s, 15 in the
1950s, 11 in the 2000s) and its histogram in 10-cent bins. The three files were fetched again to scratch at 02:04 UTC (session 1's scratch
did not survive): `bells.csv` 12,676,738 B, sha256 `8c9985fb09ae…6302192`, **identical** to session 1's; `towers.csv` 4,207,547 B,
`33b5493e…` (107 B longer than session 1's, so changed since); `founders.csv` 62,712 B, `dfcf1261…`. Looked at before writing, as
structure: the three header lines; the shapes of `towers.csv`'s `TuneYr` (digits masked: 14,375 empty, 1,346 four-digit years) and of
`bells.csv`'s `Founder` (letters masked); and `founders.csv` rows matching Taylor, Mears, Whitechapel, Gillett, Eijsbouts (its `Group`
column holds the foundry a founder belongs to, e.g. "Whitechapel", "Gillett", "Loughborough"). One page read for pitch standards
(Wikipedia, *Concert pitch*, `https://en.wikipedia.org/wiki/Concert_pitch`, read 02:06 UTC) and one web search on bells and tuning forks
(two results, neither about English founders' pitch).*

## Where session 1 left the question

Inside a ring, bells agree with their tenor to a median 4.5 cents; the ring itself stands a median 22 cents from the note it is named
by, nearly what random pitch would give, until the 1950s. A ring is a pitch of its own that a record of named notes has no place for.
Session 1 measured that distance from the *named* note. This session measures it from nothing the record says: **where in the gap
between two equal-tempered semitones (A = 440) a ring's tenor stands**, as a position on a circle of 100 cents, and asks whether
anything holds rings at a common position — an era, a foundry, a pitch standard of the concert hall.

Why a standard might: Britain's concert life ran on the Philharmonic Society's "old philharmonic pitch", about A = 452 Hz (A = 452.4 at
60 °F), until it was "replaced in 1896 by the considerably lower new philharmonic pitch of A = 439 Hz"; France fixed A = 435 Hz in 1859;
the 1939 conference recommended A = 440 Hz, adopted as ISO 16 in 1955 (all quoted from the Wikipedia page above). On the 100-cent circle
these sit at **+48.1** (452.4 Hz), **−3.9** (439), **−19.8** (435) and **0** (440). Old philharmonic pitch stands almost exactly
between two keys. That founders tuned church bells to any of these is **conjecture**: I have found no source saying so, which is why it
is a prediction and not a premise.

## The question

**Do rings' positions between the keys cluster, and if they do, is the cluster an era's pitch standard or a foundry's house pitch?**

## Definitions, fixed now

- *Ring*, *tenor*: as in `explore1.py`: a `Ring ID` of a full-circle ring whose rows hold exactly one bell whose `Bell Role` equals the
  ring size's first token; it counts if that tenor has a nominal.
- *Position* o of a frequency f (cents, on a circle of 100): o = ((1200·log2(f/440) + 50) mod 100) − 50, in [−50, 50). As an angle,
  θ = 2π·o/100. No named note enters it.
- *Ring position* = the tenor's o. (Session 1 found the ring's inside agrees with its tenor to a median 4.5 cents.)
- *Circular mean* μ = the angle of the mean of e^{iθ}, read back in cents; *concentration* R̄ = its length (0: spread evenly; 1: all at
  one point). *Rayleigh p* (Zar's approximation): p = exp(√(1 + 4n + 4(n² − (nR̄)²)) − (1 + 2n)).
- *Tuning year* of a ring = `towers.csv` `TuneYr` for the row whose `RingID` is the ring's, where it is a four-digit year; else the
  tenor's cast year (first four-digit year of `Cast Date`, as in session 1). Both counts are reported. A ring with neither is left out
  of the era counts.
- *Foundry* of a ring = the `Group` in `founders.csv` of the row whose `Name` equals the tenor's `Founder` exactly; rings whose tenor has
  `Founder Uncertain` set, or a founder not found, are left out of the foundry counts. If `Group` is empty, the founder's `Name` stands
  as its own foundry.
- Every count by `count2.py`, run once, after this file is pushed.

## The check, fixed now

An inside check, not an outside one (session 1 checked the nominals against Dove's tower pages, 20 of 20): `towers.csv` carries its own
`Hz` per ring. For every counted ring whose tower row has a positive `Hz`, the tenor's nominal from `bells.csv` is compared with it;
agreement within 0.5 Hz. Reported as a share; disagreements are counted, the first ten listed by ring id only. This tests my join of the
two files and my choice of tenor, not the bells.

## Pre-registered predictions (so they can fail)

1. Across all counted rings, positions are not spread evenly (Rayleigh p < 0.001), but weakly held: R̄ ≤ 0.25.
2. Rings with tuning year 1950 or later: R̄ ≥ 0.5, and μ within ±10 cents of 0 (A = 440).
3. Rings with tuning year 1850-1899: R̄ ≥ 0.2, and μ within ±12 cents of +48.1 (old philharmonic pitch, wrapped: a μ of −50 to −45 counts
   as within).
4. Rings with tuning year before 1800: R̄ ≤ 0.10 (no standard held them).
5. Of the foundries with at least 30 rings whose tuning year is 1880-1949, at least two thirds have Rayleigh p < 0.01 (a house pitch).
6. Among those, the circular means of "Loughborough" and "Gillett" differ by more than 10 cents (two houses, two pitches). If either has
   fewer than 30 rings in that span, P6 is reported as not testable.
7. Of rings with a `TuneYr`, at least 30 % have a tenor cast 50 or more years before it (old bells retuned).
8. The inside check agrees on at least 95 % of rings with a tower `Hz`.

Predictions are reported as registered, and again after any verified correction. Any failing is a result. Places (county, country) are
not registered; any reading of them is exploration after the count, labelled so.

## Adversarial read, before commit

(a) The position circle is A = 440's. A standard of 452.4 Hz and one a semitone away are the same point on it; the circle cannot tell
old philharmonic pitch from a key 52 cents flat of a 440 note. That is the circle's purpose here, and its blindness. (b) `TuneYr` is
the tower's latest tuning; a ring tuned in 1880 and again in 1960 counts as 1960, a ring never recorded as tuned counts by its tenor's
cast year, which may be centuries before the pitch it sounds now (session 1's (b)). The era counts mix both; both are reported. (c) A
ring augmented later keeps its old tenor; its position is the old bell's. (d) Founders' pitch practice is conjecture; a cluster near
+48 would be consistent with the old philharmonic pitch, not proof of it: a founder's own fork could sit there for another reason.
(e) Foundry by exact name match may lose founders spelled differently in the two files; the count of rings lost is reported. (f) P3 and
P5 are the bold ones and I expect at least one of them to fail; P2 is close to what session 1 already showed (the tenor 11 cents from
its named note in the 2000s) and is weak for that reason.

*Data: Dove's Guide for Church Bell Ringers, Central Council of Church Bell Ringers (`https://dove.cccbr.org.uk/`), CC BY-SA 4.0
(`https://creativecommons.org/licenses/by-sa/4.0/`); files fetched 2026-10-30 02:04 UTC. Changes: positions, concentrations and counts
computed as defined above; nothing else. No substantial part of the database is committed (`SELECTION.md`, criterion 3).*
