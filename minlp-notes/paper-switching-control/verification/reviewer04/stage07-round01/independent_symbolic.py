from fractions import Fraction as Q
from itertools import product
import sympy as S
x=S.symbols("x")
for k in range(1,15):
 C=(2-2*(k+1)*x+k*(k+1)*x*x)/(k*(2-(k+1)*x))
 L=x/((1-x)**(-k)-1)
 target=1/S.Integer(k)-S.Rational(k+1,2*k)*x
 assert S.series(C,x,0,3).removeO()==target+S.Rational(k*k-1,4*k)*x*x
 assert S.series(L,x,0,3).removeO()==target+S.Rational(k*k-1,12*k)*x*x
 for ell in range(1,min(k,4)+1):
  d=k-ell
  th=(1-d*x)*(1-(d+1)*x)/(1-x)*(2*((1-(d+1)*x)/(1-d*x))**ell-1)
  U=S.cancel(x*(1+th)/(1-th))
  c=S.Rational(3*k**3-3*k-2*ell**3+2*ell,12*k*k)
  assert S.series(U,x,0,3).removeO()==target+c*x*x
print("PASS independent symbolic coefficient expansions, k=1,...,14 and all applicable seeds")
for n in range(3,45):
 for k in range(1,n):
  C=Q(n*(n-1)+(n-k)*(n-k-1),n*k*(2*n-k-1))
  factor=Q(2*(n-k-1)*(2*n-k*(k+1)),2*n*k*(k+1)*(2*n-k-1))
  assert C-Q(1,k+1)==factor
  d=n-k
  assert (Q(k*(n-k+1),n-k)*Q(1,n)>=1)==(d*d<=k)
print("PASS independent plateau factor and every-input equal-mass reach criterion through n=44")
# A distinct representation of the history optimization: intersect bitsets of
# complete words, instead of a dynamic program on floor-history nodes.
from collections import defaultdict,Counter
N=7
allwords=list(product(range(3),repeat=N))
index=[defaultdict(int) for _ in range(N)]
costmasks=[0]*N
for widx,w in enumerate(allwords):
 counts=[0,0,0]
 for j,p in enumerate(w):
  counts[p]+=1;index[j][tuple(counts)]|=1<<widx
 costmasks[sum(a!=b for a,b in zip(w,w[1:]))]|=1<<widx
histories=[((0,0,0),)]
for j in range(2,N+1):
 histories=[h+(tuple(a+b for a,b in zip(h[-1],inc)),) for h in histories
            for inc in product((0,1),repeat=3)
            if j-sum(h[-1])-sum(inc) in (1,2)]
dist=Counter()
for h in histories:
 mask=(1<<len(allwords))-1
 for j,f in enumerate(h):
  allowed=0
  for inc in product((0,1),repeat=3):
   c=tuple(a+b for a,b in zip(f,inc))
   if sum(c)==j+1:allowed|=index[j].get(c,0)
  mask &= allowed
 assert mask
 dist[next(s for s,m in enumerate(costmasks) if mask&m)]+=1
assert dict(dist)=={0:3,1:414,2:4542,3:3891,4:6}
print("PASS independent 2187-complete-word bitset intersection for all 8856 seven-cell histories",dict(sorted(dist.items())))
