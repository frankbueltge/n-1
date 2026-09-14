# The atlas

The atlas is this practice's documentation, memory and first work-in-becoming, all at
once. It is a map in the foundation's sense: open, reversible, constantly modifiable
(ATP 12) — extended in dated layers, never rewritten. Old layers stand; the map grows.

## Form

One JSON file per working night: `layers/YYYY-MM-DD.json`, listed in `layers/index.json`
(newest last). Each layer declares nodes and edges. Definitions:

- **Node** — something that exists on the map: material, a problem, a source, a work,
  an instrument, the practice itself, a concept. Node ids are unique across all layers;
  a node is declared once and referenced forever after.
- **Edge** — a connection that *operates*. Every edge carries at least one piece of
  evidence: a commit hash, a repository path, a citation with page, a URL, an artifact.
  **An edge without evidence is decoration and gets struck** (the relabeling test,
  foundation ch. 2). Edges are the practice's longitudes (relations of material).
- **Intensity** — a latitude (ATP 261): an affective/intensive annotation on a node or
  edge. Machine-attributed intensities are always marked `"estimate": true`. There are
  no unmarked intensities.

Node `type` and edge `relation` are free strings — the vocabulary is the practice's to
grow. Suggested starting types: `practice`, `source`, `problem`, `material`, `work`,
`instrument`, `concept`, `document`, `event`.

## Session

Every layer since the founding night has carried a top-level `session` object —
`executed_by` (the model disclosure floor rule 3 requires, mirrored from
`REGISTER.md`) and a free-text field describing the night. Neither field was ever
specified here; both grew informally, night to night, un-validated by
`validate.py` and unread by any rendering code. **From 2026-09-14, this is fixed:**
`session.executed_by` stays as it was; the free-text field is `summary`, **one
sentence**, naming the night and pointing to `nights/NN-*.md` for the account —
never a restatement of it. See the revision below for why and the evidence behind
it. Layers before this date keep their `note` field exactly as written; nothing
already committed is touched.

## Validation

`python3 atlas/validate.py` checks structure, id uniqueness, edge resolution, evidence
presence, estimate marking and manifest completeness. It validates the *schema*, never
the *worth*: whether a connection increases consistency is a question for deliberation
in the record, not for a script (the five criteria are topoi, never a grid).

The schema and validator are the practice's to revise — except the evidence principle,
which is floor (see `DOWRY.md`).

## Revisions

- **2026-08-15 (night 01).** Layer dates are the Europe/Berlin civil date of the
  session's wake — inherited from the founding layer's dating, and recorded as an
  inheritance (see `reading/01-postulate-4-the-night.md` §3). Where a date is already
  occupied, the newcomer's filename takes a lowercase suffix (`YYYY-MM-DD-a.json`);
  the `layer` field equals the filename stem. Occasion: founding and first working
  night share 2026-08-15. Reasoning and alternatives weighed:
  `nights/01-first-night.md`. Validator widened to match.
- **2026-09-14 (night 27, record 53).** `session.note` cut to `session.summary`,
  one sentence. Occasion: the founder's dated act of 2026-09-12 (`DOWRY.md`,
  "the cartographic condition is sharpened, with the measurement behind it" —
  apparatus at ~233,700 words against ~19,900 in `works/`) and his request of the
  same date naming the ratio a standing condition whose form is the practice's own
  to write (`REQUESTS.md`, 2026-09-12). Evidence, checked this session: `note` (or
  its list form) is present in all 55 committed layers, unread by `index.html`,
  `record.html`, `validate.py` or `consult.py` (grep of all four; the only rendered
  free-text field of this kind is edge-level `evidence[].note`, drawn by
  `record.html`'s connection list — a materially different thing, kept as is) —
  and it grew from one sentence at founding (187 characters, layer
  `2026-08-15-a`) to a full paraphrase of the night, the register entry and the
  edge evidence together (2,138 characters, layer `2026-09-12`), an elevenfold
  growth with no reader. Total standing weight: 55 occurrences, ~43,200
  characters, ~10,800 tokens — a fourth restatement of substance the night
  record, the register entry and this same layer's own edge evidence already
  carry, in a field the schema never named. Deliberation: `nights/53-*.md`.
  Nothing already committed is touched; `note` stands in every layer through
  `2026-09-12` as written.
