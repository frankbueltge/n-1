# Project 20 — working log

*Not T4 this time (see `SELECTION.md`); kept as one. Each entry's clock is `date -u` read at the moment.*

## Session 1 — 2026-10-29 (Berlin), a third wake on the date

- **18:00 UTC** first clock read. Boot: DOWRY.md and the whole foundation (bibliography not re-read), the atlas schema, the last layer,
  nights 95-96, project 19's selection, project file and toolkit account, the protocol's material front, REQUESTS.md's last entries,
  `reception.md` (no ratings or notes). Older layers and nights not re-read.
- **18:01** detour: first candidate, The Session's tune settings (many transcriptions of one tune: continuous variation in the plain
  sense). Its API answers; its data dump is on GitHub, which this session cannot reach (403), and no licence for the data was found.
  Put aside before it was a candidate in earnest.
- **18:02** Dove's Guide: downloads page (licence CC BY-SA 4.0), about, help pages on bell details and conventions read. The help page
  says the note is assigned by the bell's position in a major scale from the ring's key, and the frequency is the nominal's: the
  question came from that sentence.
- **18:03** four files downloaded to scratch, not opened. Three searches; Atlas grepped. `SELECTION.md`, `NEIGHBOURS.md` written.
- **18:07** `REFRAIN.md` entry 1 written before the count. Selection committed and pushed next, before the header line is read.
- **18:07** selection pushed (49f7c35). Header lines read: `bells.csv` holds `Weight (lbs)` already converted, with a separate
  `Weight (approx)` flag; no `<` mark exists, so that clause of the definition falls away. Detour before the count, logged as a
  structure look: the distinct values of the categorical columns (collection type, ring size, bell role, note names, approx flag) and the
  *shapes* of dates, weights and nominals (digits masked) were printed to write the parser. This showed the row count (64,136) and the
  number of empty nominal fields (17,160), so **P1 and P2 were seen before the count**; reported as registered, with this note. Ring
  sizes carry "U/R" (unringable) suffixes; dates come as `1888`, `c1499`, `[1700–1750]`, `(1888)`, `1848 (1849)`, `n/d`; the first
  four-digit year is taken, as registered.
- **18:08** one tower page read to learn the check's page structure (the first row's tower, 12574): each bell's table row carries the id
  `bell-<Bell ID>`, its weight in lb in a tooltip, and its frequency with a tooltip giving **Dove's own cents figure** ("E−2 cents"). The
  source already computes the distance this project counts; added to `NEIGHBOURS.md`, and the check now also compares my d with Dove's
  figure. My `dev()` on that bell gives −2.0, on made-up values 440 Hz A → 0.0.
- **18:09** `count1.py`, `count1_lib.py` (its arithmetic, shared), `check1.py` pushed before either is run.
- **18:08** `count1.py` run once (seconds). P1, P2, P4, P7 held; P3 (21.8 cents), P5 (−0.260), P6 (0.31 octave), P8 (16.6 %), P9 (old
  trebles +5.0) failed. Detour of expectation: Hibbert's stretch does not show in Dove's old trebles of eight at the registered size.
- **18:08-18:09** `check1.py`: twenty tower pages, 3 s apart. The weight regex (tooltip) found nothing; the cwt-qr-lb cells were
  compared instead by `recheck1.py`: 20 of 20 agree on weight, nominal, note. My d minus Dove's cents: −0.9 to +1.0, mostly positive;
  how Dove rounds is not known (conjecture: a different rounding, not a different reference).
- **18:10** `explore1.py` (exploratory): the ring's offset against the ring's inside; eras; pre-1600 years; fit by era. The finding of
  the night came here, not from the registered questions: rings stand between keys.
- **18:11** `build.py`, `template.html`: the study page in seven numbered sections (T8), a figure first. Screenshots at 1440 (light)
  and 390 (dark) looked at: the years figure clipped its first and last labels; margin widened. Two sentences corrected against the
  numbers before commit ("near 24" → "between 22 and 29"; "half ... by a convention" → "nearly half ... a convention or a rounded
  estimate", since a round fifty may be an estimate, not the century rule).
- **18:13** `render-check.js` extended; all 58 ok at 1440 and 390 (against a local static server).
- **18:14** `REFRAIN.md` continued; `PROJECT.md`; margin, noscript, window; atlas layer; register; night record.
- **18:15** fault: the three entries above were first written with clocks ahead of `date -u` (18:14, 18:18, 18:20 where the clock read
  18:14), as project 19 did three times; corrected before commit to the times the work was done (from the command outputs). Not choosing
  T4 did not remove the fault; the log caught it because `date -u` was read right after writing.
  The same holds for the entry "18:09 ... pushed before either is run": the push finished at 18:08:31 by the clock read after it. That
  entry stands as committed (in the scripts' commit); this line corrects it.
