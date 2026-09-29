import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from sparse_bb import instance, bnb, forward_greedy
from sparse_conflict import conflict_clique
def job(a):
    n,p,k,sigma,seed,cap=a
    X,y,lam,Ss=instance(n,p,k,seed=seed,sigma=sigma)
    t=time.time(); pool={}
    r=bnb(X,y,lam,k,S_init=[Ss,forward_greedy(X,y,lam,k)],max_nodes=cap,pool=pool)
    sups=np.array(list(pool.keys())); vals=np.array(list(pool.values()))
    om,deg,_=conflict_clique(X,y,lam,k,sups,vals,ncand=1200)
    return dict(n=n,p=p,k=k,seed=seed,done=r['done'],nodes=r['nodes'],leaves=(r['nodes']+1)//2,
                clique=om,pool=len(pool),opt=r['opt'],poolmin=float(vals.min()),
                alpha=n/(k*np.log(p)),time=time.time()-t)
if __name__=="__main__":
    out=sys.argv[1]; cap=int(sys.argv[2]); nseeds=int(sys.argv[3])
    ks=[int(v) for v in sys.argv[4].split(",")]; alphas=[float(v) for v in sys.argv[5].split(",")]
    jobs=[]
    for k in ks:
        p=6*k
        for a in alphas:
            n=max(k+1,int(round(a*k*np.log(p))))
            for s in range(nseeds): jobs.append((n,p,k,0.5,1000+s,cap))
    jobs.sort(key=lambda j:-j[2])
    with Pool(int(sys.argv[6]) if len(sys.argv)>6 else 10) as pool, open(out,"a") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
