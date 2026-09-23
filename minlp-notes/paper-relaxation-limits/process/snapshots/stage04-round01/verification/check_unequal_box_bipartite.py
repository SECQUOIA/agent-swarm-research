"""Exact symbolic check of the later three-variable bipartite family.

This checks all vertex residual polynomials, attaining laws and coordinate
rescaling. Nonnegativity over 0<epsilon<=2 follows analytically from the
printed factorizations; this is not a search for a universal upper bound.
"""
from itertools import product
from pathlib import Path
import json
import sympy as s

e=s.symbols('epsilon', positive=True)
a,b,c=s.symbols('a b c')
A=2*e*a*b
B=e**2*a*b+2*e*a*c+2*e*b*c+2*e**2*a*b*c
C=A+B
vertices=list(product((0,1),repeat=3))
laws=[{(0,0,0):s.Rational(1,4),(0,0,1):s.Rational(1,4),(0,1,1):s.Rational(1,4),(1,0,1):s.Rational(1,4)},
      {(0,0,1):s.Rational(3,4),(1,1,0):s.Rational(1,4)},
      {(0,0,1):s.Rational(1,2),(0,1,1):s.Rational(1,4),(1,0,0):s.Rational(1,4)},
      {(0,0,0):s.Rational(1,4),(0,0,1):s.Rational(1,2),(1,1,1):s.Rational(1,4)}]
for law in laws:
 assert sum(law.values())==1
 assert [sum(w*v[i] for v,w in law.items()) for i in range(3)]==[s.Rational(1,4),s.Rational(1,4),s.Rational(3,4)]
def ev(f,law):return s.expand(sum(w*f.subs(dict(zip((a,b,c),v))) for v,w in law.items()))
rb=[e**2,0,0,e*(2-e),0,e*(2-e),0,e*(e+4)]
rc=[2*e,0,0,0,0,0,e**2,e*(3*e+2)]
for v,x,y in zip(vertices,rb,rc):
 sub=dict(zip((a,b,c),v))
 assert s.expand((B-e**2*(a+b+c-1)).subs(sub)-x)==0
 assert s.expand((C-2*e*(a+b+c-1)).subs(sub)-y)==0
assert ev(A,laws[0])==0
assert ev(B,laws[1])==e**2/4
assert ev(C,laws[2])==e/2
upper=ev(C,laws[3]);assert s.expand(upper-3*e/2-3*e**2/4)==0
ratio=s.factor((upper-e**2/4)/(upper-e/2))
assert s.simplify(ratio-2*(e+3)/(3*e+4))==0
assert s.limit(ratio,e,0)==s.Rational(3,2)
x=1+e*a;y=1+e*b;z=1+2*c
original=2*x*y/e+x*y*z
unit=x*y+x*y*(e*z/2)
assert s.expand(unit-e*original/2)==0
out={'status':'PASS','symbolic_vertex_residuals':16,'exact_marginal_laws':4,
     'ratio':str(ratio),'limit':'3/2','epsilon_range':'0<epsilon<=2',
     'unit_coefficient_rescaling':'verified',
     'scope':'Exact family verification; no universal unequal-box upper bound.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
