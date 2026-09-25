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

## Session 2 — night 36, 2026-09-25 (first clock check 2026-09-25T01:19:02Z)

**Plan at the start** (session 1's "open for session 2"): the full neighbour
search, the guard against *Below the Threshold* in writing, a first question
of form, and a decision on where session 3 falls relative to the vote.

**What happened, in order.**

1. **Boot deviation, logged.** Pull requests #12 (night 34) and #13 (night
   35) were both open and unmerged. #13 stacks on #12. This session builds on
   #13's head (`906012e`) and merges neither. The founder merges.
2. **Neighbour search** (`NEIGHBOURS.md`). The Atlas of Data Art holds nothing
   on the material. The web holds two close neighbours. **Detour, and the
   largest change of direction so far:** Sara Morawetz's *61/60* has been
   waiting since 2015 to answer a leap-second vote, "either a celebration of
   the continuance of the leap-second or a eulogy to its end". Session 1's plan
   to follow the vote as it happens would retrace her pre-registered move. The
   vote leaves the centre of the project. It becomes a fact the work must state
   correctly, not the work's object.
3. **Detour, unplanned: a rights route.** Looking for reuse terms led from the
   IERS registry entry (licence "other") to the IERS Rapid Service/Prediction
   Center at USNO. Its front page says "distribution unlimited", and its files
   are U.S. Government works. The Bulletin A columns are committed
   (`material/earth-rotation/2026-09-25-session-2/bulletin-a-ut1.csv`, 19,624
   days). They agree with night 35's C04 figures to 0.0001 s on the three dates
   checked. Without this the project could not have published a daily work at
   all. Night 35's rule (derived figures only) would have limited any form to
   aggregates.
4. **The material moved again.** Bulletin A runs a month past C04. UT1−UTC
   crossed zero on 2026-09-09 and stands at −0.0135 s (2026-09-24). The days
   are now longer than 86,400 s. Session 1's line "the two times have never
   been closer than they are now" held at the time it was written. Tonight they
   are on the other side of each other.
5. **T1 consultation, before the framing decision** (`python3 atlas/consult.py
   connects work:below-the-threshold work:two-nights-deep
   project:earth-rotation`). *Two Nights Deep*'s third working ("what arrives
   is itself a draft") showed a trap: a newer, revisable row overturning an
   older sentence reads exactly like that work's problem. **Decision changed:**
   item 4 is recorded as newer days, not as a correction arriving late, and the
   newest-rows provisionality is kept as a caveat, not a theme.

**Guard against re-finding *Below the Threshold*, tested in writing.** That
work's problem is an entry condition. The CT logs hold only what an
institution's act lets in, and the name it asked about never entered, so it
measured an absence. **Where this project differs in kind:** (a) the
statements here are not absences. Twenty bulletins were issued, dated and
addressed, and each one is a positive act deciding that no act is needed. (b)
The body acts every day whether or not a statement admits it: 19,624 measured
days, not one unentered name. (c) The resemblance that remains is real: "what
an institution's statement lets act". It is carried as a danger. It would
become a re-finding if the work were built on the "NO"s *alone*, as an archive
of refusals. **So the guard fixes one constraint on form: the "NO"s may
appear only against the days, never as the work's sole material.** Verdict:
the guard holds, with that constraint.

**Form, first question under both bars.** Only the question is opened; no form
is chosen tonight.
- *Reception* (someone who has read nothing): the one sentence a stranger must
  be able to say back is "the planet's day and the world's clock were kept
  together by hand, and that is about to stop". Every candidate form is tested
  against that sentence.
- *Advantage* (what only this subject could do). Claimed as a question, not a
  finding: to hold **every** day at once, the days on which nothing happened,
  at the resolution at which they were measured. Morawetz's and McClymont's
  works are keyed to the event because a person's attention is. A
  machine-attended record can be keyed to the day. **Estimate, marked:** a
  person with time could draw 19,624 points. The advantage is therefore weak
  if the work is a chart, and it has to be found in what the work *does* with
  the days, not in their number. This is what session 3 must answer, or the
  project should put back.
- *Excluded by the neighbours:* a response to the vote (Morawetz); one image
  per leap second (McClymont); a clock face per body (Paterson). The two-hands
  form (planet and clock) is **on hold** until the unverified Instagram lead
  is identified.

**Where session 3 falls. Decided, reasoned, revisable by dated addition.** The
vote no longer needs to be followed as it happens (item 2), so the project does
not wait for it. **Session 3** is the next night: the form is chosen and a
first study is built from the committed series. **Session 4:** build and
second pass. **Session 5**, if taken, falls **after 15 October 2026**, and its
only task there is to set the resolution's status (adopted, amended or
deferred) in the work. The work is built so that this is one fact changed, not
a new response. The founder's reading (14 October) falls inside that span, so
the work may be read while the vote is still a draft. That is stated here and
not managed.

**Instruments this session (trial record, KsK ch. 6):**

- *T4:* touched the decision to drop "follow the vote as it happens" (item 2)
  and to follow the rights question to a second source (item 3). Both were
  logged as they happened. Counterfactual (estimate): without the rule to log
  and follow detours, the neighbour search would likely have been filed as a
  list, and session 3 would have been placed on the vote, retracing
  Morawetz's move. Failure criterion: not triggered. The journal was written
  during the session and logs three deviations (items 2, 3, 4).
- *T2:* touched the guard's verdict. Field 2 (statements as positive acts)
  against field 1 (bodies measured daily) is what separates this from *Below
  the Threshold*'s absence. A new movement is recorded in `ASSEMBLAGE.md`.
  Failure criterion: not triggered. Field 4 now has work continuing on it (the
  constraint on form).
- *T1 (practice-wide):* **a consultation that changed a decision** (item 5),
  commit-evidenced by this session's commits. Whether this discharges T1's
  standing failure criterion is left to the balance at the founder's reading.
  It is not claimed here.

**Open for session 3.** Identify the Instagram lead, or record it as
unidentifiable. Check whether Morawetz staged the postponed response in 2022
or 2023. Choose the form under both bars and the guard's constraint. Build a
first study from `bulletin-a-ut1.csv`, with nothing fetched at runtime.
