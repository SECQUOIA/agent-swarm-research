"""Independent finite checks for frozen Section 3; these supplement proof review."""
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import sympy as sp

results = {}

def matchings(vertices):
    if not vertices:
        yield ()
        return
    u, *rest = vertices
    for v in rest:
        for m in matchings([w for w in rest if w != v]):
            yield ((u, v),) + m

def independence(n, edges):
    return max(mask.bit_count() for mask in range(1 << n)
               if all(not ((mask >> u) & (mask >> v) & 1) for u, v in edges))

graphs = 0
for n in (4, 6):
    mats = list(matchings(list(range(n))))
    for E1, E2, E3 in combinations(mats, 3):
        if len(set(E1 + E2 + E3)) != 3*n//2:
            continue
        alpha = independence(n, E1 + E2 + E3)
        H = list(E1 + E2)
        for u, v in E3:
            H += [(u, n+u), (n+u, n+v), (n+v, v)]
        assert independence(2*n, H) == n//2 + alpha
        best = 0
        for modes in product(range(3), repeat=n):  # inactive, clean, dirty
            if any(modes[u] == modes[v] == 1 for u, v in E1 + E2):
                continue
            if any(modes[u] == modes[v] == 2 for u, v in E3):
                continue
            best = max(best, sum(m > 0 for m in modes))
        assert best == n//2 + alpha
        graphs += 1
results['all_colored_matching_triples_n4_n6'] = graphs

# Full/half cycles, including heterogeneous full endpoint qualities.
# Variables for each gadget are A0,Aother,Amiddle,B0,Bother,Bmiddle.
lp_checks = 0
for kind, betas in [('full',[1]), ('full',[3,1,33]), ('half',[3,3,3])]:
    r = len(betas)
    eq, rhs, ub, urhs, bounds = [], [], [], [], []
    demand = 4 if kind == 'full' else 3
    for j,beta in enumerate(betas):
        mid = F(beta,2) if kind == 'full' else F(1)
        bounds += [(0,2),(0,2 if kind == 'full' else 1),(0,demand)]*2
        for off in (0,3):
            row = np.zeros(6*r); row[6*j+off:6*j+off+3]=1
            eq.append(row); rhs.append(demand)
            row = np.zeros(6*r)
            row[6*j+off] = -float(mid)
            row[6*j+off+1] = float(beta-mid)
            ub.append(row); urhs.append(0)
        row = np.zeros(6*r); row[6*j+2]=row[6*j+5]=1
        eq.append(row); rhs.append(demand)
        row = np.zeros(6*r); row[6*j+3]=row[6*((j+1)%r)]=1
        eq.append(row); rhs.append(2)
    for j in range(r):
        for off in (0,3):
            row = np.zeros(6*r)
            row[6*j+off]=1
            row[6*j+off+1]=-1 if kind == 'full' else -2
            for sign in (-1,1):
                sol=linprog(sign*row,A_eq=eq,b_eq=rhs,A_ub=ub,b_ub=urhs,
                            bounds=bounds,method='highs')
                assert sol.success and abs(sol.fun)<1e-8
                lp_checks+=1
results['cycle_identity_LP_extrema'] = lp_checks

# Dyadic recurrence and gate/source complements, exact rational arithmetic.
binary_cases = 0
for L in range(1,9):
    for c in range(1<<L):
        for x in (F(0),F(1,7),F(1),F(2)):
            t=F(0)
            for k in range(L):
                t=(t+((c>>k)&1)*x)/2
                assert 0<=t<=2
            assert t==F(c,1<<L)*x
            binary_cases+=1
results['exact_binary_multiplier_cases']=binary_cases
for u,v in product([F(i,4) for i in range(9)],repeat=2):
    avg=(u+v)/2
    assert avg+(1-u/2)+(1-v/2)==2
    if u+v<=2:
        assert u+v+(2-u-v)==2
    if u<=v:
        slack=v-u
        ports=[u,slack,2-v]
        assert sum(ports)==2 and sum(2-f for f in ports)==4
        assert sum(2-(2-f) for f in ports)==2
results['gate_and_grouped_source_checks']='passed'

# Symbolic Matsui algebra and independently recomputed printed counterexample.
X,Y,p,P4=sp.symbols('X Y p P4')
U=2*P4-p+Y+2*sp.sqrt(P4)*X
V=2*P4-p+Y-2*sp.sqrt(P4)*X
assert sp.expand(U*V-4*P4**2-((Y-p)**2+4*P4*(Y-X**2-p)))==0
n=5; smallp=2
Xv=sum(F(smallp**i,2) for i in range(1,n+1))
Yv=sum(F(smallp**(2*i),2) for i in range(1,n+1))
assert Yv-Xv**2==-279
assert F(smallp**2,8)-smallp*n*n==F(-99,2)
results['matsui_identity_and_counterexample']='passed: -279 < -99/2'

# Primary feasibility and radial correction over rational sample intakes.
radial_cases=0
for a in ([F(1),F(33)],[F(3,2),F(19)]):
    for x in product([F(i,8) for i in range(17)],repeat=2):
        T=sum(x)
        if not 0<T<=2:
            continue
        S=sum(ai*xi for ai,xi in zip(a,x))
        residual=S*(T-1)-T
        if residual>0:
            theta=(1+T/S)/T
            xx=[theta*xi for xi in x]
            TT=sum(xx); SS=sum(ai*xi for ai,xi in zip(a,xx))
            assert SS*(TT-1)-TT==0
            assert T-TT==residual/S
        else:
            y2=min(T,1); y1=T-y2
            anchor=(S/T-1)*y1
            assert 0<=anchor<=1 and y1+anchor<=1
            assert S/T*y1<=y1+anchor
        radial_cases+=1
results['exact_radial_cases']=radial_cases
Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
