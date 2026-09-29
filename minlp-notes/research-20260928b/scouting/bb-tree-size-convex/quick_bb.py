import numpy as np, time, itertools
from sparse_bb import bnb, instance, forward_greedy, exact_value
p,k=20,3
for n in [6,10,15,20,30]:
    X,y,lam,Ss=instance(n,p,k,seed=1,sigma=0.5)
    t0=time.time()
    G=forward_greedy(X,y,lam,k)
    r=bnb(X,y,lam,k,S_init=[Ss,G])
    # brute force check
    best=min((exact_value(X,y,lam,S),S) for S in itertools.combinations(range(p),k))
    print(n, r['nodes'], r['done'], "%.6f"%r['opt'], r['support'], "brute %.6f"%best[0], best[1], "true",Ss, "rootLB %.4f"%r['root_LB'], "%.1fs"%(time.time()-t0))
