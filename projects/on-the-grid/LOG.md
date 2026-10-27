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
