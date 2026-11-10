# Project 23 — nearest neighbours

*Searched before any work (the works condition): the Atlas of Data Art (`https://frankbueltge.de/atlas/werke.json`, 593 entries, sha256
`b6985c2c…`, fetched 2026-11-07) grepped for time zone, timezone, Zeitzone, daylight, Sommerzeit, tz database, clock — no entry; one web
search (standard mode, 2026-11-07). To be searched again before any work is declared.*

1. **`tzdata-meta`**, Tim Parenti (announced on the tz mailing list, 2019-01-12,
   `https://mm.icann.org/pipermail/tz/2019-January/027391.html`; `https://tzdata-meta.timtimeonline.com/`,
   `https://github.com/timparenti/tzdata-meta`). A hand-kept, machine-readable record of when the tz list was first told of each change
   and when it took effect, "backfilled … since 2016-01-01", with no intent to go further back (the message's words). **Nearest in
   question.** Its contents were not read tonight. Daylight, as far as read: it measures announcement → effect by hand for changes
   since 2016; this study measures first release → effect by machine for every change of offset the database records since 1997,
   and separates news from re-timing and from the past rewritten.
2. **Brian Inglis's proposal** (tz mailing list, 2018-12-30, quoted in the message above) of a table of lead times "as a basis for
   stats". A proposal, not a measurement.
3. **IANA's tz page** (`https://www.iana.org/time-zones/tz-link`): states that changes are sometimes made with little notice and points
   to an article on the timing of time-zone changes (seen in a search summary; neither read in full tonight — to be read before session 3).

No data artwork found that draws the database's notice.

*Searched again 2026-11-10 before declaring (`SESSION3.md`): the Atlas of Data Art (685 entries, sha256 `fda32f61…`) grepped for time
zone, timezone, Zeitzone, daylight, Sommerzeit, tz database, clock, Uhrzeit, correction, retroactive, errata — no work on time zones or
time files; two web searches (standard mode).*

4. **A0 TimeZone Migration**, named on IANA's tz page as a tool that "displays changes between recent tzdb versions"
   (`https://www.iana.org/time-zones/tz-link`, read 2026-11-10). Not opened. Daylight: a diff of versions for a developer; it does not
   set every hour lived against the day a release first set it right.
5. **Paul Eggert to the tz list, 2014-06-01** (`https://mm.icann.org/pipermail/tz/2014-June/020956.html`): "Unfortunately a significant
   fraction of the entries in the tz database are incorrect." Not a work; the reason the work's hidden curve ends at zero only by
   construction.
6. **"History of DST Changes"** (`https://michel-leonard.github.io/Daylight-Saving-Time/timezoneDSTHistory.html`, seen in a search
   summary only): a per-zone history of daylight-saving changes. Daylight: one version's history, not the versions' disagreements.

**The work *The Hours Shown Wrong* draws every stretch of hours the then-newest release showed wrong by when it was lived and when a release
first set it right, and counts at any date the hours already lived that the file was wrong about without yet knowing.**
