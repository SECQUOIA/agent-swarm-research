import numpy as np, itertools
from scipy.optimize import linprog
rng=np.random.default_rng(3)
def verts(n,k):
    return np.array([[1 if i in S else 0 for i in range(n)] for S in itertools.combinations(range(n),k)],float)
def systematic(p,a):
    # units sorted by a descending; systematic sampling with uniform U over cumulative sums
    o=np.argsort(-a); cs=np.concatenate([[0],np.cumsum(p[o])])
    # breakpoints in U in [0,1): unit o[j] selected if interval [cs[j],cs[j+1]) contains U+m for some integer m
    pts=sorted(set(np.concatenate([cs%1,[0.0,1.0]])))
    law=[]
    for lo,hi in zip(pts[:-1],pts[1:]):
        if hi-lo<1e-14: continue
        U=(lo+hi)/2; S=[o[j] for j in range(len(p)) if any(cs[j]<=U+m<cs[j+1] for m in range(int(np.ceil(cs[-1]))+1))]
        law.append((hi-lo,a[S].sum(),len(S)))
    return law
worst=0
for trial in range(200):
    n=rng.integers(4,8); k=rng.integers(1,n); a=rng.normal(size=n)
    p=rng.uniform(size=n); 
    # project p to sum k within [0,1] by simple scaling iterations
    for _ in range(100):
        p=np.clip(p+(k-p.sum())/n,0,1)
    if abs(p.sum()-k)>1e-9: continue
    V=verts(n,k); law=systematic(p,a)
    assert all(abs(s-k)<1e-9 for _,_,s in law)
    tv=np.array([t for _,t,_ in law]); wv=np.array([w for w,_,_ in law])
    for tau in np.linspace((V@a).min(),(V@a).max(),15):
        f=np.maximum(V@a-tau,0)
        res=linprog(-f,A_eq=np.vstack([V.T,np.ones(len(V))]),b_eq=np.append(p,1),bounds=(0,None),method='highs')
        sup=-res.fun; sysv=wv@np.maximum(tv-tau,0)
        worst=max(worst,sup-sysv)
print("max gap sup stop-loss minus systematic stop-loss:",worst)
