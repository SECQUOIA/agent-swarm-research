"""Independent finite checks; these do not establish universal theorems."""
from fractions import Fraction
from itertools import combinations, product
import json
import numpy as np
from scipy.optimize import linprog

n = 4
pairs = list(combinations(range(n), 2))
subsets = [set(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]
signs = list(product((-1, 1), repeat=n))
vertices = np.array(list(product((0, 1), repeat=n)), dtype=float)
B = np.vstack((np.ones(len(vertices)), vertices.T))

def induced(a, W):
    return [(i, j, c) for (i, j), c in zip(pairs, a) if i in W and j in W and c]

def cut_data(a, W):
    e = induced(a, W)
    values = [sum(c*s[i]*s[j] for i,j,c in e) for s in signs]
    return sum(abs(c) for _,_,c in e), Fraction(max(values)-min(values), 2)

# Exact rectangle density equality for every simple graph on four labeled vertices.
for indicators in product((0, 1), repeat=len(pairs)):
    edges = [e for e, present in zip(pairs, indicators) if present]
    rho = max(Fraction(sum(i in W and j in W for i,j in edges), len(W)) for W in subsets if W)
    beta = max(Fraction(sum((i in R and j in C)+(j in R and i in C) for i,j in edges), len(R)+len(C))
               for R in subsets for C in subsets if R or C)
    assert beta == rho

# Exact integer cut polarization and bilinear operator-to-cut comparison.
for a in product((-1, 0, 1), repeat=len(pairs)):
    _, R = cut_data(a, set(range(n)))
    polarized = max(sum(abs(sum(c*s[j] if i in S and j not in S else c*s[i] if j in S and i not in S else 0
                                       for (i,j),c in zip(pairs,a) if i == k or j == k)) for k in S)
                    for S in subsets for s in signs)
    assert R == polarized
    operator = max(sum(c*(u[i]*v[j]+u[j]*v[i]) for (i,j),c in zip(pairs,a)) for u in signs for v in signs)
    assert operator <= 4*R

# Numerical vertex-law LP checks at interior and boundary points.
rng = np.random.default_rng(606)
checked = 0
max_excess = 0.0
for _ in range(40):
    a = tuple(int(z) for z in rng.integers(-3, 4, len(pairs)))
    if not any(a):
        continue
    ratios = [L/R for W in subsets for L,R in [cut_data(a,W)] if R]
    cstar = float(max(ratios))
    objective = np.array([sum(c*x[i]*x[j] for (i,j),c in zip(pairs,a)) for x in vertices])
    points = [rng.random(n), rng.choice([0.0,0.5,1.0],size=n), np.array([0.0,1.0,0.2,0.7])]
    for x in points:
        lo = linprog(objective, A_eq=B, b_eq=np.r_[1.0,x], bounds=(0,None), method='highs')
        hi = linprog(-objective, A_eq=B, b_eq=np.r_[1.0,x], bounds=(0,None), method='highs')
        assert lo.success and hi.success
        H = -hi.fun-lo.fun
        T = sum(abs(c)*min(x[i],x[j],1-x[i],1-x[j]) for (i,j),c in zip(pairs,a))
        excess = T-cstar*H
        max_excess = max(max_excess,excess)
        assert excess <= 1e-9
        assert T+1e-9 >= H >= -1e-9
        if all(t in [0,0.5,1] for t in x):
            L,R = cut_data(a,set(i for i,t in enumerate(x) if t == 0.5))
            assert abs(H-float(R)/2) <= 1e-9
            assert abs(T-L/2) <= 1e-9
        checked += 1
print(json.dumps({'exact_rectangle_density_graphs':64, 'exact_polarization_weight_vectors':729,
                  'numerical_vertex_lp_points':checked, 'max_numerical_comparison_excess':max_excess,
                  'numerical_tolerance':1e-9}, indent=2))
