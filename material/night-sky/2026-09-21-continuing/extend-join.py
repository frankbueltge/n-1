#!/usr/bin/env python3
"""Assemble a continuing-look act's join.py from the previous act's committed
original — the assembly as committed code, carried forward (night 31, record
57, 2026-09-21).

Night 23 committed this procedure after the assembly slipped by hand three
consecutive sessions (its docstring holds the pattern's history); the rule it
set is the scan's and the asking script's: the next act carries the body
forward unchanged — verified identical before the run — and edits only the
PARAMETERS block below. Tonight is the fifth ordinary carry-forward, after a
four-session gap (nights 27-30 each declined to run this front): the standing
body is night 23's, byte-identical; only the parameters are tonight's, and
they carry nine new civil dates and six new wakes at once rather than the
usual one or two.

Every edit is verified before the write: each anchor must occur exactly once,
the result must hold exactly one docstring and parse as Python. On any failure
nothing is written.

Run from the act's directory: python3 extend-join.py
(writes join.py beside itself; then: python3 join.py)
"""

# --- PARAMETERS (the per-act block; everything below it is the standing body) —
PREV = "../2026-09-12-continuing/join.py"  # the previous act's committed original

# the previous act's last WAKES entry, verbatim, and the new entries to follow it
WAKE_ANCHOR = ' ("night 26","record 52","2026-09-12T01:02:50Z"),\n]'
NEW_WAKES = (' ("night 26","record 52","2026-09-12T01:02:50Z"),\n'
             ' ("night 27","record 53","2026-09-15T01:04:43Z"),\n'
             ' ("night 28","record 54","2026-09-16T01:06:33Z"),\n'
             ' ("night 29","record 55","2026-09-18T01:05:34Z"),\n'
             ' ("night 30","record 56","2026-09-19T01:06:44Z"),\n'
             ' ("night 31","record 57","2026-09-21T01:04:50Z"),\n]')

# the previous act's last input line, verbatim, and its replacement
# (the previous act's own slice moves to its directory path; the nine new
# slices stand bare, beside the new join.py)
INPUT_ANCHOR = '             "tempelhof-N-2026-09-10.csv"):'
NEW_INPUTS = ('             "../2026-09-12-continuing/tempelhof-N-2026-09-10.csv",\n'
              '             "tempelhof-N-2026-09-11.csv",\n'
              '             "tempelhof-N-2026-09-12.csv",\n'
              '             "tempelhof-N-2026-09-13.csv",\n'
              '             "tempelhof-N-2026-09-14.csv",\n'
              '             "tempelhof-N-2026-09-15.csv",\n'
              '             "tempelhof-N-2026-09-16.csv",\n'
              '             "tempelhof-N-2026-09-17.csv",\n'
              '             "tempelhof-N-2026-09-18.csv",\n'
              '             "tempelhof-N-2026-09-19.csv"):')

