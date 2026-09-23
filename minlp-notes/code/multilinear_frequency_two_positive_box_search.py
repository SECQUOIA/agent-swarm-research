"""Seeded numerical search for frequency-two gaps on positive boxes.

Individual envelopes use the original terms, not their affine expansions.
Subtracting affine parts and positive rescaling only condition the LPs.
The maximin LP also optimizes coefficient weights. Results are exploratory:
floating-point HiGHS values are not proof certificates. The best sample is
written to /tmp/positive_freq2_graph_best.json.
"""
import numpy as np
from scipy.optimize import linprog
import json
rng=np.random.default_rng(19304);best=1.0
for n in range(4,11):
 V=((np.arange(2**n,dtype=np.uint64)[:,None] >> np.arange(n,dtype=np.uint64))&1).astype(float)
 A=np.vstack((np.ones(2**n),V.T)); eq=np.column_stack((A,np.zeros(n+1)))
 for it in range(500):
  k=int(rng.integers(3,min(n,6)+1))
  S=[[] for _ in range(k)]
  for i in range(n):
   ends=rng.choice(k,size=2,replace=False)
   for v in ends:S[v].append(i)
  if min(map(len,S))<2 or len(set(map(tuple,S)))<k:continue
  alpha=10**rng.uniform(-4,-.005,n)
  if it%3==0:alpha=rng.uniform(.5,.99,n)
  if it%7==0:alpha=np.full(n,float(rng.choice([.01,.2,.5,.9,.99])))
  p=1/(1+np.exp(-rng.uniform(-4,4,n)))
  if it%4==0:p=rng.choice([.1,.25,.5,.75,.9],size=n)
  if it%10==0:p=np.full(n,.5)
  b=np.r_[1,p]
  values=np.column_stack([np.prod(alpha[s]+(1-alpha[s])*V[:,s],axis=1) for s in S])
  affine0=values[0].copy();gradient=np.column_stack([values[1<<i]-affine0 for i in range(n)]).T
  values-=affine0+V@gradient
  scales=values[-1].copy()
  if min(scales)<1e-12:continue
  values/=scales
  t=np.r_[0,np.sort(p),1];M=(t[:-1]+t[1:])/2;W=(M[:,None]<=p).astype(float)
  upraw=np.array([np.dot(np.diff(t),np.prod(alpha[s]+(1-alpha[s])*W[:,s],axis=1)) for s in S])
  upper=(upraw-affine0-p@gradient)/scales
  lower=np.array([linprog(values[:,j],A_eq=A,b_eq=b,bounds=(0,None),method='highs').fun for j in range(k)])
  T=upper-lower
  if min(T)<1e-7:continue
  D=(upper-values)/T
  lp=linprog(np.r_[np.zeros(2**n),-1],A_ub=np.column_stack((-D.T,np.ones(k))),b_ub=np.zeros(k),A_eq=eq,b_eq=b,bounds=[(0,None)]*(2**n)+[(0,1)],method='highs')
  if not lp.success:continue
  ratio=1/lp.x[-1]
  if ratio>best+1e-6:
   best=ratio;rec=dict(n=n,it=it,ratio=ratio,alpha=alpha.tolist(),p=p.tolist(),supports=S,upper=upper.tolist(),lower=lower.tolist(),coefficients=(-lp.ineqlin.marginals/T/scales).tolist())
   print(json.dumps(rec),flush=True)
   with open('/tmp/positive_freq2_graph_best.json','w') as f:json.dump(rec,f)
 print('done',n,'best',best,flush=True)
