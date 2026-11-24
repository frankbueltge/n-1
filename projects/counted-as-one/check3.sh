#!/bin/sh
# Project 26 session 3 check (SESSION3.md): daily hours on drawn days, recomputed by awk from the raw start/stop rows.
# Usage: sh check3.sh <start-stop dir> <tsv of WXW00799 rows written by count1.read_startstop> ; prints id day hours
# CSV times are ISO GMT (converted with GNU date); XLSX times are Excel serial days (45658 = 2025-01-01).
SS="$1"; WX="$2"
E0=$(date -u -d 2025-01-01T00:00:00Z +%s)
day_hours() { # stdin: lines "start_h stop_h"; $1 id; $2.. days
  id=$1; shift
  sort -n | awk -v id="$id" -v days="$*" '
    { a=$1; b=$2; if (b<a) next; if (a<0) a=0; if (b>8760) b=8760;
      if (n>0 && a<=B[n]) { if (b>B[n]) B[n]=b } else { n++; A[n]=a; B[n]=b } }
    END { k=split(days, D, " ");
      for (i=1;i<=k;i++) { d=D[i]; lo=d*24; hi=lo+24; h=0;
        for (j=1;j<=n;j++) { x=(A[j]>lo?A[j]:lo); y=(B[j]<hi?B[j]:hi); if (y>x) h+=y-x }
        printf "%s %d %.4f\n", id, d, h } }'
}
iso() { grep "^$1," "$SS"/*"$2"*.csv | while IFS=, read -r u s a b; do
  echo "$(( $(date -u -d "$a" +%s) - E0 )) $(( $(date -u -d "$b" +%s) - E0 ))"; done | awk '{print $1/3600, $2/3600}'; }
iso SBB00547 "South West" | day_hours SBB00547 22 70 344 354
iso AWS00016 "Anglian" | day_hours AWS00016 126 217 224 291
awk -F'\t' '{print ($3-45658)*24, ($4-45658)*24}' "$WX" | day_hours WXW00799 83 238 250 310
