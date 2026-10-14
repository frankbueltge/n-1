# Project 8, session 1 — following-journal (T4)

*Night 59, 2026-10-14. Written during the run; each item is added when it happens. Deviations from `SELECTION.md` are marked
**deviation**.*

1. 18:14 UTC. `SELECTION.md` committed and pushed (63e2c30) before any promise was read in bulk. The exposure before writing is listed
   at its head.
2. 18:15 UTC. `fetch.py` started: ten years, two Houses, seven phrases, one request at a time with a half-second pause. Texts go to
   scratch only.
3. 18:15 UTC. **Deviation in the instrument, made before any contribution was parsed.** The registered promise pattern was run on eight
   invented strings (no Hansard text): it missed "I’ll write to her", because the pattern required a space between "I" and "'ll".
   Rewritten so the contracted forms attach directly. No other change. Known limits, accepted: "I will write to the Secretary of State"
   counts as a promise but not as a promise to a member (the addressee rule is there for that); the search phrases include no
   contracted form, so "I'll write" is only seen where another phrase brings the contribution in.
   (Item 3 first carried 18:19, written by guess; corrected against the clock at 18:15 before anything else was added. Items 1-2 were
   checked against the push output and the clock and stand.)
4. 18:16 UTC. The API is slow: one test request of 100 results took 28 s, and the fetch has met two HTTP 500s (retried). At that pace
   the registered retrieval (ten years, two Houses, a count plus seven phrases each, paged) takes well over an hour. No cutoff is
   declared yet: the years are fetched in date order, so a prefix would be a biased sample (early years only), not a smaller uniform
   one as in project 7. Decision deferred until the first year's time is known; the rule will be written here before any count is read.
5. 18:18 UTC. The first run died on a body without results: the API answered "An error has occurred." (HTTP 500 after about
   30 s) for a count query, and once more inside a page. Not a property of the query (the same page answered 200 when asked again).
   `fetch.py` now retries up to eight times, accepts only bodies that carry results, and caches good answers in scratch so a restart
   repeats nothing. Restarted. Still one request at a time.
