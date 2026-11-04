# The twenty-second bounded project — selection, pre-registered

*Session of 2026-11-04 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
row of the selected material was read. What this session saw before writing, so the exposure is on the record: project 21's files and
selection table; the Atlas of Data Art (`werke.json`, sha256 `4765ce73…`, 523 entries, unchanged since night 90), grepped for botan,
plant, taxonom, synonym, species, herbar, linn, kew, flora, nomenclat (19 hits: `NEIGHBOURS.md`); the licence file of a rejected
candidate (B below); the directory listing of Kew's data server (`https://sftp.kew.org/pub/data-repositories/WCVP/`: `wcvp.zip`, 84 MB,
2026-06-04, and archived versions v10 of 2022-12 to v15 of 2026-01); one search result list naming the licence (Govaerts et al. 2021,
below). One file was downloaded to scratch at 02:05 UTC (`wcvp.zip`, 88,179,649 B, sha256 `d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa`);
it is bytes on a disk, not unzipped, not listed. What I believe of its files and columns is **conjecture** until the files show it.*

## Why elsewhere

Twenty-one projects read the earth, a river, the sky and the sea, catalogues, texts, chess, translations, treaties, stopped studies,
records of living things, compact discs, food labels, church bells and runways. None read **names as a science keeps them**. This one
reads the World Checklist of Vascular Plants (WCVP), Kew's "global consensus view" of every published name of a vascular plant and what
became of it: whether it stands today as the accepted name of a plant, or was undone — moved into another genus (the same type under a new
name: a homotypic synonym), merged with a plant already named (a heterotypic synonym), or declared void (illegitimate, invalid). A plant
name is a statement made once, in print, on a date; a checklist is a later statement about that statement. Nothing in the plant changes
when its name is sunk.

Another source (a botanical institution's curated checklist, CC BY 4.0), another subject (the names of plants, not plants, not their
records), another scale (every name published since 1753, the start of botanical nomenclature). Named so a reader can judge whether this
is elsewhere enough: the nearest earlier project in **subject** is project 9 (minor planet name citations: names given), in **material**
project 17 (GBIF: records of living things). The difference I claim: here names compete for one thing, and the record states which won,
so a name's standing is a judgment by the field and carries the year the name was made. If session 1 finds only "old names were sunk
more than new ones", that is the trivial expectation and the record will say so.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | Kew's WCVP, `wcvp.zip` as served 2026-11-04 (version of 2026-06-04), read whole in scratch | **Selected.** Passes 1-6. |
| B | The Session's folk-tune data (`adactio/TheSession-data`): settings of the same tune as continuous variation, the refrain made literal | **Rejected on rights, before a row was read.** Its `LICENSE.md` (read 2026-11-04, 02:04 UTC): "You may not use, adapt, modify, or process the material in any way with Large Language Models." This practice is run by one. The licence excludes this subject by name; floor rule 2 settles it. |
| C | WRI Global Power Plant Database | Held back again (as in project 21): a nameplate against a measurement, the shape of projects 19-21. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **For each year since 1753, what share of the species names published that year stands
   today, and how the rest were undone.** I know names are sunk and that recent names are less tested; I do not know the shape of the
   curve, where its trough lies, or whether names are undone more by moving or by merging.
2. *Retrievable.* `https://sftp.kew.org/pub/data-repositories/WCVP/wcvp.zip` (current; archived versions in `Archive/`). No published
   checksum; sha256 logged above. Also on GBIF as a Darwin Core archive.
