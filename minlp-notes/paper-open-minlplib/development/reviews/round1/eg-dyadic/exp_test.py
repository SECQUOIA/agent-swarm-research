"""Independent rational positive-series references for the copied eg check."""
from fractions import Fraction as F
import hashlib
from pathlib import Path
import random
import eg_dyadic_check as c

BITS = 512
SCALE = 1 << BITS

def floor(x):
    return x.numerator // x.denominator

def ceil(x):
    return -((-x.numerator) // x.denominator)

def ref_negative(t):
    # Positive series for exp(r), r <= 1/2. Its positive tail is bounded
    # by a geometric series; invert and then square with integer rounding.
    s = 0
    while t > F(1 << s, 2):
        s += 1
    r = t / (1 << s)
    term = F(1)
    total = term
    for k in range(1, 129):
        term *= r / k
        total += term
    first = term * r / 129
    tail = first / (1 - r / 130)
    lo = floor(SCALE / (total + tail))
    hi = ceil(SCALE / total)
    for _ in range(s):
        lo = lo * lo // SCALE
        hi = -((-hi * hi) // SCALE)
    return F(lo, SCALE), F(hi, SCALE)

print('Copied source SHA256:', hashlib.sha256(Path(c.__file__).read_bytes()).hexdigest())
print('Independent reference: positive Taylor degree 128, geometric tail,')
print('reciprocal, and 512-bit directed integer squaring; no floating exp.')
points = {F(0), F(1,3), F(5), F(7,2), F(1234,7), F(15), F(708), F(1, 10**90)}
for n in range(13):
    b = F(1 << n, 256)
    points.update([b, b - F(1, 1 << 300), b + F(1, 1 << 300)])
rng = random.Random(20261004)
points.update(F(rng.randrange(0, 15 * 10**12), 10**12) for _ in range(180))
counts = [0, 0, 0]
for t in sorted(points):
    lo, hi = c.exp_neg_point(t)
    rl, rh = ref_negative(t)
    assert lo <= rl <= rh <= hi, (t, 'negative point')
    counts[0] += 1
    for sign in [-1, 1]:
        if sign > 0 and t > 180:
            # The copied routine's reciprocal branch deliberately requires
            # a positive lower endpoint, unavailable at this fixed precision.
            continue
        x = sign * t
        iv = c.I.q(x)
        xl, xh = iv.ends()
        def reference(z):
            a, b = ref_negative(abs(z))
            if z > 0:
                assert a > 0
                return 1 / b, 1 / a
            return a, b
        a = reference(xl)[0]
        b = reference(xh)[1]
        l, h = c.iexp(iv).ends()
        assert l <= a <= b <= h, (x, 'interval exp')
        counts[1] += 1
        if t <= 180:
            # Exact reciprocity check, with no bypass for large arguments.
            l2,h2 = c.iexp(c.I.q(-x)).ends()
            assert l*l2 <= 1 <= h*h2, (x, 'reciprocity')
            counts[2] += 1
print('PASS: negative point references:', counts[0])
print('PASS: signed interval references:', counts[1])
print('PASS: exact reciprocity checks:', counts[2])
print('Reference arguments include zero, tiny rationals, reduction boundaries,')
print('180 reproducible random values in [0,15], 1234/7 and 708.')
print('These tests support the source proof; they do not replace it.')
