"""Independent dense checks of the intrinsic partial-packet locality bound.
Floating-point checks supplement, and do not prove, the symbolic theorem.
"""
import itertools
import json
from pathlib import Path
import numpy as np

n=7
gamma=0.6
signal=1.0
kappa=signal/(1+signal)
base=np.diag([1.,1.,0.])
perms=[np.eye(3)[list(p)] for p in itertools.permutations(range(3))]
rot=[perms[t%6] for t in range(n)]
latent=[u@base@u.T for u in rot]
trans=[None]+[gamma*rot[t]@base@rot[t-1].T for t in range(1,n)]
obs=[np.array([[1.,-1.,0.]])/2 if t%2==0 else np.array([[1.,0.,1.],[0.,1.,-1.]])/3 for t in range(n)]
noise=[np.eye(h.shape[0]) for h in obs]
for t in range(n):
 assert np.linalg.eigvalsh(signal*noise[t]-obs[t]@latent[t]@obs[t].T).min()>-1e-12
 if t:
  q=latent[t]-trans[t]@latent[t-1]@trans[t].T
  assert np.linalg.eigvalsh(q-(1-gamma**2)*latent[t]).min()>-1e-12
blocks={}
for t in range(n):
 blocks[t,t]=obs[t]@latent[t]@obs[t].T+noise[t]
 for j in range(t):
  a=np.eye(3)
  for u in range(j+1,t+1): a=trans[u]@a
  blocks[t,j]=obs[t]@a@latent[j]@obs[j].T
  blocks[j,t]=blocks[t,j].T

def covariance(indices):
 return np.block([[blocks[t,j] for j in indices] for t in indices])

count=0
worst=0.
for mask in range(1,1<<n):
 selected=[t for t in range(n) if mask>>t&1]
 sizes=[obs[t].shape[0] for t in selected]
 offsets=np.cumsum([0]+sizes)
 r=covariance(selected)
 for window in range(n):
  a=np.eye(sum(sizes)); d=np.zeros_like(r)
  for i,t in enumerate(selected):
   history=[j for j in selected[:i] if j>=t-window]
   rows=slice(offsets[i],offsets[i+1])
   v=blocks[t,t].copy()
   if history:
    rhh=covariance(history)
    cross=np.hstack([blocks[t,j] for j in history])
    regression=np.linalg.solve(rhh,cross.T).T
    v-=regression@cross.T
    col=0
    for j in history:
     jj=selected.index(j); length=sizes[jj]
     a[rows,offsets[jj]:offsets[jj+1]]=-regression[:,col:col+length]
     col+=length
   d[rows,rows]=v
  chol=np.linalg.cholesky(d)
  normalized=np.linalg.solve(chol,a@r@a.T)
  normalized=np.linalg.solve(chol,normalized.T).T
  error=max(abs(np.linalg.eigvalsh(normalized)-1))
  near=gamma**(window+2)*(1-gamma**window)*(1-gamma**(window+1))/((1-gamma)*(1-gamma**2))
  delta=0. if window==n-1 else 2*kappa*(gamma**(window+1)/(1-gamma)+np.sqrt(kappa*signal)*near)
  assert error<=delta+1e-12,(selected,window,error,delta)
  if delta: worst=max(worst,error/delta)
  q=a.T@np.linalg.solve(d,a)
  inv=np.linalg.inv(r)
  assert np.linalg.eigvalsh(q-(1-delta)*inv).min()>-1e-11
  assert np.linalg.eigvalsh((1+delta)*inv-q).min()>-1e-11
  count+=1
report={'status':'pass','arithmetic':'float64 diagnostic, not formal proof','cases':count,'candidate_times':n,'latent_dimension':3,'latent_rank':2,'packet_dimensions':[h.shape[0] for h in obs],'largest_error_to_bound_ratio':worst,'checks':['intrinsic promises','dense normalized residual bound','both precision sandwich directions','full-history exactness']}
Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
