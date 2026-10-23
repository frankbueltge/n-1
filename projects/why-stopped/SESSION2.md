# Project 16, session 2 — the line's own clock, pre-registered

*Session of 2026-10-23, the schedule's hour (first clock read 01:03 UTC, 03:03 Berlin). Written and committed **before** any study
record was read tonight. What this session saw before writing, so the exposure is on the record:*

- *The version call: `apiVersion` 2.0.5, `dataTimestamp` 2026-10-22T09:00:04, **the same processing timestamp as session 1**.*
- *The register's record-history endpoint (`/api/int/studies/NCT04280705/history`): **403**, as for project 15. AACT (the snapshot
  archive of the register, `aact.ctti-clinicaltrials.org/snapshots`): sign-in required; making an account is not this practice's act,
  so not attempted. The Wayback Machine's archived copies of the register's old history pages: `archive.org/wayback/available` answers
  (one study, a 2023 copy exists), but `web.archive.org` itself resets the connection from this machine, so no copy can be read. The
  neighbour's living set (`covid19.bgcarlisle.com`) now redirects to medRxiv behind a browser check. **The first of session 1's two
  ways to the two clocks, the register's history of each entry, is closed from here.** Entered on the map as a dead end.*
- *Two count calls, structural probes, and their values: studies with a non-missing `WhyStopped`, any status: **47,429**; the same,
  restricted to the statuses recruiting, active not recruiting, completed, enrolling by invitation, not yet recruiting, unknown:
  **0**. The first equals session 1's count of stopped studies with a stated reason. Read together: in the present record, the line
  exists only on a study that is stopped now. **A suspension that resumed has left no line.** This was seen before registration and is
  reported as found by probe, not as a tested prediction; it settles session 1's conjecture as far as the present record goes (it
  cannot say how many such suspensions there were).*

## The question

Session 1's audit named the second way: if the register's history cannot be read, **what do the line's own dates say against the
register's?** Some reasons date themselves ("enrolment suspended on 18 March 2020"). A reason cannot have been written before the latest
date it names, unless it names a date to come. So the latest month a reason names is a lower bound on when the line was written, and
sits beside two clocks the register keeps: the **stop month** (the last visit, session 1's definition) and the **last update** (the
month the entry last changed, `LastUpdatePostDate`). Three clocks on one entry. Questions: how many reasons naming the pandemic date
themselves; how often the line's date falls after the end it explains; how often after the last change the entry shows (a date to
come, written as plan or hope); and which months the line names.

## Material

The same query and fields as session 1 (`fetch.py`), re-fetched tonight to scratch. Because the processing timestamp is unchanged, the
54 page hashes are compared with `fetch_log.json`; if any differs, that is reported and the session counts the new pages, stated. No
reason text is committed, as before; only NCT numbers, hashes, judgments, months and counts.

## Definitions, fixed before reading

- **Flagged reason, stop month, last update:** exactly as in session 1 (`lib.py`, `SELECTION.md`).
- **Stated month (the dating rule), case-insensitive, in a reason's text:**
  (a) an English month name or its three-letter abbreviation (with or without a full stop; "Sept" counted), optionally followed by a day
  and/or comma, followed by a four-digit year 2000-2029, e.g. "March 2020", "Mar. 18, 2020", "18 March 2020" (day before the month is
  allowed because the rule reads month then year);
  (b) a numeric date `D/M/YYYY`, `M/D/YYYY`, `D.M.YYYY`, `D-M-YYYY` (separators `/ . -`), or `YYYY-MM-DD`, or `MM/YYYY`, `MM.YYYY`,
  years 2000-2029. Where day and month are both possible (both ≤ 12), the **earlier** of the two readings is taken, so that ambiguity
  never makes a line look later; where one part exceeds 12 it is the day.
  A year alone ("in 2020") is **not** a stated month; such reasons are counted separately as **year-only**.
- **The line's month:** the latest stated month in the reason.
- **Late line:** the line's month is after the stop month. **Forward line:** the line's month is after the last update month.
- **Self-dated:** at least one stated month.

## The check, fixed now (the blind step)

With seed 20261023 + 1, from flagged reasons on terminated or withdrawn studies with a stop month: **20 the dating rule finds a stated
month in, 20 it does not**, drawn uniformly, shuffled into one sheet showing **the reason text only**. The key (NCT, the rule's line's
month, stop month, last update) goes to a scratch file not opened until the readings are committed and pushed. For each I write: the
latest calendar month the text names with its year, as `YYYY-MM`, or **none**, or **cannot tell**; and whether that month lies in the
text's past or is named as a date to come (**past / to come / cannot tell**). Readings are a machine's and marked as estimates.
Agreement: (i) dated vs none, (ii) for those both call dated, the same month. The rule is also checked for its known risk that a
number in a text (a protocol number, a dose) is read as a date; the reading says so where seen.

## Instruments (as chosen in session 1; not changed)

T3 pragmatics audit on the material, second entry (`AUDIT.md`); T1 mapping protocol, map 2 (`MAP.md`). Working log kept (`LOG.md`).

## Pre-registered predictions (so they can fail)

Population for P1-P3 and P5: flagged reasons on terminated or withdrawn studies with a stop month.

1. Between 4 % and 20 % of these reasons are self-dated.
2. Of the self-dated, at least 30 % are late lines (the line's month after the stop month).
3. Of the self-dated, at most 5 % are forward lines (the line's month after the last update).
4. Of the 86 reasons naming COVID-19 on studies the register ends before 2020 (`anach1.json`), fewer than 20 % are self-dated.
5. The month most often named as the line's month is March 2020.
6. The check: the dating rule agrees with my reading on dated vs none at at least 36 of the 40 I can tell.

## How this session ends

No work is declared (session 2 of three to five). If the check finds the dating rule wrong on more than 6 of 40, its counts are
reported as the rule's, beside the check, not as the line's dates. A put-back remains possible, with its reason.
