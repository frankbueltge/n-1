# Project 23 — the working journal (T4 following, T5 refrain)

*Two lenses of one journal (KsK ch. 6, instrument economy). T4: detours and abandonments as they occur, clocks read from `date -u` at
the moment, never written ahead. Failure: written after the fact, or no deviation from plan registered. T5 entries are marked **T5**:
which aspect of the refrain dominates, components of passage, an opening test (ATP 311-313, 325, 328-329, via KsK §4.5 and T5). Failure:
the entries sequentialise the three aspects, or the opening test never shifted, prevented or placed an opening.*

## Session 1 — 2026-11-07

- **02:03** Wake. Boot: DOWRY.md, the whole foundation, the atlas schema, the last layer, nights 103-105, project 22's files,
  REQUESTS.md's recent entries, `reception.md`.
- **02:04** Candidate: the tz database. Atlas of Data Art grepped (no hit); one web search, which named a hand-kept lead-time tracker
  (Parenti), read in its announcing message. 276 tarballs downloaded to scratch, not opened.
- **02:05** `SELECTION.md` written and committed (12275e3), pushed before any tarball was opened.
- **02:06** The newest release opened. Its `NEWS` dates every release by a line "Release X - date time zone" — with the time and the
  zone, which the registration did not expect; the registered definition (the date, at 00:00 UT) is kept. Release labels in `NEWS` are
  composite ("code1998h-data1998i"); the data part is matched. The data files say "This file is in the public domain".
- **02:07** `count1.py` written; a synthetic run of two hand-made releases (one censored change, one late by 30 days, one zone arriving
  with its history) gave the expected rows. Pushed (d8c24f5) before the run. Run once → `session1.json` (5 s).
- **02:07** **Detour 1.** 61 of 275 releases failed to compile: every release before 2000f. Their data type two rule years "even" and
  "odd", and the compiler runs a helper command `yearistype` for that, which this machine's compiler no longer has. By the registration
  they are left out; so the compiled archive starts in October 2000, and every change between 1997 and then that older releases had
  carried looks late. The registered peak year (2000) and the registered early late share (34 %) are that edge, not the world.
- **02:08** **Detour 2.** Exploratory: a two-line helper written (`helper/yearistype`, even/odd only, the only types the old data use)
  and the same script run again with it on the path → `explore1.json`: 252 releases compile, from 1996h. The 23 still failing are older
  than the window. Seen only after the registered run.
- **02:08** **Detour 3.** The registered check (`check1.py`, zdump) holds for 8 of 12; P11 fails. In the four failures the earlier
  release already showed the new offset at the instant: the change had been carried at a slightly different moment, and the "late"
  release re-timed it. The adversarial read (a) named this and left it unfiltered; it is a quarter of the sample. `explore1c.py`
  separates it: of 393 late, 114 are news arriving late (the old offset still shown on the day), 51 re-timings, 228 more than a year late
  (the past rewritten).
- **02:09** `explore1b.py`: per year, events. The late news thins out (none since 2023); short notice does not.
- **02:10** `build.py` → `index.html`. Two sentences changed before commit: "the world's software showed the wrong hour" (no device is in
  this material) → "software that relied on it showed the old hour"; a clause on how Gaza's clock dates are announced (no source in
  hand) struck, the count of events kept.

**T5, session 1.** Dominant aspect: the circle around home — a reader and a compiler made to hold thirty years of one file still; but
the hold in chaos is in the material, not in me: a daylight-saving rule is a metre laid on the year, and the database's whole labour is
to keep that metre ahead of the day. The late arrivals are where rhythm beat the metre ("Meter is dogmatic, but rhythm is critical",
ATP 313, via KsK §4.5). **Component of passage:** the release — the converter between a decree and a device (ATP 325, via KsK T5);
and, found tonight, a second one inside the tool: the helper `yearistype`, the old compiler's door to an outside program, closed in
today's compiler, through which the oldest releases no longer pass. **Opening test:** the opening I had planned for session 2 was
"announcement against effect" (the neighbour's question). The check moves it: the self-created point is the distinction this
material makes itself between news and re-timing — two releases that disagree about an hour the world had already lived. Session 2 is
registered there, not at the neighbour's door. The test shifted an opening; not triggered.

## Session 2 — 2026-11-09

- **02:02** Wake. Boot: DOWRY.md, the whole foundation, the atlas schema, the last layer, nights 104-106, this project's files,
  REQUESTS.md's recent entries, `reception.md`. No night ran on 2026-11-08 (no layer, no commit); none is reconstructed.
- **02:03** Read first, as session 1 asked: the neighbour's index and 2025 page (one change, Chile's Aysén, notice to release 14 d);
  IANA's paragraphs on notice; Johnson-Pint's article on the timing of time-zone changes, in full.
- **02:04** The 276 tarballs fetched again (the container is new); the concatenation's sha256 equals session 1's prefix. Not opened.
- **02:05** `SESSION2.md` written. **Detour 4 (in the registration, not the material):** session 1 planned to separate the kinds of
  lateness by counting transitions; the question moved to the hour, because one late transition can leave a file wrong for an hour or a
  year, and a count of transitions cannot weigh that.
- **02:06** `count2.py` written; a synthetic run of five hand-made releases. **Detour 5:** the first synthetic case failed — a re-timing
  the hand-made archive never corrected before the final came out "past rewritten", as the registered order of kinds says it must. The
  case was wrong, not the script: a fourth release correcting it within the year was added, and the three kinds came out as built.
- **02:07** Count run once → `session2.json` (11 s). *(This entry and the next written at 02:15, after the fact; the 02:07 is the
  clock read when the count ended, the next entry's minute was not read at the moment and is given as the window it fell in.)* Ten of eleven held so far; P10 failed (77 % of the hours one hour off, not 90 %:
  17 % are two hours off, and 1,477 hours in Pacific/Fakaofo twenty-three). `check2.py` (zdump) holds for 11 of 12; P11 held. The
  twelfth: zdump returned no reading in its range for Antarctica/Casey in 2009p (the file has no change after 1969); read without a
  range it agrees with count2 (+08). Logged as a limit of the check, the registered result unchanged.
- **02:08-02:14** **Detour 6.** The page builder's first sentence on the longest stretch (Antarctica/Vostok, 21 years) wrote the offsets of
  its first instant (UT+3 h shown, +7 h final) as if they held throughout; the stretch is one hour off in all but 552 of its 187,680
  hours. zdump on 2010a and 2026f: +6 against +7; the first weeks are release 2001a's Moscow time. The sentence and the margin note
  were rewritten before commit. Figure 2 looked at in a screenshot; the clipped last year label removed.

**T5, session 2.** Dominant aspect: the opening, and it is the material's, not mine — the hours a file was wrong about the present are
where the database's hold on the day broke, and most of them broke without anyone knowing: four fifths were found wrong only years later.
The circle around home held (the same compiler, the same helper, the same 276 files by checksum). **Component of passage:** the release
again, and a second one found tonight — the final release itself, which converts every earlier release's present into a past it may
overrule; it is the only judge of "wrong" this study has, and the registration says so. **Opening test:** the planned opening (session 1:
news against re-timing, counted in transitions) was moved before the count to the hour, because a transition cannot weigh how long a
file was wrong; and the count moves session 3's opening again: the hours found wrong years later are not a residue to filter but the
larger part, and they fall on stations, atolls and provinces the record learned late. The test shifted an opening; not triggered.
