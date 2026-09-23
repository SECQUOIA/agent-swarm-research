from fractions import Fraction as Q
from itertools import permutations,combinations
from random import Random

rng=Random(611)
profiles=0; strong_cases=0
for n in range(3,9):
 for trial in range(35):
  A=[[Q(0)]*n]; slopes=[]
  for j in range(12):
   raw=[rng.randrange(5) for _ in range(n)]
   if trial%7==0:
    raw=[0]*n; raw[rng.randrange(n)]=1
   if not sum(raw): raw[0]=1
   a=[Q(x,sum(raw)) for x in raw]
   slopes.append(a);A.append([x+y for x,y in zip(A[-1],a)])
  def phi(i,b):
   for j,a in enumerate(slopes):
    h0=j-A[j][i];h1=j+1-A[j+1][i]
    if h1>b+1:
     assert h1>h0
     return Q(j)+(b+1-h0)/(h1-h0)
   return Q(12)
  def reach(word):
   b=Q(0)
   for i in word:b=phi(i,b)
   return b
  r=Q(n,n-1)
  R=[phi(i,Q(0)) for i in range(n)]
  pairs={(i,j):phi(j,R[i]) for i,j in permutations(range(n),2)}
  M=max(pairs.values())
  assert M>=min(Q(12),n*(r*r-1))
  if n>=4:
   assert max(phi(k,x) for (i,j),x in pairs.items() for k in range(n) if k not in (i,j))>=min(Q(12),n*(r**3-1))
  if n>=5 and M<12:
   P=[max(x for (a,b),x in pairs.items() if i not in (a,b)) for i in range(n)]
   QP={(i,j):max(x for (a,b),x in pairs.items() if not {i,j}&{a,b}) for i,j in combinations(range(n),2)}
   for S in combinations(range(n),3):
    H=sum(P[i]+sum(QP[tuple(sorted((i,j)))] for j in range(n) if i!=j) for i in S)
    for z in range(n):
     assert H>=Q(3*n*n,n-1)+Q(3*n*n,(n-1)**2)*sum(R[i] for i in range(n) if i!=z)
     strong_cases+=1
  if n>=5:
   assert max(reach(w) for w in permutations(range(n),4))>=min(Q(12),n*(r**4-1))
  profiles+=1
print('PASS exact reach checks:',profiles,'rational profiles,',strong_cases,'strong weighted-pair cases')
