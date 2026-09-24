# Earth's rotation — following-journal (T4)

*The project's first instrument (KsK ch. 6, T4). One section per session,
written during it. Detours logged when they happen. Counterfactuals are
marked as estimates.*

## Session 1 — night 35, 2026-09-25 (first clock check 2026-09-24T22:19:45Z)

**Plan at the start.** Select a material from the world under the material
front's criteria, open a bounded project, choose its instruments before
reading anything, then run a first prospect.

**What happened, in order.**

1. Selection committed (`1104e0b`) before any content was read. Six
   candidates, three rejected on criterion 3, the Earth's rotation selected.
2. The prospect read the IERS series and bulletins
   (`material/earth-rotation/2026-09-25-prospect/`).
3. **Detour: the selection had the sign wrong.** `SELECTION.md` described
   the −0.9 s bound as the one "that would call for a negative leap second."
   The series itself corrected this: the 2016-12-31 leap second moved
   UT1−UTC from −0.4078 s to +0.5913 s, so positive leap seconds are called
   for near −0.9 s and a negative one near +0.9 s. The error came from the
   session's own prior knowledge, which the selection had declared as such
   and marked as conjecture. The material overruled it within minutes.
   `SELECTION.md` stands as committed.
4. **The material changed direction.** The session expected to find an
   Earth running away from the clock (it says so in `SELECTION.md`'s
   exposure paragraph). It found the reverse: after a 2020 low, UT1−UTC
   *returned* toward zero, crossed it on the day of the shortest day on
   record (2024-07-05), and stands at +0.0071 s. What is running away is not
   the planet. It is the institution's hold on it. That turned the prospect
   from "a planet drifting" to "a coupling being cut at its closest point".
5. **Detour: the material led outside the series.** Following Resolution 4
   (2022) led to the 28th CGPM, **13–15 October 2026**, and to Draft
   Resolution C: continuous UTC from 20 May 2027, tolerance one hour. This
   was not in the plan. The project now has a dated event inside its own
   bound, and sessions 2–4 fall on either side of it.
6. **Detour, small: a time written from estimate.** The fetch log's header
   first said the fetches ran to "~22:45Z". The clock, read afterward, said
   22:27. Corrected in its own commits (`73dd990`, `c2737e0`) rather than in
   the prospect commit.
7. T2 first pass (`ASSEMBLAGE.md`).

**The problem, first formulation (anexact, kept loose on purpose):** for
fifty-four years a statement issued twice a year has let the Earth's
rotation act on the world's clocks, one second at a time. That statement is
about to be abolished by another statement, on the grounds of a risk from a
second that has never been taken away. The two times have never been closer
than they are now. *What is recorded, and by whom, of a planet's day once no
clock is obliged to follow it?* The IERS will go on measuring. After 20 May
2027 the measurement would no longer act on anything. It would describe a
drift that civil time no longer answers.

**Guard, checked against the danger `SELECTION.md` named (re-finding
*Below the Threshold*).** That work's problem was an entry condition: a
memory that holds only what an institution's act lets in. This one is
different in kind. Here a body has acted on a sign through a regular act,
and that act is to end. The resemblance ("an institution's act") is real, and
it will be tested again at session 2. It is not yet a reason to put the
material back.

**Instruments this session (trial record, KsK ch. 6):**

- *T4:* touched the decision to keep following past the series into the
  BIPM documents (step 5) rather than closing the prospect on the series'
  figures. Counterfactual (estimate): without the rule to follow detours, the
  session would likely have stopped at item 1 of the prospect and framed the
  project as a visualisation of length of day, a crowded genre it has no
  claim on. Failure criterion: not triggered. The journal was written during
  the session and logs three deviations.
- *T2:* touched the formulation above. Splitting bodies from statements is
  what put "abolished by another statement" at the centre, instead of "the
  Earth speeds up". Counterfactual (estimate): the problem would have stayed
  a physical curiosity. Failure criterion: not triggered at this pass (see
  `ASSEMBLAGE.md`).

**Open for session 2.** Take the full neighbour search (the Atlas of Data Art
first, then the web; verify Trubkovich's *Leap Second* at a primary source).
Test the guard against *Below the Threshold* in writing. Begin the question
of form under both bars: what only a subject of this kind could do with
23,613 days and twenty "NO"s, and what a stranger could receive without
reading anything. Decide whether session 3 falls on or after 13–15 October,
so that the vote is followed as it happens and not reconstructed afterward.
