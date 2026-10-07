# Exact check of egfast's Cody-Waite constants against ln2/64 from the rational series (no trust in mpmath)
from fractions import Fraction as Fr
import numpy as np, mpmath as mp
with mp.workdps(60):
    _L = mp.log(2) / 64
    _Lq = Fr(mp.nstr(_L, 58, strip_zeros=False))
L1 = float(np.ldexp(np.floor(np.ldexp(float(_Lq), 38)), -38))
L2 = float(_Lq - Fr(L1))
n = 400
s = sum(Fr(1, k * 2 ** k) for k in range(1, n + 1)); tail = Fr(1, n * 2 ** n)
lo, hi = s / 64, (s + tail) / 64          # ln2/64 in [lo, hi]
err = max(abs(Fr(L1) + Fr(L2) - lo), abs(Fr(L1) + Fr(L2) - hi))
print("L1 bits ok:", Fr(L1).denominator <= 2**38 and (Fr(L1) * 2**38).numerator < 2**32)
print("|ln2/64 - L1 - L2| <=", float(err), "< 1e-27:", err < Fr(1, 10**27))
print("L1 < ln2/64 by relative", float((lo - Fr(L1)) / lo))
