"""Rebuild event constraints directly, with row sets independent of source order.
The supplied dual's row identifiers are translated through the reference rows;
then the dual identity is checked using independently generated row vectors.
"""
import sys,importlib.util,json
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[3]/'process/snapshots/stage03-round01'
# Prevent import cache mutation of immutable snapshot.
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reference',ROOT/'verification/reference/general_reach_research.py')
ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
size,refrows,refeq,refobj=ref.weighted_triple_relaxation()
U=frozenset(range(6));S=frozenset(range(4))
events=[(h,frozenset(v)) for h in (2,3) for d in range(6,h,-1) for v in combinations(range(6),d)]
assert len(events)==64
index={event:j for j,event in enumerate(events)}
def t(event):return 6+7*index[event]
def a(event,i):return t(event)+1+i
def key(row,rhs):return (tuple(sorted((i,c) for i,c in row.items() if c)),rhs)
rows=[];eq=[]
def add(row,rhs):rows.append(key(row,rhs))
for i in U:add({i:-1},-1)
for i in U-{0}:add({0:1,i:-1},0)
add({i:-1 for i in U-{0}},-6)
for v in events:
 h,V=v
 eq.append(key({t(v):-1,**{a(v,i):1 for i in U}},0))
 for i in V:
  add({i:1,a(v,i):-1},1)
 if h==2:
  for i,j in combinations(sorted(V),2):
   add({j:1,t(v):-1,a(v,i):1},-1)
   add({i:1,t(v):-1,a(v,j):1},-1)
 else:
  for i in V:add({t((2,V-{i})):1,t(v):-1,a(v,i):1},-1)
for v in events:
 for w in events:
  if v!=w and v[0]<=w[0] and v[1]<=w[1]:
   for i in U:add({a(v,i):1,a(w,i):-1},0)
for v in events:
 P=frozenset(range(v[0]))
 if P<=v[1] and v[1]!=U:
  for i in U:add({a((v[0],U),i):1,a(v,i):-1},0)
assert Counter(rows)==Counter(key(*r) for r in refrows)
assert Counter(eq)==Counter(key(*r) for r in refeq)
obj=Counter()
for i in S:
 obj[t((3,U-{i}))]+=1
 for j in U-{i}:obj[t((3,U-{i,j}))]+=1
assert dict(obj)==refobj
old=list(map(F,json.loads((ROOT/'verification/reference/general_reach_relaxation_witness.json').read_text())['variables']))
cert=json.loads((ROOT/'verification/stage03/chronological_chamber_certificate.json').read_text())
order=sorted(events,key=lambda v:(old[t(v)],index[v]))
assert [index[v] for v in order]==cert['order']
for v,w in zip(order,order[1:]):
 for i in U:
  row={a(v,i):1,a(w,i):-1};add(row,0);refrows.append((row,0))
assert len(rows)==4038
# Transfer dual row numbers to semantic sparse coefficient rows.
y=defaultdict(F);z=defaultdict(F)
for val,row in zip(cert['inequality_dual'],refrows):y[key(*row)]+=F(val)
for val,row in zip(cert['equality_dual'],refeq):z[key(*row)]+=F(val)
assert set(y)<=set(rows) and set(z)<=set(eq)
res=[F(obj.get(i,0)) for i in range(size)];bound=F(0)
for table,coeffs in ((set(rows),y),(set(eq),z)):
 for row in table:
  mult=coeffs[row];items,rhs=row
  if table==set(rows):assert mult<=0
  bound+=mult*rhs
  for i,c in items:res[i]-=mult*c
assert min(res)>=0 and bound==F(13104,125)
primal=list(map(F,cert['primal']))
assert min(primal)>=0
for entries,rhs in set(rows):assert sum(c*primal[i] for i,c in entries)<=rhs
for entries,rhs in set(eq):assert sum(c*primal[i] for i,c in entries)==rhs
assert sum(c*primal[i] for i,c in obj.items())==bound
print('Independent event-row reconstruction matches all 3660 original inequalities and 64 equalities.')
print('All 4038 chamber rows, rational dual residual, bound, and primal checked using independent rows.')
print('Exact chamber optimum:',bound)
