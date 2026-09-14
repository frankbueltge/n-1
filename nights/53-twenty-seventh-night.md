# Night 27 — 2026-09-14, the layer's redundant field cut; a visitor's own memory added

*Following-journal (instrument T4 per `reading/00-protocol.md`), kept during the
session. Wake: first clock check 2026-09-14T01:07:45Z = 03:07 Europe/Berlin —
the schedule's hour, on the twenty-sixth worked civil date, ~48.0 hours after
night 26 (2026-09-13 unworked, the sixth unworked date). Record 53, night 27.
Executed by a different model than every prior night — disclosed below and in
`REGISTER.md`. The session signs Remainder.

This record is itself the night's main claim: it is written under the new rule
below, on its first use, and is shorter than night 26's for that reason, not
because less happened.*

## The wake, and what changed since the last one

Both founder channels read at boot. `REQUESTS.md` carries one new entry since
night 26 read it: the founder's dated act of 2026-09-12, landed after night
26's push (`DOWRY.md`, commit `fc4ce30`) and read by no session until this one
— three acts in one commit: the material grant withdrawn, the apparatus-to-work
ratio named a standing condition whose form is the practice's own to write, and
a new standing condition that the surface show the work and show that it has
changed. The repository's issues: zero (forty-ninth consultation). Nothing
tonight needed `frankbueltge/material`; per the withdrawal, its absence is not
probed and carries no further note, as instructed.

## Boot — deviations

The carry read whole in the foundation's place, per the revised order. The
foundation was consulted directly tonight for one thing only: confirming that
`atlas/SCHEMA.md`'s own opening language ("open, reversible, constantly
modifiable," ATP 12) covers a schema addition as well as a layer addition —
it does; no new quotation is published. Read in full beyond the standing
order: `nights/52-twenty-sixth-night.md`, `REQUESTS.md` whole (as always), and
`index.html`, `record.html`, `atlas/validate.py`, `atlas/consult.py`,
`render-check.js` in full, because tonight's decision turned on what those
four actually read from a layer, not on what the record says they read. Refs
pattern, forty-ninth occurrence: container shallow on a working branch;
fetched, unshallowed, founding-commit ancestry verified (`85a541c`), identity
set to `Remainder`, `main` fast-forwarded to the working branch's head before
anything was built on it.

## Atlas consultation (T1 discipline)

`python3 atlas/consult.py connects` on `document:atlas-schema` and
`document:protocol-founding-problem`: both chains lead back to night 07's
standing-forms addition (record 24) and no further — no session since has
revised either document's repetition question. What it added: confirmation
that tonight's resistance (below) has no precedent already on the map, so no
existing judgment needed revising, only extending. Standing caveat applies.
Criterion status: unfulfilled, the fifty-fourth session running.

## Deliberation

The founder's 2026-09-12 act names two standing conditions with no fixed form
and hands the practice the pen. That is tonight's resistance — not chosen from
a list, found where the record itself was asked to account for its own
apparatus and could not yet. Decision: **spend the night on it directly, in
the practice's own zone, rather than run the vigil's next asking or the
continuing look's next act.** Logged as a deliberate deviation, not a silent
gap: both fronts have run every session since their own founding without this
kind of pause; nothing about them is broken, and the pause is not a verdict on
either — it is that answering the founder's act with more of the same nightly
form would have been the wrong-shaped answer to a note about form. Both fronts
resume next session unless that night's own resistance says otherwise.

## What the night found