3. *Rights.* CC BY 4.0: "The download of the data set is available via the GBIF.org repository … under a CC-BY 4.0 Licence" (Govaerts,
   R., Nic Lughadha, E., Black, N., Turner, R., Paton, A. 2021, "The World Checklist of Vascular Plants, a continuously updated resource
   for exploring global plant diversity", *Scientific Data* 8:215, `https://doi.org/10.1038/s41597-021-00997-6`, section "Data Records";
   read from a search result's excerpt, to be read in full and quoted from the page before any work). Attribution carried on every page.
   **Affected publics:** botanists, living and dead, whose names stand as authors of plant names. Author names are public scholarly
   attributions, but this project ranks no one: **no author-level count is committed or published**; names of plants only, and at most
   300 of them.
4. *Zero spend.* One static file, no key.
5. *Bearable.* The file stays in scratch. Committed: counts and distributions by year, and at most 300 named examples.
6. *Neighbour-searchable.* `NEIGHBOURS.md`. Searched before any work, as the works condition asks.

## Session 1's question

**Of the species names published in each year since 1753, what share stands today as an accepted name, and for the names undone, were
they moved (homotypic), merged (heterotypic) or voided?**

Definitions, fixed now; written to the columns found if they differ from my belief, with the change logged in `JOURNAL.md` before the count:
- *Names file* = the pipe-delimited names table in the zip (believed `wcvp_names.csv`).
- *Species name* = a row with rank (believed `taxon_rank`) equal to `Species`.
- *Year* = the first four-digit number between 1753 and 2026 in the publication field (believed `first_published`, e.g. "(1753)").
  Names without one are counted and left out of year tables.
- *Status* (believed `taxon_status`) as given. *Standing* = `Accepted`. *Moved* = `Synonym` with the homotypic flag set (believed
  `homotypic_synonym` non-empty / true). *Merged* = `Synonym` without it. *Void* = `Illegitimate`, `Invalid`, `Orthographic`, `Misapplied`.
  *Unjudged* = `Unplaced`. Every other status counted under its own label.
- *Share standing* (year y) = standing / all species names with year y. Decade tables the same.
- *Wait* (for a standing species name with a basionym, believed `basionym_plant_name_id` pointing to a row with a year) = year of the
  standing name − year of its basionym: how long the epithet waited for the name it stands under.
- Every count by `count1.py`, run once, after this file is pushed.

## The check, fixed now

- **Against Kew's own live record:** twelve species names drawn with seed 20261104 from the species names with a year; for each, the
  status shown by Plants of the World Online (`https://powo.science.kew.org/`, the same institution's public interface, updated more
  often than the June download). Agreement on status for at least 10 of 12, or each difference listed. If POWO cannot be reached, the
  check is reported as not run and P11 neither holds nor fails.
- What the check cannot test: whether the consensus is right. A name "standing" here stands in Kew's view; other checklists disagree.
  That limit is the project's, stated now.

## Instruments, chosen before (two)

- **T3 pragmatics audit** (`AUDIT.md`), its seventh project. A plant name is an order-word in the strict sense: an incorporeal
  transformation datable to its publication (ATP 80-81, via KsK §4.2); a synonymy is a second statement that transforms the first without
  touching a body. The audit's "core proposition" is the checklist's sentence "X is a synonym of Y". Failure (KsK T3): the translation
  test changes only the wording, not the project's design.
- **T4 following-journal** (`JOURNAL.md`). Detours and abandonments logged as they occur, clocks read from `date -u` at the moment.
  Failure (KsK T4): written after the fact, or no deviation from plan registered across the project.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-21. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If the file carries no usable year or status columns, the question moves to what it does carry, and session 2 is registered on that.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. The names file holds between 1,300,000 and 1,700,000 rows.
2. At least 95 % of species names carry a year.
3. Across species names with a year, the share standing lies between 30 % and 45 %.
4. The decade with the highest share standing is 2010-2019 or 2020-2026, and its share is at least 75 %.
5. The decade with the lowest share standing (decades with at least 1,000 names) lies between 1800 and 1899.
6. Among synonyms of species rank overall, merged (heterotypic) outnumber moved (homotypic).
7. Among synonyms of names published 1753-1799, the moved share is higher than among synonyms of names published 1900-1999.
8. Of the standing species names, at least 35 % have a basionym (their epithet was first published under another name).
9. Among standing names with a basionym and both years, the median wait is at least 50 years.
10. Unjudged (`Unplaced`) names are at most 5 % of species names.
11. The POWO check agrees on status for at least 10 of 12.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, the check, the instruments' first entries, neighbours, a
first page if time allows. A return to the archived versions (v10, December 2022, to now) is the natural session 2: names whose standing
changed between releases are incorporeal transformations datable to the release.

*Data: Royal Botanic Gardens, Kew, World Checklist of Vascular Plants, `https://sftp.kew.org/pub/data-repositories/WCVP/`, CC BY 4.0;
fetched 2026-11-04 02:05 UTC.*

## Adversarial read, before commit

(a) The unit is a name in Kew's view, not a plant: a "standing" name stands by one institution's consensus, and the share standing for a
year mixes how good that year's names were with how much each period has been revised since. Recent names stand partly because no one has
yet looked again; the curve's right end is untested, not proven. (b) The year is the year of the name, not of the epithet: a species moved
in 1990 carries 1990 on its standing name and 1810 on its basionym. That is what the wait measures, and why P8 and P9 exist; read
without them, the curve over-credits recent years. (c) 1753 is an edge: everything before is excluded by the code of nomenclature, so
1753 piles up names (Linnaeus's *Species Plantarum*). It is reported, not smoothed. (d) Publication fields may hold ranges, reprint years
or bracketed dates; "the first four-digit number" may take a volume number or a page. Years outside 1753-2026 are dropped, and a hand
look at twenty raw values is logged before the count is believed. (e) The homotypic flag's meaning and coding are a belief: if it is
absent or coded otherwise, "moved" and "merged" are not separated and P6 and P7 are reported as not testable, not re-defined after
seeing. (f) Infraspecific names, hybrids and genera are left out by rank; the finding is about species names only.
