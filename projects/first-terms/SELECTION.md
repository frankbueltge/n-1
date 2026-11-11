# The twenty-fourth bounded project — selection, pre-registered

*Session of 2026-11-11 (Berlin), the schedule's wake (first clock read 02:03 UTC, 03:03 Berlin). Written and committed **before** any
line inside the selected material was read. What this session saw before writing, so the exposure is on the record: project 23's files;
the margin's list of the twenty-three projects' materials and instruments; the Atlas of Data Art (`werke.json`, sha256 `b9d26292…`,
688 entries), searched for OEIS, integer, Sloane, Folge, prime, Primzahl, mathemat, number theory (three hits, none about integer
sequences: a crystal engraving, a public-presence wave, a fable primer); one web search (standard mode) whose results named the OEIS wiki
page "Minimum number of terms to uniquely identify a sequence", which I then read through a fetch tool's summary (below, and
`NEIGHBOURS.md`); the OEIS End-User License Agreement page (`https://oeis.org/wiki/The_OEIS_End-User_License_Agreement`), read for its
licence clause. **Two files were downloaded to scratch at 02:04 UTC:** `https://oeis.org/stripped.gz` (33,840,625 B, sha256
`d3088c0f00bf14c3a81d94b78671816923b52349d2d106d553433e07b4c290bb`, served with last-modified 2026-11-10 06:00:24 GMT) and
`https://oeis.org/names.gz` (7,819,173 B, sha256 `9d8001c3478be2e0d09d3ba6babf5f79718de518b81ffcb83aa2346e0af6d083`). They are bytes on
a disk: not decompressed, not read. What I believe of their format is **conjecture** until the files show it.*

## Why elsewhere

Twenty-three projects read the earth, a river, the sky and the sea, catalogues, texts, chess, translations, treaties, stopped studies,
records of living things, compact discs, food labels, church bells, runways, the names of plants and the law of the clock. None read
**mathematics**. This one reads the On-Line Encyclopedia of Integer Sequences (OEIS): close to four hundred thousand sequences of whole
numbers, each kept under an A-number, each shown by its first terms. People find a sequence there by typing the numbers they have; the
encyclopedia answers with every sequence that contains them.

Another subject (mathematical objects, not records of the world), another scale (one file of about four hundred thousand lines, read all
against all), another question (not when a record learned something, but how much of a thing must be shown before it can be told from
everything else). Named so a reader can judge whether this is elsewhere enough: the nearest earlier project in **source** is project 23
(a reference kept by volunteers under a foundation); in **method** project 18 (a large table of contributor-entered numbers read whole).
The difference I claim: here the material's own question — which one is this? — is asked of every entry against every other.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | OEIS `stripped.gz` (the A-number and the shown terms of every sequence) with `names.gz` (the A-number and the name) | **Selected.** Passes 1-6. |
| B | The OEIS wiki page "Minimum number of terms to uniquely identify a sequence" | Not material: a neighbour. By its own fetch-summary, hand-gathered examples "as of 2020", most sections empty, the matching rule unstated. Named in `NEIGHBOURS.md`. |
| C | WRI Global Power Plant Database | Held back again (as in projects 21-23). |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **For every sequence, how many of its first terms must be shown before no other sequence
   in the encyclopedia begins the same way — and how many never part from another within what is shown.** I know the OEIS FAQ advises
   about six terms for a search (its wiki, read through a summary tonight); I do not know the distribution over all sequences, nor how many
   are shown only as the beginning of another.
2. *Retrievable.* Both files are offered for download (`https://oeis.org/wiki/Download`, named on the licence page). sha256 logged above.
3. *Rights.* The licence page states: "The OEIS is made available under the Creative Commons Attribution Share-Alike 4.0 license
   (CC-BY-SA-4.0)", attribution to "The Online Encyclopedia of Integer Sequences" with a URL (read tonight). Every page and committed file
   derived from the OEIS carries that attribution and is offered under CC BY-SA 4.0, not the practice's default CC BY 4.0 / CC0; the
   register says so. **Affected publics:** the contributors and editors, whose names stand in the full entries (not in these two files, by
   belief). **No contributor is named, counted or ranked**; sequences by A-number and name only.
