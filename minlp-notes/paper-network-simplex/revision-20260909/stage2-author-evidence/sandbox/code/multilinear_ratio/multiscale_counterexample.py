"""Symmetry-reduced hull-gap LP for multiscale positive multilinear examples.

m=2^L leaves each have marginal 1-1/m. Anchor j=1,...,L has
marginal u_j=2^-j. Its monomials are every k_j=m*u_j subset of
leaves multiplied by the anchor, with coefficient 1/(u_j*C(m,k_j)).
The total term-by-term gap is exactly L. The LP uses leaf failure
count r and z[j,r]=P(anchor_j=1, number of leaf failures=r).
"""
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from scipy.special import gammaln


def solve(levels):
    m=2**levels; nr=m+1
    u=2.**-np.arange(1,levels+1); k=(m*u).astype(int)
    r=np.arange(nr)
    g=np.ones((levels,nr))
    for j,kj in enumerate(k):
        valid=r<=m-kj
        rr=r[valid]
        logratio=gammaln(m-rr+1)-gammaln(m-rr-kj+1)-gammaln(m+1)+gammaln(m-kj+1)
        g[j,valid]=-np.expm1(logratio)
        g[j,0]=0
    nvar=nr*(levels+1)
    objective=np.zeros(nvar);objective[nr:]=(-g/u[:,None]).ravel()
    rr=np.arange(levels*nr)
    ub=coo_matrix((np.r_[np.ones(len(rr)),-np.ones(len(rr))],(np.r_[rr,rr],np.r_[nr+rr,np.tile(r,levels)])),shape=(levels*nr,nvar)).tocsr()
    erows=np.r_[np.zeros(nr,dtype=int),np.ones(nr,dtype=int),np.repeat(np.arange(2,levels+2),nr)]
    ecols=np.r_[r,r,nr+rr]
    edata=np.r_[np.ones(nr),r,np.ones(len(rr))]
    eq=coo_matrix((edata,(erows,ecols)),shape=(levels+2,nvar)).tocsr()
    res=linprog(objective,A_ub=ub,b_ub=np.zeros(levels*nr),A_eq=eq,b_eq=np.r_[1,1,u],bounds=(0,None),method='highs')
    if not res.success:raise RuntimeError(res.message)
    support=np.flatnonzero(res.x[:nr]>1e-8)
    return -res.fun,[(int(i),float(res.x[i])) for i in support]

if __name__=='__main__':
    for levels in range(2,14):
        gap,support=solve(levels)
        print('L',levels,'m',2**levels,'tbtgap',levels,'chgap',gap,'ratio',levels/gap,'failure distribution',support,flush=True)
