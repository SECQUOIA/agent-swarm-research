"""Exact finite exchangeable coupling LP for cubic polynomials with marginal groups.

Each group has m interchangeable coordinates. Symmetrizing a coupling preserves
all marginal and term constraints. Vertex states are just the success counts
in each group, and each degree-two/three monomial orbit has hypergeometric
conditional expectation. This reduces 2^(groups*m) states to (m+1)^groups.
"""
import itertools
import math
import numpy as np
from scipy.optimize import linprog


class SymmetricCubic:
    def __init__(self,m,groups=3):
        self.m=m;self.groups=groups
        self.states=np.array(list(itertools.product(range(m+1),repeat=groups)),float)
        self.types=[k for k in itertools.product(range(4),repeat=groups) if 2<=sum(k)<=3 and max(k)<=m]
        self.products=[]
        for typ in self.types:
            p=np.ones(len(self.states))
            for g,k in enumerate(typ):
                for ell in range(k):p*=np.maximum(self.states[:,g]-ell,0)/(m-ell)
            self.products.append(p)
        self.products=np.array(self.products)
        self.eq=np.column_stack([np.vstack([self.states.T/m,np.ones(len(self.states))]),np.zeros(groups+1)])

    def solve(self,x,details=False):
        x=np.array(x)
        upper=np.array([min(x[[j for j,k in enumerate(t) if k]]) for t in self.types])
        lower=np.array([max(0,np.dot(x,t)-sum(t)+1) for t in self.types])
        gaps=upper-lower
        obj=np.r_[np.zeros(len(self.states)),-1]
        res=linprog(obj,A_ub=np.column_stack([self.products,gaps]),b_ub=upper,A_eq=self.eq,b_eq=np.r_[x,1],bounds=[(0,None)]*len(self.states)+[(0,1)],method='highs')
        if not res.success:raise RuntimeError(res.message)
        if details:
            return 1/res.x[-1],[(typ,float(a)) for typ,a in zip(self.types,-res.ineqlin.marginals) if a>1e-8]
        return 1/res.x[-1]


if __name__=='__main__':
    for m in [4,8,16,32,64]:
        f=SymmetricCubic(m)
        best=(0,None)
        for u in np.linspace(.1,.3,21):
            ratio=f.solve([u,.5,1-u])
            if ratio>best[0]:best=(ratio,u)
        ratio,coefs=f.solve([best[1],.5,1-best[1]],True)
        print('m',m,'n',3*m,'ratio',ratio,'u',best[1],'orbit coefficient totals',coefs,flush=True)
