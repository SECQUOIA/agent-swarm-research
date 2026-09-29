"""Midpoint-conflict clique for CVP instances: lattice points a,b conflict iff
the midpoint (Ba+Bb)/2 is strictly closer to t than sqrt(OPT) (minus eps).
Two lattice models: 'gauss' (Gaussian basis, det 1; MIMO-like) and 'gm'
(Goldstein-Mayer random lattice of prime determinant, scaled to det 1)."""
import os, sys, json, math
os.environ["OMP_NUM_THREADS"]="1"
import numpy as np
from multiprocessing import Pool
from cvp_count import lll, enum_ball
from sympy import nextprime

def make_basis(n, kind, rng):
    if kind=="gauss":
        B=rng.standard_normal((n,n))
    else:
        P=int(nextprime(int(2**(2*n)) + int(rng.integers(0,1000))))  # det ~ 4^n
        B=np.eye(n)
        B[0,0]=P
        B[0,1:]=rng.integers(0,P,n-1)
        B=B.astype(float)
    B/=abs(np.linalg.det(B))**(1.0/n)
    return lll(B)

def sample(args):
    n,kind,seed=args
    rng=np.random.default_rng(seed)
    B=make_basis(n,kind,rng)
    Q,R=np.linalg.qr(B)
    r2=min(np.sum(B*B,0))
    pts=enum_ball(R,np.zeros(n),r2*(1+1e-9),exclude_zero=True)
    lam1sq=min(p[0] for p in pts)
    t=B@rng.random(n); tt=Q.T@t
    z=np.zeros(n)
    for i in range(n-1,-1,-1): z[i]=round((tt[i]-R[i,i+1:]@z[i+1:])/R[i,i])
    ub=float(np.sum((R@z-tt)**2))
    OPT=min(p[0] for p in enum_ball(R,tt,ub*(1+1e-12)))
    pts=enum_ball(R,tt,2.0*OPT)
    V=np.array([R@p[1]-tt for p in pts])   # coordinates relative to target (rotated)
    f=np.array([p[0] for p in pts])
    order=np.argsort(f)[:2500]; V=V[order]; f=f[order]
    sq=(V*V).sum(1); mid=0.25*(sq[:,None]+sq[None,:]+2*V@V.T)
    adj=mid<OPT*(1-1e-9); np.fill_diagonal(adj,False)
    best=0
    for s in range(min(len(f),60)):
        cl=[s]; cand=adj[s].copy()
        for j in range(len(f)):
            if cand[j]: cl.append(j); cand&=adj[j]
        best=max(best,len(cl))
    shell=int((f<OPT+lam1sq/4).sum())
    return dict(n=n,kind=kind,seed=seed,clique=best,shell=shell,npts=len(f),OPT=OPT,lam1sq=lam1sq)

if __name__=="__main__":
    ns=[int(v) for v in sys.argv[1].split(",")]; nseeds=int(sys.argv[2]); out=sys.argv[3]
    jobs=[(n,k,s) for n in ns for k in ("gauss","gm") for s in range(nseeds)]
    with Pool(int(sys.argv[4]) if len(sys.argv)>4 else 8) as pool, open(out,"w") as fo:
        for r in pool.imap_unordered(sample,jobs):
            fo.write(json.dumps(r)+"\n"); fo.flush()
