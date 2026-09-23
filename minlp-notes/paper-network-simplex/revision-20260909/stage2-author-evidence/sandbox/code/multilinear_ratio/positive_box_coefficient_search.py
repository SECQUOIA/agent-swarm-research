"""Exploratory sufficient coefficient inequalities for the rho+2 conjecture."""
from math import comb
import numpy as np


def esym(ps):
 out=np.array([1.])
 for p in ps:out=np.convolve(out,[1,p])
 return out


def coefficient_slacks(xs):
 xs=np.array(xs);n=len(xs);C=np.zeros(n+1);O=np.zeros(n+1)
 breaks=sorted(set([0.,1.]+list(xs)+list(1-xs)))
 for lo,hi in zip(breaks,breaks[1:]):
  t=(lo+hi)/2;k=int(sum(xs>t))
  C+=(hi-lo)*np.array([comb(k,j) if j<=k else 0 for j in range(n+1)])
  ps=((xs>t).astype(float)+(1-xs<t).astype(float))/2
  O+=(hi-lo)*esym(ps)
 P=esym(xs);s=sum(xs);k=int(s);theta=s-k
 V=np.array([(1-theta)*(comb(k,j) if j<=k else 0)+theta*(comb(k+1,j) if j<=k+1 else 0) for j in range(n+1)])
 slack=2*C+V-P-2*O
 slack[1:]+=C[:-1]-P[:-1]
 return slack,C,V

if __name__=='__main__':
 rng=np.random.default_rng(918)
 for n in [3,4,6,8,12,20]:
  best=(0,None)
  for _ in range(3000):
   xs=rng.beta(.4,.4,n);slack,C,V=coefficient_slacks(xs)
   for j in range(2,n+1):
    val=slack[j]/max(1,C[j])
    if val<best[0]:best=(val,(j,xs))
  print(n,best,flush=True)
