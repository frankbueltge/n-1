#!/bin/sh
# Project 27 session 3 check (SESSION3.md): twelve strokes of the work drawn with seed 20261127; each bridge's whole line 1993-2025
# and the stroke's two codes redone by awk from the raw lines. Usage: sh check3.sh DIR   (DIR holds AL93.txt .. AL25.txt).
# The draw reads ../../works/set-aside/data.json; nothing else of the project's Python is used.
D=$1
files=""; for y in $(seq 1993 2025); do files="$files $D/AL$(printf %02d $((y%100))).txt"; done
python3 -c "
import json,random
d=json.load(open('../../works/set-aside/data.json'))
s=d['strokes']
for i in sorted(random.Random(20261127).sample(range(len(s)),12)):
    b,y0,y1,L0,L1,o=s[i]; print(d['bridges'][b],y0,y1,L0,L1,d['lines'][b])
" | while read b y0 y1 L0 L1 line; do
  awk -v B="$b" -v Y0="$y0" -v Y1="$y1" -v L0="$L0" -v L1="$L1" -v EXP="$line" '
    FNR==1 { f=FILENAME; sub(/.*AL/,"",f); sub(/\.txt/,"",f); yr=(f+0>=50)?1900+f:2000+f }
    length($0)>=365 && substr($0,19,1)=="1" {
      id=substr($0,4,15); gsub(/ /,"",id)
      if (id!=B || (yr in C)) next
      bad=0; m=10; n=0
      for (k=0;k<4;k++){ c=substr($0,(k<3?259+k:263),1); if (c ~ /^[0-9]$/) { if (c+0<m) m=c+0 } else if (c=="N") n++; else bad=1 }
      if (bad) next
      C[yr]=(m==10?"N":m)
    }
    END {
      got=""; for (y=1993;y<=2025;y++) got=got ((y in C)?C[y]:"-")
      ok=(got==EXP && C[Y0]==L0 "" && C[Y1]==L1 "")
      print B, Y0 "->" Y1, L0 "->" L1, "awk:", got, "work:", EXP, (ok?"PASS":"FAIL")
    }' $files
done
