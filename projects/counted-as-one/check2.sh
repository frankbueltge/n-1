#!/bin/sh
# Project 26 session 2, check part 1: receiving / shellfish / bathing values for drawn overflows, read from the sheet's XML with
# unzip, sed, grep and awk only (not xlsx.py). Usage: sh check2.sh <annual return xlsx> <uid> [<uid> ...]
F="$1"; shift
T=$(mktemp -d)
unzip -p "$F" xl/sharedStrings.xml | awk 'BEGIN{RS="<si>"} NR>1{gsub(/\n/," "); gsub(/<[^>]*>/,""); gsub(/&amp;/,"\\&"); print}' > "$T/ss"   # line n = index n-1
unzip -p "$F" xl/worksheets/sheet1.xml | sed 's/<row /\n<row /g' | grep '^<row ' > "$T/rows"
for U in "$@"; do
  I=$(grep -n -x -F "$U" "$T/ss" | head -1 | cut -d: -f1); I=$((I - 1))
  ROW=$(grep -E "<c r=\"A[0-9]+\"[^>]*t=\"s\"[^>]*><v>$I</v>" "$T/rows" | head -1)
  for C in L M N; do
    CELL=$(printf '%s' "$ROW" | grep -o -E "<c r=\"$C[0-9]+\"[^>]*(/>|>.*?</c>)" | sed 's#</c>.*#</c>#' | head -1)
    V=$(printf '%s' "$CELL" | sed -n 's/.*<v>\([^<]*\)<\/v>.*/\1/p')
    case "$CELL" in *'t="s"'*) V=$(sed -n "$((V + 1))p" "$T/ss");; esac
    printf '%s\t%s\t%s\n' "$U" "$C" "$V"
  done
done
