"""Independent finite checks of frozen Section 3; not a proof or full compiler."""
from fractions import Fraction as F
from itertools import product
from random import Random
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

results = {}
rng = Random(23092)

def matching(n):
    vs = list(range(n))
    rng.shuffle(vs)
    return {tuple(sorted(vs[i:i+2])) for i in range(0, n, 2)}

def alpha(n, edges):
    return max(sum(bits) for bits in product((0, 1), repeat=n)
               if all(not (bits[u] and bits[v]) for u, v in edges))

graphs = 0
for n in (4, 6, 8):
    for trial in range(15):
        while True:
            colors = [matching(n) for _ in range(3)]
            if len(set.union(*colors)) == 3*n//2:
                break
        # Mode 1 is clean-strict; mode 2 is dirty-lax.
        # This explicitly includes the merged lax output constraint.
        best = max(sum(k != 0 for k in modes)
                   for modes in product(range(3), repeat=n)
                   if all(not(modes[u] == modes[v] == 1)
                          for u,v in colors[0] | colors[1])
                   and all(not(modes[u] == modes[v] == 2)
                           for u,v in colors[2]))
        assert best == n//2 + alpha(n, set.union(*colors))
        graphs += 1
results['colored_graph_mode_identities'] = graphs

# Verify the nonintegral K4 construction with exact rational arithmetic.
for delta in (F(1,100), F(1,4), F(1,2)):
    a = [1-delta, F(0), F(0), 1-delta]
    d = [delta, F(1), F(0), delta]
    strict = [F(1), F(0), F(0), F(1)]
    lax = [F(0), F(1), F(0), F(0)]
    E1, E2, E3 = [(0,1),(2,3)], [(0,2),(1,3)], [(0,3),(1,2)]
    q = [delta, F(1), F(0), delta]
    assert all(a[v]+d[v] == strict[v]+lax[v] <= 1 for v in range(4))
    assert all(a[u]+a[v] <= 1 for u,v in E1)
    assert all(d[u]+d[v] <= 1 and lax[u]+lax[v] <= 1 for u,v in E3)
    assert all(strict[u]+strict[v] <= 1 and
               q[u]*strict[u]+q[v]*strict[v] <= delta*(strict[u]+strict[v])
               for u,v in E2)
    assert sum(strict)+sum(d) == 3+2*delta
results['K4_exact_rational_tolerances'] = 3

# Recompute the printed Matsui counterexample, and the normalized generator
# bounds used to realize the large coefficients with finite physical data.
n,p = 5,2
X = sum(F(p**i,2) for i in range(1,n+1))
Y = sum(F(p**(2*i),2) for i in range(1,n+1))
assert Y-X*X == -279
assert F(p*p,8)-p*n*n == F(-99,2)
results['Matsui_counterexample'] = {'difference':str(Y-X*X), 'printed_bound':'-99/2'}
for n in (5,6,7,8):
    p = n**(n**4)
    P4 = p**(4*n)
    s = n+n*n
    u0 = 2*P4-p
    D0 = 1 << ((u0//2).bit_length()-1)
    U = [u0] + [u0+2*s*p**(2*n+i) for i in range(1,n+1)]
    U += [u0+s*p**(i+j) for i in range(1,n+1) for j in range(1,n+1)]
    V = [u0] + [u0-2*s*p**(2*n+i) for i in range(1,n+1)]
    V += [u0+s*p**(i+j) for i in range(1,n+1) for j in range(1,n+1)]
    assert all(2*D0 <= u < 20*D0 for u in U)
    assert all(D0*v < 4*p**(8*n) for v in V)
results['normalized_generator_families'] = 4

count = 0
for L in range(1,9):
    for c in range(2**L):
        for x in (F(0),F(2,3),F(2)):
            t = F(0)
            for k in range(L):
                t = (t + ((c >> k)&1)*x)/2
                assert 0 <= t <= 2
            assert t == F(c,2**L)*x
            count += 1
results['exact_binary_multiplier_checks'] = count

# Physically assemble closed full and half cycles from demand, supply,
# and upper-quality rows, without assuming any copy identities.
lp_count = 0
for half in (False, True):
    for size in (1,2,3):
        N=6*size
        eq=[]; rhs=[]; ub=[]; bound=[]
        for g in range(size):
            beta=3 if half else (1,3,33)[g]
            middle=1 if half else beta/2
            demand=3 if half else 4
            for offset in (0,3):
                row=np.zeros(N); row[6*g+offset:6*g+offset+3]=1
                eq.append(row); rhs.append(demand)
                row=np.zeros(N); row[6*g+offset+1]=beta; row[6*g+offset+2]=middle
                ub.append(row)
            row=np.zeros(N); row[6*g+2]=row[6*g+5]=1
            eq.append(row); rhs.append(demand)
            row=np.zeros(N); row[6*g+3]=1; row[6*((g+1)%size)]=1
            eq.append(row); rhs.append(2)
            bound.extend([(0,2),(0,1 if half else 2),(0,demand)]*2)
        quality_rhs=[(3 if half else (1,3,33)[g]/2*4)
                     for g in range(size) for _ in range(2)]
        relations=[]
        for g in range(size):
            for offset in (0,3):
                row=np.zeros(N); row[6*g+offset+1]=2 if half else 1
                row[6*g+offset]=-1; relations.append(row)
            row=np.zeros(N); row[6*g]=1; row[0]-=1; relations.append(row)
        for row in relations:
            for sign in (-1,1):
                res=linprog(sign*row,A_ub=ub,b_ub=quality_rhs,A_eq=eq,b_eq=rhs,
                            bounds=bound,method='highs')
                assert res.success and abs(res.fun)<1e-8
                lp_count += 1
        for value in (0,.5,2):
            fixed=np.zeros(N); fixed[0]=1
            res=linprog(np.zeros(N),A_ub=ub,b_ub=quality_rhs,
                        A_eq=eq+[fixed],b_eq=rhs+[value],bounds=bound,method='highs')
            assert res.success
            lp_count += 1
results['physical_closed_cycle_LPs'] = lp_count

dest=Path(__file__).with_name('results.json')
dest.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
