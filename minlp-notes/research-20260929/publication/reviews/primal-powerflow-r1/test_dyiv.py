"""Test of dyiv sin/cos enclosures against 200-digit mpmath (evidence for the reviewer's own code)."""
import random
from fractions import Fraction as Fr

import mpmath

import dyiv as V

mpmath.mp.dps = 200
random.seed(1)
xs = ['0.5', '-1.3', '3.0', '-7.25', '1e-30', '0', '12.5',
      '-0.0877568038634369508191933583820144319392857615828189923182143'] + [repr(random.uniform(-10, 10)) for _ in range(300)]
bad = 0
maxw = 0
for x in xs:
    q = Fr(x)
    a = V.of_frac(q)
    w = Fr(1, 10 ** 40)
    b = (a[0], V.of_frac(q + w)[1])      # [q, q + w]
    for f, mf in ((V.sin, mpmath.sin), (V.cos, mpmath.cos)):
        for arg, pts in ((a, [q]), (b, [q, q + w, q + w / 3])):
            e = f(arg)
            for p in pts:
                t = Fr(mpmath.nstr(mf(mpmath.mpf(p.numerator) / p.denominator), 195))
                if not (V.lo_frac(e) - Fr(1, 10 ** 190) <= t <= V.hi_frac(e) + Fr(1, 10 ** 190)):
                    bad += 1
                    print("FAIL", x, f.__name__, p)
        maxw = max(maxw, V.hi_frac(f(a)) - V.lo_frac(f(a)))
# products and of_frac
for _ in range(2000):
    p, q = Fr(random.randint(-10**30, 10**30), random.randint(1, 10**25)), Fr(random.randint(-10**30, 10**30), random.randint(1, 10**25))
    A, B = V.of_frac(p), V.of_frac(q)
    assert V.lo_frac(A) <= p <= V.hi_frac(A)
    M = V.mul(A, B)
    assert V.lo_frac(M) <= p * q <= V.hi_frac(M)
    D = V.div_int(A, 7)
    assert V.lo_frac(D) <= p / 7 <= V.hi_frac(D)
print(f"sin/cos tests: {bad} failures over {len(xs)} points; max width at a point {float(maxw):.2e}; mul/of_frac/div_int: 2000 random cases OK")
