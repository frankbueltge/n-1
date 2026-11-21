"""The 12/24 spill-counting rule, as fixed in SELECTION.md (project 26).

Times are floats in hours. Activations are (start, stop) pairs, stop >= start.
count_spills returns one dict per counted spill: block start/end, hours of
discharge inside the block, activations overlapping it, and the sequence index.
Stdlib only.
"""


def overlaps(a, b, lo, hi):
    # activation [a, b] overlaps block [lo, hi); a zero-length activation at a counts if lo <= a < hi
    if a == b:
        return lo <= a < hi
    return a < hi and b > lo


def count_spills(acts):
    acts = sorted(acts)
    spills = []
    i = 0
    n = len(acts)
    seq = 0
    while i < n:
        t0 = acts[i][0]
        k = 0
        j = i  # first activation not yet wholly before the current block
        last_end = None
        while True:
            lo = t0 if k == 0 else t0 + 12 + 24 * (k - 1)
            hi = t0 + 12 if k == 0 else t0 + 12 + 24 * k
            hit = []
            m = j
            while m < n and acts[m][0] < hi:
                a, b = acts[m]
                if overlaps(a, b, lo, hi):
                    hit.append(m)
                m += 1
            if not hit and k >= 1:
                break
            hours = 0.0
            for h in hit:
                a, b = acts[h]
                hours += max(0.0, min(b, hi) - max(a, lo))
            spills.append({"seq": seq, "lo": lo, "hi": hi, "hours": hours, "acts": len(hit)})
            last_end = hi
            # advance j past activations that end before the next block
            while j < n and acts[j][1] < hi and acts[j][0] < hi:
                j += 1
            k += 1
        # next sequence: first activation starting at or after the empty block's end
        empty_end = last_end + 24
        while i < n and acts[i][0] < empty_end:
            i += 1
        seq += 1
    return spills


if __name__ == "__main__":
    # synthetic cases, expected counts worked by hand (see JOURNAL.md)
    cases = [
        ([(0, 1)], 1),                      # one short spill
        ([(0, 1), (5, 6), (11, 11.5)], 1),  # three inside the first 12 h
        ([(0, 1), (13, 14)], 2),            # second inside block 1 [12,36)
        ([(0, 100)], 5),                    # 0-12,12-36,36-60,60-84,84-108
        ([(0, 1), (40, 41)], 2),            # block1 [12,36) empty -> closes; new seq at 40
        ([(0, 1), (35.9, 36.5)], 3),        # touches block1 and block2 [36,60)
        ([(0, 12)], 1),                     # ends exactly at block1 start: no overlap
        ([(0, 0), (0, 0)], 1),              # zero-length
        ([], 0),
    ]
    ok = 0
    for acts, want in cases:
        got = len(count_spills(acts))
        print(acts, want, got, "ok" if got == want else "FAIL")
        ok += got == want
    hrs = [round(s["hours"], 3) for s in count_spills([(0, 100)])]
    print("hours of (0,100):", hrs, "ok" if hrs == [12, 24, 24, 24, 16] else "FAIL")
    print(ok, "of", len(cases))
