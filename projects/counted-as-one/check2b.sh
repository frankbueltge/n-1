#!/bin/sh
# Project 26 session 2, check part 2: bathing-season hours of one overflow from its raw CSV rows, by grep, cut, GNU date and awk
# (not count1.py's reader). Usage: sh check2b.sh <uid> <csv> ...   prints: uid season_hours all_hours
U="$1"; shift
T=$(mktemp -d)
grep -h -F "$U," "$@" > "$T/r"
cut -d, -f3 "$T/r" | date -u -f - +%s > "$T/a"
cut -d, -f4 "$T/r" | date -u -f - +%s > "$T/b"
LO=$(date -u -d 2025-05-15T00:00:00Z +%s); HI=$(date -u -d 2025-10-01T00:00:00Z +%s)
paste "$T/a" "$T/b" | awk -v lo="$LO" -v hi="$HI" -v u="$U" '{a=$1;b=$2;t+=b-a; if(a<lo)a=lo; if(b>hi)b=hi; if(b>a)s+=b-a} END{printf "%s %.4f %.4f\n", u, s/3600, t/3600}'
