"""Independent finite checks; exact cut arithmetic, numerical envelope LPs."""
from itertools import product, combinations
from fractions import Fraction
import json
import numpy as np
from scipy.optimize import linprog

exact_cases = 0
for n in range(5):
    edges = list(combinations(range(n), 2))
    signs = list(product((-1, 1), repeat=n))
    for a in product((-1, 0, 1), repeat=len(edges)):
        q = [sum(c*s[i]*s[j] for (i,j),c in zip(edges,a)) for s in signs]
        r = Fraction(max(q)-min(q), 2)
        polarized = max((sum(c*s[i]*s[j] for (i,j),c in zip(edges,a)
                            if (i in side) != (j in side))
                         for mask in product((0,1),repeat=n)
                         for side in [{i for i in range(n) if mask[i]}]
                         for s in signs), default=0)
        assert r == polarized
        assert (r == 0) == (not any(a))
        if any(a):
            assert Fraction(sum(map(abs,a)),1) / r >= 1
        exact_cases += 1

rng = np.random.default_rng(3001)
lp_cases = half_grid_cases = zero_gap_cases = 0
for n in range(5):
    edges = list(combinations(range(n), 2))
    verts = np.array(list(product((0,1),repeat=n)),dtype=float).reshape(2**n,n)
    eq = np.vstack([np.ones(2**n), verts.T])
    vectors = [np.zeros(len(edges),dtype=int), np.ones(len(edges),dtype=int)]
    vectors += [rng.integers(-2,3,len(edges)) for _ in range(8)]
    for a in vectors:
        values = np.array([sum(c*v[i]*v[j] for (i,j),c in zip(edges,a)) for v in verts])
        max_induced_ratio = 0
        for mask in product((0,1),repeat=n):
            w = [i for i in range(n) if mask[i]]
            ae = [(i,j,c) for (i,j),c in zip(edges,a) if i in w and j in w]
            q = [sum(c*s[i]*s[j] for i,j,c in ae) for s in product((-1,1),repeat=n)]
            r = (max(q)-min(q))/2
            if r:
                max_induced_ratio = max(max_induced_ratio,sum(abs(c) for i,j,c in ae)/r)
        points = list(product((0,.5,1),repeat=n))
        points += [tuple(rng.integers(0,5,n)/4) for _ in range(10)]
        for p in points:
            lo = linprog(values,A_eq=eq,b_eq=[1,*p],bounds=(0,None),method='highs')
            hi = linprog(-values,A_eq=eq,b_eq=[1,*p],bounds=(0,None),method='highs')
            assert lo.success and hi.success
            h = -hi.fun-lo.fun
            t = sum(abs(c)*min(p[i],p[j],1-p[i],1-p[j]) for (i,j),c in zip(edges,a))
            assert t <= max_induced_ratio*h+1e-8
            if abs(h)<1e-9:
                assert abs(t)<1e-9
                zero_gap_cases += 1
            if all(z in (0,.5,1) for z in p):
                ae = [(i,j,c) for (i,j),c in zip(edges,a) if p[i]==p[j]==.5]
                q = [sum(c*s[i]*s[j] for i,j,c in ae) for s in product((-1,1),repeat=n)]
                assert abs(h-(max(q)-min(q))/4)<1e-8
                half_grid_cases += 1
            lp_cases += 1
print(json.dumps(dict(exact_cut_cases=exact_cases,numerical_lp_points=lp_cases,
    half_grid_points=half_grid_cases,zero_gap_points=zero_gap_cases,
    max_dimension=4,numerical_tolerance=1e-8),indent=2))
