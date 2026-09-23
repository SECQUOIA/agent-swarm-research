"""Independent reviewer checks; finite tests supplement the handwritten proof audit."""
from fractions import Fraction as F
from itertools import combinations, product
import json
import numpy as np
from scipy.optimize import linprog
import sympy as sp

results = {}
# Check the source's exact product algebra and the printed counterexample.
X,Y,p,P4=sp.symbols('X Y p P4')
U=2*P4-p+Y+2*sp.sqrt(P4)*X
V=2*P4-p+Y-2*sp.sqrt(P4)*X
assert sp.expand(U*V-4*P4**2-((Y-p)**2+4*P4*(Y-X**2-p))) == 0
xx=sum(F(2**i,2) for i in range(1,6))
yy=sum(F(2**(2*i),2) for i in range(1,6))
assert yy-xx**2 == -279
assert F(2**2,1)*F(1,4)/2-2*25 == F(-99,2)
results['product_identity_and_Matsui_counterexample']='pass'

# Exhaust all simple three-edge-coloured cubic graphs from perfect matchings
# at n=4,6; compare true independent sets with direct physical pure-mode choices.
def matchings(vertices):
    if not vertices:
        yield ()
    else:
        u=vertices[0]
        for v in vertices[1:]:
            for rest in matchings(tuple(w for w in vertices if w not in (u,v))):
                yield ((u,v),)+rest

def alpha(n,edges):
    return max(sum(mask) for mask in product((0,1),repeat=n)
               if all(not(mask[u] and mask[v]) for u,v in edges))
count=0
for n in (4,6):
    mats=list(matchings(tuple(range(n))))
    for colors in combinations(mats,3):
        if len(set(sum(colors,()))) != 3*n//2: continue
        E1,E2,E3=colors
        # state=0 inactive;1 clean-strict;2 dirty-lax.
        best=0
        for states in product(range(3),repeat=n):
            if any(states[u]==states[v]==1 for u,v in E1+E2): continue
            if any(states[u]==states[v]==2 for u,v in E3): continue
            best=max(best,sum(s>0 for s in states))
        assert best == n//2+alpha(n,E1+E2+E3)
        count+=1
results['exhaustive_coloured_cubic_graphs']=count

# Verify closed-cycle identities by LP from physical output mass constraints,
# upper quality inequalities, exact middle supplies, and zero-link supplies.
# Positive endpoint ports are otherwise independent, bounded free flows.
def cycle(betas,half=False):
    r=len(betas); N=6*r; eq=[]; rhs=[]; ub=[]; ur=[]; bounds=[]
    def row(d):
        a=np.zeros(N)
        for i,v in d.items(): a[i]=v
        return a
    for j,beta in enumerate(betas):
        d=3 if half else 4; gamma=beta/3 if half else beta/2
        for side in (0,1):
            u,v,m=6*j+3*side,6*j+3*side+1,6*j+3*side+2
            eq.append(row({u:1,v:1,m:1}));rhs.append(d)
            ub.append(row({u:-gamma,v:beta-gamma}));ur.append(0)
            bounds.extend([(0,2),(0,1 if half else 2),(0,d)])
        eq.append(row({6*j+2:1,6*j+5:1}));rhs.append(d)
        eq.append(row({6*j+3:1,6*((j+1)%r):1}));rhs.append(2)
    def extrema(d):
        c=row(d)
        vals=[]
        for sign in (1,-1):
            sol=linprog(sign*c,A_ub=ub,b_ub=ur,A_eq=eq,b_eq=rhs,bounds=bounds,method='highs')
            assert sol.success,sol.message
            vals.append(float(c@sol.x))
        return vals
    for j in range(r):
        # Compare every first zero port with signal x=u_0, and every
        # positive port with its full or half representation.
        if j:
            assert max(map(abs,extrema({6*j:1,0:-1}))) < 1e-8
        assert max(map(abs,extrema({6*j+1:2 if half else 1,6*j:-1}))) < 1e-8
        assert max(map(abs,extrema({6*j+4:2 if half else 1,6*j+3:-1}))) < 1e-8
    assert extrema({0:1}) == [0.0,2.0]
for betas,half in [([3],False),([3,1,33],False),([3],True),([3,3,3],True)]:
    cycle(betas,half)
results['physical_cycle_LP_extrema']='pass (full, mixed positive endpoints, half; one and three gadgets)'

# Exact gate identities, binary multipliers, and complement splitting
# at boundaries and rational interior points.
grid=[F(i,4) for i in range(9)]
checks=0
for u,w in product(grid,repeat=2):
    v=(u+w)/2
    assert v+(1-u/2)+(1-w/2)==2
    for signal in (u,w,v): assert 0<=signal<=2
    for caps,flows,S in [((2,1,1),(v,1-u/2,1-w/2),2)]:
        residuals=tuple(F(c)-f for c,f in zip(caps,flows))
        assert all(0<=f<=c for c,f in zip(caps,flows))
        assert sum(residuals)==sum(caps)-S
        # Grouped mates reverse the supply and collector demand.
        assert sum(F(c)-g for c,g in zip(caps,residuals))==S
    if u+w<=2:
        flows=(u,w,2-u-w);caps=(2,2,2)
        assert sum(flows)==2 and sum(c-f for c,f in zip(caps,flows))==4
    checks+=1
for L in range(1,9):
    for c in range(2**L):
        for x in (F(0),F(1,3),F(2)):
            t=F(0)
            for k in range(L):
                t=(t+((c>>k)&1)*x)/2
                assert 0<=t<=2
            assert t==F(c,2**L)*x
results['gate_grid_checks']=checks
results['all_binary_multipliers_through_8_bits']='pass'

# Radial repair for numerous rational intake vectors, including zero and
# both sides of T=1. This is independent of any optimization solver.
repairs=0
for a in ((F(1),F(33)),(F(2),F(7))):
    for x in product(grid,repeat=2):
        T=sum(x)
        if T>2: continue
        S=sum(ai*xi for ai,xi in zip(a,x)); FF=S*(T-1)-T
        if FF>0:
            theta=(1+T/S)/T
            y=tuple(theta*xi for xi in x);TT=sum(y);SS=sum(ai*yi for ai,yi in zip(a,y))
            assert SS*(TT-1)-TT==0
            assert sum(xi-yi for xi,yi in zip(x,y))==FF/S
        elif T>1:
            anchor=(S/T-1)*(T-1)
            assert 0<=anchor<=1 and (T-1)+anchor<=1
        repairs+=1
results['exact_radial_checks']=repairs
print(json.dumps(results,indent=2))
