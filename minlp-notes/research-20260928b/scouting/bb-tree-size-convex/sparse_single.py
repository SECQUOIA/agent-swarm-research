"""Single-wrong-fixing certificate for perspective B&B in sparse regression.
C1: for every i in S_opt, LB(z_i=0) >= OPT(1-rtol), and for every i not in
S_opt, LB(z_i=1) >= OPT(1-rtol).  If C1 holds, every variable-branching tree
(any rule/node order, incumbent OPT) is a path with pruned siblings."""
import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from sparse_bb import Relaxation, instance, exact_value, bnb, forward_greedy
def job(a):
    n,p,k,sigma,seed,cap=a
    X,y,lam,Ss=instance(n,p,k,seed=seed,sigma=sigma)
    t=time.time()
    r=bnb(X,y,lam,k,S_init=[Ss,forward_greedy(X,y,lam,k)],max_nodes=cap)
    if not r['done']:
        return dict(n=n,p=p,k=k,seed=seed,done=False,nodes=r['nodes'])
    OPT=r['opt']; So=set(r['support']); thr=OPT*(1-1e-6)
    R=Relaxation(X,y,lam,k)
    bad0=sum(1 for i in So if R.solve_ipm((i,),())[0]<thr)
    bad1=sum(1 for i in range(p) if i not in So and R.solve_ipm((),(i,))[0]<thr)
    return dict(n=n,p=p,k=k,seed=seed,done=True,nodes=r['nodes'],bad0=bad0,bad1=bad1,
                c1=(bad0+bad1==0),recov=(So==set(Ss)),alpha=n/(k*np.log(p)),time=time.time()-t)
if __name__=="__main__":
    out=sys.argv[1]; cap=int(sys.argv[2]); nseeds=int(sys.argv[3])
    ks=[int(v) for v in sys.argv[4].split(",")]; alphas=[float(v) for v in sys.argv[5].split(",")]
    jobs=[]
    for k in ks:
        p=6*k
        for a in alphas:
            n=max(k+1,int(round(a*k*np.log(p))))
            for s in range(nseeds): jobs.append((n,p,k,0.5,2000+s,cap))
    jobs.sort(key=lambda j:(-j[2],j[0]))
    with Pool(int(sys.argv[6]) if len(sys.argv)>6 else 12) as pool, open(out,"a") as f:
        for r in pool.imap_unordered(job,jobs):
            f.write(json.dumps(r)+"\n"); f.flush()
