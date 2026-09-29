import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from sparse_bb import instance, bnb, forward_greedy
from sparse_conflict import all_supports, conflict_clique
from dp_min_tree import min_tree
def job(a):
    n,p,k,sigma,seed=a
    X,y,lam,Ss=instance(n,p,k,seed=seed,sigma=sigma)
    t=time.time()
    size,OPT,ns=min_tree(X,y,lam,k)
    sups,vals=all_supports(X,y,lam,k)
    om,_,_=conflict_clique(X,y,lam,k,sups,vals,ncand=len(vals))
    r=bnb(X,y,lam,k,S_init=[Ss,forward_greedy(X,y,lam,k)])
    return dict(n=n,p=p,k=k,seed=seed,min_leaves=(size+1)//2,bnb_leaves=(r['nodes']+1)//2,clique=om,time=time.time()-t)
if __name__=="__main__":
    p=int(sys.argv[1]);k=int(sys.argv[2]);nseeds=int(sys.argv[3]);ns=[int(v) for v in sys.argv[4].split(",")];out=sys.argv[5]
    jobs=[(n,p,k,0.5,s) for n in ns for s in range(nseeds)]
    with Pool(int(sys.argv[6]) if len(sys.argv)>6 else 12) as pool, open(out,"w") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
