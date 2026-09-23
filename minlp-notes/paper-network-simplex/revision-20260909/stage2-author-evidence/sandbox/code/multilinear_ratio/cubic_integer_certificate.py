"""Find and exactly certify a small integer-coefficient cubic example.

Counts A,B,C refer to three interchangeable groups, each of size m, with
marginals 1/4,1/2,3/4. Polynomial:
 a*C(C,3)+b*B*C(C,2)+c*C(B,2)+d*A*C+e*A*B+f*C(A,2).
Each displayed coefficient is the coefficient of each individual monomial.
"""
import itertools
import math
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
import sympy as sp


def data(m):
    states=list(itertools.product(range(m+1),repeat=3))
    basis=np.array([[math.comb(C,3),B*math.comb(C,2),math.comb(B,2),A*C,A*B,math.comb(A,2)] for A,B,C in states],dtype=np.int64)
    eq=np.vstack([np.array(states).T,np.ones(len(states))])
    x=np.array([m/4,m/2,3*m/4,1])
    # Orbit upper gaps / lower gaps at group marginals (.25,.5,.75).
    num=[math.comb(m,3),m*math.comb(m,2),math.comb(m,2),m*m,m*m,math.comb(m,2)]
    upper=[F(3,4),F(1,2),F(1,2),F(1,4),F(1,4),F(1,4)]
    lower=[F(1,4),F(0),F(0),F(0),F(0),F(0)]
    return states,basis,eq,x,np.array([float(n*v) for n,v in zip(num,upper)]),np.array([float(n*v) for n,v in zip(num,lower)])


def solve(m,coefs,certificate=False):
    states,basis,eq,x,upper,lower=data(m)
    phi=basis@coefs
    res=linprog(phi,A_eq=eq,b_eq=x,bounds=(0,None),method='highs')
    if not res.success:raise RuntimeError(res.message)
    cav=F(float(upper@coefs));tbtl=F(float(lower@coefs))
    ratio=float(cav-tbtl)/(float(cav)-res.fun)
    if not certificate:return ratio
    support=np.flatnonzero(res.x>1e-9)
    Aq=sp.Matrix([[*states[i],1] for i in support]).T
    rhs=sp.Matrix([sp.Rational(m,4),sp.Rational(m,2),sp.Rational(3*m,4),1])
    lam,_=Aq.gauss_jordan_solve(rhs)
    assert all(v>=0 for v in lam)
    primal=sum(lam[j]*int(phi[i]) for j,i in enumerate(support))
    slacks=phi-eq.T@res.eqlin.marginals
    active=np.flatnonzero(slacks<1e-6)
    dual_matrix=sp.Matrix([[*states[i],1] for i in active])
    exact_dual_solution,parameters=dual_matrix.gauss_jordan_solve(sp.Matrix([int(phi[i]) for i in active]))
    if parameters.rows:
        exact_dual_solution=exact_dual_solution.subs({p:0 for p in parameters})
    dual=[F(v) for v in exact_dual_solution]
    for state,value in zip(states,phi):
        assert sum(v*p for v,p in zip([*state,1],dual))<=int(value),(state,value,dual)
    exact_dual=sum(v*p for v,p in zip([F(m,4),F(m,2),F(3*m,4),1],dual))
    assert F(primal)==exact_dual
    exact_ratio=(cav-tbtl)/(cav-exact_dual)
    return dict(m=m,coefs=list(map(int,coefs)),cav=cav,tbtl=tbtl,vex=exact_dual,hullgap=cav-exact_dual,ratio=exact_ratio,dual=dual,support=[(states[i],str(lam[j])) for j,i in enumerate(support)])


if __name__=='__main__':
    rng=np.random.default_rng(807)
    m=8
    best=(0,None)
    for i in range(1200):
        if i==0:coefs=np.array([1,2,12,10,7,7])
        else:coefs=np.maximum(1,np.array([1,2,12,10,7,7])+rng.integers(-3,4,6))
        ratio=solve(m,coefs)
        if ratio>best[0]:
            best=(ratio,coefs)
            print('new',ratio,coefs.tolist(),flush=True)
    print('EXACT',solve(m,best[1],True),flush=True)
