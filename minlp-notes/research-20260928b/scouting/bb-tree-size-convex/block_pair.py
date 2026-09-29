"""Correlated-pair gadget: k orthogonal 2-dim blocks, features u_j=e1,
v_j=(cos th, sin th), response in block = s*(u+v)/|u+v|.  Budget k.
Midpoint lemma => any convex-piece B&B with the perspective relaxation needs
>= 2^k leaves; the per-block 2x2 hull relaxation is exact at the root."""
import numpy as np, itertools, sys
from sparse_bb import bnb, exact_value, Relaxation
def gadget(k, th=0.3, s=3.0):
    n=p=2*k
    X=np.zeros((n,p)); y=np.zeros(n)
    u=np.array([1.0,0.0]); v=np.array([np.cos(th),np.sin(th)]); d=(u+v)/np.linalg.norm(u+v)
    for j in range(k):
        X[2*j:2*j+2,2*j]=u; X[2*j:2*j+2,2*j+1]=v; y[2*j:2*j+2]=s*d
    return X,y
lam=1.0
for k in range(2,11):
    X,y=gadget(k)
    one_per_block=[tuple(2*j+b[j] for j in range(k)) for b in itertools.product([0,1],repeat=k)]
    OPT=exact_value(X,y,lam,one_per_block[0])
    # check OPT by brute force for small k
    if k<=6:
        bf=min(exact_value(X,y,lam,S) for S in itertools.combinations(range(2*k),k))
        assert abs(bf-OPT)<1e-9, (bf,OPT)
    R=Relaxation(X,y,lam,k)
    root,_,_=R.solve_ipm((),())
    # blockwise quantities
    g00=y[:2]@y[:2]; g10=exact_value(X[:2,:2],y[:2],lam,[0]); g11=exact_value(X[:2,:2],y[:2],lam,[0,1])
    Rb=Relaxation(X[:2,:2],y[:2],lam,1); ghalf,_,_=Rb.solve_ipm((),())
    r=bnb(X,y,lam,k,S_init=[one_per_block[0]],max_nodes=200000)
    print("k=%2d OPT=%.4f root=%.4f delta=%.4f  g00-g10=%.3f g10-g11=%.3f  B&B nodes=%d leaves=%d  2^k=%d"%(
        k,OPT,root,g10-ghalf,g00-g10,g10-g11,r['nodes'],(r['nodes']+1)//2,2**k))
