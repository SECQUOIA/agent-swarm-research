"""Enumerate realizable strict histories using complete-word bitsets.
Does not use the manuscript transition graph or its minimum-switch DP.
"""
from itertools import product,permutations
from collections import Counter
from fractions import Fraction as F
N=7;words=list(product(range(3),repeat=N));prefix=[];cost=[]
exact={};budget={}
for h,w in enumerate(words):
 C=[0,0,0];path=[]
 for j,p in enumerate(w,1):
  C[p]+=1;path.append(tuple(C))
  for i,v in enumerate(C):exact[j,i,v]=exact.get((j,i,v),0)|(1<<h)
 prefix.append(tuple(path));cost.append(sum(a!=b for a,b in zip(w,w[1:])))
for s in range(N):budget[s]=sum(1<<h for h,c in enumerate(cost) if c<=s)
def bit(j,i,v):return exact.get((j,i,v),0)
def boxes(j):
 for f in product(range(j+1),repeat=3):
  if sum(f) not in (j-1,j-2):continue
  mask=(1<<len(words))-1
  for i,v in enumerate(f):mask&=bit(j,i,v)|bit(j,i,v+1)
  yield f,mask
states={(): (1<<len(words))-1}
for j in range(1,N+1):
 nxt={};opts=list(boxes(j))
 for hist,mask in states.items():
  for f,allowed in opts:
   m=mask&allowed
   if not m:continue
   hh=hist+(f,)
   # Exact convex-average realization: every floor and ceiling is reached
   # by at least one complete word remaining in this box intersection.
   if all(m&bit(t,i,v) and m&bit(t,i,v+1) for t,g in enumerate(hh,1) for i,v in enumerate(g)):
    nxt[hh]=m
 states=nxt
 dist=Counter(next(s for s in range(N) if m&budget[s]) for m in states.values())
 print('N=',j,'histories=',len(states),'minimum-switch distribution=',dict(sorted(dist.items())))
 expected={5:{0:3,1:138,2:255},6:{0:3,1:255,2:1377,3:237},7:{0:3,1:414,2:4542,3:3891,4:6}}
 if j in expected:assert dist==expected[j]
bad={h for h,m in states.items() if not(m&budget[3])}
canon=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
orbit={tuple(tuple(g[p[i]] for i in range(3)) for g in canon) for p in permutations(range(3))}
assert bad==orbit and len(bad)==6
for i,w in enumerate(((1,2,0,0,0,2,2),(0,0,2,1,1,2,2),(0,0,1,1,2,2,0))):
 h=words.index(w);assert cost[h]<=3
 violations=[(j,q,p[q]) for j,(f,p) in enumerate(zip(canon,prefix[h]),1) for q in range(3) if not(f[q]<=p[q]<=f[q]+1)]
 assert violations==[(i+2,i,0)]
raw=((1,1,1),(4,1,1),(4,4,1),(4,4,4),(7,4,4),(8,5,5),(8,5,8))
A=[[F(v,3) for v in row] for row in raw]
errors=[max(abs(a-v) for aa,pp in zip(A,p) for a,v in zip(aa,pp)) for p in prefix]
assert min(e for e,c in zip(errors,cost) if c<=3)==F(4,3)
assert states[canon].bit_count()==104
print('Six exceptional histories equal the exact permutation orbit; all repairs pass.')
print('All 2187 words directly checked: seven-cell optimum 4/3; 104 chamber words.')
