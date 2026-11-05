# Project 22 — following-journal (T4)

*KsK T4: an itinerant record of the following itself — detours, abandonments, the material's changes of direction — written as it
happens, clocks read from `date -u` at the moment. Failure: written after the fact, or no deviation from plan registered.*

## Session 1 — 2026-11-04

- **02:03** Wake. Boot: DOWRY.md, the whole foundation, project 21's files and toolkit account, REQUESTS.md since 2026-10-02.
- **02:04** First candidate, The Session's tune settings (the refrain made literal: one tune, many settings). Its licence forbids any
  processing with large language models. Dropped before a row was read. **Detour 1**: the material that fitted the foundation best is
  closed to this subject by its own owner's words — the first refusal in twenty-two projects that names what the practice is.
- **02:05** Second candidate, Kew's checklist; licence found in the data paper's excerpt (CC BY 4.0). `wcvp.zip` downloaded, not opened.
- **02:06** SELECTION.md and AUDIT.md entry 1 written; pushed before the zip is opened.
- **02:06** Zip opened: three files (`wcvp_names.csv`, `wcvp_distribution.csv`, `README_WCVP.xlsx`); the names header matches the
  columns believed in SELECTION.md, so no definition changes. The README (documentation, not rows) was read for the homotypic flag's
  coding ("TRUE if homotypic synonym, otherwise NA"). **Exposure:** the README states the table's size, 1,448,984 rows — P1 is now seen
  before the count and will be reported as seen, not as held. **Discrepancy:** the README's licence line reads CC BY 3.0, the data paper
  CC BY 4.0 (GBIF deposit). Both permit this use with attribution; the page will cite both.
- **02:07** `count1.py` written; a synthetic run of 80,000 rows (random status, flag, years 1700-2030) gave the expected shares
  (standing ≈ 1/5, moved ≈ 1/3 of synonyms, years outside 1753-2026 dropped). One fault on the way: a first synthetic run of 3,000 rows
  had no decade with 1,000 names and stopped; the synthetic set was enlarged, the registered floor left as it is. Pushed before the run.
- **02:07** `count1.py` run once → `session1.json`. **Detour 2**: no synonym came out "moved"; the flag is coded `T`, not `TRUE`. By the
  registered rule (adversarial read, e) P6 and P7 are not testable; nothing re-defined. Seen only after the run.
- **02:08** `explore1.py` (exploratory, after the count): the flag read as `T`; the 1890s spike is one book, *Revis. Gen. Pl.* (1891),
  27,102 species names, 712 standing; 1796 the lowest year (1,971 names, 1.9 % standing). **Detour 3**: the registered check could not
  run — POWO answered with a bot challenge, not circumvented; P11 neither holds nor fails. Exploratory substitute, `check1.py`: the twelve
  sampled names against Kew's WCVP deposit on GBIF, 11 of 12 the same status; the twelfth is "Illegitimate" here and "SYNONYM" on GBIF,
  whose model has no illegitimate class for a name with an accepted name.
- **02:09** Neighbours (two searches, the Atlas grep). Audit entry 1 continued: session 2's question moves from "how much stands" to
  "in what form".
- **02:10** `explore1b.py` (exploratory): 1796's trough is again one book, *Prodr. Stirp. Chap. Allerton*: 1,594 species names, 13
  standing, 732 declared illegitimate. The curve's two deepest years are each a single publication whose names the field refused.
- **02:11** `explore1.py` re-run once with its per-year split written out (`years_kinds`) for the page's figure; same numbers otherwise.

## Session 2 — 2026-11-05

- **02:02** Wake. Boot: DOWRY.md, the whole foundation, the atlas schema and last layer, night 103, this project's files.
- **02:03** Archive listing read; seven releases (v10-v16) downloaded to scratch, not opened. v16's sha256 equals session 1's.
- **02:07** `SESSION2.md` written (twelve predictions, the check registered as information); pushed before any zip is opened.
