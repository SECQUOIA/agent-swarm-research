"""Exact three-mode counterexample to allowing three distinct blocks in the reach conjecture."""
from fractions import Fraction as F
from itertools import permutations
if not __debug__:
    raise RuntimeError("Run without -O: exact checks require assertions")

points=[(F(0),[F(0)]*3),(F(1),[F(49,73),F(24,73),F(0)]),(F(97,73),[F(55,73),F(24,73),F(18,73)]),(F(128,73),[F(55,73),F(39,73),F(34,73)]),(F(204,73),[F(112,73),F(58,73),F(34,73)]),(F(258,73),[F(112,73),F(89,73),F(57,73)]),(F(290,73),[F(120,73),F(89,73),F(81,73)]),(F(971,146),[F(417,146),F(309,146),F(245,146)])]
last=F(57,8);t,a=points[-1];points.append((last,[v+(last-t)/3 for v in a]))
for (s,a),(t,b) in zip(points,points[1:]):
 assert sum(b)==t
 assert all(0<=(v-u)/(t-s)<=F(3,4) for u,v in zip(a,b))
def reach(i,s):
 target=s+1
 for (t,a),(u,b) in zip(points,points[1:]):
  lo,hi=t-a[i],u-b[i]
  if lo<=target<=hi:return t+(target-lo)*(u-t)/(hi-lo)
 return last
R=[reach(i,0) for i in range(3)]
M=[max(reach(k,R[j]) for j,k in permutations([v for v in range(3) if v!=i],2)) for i in range(3)]
assert R == [F(128,73),F(97,73),F(1)]
assert M == [F(204,73),F(258,73),F(290,73)]
for i in range(3):
 for j,k in permutations([v for v in range(3) if v!=i],2):
  assert reach(k,R[j]) == M[i]
print('R',list(map(str,R)),'M',list(map(str,M)))
for order in permutations(range(3)):
 t=F(0)
 for i in order:t=reach(i,t)
 print(order,t)
 assert t==F(971,146)
 assert t<F(57,8)
