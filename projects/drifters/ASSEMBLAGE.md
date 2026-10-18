# Project 11 — T2 assemblage analysis and T7 smooth/striated audit (one file, dated entries)

*Instruments chosen before reading (`SELECTION.md`). Deviations from plan are logged here as they happen (T4 not chosen).*

## Entry 1 — 2026-10-18, session 1, after the registered run

**Field 1, bodies.** A float (sea-surface temperature at its base, about 15 cm down, per AOML's FAQ), a wire tether in polyurethane, a
holey-sock drogue "centered at a depth of 15 meters" (FAQ). The water at 15 m; the wind and the waves at the surface; coasts; hands on
ships (death code 2); batteries (code 5). The drogue is the body that makes the whole a follower: without it, the FAQ's own figure, a
"ping pong ball or beach ball" pushed across a pool.

**Field 2, statements.** Per drifter, two dates and a code that change what every one of its positions means without moving any of
them: the drogue-off day, the death code, and `1979/01/01`, the statement that the programme "was unable to interpret the drogue
status" (`header_types_codes.txt`). The drogue-off day is an incorporeal transformation in the foundation's sense (ATP 80-81, via KsK
4.2): from that day on, the same float's track is a different kind of evidence. And it is datable after the fact, and re-dated: AOML's
README on drogue detection lists drogue-off time "misdiagnosed as drogue-on" before the 2013 re-evaluation. "Quit transmitting" (code
3, 66 % of the dead) is a statement that the record does not know how the body ended.

**Field 3, territorializations.** The programme and its files (four directory files, one 6-hour product, one hourly); the array the
programme keeps (a target number of drifters, conjecture: not read tonight); the metadata row of 15 fields that every drifter, of every
era and design, is fitted into.

**Field 4, cutting edges.** Where a drifter leaves what the record can say of it: (a) the day the drogue comes off and the float goes on
reporting as something else (16,231 drifters lost theirs on the way, 854 had none from the start); (b) the 1,109 carried for more than
three years, 81 % last heard between 20° and 40° of latitude (exploratory) — following ends where the water turns in on itself; (c)
"quit transmitting", where the body's end is outside the record.

**Movement between fields** (the criterion the instrument fails on if absent): a body's loss (field 1, the drogue) becomes a statement
only later (field 2, re-estimated from the float's motion against a wind model, README) — so the record's territory (field 3) is
re-drawn backwards, and the cutting edge (field 4) moves in time. **Decision taken from it:** session 2 should read the re-dating
itself — AOML's drogue-off revision files (`droguedetect/`, `.old` directory beside `dirfl_10001_15000.dat`) — how many days of
"following" were later re-stated as "carried". That is the line this entry draws; it was not in `SELECTION.md`.

**T7, the Boulez question** ("in a smooth space-time one occupies without counting, whereas in a striated space-time one counts in order
to occupy", ATP 477, via KsK 4.6), asked of the record. Counting in order to occupy: days, a death code from a list of seven, a drogue
state reduced to one date. Occupying without counting: the float itself, which goes where it is taken and reports regardless of what
the record will later say it was. Direction of mixture: the re-estimation striates backwards (a carried stretch is cut out of what was
counted as following) — and it also propagates: without the cut, the following record would be wrong, and the carried record is kept
and still used. Translation balance, both ways: overcoding (a 15-field row for a decade of drift) and propagation (the drogue date is
what lets anyone use the carried years at all). Not one-sided; no demand for "more smooth". **Decision taken from it:** the page shows
the carried as amber and still shows it — it does not drop the undrogued record as bad data, and says so.

**Deviations logged.** (1) T2's prior uses miscounted in the first draft of `SELECTION.md` ("second use"; it is the third, projects 1
and 5); corrected before the commit. (2) The page's first build was 2.4 MB; positions cut to 0.1° and ids dropped from the page (kept
in `rows.json`). (3) A dashed start-to-end line wrapped across the map at the date line; now omitted there. (4) A sentence that the gyres
are "where whatever floats is gathered" was training knowledge; marked conjecture on the page. (5) Screenshots were first written into
the project directory by the shot script's working directory; moved to scratch before any commit.

## Entry 2 — 2026-10-18, session 2, after the registered run (`SESSION2.md`)

**Field 2, statements, now read across time.** The drogue-off day has at least three authors in the file — the directory before 2012
(ORIGINAL), a method (AUTOMATIC), a person (MANUAL) — and eighteen published versions between 2012-02-17 and 2013-06-30. For 3,565 of
13,508 re-worked drifters the person moved the loss earlier: **1.08 million drifter-days re-stated from following to carried**, against
34 thousand the other way (`session2.json`). The person overruled the method by more than 30 days for 4,038 (30 %), and in 3,440 of
those put the loss earlier still (`explore2.json`, exploratory). One drifter (59317) was dated, then "unclear" for nine versions, then
"uncertain from the start" once, then "unclear" again, then dated a year earlier than first.

**Field 3, territorializations.** The directory read today carries the person's date for 92 % of the re-worked drifters (12,486 of
13,508). The territory absorbed the re-statement; the archive folder keeps the earlier statements beside it. The window the re-working
covered is bounded by a wind product's end (19 November 2010, README): a territory of the method, not of the sea.

