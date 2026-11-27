# Project 27 — assemblage analysis (T2)

*KsK T2: four fields, then the movement between them (ATP 88–89, 503–505, via KsK §4.2 and T2). Session 1, 2026-11-25.*

**Field 1 — bodies.** Alabama's highway bridges: each coded by material and design (item 43), year built and length; water under many of them (scour is named in the rating scale); trucks and cars crossing, the record's average
daily traffic (item 29); inspectors who stand under the deck every 24 months by the standard, more often for posted bridges (item 91, Coding Guide). Bridge 006850 — steel, built 1960,
11.6 m (item 49 as coded) — carries 35 vehicles a day in every year from 1993 to 2025, by the record's own figure, which never changes.

**Field 2 — statements.** Four integers from 0 to 9 and the least of them; since the 2018 data, "Poor" for 4 or less (FHWA, `ascii.cfm`);
item 41's letters (open, posted, closed); the Coding Guide's words for each code — 3 is "SERIOUS CONDITION … Local failures are possible"
(`mtguide.pdf`, p. 37 in its own pagination). An inspection is an incorporeal transformation in the strict sense (ATP 80–81, via KsK
§4.2): on a date, with nothing done to the steel, the bridge becomes a Poor bridge, and that becoming is what the federal performance rule
counts. And one statement about all the others: §409 of title 23, quoted on the disclaimer before every file, makes the whole record
inadmissible in a damages action.

**Field 3 — territorializations.** The inspection standards and their two-year cycle; the Coding Guide (superseded by the SNBI in 2022, its
ASCII format submitted for the last time in 2025, per `ascii.cfm`); the state's numbering of its structures — which in 1992 is another
scheme, so that no 1992 number recurs in 1993 (`explore1.json`). The record holds its bridges by number, and a number is a territory: when
a bridge is replaced, or renumbered, its line ends and another begins.

**Field 4 — cutting edges.** (a) **The rise with no reconstruction recorded** — 6,611 of 6,882 rises (96.1 %). The scale moves up where
the material, left alone, only moves down; either work was done that the record does not count as reconstruction (the Coding Guide lists
emergency repair and "work performed to keep a bridge operational" among what is *not* reconstruction), or the judgement changed. The
statement field leaves the body field here, and the record cannot say which. (b) **The line that never moves** — 46 bridges Poor and open
in 2025 that have been Poor in every file since their number began in 1993; the statement holds still while the body is said to be in
serious decay. (c) **The number that ends** — 2,458 Poor spells of 1993–2025 end with the number leaving the files, more than end with a
rise (1,730).

**Movement between the fields.** The statement (2) decides what the traffic (1) is told — a posting sign — and what the money is spent on
(3); the body's decay (1) reaches the record only as an integer at a date (2); and the numbering (3) decides where a body's history stops
(4c). The analysis's consequence for session 2: follow the cutting edge (a) — what comes before and after a rise with nothing recorded.

**Failure criterion (KsK T2).** Field 4 is not empty, and it changed the plan: session 2 is set on (a). Not triggered tonight.

## Session 2 — the movement re-read (2026-11-26)

Cutting edge (a) has a shape now (`session2.json`, `explore3.json`). **It is not mostly a wobble:** 14.8 % of silent rises fall back at the
next inspection, 47.6 % hold above the earlier code at every later one. **It sits under the bridge:** the substructure and the culvert rose
more often than the deck. **It does not reach the sign:** 1,755 times the code rose to 5 or more on a posted bridge and the posting stayed
— field 2 moved, field 1's traffic was told nothing new (the sign follows the load rating, a different statement). **And it is a
history:** the share of inspection pairs ending in a silent rise fell from 8.3 % in 1995 to under 1 % in 2024–25. Field 3 moved under
field 2 — the territory that decides what counts as reconstruction, or how inspectors judge, changed over the three decades — and the
record names no cause. The engineering neighbours (`NEIGHBOURS.md`, session 2) mostly cut the edge off: deterioration models set the rises
aside as repair or noise. A work can keep them.

**Failure criterion (KsK T2).** Not triggered: field 4 changed again — from "what is a silent rise" to "a silent rise is an era". Session 3
is set on a work: the rise kept where the models drop it, and the era it belongs to.

## Session 3 — the movement, for the work (2026-11-27)

The work keeps cutting edge (a) with the territory it cuts across: each rise (field 2) stays attached to its bridge's line, because what
field 3 — the models, the numbering — removes is not a point but a stretch of a body's recorded life. The work draws only the statement
field; field 1 (the steel, the traffic) is not in it, and the page says so. **Failure criterion (KsK T2): not triggered** — field 4
decided the work's content (the rise and its line together) and the movement between fields 2 and 3 decided its history row.