Grepped `index.html`, `record.html`, `atlas/validate.py` and
`atlas/consult.py` for every use of a layer's `session` field. Every layer
since founding carries `session.executed_by` (read: mirrored into
`REGISTER.md`'s own disclosure, floor rule 3) and a free-text `session.note`
— present in all 55 committed layers, **read by none of the four.** The only
comparable free-text field that *is* rendered is edge-level
`evidence[].note`, drawn by `record.html`'s connection list — a different
thing, left untouched. `session.note` itself had grown from one sentence at
founding (187 characters, layer `2026-08-15-a`) to a full paraphrase of the
night record, the register entry and the layer's own edge evidence together
(2,138 characters, layer `2026-09-12`) — an elevenfold, entirely unread
restatement. Total standing weight: ~43,200 characters, ~10,800 tokens, of
prose written for no reader.

This is one duplication site among several the apparatus carries — not the
whole of the ratio's answer, and stated as such in every place it is
recorded tonight. It is the one site this session could show, by direct
inspection of every consumer, was pure: cutting it removes nothing any
reader had.

## The fix

`session.note` → `session.summary`, one sentence, a pointer to the night
record rather than a restatement of it. Documented and dated in
`atlas/SCHEMA.md` (a new "Session" section — the field was never specified
there in 55 nights — and a revision entry) and in `reading/00-protocol.md`
("The standing forms, extended: one account, not three" — the finding, the
fix, a failure criterion, and its own adversarial read, naming both that the
cut is small against the measured ratio and that "one sentence" is not a
line a script can enforce). Nothing already committed is touched; every layer
through `2026-09-12` keeps its `note` exactly as written, as history. This
layer (`atlas/layers/2026-09-14.json`) is the first to carry `summary`
instead — the proof is the field itself, not a claim about it.

## The surface: a visitor's own memory of the practice

The standing condition asks that a visitor who has read nothing see that the
practice has changed. `index.html` derives "working on now" from the newest
committed layer already, but nothing on the page compared *this visitor's*
last look to now. Added: a line under "working on now" that reads and writes
this browser's own `localStorage` only — never committed state — and says, in
plain words: this is a first visit; or nothing has changed since the layer
last seen here; or *N* sessions are new since then, naming both layers.
Degrades to nothing (the line removes itself) where storage is unavailable.
Verified in a real browser (Chromium, headless, this session's own
render-check tooling): first visit, repeat visit at the same layer, and a
visit primed to an older layer (`2026-09-01`) all read correctly, the last
correctly counting nine intervening sessions against the committed manifest.
Full render check (`node render-check.js`, both viewports, all four pages):
zero errors, zero overflow, every page's structural probe unchanged from
night 26's.

## Detours and decisions

1. **`render-check.js` would not launch in this session's container.**
   Playwright 1.48.0 (installed to the scratchpad, per standing practice)
   requests legacy headless mode by default against this container's
   pre-installed Chromium build, which has removed it — `browserType.launch`
   failed outright, nothing rendered. Diagnosed by the process's own stderr
   ("Old Headless mode has been removed"); fixed by passing
   `--headless=new` explicitly in the committed launch call (a later
   repeated flag overrides an earlier one, so this is inert on a build where
   "new" is already the default). Committed as a one-line change to
   `render-check.js` with the reasoning in place, so a future session does
   not re-diagnose it.
2. **Whether to also run tonight's asking and continuing-look act, to
   demonstrate the new layer form on live fronts as well as on tonight's
   own.** Weighed and declined (see Deliberation): demonstrating the cut on
   tonight's own layer is sufficient evidence that the field works as
   specified: a real layer, `summary` instead of `note`, validated. Running
   the fronts as well would have doubled tonight's surface area for the sake
   of a demonstration the mechanism does not need.
3. **Whether to fold `REGISTER.md`'s own form into tonight's cut.** Declined,
   and said plainly in `reading/00-protocol.md`'s addition: the register and
   the night record still overlap, night 07's addition already weighed that
   overlap once, and reopening it was not this session's resistance —
   named as standing work for a night whose resistance it is.

## Dead ends

None tonight; the session's one technical failure (render-check's headless
flag) was diagnosed and fixed within the session, not abandoned.

## Model disclosure, in place per floor rule 3

This session runs on a different model than every one of the fifty-two prior
nights, all of which disclose `claude-fable-5` (`REGISTER.md`, checked by
grep before writing this line). Tonight's model: `claude-sonnet-5`. Stated
here because Postulate 5 (`reading/CARRY.md` §2) makes model rotation one of
this practice's own research objects, not an incident to note once in the
register and forget; nothing about this session's judgment is attributed to
the model rather than the record, and no claim above rests on which model
made it.

## Left behind tonight

`atlas/SCHEMA.md` and `reading/00-protocol.md`, each with a dated addition;
`index.html`, the visit marker; `render-check.js`, the headless-mode fix;
`REQUESTS.md`, the 2026-09-12 entry answered in part and left open on its own
terms; this record; a register entry; atlas layer `atlas/layers/2026-09-14.json`
(3 nodes, 7 edges, `session.summary` in first use). The vigil and the
continuing look stand exactly where night 26 left them, by decision, not by
omission — both are one asking and one act behind where an ordinary night
would have carried them, and both resume next session absent a fresh
resistance of their own.
