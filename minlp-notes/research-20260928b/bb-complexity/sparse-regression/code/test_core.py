import sys, time, numpy as np
sys.path.insert(0,'/home/sgusev/repo/minlp-notes/research-20260928b/scouting/bb-tree-size-convex')
from sparse_bb import Relaxation, instance as inst0
from core import *
rng=np.random.default_rng(3)
for trial in range(6):
    n,p,k=int(rng.integers(15,40)),int(rng.integers(20,50)),int(rng.integers(2,6))
    X,y,lam,Ss=inst0(n,p,k,seed=trial,sigma=0.5)
    perm=rng.permutation(p); S0=tuple(perm[:rng.integers(0,3)].tolist()); S1=tuple(perm[3:3+rng.integers(0,3)].tolist())
    R=Relaxation(X,y,lam,k)
    t0=time.time(); LB0,v0,_=R.solve_ipm(S0,S1); t1=time.time()
    LB1,v1,z1,a1=solve_node(X,y,lam,k,S0,S1); t2=time.time()
    print(n,p,k,len(S0),len(S1),"scout LB %.9f val %.9f | new LB %.9f val %.9f  (%.0fms %.0fms)"%(LB0,v0,LB1,v1,1e3*(t1-t0),1e3*(t2-t1)))
# speed test
X,y,lam,Ss=instance(150,1000,10,tau0=1.5,seed=1)
t0=time.time(); LB,v,z,a=solve_node(X,y,lam,10); print("p=1000 n=150 root: LB %.6f val %.6f gap %.2e time %.2fs"%(LB,v,v-LB,time.time()-t0))
