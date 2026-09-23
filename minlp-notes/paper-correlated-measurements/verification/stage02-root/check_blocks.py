"""Dense diagnostic of the improved complete-block far-pair bound."""
import json
from pathlib import Path
import numpy as np

n=6; rho=.6; pbar=1.; kappa=.5
p=np.diag([1.,.5]); v=np.eye(2)
a=[None]+[rho*(np.array([[.6,-.8],[.8,.6]]) if t%2 else np.diag([1.,-1.])) for t in range(1,n)]
for t in range(1,n): assert np.linalg.eigvalsh(p-a[t]@p@a[t].T).min()>0
r=np.zeros((2*n,2*n))
for t in range(n):
 r[2*t:2*t+2,2*t:2*t+2]=p+v
 for j in range(t):
  phi=np.eye(2)
  for u in range(j+1,t+1): phi=a[u]@phi
  c=phi@p
  r[2*t:2*t+2,2*j:2*j+2]=c
  r[2*j:2*j+2,2*t:2*t+2]=c.T
counts={'subset_windows':0,'far_pairs':0}; worst=0.
for mask in range(1,1<<n):
 selected=[t for t in range(n) if mask>>t&1]
 ids=[j for t in selected for j in [2*t,2*t+1]]
 cov=r[np.ix_(ids,ids)]
 for window in range(n):
  residual=np.eye(len(ids)); d=np.zeros_like(cov)
  for i,t in enumerate(selected):
   hist=[h for h in range(i) if selected[h]>=t-window]
   rows=[2*i,2*i+1]; cols=[u for h in hist for u in [2*h,2*h+1]]
   dt=cov[np.ix_(rows,rows)].copy()
   if hist:
    cross=cov[np.ix_(rows,cols)]
    reg=np.linalg.solve(cov[np.ix_(cols,cols)],cross.T).T
    residual[np.ix_(rows,cols)]=-reg
    dt-=reg@cross.T
   d[np.ix_(rows,rows)]=dt
  c=residual@cov@residual.T
  for i,t in enumerate(selected):
   for j,s in enumerate(selected[:i]):
    if t-s>window:
     val=np.linalg.norm(c[2*i:2*i+2,2*j:2*j+2],2)
     assert val<=pbar*rho**(t-s)+1e-12
     counts['far_pairs']+=1
  chol=np.linalg.cholesky(d)
  normalized=np.linalg.solve(chol,c)
  normalized=np.linalg.solve(chol,normalized.T).T
  error=max(abs(np.linalg.eigvalsh(normalized)-1))
  near=rho**(window+2)*(1-rho**window)*(1-rho**(window+1))/((1-rho)*(1-rho**2))
  delta=0. if window==n-1 else 2*pbar*(rho**(window+1)/(1-rho)+kappa*near)
  assert error<=delta+1e-12
  if delta: worst=max(worst,error/delta)
  counts['subset_windows']+=1
report={'status':'pass','arithmetic':'float64 diagnostic, not proof','counts':counts,'largest_error_to_bound_ratio':worst,'model':'noncommuting two-dimensional complete packets, positive process covariance'}
Path(__file__).with_name('blocks-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
