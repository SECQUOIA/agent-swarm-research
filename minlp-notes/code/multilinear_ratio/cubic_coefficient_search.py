"""Search all nonnegative cubic/bilinear coefficients at selected marginals.

Each fixed-marginal LP is the universal coupling minimax formulation, restricted
to degrees two and three. Floating-point searches do not prove a global bound.
"""
import numpy as np
from universal_coupling import UniversalCoupling


def main():
    rng=np.random.default_rng(4607)
    for n, samples in [(6,200),(8,200),(10,200),(12,100),(14,60)]:
        solver=UniversalCoupling(n,max_degree=3)
        best=(0,None)
        for i in range(samples):
            if i==0:x=np.full(n,.5)
            elif i<samples//3:
                a=10.**rng.uniform(-3,-.01)
                x=rng.choice([a,1-a,.5],n)
            elif i<2*samples//3:
                x=rng.choice([.01,.05,.1,.2,.25,1/3,.5,2/3,.75,.8,.9,.95,.99],n)
            else:
                x=rng.beta(.3,.3,n)
            ratio=solver.solve(x)
            if ratio>best[0]+1e-8:
                best=ratio,x
                print('new',n,i,ratio,x.tolist(),flush=True)
            if ratio>2+1e-7:
                val,terms,_=solver.solve(x,True)
                print('COUNTEREXAMPLE?',val,x.tolist(),terms,flush=True)
                return
        val,terms,_=solver.solve(best[1],True)
        print('BEST',n,val,best[1].tolist(),terms,flush=True)


if __name__=='__main__':main()
