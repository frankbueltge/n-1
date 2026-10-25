# Project 18 — T2 assemblage analysis

*KsK T2: four fields, the movement between them, no field derived from another (ATP 88-90, 503-505, via KsK §4.2 and ch. 6). Failure:
field 4 stays empty or without consequence, or no movement between the fields is described. Each entry dated; earlier entries stand.*

## Entry 1 — 2026-10-25, session 1, written before the count

**Field 1, bodies.** A polycarbonate disc 12 cm across with a spiral of pits; a laser and a drive that read it; a lead-out ring after the
last track; a computer the disc was put into; a person who put it there; a server that keeps the table. *(Disc geometry and the frame rate
are training knowledge, conjecture until a source is read.)*

**Field 2, statements.** A standard that states how long a disc may be; the table of contents the drive reads, in frames of 1/75 s; a
hash that turns that table into a 28-character name (`count1.py`, reproduced on MusicBrainz's documented example); a database row; a
licence that places the row in the public domain (`SELECTION.md`, rights). The incorporeal transformation (ATP 80-81): a disc becomes a
*known* disc the moment its table is hashed and the hash attached to a release; from then on any drive that reads the same table is told
what it holds.

**Field 3, territorializations.** The ceiling (74, later 80 minutes, conjecture); the frame as the unit; the two-second pregap before
track one; the rule that one table names one pressing, so that the database counts pressings and never copies.

**Field 4, cutting edges (to be filled from the count, not before).** Candidates named now so the count can refuse them: discs past the
ceiling; audio hidden before track one; tables that do not reproduce their own name.

**Movement, expected.** Field 3 (a ceiling) is said to have been set by a field-2 statement about a single work (the Ninth); the count can
show only whether bodies (discs as pressed) press against it. Whether the instrument moves a decision is asked after the count.

## Entry 1, continued — after the count (23:16 UTC)

**Field 4, cutting edges, from the count** (`session1.json`, `explore1.json`). Of the three candidates named before, one held as a cutting
edge and two did not. *Held:* 3,959 discs (0.32 %) play at or past 80:00, thinning minute by minute to 89 (93 discs) and almost nothing
after; and 84 tables whose lead-out lies past 99:59.74, up to one that claims 22 days, which no pressed disc can be (conjecture as to cause:
a drive or program reporting a wrong lead-out). *Not held:* every one of 1,226,541 tables reproduces its own name (the hash refuses
nothing), and the "hidden track" before track one is mostly not there: 12.6 % of discs start later than two seconds, but 144,753 of those
by under one second (182 and 183 frames lead, 112,000 discs between them); 9,610 (0.8 %) by a second or more.

**Movement between the fields.** The territory (field 3) does not show where the story put it. In whole minutes neither ceiling shows:
minute 73 is a crest, minute 79 is lower than 70-78. In seconds both do: **73:58 is the single commonest length of all 1,226,541 discs
(1,219), and the count falls by two thirds between 79:57 (498) and 79:58 (167).** 73:58 and 79:58 are each two seconds short of 74:00 and
80:00, the length of the standard pregap before track one (the playing length here starts at track one, field 2's definition). So a
statement (the 2-second pregap, field 2) displaces the territory (field 3) by exactly its length in what the bodies (field 1) show; the
ceiling is met by the disc's address, not by its music. That is a conjecture from arithmetic, not from a read standard, and it is the first
thing session 2 tests.

**Consequence (the failure criterion asks for one).** Field 4 moves session 2: the unit to read is not the minute but the second, and the
question is which discs sit on the two crests (what releases, of what kind, when pressed) against the discs around them. The minute
histograms the selection registered would have hidden both crests; they stand as registered and are not the page's main figure.

## Entry 2 — 2026-10-25, session 2, written before the count (01:06 UTC)

**Field 2, statements, from the standard read tonight** (ECMA-130, `SESSION2.md`). The table of contents does not state a length. It
states addresses: each track's start, and under pointer A2 "the address of the first Section of the Lead-out Track", all "in absolute
time" from the start of the user data area, the 2-second gap before track one counted in. Session 1's playing length (lead-out minus
track one) is my statement, not the disc's. The disc's own statement is the address.

**Field 3, territorializations, moved.** The ceiling I carried into session 1 as minutes is not in the free standard at all. Its
territory is a diameter (d8 = 116 mm max) and two tolerances (pitch, velocity); minutes are what a manufacturer's choice inside those
tolerances turns the diameter into. So the territory has two layers, a body's (millimetres, field 1) and a statement's (the address a
drive reads, field 2), and the count can only see the second.

**Movement, expected.** If discs stop at an address second (P1, P3, P4), the edge they meet is the statement's, not the body's: nothing
in the millimetres falls on 74:00 or 80:00. If they stop smeared across seconds, the body's tolerances are showing through the address.

**Field 4, to be filled from the count.** Named now so the count can refuse them: discs at the edge that are compilations (P5); the old
edge kept by old discs (P6); burnt discs (CD-R) at the new edge (P7).

## Entry 2, continued — after the count (01:27 UTC)

**Field 4, cutting edges, from the count** (`session2.json`, `explore2.json`). Of the three candidates named before, none held as named.
Compilations are not the 80 edge (59 % of B80 against 63 % of C76, P5 failed); the old edge is not kept by old discs (median year 2007 at
74:00, 2009 at 79:55-79:59, P6 failed); burnt discs are not the new edge (2.6 % CD-R at B80). What the count found instead: **at 74:00:00
the discs stop on one frame. 502 lead-outs at exactly 333,000; three quarters of those attached are audiobooks.** A book does not end at
74 minutes; a program that cuts a reading into discs does, at the last address the disc is said to hold.

**Movement between the fields.** Entry 2 expected one of two pictures and the count shows both, one at each edge. At 74 a statement (the
address 74:00:00, field 2) makes the body (field 1): a long reading is cut where the number says, to the frame, and the result is the single
commonest disc length of all. At 80 the bodies show through: discs crowd the last seconds and stop over three or four seconds (495, 169,
102, 80 from 79:59 to 80:02), no frame standing out, music filled toward a limit that each pressing meets a little differently. The
territory (field 3) is two kinds of thing: at 74 an order-word obeyed exactly (ATP 76, via KsK §4.2), at 80 a margin.

**Consequence.** Field 4 moves session 3: the work, if there is one, is at the 74:00:00 frame, where a machine's cut of spoken books
became the commonest length a compact disc has. Not triggered.
