# Project 14, session 2 — the hinge, counted: pre-registration

*Session of 2026-10-21, first clock read 01:03 UTC (03:03 Berlin), the schedule's hour. Written and committed **before** any sentence is
read tonight. What this session saw before writing, so the exposure is on the record: session 1's record (`SELECTION.md`, `PROJECT.md`,
`LOG.md`, `AUDIT.md`, `REFRAIN.md`, `NEIGHBOURS.md`, `lib.py`, `session1.py`, `bridges.json`); the export's headers (same length and
last-modified as session 1's, 2026-10-17). The export is being re-fetched to scratch; no row of it has been looked at. What I know of
French and Russian address (tu/vous, ты/вы) and of English "you" is training knowledge, used to write the rules below; whether the rules
read the sentences right is tested by a reading registered here.*

## Question

Session 1 found that half the losses in its 29 chains were in no single translation: the sentence in the middle held a form with two
readings, most often English "you" (5 of 15). That was read in 150 sampled chains. Tonight asks it of the whole graph for one hinge, the
one session 1 met most: **when a French sentence and a Russian sentence are joined only through a sentence in between, how often do they
disagree on who is addressed, and does that depend on what the middle sentence can say?**

French and Russian split address in the same place: a singular, familiar "tu" / "ты" against a "vous" / "вы" that is plural or polite.
English "you" and Esperanto "vi" do not make that split; most other bridge languages do (German du/Sie-ihr, Spanish tú/usted-vosotros,
Ukrainian ти/ви: training knowledge, not tested tonight). The pair is chosen because both languages almost always write the pronoun,
so the address can be read by rule without reading each sentence.

## Rules, fixed now

- **Ends:** a French sentence (`fra`) and a Russian sentence (`rus`). Tokens: the lowercased text split on anything that is not a letter
  (Unicode), keeping French elisions as tokens (`t'` / `t’`).
- **Address of a French sentence.** *T* if it holds any of `tu te t' toi ton ta tes` and none of `vous votre vos vôtre vôtres`; *V* if
  the reverse; *mixed* if both; *none* if neither. (`tien(s)`, `tienne(s)` left out: `tiens` is also a verb.)
- **Address of a Russian sentence.** *T*: `ты тебя тебе тобой тобою твой твоя твоё твое твои твоего твоей твоему твоим твоих твоими твою
  твоею`; *V*: `вы вас вам вами ваш ваша ваше ваши вашего вашей вашему вашим ваших вашими вашу вашею`; mixed and none as above.
- **Classified:** T or V. Mixed and none are counted and set aside.
- **Bridge classes** for a chain fra–B–rus (session 1's chain rule: B linked to both, three different languages, no fra–rus link):
  - **eng-you:** B is English and holds `you your yours yourself yourselves` (case-insensitive, whole tokens);
  - **eng-other:** B is English without them;
  - **epo-vi:** B is Esperanto and holds `vi vin via viaj vian viajn`;
  - **epo-other:** B is Esperanto without them;
  - **other:** B is in any other language.
- **Disagreement:** both ends classified and A's class differs from C's.
- **Units.** The **chain** (A, B, C) is the unit of the predictions; a pair of ends with several bridges counts once per bridge. Distinct
  pairs of ends are reported beside it. **Direct pairs:** a fra–rus link, both ends classified.
- **Independence baseline** for a class: 1 − (t_A·t_C + v_A·v_C), where t and v are the shares of T and V among that class's French ends
  and among its Russian ends: the disagreement if the two translators had chosen independently, each by their own habit.

## The rules' reading, registered (so the rules can fail)

Before the count is looked at, with seed 20261021: 40 French and 40 Russian sentences drawn from the ends of fra–rus chains, 10 per
class T, V, mixed, none for each language, written to a sheet **without their class**. This session reads each and says T, V, both or
neither by reading, not by the word lists. Readings committed before the classes are compared. **If the rule agrees with the reading on
fewer than 36 of the 40 T-or-V-classified sentences (90 %), the rule fails**; it is then revised, the count re-run, and both counts
published. The readings are a machine's and are estimates.

## Predictions (so they can fail)

7. Direct fra–rus pairs, both ends classified: disagreement **at most 8 %**.
8. eng-you chains, both ends classified: disagreement **at least 35 %**.
9. eng-you chains: observed disagreement **at least three quarters of its independence baseline** (the English bridge carries almost
   nothing of the address across).
10. "other" chains: disagreement **at most 15 %**.
11. epo-vi chains: disagreement **at least 30 %**, if at least 100 such chains have both ends classified; otherwise reported as too few.
12. eng-you is the largest class among fra–rus chains with both ends classified.

Predictions are reported as registered, and again after any verified correction. Any failing is a result.

## Instruments

T3 (`AUDIT.md`) asks of the count what passes and what does not, and asks the session's own sentence the same; T5 (`REFRAIN.md`) draws
the session's balance and tests any proposed opening. The log stays `LOG.md`, stamped by `date -u`. No work is declared tonight
(`SELECTION.md`, rule 1: none before session 3).

## Rights

As `SELECTION.md`. Committed: counts, and the sentences of the rule check and of any example shown, quoted with their ids and links. No
username is fetched or read. A pair that disagrees is two people's faithful choices meeting through a third, not an error, and the page
says so.
