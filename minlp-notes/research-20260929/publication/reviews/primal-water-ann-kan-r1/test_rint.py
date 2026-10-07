"""Self-test of rint.py against mpmath at 120 digits (mpmath is only the reference here)."""
import random
import time
from fractions import Fraction as Fr

import mpmath as mp

import rint

mp.mp.dps = 120
random.seed(1)
t0 = time.time()
worst = 0
for t in range(400):
    x = Fr(random.randint(-60 * 10**15, 60 * 10**15), 10**15) / random.choice([1, 3, 7, 1024])
    if t % 2:
        x = Fr(x.numerator * 10**40 + random.randint(0, 10**40), x.denominator * 10**40)  # long rationals
    lo, hi = rint.exp_bounds(x)
    ref = mp.exp(mp.mpf(x.numerator) / x.denominator)
    L, H = mp.mpf(lo.numerator) / lo.denominator, mp.mpf(hi.numerator) / hi.denominator
    assert L <= ref <= H, x
    worst = max(worst, (H - L) / ref)
    T = rint.V.tanh(rint.V(x, exact=True))
    rt = mp.tanh(mp.mpf(x.numerator) / x.denominator)
    assert mp.mpf(T.lo.numerator) / T.lo.denominator <= rt <= mp.mpf(T.hi.numerator) / T.hi.denominator
print(f"exp/tanh enclosure test passed: 400 random points in [-60, 60], worst relative width {mp.nstr(worst, 3)}")
for t in range(3000):
    q = Fr(random.randint(-10**200, 10**200), random.randint(1, 10**150))
    assert rint._rd(q, False) <= q <= rint._rd(q, True)
    assert (rint._rd(q, True) - rint._rd(q, False)) <= abs(q) * Fr(1, 2**(rint.PREC - 2))
print("outward rounding test passed (3000 rationals)")
# interval ops contain the exact result
for t in range(2000):
    a, b, c, d = sorted(Fr(random.randint(-10**9, 10**9), random.randint(1, 10**6)) for _ in range(2)) + \
        sorted(Fr(random.randint(-10**9, 10**9), random.randint(1, 10**6)) for _ in range(2))
    A, B = rint.V(a, b), rint.V(c, d)
    xa, xb = a + (b - a) * Fr(random.randint(0, 100), 100), c + (d - c) * Fr(random.randint(0, 100), 100)
    for res, ex in ((A + B, xa + xb), (A - B, xa - xb), (A * B, xa * xb)):
        assert res.lo <= ex <= res.hi
    if not B.contains0():
        R = rint.V.div(A, B)
        assert R.lo <= xa / xb <= R.hi
print(f"interval +,-,*,/ containment test passed (2000 random pairs); {time.time() - t0:.1f} s")