NEW_DOC = '''"""Join: every recorded wake x the sky's record - the continuing look, eighteenth
act (night 31, record 57, 2026-09-21, the schedule's hour arriving late after a
four-session gap).

Extends night 26's join (../2026-09-12-continuing/join.py) by five wakes (nights
27, 28, 29, 30 - each a session that declined to run this front - plus night 31,
tonight) and by nine new civil dates (2026-09-11 through 2026-09-19), which
entered the archive's recent window with the generation dated 2026-09-20 08:18 -
the drawer turned nine times since the last reading, the largest jump this vigil
has recorded (every prior act turned it at most twice). Three of the nine
entering dates are doubly absent (2026-09-13, -14, -17: no wake ever fell in
them); six of the practice's own wake hours get their sky written for the first
time in this single act - nights 25, 26, 27, 28, 29 and 30 - where every prior
act wrote at most two. The unwritten wake after this act is tonight's own
(2026-09-21 01:00, beyond the window's end).

Inputs, all committed:
- ../2026-08-22-prospect/tempelhof-N-2026-08-14--2026-08-21.csv  (DWD station
  00433, hourly total cloud cover V_N in eighths, MESS_DATUM in UTC; Source:
  Deutscher Wetterdienst, CC BY 4.0)
- ../2026-08-24-continuing/tempelhof-N-2026-08-22.csv  (the eighth civil date)
- ../2026-08-25-continuing/tempelhof-N-2026-08-23.csv  (the ninth civil date)
- ../2026-08-28-continuing/tempelhof-N-2026-08-24.csv, -2026-08-25.csv,
  -2026-08-26.csv  (the tenth, eleventh and twelfth civil dates)
- ../2026-08-29-continuing/tempelhof-N-2026-08-27.csv  (the thirteenth)
- ../2026-08-30-continuing/tempelhof-N-2026-08-28.csv  (the fourteenth)
- ../2026-08-31-continuing/tempelhof-N-2026-08-29.csv  (the fifteenth)
- ../2026-09-01-continuing/tempelhof-N-2026-08-30.csv  (the sixteenth)
- ../2026-09-02-continuing/tempelhof-N-2026-08-31.csv  (the seventeenth)
- ../2026-09-03-continuing/tempelhof-N-2026-09-01.csv  (the eighteenth)
- ../2026-09-03-a-continuing/tempelhof-N-2026-09-02.csv  (the nineteenth)
- ../2026-09-05-continuing/tempelhof-N-2026-09-03.csv  (the twentieth)
- ../2026-09-06-continuing/tempelhof-N-2026-09-04.csv  (the twenty-first)
- ../2026-09-08-continuing/tempelhof-N-2026-09-05.csv, -2026-09-06.csv  (the
  twenty-second and twenty-third civil dates)
- ../2026-09-09-continuing/tempelhof-N-2026-09-07.csv  (the twenty-fourth)
- ../2026-09-11-continuing/tempelhof-N-2026-09-08.csv, -2026-09-09.csv  (the
  twenty-fifth and twenty-sixth civil dates)
- ../2026-09-12-continuing/tempelhof-N-2026-09-10.csv  (the twenty-seventh)
- tempelhof-N-2026-09-11.csv .. tempelhof-N-2026-09-19.csv  (the twenty-eighth
  through thirty-sixth civil dates; committed tonight)
- the wake list below: night 26's 53 wakes verbatim, plus nights 27-31.

Where the same MESS_DATUM appears in more than one committed slice, the value is
read from the OLDEST slice that carries it - the archive's first telling in the
practice's committed record - so the join preserves each hour as it was first
committed, and the rewrite frontier is measured separately (see the README and
indicator-rewrite-frontier.txt). Newer slices only add hours the older ones did
not reach.

Output: join.json - one row per recorded wake: UTC and Berlin-local time, the
geometric solar elevation at Berlin-Tempelhof (52.4676 N, 13.4020 E; NOAA-style
low-accuracy algorithm, no refraction - a computed estimate, not an observation),
a twilight class from that elevation, and the station's cloud cover at the wake
hour and the following hour (None where the archive does not yet reach).

Re-run: python3 join.py   (writes join.json beside itself)
"""'''

# --- the standing body: verify every anchor, edit, verify the result, write —
import ast
import os

here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, PREV)).read()

a = src.index('"""')
b = src.index('"""', a + 3) + 3
old_doc = src[a:b]
assert old_doc.startswith('"""') and old_doc.endswith('"""') and len(old_doc) > 6, \
    "docstring extraction failed"
src = src.replace(old_doc, NEW_DOC, 1)

assert src.count(WAKE_ANCHOR) == 1, "wake anchor not unique"
src = src.replace(WAKE_ANCHOR, NEW_WAKES, 1)

assert src.count(INPUT_ANCHOR) == 1, "input anchor not unique"
src = src.replace(INPUT_ANCHOR, NEW_INPUTS, 1)

assert src.count('"""') == 2, "result does not hold exactly one docstring"
ast.parse(src)

open(os.path.join(here, "join.py"), "w").write(src)
print("join.py assembled: 3/3 replacements verified, syntax OK")
