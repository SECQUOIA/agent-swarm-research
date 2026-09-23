from itertools import product,permutations
from collections import Counter,defaultdict
from fractions import Fraction as Q

def counts(word):
 c=[0]*3;out=[]
 for i in word:c[i]+=1;out.append(tuple(c))
 return tuple(out)
def histories(N):
 current=[((0,0,0),)]
 for j in range(2,N+1):
  candidates=[f for f in product(range(j),repeat=3) if sum(f) in (j-1,j-2)]
  current=[h+(f,) for h in current for f in candidates if all(f[i]-h[-1][i] in (0,1) for i in range(3))]
 return current
for N in (5,6,7):
 words=list(product(range(3),repeat=N));cc=[counts(w) for w in words]
 byfloor=defaultdict(int);bypoint=defaultdict(int);byswitch=defaultdict(int)
 for bit,(w,c) in enumerate(zip(words,cc)):
  mark=1<<bit;s=sum(a!=b for a,b in zip(w,w[1:]));byswitch[s]|=mark
  for j,cj in enumerate(c,1):
   for i in range(3):bypoint[(j,i,cj[i])]|=mark
   for mask in product((0,1),repeat=3):
    f=tuple(cj[i]-mask[i] for i in range(3))
    if min(f)>=0 and sum(f) in (j-1,j-2):byfloor[(j,f)]|=mark
 dist=Counter();bad=[]
 for h in histories(N):
  feasible=(1<<len(words))-1
  for j,f in enumerate(h,1):feasible&=byfloor[j,f]
  assert feasible
  # Independent integral-word realization check: both extreme prefix counts
  # must occur in the set of complete compatible words.
  for j,f in enumerate(h,1):
   for i in range(3):
    assert feasible&bypoint[j,i,f[i]]
    assert feasible&bypoint[j,i,f[i]+1]
  cost=min(s for s,mask in byswitch.items() if mask&feasible)
  dist[cost]+=1
  if cost==4:bad.append(h)
 if N==5:assert dist=={0:3,1:138,2:255}
 if N==6:assert dist=={0:3,1:255,2:1377,3:237}
 if N==7:
  assert dist=={0:3,1:414,2:4542,3:3891,4:6}
  canonical=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
  orbit={tuple(tuple(f[i] for i in p) for f in canonical) for p in permutations(range(3))}
  assert set(bad)==orbit
  repairs=((1,2,0,0,0,2,2),(0,0,2,1,1,2,2),(0,0,1,1,2,2,0))
  for i,w in enumerate(repairs):
   violations=[(j,a) for j,(f,c) in enumerate(zip(canonical,counts(w)),1) for a in range(3) if not f[a]<=c[a]<=f[a]+1]
   assert violations==[(i+2,i)]
  A=[tuple(Q(x,3) for x in f) for f in ((1,1,1),(4,1,1),(4,4,1),(4,4,4),(7,4,4),(8,5,5),(8,5,8))]
  def err(c):return max(abs(a-b) for aa,bb in zip(A,c) for a,b in zip(aa,bb))
  assert min(err(c) for w,c in zip(words,cc) if sum(a!=b for a,b in zip(w,w[1:]))<=3)==Q(4,3)
 print('PASS independent word-bitset chamber audit',N,dict(sorted(dist.items())))
