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
