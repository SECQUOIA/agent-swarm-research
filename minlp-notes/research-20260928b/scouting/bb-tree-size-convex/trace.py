import numpy as np, sys
from sparse_bb import Relaxation, instance, exact_value, forward_greedy
import itertools
n,p,k,seed=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
X,y,lam,Ss=instance(n,p,k,seed=seed,sigma=0.5)
R=Relaxation(X,y,lam,k)
G=forward_greedy(X,y,lam,k)
UB=min(exact_value(X,y,lam,Ss),exact_value(X,y,lam,G))
print("true",Ss,"greedy",G,"UB",UB)
LB,val,z=R.solve_ipm((),())
print("root LB %.4f gap %.4f"%(LB,(UB-LB)/UB))
print("root z on S*:",np.round(z[list(Ss)],3)," max z off S*: %.3f  sum z off S*: %.3f"%(np.delete(z,list(Ss)).max(),np.delete(z,list(Ss)).sum()))
# single-fixing children
pr0=[];pr1=[]
for i in range(p):
    lb0,_,_=R.solve_ipm((i,),()); lb1,_,_=R.solve_ipm((),(i,))
    if i in Ss: pr0.append(lb0>=UB*(1-1e-6))
    else: pr1.append(lb1>=UB*(1-1e-6))
print("true i: z_i=0 child prunable: %d/%d"%(sum(pr0),len(pr0)), "  null i: z_i=1 child prunable: %d/%d"%(sum(pr1),len(pr1)))
