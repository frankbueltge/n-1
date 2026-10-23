# Project 16 — T1 mapping protocol

*One map, reworked each session, dated. KsK T1; failure: never revised, or no case named in which it changed a working decision.*

## Map 1 — 2026-10-22, session 1

Elements, on one plane: **the register** (NLM; its API; processing timestamp 2026-10-22T09:00:04) · **the closed list** of states ·
**the line** "why stopped" · **sponsors and investigators** (who write the line; unnamed here) · **participants** (whom the stops
touched; unnamed in the register) · **the event** (SARS-CoV-2, 2020 onward; and an influenza pandemic in 2009, found in the line) ·
**the register's dates** (start, primary completion, completion, last update) · **the law** behind the register (FDAAA 801, named in
its glossary) · **the neighbours' counts** (windows of 2020-2022) · **this project's rule** (seven words) and **its check** (40 read).

Lines that operate, with evidence:

- the event → the line, never the list: 2,642 flagged reasons (`session1.json`); the list has no state for it.
- the line → the register's dates, crossed: 86 reasons naming COVID-19 on studies ending before 2020 (`anach1.json`); median 41 months
  from the recorded end to the entry's last change.
- the list → forgetting (conjecture): suspended studies that resumed leave no stop (`NEIGHBOURS.md`, 905 vs 198).
- the rule → the count, with its own errors: 39 of 40 for the words, 38 for the event, two takings of a company's name (`result1.json`,
  `LOG.md`).
- the neighbours → this project's daylight: they count windows; this reads the line's duration and its two clocks.

Dead end, entered as one: the stop month as the time of stopping. It is the time of the last visit; the map keeps it as a line to the
event, not as its date.

Decisions changed by this map tonight: **none yet named.** Map 1 is its creation; the failure criterion is open.

## Map 2 — 2026-10-23, session 2

Reworked from map 1. New elements: **the line's own month** (65 reasons name one, `session2.json`); **the decision** (the month a study
was decided or closed, named in 10 of the 20 late lines, `late2.json`); **the register's history of each entry** (403 from here),
**the snapshot archive** (sign-in), **the web archive** (unreachable from here).

Lines that operate, with evidence:

- the line → the decision: 10 of 20 late lines name the month of a decision the register has no field for (`late2.json`, by eye).
- the line → its own writing: 2 lines date the moment they were written (`late2.json`).
- the list → forgetting, **no longer conjecture for the present record**: 0 studies outside the stopped statuses carry a line
  (`probe2.json`); how many stops were forgotten stays unknown.
- the dating rule → the count, with one error: 40 of 40 dated/none, 19 of 20 months (`result2.json`).

Dead ends, entered as such: the register's history (403), the snapshot archive (sign-in is a third-party act, not taken), the web
archive (connection reset). Each would have given the first clock directly; their closing is why the line's own clock was read.

**Decision changed by the map:** map 1 entered "the stop month as the time of stopping" as a dead end and kept it as a line to the
event, not as its date. Tonight's question read the stop month exactly that way, as one clock among three, and the late lines are
counted against it rather than corrected by it. That is a decision of design the map carried: without the dead end, the 20 late lines
would have been filed as the register's errors. T1's failure criterion (never revised, or no decision changed) is **not triggered**.
