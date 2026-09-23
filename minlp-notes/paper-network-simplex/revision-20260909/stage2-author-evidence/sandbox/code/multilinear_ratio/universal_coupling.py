"""Exact coefficient optimization at fixed marginals via a coupling LP.

The LP maximizes gamma over joint Bernoulli distributions with marginals x,
subject to min(x_e) - E[AND_e] >= gamma * tbtgap_e for every subset e.
Its value is the reciprocal of the worst positive-coefficient gap ratio at x.
The constraints include all monomials of degree >= 2. Zero-gap terms are omitted.
"""
import itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack, vstack


class UniversalCoupling:
    def __init__(self, n, max_degree=None):
        self.n = n
        self.terms = [t for k in range(2,min(n, max_degree or n)+1) for t in itertools.combinations(range(n),k)]
        codes = np.arange(2**n)
        self.vertices = ((codes[:,None] >> np.arange(n)) & 1).astype(float)
        self.products = np.array([self.vertices[:,t].prod(axis=1) for t in self.terms])
        self.eq = csr_matrix(np.column_stack([np.vstack([self.vertices.T,np.ones(2**n)]), np.zeros(n+1)]))

    def solve(self, x, details=False):
        x = np.asarray(x)
        upper = np.array([min(x[list(t)]) for t in self.terms])
        lower = np.array([max(0,sum(x[list(t)])-len(t)+1) for t in self.terms])
        gaps = upper-lower
        selected = gaps>1e-10
        mat = hstack([csr_matrix(self.products[selected]),csr_matrix(gaps[selected,None])], format='csr')
        obj = np.zeros(2**self.n+1); obj[-1] = -1
        res=linprog(obj,A_ub=mat,b_ub=upper[selected],A_eq=self.eq,b_eq=np.append(x,1),bounds=[(0,None)]*(2**self.n)+[(0,1)],method='highs')
        if not res.success: raise RuntimeError(res.message)
        if details:
            coefs=np.zeros(len(self.terms)); coefs[selected]=-res.ineqlin.marginals
            return 1/res.x[-1], [(float(a),t) for a,t in zip(coefs,self.terms) if a>1e-8],res
        return 1/res.x[-1]

if __name__=='__main__':
    rng=np.random.default_rng(610)
    for n in range(3,10):
        solver=UniversalCoupling(n)
        best=(0,None)
        for i in range(200):
            x=rng.choice([.05,.1,.2,.25,1/3,.5,2/3,.75,.8,.9,.95],n) if i<100 else rng.random(n)
            ratio=solver.solve(x)
            if ratio>best[0]+1e-8: best=(ratio,x);print(n,i,ratio,x,flush=True)
        ratio,terms,res=solver.solve(best[1],True)
        print('BEST',n,ratio,best[1].tolist(),terms,flush=True)
