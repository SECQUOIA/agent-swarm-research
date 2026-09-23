"""Exploratory finite-grid LP over globally defined rounding couplings.

The LP is only a heuristic search for a universal cubic bound. It does not
certify unsampled marginal triples. Each candidate coupling preserves every
coordinate marginal and its monomial expectation is integrated exactly
between its breakpoints (up to floating arithmetic).
"""
import itertools
import numpy as np
from scipy.optimize import linprog


def threshold_product(xs, theta, scale):
    lows = [x for x in xs if x <= theta]
    highs = [1-x for x in xs if x > theta]
    cap = min(lows, default=1.)
    breaks = sorted(set([0., cap]+[min(scale*p,1.) for p in highs if min(scale*p,1.) < cap]))
    product = 0.
    for lo,hi in zip(breaks,breaks[1:]):
        t=(lo+hi)/2
        factors=[1-p/min(scale*p,1.) if t < min(scale*p,1.) else 1. for p in highs]
        product += (hi-lo)*np.prod(factors)
    return product


def orientation_deficiency(xs):
    vals=sorted((min(min(xs),1-x) for x in sorted(xs)[1:]),reverse=True)
    return sum(a/2**(j+1) for j,a in enumerate(vals))


def solve(grid, verbose=True, simple=False):
    edges=[xs for k in [2,3] for xs in itertools.combinations_with_replacement(grid,k)]
    couplings=[('orientation',0,0),('independent',0,0)]+[('threshold',theta,scale) for theta in np.linspace(0,1,21) for scale in [1,1.5,2,3,4,8]]
    if simple:
        couplings=[('orientation',0,0),('independent',0,0),('threshold',.5,2)]
    if simple == 'four':
        couplings += [('threshold',2/3,3)]
    table=[]
    for xs in edges:
        u=min(xs);gap=u-max(0,sum(xs)-len(xs)+1)
        row=[]
        for name,theta,scale in couplings:
            deficiency=orientation_deficiency(xs) if name=='orientation' else u-np.prod(xs) if name=='independent' else u-threshold_product(xs,theta,scale)
            row.append(deficiency/gap)
        table.append(row)
    table=np.array(table)
    res=linprog(np.r_[np.zeros(len(couplings)),-1],A_ub=np.column_stack([-table,np.ones(len(edges))]),b_ub=np.zeros(len(edges)),A_eq=np.array([np.r_[np.ones(len(couplings)),0]]),b_eq=[1],bounds=[(0,None)]*(len(couplings)+1),method='highs')
    assert res.success,res.message
    print('grid',len(grid),'alpha',res.x[-1],'ratio',1/res.x[-1],flush=True)
    for spec,w in zip(couplings,res.x[:-1]):
        if w>1e-8:print(spec,w,flush=True)
    active=np.where(table@res.x[:-1]<res.x[-1]+1e-7)[0]
    print('active edges',[edges[i] for i in active],flush=True)

if __name__=='__main__':
    solve(np.linspace(.025,.975,20))
    solve(np.linspace(.005,.995,31),simple=True)
