"""Independent dense-covariance diagnostics; no author/historical imports."""
import itertools
import json
from pathlib import Path
import numpy as np
import scipy.linalg as la
import sympy as sp

rng = np.random.default_rng(928361)
counts = dict(block=0, partial=0, far=0, metric=0)
worst = dict(block=0., partial=0., far=0., metric=0.)

def norm(A): return la.norm(A, 2)
def invsqrt(A):
    e, u = la.eigh(A)
    return (u / np.sqrt(e)) @ u.T
def local(R, dims, S, L):
    off=np.cumsum([0]+dims)
    ix=np.concatenate([np.arange(off[t],off[t+1]) for t in S])
    rr=R[np.ix_(ix,ix)]
    oo=np.cumsum([0]+[dims[t] for t in S])
    A=np.eye(len(ix))
    for a,t in enumerate(S):
        hh=np.concatenate([np.arange(oo[b],oo[b+1]) for b,s in enumerate(S[:a]) if t-s<=L]) if any(t-s<=L for s in S[:a]) else np.array([], dtype=int)
        ii=np.arange(oo[a],oo[a+1])
        if len(hh): A[np.ix_(ii,hh)]=-la.solve(rr[np.ix_(hh,hh)],rr[np.ix_(hh,ii)],assume_a='pos').T
    C=A@rr@A.T
    Ds=[C[oo[a]:oo[a+1],oo[a]:oo[a+1]] for a in range(len(S))]
    Z=la.block_diag(*[invsqrt(D) for D in Ds])
    return C, Z@C@Z, oo

def tails(x,L):
    return x**(L+1)/(1-x),sum(x**(h+2*d) for h in range(1,L+1) for d in range(L+1-h,L+1))

for model in range(18):
    n=6; d=3; rho=.25+.65*rng.random(); pbar=1.3
    # Variable-rank state covariance with transitions that rotate supported ranges.
    bases=[la.qr(rng.normal(size=(d,d)))[0] for _ in range(n)]
    P=[U@np.diag([1., .7, 0.])@U.T for U in bases]
    gamma=rho
    transitions=[None]+[rho*bases[t]@np.diag([.8,.6,0.])@bases[t-1].T for t in range(1,n)]
    K=np.zeros((n*d,n*d))
    for t in range(n):
        K[t*d:(t+1)*d,t*d:(t+1)*d]=P[t]
        for s in range(t):
            v=transitions[t]@K[(t-1)*d:t*d,s*d:(s+1)*d]
            K[t*d:(t+1)*d,s*d:(s+1)*d]=v
            K[s*d:(s+1)*d,t*d:(t+1)*d]=v.T
    for t in range(1,n):
        assert la.eigvalsh(P[t]-transitions[t]@P[t-1]@transitions[t].T-(1-gamma**2)*P[t]).min()>-1e-12
    # Full-block theorem: independent identity observation noise.
    R=K+np.eye(n*d)
    for S in ([0,1,2,3,4,5],[0,2,3,5],[0,1,4,5]):
        for L in range(4):
            C, CC, off=local(R,[d]*n,S,L)
            T,N=tails(rho,L)
            bound=2*pbar*(T+pbar/(1+pbar)*N)
            error=norm(CC-np.eye(len(CC)))
            assert error <= bound+1e-10
            worst['block']=max(worst['block'],error/bound); counts['block']+=1
            for a,t in enumerate(S):
                for b,s0 in enumerate(S[:a]):
                    if t-s0>L:
                        value=norm(C[off[a]:off[a+1],off[b]:off[b+1]])
                        assert value<=pbar*rho**(t-s0)+1e-10
                        worst['far']=max(worst['far'],value/(pbar*rho**(t-s0)));counts['far']+=1
    # Partial packets in independent, anisotropic observation coordinates.
    dims=[1,2,3,1,2,3]; s=.8
    H=[]; V=[]
    for t,dt in enumerate(dims):
        v=np.diag(np.geomspace(.1,7,dt)); h=rng.normal(size=(dt,d))
        root=bases[t]@np.diag([1.,np.sqrt(.7),0.])@bases[t].T
        lam=norm(invsqrt(v)@h@root)**2
        h*=np.sqrt(s/max(lam,1e-15))*.95
        H.append(h); V.append(v)
    HH=la.block_diag(*H); VV=la.block_diag(*V)
    R=HH@K@HH.T+VV
    coord=la.block_diag(*[np.diag(np.geomspace(.2,3,dt)) for dt in dims])
    for S in ([0,1,2,3,4,5],[0,2,3,5],[0,1,4,5]):
        for L in range(4):
            _, CC, _=local(R,dims,S,L)
            _, CCC, _=local(coord@R@coord.T,dims,S,L)
            k=s/(1+s); T,N=tails(gamma,L)
            bound=2*k*(T+np.sqrt(k*s)*N)
            error=norm(CC-np.eye(len(CC)))
            assert error<=bound+1e-10
            worst['partial']=max(worst['partial'],error/bound);counts['partial']+=1
            change=abs(error-norm(CCC-np.eye(len(CCC))))
            assert change<1e-10
            worst['metric']=max(worst['metric'],change);counts['metric']+=1

# Independent exact source witness and correct marginal ratios.
q=sp.Rational
R=sp.Matrix([[1,0,q(3,5)],[0,1,q(3,5)],[q(3,5),q(3,5),1]])
det_products=[]
for pivots in [[],[0],[1],[0,1]]:
    A=sp.eye(3); D=sp.zeros(3)
    for j in range(3):
        h=[i for i in pivots if i<j]
        if h:
            b=R.extract([j],h)*R.extract(h,h).inv()
            for ii,i in enumerate(h): A[j,i]=-b[ii]
        D[j,j]=(A[j,:]*R*A[j,:].T)[0]
    Q=A.T*D.inv()*A
    assert sp.trace(Q*R)==3
    det_products.append(sp.factor(1/(Q*R).det()))
assert det_products==[q(25,7),q(16,7),q(16,7),1]
assert sp.factor(det_products[0]*det_products[3]/(det_products[1]*det_products[2]))==q(175,256)

out={'counts':counts,'largest_bound_ratios_or_metric_difference':worst,'exact_pivot_exp2KL':[str(x) for x in det_products],'status':'PASS; floating diagnostics are not proof certificates'}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
