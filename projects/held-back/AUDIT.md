# Project 15 — T7 smooth/striated audit, turned on the material's translation

*KsK T7: "in a smooth space-time one occupies without counting, whereas in a striated space-time one counts in order to occupy" (ATP
477); translation is double-faced, it can overcode or give "a milieu of propagation" (ATP 486-487). Failure: the audit demands "more
smooth", or its balance comes out one-sided.*

## Session 1 — 2026-10-22

**The two spaces.** The depositary record is prose: a state's entry, its footnotes, other states' objections, elisions marked "[...]"
where a withdrawn text stood. The file counts it: one row per state and provision, a zero or a one, a year. The scholars counted in
order to occupy, with models of why states withdraw (`Replication_Zvobgo_Shannon_Eldredge.do`, heckprobit on `withdrawal`).

**What the counting overcodes (found tonight, each with its evidence).**
- *Scope.* All 72,396 coded rows are of function "5. obligation" (`session1.json`; value-label table lists ten functions). The dispute
  clauses, the treaty-body clauses, the procedure are not in the file. Prediction 1 failed on exactly this: it asked the count about
  something the count had already subtracted. The record's most-reserved provision may be a dispute clause; the file cannot say.
- *Generality.* The general part of a reservation that names a constitution and a religion (Brunei Darussalam, CEDAW; its specific part names 9 (2)
  and 29 (1)) is not spread over the provisions it may cover (check item 6, coded 0 on 9 (1)); a general declaration that names a range of articles (articles 1 to 16 declared not
  self-executing, United States, CAT) is (item 12, coded 1 on 8 (4)). The count keeps what names articles, and loses what names a law.
- *Time.* The file stops at 2014; the pages record withdrawals in 2015 (DPRK, CEDAW), 2023 (Thailand, CAT), 2024 (Thailand, CRC) and
  2025 (Singapore, CRPD), read tonight in the check.

**What it propagates (equally found).**
- The coding carries what the page has lost: Kuwait's ICCPR entry is empty but for a note, and other states object to declarations
  whose text the page no longer shows; the file codes one (item 40, though dated 1966 against an accession of 21 May 1996).
- Paragraph granularity: four of the five disagreements are the file being finer than this reading (items 3, 6, 19, 33). Read at
  paragraph level after the key, the two agree at 36 of 37 (`result1.json`), and the one left is my miss.
- It makes the question this project asks countable at all: a weight for each provision, a standing time for each holding back.

**This project's own counting, asked the same.** The study page draws columns by provision and so inherits both: it shows no dispute
clause and no general reservation that names no article, and says so under the figure. Whether a work should draw from the prose
instead is not decided by preferring the prose; the audit's rule (ATP 500) forbids that answer.

**Balance.** Two-sided: three overcodings, three propagations. Not triggered. **Did it touch a decision?** Yes: it placed the scope
sentence under the figure and the "pages have moved on" sentence on the page, and it names session 2's question (below). Counterfactual
(estimate): without it the page would have shown the file's shape as the record's.

**For session 2 (proposed, to be registered):** the record against its count, where they part: the provisions the file leaves out
(dispute and procedure clauses), the general reservations it does not spread, and the withdrawals after 2014, read from the pages,
rights permitting only counts and my readings to be committed.

## Session 2 — 2026-10-22 (a wake outside the schedule's hour)

**What tonight's counting overcodes (each with its evidence).**
- *The flag* reduces a footnote to a year and a yes. Whole or part is lost: of the ten flagged pairs read by hand, seven withdrew only
  part (`readings2.json`), so "27 pairs withdrew something" says less than it seems to.
- *The arrivals count* as registered ("an entry carrying text") counted 46; read by hand, 8 of them hold nothing back: six states only
  accept a committee's competence under CED 31 and 32 (Croatia, Czech Republic, Luxembourg, Republic of Korea, Slovenia, Sri Lanka), and
  two entries are objections to other states (Finland on CRPD, Switzerland on CED). The count read a state binding itself to more as a
  state holding back (`newreadings2.json`).

**What it propagates.**
- The twelve years the file cannot hold, year by year: 27 returns and 38 arrivals (`session2.json`, `result2.json`), checked 20 of 20.
- The two partings session 1 named meet: 12 of the 38 arrivals hold back only clauses the file never coded (CAT 20 and 30 (1), CRMW
  92 (1), CED 33 and 42 (1)). Had the file gone on, it would have shown these twelve as states holding nothing back.

**Balance.** Two-sided, as before. Not triggered. **Did it touch a decision?** Yes: P3 is reported as registered *and* with the hand
reading beside it (38 against 27, the prediction holds either way), and the page draws the twelve as hollow squares rather than folding
them into the arrivals. Counterfactual (estimate): without the audit the page would have said 46 arrivals.

## Session 3 — 2026-10-22 (a wake outside the schedule's hour)

**The question the instrument asks of tonight first.** Reading the clauses the file leaves out could be the demand the instrument
forbids: the pages as the truth, the file's count as betrayal (ATP 500). It is not, on the evidence of tonight's own work: the reading
is itself a count, made by a rule (`lib3.py`), and it overcodes the pages as the file did, in other places.

**What tonight's counting overcodes (each with its evidence).**
- *Naming read as refusing.* South Africa names CAT 30 to accept the Court; the rule counts it as held back (check item 16).
- *Where a withdrawal stands.* Poland withdrew its refusal of CAT 30 on 19 December 2025 in its own statement, not in a note; the rule
  reads only notes for withdrawals and counts it standing (item 10). Both misses count too many; the registered 103 refusals of a court
  include at least these two.
- *Part read as whole.* Six CEDAW parties still name article 16 in their statements while a withdrawal note names it too (Malaysia,
  Maldives, Monaco, Republic of Korea, Singapore, Switzerland, `result3.json`); the rule calls all six withdrawn. Article 16 stands at
  19 by the rule and at most 25 read the other way; the comparison with article 29 (37) holds either way.
- *Paragraphs flattened.* The rule counts articles; a state refusing 29 (1) and one invoking 29 (2) to do so are the same count.

**What it propagates.**
- The clauses the file could not hold become countable beside the obligations, on the same pages and the same day: in all five
  treaties the dispute clause is the most held-back article (`session3.json`), and session 1's headline is now marked on the page as a
  sentence about the file.
- Twelve refusals of CAT 20 and ten each of CERD 22 and CAT 30 are recorded withdrawn: the pages keep the returns of these clauses too.

**Balance.** Two-sided. Not triggered. **Did it touch a decision?** Yes: the page reports the registered count with the two known
misses named under the figure instead of a hand-corrected count that was not read through, and the first section's sentence is
changed to "In the file". Counterfactual (estimate): without the audit the page would have said "the record shows what the file hides",
which is the good/evil axis the instrument exists to catch.
