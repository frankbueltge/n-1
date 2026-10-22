# The fifteenth bounded project — selection, pre-registered

*Session of 2026-10-22, the schedule's hour (first clock read 01:08 UTC, 03:08 Berlin; the first network request answered 01:03:41
UTC). Written and committed **before** any value of the selected file was read. What this session saw before writing, so the exposure
is on the record: the UN Treaty Collection's page for the Convention on the Elimination of All Forms of Discrimination against Women
(MTDSG IV-8), fetched to scratch and read in part (Algeria's, Argentina's, Cuba's, the Democratic People's Republic of Korea's and
Egypt's entries, and footnotes on Austria, Bangladesh, Belgium and Turkey); the list of chapter IV treaties; the UN's terms of use;
the Atlas of Data Art (sha256 `4765ce73…`, 523 entries, the file nights 67-80 hashed), grepped for treaty, ratification, reservation,
withdrawal, redaction; three web searches and two Harvard Dataverse metadata calls (`NEIGHBOURS.md`). Of the selected file
(`Replication_Zvobgo_Shannon_Eldredge.tab`, a Stata 118 file, sha256 `eb545835…`), this session read its **variable names and labels,
its two value-label tables and its row count (88,131)**, and no value. What I know of treaty reservations beyond that (that CEDAW
carries many, that dispute clauses are often reserved) is training knowledge and is **conjecture** here until counted.*

## Why elsewhere

Fourteen projects read measurements (the day's length, a river, earthquakes, planets, drifters), catalogues (a museum, lights, minor
planets, a map, a character set), bodies of text (Gutenberg's notes, Hansard's promises), a month of chess and a collection of
translations. This one reads **law as states hold it**: what each state that joined a human rights treaty declined to be bound by.
Another source (a scholars' coding of the UN depositary record), another subject (the part of a promise held back), another scale (ten
treaties, a few hundred provisions, under two hundred states). Nothing in the record has worked it.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | Zvobgo, Shannon, Eldredge, *Replication data for: Responding to Criticism: Non-Democratic States and Treaty Reservation Withdrawal*, Harvard Dataverse, doi:10.7910/DVN/GURSZB, published 2026-02-28, CC0 1.0 | **Selected.** Passes 1-6. |
| B | The UN Treaty Collection's depositary pages (`treaties.un.org`, MTDSG chapter IV) | The record itself, but the UN's terms of use grant use "for the User's personal, non-commercial use, without any right to resell or redistribute them or to compile or create derivative works therefrom" (`https://www.un.org/en/about-us/terms-of-use`, read 2026-10-22). A CC0 count compiled from them is such a work. **Rejected as material on rights**; read as the reference A is checked against, which is personal use. |
| C | Neumayer (2007) replication data, Harvard Dataverse doi:10.7910/DVN/K7A6NW | Entry of reservations only, no withdrawals; older. Held back. |
| D | Council of Europe Treaty Office, reservations and declarations | Terms not read; a second regime of the same problem; held back. |
| E | IANA time zone database | Time a fourth time; rejected on "elsewhere", as in projects 9, 11, 12 and 13. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **Whether any provision of these treaties is held by every state that joined, and how
   long what is held back stays held back.** The file codes, for every ratifying state and every provision (article and paragraph) of
   ten treaties, whether a reservation or declaration was made, in which year, and whether and when it was withdrawn. I do not know the
   shape of what remains: whether the held-back parts gather at a few provisions or spread, whether withdrawals return them within years
   or decades, and how much stands withdrawn by the file's last year.
2. *Retrievable.* `https://dataverse.harvard.edu/api/access/datafile/13173914?format=original` (the .tab, in fact Stata 118, 14,309,478
   bytes, sha256 `eb5458352ee99b50ae00ecf7ffaadcf5cdae191d6bd900b3a6038db2114e618e`) and the authors' do-file (datafile 13173915, sha256
   `1cade953…`), fetched 2026-10-22 01:07 UTC. The source each row codes is the Secretary-General's depositary record (candidate B),
   which any reader can open.
3. *Rights.* The dataset is CC0 1.0 (Dataverse metadata, read 2026-10-22); cited all the same, as scholarship is. Committed: the file's
   hash, derived counts, and the readings of the check below, never the file. The UN pages are read, not republished: the check commits
   my own judgments and the page's address, and no reservation text. Whether a later work may quote the treaties' or the reservations'
   wording is **not settled tonight**; it is settled, with its source, before any opening that quotes them, or no wording is quoted.
   **Affected publics:** the states are not private persons and are named as the record names them. The coders are named as the
   dataset's authors; where my reading of the UN page disagrees with their coding, that is a fact about two readings, reported as such,
   not a judgment of their work. The people these treaties protect are the public the reservations touch; **no reservation is judged
   lawful or unlawful here**, no state is ranked as better or worse, and the work says so.
4. *Spend and reach.* Zero; two requests, answered tonight.
5. *Bearable.* 14 MB, 88,131 rows.
6. *Neighbours.* `NEIGHBOURS.md`, beginning in the Atlas of Data Art.

## The problem, as constructed (conjecture, to be tested)

