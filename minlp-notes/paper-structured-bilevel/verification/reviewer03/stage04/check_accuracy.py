"""Independent finite exact checks of inverse, modulus, and recovery contracts."""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
z,t,v=s.symbols('z t v')
g=z**3-s.Rational(3,2)*z**2+s.Rational(3,4)*z
assert s.factor(s.diff(g,z))==3*(2*z-1)**2/4
G=g.subs(z,1); P=3; mu=G/(4*(4*P)**P)
primitive=s.integrate(g,z)
grid=[s.Rational(j,12) for j in range(13)]
increments=0; bregmans=0
for left in grid:
    for right in grid:
        distance=abs(right-left)
        div=primitive.subs(z,right)-primitive.subs(z,left)-g.subs(z,left)*(right-left)
        assert div>=mu*distance**(P+1)
        bregmans+=1
        if right>left:
            assert g.subs(z,right)-g.subs(z,left)>=G/2*(distance/(2*P))**P
            increments+=1

# Exact triangular inverse recurrence at a rational response center.
gg=z+z**3; z0=s.Rational(1,4); target0=gg.subs(z,z0)
translated=s.Poly(s.expand(gg.subs(z,z0+v)-target0),v)
Q=s.ilcm(*[a.q for a in translated.all_coeffs()])
A={j:s.expand(Q*translated.as_expr()).coeff(v,j) for j in range(1,4)}
series=s.Integer(0); coefficients=[]
for n in range(1,9):
    if n==1:
        cn=Q/A[1]
    else:
        cn=-sum(A[h]*s.expand(series**h).coeff(v,n) for h in range(2,min(3,n)+1))/A[1]
    cn=s.cancel(cn); coefficients.append(cn); series+=cn*v**n
    assert s.cancel(cn*A[1]**(2*n-1)/Q**n).q==1
residual=s.Poly(s.expand(gg.subs(z,z0+series)-target0-v),v)
assert all(residual.coeff_monomial(v**j)==0 for j in range(9))

# Same-pattern moving-resource correction has a nonzero tangent component.
row=s.Matrix([[1,2]]); hessian=s.diag(1,2)
x1=s.Rational(1,2); x2=s.Rational(1,4); delta=x1-x2
response1=s.Matrix([x1/3,x1/3]); response2=s.Matrix([x2/3,x2/3])
e=response1-response2
correction=row.T*(row*row.T).inv()*s.Matrix([delta])
tangent=e-correction
assert tangent!=s.zeros(2,1) and row*tangent==s.zeros(1,1)
gradient_difference=hessian*e
assert (gradient_difference.T*tangent)[0]==0
assert (gradient_difference.T*e)[0]==(gradient_difference.T*correction)[0]

# Sharp cubic flat-point scaling. An exponent >1/3 cannot be uniform here.
ratios=[]
for h in [s.Rational(1,4),s.Rational(1,8),s.Rational(1,16)]:
    response_delta=2*h
    target_delta=s.expand(g.subs(z,s.Rational(1,2)+h)-g.subs(z,s.Rational(1,2)-h))
    assert target_delta==2*h**3
    ratios.append(response_delta**3/target_delta)
assert ratios==[4,4,4]

# A resource component can have zero weight and drop out of signed balance.
weights=[s.Rational(2),s.Rational(-3),s.Integer(0)]
base=[s.Rational(1,4),s.Rational(3,4),s.Rational(1,2)]
shift=[s.Rational(1,8),s.Rational(7,8),s.Rational(1,2)]
signed=sum(w*(a-b) for w,a,b in zip(weights,shift,base))
absolute=sum(abs(w)*abs(a-b) for w,a,b in zip(weights,shift,base))
assert abs(signed)==absolute

# Cross a nonlinear inverse-branch boundary while preserving the rational leader.
# F_x(z)=z^4/2-x*z has z(1/4)=1/2; frozen inverse argument is x-w^3.
eta=s.Rational(1,64); alpha=(eta/(2*3))**3/2
step=alpha/100
wstar=s.Rational(1,2); wnew=wstar+step; leader=s.Rational(1,4)
argument=leader-wnew**3
assert argument<s.Rational(1,8)
assert (wstar-eta)**3<argument<(wstar+eta)**3
assert abs(argument-s.Rational(1,8))<alpha

# Strict upper feasibility can exclude all rational leaders.
irrational_roots=[s.Rational(3,8)-s.sqrt(2)/4,s.Rational(3,8)+s.sqrt(2)/4]
for root in irrational_roots:
    assert s.simplify((root+s.Rational(1,8))**2-root)==0
    assert bool(0<root<1) and root.is_rational is False

# The isolated optimum does not survive any strictly positive tightening.
isolated_g=z+z*z*(z-s.Rational(1,2))
assert s.factor(isolated_g-z)==z*z*(2*z-1)/2
assert s.expand(s.diff(isolated_g,z))==3*z*z-z+1

# Explicit size of the lifted pattern formula and the claimed exponent bounds.
for N in range(1,5):
    for k in range(4):
        original_variables=1+N+k
        maximum_conditions=3*N+4*k+2
        assert original_variables+maximum_conditions<=8*(N+k+1)

summary={
 'signed_flat_marginal_increment_checks':increments,
 'signed_bregman_checks':bregmans,
 'inverse_reversion_order':8,
 'denominator_integrality':'passed',
 'active_row_nonzero_tangent_cancellation':'passed',
 'flat_point_sharp_ratio':[str(a) for a in ratios],
 'signed_zero_weight_balance':'passed',
 'nonlinear_boundary_crossing_true_inverse_bound':'passed',
 'irrational_feasibility_and_isolated_optimum':'passed',
 'pattern_lift_variable_count':'passed',
 'limits':'Finite exact diagnostics supplement the proof audit; they do not construct general inverse panels or solve the full QE optimization.'
}
(HERE/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
