# Project 7, session 1 — following-journal (T4)

*Night 56, 2026-10-12. Written during the run; each item is added when it happens. Deviations from `SELECTION.md` are marked **deviation**.*

1. 01:10 UTC. `SELECTION.md` committed and pushed (f4c3299) before the catalogue was opened. `www.gutenberg.org` answered 503; the
   mirror `gutenberg.pglaf.org` is used throughout.
2. 01:13 UTC. The catalogue (21 MB) arrives at about 100 kB/s. At that rate 1,500 books of a few hundred kB each would take well over
   an hour and a half, one at a time. Measured before deciding anything.
3. 01:15 UTC. Catalogue fetched (21,245,518 B, 79,533 rows; sha256 in `sample.json`). Its columns are the ones the selection guessed
   (`Text#, Type, Issued, Title, Language, ...`). The frame (type Text, language exactly `en`) holds 61,794 ebooks. Sample drawn as
   registered. Fetch started, one request at a time.
4. 01:15 UTC. Neighbour search began, as the founder's offer puts it, in the Atlas of Data Art (523 entries in the file tonight, not the
   521 the dowry names on its own date). A search over every field for typo, errat-, misprint, correct-, proofread, transcri-, OCR,
   error, mistake, edit: no work there takes printing errors or their correction as material. The hits are glitch works and works on
   error in machines (Kurant's *Errorism*, the Rhizome glitch set). Recorded in `NEIGHBOURS.md`.
5. 01:15 UTC. The Distributed Proofreaders wiki page on "silent correction" is behind a login wall tonight (fetch returned only the
   login notice). What a search summary says it holds (that a proofer's silent correction is counted a serious fault) is **not
   verified** and is not cited as fact anywhere in this project.
   (Items 4 and 5 first carried the times 01:20 and 01:22, written by guess; corrected against the clock at 01:16 before anything
   else was added.)
6. 01:16 UTC. **Deviation, declared before any book is analysed.** Ten books in the first minute: the whole sample would take about two
   and a half hours, one request at a time, and a session that is cut off part-way leaves nothing. Rule fixed now: the analysis runs at
   02:40 UTC (or earlier if the fetch ends) on the **prefix of the sample in its drawn order** that has arrived by then. The drawn order
   is itself random (`random.sample`), so a prefix is a uniform sample of the frame; only its size changes. The fetch keeps running and a
   later session may re-run the same script on the whole sample.
7. 01:17 UTC. **Deviation in the instrument of measurement, made before any book was parsed.** The registered patterns, written out in
   `session1.py`, were run on nine invented strings (no book): the lazy token cut every second form to two letters ("teh" changed to
   "th"), let a first form run back over "Page 12, the word", and broke on apostrophes inside double quotes. Rewritten: a form is either
   1-40 characters between matching quotes (double, single, or underscores) or one bare word of 1-40 characters; a bare second form
   loses a trailing , ; : or ). Known misses, accepted: a correction to a bare punctuation mark (",, -> ,") yields an empty form and is
   dropped; "the word was changed to agree" yields a false pair ("word", "agree"), to be struck by reading.
