"""Direct rational controls -> printed event relaxation, including flat H segments."""
from fractions import Fraction as F
from itertools import combinations,permutations
from pathlib import Path
import json,random
rng=random.Random(8302)
counts={'inputs':0,'strong_weighted_inequalities':0,'pair_constraints':0,'flat_H_cells':0}
for n in range(5,11):
 for sample in range(8):
  L=20;cols=[]
  for j in range(L):
   if sample%2==0:
    q=rng.randrange(n);col=[F(i==q) for i in range(n)];counts['flat_H_cells']+=1
   else:
    nums=[rng.randint(0,10) for i in range(n)];tot=sum(nums)
    col=[F(v,tot) for v in nums]
   cols.append(col)
  cumulative=[[F(0)]*n]
  for col in cols:cumulative.append([a+b for a,b in zip(cumulative[-1],col)])
  def A(i,t):
   j=min(int(t),L-1)
   return cumulative[j][i]+(t-j)*cols[j][i]
  def phi(i,b):
   level=b+1
   for j in range(L):
    hlo=F(j)-cumulative[j][i];hhi=F(j+1)-cumulative[j+1][i]
    if hhi>level:return F(j)+(level-hlo)/(1-cols[j][i])
   return F(L)
  R=[phi(i,F(0)) for i in range(n)]
  pair={(i,j):phi(j,R[i]) for i,j in permutations(range(n),2)}
  M=max(pair.values())
  if M==L:continue
  P=[max(v for (a,b),v in pair.items() if i not in (a,b)) for i in range(n)]
  Q={frozenset((i,j)):max(v for (a,b),v in pair.items() if not set((a,b))&set((i,j))) for i,j in combinations(range(n),2)}
  winning=next(k for k,v in pair.items() if v==M)
  for S in combinations(range(n),3):
   events=[(frozenset(),M)]+[(frozenset([i]),P[i]) for i in S]+[(ij,v) for ij,v in Q.items() if ij&set(S)]
   for excluded,t in events:
    assert sum(A(i,t) for i in range(n))==t
    for j,k in permutations(set(range(n))-excluded,2):
     assert R[j]-t+A(k,t)<=-1
     counts['pair_constraints']+=1
    for k in range(n):assert A(k,t)<=A(k,M)
    if not excluded&set(winning):assert t==M
   for i in S:
    for j in range(n):
     if i==j:continue
     for k in range(n):assert A(k,Q[frozenset((i,j))])<=A(k,P[i])
   H=sum(P[i]+sum(Q[frozenset((i,j))] for j in range(n) if j!=i) for i in S)
   for z in range(n):
    assert H>=F(3*n*n,n-1)+F(3*n*n,(n-1)**2)*sum(R[i] for i in range(n) if i!=z)
    counts['strong_weighted_inequalities']+=1
  counts['inputs']+=1
out=Path(__file__).with_name('control-embedding-results.json')
out.write_text(json.dumps(counts,indent=2)+'\n');print(json.dumps(counts,indent=2))
