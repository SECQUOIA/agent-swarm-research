"""Independent exact checks for Stage 5 review 14; no asymptotic testing."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import sympy as s

x, y, z, u, v, a, b, c, h, sign = s.symbols("x y z u v a b c h sign")
q = 3*h/2 - sign*(u*(z-c) + c*(x*y-a*b))/2
lhs = (1-sign*v)/2 - (1-sign*a*b*c)/2 + 3*h/2
assert s.expand(lhs-q + sign*((v-u*z)+c*(u-x*y))/2) == 0
assert s.expand(v-x*y*z-(v-u*z)-z*(u-x*y)) == 0
bernstein = 0
for bits in product([0, 1], repeat=3):
    corner = [base+h*t for base, t in zip([a,b,c], bits)]
    weight = s.prod((coord-base)/h if t else (base+h-coord)/h
                    for coord,base,t in zip([x,y,z], [a,b,c], bits))
    bernstein += (1-sign*s.prod(corner))/2 * weight
assert s.cancel(bernstein-(1-sign*x*y*z)/2) == 0
assert 384*3**24 < 2**64
assert Q(7,16*64) == Q(7,1024)
assert Q(7,16*64*3) == Q(7,3072)
assert Q(7,3072*17) == Q(7,52224)
assert 3/Q(1,16) == 48
rows = [(xi,xj,xk,ui,ui*xk) for xi,xj,xk,ui in product([-1,1],repeat=4)]
assert sum(t[3]-t[0]*t[1] for t in rows) == 0
assert sum(t[4]-t[3]*t[2] for t in rows) == 0
assert sum(t[3] != t[0]*t[1] for t in rows) == 8
result = {
    "arithmetic": "exact integers and rational fractions",
    "identities": "symbolic over the rational polynomial/rational-function ring",
    "checks": ["order-one quadratic cut identity", "order-two cubic graph transfer",
               "all-eight-corner Bernstein identity", "deletion sufficient integer inequality",
               "both original and lifted exponents, including N conversion", "grid base 48"],
    "nongraph_law": {"support_size": 16, "off_graph_support_points": 8,
                     "both_graph_equations_hold_in_expectation": True},
    "limits": "Identities are universal symbolic checks. The 16-point law only illustrates the full-box versus feasible-graph distinction; it proves no lower bound or asymptotic theorem."
}
Path(__file__).with_name("independent-checks.json").write_text(json.dumps(result,indent=2)+"\n")
print("PASS: all exact identities and arithmetic checks")
