"""Confirm-r1 check: x - m*L1 in egfast.fexp is exact for every float x near EVERY reduction
boundary (m + 1/2) ln2/64, |m| <= 64640, within +-8 ulps, using Knuth's TwoSum error term
(exact in IEEE double) and the Sterbenz condition y/2 <= x <= 2y (y = m L1, exact float).
Also reports L1 vs ln2/64 and the tightest Sterbenz margin (expected at m = +-1)."""
import os, sys
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "open-instances-wave3", "eg", "retry"))
import egfast as ef

with mp.workdps(80):
    L = Fr(mp.nstr(mp.log(2) / 64, 75, strip_zeros=False))
L1, L2, INV = ef._L1, ef._L2, ef._INV_L
print("L1 < ln2/64:", Fr(L1) < L, " rel gap %.4e" % float((L - Fr(L1)) / L),
      " m*L1 exact for |m|<=64641:", (Fr(L1) * 64641).denominator <= 2**38 and
      abs(Fr(L1) * 2**38 * 64641) < 2**53)
ms = np.arange(-64641, 64641, dtype=np.float64)
b = np.concatenate([(ms + 0.5) * float(L), (ms - 0.5) * float(L)])
xs = [b]
up, dn = b.copy(), b.copy()
for _ in range(8):
    up = np.nextafter(up, np.inf); dn = np.nextafter(dn, -np.inf)
    xs += [up, dn]
x = np.concatenate(xs)
x = x[(x >= -700.0) & (x <= 700.0)]
x = np.concatenate([x, np.linspace(-1e-2, 1e-2, 200001)])
m = np.rint(x * INV)
y = m * L1
s = x - y
bb = s - x
err = (x - (s - bb)) + (-y - bb)
pos, neg = m > 0, m < 0
ster = np.where(pos, (y / 2 <= x) & (x <= 2 * y), np.where(neg, (y / 2 >= x) & (x >= 2 * y), True))
print("arguments", x.size, " TwoSum nonzero error:", int(np.count_nonzero(err)),
      " Sterbenz condition fails:", int(np.count_nonzero(~ster)),
      " |r~|max %.6f" % np.max(np.abs(s - m * L2)))
k = pos & (m == 1)
print("m=1: smallest x %.17g, ratio x/(L1/2) - 1 = %.3e" % (x[k].min(), x[k].min() / (L1 / 2) - 1))
k = neg & (m == -1)
print("m=-1: largest x %.17g, ratio x/(-L1/2) - 1 = %.3e" % (x[k].max(), x[k].max() / (-L1 / 2) - 1))
