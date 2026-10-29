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
