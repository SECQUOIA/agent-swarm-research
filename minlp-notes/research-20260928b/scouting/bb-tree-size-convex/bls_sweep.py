import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from bls import *
def job(a):
    N,M,rho,seed,do_dp=a
    A,y,xs=instance(N,M,rho,seed)
    t=time.time()
    vals=all_values(A,y); OPT=vals.min(); iopt=int(np.argmin(vals))
    xopt=to_vec(iopt,N)
    nodes,UB,done=bnb(A,y,[xs],max_nodes=200000)
    om,gaps=conflict_clique(A,y,vals)
    cnt={str(e):int((vals<=OPT+e).sum()) for e in [0.5,1,2,4]}
    mt=min_tree(A,y,OPT) if do_dp else None
    return dict(N=N,M=M,rho=rho,seed=seed,nodes=nodes,done=done,clique=om,cnt=cnt,mintree=mt,
                ml_err=int((xopt!=xs).sum()),time=time.time()-t)
if __name__=="__main__":
    out=sys.argv[1]
    jobs=[]
    for N in [10,12,14,16,18,20]:
        for M in [N,2*N]:
            for rho in [1,2,4,8,16,32]:
                for s in range(10):
                    jobs.append((N,M,rho,s, N<=10))
    jobs.sort(key=lambda j:-j[0])
    with Pool(30) as pool, open(out,"w") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
