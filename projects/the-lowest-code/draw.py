"""Project 27: the blind draw of one state, registered before any NBI record is downloaded.

Input: the per-state counts of highway bridges on FHWA's 2025 download page
(https://www.fhwa.dot.gov/bridge/nbi/ascii2025.cfm, fetched 2026-11-25, sha256 16d8bbec...),
transcribed below. Rule: states, DC and Puerto Rico with 5,000 to 20,000 highway bridges
in 2025, sorted by postal code, one drawn with random.Random(20261125).choice.
"""
import random

COUNTS_2025 = {
    "AL": 16181, "AK": 1660, "AZ": 8587, "AR": 12978, "CA": 25975, "CO": 8990, "CT": 4363,
    "DE": 874, "DC": 261, "FL": 13070, "GA": 15090, "HI": 1180, "ID": 4646, "IL": 26927,
    "IN": 19542, "IA": 23716, "KS": 24891, "KY": 14590, "LA": 12684, "ME": 2542, "MD": 5500,
    "MA": 5311, "MI": 11397, "MN": 13551, "MS": 16711, "MO": 24647, "MT": 5235, "NE": 15412,
    "NV": 2123, "NH": 2549, "NJ": 6825, "NM": 4033, "NY": 17666, "NC": 19343, "ND": 4250,
    "OH": 26713, "OK": 22926, "OR": 8329, "PA": 23314, "RI": 787, "SC": 9504, "SD": 5883,
    "TN": 20374, "TX": 56951, "UT": 3144, "VT": 2866, "VA": 14143, "WA": 8520, "WV": 7345,
    "WI": 14498, "WY": 3138, "PR": 2434,
}

if __name__ == "__main__":
    pool = sorted(k for k, n in COUNTS_2025.items() if 5000 <= n <= 20000)
    print(len(pool), pool)
    print(random.Random(20261125).choice(pool))
