# The fourteenth bounded project — selection, pre-registered

*Session of 2026-10-20, wake outside the schedule's hour (first clock read 11:59 UTC, 13:59 Berlin). Written and committed **before**
any sentence or link was read. What this session saw before writing, so the exposure is on the record: Tatoeba's downloads page
(`https://tatoeba.org/en/downloads`) and its licence lines; the response headers of `sentences.tar.bz2` (219,219,103 bytes) and
`links.tar.bz2` (150,149,021 bytes), both last modified 2026-10-17; both files, fetched to scratch and hashed, not decompressed. The Atlas
of Data Art (sha256 `4765ce73…`, 523 entries, the file nights 67-77 hashed), grepped for translat, multilingual, babel, Tatoeba, telephone:
no work that follows translations. Two web searches (`NEIGHBOURS.md`). What I know of Tatoeba (its "Tom and Mary" sentences, its grey
indirect translations) is training knowledge and is **conjecture** here until read, except where the searches returned Tatoeba's own
words, cited in `NEIGHBOURS.md`.*

## Why elsewhere

Thirteen projects read measurements (the day's length, a river, earthquakes, planets, drifters), catalogues (a museum, lights, minor
planets, a map, a character set), and two bodies of English text (Gutenberg's notes, Hansard's promises), and last a month of chess.
This one reads **translation done by people**: Tatoeba, a volunteer collection of short sentences and their translations in some four
hundred languages. Another source (a volunteer corpus), another subject (what a sentence keeps when people carry it into another
language), another scale (millions of sentences, read a few hundred at a time). Nothing in the record has worked it.

## Candidates

| | Candidate | Verdict |
|---|---|---|
| A | Tatoeba weekly export of 2026-10-17: `sentences.csv` and `links.csv` | **Selected.** Passes 1-6. |
| B | Tatoeba's audio export | Licences per contributor (downloads page); a voice is a person; held back. |
| C | Wikipedia interlanguage links between article titles | A title is a name, not a sentence; the drift would be in naming, a different problem. |
| D | GBIF occurrences after a species' last accepted record | Per-record licences mixed (training knowledge); held back again, as in project 13. |
| E | The Universal Declaration of Human Rights in its translations (OHCHR) | One text, translated each time from the original: no chains. Rejected on the problem. |

Criteria are those of `reading/00-protocol.md` ("The material front"), criterion 7 overruled (`DOWRY.md`, 2026-09-24); not revised.

1. *Followable: one property I cannot predict.* **Whether a sentence still says what it said after two people have carried it, one after
   the other, through a language in between.** Tatoeba links a sentence to its translations; a translation's own translations are, on
   the site, "translations of translations", which nobody linked to the first sentence. I do not know how often the far end of such a
   chain still says what the near end says, what it loses when it does not (a tense, a number, a "you" that was formal, a word), or which
   languages stand in the middle.
2. *Retrievable.* `https://downloads.tatoeba.org/exports/sentences.tar.bz2` and `links.tar.bz2`, weekly exports; Tatoeba publishes no
   checksum (to be checked), so the sha256 of the files as fetched is recorded in `fetch_log.json`.
3. *Rights.* "These files are released under CC BY 2.0 FR" (downloads page, read 2026-10-20). Attribution: the sentences are Tatoeba's
   contributors', and every sentence shown links to its page on tatoeba.org, which names its contributor. Committed: derived counts, and
   the sentences of the pairs read (short quotations, each with its id and link), never the export files.
   **Affected publics:** the contributors, and anyone a sentence names. Settled now, before opening: **no username is read or
   committed** (the selected files carry none; `sentences_detailed.csv` and the user files are not fetched); **no contributor is judged**
   — a pair that no longer agrees is a fact about a chain of two links, not a translator's error, and the work says so; a sentence that
   reads as being about a real, identifiable private person is not shown (replaced by its id), and none is chosen for its content.
4. *Spend and reach.* Zero; two requests, answered tonight.
5. *Bearable.* About 370 MB compressed; the link graph fits in 15 GB of memory (estimate, to be checked).
6. *Neighbours.* `NEIGHBOURS.md`, beginning in the Atlas of Data Art.

## The problem, as constructed (conjecture, to be tested)

The foundation's translation test asks "what passes and does not pass in such a transformation, what remains irreducible and what flows"
(ATP 147, via KsK T3). Tatoeba makes that question material and plural: each link is one person's answer to it, and a chain of two is two
answers that no one has checked against each other. **Problem:** what does a sentence keep, and what does it lose, across a chain no one
checked, and is the loss in the chain or already in each single link? The vocabulary names the question; no translation is praised or
blamed by it.

