"""Independent deterministic row builder for the printed six-mode chamber.
No project code is imported. All certificate checks use exact fractions.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
from collections import Counter
import json,hashlib
OUT=Path(__file__).resolve().parent
SNAP=OUT.parents[2]/'process/snapshots/stage03-round01'
REF=SNAP/'verification/reference'
manifest=json.loads((SNAP/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((SNAP/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
origin=json.loads((REF/'origin-manifest.json').read_text())
assert all(hashlib.sha256((REF/p).read_bytes()).hexdigest()==r['sha256'] for p,r in origin.items())
N=6;allmodes=tuple(range(N));S=tuple(range(4))
# Fixed event sequence specified in the manuscript.
events=[(h,U) for h in (2,3) for size in range(6,h,-1) for U in combinations(allmodes,size)]
assert len(events)==64 and sum(h==2 for h,U in events)==42
ids={v:j for j,v in enumerate(events)}
def tid(v):return 6+7*ids[v]
def aid(v,i):return tid(v)+1+i
rows=[];rhs=[];massrows=[]
def add(terms,b):
 r={}
 for v,c in terms:r[v]=r.get(v,0)+c
 rows.append({v:c for v,c in r.items() if c});rhs.append(F(b))
# Row ordering read from the bundled source solely to address saved coordinates;
# all loops use sorted lists/tuples, and equations are reconstructed independently.
for i in range(1,6):add([(0,1),(i,-1)],0)
add([(i,-1) for i in range(1,6)],-6)
for i in allmodes:add([(i,-1)],-1)
for ev in events:
 h,U=ev
 massrows.append({tid(ev):-1,**{aid(ev,i):1 for i in allmodes}})
 for i in U:
  add([(i,1),(aid(ev,i),-1)],1)
  if h==2:
   for j in U:
    if j!=i:add([(j,1),(tid(ev),-1),(aid(ev,i),1)],-1)
  else:
   previous=(2,tuple(j for j in U if j!=i))
   add([(tid(previous),1),(tid(ev),-1),(aid(ev,i),1)],-1)
 for later in events:
  hh,V=later
  if h<=hh and set(U)<=set(V) and ev!=later:
   for i in allmodes:add([(aid(ev,i),1),(aid(later,i),-1)],0)
 P=(0,1) if h==2 else (0,1,2)
 if set(P)<=set(U) and len(U)!=6:
  for i in allmodes:add([(aid((h,allmodes),i),1),(aid(ev,i),-1)],0)
assert len(rows)==3660 and len(massrows)==64
objective=Counter()
for i in S:
 objective[tid((3,tuple(j for j in allmodes if j!=i)))]+=1
 for j in allmodes:
  if j!=i:objective[tid((3,tuple(a for a in allmodes if a not in (i,j))))]+=1
assert sum(objective.values())==24
old=[F(v) for v in json.loads((REF/'general_reach_relaxation_witness.json').read_text())['variables']]
assert len(old)==454 and min(old)>=0
for r,b in zip(rows,rhs):assert sum(c*old[v] for v,c in r.items())<=b
for r in massrows:assert sum(c*old[v] for v,c in r.items())==0
assert sum(c*old[v] for v,c in objective.items())==F(40328,387)<F(13104,125)
u=(2,(0,2,3));v=(2,(2,3,4,5))
assert old[tid(u)]==F(1658,645) and old[tid(v)]==F(614,215)
assert old[aid(u,2)]==F(239,645) and old[aid(v,2)]==F(47,129)
assert old[tid(v)]-old[tid(u)]==F(184,645)
assert old[aid(u,2)]-old[aid(v,2)]==F(4,645)
cert=json.loads((SNAP/'verification/stage03/chronological_chamber_certificate.json').read_text())
order=sorted(range(64),key=lambda j:(old[6+7*j],j))
assert cert['order']==order
assert all(j<42 for j in order[:42]) and all(j>=42 for j in order[42:])
violations=[]
for pos,j in enumerate(order):
 for k in order[pos+1:]:
  for i in allmodes:
   drop=old[7+7*j+i]-old[7+7*k+i]
   if drop>0:violations.append(drop)
assert len(violations)==239 and max(violations)==F(224,645)
for a,b in zip(order,order[1:]):
 for i in allmodes:add([(7+7*a+i,1),(7+7*b+i,-1)],0)
assert len(rows)==4038
Y=[F(v) for v in cert['inequality_dual']];Z=[F(v) for v in cert['equality_dual']]
assert len(Y)==4038 and len(Z)==64 and max(Y)<=0
res=[F(objective.get(i,0)) for i in range(454)]
for r,w in zip(rows,Y):
 for j,c in r.items():res[j]-=w*c
for r,w in zip(massrows,Z):
 for j,c in r.items():res[j]-=w*c
assert min(res)>=0
assert sum(w*b for w,b in zip(Y,rhs))==F(13104,125)
assert sum(bool(v) for v in Y+Z)==254
# Construct uniform primal independently; then compare the supplied primal.
uniform=[F(6,5)]*6
for h,U in events:
 t=F(66,25) if h==2 else F(546,125)
 uniform.extend([t]+[t/6]*6)
assert uniform==[F(v) for v in cert['primal']]
for r,b in zip(rows,rhs):assert sum(c*uniform[v] for v,c in r.items())<=b
for r in massrows:assert sum(c*uniform[v] for v,c in r.items())==0
assert sum(c*uniform[v] for v,c in objective.items())==F(13104,125)
result={'snapshot_hashes':len(manifest),'origin_hashes':len(origin),'variables':454,'old_inequalities':3660,'equalities':64,'new_inequalities':4038,'old_witness_objective':str(F(40328,387)),'chronology_violations':len(violations),'max_chronology_drop':str(max(violations)),'exact_chamber_minimum':str(F(13104,125)),'nonzero_dual_rows':sum(bool(v) for v in Y+Z),'positive_dual_residuals':sum(v>0 for v in res)}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
