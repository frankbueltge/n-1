"""Project 26 session 2: print the whole vocabulary of the annual return columns 12 (shellfish) and 13 (bathing). Usage: python3 -I vocab2.py SCRATCH"""
import sys,glob,collections
sys.path.insert(0,'.')
import xlsx
S=sys.argv[1]
f=glob.glob(S+'/dl/ar/*/*all water*.xlsx')[0]
hdr=None; rows=[]
for sh,r in xlsx.rows(f,"All WaSC"):
    if hdr is None:
        if r and r[0]=="Unique ID": hdr=r
        continue
    if r and r[0]: rows.append(r+[None]*40)
for i in (12,13):
    for v,c in sorted(collections.Counter(repr(r[i]) for r in rows).items(), key=lambda x:-x[1]):
        print(i,c,v,sep='\t')
