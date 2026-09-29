"""Targeted numerical challenge of proposed PSD-center SDP exactness."""
import itertools
import numpy as np
import cvxpy as cp
rng=np.random.default_rng(20260928)
def boxmin(Q,b):
 k=len(b); best=None
 for status in itertools.product((0,1,2),repeat=k):
  free=[i for i,s in enumerate(status) if s==2]
  fixed=[i for i,s in enumerate(status) if s!=2]
  x=np.array([float(s) if s<2 else 0.0 for s in status],dtype=float)
  if free:
   x[free]=np.linalg.solve(Q[np.ix_(free,free)],-b[free]/2-Q[np.ix_(free,fixed)]@x[fixed])
  if min(x)<-1e-8 or max(x)>1+1e-8: continue
  val=x@Q@x+b@x
  if best is None or val<best[0]:best=(val,x)
 return best
for nC,nB in [(2,2)]:
 n=nC+nB; m=cp.Variable(n); X=cp.Variable((n,n),symmetric=True)
 pQ=cp.Parameter((n,n),symmetric=True); pb=cp.Parameter(n); pu=cp.Parameter(nB)
 constraints=[cp.bmat([[np.ones((1,1)),cp.reshape(m,(1,n),order='C')],[cp.reshape(m,(n,1),order='C'),X]])>>0,X<=cp.reshape(m,(n,1),order='C'),m[nC:]==pu]
 prob=cp.Problem(cp.Minimize(cp.sum(cp.multiply(pQ,X))+pb@m),constraints)
 for rep in range(300):
  Q=-rng.integers(0,9,size=(n,n)).astype(float);Q=(Q+Q.T)/2
  H=-rng.integers(0,8,size=(nC,nC)).astype(float);H=(H+H.T)/2;np.fill_diagonal(H,0);np.fill_diagonal(H,-H.sum(1)+rng.integers(1,7,size=nC))
  Q[:nC,:nC]=H;Q[0,3]=Q[3,0]=Q[1,2]=Q[2,1]=Q[2,3]=Q[3,2]=0;np.fill_diagonal(Q[nC:,nC:],-rng.integers(0,7,size=nB))
  b=rng.integers(-8,30,size=n).astype(float);u=np.array([1/3,2/3])
  true=0;prev=0
  for t in list(u)+[1]:
   z=(u>prev+1e-10).astype(float)
   v,x=boxmin(H,b[:nC]+2*Q[:nC,nC:]@z)
   v+=z@Q[nC:,nC:]@z+b[nC:]@z
   true+=(t-prev)*v;prev=t
  pQ.value=Q;pb.value=b;pu.value=u
  prob.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8)
  gap=true-prob.value
  if gap>1e-5:
   print('GAP',nC,nB,rep,gap,'true',true,'sdp',prob.value);print('Q=',Q.tolist());print('b=',b.tolist());print('u=',u.tolist());np.savez('research-20260928/submodular/psd_center_path_counterexample.npz',Q=Q,b=b,u=u,m=m.value,X=X.value);raise SystemExit
 print('No gap',nC,nB)
