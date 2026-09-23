"""Exact symbolic certificate for the analytic cubic lower family."""
import math
import sympy as s

a,b,c,t,m=s.symbols('a b c t m')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a*a
plane=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h=F-plane
Q=s.hessian(h,(a,b))
assert Q[0,0]>0 and Q.det()==248
bstar=s.Rational(13,24)-s.Rational(3,4)*c*c
p=s.factor(h.subs({a:1,b:bstar}))
assert s.diff(h,b).subs({a:1,b:bstar})==0
grad_a=s.factor(s.diff(h,a).subs({a:1,b:bstar}))
assert s.simplify(grad_a+(90*c*c-180*c+49)/6)==0
assert grad_a.subs(c,s.Rational(3,10))==-s.Rational(31,60)
assert s.simplify(s.diff(grad_a,c)-(30-30*c))==0
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.factor(h.subs(stationary))
print('Boundary residual:',p)
print('Unconstrained residual:',r)
certificates=[(p,0,s.Rational(1,5)),(p,s.Rational(1,5),s.Rational(3,10)),(r,s.Rational(3,10),s.Rational(1,2)),(r,s.Rational(1,2),s.Rational(3,4)),(r,s.Rational(3,4),1)]
for poly,lo,hi in certificates:
    q=s.Poly(s.expand(poly.subs(c,lo+(hi-lo)*t)),t)
    degree=q.degree()
    coefficients=[s.factor(sum(q.nth(k)*s.Rational(math.comb(i,k),math.comb(degree,k)) for k in range(i+1))) for i in range(degree+1)]
    assert all(v>0 for v in coefficients)
    reconstructed=sum(coefficients[i]*math.comb(degree,i)*t**i*(1-t)**(degree-i) for i in range(degree+1))
    assert s.expand(reconstructed-q.as_expr())==0
    denominator=s.ilcm(*[s.denom(v) for v in coefficients])
    print('Interval',lo,hi,'positive Bernstein numerators',[int(v*denominator) for v in coefficients],'denominator',denominator)
count_a,count_b,count_c=m*a,m*b,m*c
choose2=lambda x:x*(x-1)/2
choose3=lambda x:x*(x-1)*(x-2)/6
fm=2*choose3(count_c)+3*count_b*choose2(count_c)+2*m*choose2(count_b)+5*m*count_a*count_c/3+10*m*count_a*count_b/9+m*choose2(count_a)
expected=F-(18*c*c+27*b*c+18*b+9*a)/m+12*c/m**2
assert s.expand(18*fm/m**3-expected)==0
cav=s.Rational(167,4)-s.Rational(153,4)/m+9/m**2
tbt=s.Rational(161,4)-s.Rational(135,4)/m+6/m**2
vex_lower=s.Rational(139,6)-72/m
hull_upper=s.Rational(223,12)+s.Rational(135,4)/m+9/m**2
assert s.simplify(cav-vex_lower-hull_upper)==0
assert plane.subs({a:s.Rational(1,4),b:s.Rational(1,2),c:s.Rational(3,4)})==s.Rational(139,6)
assert s.limit(tbt/hull_upper,m,s.oo)==s.Rational(483,223)
print('Certified ratio lower bound at m=36:',s.factor((tbt/hull_upper).subs(m,36)))
print('Limiting certified lower bound:',s.Rational(483,223))
print('All symbolic convexity, Bernstein, and finite-family identities passed.')
