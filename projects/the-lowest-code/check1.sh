#!/bin/sh
# Project 27 session 1, registered check: twelve bridges drawn with seed 20261125 from those with at least one Poor year,
# plus the bridge with the longest Poor spell, recomputed from the raw files by grep/awk alone (no code shared with count1.py).
# Usage: sh check1.sh DIR   (writes check1.json beside this script)
D=$1
H=$(dirname "$0")
python3 -c "
import gzip,json,random
per=json.load(gzip.open('$H/session1-per.json.gz'))
r=json.load(open('$H/session1.json'))
pool=sorted(b for b,v in per.items() if v['poor_open_years']>0 or v['spells'])
ids=random.Random(20261125).sample(pool,12)+[r['P6_longest_spell_bridge']]
print('\n'.join(ids))" > "$H/.check_ids"
# 1. per bridge-year: year, id, L, item41, item90, item27, item106, ADT  (record type 1 only)
for y in $(seq 1992 2025); do
  yy=$(printf %02d $((y % 100)))
  awk -v Y=$y 'NR==FNR{want[$1]=1;next}
    substr($0,19,1)=="1" { id=substr($0,4,15); gsub(/ /,"",id); if(!(id in want)) next;
      if(seen[id]++) next;
      L=""; bad=0;
      for(i=0;i<5;i++){ if(i==3) continue; c=substr($0,259+i,1); if(c ~ /^[0-9]$/){ if(L=="" || c+0<L+0) L=c } else if(c!="N") bad=1 }
      if(bad) next; if(L=="") L="N";
      print id, Y, L, substr($0,199,1), substr($0,287,4), substr($0,157,4), substr($0,362,4), substr($0,165,6)+0 }' \
    "$H/.check_ids" "$D/AL$yy.txt"
done | sort -k1,1 -k2,2n > "$H/.check_rows"
# 2. per bridge: poor open years, ADT-years, rises (with/without reconstruction), falls, spells
awk '
function flush(){ if(id=="") return; if(inspell){ sp=sp (sp==""?"":";") s0 "-" prevpoor ":" (prevy==2025?"censored":"left") }
  printf "%s %d %d %d %d %s\n", id, poor, rises, norec, falls, (sp==""?"none":sp) }
$1!=id { flush(); id=$1; poor=0; rises=0; norec=0; falls=0; sp=""; inspell=0; lastinsp=""; lastL=""; prevy=0 }
{ y=$2; L=$3;
  # spells over consecutive file years
  isp=(L!="N" && L+0<=4);
  if(inspell && (y!=prevy+1)) { sp=sp (sp==""?"":";") s0 "-" prevpoor ":left"; inspell=0 }
  if(isp){ if(!inspell){ inspell=1; s0=y; b0=$6; r0=$7 } prevpoor=y }
  else if(inspell){ out=(L=="N")?"unrated":"rose"; if(out=="rose") out=out ((($6!=b0)||($7!=r0))?"+recon":"+norecon"); sp=sp (sp==""?"":";") s0 "-" prevpoor ":" out; inspell=0 }
  if(isp && $4!="K") poor++;
  # transitions between distinct consecutive inspections
  if($5!=lastinsp){ if(lastL!="" && lastL!="N" && L!="N"){ if(L+0>lastL+0){ rises++; if($6==lb && $7==lr) norec++ } else if(L+0<lastL+0) falls++ }
    lastinsp=$5; lastL=L; lb=$6; lr=$7 }
  prevy=y }
END{ flush() }' "$H/.check_rows" > "$H/.check_out"
# 3. compare with the count
python3 -c "
import gzip,json
per=json.load(gzip.open('$H/session1-per.json.gz'))
res=[]
for line in open('$H/.check_out'):
    i,poor,ri,nr,fa,sp=line.split()
    v=per[i]
    mine=[]
    for s in v['spells']:
        o=s[2]
        if o=='rose': o+='+recon' if s[3] else '+norecon'
        mine.append(f'{s[0]}-{s[1]}:{o}')
    ok=(int(poor)==v['poor_open_years'] and int(ri)==v['rises'] and int(nr)==v['rises_norecon'] and int(fa)==v['falls'] and (';'.join(mine) or 'none')==sp)
    res.append({'bridge':i,'awk':[int(poor),int(ri),int(nr),int(fa),sp],'count':[v['poor_open_years'],v['rises'],v['rises_norecon'],v['falls'],';'.join(mine) or 'none'],'holds':ok})
json.dump({'checked':len(res),'held':sum(r['holds'] for r in res),'bridges':res},open('$H/check1.json','w'),indent=1)
print(sum(r['holds'] for r in res),'of',len(res))
for r in res:
    if not r['holds']: print(r)
"
rm -f "$H/.check_ids" "$H/.check_rows" "$H/.check_out"
