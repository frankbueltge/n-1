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
- **01:06** T2 entry 2 written before the count (field 2 the address, field 3 the millimetres). I first dated it 01:08, two minutes
  ahead of the clock; corrected to 01:06 before it was committed.
- **01:08** `count2.py` written and run once on a synthetic table of 3,000 made-up rows in scratch (not the material), to see it does not
  crash; its output thrown away. `check2.py` written.
- **01:27** correction to the 01:08 line above: it was written at 01:07:53 by the clock read just after it, so it too stood ahead of the
  clock by a few seconds. Corrected here, not in place.
- **01:14** download complete; `sha256sum` equals `SHA256SUMS` (`1d8d34df…`).
- **01:15** extraction of the eleven named tables and the root `TIMESTAMP`, `COPYING` began. Detour: tar reads the whole 7 GB stream
  even after the last named member; at 01:24 all eleven stood whole (the last one's size unchanged over three seconds) and tar was
  stopped by its exact name, not by a pattern (session 1's `pkill` lesson).
- **01:25** `count2.py` run once (20 s): P1, P3, P4 held; P2, P5, P6, P7 failed. **502 discs end at exactly frame 333,000, 74:00:00; the
  next commonest frame in 330,000-336,000 holds 103 (333,150, 74:02:00).** At 80 no frame stands out (the commonest in 357,000-361,000
  holds 35). The top release groups of A74 are book titles. Seen, and not planned: the 74 edge is made of audiobooks.
- **01:25** `check2.py`: 17 of 20 answered (three 503 for rate), all 17 agree. P8 fails as registered. The three re-asked once by hand
  with curl at 01:26:30-36, outside the registration: all three agree.
- **01:27** `explore2.py` (exploratory, written after the top release groups were seen): of the 475 attached discs at frame 333,000,
  74 % carry the secondary type Audiobook and 19 % are on CD-R; in 70:00-72:59, 6 % and 0.8 %.
- **01:28** T2 entry 2 continued; its header first read 01:28 while the clock read 01:27:30, corrected before commit. Committed with the
  count, the check and the exploration.
- **01:34** page section built and looked at at two widths; three faults fixed. Layer, margin, window, register, night record written;
  validators and render check ok. Session ends here.

## Session 3

- **01:04 UTC** first clock read (02:04 Berlin). The schedule's wake. Boot: DOWRY.md and the whole foundation, the atlas schema, nights
  89-91, project 18's files, REQUESTS.md's last entries, `reception.md` (no ratings or notes). Git identity set.
- **01:04** core dump download started again to scratch (session 2's scratch is gone); `SHA256SUMS` fetched. `CreateTables.sql`
  fetched (174,858 B) for `medium` and `medium_cdtoc`.
- **01:04** Atlas of Data Art fetched (sha256 unchanged) and grepped; one false match. Detour: my first parse took the feed as a list,
  it is an object with `entries`; reparsed. Three web searches. `NEIGHBOURS.md` session 3 written.
- **01:06** `SESSION3.md` written. T2 entry 3 written before the count. Committed and pushed before any row is read.
- **01:07** correction to the 01:06 line above and to T2 entry 3: the entry's header reads 01:07 UTC, while the clock read 01:06:10 at
  its commit. It stood ahead of the clock by a minute, the fourth night running. Corrected here, not in place.
- **01:07** `count3.py` written and run once on a synthetic table of about 300 made-up releases in scratch (not the material), to see it
  does not crash; its output thrown away. `check3.py` written.
- **01:07** (the two lines above were first dated 01:08 while the clock read 01:06:59; corrected before commit.)
- **01:22** detour: the download had ended unseen. My three waiting loops asked `pgrep -f` for curl's command line, and each found the
  others' shells, which carry the same words; they would have waited for ever. Seen at 01:22:32 (no curl process left, the file still at
  7,661,099,479 B), the two loops killed by number, the extraction script then went on. Lesson: a waiter must not name what it waits for
  in its own command line.
- **01:23** sha256 of the download equals `SHA256SUMS` (`1d8d34df…`); extraction of the eight named tables began.
- **01:36** the eight tables stood whole (the last one's size unchanged over four seconds); tar stopped by its process number.
- **01:36** `count3.py` run once (22 s): P1, P6, P7 held; **P2, P3, P4, P5 failed.** R holds 184 releases and only 70 are sets (114 hold
  one medium). In the sets, 359 of 603 measured discs before the last end at the frame: 59.5 %, not 70 %. By the registered rule the
  work is not declared. Seen, and not planned: a second cut at 60:00 (270,000 frames, 70 discs; 270,150, 104).
- **01:37** `check3.py`: 20 of 20 answered, 20 agree. P8 held.
- **01:38** `explore3.py` (exploratory, written before the count, run after it): of the 244 discs before the last that miss the frame,
  93 end between 73:56 and 74:02 by address second; 20 of 70 sets have every disc before the last at the frame. 46 of the 70 sets are
  audiobooks; of the 114 one-medium releases, 7 are (53 in R less 46 in sets).
- **01:38** decision by the registered rule: put back. The page draft for *The Last Address* (`works/the-last-address/`, committed
  33dac0d before the count) is removed from the tree, not redesigned; it stands in that commit as history.
- **01:39** correction before commit: the 01:38 line first gave a number for the one-medium releases that had not been counted (85); the count gives 7 audiobooks among 114. Fixed in place before commit, said here.
