"""Relaxation volumes for (t2, t3) = (x^2, x^3), x in [1,2]  (task 4).
Term-by-term: t2 in [conv env of x^2, concave env]; t3 likewise, both as functions of x; volume in (x, t2, t3) space.
With the link t3 = t2^1.5: the set {(x,t2,t3): x^2 <= t2 <= 3x-2, x^3 <= t3 <= 7x-6, and the link region}.
The link region in (t2, t3) is between the convex curve t3 = t2^1.5 and its chord on [1,4]: t2^1.5 <= t3 <= 1 + (7/3)(t2 - 1)
(the relaxation of the convex equality t3 = t2^1.5 over t2 in [1,4]).  Volume by dense grid / exact 1-D integrals."""
import math
def vol_term():  # integral over x of (3x-2-x^2)*(7x-6-x^3)
    N = 200000; h = 1.0 / N; s = 0.0
    for i in range(N):
        x = 1 + (i + 0.5) * h; s += (3 * x - 2 - x * x) * (7 * x - 6 - x ** 3)
    return s * h
def vol_linked():
    N = 4000; h = 1.0 / N; s = 0.0
    for i in range(N):
        x = 1 + (i + 0.5) * h
        lo2, hi2 = x * x, 3 * x - 2
        lo3, hi3 = x ** 3, 7 * x - 6
        M = 400; h2 = (hi2 - lo2) / M
        for j in range(M):
            t2 = lo2 + (j + 0.5) * h2
            a = max(lo3, t2 ** 1.5); b = min(hi3, 1 + 7 / 3 * (t2 - 1))
            if b > a: s += (b - a) * h2
    return s * h
print("term-by-term volume: %.4f" % vol_term())
print("with link t3 = t2^1.5 (curve-chord in (t2,t3)) volume: %.4f" % vol_linked())
# exact polynomial for term-by-term: integrate (3x-2-x^2)(7x-6-x^3) on [1,2]
import sympy as sp
x = sp.symbols("x")
print("exact term-by-term:", sp.integrate((3 * x - 2 - x ** 2) * (7 * x - 6 - x ** 3), (x, 1, 2)), float(sp.integrate((3 * x - 2 - x ** 2) * (7 * x - 6 - x ** 3), (x, 1, 2))))
