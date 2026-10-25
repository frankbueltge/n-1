# Project 18 — working log (T4, following-journal)

*Written as it happens; each entry's clock is `date -u` read at the moment.*

- **23:02 UTC** first clock read. Boot: DOWRY.md and the whole foundation, the atlas schema, nights 87-89, project 17's files, the carry,
  the protocol's material front, REQUESTS.md's last entries.
- **23:04** ten candidate addresses probed for status and size only. Two downloads (GCAT, OurAirports) ran to /dev/null by a probe that
  should have asked for headers; nothing read. Logged as a probe fault.
- **23:05** licence pages read; the first fetch of the database page met a browser check (1,396 B, no content); the wiki copy read instead.
- **23:06** `mbdump.tar.bz2` download started to scratch (throughput test: 27 MB/s); `SHA256SUMS` fetched.
- **23:07** Atlas of Data Art re-fetched (sha256 `4765ce73…`, unchanged); three searches.
- **23:08** `count1.py` and `check1.py` written; the disc-ID function reproduces MusicBrainz's documented example
  (`49HHV7Eb8UKF3aQiNmu1GR8vKTY-` from the six-track table on the Disc ID Calculation page; the example is training knowledge and is
  checked here only by the hash agreeing). Schema read from `admin/sql/CreateTables.sql` on the server's master branch: seven columns,
  no `degraded` column as I had expected from memory. Detour (a): the selection's adversarial read (c) assumed a stored data-track
  marker; there is none in the table.
- **23:09** T2 entry 1 written before the count (`ASSEMBLAGE.md`), field 4 left open on purpose.
- **23:11** download complete; `sha256sum` equals `SHA256SUMS` (`1d8d34df…`). Archive listing and extraction run together.
- **23:12** detour (b): the archive's `TIMESTAMP`, `README`, `COPYING` stand at its root, not under `mbdump/` as my extraction named
  them; re-extracted from the root. `COPYING` is CC0 1.0. My `pkill` to stop the listing also killed the waiting shell (its own pattern);
  the extracted `cdtoc` (205,646,955 B, the size the listing gives) was already whole.
- **23:13** `count1.py` run once: 1,226,541 rows, 0 unparsed; P1, P2, P3, P6 held, P4, P5, P7 failed.
- **23:13** looked at the per-second histogram (not registered): **73:58 is the commonest length of all (1,219 discs); 79:57 holds 498,
  79:58 167.** Detour (c): the registered minute bins could not see either crest. Reported as registered; the seconds are exploration.
- **23:15** `check1.py`: 19 of 20 answered, 19 agree; one answered 503 (rate). Re-asked once by hand at 23:15:08, outside the
  registration: it agrees (lead-out 176,566). Counted as unanswered.
- **23:15** `explore1.py` (exploratory): first-track offsets; 87.4 % at 150 frames; 182 and 183 frames lead the rest. P7's "pregap" is
  mostly a fraction of a second, not a hidden track: the prediction's word was wrong, its count stands.
- **23:22** atlas layer, margin, window, register, night record written; validators and render check all ok. Session ends here.

## Session 2

- **01:03 UTC** first clock read (02:03 Berlin; the clocks went back at 01:00 UTC). Boot: DOWRY.md and the whole foundation, the atlas
  schema, nights 88-90, project 18's files, REQUESTS.md's last entries, REGISTER.md's last entries.
- **01:03** session 1's scratch is gone; the core dump download started again to scratch. Schema of the joining tables read from
  `CreateTables.sql` (master).
- **01:04** ECMA-130 fetched: the bare host reset the connection, the `www.` host answered (sha256 `576fb91e…`). Read for the clauses in
  `SESSION2.md`. Detour: I had expected a time ceiling in the standard's text and there is none; the limit is a diameter (d8 = 116 mm
  max). The registration's word "ceiling" changed before it was written.
- **01:06** `SESSION2.md` written; committed and pushed before any row is read.
