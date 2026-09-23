from fractions import Fraction as F
from itertools import permutations,combinations
from random import Random
rng=Random(628271)
count=0
for n in (5,6,10,30):
 for sample in range(15):
  rows=[]
  for j in range(8):
   a=[rng.randrange(7) for _ in range(n)]
   if not sum(a):a[0]=1
   rows.append([F(x,sum(a)) for x in a])
  C=[[F(0)]*n]
  for row in rows:C.append([a+b for a,b in zip(C[-1],row)])
  def reach(i,b,E):
   # Locate last feasible knot; then solve within its next affine interval.
   good=[j for j in range(9) if j-C[j][i]<=b+E]
   j=max(good)
   if j==8:return F(8)
   return F(j)+(b+E-(j-C[j][i]))/(1-rows[j][i])
  for E in (F(1,2),F(1),F(2)):
   R=[reach(i,F(0),E) for i in range(n)]
   pairs={(p,q):reach(q,R[p],E) for p,q in permutations(range(n),2)}
   M=max(pairs.values())
   if M==8:continue
   P=[max(v for (a,b),v in pairs.items() if i not in (a,b)) for i in range(n)]
   Q={(i,j):max(v for (a,b),v in pairs.items() if i not in (a,b) and j not in (a,b)) for i,j in combinations(range(n),2)}
   choices=list(combinations(range(n),3)) if n<=6 else [tuple(sorted(rng.sample(range(n),3))) for _ in range(5)]
   for S in choices:
    H=sum(P[i]+sum(Q[tuple(sorted((i,j)))] for j in range(n) if j!=i) for i in S)
    for z in range(n):
     bound=F(3*n*n,n-1)*E+F(3*n*n,(n-1)**2)*sum(R[i] for i in range(n) if i!=z)
     assert H>=bound,(n,sample,E,S,z,H,bound)
     count+=1
   # Observe actual 3/4-block reach, including no-repeat constraint.
   for k in (3,4):
    B=n*E*(F(n,n-1)**k-1)
    # Dynamic recursion over mode subsets for n<=10; n30 only the weighted check.
    if n>10:continue
    states={frozenset([i]):R[i] for i in range(n)}
    for level in range(2,k+1):
     nxt={}
     for used,b in states.items():
      for i in range(n):
       if i in used:continue
       key=used|{i};value=reach(i,b,E)
       nxt[key]=max(nxt.get(key,F(0)),value)
     states=nxt
    assert max(states.values())>=min(F(8),B)
print('Strong weighted-pair inequalities independently evaluated on controls:',count)
print('Actual distinct 3/4-block reaches passed on n=5,6,10 rational profiles.')