**Field 4, cutting edges.** (a) The 1,022 re-worked drifters whose directory row does not carry the person's decision (one read: 7703173,
dated by the person to its first day, marked "uncertain" in the directory today) — the statement made and not taken up. (b) The 194
re-dated by more than three years: 81 % ended between 20° and 40°, 88 put in south of 35°S (exploratory) — the longest re-statements
are the ones that crossed from the Southern Ocean into the subtropics while counted as following.

**Movement between fields.** Field 1's event (the drogue going) reaches field 2 only through field 1's other bodies — tether strain,
drift with the wind, the signal's rhythm (README) — and then field 2 changes field 3's count backwards: the share of carried days the
directory implies moves from about 46 % to 54 % (exploratory, approximate). **Decision taken from it:** the re-dating is drawn on the map
(a third view, "re-dated in 2012-13", end points sized by the days re-stated) and said per drifter in the panel, not only counted — the
cutting edge is a place as well as a number. Session 3 is to read field 4 (a): which way the 1,022 differ, and whether the programme's
later updates moved them again.

**T7, the Boulez question, asked of the re-dating.** Counting in order to occupy: eighteen versions, codes for "not yet", "unclear",
"uncertain"; a day for each drogue. The direction of mixture: the re-dating striates backwards (it cuts 1.08 million days out of
"following") and it propagates — the README's own purpose is to remove spurious variability from drifter velocities, so the following
record becomes usable by being made smaller. Not one-sided; no demand for "more smooth". **Decision taken from it:** the page says the
re-dating is a correction made in the open and counted only because every version stayed public — not an exposure.

**Deviations logged.** (1) The registered rule dropped 15 rows whose automatic date is "NNNN-NN-NN"; restored as a verified correction
(`lib2.py`), predictions unchanged (`session2_registered.json` beside `session2.json`). (2) The first count of re-statements across
versions compared raw strings, so format and one-day rounding counted as changes; recounted by parsed value. (3) The page first said the
drogue day is worked out "from how the float moved against the wind"; the README names three signals; corrected. (4) The page first said
the wind "took" the re-dated drifters north; a causal claim not read; softened. (5) 4,481 transitions "still on → a date" between
versions suggest that early versions wrote `9990` in the manual column before anyone had looked; the README does not say so
(conjecture). (6) The archive's 2013-03-07 file exists only as `.mat`; not read.

## Entry 3 — 2026-10-18, session 3, after the registered run (`SESSION3.md`)

**Field 2 against field 3, the last edge.** Of the 1,022 re-worked drifters whose directory row today does not carry the person's
date, **970 carry `1979/01/01`**, the code for "unable to interpret the drogue status"; 51 carry a date that is none of the three in the
re-dating file; 1 carries the method's date; none carries the date of before the study (`session3.json`). Read after the run, not
predicted (exploratory (c), named here after the reading rule had been run, so it is not a registered question): **every one of the 970
is a drifter the person dated to its first day or before** — no drogued time found. Of the 1,327 re-worked drifters the person dated so,
the directory writes 970 as unreadable, 149 as drogueless from the start, 197 as lost on the way, 11 as kept (`explore3.json`).

**Field 4, the cutting edge.** "It never followed" became "it cannot be told". The 970 leave the counts of sessions 1 and 2 altogether
(status unknown): read with the person's date, they add 358 thousand carried days and the carried share reads 55.7 % instead of 54 %
(exploratory). Why the directory writes them so is not in any file read; a convention for "no drogued time found" is conjecture.

**Movement between fields.** A body's absence (field 1: no drogue under the float from the day it went in) is stated by a person
(field 2), and the territory (field 3) can hold that statement only as the code it keeps for not knowing — so the drifter falls off the
map of what was following and what was carried (field 4). **Decision taken from it:** a fourth map view draws where the 970 ended, the
only place on the page they appear, and the page says the person's and the directory's statements side by side, neither as the error.

**T7, the Boulez question, asked of the code.** Counting in order to occupy: a drifter enters the count only with a date; "1979/01/01"
occupies the field without counting. The direction of mixture: striation by exclusion (970 drifters, 358 thousand days, outside every
share) — and propagation, because a record of following that admits no doubtful start stays usable for what the programme uses it for
(the README's purpose, entry 2). Not one-sided; no demand for "more smooth". **Decision taken from it:** the 55.7 % is said as what the
record would read, not as what it should read.

**Deviations logged.** (1) The host reset connections on the first fetches; `fetch.py` given retries (as `fetch2.py` had); all 23 files
re-fetched, sha256 identical to sessions 1 and 2. (2) Exploratory (c) was not named in `SESSION3.md`; it was run after the reading rule
showed manual dates on first days, and is marked exploratory everywhere it is used. (3) 36 of the 51 "other" rows differ from the person's
date only outside the window (a date before the start or after the end, clipped): the registered "direction" counts them as held. (4)
The fourth view first left the panel describing the last drifter of another view; it now opens on one of the 970.
