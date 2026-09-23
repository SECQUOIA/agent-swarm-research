import numpy as np, itertools
from scipy.optimize import linprog
rng=np.random.default_rng(3)
def verts(n,k):
    return np.array([[1 if i in S else 0 for i in range(n)] for S in itertools.combinations(range(n),k)],float)
cnt=0;fail=0;bad=[]
for trial in range(100):
    n=int(rng.integers(4,7)); k=int(rng.integers(2,n-1)) if n>3 else 1; a=rng.normal(size=n)
    p=rng.uniform(size=n)
    for _ in range(200): p=np.clip(p+(k-p.sum())/n,0,1)
    if abs(p.sum()-k)>1e-9: continue
    V=verts(n,k); t=V@a; taus=np.unique(t)
    A=np.vstack([V.T,np.ones(len(V))]); b=np.append(p,1)
    sups=[]
    for tau in taus:
        r=linprog(-np.maximum(t-tau,0),A_eq=A,b_eq=b,bounds=(0,None),method='highs'); sups.append(-r.fun)
    # can a single law attain all sups? add constraints stop-loss >= sup - eps
    G=-np.array([np.maximum(t-tau,0) for tau in taus]); h=-(np.array(sups)-1e-9)
    r=linprog(np.zeros(len(V)),A_ub=G,b_ub=h,A_eq=A,b_eq=b,bounds=(0,None),method='highs')
    cnt+=1; 
    if r.status!=0: fail+=1
print("instances",cnt,"no maximal element",fail)
