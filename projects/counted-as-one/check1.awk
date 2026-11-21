# The 12/24 rule again, written apart from rule.py. Input: "start_h stop_h" lines of one overflow, sorted by start.
# Output: "count hours". Block of time t relative to t0: 0 if t < t0+12, else int((t-t0-12)/24)+1.
function blk(t) { return (t < t0 + 12) ? 0 : int((t - t0 - 12) / 24) + 1 }
BEGIN { open = 0; n = 0; h = 0 }
{
  a = $1 + 0; b = $2 + 0; h += b - a
  if (open) { ka = blk(a); if (ka > last + 1) open = 0 }
  if (!open) { t0 = a; open = 1; last = -1; ka = 0 }
  kb = (b > a) ? blk(b - 1e-9) : ka
  if (kb > last) { n += kb - last; last = kb }
}
END { printf "%d %.4f\n", n, h }
