import numpy as np, itertools
from scipy.optimize import linprog
rng=np.random.default_rng(1)
def box_env(sig,a,b,l,u,xbar,N):
    grids=[np.linspace(l[i],u[i],N) for i in range(len(a))]
    P=np.array(list(itertools.product(*grids)))
    f=sig(P@a+b)
    A=np.vstack([P.T,np.ones(len(P))]); r=np.append(xbar,1)
    res=linprog(f,A_eq=A,b_eq=r,bounds=(0,None),method='highs')
    return res.fun
def staircase(a,b,l,u,xbar):
    # assume a>0 after flips
    p=(xbar-l)/(u-l); order=np.argsort(-p)  # coordinates flip to u in decreasing p
    atoms=[];w=[]; v=l.copy(); prev=1.0
    ps=np.append(p[order],0.0)
    # atom k: first k coords (in order) at u, prob = ps[k-1]-ps[k] (with ps[-1]=1)
    pk=np.concatenate([[1.0],p[order]])
    for k in range(len(a)+1):
        if k>0: v[order[k-1]]=u[order[k-1]]
        prob=pk[k]-(pk[k+1] if k<len(a) else 0.0)
        atoms.append(a@v+b); w.append(prob)
    return np.array(atoms),np.array(w)
def cx_min(sig,atoms,w,M):
    L,U=atoms.min(),atoms.max(); m=w@atoms
    t=np.unique(np.concatenate([np.linspace(L,U,M),atoms]))
    Umu=lambda tau: w@np.maximum(atoms-tau,0)
    A_ub=np.array([np.maximum(t-tau,0) for tau in t]); b_ub=np.array([Umu(tau) for tau in t])
    res=linprog(sig(t),A_ub=A_ub,b_ub=b_ub+1e-12,A_eq=np.vstack([np.ones_like(t),t]),b_eq=[1,m],bounds=(0,None),method='highs')
    return res.fun
def uni_env(sig,L,U,m,M):
    t=np.linspace(L,U,M)
    res=linprog(sig(t),A_eq=np.vstack([np.ones_like(t),t]),b_eq=[1,m],bounds=(0,None),method='highs'); return res.fun
fns={'sigmoid':lambda z:1/(1+np.exp(-z)),'silu':lambda z:z/(1+np.exp(-z)),'sin':np.sin,'neg_sigmoid':lambda z:-1/(1+np.exp(-z))}
for name,sig in fns.items():
  for trial in range(3):
    n=3; a=rng.uniform(0.3,2,n); b=rng.uniform(-2,2); l=rng.uniform(-3,0,n); u=l+rng.uniform(0.5,3,n)
    xbar=l+(u-l)*rng.uniform(0,1,n)
    atoms,w=staircase(a,b,l,u,xbar)
    e_box=box_env(sig,a,b,l,u,xbar,25); e_co=cx_min(sig,atoms,w,400)
    e_uni=uni_env(sig,a@l+b,a@u+b,a@xbar+b,2001)
    print(f"{name:12s} box-grid={e_box:.5f} convex-order={e_co:.5f} univariate={e_uni:.5f} f={sig(a@xbar+b):.5f}")
