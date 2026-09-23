"""Bounded independent checks; no manuscript verification code is imported."""
from fractions import Fraction as F
from itertools import product
from random import Random
import json
import numpy as np
from scipy.optimize import linprog
rng=Random(9173)
results={}
# Independent subset definition of the box rank versus a direct LP in arc flows.
max_error=0
for trial in range(24):
    n=6
    edges=[(i,(i+1)%n) if rng.randrange(2) else ((i+1)%n,i) for i in range(n)]
    lo=[F(rng.randrange(-6,3),3) for _ in edges]
    hi=[v+F(rng.randrange(1,7),3) for v in lo]
    w0=[(l+u)/2 for l,u in zip(lo,hi)]
    incidence=[[int(a==v)-int(b==v) for a,b in edges] for v in range(n)]
    d0=[sum(F(a)*w for a,w in zip(row,w0)) for row in incidence]
    alpha=[d-F(rng.randrange(4),3) for d in d0]
    beta=[d+F(rng.randrange(4),3) for d in d0]
    costs=[F(rng.randrange(-8,9),3) for _ in range(n)]
    sets=[{i for i,b in enumerate(bits) if b} for bits in product([0,1],repeat=n)]
    def f(S):
        return sum(u for (a,b),u in zip(edges,hi) if a in S and b not in S)-sum(l for (a,b),l in zip(edges,lo) if a not in S and b in S)
    def g(S):
        return min(f(T)+sum(beta[i] for i in S-T)-sum(alpha[i] for i in T-S) for T in sets)
    order=sorted(range(n),key=lambda i:costs[i],reverse=True)
    greedy=[F(0)]*n
    S=set(); old=g(S)
    assert old==0
    for i in order:
        S.add(i); new=g(S); greedy[i]=new-old; old=new
    assert old==0
    assert all(sum(greedy[i] for i in S)<=g(S) for S in sets)
    value=sum(c*d for c,d in zip(costs,greedy))
    A=np.array(incidence,dtype=float)
    obj=-np.array(costs,dtype=float)@A
    sol=linprog(obj,A_ub=np.vstack([A,-A]),b_ub=np.array(beta+[-v for v in alpha],float),bounds=list(zip(map(float,lo),map(float,hi))),method='highs')
    assert sol.success
    err=abs(float(value)+sol.fun); max_error=max(max_error,err)
    assert err<1e-8
results['signed_box_support']={'cases':24,'max_direct_lp_difference':max_error,'description':'Exhaustive subset rank and exact greedy margins versus direct signed-arc LP; includes negative bounds and fixed node intervals.'}
# Symbolic quadratic identities used to retain physical contracts and the two-vector map.
import sympy as sp
q,C1,C2,B,b,s,w1=sp.symbols('q C1 C2 B b s w1')
g1=C1-q;g2=C2-q;R=b*(B-q)
w1_formula=g1*(R-g2*s)/(C1-C2)
assert sp.factor(w1_formula/g1+(R-w1_formula)/g2-s)==0
W0,v=sp.symbols('W0 v')
W1=b*(B-q)-W0
outlet=b+W0/q-W1/(1-q)
assert sp.factor(outlet.subs(W0,q*b*(B-1)+q*(1-q)*v)-v)==0
results['contract_identities']={'exact':True,'description':'Derived total-bypass inversion and two-class outlet identity independently with symbolic algebra.'}
# Exact rational stress cases for the quantitative generator-to-face estimate.
max_exposure_slack=F(0)
for m in range(1,6):
  for trial in range(25):
    S=F(rng.randrange(1,11),10)*m
    # Convex combinations of unit-box simplex vectors with identical S.
    def margins():
      a=[F(0)]*(2*m); rem=S
      for i in rng.sample(range(2*m),2*m):
        a[i]=min(F(1),rem); rem-=a[i]
      bvec=a[:];rng.shuffle(bvec)
      return [(x+y)/2 for x,y in zip(a,bvec)]
    r=margins();c=margins();W=[[a*b/S for b in c] for a in r]
    deficit=1-sum(W[i][i] for i in range(2*m))
    cross=sum(W[i][m+i] for i in range(m))
    assert S<=m+2*m*cross+4*m*deficit
    a=[int(x>=F(1,2)) for x in r]
    for i in range(m):
      if a[i]+a[m+i]==2:a[m+i]=0
      elif a[i]+a[m+i]==0:a[i]=1
    distance=sum(abs(W[i][j]-F(a[i]*a[j],m)) for i in range(2*m) for j in range(2*m))
    rhs=28*m*cross+156*m*deficit+5*(m-S)
    assert distance<=rhs
results['face_rounding']={'cases':125,'exact':True,'description':'Exact Fraction checks of exposure and stated rounding estimate at varied common totals; not a proof of general validity.'}
print(json.dumps(results,indent=2))
