# Project 19 — working log (T4, following-journal)

*Written as it happens; each entry's clock is `date -u` read at the moment.*

- **01:04 UTC** first clock read. Boot: DOWRY.md and the whole foundation (bibliography not re-read), the atlas schema, nights 88-92,
  project 18's selection and project file, the carry, the protocol's material front, REQUESTS.md's and reception.md's last entries (no
  ratings or notes). Older layers and nights not re-read.
- **01:04** candidate addresses probed for status and size. The record shows time zones rejected four times as "time again"; not
  re-proposed. FoodData Central's pages read for terms and file names; its FAQ page came back as an application shell with styles, its
  text not reached; the licence found in the API guide instead.
- **01:06** 21 CFR 101.9 fetched from the eCFR; the first request was refused for want of compression (171 B error), the second taken
  compressed. The rounding rules read.
- **01:06** Atlas of Data Art fetched (sha256 `4765ce73…`, unchanged); three searches.
- **01:07** the branded-foods JSON archive downloaded to scratch (204,270,542 B); not opened.
- **01:08** `SELECTION.md` written; `NEIGHBOURS.md`; T3 entry 1 before the count (`AUDIT.md`).
- **01:10** structure looked at before writing the count: one food per line; the first record's keys and its `labelNutrients` key names (12 nutrients, each `{value}`), no values printed. Archive sha256 `57b0f122…` (no published checksum seen); one JSON file, 3,315,545,449 B. `count1.py`, `check1.py` pushed. `count1.py` run once.
- **01:11** count done (35 s): 455,457 foods; P1, P2, P6, P7 held, P3, P4, P5 failed. Looked at the commonest off-grid values (not registered): 80.1, 89.9, 99.9 kcal; 8.99, 8.01 g fat; 1.01 g fiber. Near misses, not other steps. Detour: the registered question assumed the record holds the printed numbers; it looks as if it holds numbers that went to per-100 g and back. `explore1.py` written to test that, exploration only.
- **01:15** fault: the count left one line unparsed, the last food, whose line also closes the array. First correction stripped a trailing `]}` and broke every line (each food ends in one); caught on its output (1 food), not kept. Second correction: `count1b.py`, `raw_decode` per line. Registered and corrected outcomes both kept.
- **01:19** `explore1.py` (exploratory): of 128,204 off-grid calorie values, 83,948 are a grid number sent to per-100 g (stored as a whole number) and multiplied back; 14,023 match the round trip with no grid point behind it; 28,725 do not match it (the commonest: 149, 101, 139, whole numbers one off the step). Fat and sodium alike. `check1.py`: 10 of 20 answered (ten refused, 429, the shared DEMO_KEY's rate), 7 agree, 3 disagree, each a dump value off the grid (8.01, 8.03, 8.99 g) where the live service gives the grid value (8.0, 8.0, 9.0). P8 failed as registered.
- **01:20** the ten refused re-asked once by hand at 8 s spacing (`recheck1.py`): all ten refused again (429); the demo key is spent. Not counted. Caution: the three disagreeing live values equal the dump's values rounded to one decimal (8.01→8.0, 8.03→8.0, 8.99→9.0; 90.2 unchanged), so the service may round its output rather than hold the grid number. Not decidable from three foods; conjecture either way.
- **01:26** page built; render check 54 ok. Two screenshots looked at: the bar figure at 390 px is cut by its own scroll box (as on earlier pages, kept); in the tenths figure the near-misses vanish above 100 kcal. Detour: the stored values look rounded to three significant digits (80.1, 8.99, 0.999, 149), which would turn 150 sent to 100 g and back into 149, the commonest value my round-trip test could not explain. `explore1c.py` written to test it, exploration only.
- **01:30** `explore1c.py`: of 128,204 off-grid calorie values, 103,607 are a grid number sent to 100 g and back with three significant digits kept; 20,822 fit the round trip with no grid number behind them; 2,267 fit neither. Fat and sodium alike. The page's worked example (150 kcal on 70 g) was wrong by its own arithmetic (it returns 150, not 149); replaced by 145 g before commit. Page rebuilt on the three-digit test; render check ok at both widths.
- **01:32** T3 entry 1 continued; PROJECT.md; margin, noscript, window 4.57.0; atlas layer; register; night record. Validators ok. Session ends here.
