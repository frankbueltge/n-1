# Project 26 session 2, check part 3: rule variant V2 (sequence closes after 24 h with no discharge, measured from the latest stop),
# a separate implementation in awk sharing no code with count2.py. Input: lines "start_epoch stop_epoch", sorted. Prints the count.
function kk(t) { return (t < t0 + 43200) ? 0 : 1 + int((t - t0 - 43200) / 86400) }
function edge(t,  x) { if (t == t0 + 43200) return 1; x = (t - t0 - 43200) / 86400; return (t > t0 + 43200 && x == int(x)) }
function flush(  k) { for (k in seen) n++; split("", seen) }
NR == 1 || $1 - mx >= 86400 { if (NR > 1) flush(); t0 = $1; mx = $2 }
{ if ($2 > mx) mx = $2
  if ($2 == $1) { seen[kk($1)] = 1 } else { hi = kk($2); if (edge($2)) hi--; if (hi < kk($1)) hi = kk($1); for (k = kk($1); k <= hi; k++) seen[k] = 1 } }
END { flush(); print n + 0 }
