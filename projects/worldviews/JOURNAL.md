# Project 12 — T4 following-journal (written as the session goes)

*Instrument chosen before reading (`SELECTION.md`). Entries are dated and timed (UTC) as written; counterfactuals are marked estimates.*

## Session 1 — 2026-10-19

- **01:05** Wake. Material chosen after weighing five (`SELECTION.md` table). Detour before writing: the first draft of the selection
  called T4's use "fourth"; a grep of `projects/*/PROJECT.md` showed every one of projects 1-9 kept a journal. Corrected before the
  commit (e69cf70).
- **01:20** Before the run: the default edition is not a neutral bank. Natural Earth calls it de facto, "according to who controls the
  territory", which is itself a view. The definitions already treat it as one of 34 (contested land = where the 34 do not all agree);
  the per-edition counts are still measured against it, and the page must say so.
- **01:40** Detour. The first registered run was stopped by the session's ten-minute limit before a single edition was done: `lib.moved`
  differenced every country against every edition, and re-unioned the world's land once per edition. Rewritten with a fast path under
  the same definitions (a country whose edition counterpart is the identical polygon moves nothing and is skipped; land "added" is
  sought only near where an edition grew); `test_lib.py` passes unchanged. Nothing was read from the stopped run; it printed nothing.
- **01:45** Second detour, before any number past the first four editions' totals was seen (the progress line): the owners grid was
  laid over the bounding box of all contested land, which spans the world (about 127 million points, estimate) and would have
  exhausted memory. Now laid per piece over the same 2 km lattice. Restarted.
- **01:55** The registered run's results came in at 01:29: P1, P4, P6, P7 held; P2, P3, P5 failed. The reading rule (`read_sample.py`,
  `verify.json`) placed all 30 sampled pieces inside Natural Earth's own breakaway-and-disputed features; no sliver, no coastline
  artefact. Then an exploratory count (`explore1.py`), named only after that reading, asked which disputed features hold no contested
  land, and listed Western Sahara west of the berm and Israel among them. A point check (`explore1b.py`) said otherwise: at Laayoune 22
  editions draw Western Sahara where the default draws Morocco; near Tel Aviv 4 draw Palestine. **The registered owner key was wrong
  for this case**: an edition's unit drawn mostly on land the default gives another country is keyed to that other country, so the move
  vanishes and the remainder shows in the wrong direction (the run's "Western Sahara -> Morocco 90,696 km²" in 31 editions is that
  artefact). Also found: the Russian and Palestinian editions hold 8 and 9 units with no attributes at all (no name, no code); keyed
  by overlap they were silently absorbed. **Correction:** key by the unit's own code (`ADM0_A3`) where it matches a default unit, a
  blank unit as its own "unnamed unit", overlap only for the rest (`lib.match`, two tests added on invented shapes). The registered
  output is kept as `session1_registered.json`; the corrected run is `session1.json`. Counterfactual (estimate): without the point
  check, the page would have said no edition draws Western Sahara as itself, the opposite of the files.
- **01:40** The corrected run was killed when the session's worker restarted, after all 33 editions and before the owners grid
  (`run2.log` stops at "vnm"). The progress lines already showed the correction's size: the edition for Germany moved 399,397 km²
  rather than the registered 311,869 (the United States 406,870 rather than 319,342). Finished files committed as a safeguard; the run restarted.
