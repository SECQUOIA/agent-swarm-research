"""Independent exact signed P/Q and reciprocal endpoint checks for stage 3."""
from fractions import Fraction as F
from itertools import product


def eval_poly(cs, t):
    return sum((c * t**k for k, c in enumerate(cs)), F(0))

# Q = 2(t - 1/2)^2 + 1/2. P has both signs and R has excursions.
Q = [F(1), F(-2), F(2), F(0)]
P = [F(0), F(2), F(-9), F(8)]
qmin = F(1, 2)
assert eval_poly(P, F(0)) == 0
assert eval_poly(P, F(1)) == eval_poly(Q, F(1)) == 1
count = 0
for L in range(6):
    h = F(1, 2**L)
    for bits in product((0, 1), repeat=L):
        a = sum((F(b, 2**(i+1)) for i, b in enumerate(bits)), F(0))
        for side in (0, 1):
            t = a + side*h
            den = eval_poly(Q, t)
            assert den == 2*(t-F(1,2))**2 + F(1,2)
            assert den >= qmin
            for theta in (F(0), F(1,7), F(1,2), F(1)):
                v = [theta*t**k/den for k in range(4)]
                assert all(0 <= x <= 1/qmin for x in v)
                for k in range(1,4):
                    rhs = sum((F(b,2**(i+1))*v[k-1] for i,b in enumerate(bits)), F(0)) + side*h*v[k-1]
                    assert v[k] == rhs
                    for bit in bits:
                        z = bit*v[k-1]
                        assert 0 <= z <= bit/qmin and z <= v[k-1]
                        assert z >= v[k-1] - (1-bit)/qmin
                assert sum((Q[k]*v[k] for k in range(4)), F(0)) == theta
                assert sum((P[k]*v[k] for k in range(4)), F(0)) == theta*eval_poly(P,t)/den
                count += 1
# Partial fractions with positive coefficients and exact R(1)=1.
raw = [(F(3,5),F(1,128)),(F(7,3),F(3,2)),(F(2,7),F(17))]
norm = sum((A/(1+B) for A,B in raw), F(0))
terms = [(A/norm,B) for A,B in raw]
def R(t):
    return sum((A*t/(t+B) for A,B in terms), F(0))
assert R(F(0)) == 0 and R(F(1)) == 1
reciprocal = 0
for L in range(5):
    h=F(1,2**L)
    for k in range(2**L):
        a=k*h
        for theta in (F(0),F(1,3),F(1)):
            x=F(0)
            for A,B in terms:
                vm=(1-theta)/(a+B); vp=theta/(a+h+B)
                assert 0 <= vm <= 1/B and 0 <= vp <= 1/B
                x += A*(1-B*(vm+vp))
            assert x == (1-theta)*R(a)+theta*R(a+h)
            y=a*a+2*h*a*theta+h*h*theta
            assert y == (1-theta)*a*a+theta*(a+h)**2
            reciprocal += 1
print(f'PASS: {count} exact signed P/Q endpoint cases and {reciprocal} normalized reciprocal/chord cases, including L=0 and theta=0,1.')