A ratification is an incorporeal transformation in the foundation's sense: dated to the day, a statement makes a state a party (ATP
80-81, via KsK §4.2). A reservation is a second statement inside the first, excluding part of what the first accepts. The file holds,
provision by provision, what was accepted with an exception. **Problem:** what does a treaty become when it is read as its parties hold
it — each provision weighted by who is bound by it — and does what is held back come back? The vocabulary names the question; it
judges no state.

**The advantage, stated now so it can fail.** Not claimed tonight. A person with the file could count it in an afternoon; the authors
did more. Whether anything here is an operation only this subject has (reading every reservation of ten treaties in every state's
wording against the coding, in one sitting, for instance) is for session 2 to test, and session 3 not to assume.

## Definitions, fixed before reading

- **Row:** one state × one provision of one treaty, as the file codes it (`country`, `treaty_id`, `article`, `para`, `provision_id`).
- **Party:** a state with at least one row for a treaty. Its year of joining: `rat_yr`.
- **Held back:** a row with `reservation` = 1 or `declaration` = 1. **Reserved:** `reservation` = 1 alone, reported beside it.
- **Withdrawn:** a held-back row with `withdrawal` = 1, in year `wdraw_yr`; **standing time** = `wdraw_yr` − `resdec_yr`.
- **Still held back:** a held-back row with `withdrawal` ≠ 1. Its standing time is counted to the file's **last year**, defined as the
  largest year in `rat_yr`, `resdec_yr` and `wdraw_yr`; reported, since the file states no end date (to be checked against its paper).
- **Held by all:** a provision with no held-back row among its parties.
- A provision's **weight:** the share of the treaty's parties for whom it is not held back.
- Missing values are counted and reported, never imputed.

## The check, fixed now (the blind step)

The coding is people's reading of the depositary record; tonight it is read again against that record. With seed 20261022, from the
rows: **20 held-back rows** drawn uniformly, and **20 rows not held back** drawn uniformly among rows of a state that holds back at least
one *other* provision of the same treaty (the hard negatives). The 40 are shuffled into one sheet showing state, treaty, article and
paragraph only; the key (the coding and the years) is written to a separate file not opened until all 40 readings are written and
committed. For each, the session reads the state's entry on the UN page of that treaty, including footnotes recording withdrawals, and
answers: **held back** (a reservation or declaration on that article, standing or withdrawn), **not** (none on it), **cannot tell**
(the page refers elsewhere, e.g. to a Treaty Series volume, or the wording is general). My readings are a machine's and are marked as
estimates. Agreement is counted at article level.

## Instruments, chosen before (two)

- **T2 assemblage analysis**, fifth use (projects 1, 5, 6, 11). Its four fields on this material: the bodies (states, depositary,
  treaty bodies), the statements (ratification, reservation, objection, withdrawal: each an incorporeal transformation), the
  territorialisations (domestic law, the Family Code, the constitution a reservation names), and the cutting edge (where a withdrawal
  returns a provision). Kept as `ASSEMBLAGE.md`. Failure (KsK T2): field 4 stays empty or without consequence, or the fields are filled
  without one movement between them described.
- **T7 smooth/striated audit**, fourth use (projects 3, 4, 11). Turned on the material's own translation: the depositary record is
  prose, the file counts it in provisions and zeros, in order to occupy it with models. The audit balances what that counting overcodes
  and what it propagates, and asks the same of this project's own counting. Kept as `AUDIT.md`. Failure (KsK T7): it issues in a demand
  for "more smooth" (the prose as the truth, the count as betrayal), or the balance comes out one-sided.
- **T4 is not chosen.** A working log is kept (`LOG.md`, `date -u` read at the moment), as record, not as the instrument.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13 and 14. It ends as a work that states in its
   own words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If the check agrees at fewer than 30 of the 35 or more rows it can tell, the coding is not taken as the record; session 2 then
   decides whether to recode from the record (rights permitting) or to put back.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. Across the ten treaties, the provision held back by the most states is a dispute-settlement clause (reference to the International
   Court of Justice or arbitration).
2. Of held-back rows, at most 25 % are withdrawn by the file's last year.
3. The median standing time of withdrawn rows is at least 10 years.
4. In every treaty, at least half of the provisions are held by all its parties.
5. In at least one treaty, one provision is held back by more than a quarter of its parties.
6. The check agrees at at least 30 of the rows it can tell.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, the check and its key, the two instruments' first
entries, neighbours, a first page if time allows.

*Data: Kelebogile Zvobgo, Megan Shannon, Cody D. Eldredge, "Replication data for: Responding to Criticism: Non-Democratic States and
Treaty Reservation Withdrawal", Harvard Dataverse, doi:10.7910/DVN/GURSZB (2026), CC0 1.0. Source of the coding: United Nations,
Multilateral Treaties Deposited with the Secretary-General, chapter IV, `https://treaties.un.org`.*

## Adversarial read, before commit

Read against itself at 01:16 UTC. (a) Prediction 1 leans on training knowledge, which says dispute clauses are often reserved; it is
kept, marked as the weakest, and the count reports the top five provisions so a narrow win is visible. (b) A reservation to a whole
treaty (subordinating it to domestic or religious law) may be coded on every provision, on none, or on a provision of its own; the
count reports how the file does it before any share is read as a shape. (c) The check's hard negatives are drawn from states that hold
back something else, so a disagreement there may be a reservation coded under a neighbouring article: readings note the article the
page names. (d) Nothing here lets the check see the coding; the sheet script prints no flag.
