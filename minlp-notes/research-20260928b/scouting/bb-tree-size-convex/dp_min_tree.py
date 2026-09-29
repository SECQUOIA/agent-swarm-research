"""Exact minimum size of a variable-branching B&B tree (perspective relaxation,
incumbent = OPT given) for tiny instances, by dynamic programming over partial
assignments.  A node is a leaf iff it is prunable: |S1|>k, or LB >= OPT(1-rtol).
Size counts all nodes of the (full binary) tree."""
import os, sys, json, itertools, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from functools import lru_cache
from multiprocessing import Pool
from sparse_bb import Relaxation, instance, exact_value, bnb, forward_greedy

def min_tree(X,y,lam,k,rtol=1e-6):
    n,p=X.shape
    OPT=min(exact_value(X,y,lam,S) for S in itertools.combinations(range(p),k))
    rel=Relaxation(X,y,lam,k)
    thr=OPT*(1-rtol)
    @lru_cache(maxsize=None)
    def T(m0,m1):
        S1=[i for i in range(p) if m1>>i&1]
        if len(S1)>k: return 1
        S0=[i for i in range(p) if m0>>i&1]
        LB,_,z=rel.solve_ipm(tuple(S0),tuple(S1))
        if LB>=thr: return 1
        best=None
        for i in range(p):
            if (m0|m1)>>i&1: continue
            v=T(m0|1<<i,m1)
            if best is not None and v>=best: continue
            v+=T(m0,m1|1<<i)
            if best is None or v<best: best=v
        return 1+best
    size=T(0,0)
    return size, OPT, rel.nsolves

def job(a):
    n,p,k,sigma,seed=a
    X,y,lam,Ss=instance(n,p,k,seed=seed,sigma=sigma)
    t0=time.time()
    size,OPT,ns=min_tree(X,y,lam,k)
    r=bnb(X,y,lam,k,S_init=[Ss,forward_greedy(X,y,lam,k)])
    return dict(n=n,p=p,k=k,sigma=sigma,seed=seed,min_tree=size,bnb_nodes=r['nodes'],opt=OPT,
                rootLB=r['root_LB'],nsolves=ns,time=time.time()-t0)

if __name__=="__main__":
    p=int(sys.argv[1]);k=int(sys.argv[2]);sigma=float(sys.argv[3]);nseeds=int(sys.argv[4])
    ns=[int(v) for v in sys.argv[5].split(",")]; out=sys.argv[6]
    jobs=[(n,p,k,sigma,s) for n in ns for s in range(nseeds)]
    with Pool(int(sys.argv[7]) if len(sys.argv)>7 else 8) as pool, open(out,"a") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