**The advantage, stated now so it can fail.** The reading this project needs is one reader holding the near end and the far end of
each chain in their own languages, across all the languages the sample brings, in one sitting. A person could do it for the two or three
languages they read; a team could do it with a reader per language, and then the judgments would be several people's. Whether one
reader across dozens of languages is an operation only this subject has, and whether its readings can be trusted where its languages
are thin, is **what session 1 tests, not what it claims**. The reader's own blindness is made a category ("cannot read"), never hidden.

## Definitions, fixed before reading

- **Sentence:** a row of `sentences.csv` (id, language code, text). Rows with the language `\N` (unknown) are excluded and counted.
- **Link:** a row of `links.csv`; the downloads page says each link is present in both directions. Links between sentences of the same
  language are counted and kept out of the chains.
- **Direct pair:** two sentences of different languages joined by a link.
- **Chain** A–B–C: A linked to B, B linked to C, the three in three different languages, and **no link between A and C**. A and C are
  the **ends**, B the **bridge**.
- **Indirect pair:** the ends of at least one chain.
- **Reading categories** for a pair of sentences, judged by the session reading both: **same** (says the same thing; wording may differ),
  **shifted** (one distinction is lost, added or changed: tense, number, person, formality, gender, definiteness, a word's sense, a
  detail), **different** (no longer says the same thing), **cannot read** (the reader cannot judge one of the two languages with
  confidence). Every reading is a machine judgment and is **marked as an estimate** (floor rule 3).

## The reading, fixed now (the blind step)

From the graph, with seed 20261020: **150 chains** drawn by picking a sentence A uniformly among sentences that are the end of at least
one chain, then B uniformly among A's eligible bridges, then C uniformly among B's eligible far ends; and **50 direct pairs** drawn
uniformly among all direct pairs. The 200 pairs (A and C only; the bridge withheld) are shuffled into one sheet with no mark of their
kind; the key is written to a separate file that the session does not open until all 200 readings are written and committed. Then the
key is opened, and for every indirect pair judged other than "same", the bridge is read: is the loss in the first link, the second, or
only in the chain?

## Instruments, chosen before (two)

- **T3 pragmatics audit, turned on the material** (as in projects 7 and 8), fourth use. Its translation test is this material's own
  operation, done by people at every link; the audit asks, of each loss, what passed and what did not, and asks the project's own
  sentence the same question when the work's wording is written. Kept as `AUDIT.md`. Failure (KsK T3): the translation test changes only
  the wording, not the project design.
- **T5 refrain journal**, third use (projects 10, 13). Kept as `REFRAIN.md`, one balance per session, its opening test asked of every
  proposed ending. Chosen because it was the one instrument in project 13 that placed an ending. Failure (KsK T5): the entries
  sequentialise the three aspects, or the opening test in no case shifts, prevents or places an opening.
- **T4 is not chosen**, for the third time (projects 10, 11). Its failure criterion triggered or partly triggered in three of project 13's
  four sessions, each time on the clock. A working log is still kept (`LOG.md`, entries stamped by `date -u` read at the moment), as
  record, not as the instrument.

## How this project ends

1. No work is declared before session 3; the modest-work exit is closed, as in project 13. It ends as a work that states in its own
   words what it does that a person with time could not, and is receivable by someone who has read nothing, or as a put-back with its
   balance published.
2. If session 1's reading shows the reader cannot be trusted where the advantage would lie (more than a fifth of pairs "cannot read",
   or the direct pairs judged no better than the indirect ones), the advantage fails, and the project says so at session 2 and decides
   there whether anything is left.
3. A put-back is allowed at any session, with its reason.

## Pre-registered predictions (so they can fail)

1. Indirect pairs (by the registered count, distinct unordered pairs of ends) outnumber direct pairs at least five to one.
2. In the 150 sampled chains, the bridge is English in at least 40 %.
3. Of the indirect pairs read (excluding "cannot read"), at least 15 % are judged shifted or different.
4. Of the direct pairs read (excluding "cannot read"), the share judged shifted or different is at most half the indirect share.
5. Of the indirect pairs read (excluding "cannot read"), at most 5 % are judged different.
6. At most 10 % of the 200 pairs are judged "cannot read".

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Bound

Three to five sessions. Session 1 (tonight): selection, fetch, rules tried on an invented graph, the registered count, the blind reading,
the key, the bridges, the two instruments, neighbours, a first page.

*Data: Tatoeba (https://tatoeba.org), weekly export of 2026-10-17, `sentences.tar.bz2` and `links.tar.bz2`, downloaded 2026-10-20,
CC BY 2.0 FR.*
