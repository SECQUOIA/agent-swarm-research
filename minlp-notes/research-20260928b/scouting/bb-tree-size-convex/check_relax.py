import numpy as np, cvxpy as cp, time
from sparse_bb import Relaxation, instance
def cvx_relax(X,y,lam,k,S0,S1):
    n,p=X.shape
    b=cp.Variable(p); z=cp.Variable(p); t=cp.Variable(p)
    cons=[z>=0,z<=1,cp.sum(z)<=k]
    for i in range(p):
        cons.append(cp.quad_over_lin(b[i],z[i])<=t[i]) if i not in S0 else cons.append(b[i]==0)
    for i in S0: cons+= [z[i]==0, t[i]==0]
    for i in S1: cons.append(z[i]==1)
    pr=cp.Problem(cp.Minimize(cp.sum_squares(y-X@b)+lam*cp.sum(t)),cons)
    pr.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    return pr.value
rng=np.random.default_rng(1)
for trial in range(8):
    n,p,k=int(rng.integers(8,30)),int(rng.integers(10,25)),int(rng.integers(2,5))
    X,y,lam,Ss=instance(n,p,k,seed=trial,sigma=0.5)
    perm=rng.permutation(p); S0=tuple(perm[:rng.integers(0,3)].tolist()); S1=tuple(perm[3:3+rng.integers(0,2)].tolist())
    R=Relaxation(X,y,lam,k)
    t0=time.time(); LB,val,z=R.solve(S0,S1); t1=time.time()
    v=cvx_relax(X,y,lam,k,S0,S1)
    print(n,p,k,S0,S1,"LB=%.8f val=%.8f cvx=%.8f  time=%.1fms"%(LB,val,v,1000*(t1-t0)))
