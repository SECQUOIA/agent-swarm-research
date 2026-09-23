from fractions import Fraction as Q
from itertools import combinations, product
from random import Random
import json
import sympy as sp
import mpmath as mp
from pathlib import Path
rng=Random(4021)
def fl(x): return x.numerator//x.denominator
def ce(x): return -fl(-x)
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[1],x[1]-y[0])
def mul(x,y):
 a=[u*v for u in x for v in y]; return min(a),max(a)
def sq(x): return (0 if x[0]<=0<=x[1] else min(t*t for t in x),max(t*t for t in x))
def enc(x,g): return fl(g*x),ce(g*x)
def rat(): return Q(rng.randint(-20,20),rng.randint(1,13))
interval_cases=0; indefinite_clamps=0
for _ in range(1200):
 p=rng.randint(1,4); h=rng.randint(0,3); G=rng.randint(2,15); GF=rng.randint(1,11); GS=rng.randint(1,17)
 f=[[rat() for i in range(p)] for j in range(h+1)]; b=[rat() for j in range(h)]
 H=[[rat() for j in range(p)] for i in range(p)]
 for i in range(p):
  for j in range(i): H[i][j]=H[j][i]
 u=[f[0][i]-sum(b[j]*f[j+1][i] for j in range(h)) for i in range(p)]
 ui=[]
 for i in range(p):
  z=mul(enc(f[0][i],GF),(G,G))
  for j in range(h): z=sub(z,mul(enc(b[j],G),enc(f[j+1][i],GF)))
  assert z[0]<=u[i]*G*GF<=z[1]; ui.append(z)
 numerator=sum(u[i]*H[i][j]*u[j] for i in range(p) for j in range(p))
 qu=(0,0)
 for i in range(p):
  qu=add(qu,mul(enc(H[i][i],G),sq(ui[i])))
  for j in range(i+1,p): qu=add(qu,mul((2,2),mul(enc(H[i][j],G),mul(ui[i],ui[j]))))
 assert qu[0]<=numerator*G**3*GF**2<=qu[1]
 d=Q(rng.randint(20,100),rng.randint(1,15)); dl=fl(G*d)
 if dl<=0: continue
 score=numerator/d; upper=Q(max(0,qu[1]),G**2*GF**2*dl); integer=ce(GS*upper)
 assert score<=upper<=Q(integer,GS)
 if qu[1]<0: indefinite_clamps+=1
 interval_cases+=1
# Log intervals: exact endpoints constructed from rational series; high precision is
# an independent numerical diagnostic of signs/implementation, not a log theorem proof.
def log_bounds(x,m=60):
 h=0; y=x
 while y>=2: h+=1;y/=2
 while y<1: h-=1;y*=2
 def base(u):
  s=sum((2*u**(2*j+1)/Q(2*j+1) for j in range(m)),Q(0))
  return s,s+2*u**(2*m+1)/(Q(2*m+1)*(1-u*u))
 yl,yu=base((y-1)/(y+1)); l2,u2=base(Q(1,3))
 return (yl+h*l2,yu+h*u2) if h>=0 else (yl+h*u2,yu+h*l2)
mp.mp.dps=100
for x in [Q(1),Q(1,2),Q(1,8),Q(7,1000000),Q(2),Q(9999),Q(2)**300,Q(2)**-300,Q(499,251)]:
 lo,hi=log_bounds(x)
 val=mp.log(mp.mpf(x.numerator)/x.denominator)
 assert mp.mpf(lo.numerator)/lo.denominator <= val+mp.mpf('1e-95')
 assert val <= mp.mpf(hi.numerator)/hi.denominator+mp.mpf('1e-95')
# Independently form local innovations and compare an explicit calendar DP with
# exhaustive complete schedules under gap, mandatory and forbidden constraints.
n=6;p=2;rho=sp.Rational(1,4); R=sp.Matrix(n,n,lambda i,j:rho**abs(i-j)+(1 if i==j else 0))
F=sp.Matrix([[1,sp.Rational((-1)**i*(i+1),5)] for i in range(n)])
J0=sp.Matrix([[2,sp.Rational(1,3)],[sp.Rational(1,3),1]])
N=sp.Matrix([[3,sp.Rational(-1,4)],[sp.Rational(-1,4),2]])
W=N.inv(); delta=sp.Rational(1,2); L=1; cache={}
def arc(t,hist):
 key=(t,tuple(hist))
 if key not in cache:
  if hist:
   b=R.extract([t],hist)*R.extract(hist,hist).inv()
   v=F[t,:]-b*F.extract(hist,list(range(p))); d=R[t,t]-(b*R.extract(hist,[t]))[0]
  else: v=F[t,:];d=R[t,t]
  cache[key]=v.T*v/d
 return cache[key]
def exactJ(S): return J0+F.extract(S,[0,1]).T*R.extract(S,S).inv()*F.extract(S,[0,1]) if S else J0
cases=0; certificate_cases=0;ceil_cases=0
allsets=[list(c) for k in range(n+1) for c in combinations(range(n),k)]
for S in allsets:
 I=sp.zeros(p)
 for t in S: I+=arc(t,[s for s in S if t-L<=s<t])
 M=J0+I/(1-delta)-exactJ(S)
 assert M[0,0]>=0 and M[1,1]>=0 and M.det()>=0
 certificate_cases+=1
for gap in [1,2,4,9]:
 for k in range(n+1):
  for mandatory,forbidden in [(set(),set()),({0},set()),({2},{2}),({1},{4})]:
   feasible=[S for S in allsets if len(S)==k and mandatory<=set(S) and not forbidden.intersection(S) and all(b-a>=gap for a,b in zip(S,S[1:]))]
   def score(S,grid=None):
    vals=[sp.trace(W*arc(t,[s for s in S if t-L<=s<t]))/(1-delta) for t in S]
    return sum(sp.ceiling(v*grid) if grid else v for v in vals)
   for grid in [None,7]:
    states={(0,0,0):sp.Rational(0)} # count, one-bit history, cooldown
    for t in range(n):
     nxt={}
     for (count,mask,cool),val in states.items():
      for take in [0,1]:
       if (take and (cool or t in forbidden or count==k)) or (not take and t in mandatory): continue
       hist=[t-1] if mask else []
       v=sp.trace(W*arc(t,hist))/(1-delta) if take else 0
       if grid:v=sp.ceiling(grid*v)
       key=(count+take,take,max(0,gap-1) if take else max(0,cool-1))
       if key not in nxt or nxt[key]<val+v:nxt[key]=val+v
     states=nxt
    found=[v for key,v in states.items() if key[0]==k]
    assert bool(found)==bool(feasible)
    if feasible: assert max(found)==max(score(S,grid) for S in feasible)
    if grid and feasible:
     assert max(found)/grid <= max(score(S) for S in feasible)+sp.Rational(k,grid)
     ceil_cases+=1
   cases+=1
result={'signed_interval_cases':interval_cases,'negative_upper_numerator_clamps':indefinite_clamps,'log_sign_diagnostics':9,'exact_matrix_certificate_checks':certificate_cases,'calendar_family_checks':cases,'ceiling_loss_checks':ceil_cases,'status':'PASS'}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
