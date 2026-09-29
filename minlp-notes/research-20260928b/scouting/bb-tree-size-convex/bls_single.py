"""Single-wrong-fixing certificate for binary least squares.
Condition C1: for every i, the box relaxation with x_i fixed to -xhat_i has
certified lower bound >= OPT - tol.  If C1 holds, every variable-branching
B&B tree (any rule) is a path: <= 2N+1 nodes."""
import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from bls import instance, bnb, relax_lb, relax
def job(a):
    N,M,c,seed=a
    rho=c*np.log(N)
    A,y,xs=instance(N,M,rho,seed)
    t=time.time()
    nodes,UB,done=bnb(A,y,[xs],max_nodes=100000)
    if not done:
        return dict(N=N,M=M,c=c,seed=seed,done=False,nodes=nodes)
    # recover xhat: run relaxation-free local check: use B&B incumbent value; find xhat by rounding search
    # recompute xhat by B&B returning UB only -> derive xhat via greedy descent from xs and compare
    # simpler: bnb returns UB; find xhat with f=UB among xs and its 1-flip neighbours, else skip
    f=lambda x: float(np.sum((y-A@x)**2))
    xhat=xs.copy()
    if abs(f(xhat)-UB)>1e-9*abs(UB):
        # local search to reach UB
        improved=True
        while improved:
            improved=False
            for i in range(N):
                x2=xhat.copy(); x2[i]*=-1
                if f(x2)<f(xhat)-1e-12: xhat=x2; improved=True
    ok = abs(f(xhat)-UB)<=1e-7*abs(UB)
    nprune=0; tol=1e-9*abs(UB)
    minmargin=np.inf
    for i in range(N):
        lb,_,_=relax_lb(A,y,{i:-xhat[i]})
        minmargin=min(minmargin,(lb-UB)/abs(UB))
        if lb>=UB-tol: nprune+=1
    rootlb,_,xr=relax_lb(A,y,{})
    return dict(N=N,M=M,c=c,seed=seed,done=True,nodes=nodes,xhat_found=ok,nprune=nprune,
                allprune=(nprune==N),minmargin=minmargin,ml_err=int((xhat!=xs).sum()),
                rootgap=(UB-rootlb)/abs(UB),time=time.time()-t)
if __name__=="__main__":
    out=sys.argv[1]
    Ns=[int(v) for v in sys.argv[2].split(",")]; cs=[float(v) for v in sys.argv[3].split(",")]
    mult=float(sys.argv[4]); nseeds=int(sys.argv[5])
    jobs=[(N,int(mult*N),c,s) for N in Ns for c in cs for s in range(nseeds)]
    jobs.sort(key=lambda j:(-j[0],j[2]))
    with Pool(int(sys.argv[6]) if len(sys.argv)>6 else 12) as pool, open(out,"a") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
