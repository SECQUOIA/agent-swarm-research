"""Exploratory single-product test for fixed positive boxes [1,rho]."""
import numpy as np


def values(xs,rho=2.):
 rho=float(rho)
 xs=np.array(xs);s=sum(xs);k=int(np.floor(s));v=rho**k*(1+(rho-1)*(s-k))
 breaks=sorted(set([0.,1.]+list(xs)+list(1-xs)))
 cav=ori=0.
 for lo,hi in zip(breaks,breaks[1:]):
  t=(lo+hi)/2
  cav+=(hi-lo)*rho**sum(xs>t)
  probs=((xs>t).astype(float)+(1-xs<t).astype(float))/2
  ori+=(hi-lo)*np.prod(1+(rho-1)*probs)
 return cav,v,ori

if __name__=='__main__':
 rng=np.random.default_rng(772)
 for rho in [1.01,1.1,2,10]:
  best=(0,None)
  for d in [2,3,4,5,8,12,20]:
   for _ in range(3000):
    xs=rng.beta(.3,.3,d)
    cav,v,ori=values(xs,rho)
    if cav-ori>1e-12:
     rat=(cav-v)/(cav-ori)
     if rat>best[0]:best=(rat,xs)
  print('rho',rho,'best',best,flush=True)
