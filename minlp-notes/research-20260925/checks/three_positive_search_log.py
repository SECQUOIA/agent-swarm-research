"""Log-scale discovery search using the full three-variable relaxation."""

from three_positive_search import *
import sys
rng=np.random.default_rng(8111);bestgap=0;t=time()
for k in range(int(sys.argv[1]) if len(sys.argv)>1 else 50000):
 Q=10**rng.uniform(-3,3,(n,n));Q=np.triu(Q)+np.triu(Q,1).T; Q/=max(np.max(Q),1)
 C=-Q@np.ones(3)+rng.uniform(-1,1,3)*np.max(Q,axis=1)
 if k%3==0: C=-Q@np.ones(3)
 q.value=Q;c.value=C
 try:v=prob.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9)
 except cp.error.SolverError:continue
 e,xx=exact(Q,C);gap=e-v
 if gap>bestgap+1e-7:
  bestgap=gap;print('BEST',k,gap,'Q',Q.tolist(),'C',C.tolist(),'exact',e,'pt',xx.tolist(),'relax',v,flush=True)
  np.savez('/tmp/minlp_three_positive_best_log.npz',Q=Q,c=C,y=y.value,keys=keys,exact=e,pt=xx)
 if k%1000==0:print('PROGRESS',k,'gap',bestgap,'seconds',time()-t,flush=True)
