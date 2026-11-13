# Project 24 — map (T1 mapping protocol)

*Revised each session, dated; earlier states stand. Lines, not positions (KsK T1). Each line names what carries it.*

## 2026-11-11 (session 1)

**Elements, on one sheet:** the file of shown terms (`stripped.gz`); the names (`names.gz`); the search box and its advice of six terms
(neighbour 1); the editors who add sequences (not named, not counted); the mathematical objects behind the shown terms (not in this
material); this count (`count1.py`); the grep check.

**Lines that operate:**
- *search box → six terms*: the advice is about a run anywhere; this count is about a beginning. They are two questions. Tonight's
  median, 6, coincides with the advice's number, and the coincidence is not a confirmation (neighbour 1 counts a plurality, not a unique
  hit).
- *shown terms → identity*: for 395,353 sequences the shown terms decide; for 5,861 they do not. 3,394 are twins in 835 groups; the largest
  groups are families added together (growth series of surface groups, reduced words in Coxeter groups), whose shown terms coincide and
  whose definitions differ (names, `explore1.json`). Whether they differ further on is **not in this material** — belief only.
- *the sorted file → a tree*: the count sorts every sequence by its terms; each sequence is a path, parting where its terms part. The
  arborescent structure is the material's own (an encyclopedia looked up by beginnings), not the practice's. Line of flight to test in
  session 2: what the search box actually does — a run anywhere, not a beginning.

**Dead ends, entered as dead ends:** P9 assumed the counting numbers are the most shared beginning; the six ones and the six zeros
are (`session1.json`). P10 assumed newer sequences need more terms; the median is 6 in both groups.

**Decision this map changed:** session 2's question moves from beginnings to runs anywhere (the search box's own rule), because the line
*search box → six terms* shows that session 1 measured a question the encyclopedia's readers do not ask.

## 2026-11-13 (session 2)

**Elements added:** the hints page's rule (a run, consecutive, in order, anywhere; signs "possibly" ignored); tonight's file (one day
newer, 401,318 sequences); this count (`count2.py`) and its check by `grep -F`.

**Lines that operate:**
- *search box → a run anywhere*: measured. Typed from the beginning, the box needs more terms than session 1's count for 32 % of the
  sequences, and the median stays at six. The run that names a sequence alone is shorter than its beginning for 95.8 %, and stands at
  the beginning for 4.2 %: **a sequence is named further in** (conjecture, not measured: by its larger numbers) — 173,951 by a single number.
- *the canon → nowhere alone*: the line session 1 could not see. Fibonacci, primes, counting numbers, squares, factorials, ones and zeros
  can never be the box's only answer: each stands whole inside another entry that adds a term in front, shifts the index or prepends a
  remark (`explore2.json`, checked by `grep`). The more a sequence is used, the more other entries carry it whole. *Conjecture*, not
  measured: the relation runs through the editors' habit of entering variants; the material shows the containment, not the habit.
- *A-number → findability*: a step at A200000 (3.2-3.6 % never found alone below, 0.8-0.9 % above; `explore2b.json`). Unexplained here.
- *the advice of six → a fifth failed*: 84,847 sequences give fifty-one or more hits for their first six terms.

**Dead ends, entered as dead ends:** P4 believed a name needs three to five numbers; one or two do for two in three sequences. P8 believed
signs barely matter; they decide for 2.8 %.

**Decision this map changed:** session 3's question. Planned (session 1): the shortest names as a gallery. Moved by the line *the canon →
nowhere alone*: session 3 asks of the whole encyclopedia **what holds what** — the graph in which an edge runs from a sequence to every
other that shows its whole run inside its own — and whether the work is that containment drawn: the encyclopedia as the box sees it,
where the most famous entries are the ones it can never return alone.
