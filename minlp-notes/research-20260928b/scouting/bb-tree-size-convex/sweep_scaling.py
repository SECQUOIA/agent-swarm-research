import os, sys, json, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from sweep import run

if __name__=="__main__":
    out=sys.argv[1]; sigma=float(sys.argv[2]); cap=int(sys.argv[3]); nseeds=int(sys.argv[4])
    ks=[int(v) for v in sys.argv[5].split(",")]; alphas=[float(v) for v in sys.argv[6].split(",")]
    pmult=int(sys.argv[7]) if len(sys.argv)>7 else 6
    jobs=[]
    for k in ks:
        p=pmult*k
        for a in alphas:
            n=max(k+1,int(round(a*k*np.log(p))))
            for s in range(nseeds):
                jobs.append((n,p,k,sigma,1000+s,cap,"maxfrac"))
    # longest first
    jobs.sort(key=lambda j:-j[2])
    with Pool(34) as pool, open(out,"a") as f:
        for res in pool.imap_unordered(run, jobs):
            res['alpha']=res['n']/(res['k']*np.log(res['p']))
            f.write(json.dumps(res)+"\n"); f.flush()
