"""Exact (rational) check of the constants behind kan_iv.iexp_pt_fast, without trusting mpmath:
 (1) TLO_j^64 <= 2^j <= THI_j^64 for j = 0..63 (so [TLO_j, THI_j] contains 2^(j/64));
 (2) the double bracket [l2lo, l2hi] of ln 2, against rational bounds from
     ln 2 = sum_{k>=1} 1/(k 2^k) with tail < 1/(n 2^n);
 (3) LN2_64 = [l2lo/64, l2hi/64] is an exact scaling;
 (4) _REM2 >= r^9/9! e^r for |r| <= 0.0055 (with e^r <= 1 + 2r)."""
from fractions import Fraction as F
import math
import kan_iv as K
ok = True
for j in range(64):
    lo, hi = F(float(K._TLO[j])), F(float(K._THI[j]))
    if not (lo ** 64 <= 2 ** j <= hi ** 64): ok = False; print("table FAIL", j)
print("table exact check:", "all 64 entries enclose 2^(j/64)" if ok else "FAIL")
n = 200
s = sum(F(1, k * 2 ** k) for k in range(1, n + 1)); tail = F(1, n * 2 ** n)
l2lo, l2hi = F(float(K.LN2.lo)), F(float(K.LN2.hi))
print("ln2 bracket exact check:", l2lo <= s and s + tail <= l2hi, "; width (ulps):", float((l2hi - l2lo) / F(2) ** -53))
print("LN2_64 exact scaling:", F(float(K.LN2_64.lo)) == l2lo / 64 and F(float(K.LN2_64.hi)) == l2hi / 64)
r = F(55, 10000)
bound = r ** 9 / math.factorial(9) * (1 + 2 * r)
print("remainder:", float(bound), "<= _REM2 =", K._REM2, bound <= F(K._REM2))
print("factorials exact in double for j <= 8:", all(float(math.factorial(j)) == math.factorial(j) for j in range(9)))
