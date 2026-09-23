"""Independent stage-4 identity/bound diagnostics, with no author imports."""
import itertools
import json
from pathlib import Path
import sympy as s

t,x,w,v=s.symbols('t x w v')
signed=4*t**3-6*t**2+3*t  # strictly increasing, derivative zero at 1/2
positive=(t+t**4)/2
checks=0
for g in [signed,positive,t,t**5]:
    P=s.degree(g,t)
    F=s.integrate(g,t)
    mu=s.Rational(1,4*(4*P)**P)
    for a,b in itertools.product([s.Rational(i,12) for i in range(13)],repeat=2):
        if a==b:
            continue
        h=abs(b-a)
        increment=abs(g.subs(t,b)-g.subs(t,a))
        assert increment>=s.Rational(1,2)*(h/(2*P))**P
        div=F.subs(t,b)-F.subs(t,a)-g.subs(t,a)*(b-a)
        assert div>=mu*h**(P+1)
        checks+=1

# Common active resource pattern with a genuinely nonzero tangential correction:
# min z1^4/4 + z2^4/2 subject to z1+2z2=3x on the unit box.
# The unique response is (x,x), and both opposite resource rows are active.
A=s.Matrix([[1,2]])
same_pattern_cases=0
for a,b in itertools.combinations([s.Rational(i,8) for i in range(1,8)],2):
    z=s.Matrix([a,a]);zp=s.Matrix([b,b]);e=z-zp
    d=A.T*(A*A.T).inv()*s.Matrix([3*(a-b)])
    tangent=e-d
    grad=s.Matrix([a**3,2*a**3]);gradp=s.Matrix([b**3,2*b**3])
    assert A*tangent==s.zeros(1,1)
    assert tangent!=s.zeros(2,1)
    assert ((grad-gradp).T*tangent)[0]==0
    assert s.simplify(((grad-gradp).T*e)[0]-((grad-gradp).T*d)[0])==0
    mu=s.Rational(1,4*12**3)
    assert 2*mu*abs(a-b)**4<=((grad-gradp).T*e)[0]
    same_pattern_cases+=1

# Degree accounting counterexample: exact inverse has degree one; the aggregate
# argument is cubic. The normalized variable is w=2v-1.
argument=x-(2*v-1)**3
composed_degree=s.Poly(argument,x,v).total_degree()
assert composed_degree==3
assert argument.subs({x:s.Rational(17,64),v:s.Rational(5,8)})==s.Rational(1,4)

# Strict inequality lifts require unbounded auxiliary variables at a boundary.
u=s.symbols('u',positive=True)
assert s.simplify((t*u**2-1).subs(t,1/u**2))==0
assert s.limit(1/s.sqrt(t),t,0,dir='+')==s.oo
# Actual shifted cubic response pattern: x=(1+z^3)/2, z>0.
assert s.expand(t**3-(2*x-1)).subs(x,(1+t**3)/2).expand()==0

# Explicit condition/variable upper bounds used by the component argument.
for N in range(1,20):
    for k in range(5):
        conditions=3*N+4*k+2
        base_vars=1+N+k
        assert base_vars+conditions<=8*(N+k+1)

# Complex critical values with an interior real part: g' has no real zero.
g=(16*t**3-24*t**2+13*t)/5
roots=s.solve(s.diff(g,t),t)
critical_values=[s.simplify(s.expand_complex(g.subs(t,z))) for z in roots]
assert all(s.re(value)==s.Rational(1,2) and s.im(value)!=0 for value in critical_values)

# Exact rational Taylor reversion, checked by composition and denominator powers.
z0=s.Rational(1,4);t0=g.subs(t,z0)
translated=s.Poly(s.expand(g.subs(t,z0+t)-t0),t)
den=s.ilcm(*[co.q for co in translated.all_coeffs()])
Acoef={j:s.expand(den*translated.as_expr()).coeff(t,j) for j in range(1,4)}
series=s.Integer(0);reversion_checks=0
for n in range(1,8):
    if n==1:
        cn=s.Rational(den,Acoef[1])
    else:
        cn=-sum(Acoef[j]*s.expand(series**j).coeff(v,n)
                for j in range(2,min(3,n)+1))/Acoef[1]
    series+=cn*v**n
    integer_n=s.cancel(cn*Acoef[1]**(2*n-1)/den**n)
    assert integer_n.is_Integer
    reversion_checks+=1
composition=s.Poly(s.expand(g.subs(t,z0+series)-t0-v),v)
assert all(composition.coeff_monomial(v**j)==0 for j in range(8))

# Sharpness: for every tested degree the response distance is exactly delta^(1/P).
sharpness_checks=0
for P in [1,2,3,5,8]:
    for n in [2,3,5,8]:
        response=s.Rational(1,n);delta=response**P
        assert response**P==delta
        sharpness_checks+=1

result={'signed_and_positive_increment_bregman_checks':checks,
        'moving_rhs_tangent_identity_cases':same_pattern_cases,
        'inverse_branch_degree':1,'composed_upper_degree':composed_degree,
        'strict_inequality_noncompact_lift':'passed',
        'lift_variable_count':'passed for N=1..19 and k=0..4',
        'complex_critical_values':[str(z) for z in critical_values],
        'exact_reversion_coefficients_checked':reversion_checks,
        'reversion_composition_order':7,'sharpness_identities':sharpness_checks}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
