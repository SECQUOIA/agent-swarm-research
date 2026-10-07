"""usage: python3 sanity_zB.py RHO.  Independent sanity check of Theorem B2's logic: random X (det>0); check directly (rb.in_B_X and a
line test) that never all conditions hold at rho=160."""
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np, rb
rho=float(sys.argv[1]) if len(sys.argv)>1 else 160.0
rng=np.random.default_rng(5)
pts=[np.array(p) for p in [(0,0,1.0),(rho,-rho,1.0),(rho,-2*rho,1.0)]]
def line_ok(X):
    A0=rb.sym(X@rb.M(np.array([rho,rho,0.0]))); Z=rb.sym(X@rb.E)
    hs=np.concatenate([rho*rho+np.logspace(-6,12,4000)])
    return max(np.linalg.eigvalsh(A0+h*Z)[0] for h in hs[::10])>=-1e-9*np.abs(X).max()*(1+rho*rho)
n=0;allok=0;near=[]
# sample around the near-optimal region and broadly
for k in range(4000):
    if k%2==0:
        X=np.array([[1.18,-1.99],[0.0087,0.83]])*(1+0.05*rng.normal(size=(2,2)))
    else:
        X=rng.normal(size=(2,2))
    if np.linalg.det(X)<=0: continue
    n+=1
    c=[rb.in_B_X(X,p) for p in pts]
    if all(c):
        if line_ok(X): allok+=1; near.append(X)
print('samples',n,'all conditions hold',allok)
