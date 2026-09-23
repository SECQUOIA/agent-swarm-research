"""Independent targeted checks of frozen pooling manuscript identities.

Symbolic checks use exact arithmetic. Signed-flow fixtures compare an exact
subset formula with SciPy LP, and are numerical corroboration, not proofs.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.optimize import linprog

results = {}

# Appendix A: telescoping identity with symbolic, nongeometric supplies.
n = 5
t = (s.Integer(0),) + s.symbols('t1:6')
cap = (s.Integer(0),) + s.symbols('s1:5') + (s.Integer(1),)
lhs = t[n] - t[n]**2 - sum((cap[j+1]-cap[j])*t[j] for j in range(1,n))
rhs = sum((t[j]-t[j-1])*(cap[j]-t[j-1]-t[j]) for j in range(1,n+1))
assert s.expand(lhs-rhs) == 0
results['general_supply_telescoping'] = 'exact symbolic identity passed'

# Section 3: positive-product gap identity and binary multiplier bit order.
X,Y,p,P4 = s.symbols('X Y p P4')
U,V = 2*P4-p+Y+2*s.sqrt(P4)*X, 2*P4-p+Y-2*s.sqrt(P4)*X
assert s.expand(U*V-4*P4**2-(Y-p)**2-4*P4*(Y-X**2-p)) == 0
for L in range(1,9):
    for c in range(2**L):
        value = F(0)
        for k in range(L):
            value = (value + ((c>>k)&1))/2
        assert value == F(c,2**L)
results['matsui_identity_and_binary_multiplier'] = 'exact identities passed'

# Section 5: two-vector outlet identity and residual cancellation.
q,b,B,v,z0,z1 = s.symbols('q b B v z0 z1')
quality = q*(b-z0-z1)+z1-b*B
outlet = -q*z0 - (q*b*(B-1)+q*(1-q)*(b-z0-z1))
assert s.expand(outlet-q*quality) == 0
q1,q2,c11,c12,c21,c22,b1,b2,beta = s.symbols('q1 q2 c11 c12 c21 c22 b1 b2 beta')
g1=(c11-q1)+beta*(c12-q2)
g2=(c21-q1)+beta*(c22-q2)
R=b*((b1-q1)+beta*(b2-q2))
aa=s.expand((c11-q1)*g2-(c21-q1)*g1)
ff=s.expand(g1*(b*(b1-q1)*g2-(c21-q1)*R))
assert s.Poly(aa,q1,q2).total_degree() <= 1
assert s.Poly(ff,q1,q2).total_degree() <= 2
results['signed_quality_and_two_vector_identities'] = 'exact symbolic identities/degrees passed'

# Section 5: signed node-box rank, greedy support, including a cycle,
# a disconnected isolated node, signed lower bounds, and asymmetric orientation.
fixtures = [
    ('path',4,[(0,1),(2,1),(2,3)],[-2,-1,0],[2,3,2],[-2,-3,-1,-2],[2,1,3,1],[3,-2,1,0]),
    ('cycle',4,[(0,1),(1,2),(3,2),(0,3)],[-1,-2,-1,0],[2,2,3,2],[-1,-2,-2,-1],[2,2,2,2],[2,-3,4,1]),
    ('isolated',5,[(0,1),(2,1),(2,3)],[-2,-1,0],[2,3,2],[-2,-3,-1,-2,0],[2,1,3,1,0],[3,-2,1,0,7]),
]
for name,n,edges,lo,hi,alpha,beta,cost in fixtures:
    subsets=range(1<<n)
    def members(mask): return [i for i in range(n) if mask>>i&1]
    def cut(mask):
        return sum(hi[e] for e,(i,j) in enumerate(edges) if mask>>i&1 and not mask>>j&1)-sum(lo[e] for e,(i,j) in enumerate(edges) if not mask>>i&1 and mask>>j&1)
    def rank(mask):
        return min(cut(other)+sum(beta[i] for i in members(mask&~other))-sum(alpha[i] for i in members(other&~mask)) for other in subsets)
    ranks=[rank(mask) for mask in subsets]
    assert ranks[0] == ranks[-1] == 0
    incidence=np.zeros((n,len(edges)))
    for e,(i,j) in enumerate(edges): incidence[i,e]=1; incidence[j,e]=-1
    for sign in [1,-1]:
        c=[sign*v for v in cost]
        order=sorted(range(n),key=lambda i:-c[i])
        d=[0]*n; mask=0
        for i in order:
            new=mask|(1<<i);d[i]=ranks[new]-ranks[mask];mask=new
        assert all(sum(d[i] for i in members(mask))<=ranks[mask] for mask in subsets)
        exact=sum(c[i]*d[i] for i in range(n))
        lp=linprog(-np.array(c)@incidence,A_ub=np.vstack([incidence,-incidence]),b_ub=np.array(beta+[-a for a in alpha]),bounds=list(zip(lo,hi)),method='highs')
        assert lp.success and abs(-lp.fun-exact)<1e-8
    results['box_rank_'+name] = 'exact greedy vector feasible; both support values match original LP'

path=Path(__file__).with_name('independent_checks.json')
path.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
