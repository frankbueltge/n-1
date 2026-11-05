# Project 22, session 2 — the verdicts that changed, pre-registered

*Session of 2026-11-05 (Berlin), the schedule's wake (first clock read 02:02 UTC, 03:02 Berlin). Written and committed **before** any
row of the archived releases was read. What this session saw before writing, so the exposure is on the record: session 1's files and
results (`session1.json`, `explore1.json`, `AUDIT.md` entry 1); the directory listing of Kew's archive
(`https://sftp.kew.org/pub/data-repositories/WCVP/Archive/`, read 02:03 UTC: `wcvp_v10.zip` 2022-12-08, `wcvp_v11.zip` 2023-10-04 15:40,
`wcvp_v12.zip` 2023-10-04 15:58, `wcvp_v13.zip` 2025-05-29, `wcvp_v14.zip` 2025-07-03, `wcvp_v15.zip` 2026-01-07, and their Darwin Core
twins). Seven files were downloaded to scratch at 02:03 UTC — bytes on a disk, not unzipped, not listed:*

| release | file | bytes | sha256 |
|---|---|---|---|
| v10 | `Archive/wcvp_v10.zip` | 84,920,344 | `47bfccb291a3e9fc76addbaf697ac25404df5666e0dc1556eaa894269d2ce867` |
| v11 | `Archive/wcvp_v11.zip` | 85,429,528 | `65040ae34532d16c3a0683e004e41ef27c905f21a728f78ef4a8f919703b6087` |
| v12 | `Archive/wcvp_v12.zip` | 102,696,144 | `073a7677156669771e67b8118d7b006028a5735716437aa343f18ca8d8da20e7` |
| v13 | `Archive/wcvp_v13.zip` | 103,958,565 | `198ff3100db16e27c51632b70448faf2bb8ff2c1994ea27efde7e7602ade73bb` |
| v14 | `Archive/wcvp_v14.zip` | 105,093,449 | `ab4af48d24b25d2494e74558823253986f8d75603a04967568dabbf9c317285d` |
| v15 | `Archive/wcvp_v15.zip` | 89,508,082 | `693e05b31ea6ce724c88ccf38bb964db2f22424b396f7ed1fd04fdb203af7e81` |
| v16 | `wcvp.zip` (current) | 88,179,649 | `d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa` (= session 1's) |

What I believe of the archived files — that each holds a pipe-delimited `wcvp_names.csv` with the columns session 1 found — is
**conjecture** until the files show it.

## Why this, after session 1

Session 1 counted one release and found a curve: what share of each year's species names stand today. Its audit (entry 1, continued)
moved the question from *how much* stands to *in what form*: whole (accepted), as an epithet passed on (moved: a homotypic synonym, its
epithet alive in another name), or gone (merged into a plant named before, or voided). Session 1 could only see the verdicts as they stand
on one date. Seven releases over three and a half years let each change of verdict be **dated to a release**: the incorporeal
transformation (ATP 80-81, via KsK §4.2) caught between the two statements that bracket it. Nothing in any plant changed in those years.

## Session 2's question

**Between December 2022 (v10) and June 2026 (v16), which species names changed their form in Kew's view, in which direction, and
whose names were they — of which years?**

Definitions, fixed now; written to the columns found if they differ from my belief, with the change logged in `JOURNAL.md` before the
count:
- *Names file* = the pipe-delimited names table in each zip (believed `wcvp_names.csv`). Columns as in session 1 (`plant_name_id`,
  `taxon_rank`, `taxon_status`, `homotypic_synonym`, `first_published`, `place_of_publication`).
- *Identity* = `plant_name_id`. A name is the same name across releases if and only if its id is the same. Names are matched by id
  only, never by spelling.
- *Kind* (per release) as in session 1, with the flag coding learnt there fixed now: *standing* = `Accepted`; *moved* = `Synonym` with
  `homotypic_synonym` stripped and upper-cased in {`T`, `TRUE`}; *merged* = `Synonym` otherwise; *void* = `Illegitimate`, `Invalid`,
  `Orthographic`, `Misapplied`; *unjudged* = `Unplaced`; any other status its own label.
- *Form* = three of the kinds collapsed: *whole* = standing; *passed on* = moved; *gone* = merged or void. Unjudged and other labels stay
  as they are.
- *Species name* = `taxon_rank` = `Species` in **both** releases compared. Names that change rank are counted and set aside.
- *Year* = as in session 1 (the first four-digit number 1753-2026 in `first_published`), read from **v16** (or from the latest release
  holding the name, for names gone by v16).
- *Changed* (between two releases) = present as a species name in both with a different kind.
- *Step* = two consecutive releases (six steps, v10→v11 … v15→v16).
- *Reversal* = a species name present in all seven releases whose kind changes at least twice and whose v16 kind equals an earlier kind
  it had left.
- *Publication* = `place_of_publication` as given (the book or journal, without volume or page).
- Every count by `count2.py`, run once, after this file and the script are pushed.

## Pre-registered predictions (so they can fail)

1. At least 98 % of v10's species-name ids are present as species names in v16.
2. Of the species names present in both v10 and v16, between 1 % and 5 % changed kind.
3. Standing → not standing (moved, merged or void) outnumbers not standing → standing between v10 and v16.
4. Among names standing in v10, the share no longer standing in v16 is higher for names published 2000-2022 than for names published
   1800-1899.
5. Among standing → synonym changes (v10 to v16), moved outnumbers merged.
6. At least 10 % of v10's unjudged species names carry a verdict (any kind other than unjudged) in v16.
7. The share standing among species names with a year differs between v10 and v16 by less than one percentage point.
8. The single publication with the most changed names (v10 to v16) holds less than 5 % of all changed names.
9. Of the six steps, the one with the most changed names is v12→v13 (the longest interval, October 2023 to May 2025).
10. At least 5,000 species names in v16 with a year of 2022 or earlier are absent (by id) from v10 — names added to the record after
    the fact.
11. Fewer than 0.1 % of species names present in all seven releases show a reversal.
12. **The check:** twelve changed names (v10 to v16), drawn with seed 20261105, looked up in Kew's WCVP deposit on GBIF (dataset
    `f382f0ce-323a-4091-bb9f-add557f3a9a2`, open species API, one request per 2 s), as session 1's substitute did. For each, which of the
    two statuses (v10's or v16's) GBIF shows. Registered as information, not as a pass mark: GBIF's copy has its own release date, so
    the check says which release the deposit follows, and no prediction rests on it. Plants of the World Online is not asked again
    (session 1 met a bot challenge, not to be circumvented).

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Instruments (chosen in session 1, continued)

