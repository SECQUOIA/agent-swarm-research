"""Independent exact checks: Lagrange inverse coefficients and tangent cancellation."""
from pathlib import Path
import json
import sympy as s

z,u,v=s.symbols('z u v')
polys=[z**3,4*z**3-6*z**2+3*z,(z+z**3)/2]
q=6
records=[]
for g in polys:
    center=s.Rational(1,4)
    t0=g.subs(z,center)
    translated=s.Poly(s.expand(g.subs(z,center+u)-t0),u)
    Q=s.ilcm(*(a.q for a in translated.all_coeffs()))
    A1=Q*translated.nth(1)
    ratio=s.cancel(u/translated.as_expr())
    coeff=[s.expand(s.series(ratio**n,u,0,n).removeO()).coeff(u,n-1)/n for n in range(1,q+1)]
    inverse=center+sum(c*v**n for n,c in enumerate(coeff,1))
    composition=s.Poly(s.expand(g.subs(z,inverse)-t0-v),v)
    assert all(composition.nth(n)==0 for n in range(q+1))
    assert all(s.cancel(c*A1**(2*n-1)/Q**n).is_Integer for n,c in enumerate(coeff,1))
    # Exact inverse bracketing at nearby targets, without evaluating radicals.
    eta=s.Rational(1,64)
    step=s.Rational(1,2**18)
    for j in (-1,0,1):
        target=t0+j*step
        approx=inverse.subs(v,j*step)
        assert 0<approx-eta<approx+eta<1
        assert g.subs(z,approx-eta)<=target<=g.subs(z,approx+eta)
    records.append({'marginal':str(g),'degree':s.degree(g,z),'inverse_terms_checked':q,'target_brackets':3})

# Same active equality z1+z2=x, marginals z1^3 and z2. The response
# (a,a^3) is exact at x=a+a^3, and the gradients are in span((1,1)).
tangent_checks=0
for a,b in [(s.Rational(1,8),s.Rational(1,4)),(s.Rational(1,4),s.Rational(1,2)),(s.Rational(1,16),s.Rational(1,8))]:
    first=s.Matrix([a,a**3]);second=s.Matrix([b,b**3]);e=first-second
    Delta=sum(e);d=s.ones(2,1)*Delta/2
    tangent=e-d
    grad=s.Matrix([a**3,a**3])-s.Matrix([b**3,b**3])
    assert sum(tangent)==0 and grad.dot(tangent)==0
    mu=s.Rational(1,4*12**3)
    assert 2*mu*max(abs(e[0]),abs(e[1]))**4<=grad.dot(e)
    tangent_checks+=1

# The displayed upper-composition degree bound needs the argument degree.
t=s.symbols('t')
arg=s.Rational(1,2)-(2*t-1)**3
branch=z
composed=branch.subs(z,arg)
assert s.degree(branch,z)==1 and s.degree(composed,t)==3
report={'inverse_checks':records,'same_pattern_tangent_checks':tangent_checks,'composition_counterexample':{'inverse_branch_degree':1,'upper_degree':1,'actual_composition_degree':3}}
report=json.loads(json.dumps(report,default=int))
print(json.dumps(report,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
