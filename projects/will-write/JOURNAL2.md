# Project 8, session 2 — following-journal (T4)

*Night 60, 2026-10-14. Written during the run; each item is added when it happens. Deviations from `SESSION2.md` are marked
**deviation**. Times are read from the clock (`date -u`) before each item is written.*

1. 20:05 UTC. `SESSION2.md` committed and pushed (18d5079) before any letter was read or any new promise fetched.
2. 20:06 UTC. **Deviation, arithmetic:** `SESSION2.md` says "19 years"; its own definition (every year 2001-2024 not sampled in
   session 1) gives 20 (2001-2004, 2006-2009, 2011-2014, 2016-2019, 2021-2024). The definition governs; 20 years are fetched.
   `fetch2.py` started in the background, Commons only, one request at a time, texts to scratch.
3. 20:07 UTC. Probing the shape of a bill's publication list (to write the script), the Academies Act 2010's list was read: 43
   publications, none of type 44. One bill's outcome seen before the run; it is in the frame only if a 2010 promise names it.
4. 20:08 UTC. **Deviation in the match rule, before any bill was searched:** frame titles carry curly apostrophes ("Renters’
   Rights Bill"); the registered comparison would fail on a straight one. Both sides now read ’ as '. No other change. Known
   limit, accepted: a title such as "Bill of Rights" yields "Bill" and will not match.
   (Items 3 and 4 first carried 20:08 and 20:10, written by guess against this journal's own rule; corrected against the clock,
   which read 20:08:37 after item 4 was written.)
5. 20:09 UTC. **Found while looking for a neighbour, before any outcome:** the register's own page
   (`https://api.parliament.uk/bill-papers/publication-types/44`, fetched with curl and read in scratch) says: "Such “will write”
   replies are not published in Hansard but are placed in the Library of the House concerned and published on the Parliamentary
   website." It lists 1,451 papers in all. So for bill debates, the Library copy session 1 counted as *said* is, by Parliament's
   own account, routine: a minister need not say it for it to happen. This changes what session 1's Commons series can mean (the
   saying may have stopped because the depositing became automatic; conjecture) and it is carried to `AUDIT.md` part D. It does
   not change Q1's rule, which was fixed before.
6. 20:09 UTC. The register's CSV (`https://api.parliament.uk/bill-papers/publication-types/44.csv`, 1,451 rows, scratch only; its
   titles name members) dated by year: 2014 30, 2015 34, 2016 190, 2017 119, 2018 107, 2019 56, 2020 188, 2021 185, 2022 153, 2023
   99, 2024 87, 2025 184, 2026 19. **The register begins in 2014.** P9 (2010: fewer than a fifth have a letter back) will hold by
   the register's coverage, not by anything ministers did; it is reported as registered with that said beside it, and counts for
   nothing about practice. 2015 is thin (34 letters in the year). Q1 runs on as registered, against the Bills API itself, not this
   CSV; the CSV is used only to say when the register starts.
   (Item 6 first carried 20:10, by guess; corrected against the clock, 20:09:48.)
7. 20:21 UTC. The Hansard fetch died on 2004 after eight failed tries at one page (HTTP 500 each time); 2001-2003 are cached.
   Restarted from the cache; nothing repeated, nothing changed. The bill matching runs slower than planned (about one bill a
   minute: the Bills API pages each bill's stages); the 23:30 cut-off stands.
8. 20:32 UTC. It died again at the same 2004 page (the API answered "An error has occurred." eight times; by hand, the same
   URL then answered 200 twice). Now restarted inside a loop of up to ten restarts, from the cache. Retrieval unchanged.
9. 20:37 UTC. Q1 ran (`q1.py` -> `q1_rows.json`; `q1_test.py` -> `q1.json`). Frame 368; **326 matched** to a bill; 26 found no
   bill by search (Education and Adoption Bill 7, Bus Services (No. 2) Bill 5, and others), 16 found a bill whose recorded
   sittings do not include the promise date (Pension Schemes Bill 11: several bills share the name). Unmatched are left out, as
   registered. **P7 held** (Lords 2015-2025: 130 of 177 matched promises, 73 %, have a letter on that bill within 60 days).
   **P8 failed** (Commons 2015-2025: 49 of 93, 53 %; registered "fewer than a quarter"). **P9 held, and means nothing about
   practice** (2010: 0 of 56; the register begins in 2014, item 6).
   Read after the run: 15 random matched promises (seed 20261014) against the bill's short title: all 15 the right bill. The API
   marks the letters' House "Unassigned", so a Commons promise could be meeting a Lords letter. Exploratory, by a title rule
   (a letter is Lords-side if its title names Lord, Baroness, Earl, Viscount, Countess, Duke, Marquess or Peers; titles read in
   scratch, not committed): of the 49 Commons promises with a letter back, 47 have a Commons-side letter in the window; of the 130
   Lords ones, 126 have a Lords-side letter. The house confusion does not carry the result.
10. 20:37 UTC. What this does to session 1. Session 1's page says "the copy for the Library did not follow". That sentence measured the
   saying. For bill debates the register now shows the other half: since 2014 the letters come back in public by Parliament's own
   route, unsaid (item 5), for half the Commons promises and three quarters of the Lords ones within sixty days (upper bounds:
   a letter on the same bill is not shown to be the letter promised). The finding moves from "the way back went silent" to **"the
   way back stopped being spoken because it became a filing"** — for the 16-32 % of promises made on bills. For the rest
   (questions, general debates) there is no register, and the measured silence stands. The page must say this.
   (Item 9 first carried 20:39, by guess; corrected against the clock, 20:37:45.)