- **T3** (`AUDIT.md`, entry 2): the order-word now has a date. Translation test: a verdict per name becomes a flow between forms per
  release. Failure (KsK T3): the translation test changes only the wording, not the project's design for session 3.
- **T4** (`JOURNAL.md`): detours logged as they occur, clocks read from `date -u`.

## Adversarial read, before commit

(a) **Ids may not be stable.** If Kew re-issued ids between releases, "changed" undercounts and "added" overcounts; P1 measures it, and
the count reports how many v10 ids vanish. A name whose id changed is two names here; that is the stated limit. (b) **A change of kind
is not always a taxonomic act.** Data repairs (a status corrected, a flag filled in where it was blank) look like verdicts. The flag in
particular may have been coded differently in older releases (empty instead of `T`); so moved ↔ merged changes are reported apart from
changes across the standing line, and if the flag's raw values differ by release, that is logged before the count is believed. (c)
**Releases are not dated acts.** A change seen between v12 and v13 happened at some date in a nineteen-month gap, entered by an editor;
the release dates bracket it, nothing narrower. (d) **v11 and v12 were posted the same afternoon** (listing, 15:40 and 15:58): the
v11→v12 step may be a re-issue, not an interval; reported as found. (e) **The year is read from v16**, so a corrected publication year
does not move a name between decades across releases. (f) **Twelve sampled names cannot check the whole**; the GBIF look-up checks only
that the changes are not artefacts of my parsing.

*Data: Royal Botanic Gardens, Kew, World Checklist of Vascular Plants, releases 10-16, `https://sftp.kew.org/pub/data-repositories/WCVP/`,
CC BY 4.0 (Govaerts et al. 2021, *Scientific Data* 8:215); fetched 2026-11-05 02:03 UTC.*
