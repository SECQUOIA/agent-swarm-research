"""Independent finite rational checks for whole-paper reviewer 07.

Run from paper-relaxation-limits. This script writes only its sibling JSON.
Finite checks do not establish the universally quantified theorems.
"""
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction
import hashlib
import json
import re
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SNAP = ROOT / 'process/snapshots/whole-round01'
assert hashlib.sha256((SNAP/'main.pdf').read_bytes()).hexdigest() == '912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084'

# Enumerate every vertex of the claimed eliminated four-dimensional hull.
# Variables are count n, aggregate load X, intensive T, aggregate output W.
n,x,t,w = S.symbols('n x t w')
variables = (n,x,t,w)
parameters = [(0,2,-2,3,4), (S.Rational(2,5),S.Rational(7,3),-3,-1,2),
              (1,3,0,4,1), (2,5,S.Rational(-1,3),S.Rational(7,6),3)]
scaling = []
for lo,hi,a,b,N in parameters:
    slacks = [n,N-n,x-lo*n,hi*n-x,t-a,b-t,
              w-a*x,w-N*hi*t-b*x+N*hi*b,
              N*hi*t+a*x-N*hi*a-w,b*x-w,
              b*x+lo*(N*t-N*a-n*(b-a))-w,
              w-a*x-lo*(N*t-N*b+n*(b-a))]
    matrix = S.Matrix([[S.diff(f,v) for v in variables] for f in slacks])
    rhs = S.Matrix([-f.subs(dict.fromkeys(variables,0)) for f in slacks])
    vertices=set()
    for inds in combinations(range(len(slacks)),4):
        A=matrix[list(inds),:]
        if A.det() == 0:
            continue
        z=A.inv()*rhs[list(inds),:]
        if all(q>=0 for q in matrix*z-rhs):
            vertices.add(tuple(z))
    expected={(S.Integer(0),S.Integer(0),q,S.Integer(0)) for q in (a,b)}
    expected|={(S.Integer(N),N*p,q,N*p*q) for p,q in product((lo,hi),(a,b))}
    assert vertices == expected, (parameters,vertices,expected)
    scaling.append({'parameters':list(map(str,(lo,hi,a,b,N))), 'vertices':len(vertices)})

# Exact basic-feasible-solution minimization of the six-atom cost example.
atoms=[(q,q*v,v,1 if q!=1 else 0) for q in range(3) for v in (0,1)]
A=S.Matrix([[1]*6,[z[0] for z in atoms],[z[1] for z in atoms],[z[2] for z in atoms]])
target=S.Matrix([1,1,1,S.Rational(1,2)])
costs=[]
for size in range(1,5):
    for inds in combinations(range(6),size):
        sub=A[:,list(inds)]
        if sub.rank()!=size:
            continue
        try:
            weights=sub.gauss_jordan_solve(target)[0]
        except ValueError:
            continue
        if all(q>=0 for q in weights):
            costs.append(sum(weights[j]*atoms[i][3] for j,i in enumerate(inds)))
assert min(costs)==1

# Run the manuscript's complete finite proof programs, directly extracted.
cubic=(SNAP/'sections/appendix-cubic-certificates.tex').read_text()
printed='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',cubic,re.S))
exec(compile(printed,'printed-cubic-checker','exec'),{})
signings=(SNAP/'sections/appendix-finite-signings.tex').read_text()
program=re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',signings,re.S)[0]
exec(compile(program,'printed-signing-checker','exec'),{})

# Reconstruct the three scalar polynomial identities independently.
a,b,c=S.symbols('a b c')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a*a
ell=37*a+S.Rational(79,2)*b+38*c-S.Rational(103,3)
p=S.expand((F-ell).subs({a:1,b:S.Rational(13,24)-3*c*c/4}))
stationary=S.solve([S.diff(F-ell,a),S.diff(F-ell,b)],(a,b))
r=S.expand((F-ell).subs(stationary))
rows=[(p,0,S.Rational(1,5),60000,[63125,39125,20975,9395,4133]),
      (p,S.Rational(1,5),S.Rational(3,10),240000,[16532,6008,1802,3788,11597]),
      (r,S.Rational(3,10),S.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),
      (r,S.Rational(1,2),S.Rational(3,4),190464,[25808,18056,7964,9230,15869]),
      (r,S.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
u=S.symbols('u')
for f,lo,hi,den,nums in rows:
    bern=sum(S.Rational(v,den)*S.binomial(4,i)*u**i*(1-u)**(4-i) for i,v in enumerate(nums))
    assert S.expand(f.subs(c,lo+(hi-lo)*u)-bern)==0
assert min(S.Rational(v,den) for _,_,_,den,nums in rows for v in nums)==S.Rational(901,120000)
two=a*c*c+S.Rational(5,4)*a*a-S.Rational(11,6)*a-S.Rational(20,27)*c+S.Rational(95,108)
assert S.expand(two-S.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0

out={'exact_scaling_vertices':scaling,'scale_cost_example_optimum':'1',
     'printed_finite_cubic_program':'PASS','printed_signing_program':'PASS',
     'scalar_bernstein_rows':5,'two_level_identity':'PASS',
     'scope':'Finite exact checks and polynomial identities; not general theorem certification.',
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'independent-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
