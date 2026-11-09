# Project 23, session 2 — the hours the file showed wrong, pre-registered

*Session of 2026-11-09 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). Written and committed **before**
`count2.py` was run on any release. What this session saw before writing, so the exposure is on the record: session 1's files and
results (`session1.json`, `explore1.json`, `explore1b.json`, `explore1c.json`, `check1.json`, `JOURNAL.md`); the neighbour's index page
and its 2025 page (`https://tzdata-meta.timtimeonline.com/`, `.../metadata/2025`, read 02:03 UTC); IANA's tz page
(`https://www.iana.org/time-zones/tz-link`, the paragraphs on notice); the article it points to, Matt Johnson-Pint, "On the Timing of
Time Zone Changes" (`https://codeofmatt.com/on-the-timing-of-time-zone-changes/`, published 2016-04-23, modified 2018-11-11), read in
full. The same 276 tarballs were downloaded again to scratch at 02:04 UTC (the container of session 1 is gone): **sha256 of their
concatenation in name order `69c85cb0ffb4aef86077c4f8d9f54cd2f403be3ca007bc8dcbd4a9c00ef34d01`, equal to session 1's prefix
`69c85cb0…`** — the same material. The listing holds no release newer than 2026f.*

## Why this, after session 1

Session 1 timed each change of a region's clock by the first release that carried it, and found three kinds of lateness: news arriving
after the clocks moved, a change already carried but at another moment (re-timing), and the record correcting its past more than a year
later. Its check found the second kind inside the first. A count of transitions cannot weigh them: one late transition may leave a file
wrong for an hour or for a year.

So the unit changes from the transition to **the hour**. On every day since 1997 one release was the newest; that is the file anyone
updating faithfully would have had. Session 2 asks: **for how many hours, in which zones, did the then-newest release show an offset
for the present moment that the newest release of all (2026f) now says was wrong — and of which kind was each error?** This is not the
neighbour's question. `tzdata-meta` records, by hand, for changes since 2016, when the tz list was told and when a release followed, and
is "limited to changes affecting UTC offsets for current and/or future timestamps at the time that notice is first received" (its own
words) — the past rewritten is outside it by scope. This counts, by machine, every hour since 1997 the file was wrong about the present,
including the hours it was only later found to have been wrong about.

## Definitions, fixed now

- *Releases*: the 275 tarballs except `tzdatabeta`, named and dated as in session 1 (`NEWS` of 2026f). Compiled as in session 1 with
  this machine's `zic -b fat`, **with session 1's helper `helper/yearistype` on the path** — exploratory in session 1, registered now.
  Releases that still fail are counted and left out. Order: by (date, name).
- *Life* of release R_i: from its date (00:00 UT) to the date of R_{i+1}; the last compiled release, 2026f (= *final*), has no life
  counted. *Window*: 1997-01-01T00:00Z to 2026-11-07T00:00Z, as in session 1.
- *Zones*: those of the final release (`Zone` lines, without `Etc/`), as in session 1.
- *Offset*: UT offset of zone Z in release R at instant τ, read from R's compiled file (full file, all transitions; before the first
  transition the first local-time type).
- *Wrong instant*: τ in the window and in the life of the release R current at τ, Z exists in R, and offset_R(Z, τ) ≠
  offset_final(Z, τ). *Absent*: Z not in R — counted apart, never wrong.
- *Episode*: a maximal run of wrong instants of one zone, joined across consecutive lives if contiguous. Start τ0, end τ1, hours =
  (τ1 − τ0)/3600.
- *Correction*: the first release after the one current at τ0 whose offset at τ0 equals the final's. *Lag* = its date − τ0, in days.
- *Kind* of an episode, decided in this order:
  1. **past rewritten** — lag > 365 days;
  2. **re-timed** — the release current at τ0 carries a transition t_R, and the final a transition t_F, to the same offset,
     |t_R − t_F| ≤ 31 days, and [τ0, τ1) lies between them: the same change, carried at another moment;
  3. **news** — every other episode: the change was not in the file at all when the clocks moved.
- *Error*: |offset_R − offset_final| over the episode (constant within an episode or the episode's largest).
- *Exposure*: zone-hours in the window during which the zone existed in the current release.
- Every count by `count2.py`, run once, after this file is pushed.

## Measures

Zone-hours wrong (all, and by kind); episodes and distinct zones (by kind); zone-hours by year of τ0 and kind; the error distribution
weighted by hours; the share of exposure; news episodes grouped into *events* (same correction release, start within two days).

## The check, fixed now

Twelve episodes drawn with seed 20261109 from all episodes; for each, the midpoint τm: `zdump -v` (not count2's TZif reader) on the
release current at τm and on the final; holds if both offsets equal count2's and differ from each other. At least 11 of 12.

## Pre-registered predictions (so they can fail)

1. Exactly 252 releases compile with the helper (session 1's exploratory run).
2. Zone-hours wrong lie between 200,000 and 5,000,000.
3. The past-rewritten kind carries more than 70 % of zone-hours wrong.
4. Re-timed episodes carry fewer zone-hours than news episodes.
5. Between 60 and 200 distinct zones have at least one episode.
6. Zone-hours wrong are between 0.1 % and 3 % of exposure.
7. The median length of news episodes lies between 1 and 30 days.
8. The longest episode exceeds 365 days.
9. News zone-hours with τ0 in 2017–2026 are under 10 % of all news zone-hours.
10. At least 90 % of zone-hours wrong are wrong by exactly one hour.
11. The `zdump` check holds for at least 11 of 12.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## What this cannot say

How many people were affected, or whether any device showed the wrong hour: no population and no device is in this material. The
release date is the day a file was published; a device received it later (IANA's page: updates "may take substantial time to reach end
users"). Every hour counted here is therefore a lower bound on a device's error and an upper bound on the database's own speed — the
hours a perfectly updated machine would have been wrong. Whether the final release is right about the world is not tested: "wrong" means
wrong by the database's latest word.

## Adversarial read, before commit

(a) The final release is not the truth; it is the latest verdict. An episode can be "wrong" only because 2026f changed its mind about a
past it had right before. That is the past-rewritten kind, and it is reported as the record's revision, not as anyone's error on the day.
(b) A zone split from another (session 1's "arrived with its zone") is absent before its arrival, not wrong; after, its own history may
differ from what the parent zone's file showed on the day — that difference is not counted, because the zone did not exist. A
population-weighted reading would see it; this one cannot. (c) The re-timed test may mistake two unrelated changes within 31 days for one;
DST transitions to the same offset recur at most twice a year, so a match within 31 days is rarely chance. (d) The 1996h–2000e releases
compile only through a helper written by this practice; a wrong helper would show as episodes at the even/odd-year rules in 1997–2000.
If the episodes of 1997–2000 cluster on rules typed even/odd, the record says so. (e) The window starts in 1997 but the first compiled
release is from 1996: hours before 1996h's date are outside every life.
