"""Discovery-only random search; numerical results do not certify exactness."""

import cvxpy as cp
import numpy as np
from itertools import product,combinations
from time import time
n=3
keys=[p for p in product(range(3),repeat=n) if p.count(2)<=1 and all(x<=1 for x in p if x!=2)]
# remove patterns two 2 automatically; count is 20.
idx={p:i for i,p in enumerate(keys)};y=cp.Variable(len(keys));q=cp.Parameter((3,3),symmetric=True);c=cp.Parameter(3)
def moment(p): return y[idx[tuple(p)]]
def loc(free,fixed):
 powers=[(0,0,0)]+[tuple(int(j==i) for j in range(n)) for i in free]
 def entry(a,b):
  exponent=tuple(x+z for x,z in zip(a,b)); terms={exponent:1}
  for k,v in fixed.items():
   new={}
   for p,coeff in terms.items():
    r=list(p);r[k]+=1;r=tuple(r)
    new[r]=new.get(r,0)+(coeff if v else -coeff)
    if not v:new[p]=new.get(p,0)+coeff
   terms=new
  return sum(coeff*moment(p) for p,coeff in terms.items())
 return cp.bmat([[entry(a,b) for b in powers] for a in powers])
constraints=[moment((0,0,0))==1]
for status in product((-1,0,1),repeat=n):
 free=[i for i,s in enumerate(status) if s==-1];fixed={i:s for i,s in enumerate(status) if s!=-1}
 constraints.append(loc(free,fixed)>>0)
x=cp.hstack([moment(tuple(int(j==i) for j in range(n))) for i in range(n)])
Y=cp.bmat([[moment(tuple(int(k==i)+int(k==j) for k in range(n))) for j in range(n)] for i in range(n)])
prob=cp.Problem(cp.Minimize(cp.sum(cp.multiply(q,Y))+c@x),constraints)
def exact(Q,C):
 best=np.inf;pt=None
 for status in product((-1,0,1),repeat=n):
  free=[i for i,s in enumerate(status) if s==-1];bound=[i for i,s in enumerate(status) if s!=-1];xx=np.array(status,float)
  if free:
   try:xx[free]=np.linalg.solve(2*Q[np.ix_(free,free)],-C[free]-2*Q[np.ix_(free,bound)]@xx[bound])
   except np.linalg.LinAlgError:continue
   if np.any(xx[free]<-1e-8) or np.any(xx[free]>1+1e-8):continue
  val=xx@Q@xx+C@xx
  if val<best:best=val;pt=xx
 return best,pt
if __name__=='__main__':
 import sys
 rng=np.random.default_rng(198);bestgap=0;t=time()
 for k in range(int(sys.argv[1]) if len(sys.argv)>1 else 2000):
  Q=rng.uniform(0,5,(n,n));Q=(Q+Q.T)/2
  np.fill_diagonal(Q,rng.uniform(.01,3,n))
  if k%3==0:C=-Q@np.ones(3) # centered symmetry
  else:C=-Q@np.ones(3)+rng.normal(0,.5,3)
  q.value=Q;c.value=C
  try:v=prob.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9)
  except cp.error.SolverError:continue
  e,xx=exact(Q,C);gap=e-v
  if gap>bestgap+1e-7:
   bestgap=gap;print('BEST',k,gap,'Q',Q.tolist(),'C',C.tolist(),'exact',e,'pt',xx.tolist(),'relax',v,flush=True)
   np.savez('/tmp/minlp_three_positive_best.npz',Q=Q,c=C,y=y.value,keys=keys,exact=e,pt=xx)
  if k%100==0:print('PROGRESS',k,'gap',bestgap,'seconds',time()-t,flush=True)
