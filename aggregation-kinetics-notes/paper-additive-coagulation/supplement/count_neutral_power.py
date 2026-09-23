"""Verify the atomic generator formula and certify a positive half-moment drift."""
from fractions import Fraction
from math import sqrt


def direct(alpha, p, radius):
    atoms = [(1.0, 1.0), (float(radius), 1.0 / radius)]
    mass = sum(x * w for x, w in atoms)
    coag = sum(
        0.5 * (x*y**alpha + y*x**alpha)
        * ((x+y)**p - x**p - y**p) * wx * wy
        for x, wx in atoms for y, wy in atoms
    )
    frag = mass * (2**(1-p)-1) * sum(x**(alpha+p)*w for x,w in atoms)
    return coag + frag


def formula(alpha, p, radius):
    a = 2**p + 2**(2-p)-4
    return a*(1+radius**(alpha+p-1)) + (1+radius**(alpha-1))*(
        (1+radius)**p-1-radius**p
    )


for alpha,p,radius in [(1,.5,64),(.8,.5,10000),(.4,.8,1000000),(.2,.9,10000)]:
    actual, expected = direct(alpha,p,radius), formula(alpha,p,radius)
    assert abs(actual-expected) < 1e-9*max(1,abs(actual))
    print(f"alpha={alpha}, p={p}, R={radius}: derivative={actual:.12g}")

r2, r65 = Fraction(1414,1000), Fraction(8062,1000)
assert r2*r2 < 2 and r65*r65 < 65
lower = 27*r2+2*r65-54
assert lower > 0
assert direct(1,.5,64) > float(lower)
print(f"Certified positive lower bound: {lower}")
print(f"Exact-expression decimal: {27*sqrt(2)+2*sqrt(65)-54:.12g}")

