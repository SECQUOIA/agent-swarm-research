"""Exact (Fraction) check of the constants of kan_iv.iexp_pt_fast and egfast.fexp's table, without mpmath:
TLO_j^64 <= 2^j <= THI_j^64; ln2 bracket vs rational series bounds; LN2_64 scaling; Taylor remainder."""
from fractions import Fraction as F
import math, kan_iv as K
bad = [j for j in range(64) if not (F(float(K._TLO[j])) ** 64 <= 2 ** j <= F(float(K._THI[j])) ** 64)]
print("table entries failing:", bad)
rel = max(float((F(float(K._THI[j])) - F(float(K._TLO[j]))) / F(float(K._TLO[j]))) for j in range(64))
print(f"max relative table width {rel:.3e}")
n = 300; s = sum(F(1, k * 2 ** k) for k in range(1, n + 1)); tail = F(1, n * 2 ** n)
lo, hi = F(float(K.LN2.lo)), F(float(K.LN2.hi))
print("ln2 in [LN2.lo, LN2.hi]:", lo <= s and s + tail <= hi, "; width/2^-53 =", float((hi - lo) / F(2) ** -53))
print("LN2_64 = LN2/64 exactly:", F(float(K.LN2_64.lo)) == lo / 64 and F(float(K.LN2_64.hi)) == hi / 64)
r = F(55, 10000); b = r ** 9 / math.factorial(9) * (1 + 2 * r)
print(f"degree-8 remainder bound {float(b):.3e} <= 1e-25: {b <= F(1e-25)}")
print("inverse factorial intervals contain 1/j!:", all(F(float(K._INVF2[j].lo)) <= F(1, math.factorial(j)) <= F(float(K._INVF2[j].hi)) for j in range(9)))