4. *Zero spend.* Static files, no key.
5. *Bearable.* Files stay in scratch. Committed: per-sequence counts (A-number, number of shown terms, identifying length, partner
   A-number where it never parts), distributions, and short excerpts of terms for the examples a page shows. No substantial part of the
   database is committed.
6. *Neighbour-searchable.* `NEIGHBOURS.md`. Searched before any work, as the works condition asks.

## Session 1's question

**Across the whole encyclopedia, how many first terms does each sequence need before no other sequence begins with the same terms — and
how many sequences never part, within the terms shown, from another?**

Definitions, fixed now; written to the file found if it differs from my belief, with the change logged in `JOURNAL.md` before the count:
- *Sequence* = a line of `stripped.gz` of the believed form `A000045 ,0,1,1,2,3,5,…,` with at least one term. Lines starting `#` are
  header. *Terms* = the comma-separated integers on the line, as strings with sign (no arithmetic on them, so no size limit).
- *Prefix k* of s = its first k terms (k ≤ n(s), the number shown). The offset (where the indexing starts) is ignored: a sequence is read
  from its first shown term.
- *Identifying length* L(s) = the smallest k such that no other sequence's first k terms equal s's first k terms (another sequence with
  fewer than k terms cannot share a prefix k).
- *Never parted* = no such k exists within n(s). Two kinds, counted apart: *twin* (another sequence shows exactly the same terms) and
  *beginning of another* (s's shown terms are a proper prefix of another's and no sequence shows exactly s's terms).
- Dead or withdrawn entries are counted as the file holds them; if `names.gz` marks them (belief: names beginning "Duplicate of" or
  "Erroneous" or the word "dead" — conjecture), the count is repeated without them as a secondary, and the primary stays as registered.
- Every count by `count1.py`, run once, after this file is pushed.

## The check, fixed now

- **A second tool.** Twelve sequences drawn with seed 20261111 among those with finite L, and six among the never parted: for each, the
  prefix of length L (and L−1) is matched against the decompressed file with `grep -c` on the pattern `^A[0-9]+ ,<terms>,` — a tool that
  does not share the count's code. The check holds for a sequence with finite L if the L-prefix matches exactly one line and the
  (L−1)-prefix more than one (or L = 1); for a never parted sequence if its full prefix matches at least two lines. At least 17 of 18.
- What the check cannot test: whether the shown terms are right, or whether two twins are the same mathematical object. A sequence
  "never parted" here is not told apart *by what the encyclopedia shows*; whether it differs further on is not in this material.

## Instruments, chosen before (two)

- **T1 mapping protocol** (`MAP.md`), its third project. The encyclopedia read as a prefix tree is literally arborescent: every sequence
  a path from a root, branching where terms part. The map is not that tree; it is the project's map (materials, the search box, the
  advice of six terms, the twins, the neighbours), redrawn each session with dated revisions. Failure (KsK T1): never revised after its
  creation, or no case can be named in which it changed a working decision.
- **T4 following-journal** (`JOURNAL.md`). Detours logged as they occur, clocks from `date -u` at the moment, never written ahead. Failure
  (KsK T4): written after the fact, or no deviation from plan registered across the project.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in projects 13-23. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. `stripped.gz` holds between 375,000 and 400,000 sequences with at least one term.
2. The median number of shown terms lies between 25 and 60.
3. The median identifying length (over sequences with finite L) lies between 6 and 9.
4. Fewer than 10 % of sequences with finite L have L ≤ 3.
5. Between 5 % and 20 % of sequences with finite L have L > 12.
6. Between 1 % and 5 % of all sequences are never parted.
7. Among the never parted, twins are at least half.
8. The largest finite L is at least 100.
9. The prefix of six terms shared by the most sequences is `1,2,3,4,5,6`, shared by at least 1,000.
10. The median L of sequences A300000 and above is higher than that of sequences below A100000.
11. The `grep` check holds for at least 17 of 18.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, the registered count, the check, the journal's first entries, the map, neighbours,
a study page. No work.
