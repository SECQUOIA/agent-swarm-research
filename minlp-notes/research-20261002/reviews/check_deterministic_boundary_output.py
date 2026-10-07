"""Targeted exact checks for deterministic-boundary-output.md.

This checks symbolic identities and budget inequalities, not the existing
grid implementation or a general global-optimization algorithm.
"""
from fractions import Fraction as Q

import sympy as sp


u, x, y, base = sp.symbols("u x y base")
r = x - u**2 / 4
f = base + r**2
g = f + y**2 + 3 * y * (x - u**2 / 8)
identity = (f + y**2) / 4 + 3 * (f - r**2) / 4 + 3 * (r + y)**2 / 4 + 3 * y * x / 2
assert sp.expand(g - identity) == 0
face = g.subs(x, 0)
ystar = 3 * u**2 / 16
assert sp.expand(face.subs(y, ystar) - base - 7 * u**4 / 256) == 0
assert sp.simplify(sp.diff(g, x).subs({x: 0, y: ystar})) == u**2 / 16
schur = sp.diff(face, u, 2) - sp.diff(face, u, y)**2 / sp.diff(face, y, 2)
assert sp.simplify(schur.subs(y, ystar)) == 21 * u**2 / 64

# n=1: a strictly increasing cubic isolates the secondary local minimum.
p = 7 * u**3 + 128 * u - 32
lo, hi = Q(6, 25), Q(1, 4)
def cubic(t):
    return 7 * t**3 + 128 * t - 32
assert cubic(lo) < 0 < cubic(hi)
for _ in range(100):
    mid = (lo + hi) / 2
    if cubic(mid) < 0:
        lo = mid
    else:
        hi = mid
assert hi - lo < Q(1, 2**100)
g1 = g.subs(base, (u - sp.Rational(1, 4))**2)
stationarity = sp.diff(g1, u).subs({x: 0, y: ystar})
assert sp.rem(stationarity, p, u) == 0
assert sp.diff(g1, y).subs({x: 0, y: ystar}) == 0
assert lo > 0 and hi < Q(1, 2)
assert 2 + Q(21, 64) * lo**2 > 0  # free Schur complement
assert lo**2 / 16 > 0  # strict active derivative
assert Q(7, 256) * lo**4 > 0  # strict positive objective
an = Q(1, 64)
distance_upper = (Q(1, 4) - lo)**2 + an**2 + (Q(3, 16) * hi**2)**2
assert distance_upper < 3 * an**2
assert Q(7, 9) + 1 + Q(867, 1024)**2 < 3

# First admissible trial and target-depth checks across independent scales.
trials = 0
for n in (1, 2, 13):
    for kappa in (Q(1), Q(7, 3), Q(2**30)):
        for curvature in (Q(1, 2**25), Q(35, 16), Q(2**40)):
            for width in (Q(1, 2**20), Q(1, 2), Q(2**25)):
                for bits in (0, 1, 40):
                    mu = 2
                    while 4**mu < 8 * kappa:
                        mu += 1
                    K = 4**mu
                    assert 8 * kappa <= K <= 32 * kappa
                    target = min(Q(1, 2**(2*bits) * 100*n*n*K),
                                 Q(8, 2**bits * 7*curvature*n))
                    h = width
                    stages = 0
                    while h*h > target:
                        h /= 2
                        stages += 1
                    assert 100*n*n*kappa*h*h <= Q(1, 2**(2*bits))
                    assert 100*n*kappa*h*h <= 1
                    assert Q(22, 15)*kappa*n*h*h < 1
                    assert Q(7, 8)*curvature*n*h*h <= Q(1, 2**bits)
                    # R <= 2 and theta <= 1/4 imply every integer step is one.
                    assert h <= Q(1, 10)
                    assert h + Q(2, 2**mu) < 2
                    assert stages == 0 or 4*h*h > target
                    trials += 1

print(f"PASS: 4 symbolic identities; n=1 cubic isolated through 100 exact bisections; {trials} budget fixtures")
