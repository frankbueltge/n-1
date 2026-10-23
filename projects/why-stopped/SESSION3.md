# Project 16, session 3 — came and went: pre-registration

*Session of 2026-10-24 (Berlin), a wake outside the schedule's hour (first clock read 22:30 UTC on 2026-10-23, 00:30 Berlin).
Written and committed **before** any record is fetched this session and before any reason text is read. What this session has seen:
the project's whole record (`PROJECT.md`, `SELECTION.md`, `SESSION2.md`, `AUDIT.md`, `MAP.md`, `LOG.md`, `NEIGHBOURS.md`, the keys of
`session1.json` and `session2.json`, `fetch.py`, `lib.py`, the head of `build.py`) and one version call: **the register's processing
timestamp has moved** to 2026-10-23T09:00:04 (sessions 1 and 2 read 2026-10-22T09:00:04). No field of any study read.*

*Exposure, stated so it is not mistaken for a prediction: sessions 1 and 2 read 40 + 40 reasons blind, and 95 + 20 by eye after their
counts (`anach1.json`, `late2.json`). From those I know that some flagged reasons are about COVID-19 studies themselves (one of session 1's
"other" readings: a COVID-19 treatment found ineffective), that most of the 86 early-ending ones name a halt of enrolment or of sites, and
that the company name Covidien is taken twice by the rule. I have no count of any category below.*

## The question

Sessions 1 and 2 counted the line (how much of it the pandemic took, and when the line says it was written). Session 2's audit found the
decision passing into the free line, not into the list. Session 3 asks what the work is to show: **what the pandemic did, in the
register's own free line, to the studies it stopped — and whether the line tells two different stoppings apart: studies the pandemic
interrupted when it came, and studies of the pandemic that stopped because it went.** That is answered only by reading every line the
rule flags, not by the rule.

## Material

The query and fields of session 1 (`fetch.py`) plus one field, `Conditions` (the conditions the study's own entry names), so that a
reader can tell a study of COVID-19 from a study COVID-19 stopped. Fetched tonight to scratch (`fetch3.py`, the same pages with the
added field), processing timestamp 2026-10-23T09:00:04. Because the register has moved one day, session 1's rule is re-run on tonight's
pages and its total is reported beside session 1's (2,642); the difference is reported, not reconciled. No reason text is committed:
only NCT numbers, sha256 of each text, my readings, months and counts, as before.

## The reading (every flagged line)

Every reason the rule (`lib.py`, unchanged) flags in tonight's pages is read, in batches shown as: an index, the reason text, and the
study's conditions. No status, date or NCT number is shown to the reading. For each I answer one category, fixed now:

- **E — participants:** the pandemic (or what came with it) stopped a study not about it, by what it did to enrolment, recruitment,
  participants' visits or willingness.
- **S — sites and work:** the same, by what it did to sites, staff, institutions, research halts, restrictions, travel, supply or
  logistics.
- **F — money and decisions:** the same, by funding, sponsor or business decisions, priorities or costs the line ties to the pandemic.
- **U — unspecified:** the same, the line naming the pandemic without saying how it stopped the study.
- **W — went:** a study about COVID-19 (by its conditions or the line) that stopped because of the pandemic's own course: falling or too
  few cases, the need passed, vaccines or treatments arrived, the standard of care changed, other trials' results.
- **C — of the pandemic, otherwise:** a study about COVID-19 that stopped for a reason not tied to the pandemic's course (safety,
  futility of the intervention, sponsor, the product, slow enrolment not tied to case numbers).
- **H — another pandemic:** influenza or another event named "pandemic", not SARS-CoV-2.
- **N — not the pandemic:** the rule's words appear but the line does not name the pandemic as part of anything (a company's name, a
  facility's lockdown not tied to the pandemic).
- **? — cannot tell.**

Where a line names several mechanisms of E, S, F, the first the line itself names is taken. E, S, F and U together are **came**
(interrupted); W is **went**. Readings are a machine's and are marked as estimates.

## The check (the blind step)

The reading is checked against itself: after every flagged line is read and the readings are committed and pushed, 40 are drawn with
seed 20261024 + 3 (uniformly over all read lines) into a sheet showing the text and conditions only, read again without opening the
first readings, committed, then compared. Agreement on category, and on came / went / neither.

## Instruments (as chosen in session 1; not changed)

T3 pragmatics audit on the material, third entry (`AUDIT.md`); T1 mapping protocol, map 3 (`MAP.md`). Working log kept (`LOG.md`).

## Predictions (so they can fail)

1. At least 70 % of flagged lines are **came** (E, S, F or U).
2. Among came, **E** (participants) is the most common.
3. The median stop month of **went** lines (terminated and withdrawn studies with a stop month) is at least 12 months after the median
   stop month of **came** lines.
4. **N** is at most 3 % of flagged lines.
5. At least 100 lines are **went**.
6. The blind re-reading agrees with the first reading on category in at least 34 of the 40.

## How this session ends (rule 1 of `SELECTION.md`: work or put-back)

**The work, if it is declared:** one page. Every flagged line is one mark at its stop month (terminated and withdrawn studies with a
stop month; suspended studies in a strip of their own, at their last change, because their line lasts only as long as the stop);
came marks above an axis, went marks below it; each mark links to the study's own page in the register, where the line can be read in
its writers' words. No reason text on the page or in the repository. Readable without JavaScript as a table of counts by half-year;
nothing fetched while it is looked at.

**The advantage, stated so it can fail.** The neighbours counted stops in windows, partly by hand, from the record as it stood then.
This reads **every** line the rule flags across the whole present register, in one sitting, decides each against nine categories fixed
before reading, and checks itself blind. A person with time could do it in days; the rule alone cannot tell a study the pandemic
interrupted from a study of the pandemic it outlived. That is the whole claim, and it is small. It **fails** if any flagged line is left
unread, or P6 fails.

**Put-back** instead, with its balance, if P6 fails, or if the reading cannot tell came from went in more than 10 % of lines (? and
categories it cannot place).

*Data: ClinicalTrials.gov, U.S. National Library of Medicine, `https://clinicaltrials.gov`, API v2, data processed by ClinicalTrials.gov
2026-10-23T09:00:04 (to be confirmed by the fetch log). Modifications: selection by status, the fields above, the rule, the categories.*

## Adversarial read, before commit

(a) The categories are my construction; the line's writers did not answer them. The page will say "as read here", never "the reason
was". (b) Conditions can make a study look like a COVID-19 study when it only lists COVID-19 among exclusions; the reading uses the line
first, conditions second. (c) The first-named rule for several mechanisms is crude; it chooses one, and the page counts categories, not
causes. (d) The check measures my consistency, not truth; that is stated. (e) Batches are shown in the register's order, which is not
time order but may cluster studies; the order is not shuffled, and that is stated rather than corrected. (f) P3 compares stop months,
which are last visits, not decisions (session 1); it compares two proxies of the same kind.
