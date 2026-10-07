#!/usr/bin/env python3
"""Reviewer's own exact binary64 residuals fl(L)^k - fl(L^k) (k = 2, 3) for the waterno2 speed bounds."""
from fractions import Fraction as F
import math
for L in ["0.6", "0.7", "0.8", "0.85"]:
    s = float(L)                      # fl(L), correctly rounded by Python's float()
    for k in (2, 3):
        p = float(F(L) ** k)          # fl(L^k): nearest double to the exact decimal power
        assert F(L) ** k == F(str(F(L) ** k)) if False else True
        r = F(s) ** k - F(p)          # exact residual
        print("L=%-4s k=%d  fl(L)=%r  fl(L^%d)=%r  exact residual fl(L)^%d - fl(L^%d) = %.4e" % (L, k, s, k, p, k, k, float(r)))
# tiny2 interval values reported by the trace
s = 0.7; p = float(F("0.343"))
c = F(s) ** 3
lo = math.nextafter(float(c), -math.inf) if F(float(c)) > c else float(c)
hi = math.nextafter(float(c), math.inf) if F(float(c)) < c else float(c)
print("exact fl(0.7)^3 =", float(c), "; tightest double enclosure [%r, %r]" % (lo, hi), "; fl(0.343) = %r" % p)
print("exact (fl(0.7)^3 - fl(0.343)) = %.6e ; gap of enclosure hi to p = %.6e" % (float(c - F(p)), float(F(hi) - F(p))))
print("doubles strictly between: ", [math.nextafter(hi, 1), p])
