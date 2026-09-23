from pathlib import Path
from itertools import combinations
from fractions import Fraction as Q
from collections import Counter
import runpy,json
base=Path(__file__).resolve().parent/'relocated'
code=runpy.run_path(str(base/'reference/general_reach_research.py'))
D=frozenset(range(6));events=[]
for h in (2,3):
 for size in range(6,h,-1):
  events.extend((h,frozenset(U)) for U in combinations(range(6),size))
assert len(events)==64
position={v:j for j,v in enumerate(events)}
def t(v):return 6+7*position[v]
def a(v,i):return t(v)+1+i
def canonical(row,rhs):return tuple(sorted(row.items())),rhs
ours=[];eq=[]
def row(entries,rhs):ours.append(canonical(entries,rhs))
# Generate in equation-family order, independently of reference row order.
for i in range(6):row({i:-1},-1)
for i in range(1,6):row({0:1,i:-1},0)
row({i:-1 for i in range(1,6)},-6)
for v in events:
 eq.append(canonical({t(v):-1,**{a(v,i):1 for i in range(6)}},0))
 h,U=v
 for i in U:row({i:1,a(v,i):-1},1)
for v in events:
 h,U=v
 if h==2:
  for i in U:
   for j in U-{i}:row({j:1,t(v):-1,a(v,i):1},-1)
 else:
  for i in U:row({t((2,U-{i})):1,t(v):-1,a(v,i):1},-1)
for v in events:
 for w in events:
  if v!=w and v[0]<=w[0] and v[1]<=w[1]:
   for i in range(6):row({a(v,i):1,a(w,i):-1},0)
for v in events:
 P=frozenset(range(v[0]))
 if P<=v[1] and v[1]!=D:
  for i in range(6):row({a((v[0],D),i):1,a(v,i):-1},0)
size,reference,refeq,obj=code['weighted_triple_relaxation']()
assert size==454 and len(ours)==3660 and len(eq)==64
assert Counter(ours)==Counter(canonical(r,b) for r,b in reference)
assert Counter(eq)==Counter(canonical(r,b) for r,b in refeq)
indobj=Counter()
for i in range(4):
 indobj[t((3,D-{i}))]+=1
 for j in D-{i}:indobj[t((3,D-{i,j}))]+=1
assert dict(indobj)==obj
witness=[Q(x) for x in json.loads((base/'reference/general_reach_relaxation_witness.json').read_text())['variables']]
assert all(x>=0 for x in witness)
for rr,b in ours:assert sum(co*witness[j] for j,co in rr)<=b
for rr,b in eq:assert sum(co*witness[j] for j,co in rr)==b
assert sum(co*witness[j] for j,co in indobj.items())==Q(40328,387)
U=(2,frozenset([0,2,3]));V=(2,frozenset([2,3,4,5]))
assert witness[t(V)]-witness[t(U)]==Q(184,645)
assert witness[a(U,2)]-witness[a(V,2)]==Q(4,645)
print('PASS independent equation-family matrix reconstruction, all witness rows, objective, and nonphysical decrease')
check=runpy.run_path(str(base/'stage03/check_chronological.py'))
check['check']()
