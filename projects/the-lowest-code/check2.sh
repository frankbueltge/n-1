#!/bin/sh
# Project 27 session 2 check (SESSION2.md): twelve silent rises drawn with seed 20261126, redone by awk from the raw lines.
# Usage: sh check2.sh DIR   (DIR holds AL93.txt .. AL25.txt). The draw reads session2-rises.json.gz; nothing else from count2.py.
D=$1
python3 -c "
import gzip,json,random
r=json.load(gzip.open('session2-rises.json.gz','rt'))
for i in sorted(random.Random(20261126).sample(range(len(r)),12)):
    s=r[i]; print(s['b'],s['y0'],s['y1'],s['L0'],s['L1'],s['open0'],s['open1'],s['w75'].replace(' ','_'),'NA' if s['next_L'] is None else s['next_L'])
" | while read b y0 y1 L0 L1 o0 o1 w nx; do
  files=""; for y in $(seq 1993 2025); do files="$files $D/AL$(printf %02d $((y%100))).txt"; done
  awk -v B="$b" -v Y0="$y0" -v Y1="$y1" -v EXP="$L0 $L1 $o0 $o1 $w $nx" '
    FNR==1 { f=FILENAME; sub(/.*AL/,"",f); sub(/\.txt/,"",f); yr=(f+0>=50)?1900+f:2000+f }
    { id=substr($0,4,15); gsub(/ /,"",id) }
    id==B && substr($0,19,1)=="1" && !(yr in seen) {
      seen[yr]=1; m=10
      for (k=0;k<4;k++){ c=substr($0,(k<3?259+k:263),1); if (c ~ /[0-9]/ && c+0<m) m=c+0 }
      L[yr]=m; I[yr]=substr($0,287,4); O[yr]=substr($0,199,1); W[yr]=substr($0,278,2); BU[yr]=substr($0,157,4); RE[yr]=substr($0,362,4)
    }
    END {
      w=W[Y0]; gsub(/ /,"_",w)
      nx="NA"; last=I[Y1]
      for (y=Y1+1;y<=2025;y++) if (y in L && I[y]!=last) { nx=(L[y]==10?"NA":L[y]); break }
      same=(BU[Y0]==BU[Y1] && RE[Y0]==RE[Y1])
      got=L[Y0] " " L[Y1] " " O[Y0] " " O[Y1] " " w " " nx
      ok=(got==EXP && same)
      print B, Y0, Y1, "awk:", got, "recon_unchanged=" same, "count2:", EXP, (ok?"PASS":"FAIL")
    }' $files
done
