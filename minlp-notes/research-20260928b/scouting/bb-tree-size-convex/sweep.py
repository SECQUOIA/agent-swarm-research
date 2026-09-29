import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from sparse_bb import bnb, instance, forward_greedy, exact_value

def run(args):
    n,p,k,sigma,seed,cap,branch = args
    X,y,lam,Ss = instance(n,p,k,seed=seed,sigma=sigma)
    G = forward_greedy(X,y,lam,k)
    t0=time.time()
    r = bnb(X,y,lam,k,S_init=[Ss,G],max_nodes=cap,branch=branch)
    return dict(n=n,p=p,k=k,sigma=sigma,seed=seed,nodes=r['nodes'],done=r['done'],opt=r['opt'],
                rootLB=r['root_LB'],supp=list(r['support']),true=list(Ss),
                exact_true=exact_value(X,y,lam,Ss), time=time.time()-t0, branch=branch)

if __name__=="__main__":
    p=int(sys.argv[1]); k=int(sys.argv[2]); sigma=float(sys.argv[3]); cap=int(sys.argv[4]); nseeds=int(sys.argv[5])
    ns=[int(v) for v in sys.argv[6].split(",")]; branch=sys.argv[7] if len(sys.argv)>7 else "maxfrac"
    out=sys.argv[8] if len(sys.argv)>8 else f"sweep_p{p}_k{k}_s{sigma}_{branch}.jsonl"
    jobs=[(n,p,k,sigma,s,cap,branch) for n in ns for s in range(nseeds)]
    with Pool(34) as pool, open(out,"a") as f:
        for res in pool.imap_unordered(run, jobs):
            f.write(json.dumps(res)+"\n"); f.flush()
            print(res['n'],res['seed'],res['nodes'],res['done'],"%.1fs"%res['time'],flush=True)
