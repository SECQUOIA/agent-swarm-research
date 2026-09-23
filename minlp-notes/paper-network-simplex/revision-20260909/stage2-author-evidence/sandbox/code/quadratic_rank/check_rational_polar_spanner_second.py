"""Independent exact checks for the rational polar-spanner oracle.

The generic checks use a synthetic weak optimizer on rational boxes and
verify exact repair, fixed denominator, exchange growth, and the complete
image-vertex coefficient bound. They do not implement the GLS oracle.
The polar checks use asymmetric rational boxes with explicit support values.
Run from the repository with Python and SymPy installed.
"""

from fractions import Fraction as F
from itertools import product, combinations
from math import factorial,lcm
import random
import sympy as s
rng=random.Random(155890)
exchanges=calls=systems=vertices_checked=0
for n in range(1,5):
 for trial in range(4):
  r=min(n,3); sigma=F(rng.randrange(1,7),9)
  c=[F(rng.randrange(-9,10),11) for _ in range(n)];R0=n*sigma
  verts=[[ci+sg*sigma for ci,sg in zip(c,sign)] for sign in product((-1,1),repeat=n)]
  while True:
   V=s.Matrix([[s.Rational(rng.randrange(-7,8),2**rng.randrange(0,7)) for j in range(r)] for i in range(n)])
   if V.rank()==r:break
  imgs=[s.Matrix([v])*V for v in verts]
  inds=next(I for I in combinations(range(len(verts)),r) if s.Matrix.vstack(*(imgs[j] for j in I)).det()!=0)
  basis=[verts[j] for j in inds]
  B=s.Matrix.vstack(*(s.Matrix([v])*V for v in basis));D0=abs(F(B.det()))
  Z=1+sum(map(abs,c))+R0;M=1+sum(abs(F(v)) for v in V);W=1+n*M*Z
  U=1+F(factorial(r))*W**(r-1)/D0;L=1+n*M*U
  delta=F(1)
  while 2*n*delta>1 or n*delta*(1+L+2*L*(R0+1)/sigma)>F(1,4):delta/=2
  eta=n*delta;ep=2*n*delta
  qa=sigma*delta/(sigma+ep);qb=[ep*ci/(sigma+ep) for ci in c]
  common=lcm(qa.denominator,*(x.denominator for x in qb),*(x.denominator for row in basis for x in row))
  def oracle(d):
   global calls
   calls+=1
   v=[ci+(sigma if di>=0 else -sigma) for ci,di in zip(c,d)]
   z=v[:]
   # A rational approximately feasible point with no objective loss.
   z[0]+=eta/2*(1 if d[0]>=0 else -1)
   q=[F((zi/delta).__floor__())*delta for zi in z]
   lam=[(sigma*qi+ep*ci)/(sigma+ep) for qi,ci in zip(q,c)]
   assert all(ci-sigma<=li<=ci+sigma for li,ci in zip(lam,c))
   assert all((li*common).denominator==1 for li in lam)
   opt=sum(di*vi for di,vi in zip(d,v));val=sum(di*li for di,li in zip(d,lam))
   assert 0<=opt-val<=F(1,4)
   return lam
  while True:
   B=s.Matrix.vstack(*(s.Matrix([v])*V for v in basis));inv=B.inv();old=abs(F(B.det()))
   assert old>=D0 and all(abs(F(v))<=U for v in inv)
   changed=False
   for i in range(r):
    d=[F(x) for x in V*inv[:,i]]
    assert sum(map(abs,d))<=L
    for sign in (1,-1):
     lam=oracle([sign*x for x in d]);coef=sum(li*di for li,di in zip(lam,d))
     if abs(coef)>2:
      basis[i]=lam
      B2=s.Matrix.vstack(*(s.Matrix([v])*V for v in basis))
      assert abs(F(B2.det()))>2*old
      exchanges+=1;changed=True;break
    if changed:break
   if not changed:break
  for img in imgs:
   assert all(abs(F(x))<=F(9,4) for x in img*inv)
   vertices_checked+=1
  systems+=1
print('generic systems',systems,'exact repaired optimizer calls',calls,'exchanges',exchanges,'full-image vertex checks',vertices_checked)
polar=0
for m in range(1,7):
 for trial in range(12):
  lower=[F(rng.randrange(1,9),5) for _ in range(m)]
  upper=[F(rng.randrange(1,9),5) for _ in range(m)]
  rho=min(lower+upper);R=sum(max(l,u) for l,u in zip(lower,upper))
  a=F(1)
  while a>min(F(1),1/(8*R*m)):a/=2
  assert 2*a*R<=1
  eta=F(1,17);tau=eta/(2*(1+F(m)/rho))
  for height in (F(1,5),F(9,10),F(1),1+tau/4,F(2)):
   lam=[height/(m*u) for u in upper]
   if any(li>1/rho for li in lam):continue
   # Exact feasible approximate support optimizer in the original asymmetric box.
   factor=1-min(F(1,2),tau/(2*height))
   x=[factor*u for u in upper];dot=sum(li*xi for li,xi in zip(lam,x))
   assert 0<=height-dot<=tau
   if dot>1:
    assert all(xi/ui<=1 for xi,ui in zip(x,upper))
   else:
    nearby=[li/(1+tau) for li in lam]
    assert sum(li*u for li,u in zip(nearby,upper))<=1
    assert sum(abs(li-ni) for li,ni in zip(lam,nearby))<=eta/2
   polar+=1
print('positive-polar membership/separation cases',polar)
