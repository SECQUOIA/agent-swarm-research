"""Independent exact Stage 5 upper-certificate checks; no author code imported."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import sympy as s

x = s.symbols('x0:3')
a = s.symbols('a0:3')
h, b, beta, u, v = s.symbols('h b beta u v', nonzero=True)
c = (1-b*s.prod(x))/2
rhs = 0
for bits in product((0,1), repeat=3):
    corner = (1-b*s.prod(a[i]+h*bits[i] for i in range(3)))/2
    basis = s.prod((x[i]-a[i])/h if bits[i] else (a[i]+h-x[i])/h for i in range(3))
    rhs += (corner-beta)*basis
assert s.expand(h**3*(c-beta-rhs)) == 0
assert s.expand(v-s.prod(x) - ((v-u*x[2])+x[2]*(u-x[0]*x[1]))) == 0
q = 3*h/2-b/2*(u*(x[2]-a[2])+a[2]*(x[0]*x[1]-a[0]*a[1]))
assert s.expand((1-b*v)/2-(1-b*s.prod(a))/2+3*h/2-q+b/2*((v-u*x[2])+a[2]*(u-x[0]*x[1]))) == 0

# Every grid box in three dimensions for several grid bases; exact rational
# vertices suffice for q because q is multiaffine in the full box variables.
vertex_count = 0
for M in (1,2,3,4,7):
    width = Q(2,M)
    for inds in product(range(M), repeat=3):
        lower = tuple(-1+width*i for i in inds)
        for bits in product((0,1), repeat=3):
            xx = tuple(lower[i]+width*bits[i] for i in range(3))
            for sign, uu in product((-1,1), repeat=2):
                qq = 3*width/2-Q(sign,2)*(uu*(xx[2]-lower[2])+lower[2]*(xx[0]*xx[1]-lower[0]*lower[1]))
                assert qq >= 0
                vertex_count += 1

# Explicit first/second moment law outside the graph, even with value below
# the true graph minimum on the node. xi=xj=0, xk in [0,h], u in {-1,1}.
# Correlate u=+1 with xk=h and u=-1 with xk=0. v is independent with mean h/2.
width = Q(1,24)
law=[]
for uu, vv in product((-1,1), repeat=2):
    weight = Q(1,2)*(Q(1,2)+vv*width/4)
    law.append((weight,(Q(0),Q(0),width if uu==1 else Q(0),uu,vv)))
assert sum(p for p,z in law)==1
assert all(p>0 and z[3] != z[0]*z[1] for p,z in law)
assert sum(p*(z[3]-z[0]*z[1]) for p,z in law)==0
assert sum(p*(z[4]-z[3]*z[2]) for p,z in law)==0
obj=sum(p*(1-z[4])/2 for p,z in law)
assert obj==Q(1,2)-width/4 < Q(1,2)
assert obj>=Q(1,2)-3*width/2

# Exact ceiling edge cases, including epsilon > 3 (one full-cube box).
for eps in (Q(1,16),Q(3),Q(3001,1000),Q(2999,1000),Q(1,10**6),Q(100)):
    ratio=3/eps
    M=(ratio.numerator+ratio.denominator-1)//ratio.denominator
    assert M>=1 and Q(3,M)<=eps
assert 384*3**24 < 2**64
assert Q(7,16*64)==Q(7,1024)
assert Q(7,16*64*3)==Q(7,3072)
assert Q(7,3072*17)==Q(7,52224)

result={"status":"PASS","arithmetic":"exact rational and formal symbolic", "formal_identities":3,
        "quadratic_vertex_cases":vertex_count,"nongraph_law_support":4,
        "nongraph_objective":str(obj),"nongraph_true_node_minimum":"1/2",
        "grid_epsilon_cases":6,
        "limits":"Finite inequalities and one nongraph law do not prove asymptotic lower bounds. Formal identities hold symbolically; universal inequality proofs are in the independent review."}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
