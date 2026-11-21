# Project 26 — smooth/striated audit (T7)

*Chosen before the work (`SELECTION.md`). The question put to the material: "in a smooth space-time one occupies without counting,
whereas in a striated space-time one counts in order to occupy" (ATP 477, via KsK §4.6, T7). Failure criterion (KsK T7): the audit
issues in a demand for "more smooth", or the translation balance comes out one-sided — only overcoding, never propagation.*

## Session 1 — 2026-11-21

**The space.** A discharge is a flow with no unit of its own: it starts, stops, starts again, runs for days. The monitor's record
(start, stop) is already a first striation — it cuts the flow at a threshold — but it keeps duration. The 12/24 rule is the second: a
grid of one 12-hour and then 24-hour blocks laid from the first discharge, each touched block one count. The triggers (30 in a year, 20 a
year over two) are where the count occupies: an investigation, a plan, money.

**Which way the translation runs, measured tonight** (`session1.json`, `explore1.json`):
- *Overcoding.* The grid erases duration inside a block and erases frequency across one: 226 discharges totalling 1 h 16 min at
  SBB01164 become 44, over the trigger; 14 discharges totalling 567 h at SBB01318 become 27, under it. 206 overflows below the trigger
  discharged longer than the median one above it. One counted spill folds on average 3.8 recorded discharges, at most 1,077.
- *Propagation.* The same grid is what gives a days-long discharge a public number at all: 21 recorded discharges at SBB01043 are, by
  the grid, 235 — a long discharge is not let off as one event. 22.2 % of counted spills hold twelve hours or more; under a count of
  activations they would be a few hundred events among a million. And the count is reproducible: the rule applied to the companies' own
  start/stop rows gives the companies' returned count for 89.4 % of overflows.

**Balance.** Two-sided: the grid overcodes short frequent discharges upward and long rare ones downward, *and* it is the only reason a
long discharge reaches the public as more than one. Failure criterion not triggered. Nothing here asks for a smoother count; the
finding is where the striation's two errors meet — at the trigger line, where the count begins to occupy.

**Decision touched.** The study page's figure: not a chart of counts, nor of hours, but the two against each other with the trigger
drawn, because the audit located the problem *at the line*, not in either measure. Session 2's question follows from it (see
`PROJECT.md`).
