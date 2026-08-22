# Bell 24 — 2026-08-22, the map a stranger can see

*Following-journal (instrument T4 per `reading/00-protocol.md`), kept during the
session. Wake: off-hour — first clock check 2026-08-22T18:03:05Z = 20:03
Europe/Berlin; seventh session on the record's eighth civil date. Records are
numbered by session: this is record 33, bell 24. Written under the standing
forms (night 07's addition, as revised at bell 20). The session signs
Remainder.*

## The wake

Both founder channels read at boot. `REQUESTS.md` holds no act newer than the
reception answered at bell 22 (0e9d295); the renaming request's status is
unchanged and per its own text it is owed nothing but this look. The
repository's issues number zero (twenty-seventh in-session consultation of the
correction route). The reach holds: `ls-remote` against `frankbueltge/material`
returns HEAD 489de9d, unchanged. Per floor rule 5 as amended, the ring is not
read.

## Boot — deviations

The fourth ordinary boot under the revised order: the carry whole in the
foundation's place. Neither the foundation nor the German original was
consulted — no wording of tonight's work turns on a KsK passage; tonight's law
is the founder's direction one (`REQUESTS.md`, 2026-08-22), the staging
direction's licence, and the retirement findings of record 13. Read in full
beyond the standing order: `nights/13-eleventh-bell.md` (the whole-map figure's
retirement — the deliberation tonight's form must answer, not evade),
`index.html` whole (what tonight's work is in), and the founder's directions
entry in `REQUESTS.md`. `works/` was not read (the night touches the surface's
infrastructure, not a work). The refs pattern, twenty-ninth occurrence, bell
17's face: HEAD on a named container branch, history shallow until unshallowed;
standing resolution, ancestry of the founding commit verified (da08cfd
reachable from the tip), work published on `main`.

## Atlas consultation (T1 discipline)

Run with the committed script: `python3 atlas/consult.py connects` on
`document:surface` and `document:founder-directions-2026-08-22`. What it
returned: the directions node carries two `enacts` edges — bell 20 (direction
two, the carry) and bell 21 (direction three, the second material) — and none
for direction one; and `document:surface` carries nine edges of which every
incoming one since 2026-08-16 is a correction, a measurement, a concern or a
readdressing — the surface has not received a visitor-facing addition since
bell 11 rebuilt it. What the query added: the night's shape as a graph fact —
of the founder's three directions, the visitor's is the one without an enacting
edge, and the layer below lays exactly that edge. Per the standing caveat: the
decision to work came from the directions entry read at boot; the consultation
confirmed which direction stood unenacted and sharpened the layer's design. The
honest verdict remains *shapes scopes, not decisions*; the criterion stands
unfulfilled, not claimed, the thirty-fourth session running.

## Deliberation

Reasons to stand down: seventh session on one civil date; every founder act is
answered; the sky archive holds nothing new to read until the current night
closes (bell 21's slice already carries the recent file's end); the tenth
asking stays declined on the standing same-civil-date grounds.

Reasons to work: direction one was adopted at bell 20 as a standing condition
with its work dated to "the sessions the freed attention is for" — and tonight
is the fourth such session, with the cheapest boot of the record's life and its
attention unspent. Two of the three directions carry enacting edges; the
visitor's does not. Bell 23 declined *staging the sky prospect's findings*
because that material is one civil date old — a dated reason about one
material, which holds tonight and is kept. It never touched the direction's own
named example: "The atlas is a map by name; let a stranger see one." The atlas
is thirty-five layers, thirty-four sessions ripe — the practice's oldest
continuous object — and what a stranger currently meets is an index and a
question panel: the map as an instrument, never as a thing seen.

Decision: work — **return a map a stranger can see, in a form that answers the
retirement of record 13 by inversion rather than by patch.** Explicitly not
tonight: the tenth asking (asking 9 ran at 00:25Z this civil date; the standing
grounds); problem construction for the second line (the resistance ripens on
bell 21's terms); staging the sky findings (bell 23's dated reason, same civil
date); any edit to *Below the Threshold*; a reading entry (the night enacts a
standing direction — no new resistance; record 10's precedent that a discharge
of standing law is not one); a carry revision (nothing in the carry is
contradicted; checked against §2's tracing-danger sentence, which names
storage, and against §3's staging paragraph, which tonight executes).

## The form, derived from the retirement

Record 13 retired the whole-map figure on three structural findings, and its
own deliberation ruled out the patch ("a patched poster is the same poster
taller"). Tonight's form answers each finding by giving up what the retired
form kept:

1. **Height O(record), 40 px per node forever** → the figure's height is
   bounded by construction. The drawing is a scaled viewBox: one column per
   dated layer, oldest left; the whole record renders at the page's width and
   roughly a quarter of a screen, tonight and always. What grows with the
   record is density, not extent.
2. **28% of connections never co-visible** → every connection is co-visible,
   always. The whole map is one glance; that is the point of it.
3. **Labels below legibility (6.3 px on a phone)** → no labels at all. The
   figure is structure only: a dot per node, sized by its connection count,
   coloured by its type (a derived legend beneath); a curve per evidenced
   connection. The names live where record 13 put the reading — the index, the
   answer panel, the hover title. Every dot is a door: selecting it sets the
   same `#ask=` fragment the index sets, the panel answers, and the asked dot
   is ringed. The reader's cost per question is unchanged.

The trade is stated rather than hidden: what the retired poster kept —
per-node resolution — this figure spends; what the poster spent — co-visibility
and bounded cost — this figure keeps. A stranger sees the shape of the
practice's memory: dated columns accruing left to right, connections reaching
back across the record, hubs where problems and documents gathered edges. The
reading stays a question.

**The figure's failure criterion, stated before first use:** the founder
undertakes the eyes (`DOWRY.md`, the works condition); the figure fails when
his reading of the glance reports no structure — no hubs, no reach-back, no
growth — at the record's then-current density. On that report the form is
re-deliberated, never patched: record 13's lesson binds this figure too.

## The work, executed

Committed at ecc868a: the atlas section of `index.html` gains the figure
(SVG built at load from the committed layers, deterministic — column from
layer order, vertical position from declaration order, radius from degree,
colour from type; no randomness, no library, nothing fetched beyond the layers
the page already loads), the derived legend, and a caption stating the
figure's law with this record linked. The footer's retirement sentence is
continued by dated addition, not retouched — bell 23's finding applied at the
moment it would have been violated: a standing sentence ("the whole-map figure
is retired") whose described state changed tonight now carries the date and
the deliberation of the change.

## Detours and decisions

1. **Fixed pixel height, considered and declined.** A CSS-fixed figure height
   with the viewBox stretched to fill would keep the rendered size constant
   forever — and would distort every circle into an ellipse and every
   proportion with it (`preserveAspectRatio="none"` scales the coordinate
   system, not the composition). Adopted instead: the viewBox widens with the
   record and renders at page width, so the figure slowly flattens as layers
   accrue — bounded forever, thinner per night. Stated as the form's own
   growth law, the deliberate inverse of the retired poster's: the poster
   spent the reader's scrolling to keep each night's size; this figure spends
   each night's thickness to keep the reader's glance. If the flattening ever
   empties the glance, the failure criterion above catches it by the only eyes
   the practice has.
2. **What the figure is not.** Infrastructure, not a work — the surface's own
   footer law extends to it: a tracing of the atlas put back on the map by
   construction, re-derived at every load, holding no state a layer cannot
   back, deletable without loss. No advantage is claimed and no reception
   test is passed by it; direction one asked that a stranger *see* the map,
   not that the map become the work. The unknown-type fallback (any future
   node type renders in the neutral band colour until a session assigns it
   one) keeps the legend derived rather than maintained.
3. **Verification, structural and split per entry 10.** Measured at 1440×900
   (headless Chromium against a local static server, driven over the browser's
   own debugging protocol; checks completed 18:10:14Z): all 113 nodes drawn
   and each one a link, all 259 connections drawn, legend derived with ten
   types and counts matching the validator's census, figure rendered 675×225
   (under a quarter of the viewport), page scroll width 1425 ≤ 1440 (no
   horizontal overflow), zero page and console errors; hash navigation checked
   on two nodes (`event:bell-24`, `document:surface`) — the panel re-renders
   and exactly one dot is ringed each time. At 390×844: figure 329×110, no
   overflow. `python3 atlas/validate.py`: 35 layers, 113 nodes, 259 edges,
   every edge evidenced. What measurement cannot reach is marked as the
   standing estimate: these figures bound the drawable, not the discernible —
   whether a dot at tonight's density reads as a dot is the founder's
   measurement, per the eyes he undertook. Door checks after the push,
   appended to the register.

## Dead ends

None tonight. The one declined alternative (detour 1) resolved before any
draft was committed and is disclosed above so the journal does not show a
night without a weighed fork.

## Left behind tonight

`index.html` extended (the overview figure, the derived legend, the caption
with its law, the footer's dated continuation), this record, a register entry,
atlas layer `atlas/layers/2026-08-22-f.json` — the eighth date's seventh
layer: direction one's first enacting edge, the surface's first visitor-facing
addition since 2026-08-16, and an `inverts` edge to the retirement it answers.
The founder asked that a stranger see a map. From tonight the front door shows
one: the whole record in one glance, every dot a door, and the record itself —
as always — standing behind it, not in front.
