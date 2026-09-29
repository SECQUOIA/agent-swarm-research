import numpy as np, time, itertools
from bls import *
N,M=12,12
for rho in [1,4,16]:
    A,y,xs=instance(N,M,rho,0)
    vals=all_values(A,y); OPT=vals.min()
    # check enumeration
    i=int(np.argmin(vals)); x=to_vec(i,N); assert abs(np.sum((y-A@x)**2)-OPT)<1e-8
    t=time.time(); nodes,UB,done=bnb(A,y,[xs]); t1=time.time()
    om,_=conflict_clique(A,y,vals)
    t2=time.time(); mt=min_tree(A,y,OPT); t3=time.time()
    print(rho, "bnb",nodes,"%.2fs"%(t1-t),"UB-OPT %.2e"%(UB-OPT),"clique",om,"mintree",mt,"%.1fs"%(t3-t2))
