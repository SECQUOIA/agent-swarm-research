from fractions import Fraction as F
from math import factorial,lcm
import sympy as s
z=s.symbols('z')
# Increasing normalized signed marginals: one with an interior flat point,
# one with two nonreal critical points, and one nonlinear endpoint-flat map.
gs=[4*z**3-6*z**2+3*z, (z**3/3-z**2/2+F(5,16)*z)/F(7,48),z**5]
results=[]
for g in gs:
    g=s.Poly(g,z);D=g.degree()
    assert g.eval(0)==0 and g.eval(1)==1
    fi=s.integrate(g.as_expr(),z)
    checks=0
    for a in range(17):
        for b in range(a+1,17):
            aa,bb=s.Rational(a,16),s.Rational(b,16);h=bb-aa
            assert g.eval(bb)-g.eval(aa)>=s.Rational(1,2)*(h/(2*D))**D
            for u,v in ((aa,bb),(bb,aa)):
                val=fi.subs(z,u)-fi.subs(z,v)-g.eval(v)*(u-v)
                assert val>=abs(u-v)**(D+1)/(4*(4*D)**D)
            checks+=1
    z0=F(1,4); t0=F(g.eval(s.Rational(z0)))
    ah=[F(s.diff(g.as_expr(),z,h).subs(z,s.Rational(z0)))/factorial(h) for h in range(1,D+1)]
    Q=lcm(*(a.denominator for a in ah));A=[int(a*Q) for a in ah];q=12
    c=[F(0)]*(q+1);c[1]=F(Q,A[0])
    def mul(a,b):
        out=[F(0)]*(q+1)
        for i in range(q+1):
            for j in range(q+1-i): out[i+j]+=a[i]*b[j]
        return out
    for n in range(2,q+1):
        power=c.copy();total=F(0)
        for h in range(2,min(D,n)+1):
            power=mul(power,c);total+=A[h-1]*power[n]
        c[n]=-total/A[0]
    # Independent complete composition verifies the inverse series.
    out=[F(0)]*(q+1);power=c.copy()
    for h in range(1,D+1):
        for n in range(q+1):out[n]+=ah[h-1]*power[n]
        power=mul(power,c)
    assert out[1]==1 and all(out[n]==0 for n in range(q+1) if n!=1)
    for n in range(1,q+1):
        assert (c[n]*A[0]**(2*n-1)/Q**n).denominator==1
    critical=s.solve(s.diff(g.as_expr(),z),z)
    results.append(dict(g=str(g.as_expr()),grid_intervals=checks,taylor_order=q,critical_points=list(map(str,critical))))
print('PASS: exact increment/Bregman bounds on 408 rational intervals, both Bregman orientations; three order-12 inverse compositions and denominator identities')
print(results)
