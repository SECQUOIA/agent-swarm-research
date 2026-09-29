import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from bls import instance, bnb
def job(a):
    N,M,rho,seed,cap=a
    A,y,xs=instance(N,M,rho,seed)
    t=time.time()
    nodes,UB,done=bnb(A,y,[xs],max_nodes=cap)
    return dict(N=N,M=M,rho=rho,seed=seed,nodes=nodes,done=done,time=time.time()-t)
if __name__=="__main__":
    out=sys.argv[1]; cap=int(sys.argv[2])
    Ns=[int(v) for v in sys.argv[3].split(",")]; rhos=sys.argv[4].split(",")
    mult=float(sys.argv[5]); nseeds=int(sys.argv[6])
    jobs=[(N,int(mult*N),(float(r[1:])*np.log(N) if r.startswith('L') else float(r)),s,cap) for N in Ns for r in rhos for s in range(nseeds)]
    jobs.sort(key=lambda j:j[0])
    with Pool(int(sys.argv[7]) if len(sys.argv)>7 else 30) as pool, open(out,"a") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
