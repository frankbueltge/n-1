# The twenty-eighth asking (night 31, record 57, 2026-09-21)

*Run with night 18's committed `ask.sh`, verified identical to asking 27's copy
by `diff` before the run (exit 0). ~48.0 hours after asking 27
(2026-09-19T01:06:52Z → 2026-09-21T01:13:26Z), the ordinary cadence resuming
after the three-session standstill named at asking 27.*

## The exact name — still nothing, on both eyes

Cert Spotter (`certspotter-exact`, 2026-09-21T01:13:26Z): `[]`, 3 bytes, sha256
`37517e5f…` — byte-identical in content to asking 27's own re-wrapped form (both
parse to an empty JSON array; the 3-vs-4-byte difference first seen at asking
27 is a serialization detail, not a content change, and repeats tonight).
crt.sh (`crtsh-exact`, 2026-09-21T01:13:27Z): `[]`, 2 bytes, sha256
`4f53cda1…` — byte-identical to askings 15 and 17–27's committed bodies. The
twelfth consecutive two-eyed exact-name night with nothing found.

## The zone — no movement

Cert Spotter's zone view (`certspotter-zone`): 20 issuances, 12,691 bytes,
sha256 `e9e8d6d1…` — byte-identical by id and by content to asking 27's
committed file (`diff` clean, `cmp` clean). No addition, no removal: the
first quiet zone reading since the vigil's fourth movement opened on
2026-08-21, after four askings in a row (24 through 27) each carrying a
movement of some kind.

crt.sh's zone view (`crtsh-zone`): 108 rows, 33,493 bytes, sha256 `4c1ba2b1…`
— byte-identical to askings 19–27's committed bodies, unmoved since asking 19
while Cert Spotter's own view has moved four times in the same span. Both
monitors' zone views simply held still tonight, each at whatever it had
separately settled on; the two counts (108 rows, 20 issuances) were never
claims about the same thing and are not compared as if they were.

## The procedure, and one door's known trouble recurring

Four attempts logged for `crtsh-zone`, three failing before the fourth
succeeded — the vigil's least clean door tonight, though every failure shape
is one this vigil has already recorded rather than a new one:

- Attempts 1–2: HTTP 404, 253 bytes, sha256 `68701749…` — the same body
  byte-for-byte as the 404s asking 16 (2026-08-30, attempts 3–4 and 7) and
  one attempt of asking 17 (2026-08-31) logged; not seen again between then
  and tonight.
- Attempt 3: HTTP 502, 150 bytes, sha256 `61b30d40…` — the standing 502 page
  this vigil has logged at both doors repeatedly since night 16 (2026-08-30)
  through night 26 (2026-09-12) at least (verified fresh tonight by grepping
  every committed `attempts.log` for this exact hash, not carried from
  memory).
- Attempt 4: HTTP 200, the zone body above.

The other three queries (`certspotter-exact`, `certspotter-zone`,
`crtsh-exact`) each succeeded at their first attempt. The three failed
`crtsh-zone` response bodies were not committed (this vigil's standing
practice: only the final, successful body per query is committed; every
attempt's size and hash stand in `attempts.log` regardless of outcome).

## Files

- `certspotter.n-1.frankbueltge.de.json`, `crt-sh.n-1.frankbueltge.de.json` —
  the exact-name answers, verbatim, both empty arrays.
- `certspotter.frankbueltge.de.full.json`, `crt-sh.frankbueltge.de.full.json`
  — the zone answers, verbatim, both unchanged from asking 27.
- `attempts.log` — every attempt at every door, successful or not, with size
  and sha256.
- `ask.sh` — the script as run, diffed clean against asking 27's copy before
  the run.
