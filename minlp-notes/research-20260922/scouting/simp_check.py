import numpy as np, itertools
from scipy.optimize import linprog
rng=np.random.default_rng(5)
fail=0;cnt=0
for trial in range(100):
    sizes=list(rng.integers(2,5,size=int(rng.integers(2,4)))); a=[rng.normal(size=s) for s in sizes]
    xb=[rng.dirichlet(np.ones(s)) for s in sizes]
    V=[];t=[]
    for choice in itertools.product(*[range(s) for s in sizes]):
        v=np.concatenate([np.eye(s)[c] for s,c in zip(sizes,choice)]); V.append(v); t.append(sum(a[j][c] for j,c in enumerate(choice)))
    V=np.array(V);t=np.array(t); A=np.vstack([V.T,np.ones(len(V))]); b=np.append(np.concatenate(xb),1)
    # comonotone law: quantile sum
    qs=[]
    for aj,pj in zip(a,xb):
        o=np.argsort(aj); qs.append((np.concatenate([[0],np.cumsum(pj[o])]),aj[o]))
    brk=sorted(set(np.concatenate([q[0] for q in qs])))
    law=[(hi-lo, sum(q[1][np.searchsorted(q[0],(lo+hi)/2)-1] for q in qs)) for lo,hi in zip(brk[:-1],brk[1:]) if hi-lo>1e-14]
    w=np.array([x for x,_ in law]); tv=np.array([y for _,y in law])
    worst=0
    for tau in np.unique(t):
        r=linprog(-np.maximum(t-tau,0),A_eq=A,b_eq=b,bounds=(0,None),method='highs')
        worst=max(worst,-r.fun-w@np.maximum(tv-tau,0))
    cnt+=1; fail+= worst>1e-8
print("instances",cnt,"comonotone not maximal",fail)
