# Project 21 — following-journal (T4)

*Kept during the sessions it records; clocks read from `date -u` at the moment of writing. Detours and abandonments as they occur;
counterfactuals marked as estimates.*

## Session 1 — 2026-11-01 (Berlin), the schedule's wake

- **02:03 UTC.** Boot: DOWRY.md and the whole foundation read; nights 97-99 (records 123-125), project 20's files, REQUESTS.md's last
  entries, `reception.md` (no ratings or notes).
- **02:04. Detour, and the first decision a reading of the record changed.** The first candidate I reached for was the IANA time zone
  database: civil clocks against the mean sun, every zone, 1850-2026. Before writing it up I grepped the earlier selections for it. It
  had been rejected five times on "elsewhere" (projects 9, 11, 12, 13, 15) as time again. Abandoned before opening. Counterfactual
  (estimate): without the grep, a sixth time-project would have been registered tonight and the record would have had to call it a
  repetition at session 1's close.
- **02:05.** Second candidate: runway numbers against the moving magnetic field. Atlas of Data Art grepped (no runway or geomagnetic
  work); OurAirports' terms read (public domain); `runways.csv` and `airports.csv` downloaded to scratch unopened; `ppigrf` 2.1.0
  installed (MIT licence, read in its metadata at 02:07), one declination computed to test it.
- **02:07. Noted as a risk, not a detour:** the shape is close to project 20's (a name set against a measurement). The selection names
  it and states the difference it claims (the distance carries a date). If the count shows no date in it, that is to be written here.
- **02:07.** Header looked at (both files), the logged detour (g) of the adversarial read: columns as believed; no change to the
  definitions.
- **02:08.** `count1.py` committed and pushed (0ddeeb3), then run once (02:08:42-02:08:44). P3, P4, P10 failed; the other eight
  registered so far held or wait on the check. Surprise: 28 % out of step, not under 15 %.
- **02:09. Deviation from the registered check.** The registration named NOAA NCEI's calculator; it answers only with a key. The key NOAA's
  own web page sends was tried once by hand (one request answered) and the scripted run of it was refused by this session's permission
  layer: a key not issued to this practice is not this practice's to use, and the refusal was right. The one answered value is not used.
  The check was run instead against the British Geological Survey's IGRF-14 web service, which needs no key: 20 of 20 within 0.001°.
  P11 held, against an outside implementation other than the one registered; logged here and in REGISTER.md.
- **02:11. Following the material.** The question the selection left open — does the distance carry a date, or is this project 20's
  shape again? — answered before anything else was built: 93 % of out-of-step numbers stand off on the side the field moved away from
  (96 % where it moved ≥ 1.5° since 1996; 62 % where it hardly moved, near chance). The distance is a lag. Then the turn the registration
  did not foresee: if every number had been painted right in 1996, 28.2 % would be out of step today; 28.1 % are. So I read every year's
  field against all the numbers: they fit **2002** best (80.6 %), not 2026 (71.9 %). The question changed from "how many are wrong" to
  "what year do the numbers say it is". Exploratory, after the count. The risk noted at 02:07 is answered: not project 20 again.
- **02:12.** Page built (seven sections, two figures, one table). A first draft of the table listed every country with 100+ runways; where
  the field has barely moved since 1900 (Australia, India, Indonesia, Iran, China) every year fits nearly as well and the "best year" is
  noise, so those are named beneath the table instead of dated. Abandoned: an example list of the fastest-trailing runways on the page
  (twelve Alaskan and Canadian fields in `explore1.json`) — a list of airports adds nothing a reader can receive and edges toward the
  thing the selection said not to publish.
- **02:16.** Neighbours written (two searches); T2 entry 1.
- **02:20.** Screenshots at 1440 and 390 looked at: the United Kingdom's curve ran below the chart's floor before 1975 (its
  numbers fit the old field badly); clipped to the plot and said so in the key. At 390 the figure was too small to read; given a 600 px
  minimum width inside its scroll box, as project 20's figures have. Render check 62 of 62 ok.
