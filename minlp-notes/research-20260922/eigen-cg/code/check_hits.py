"""Exact check of the two hits of the perturbation search (n = 6)."""
import math
from fractions import Fraction as Fr
from verify import *
from bh import pairs

n = 6
z = [Fr(3, 8), Fr(5, 8), Fr(3, 8), Fr(3, 8), Fr(3, 8), Fr(3, 8),
     Fr(1, 8), Fr(0), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4),
     Fr(1, 8), Fr(1, 8), Fr(1, 8), Fr(1, 8), Fr(1, 8), Fr(1, 8)]
print("pairs:", pairs(n))
ok, info = in_PBH(n, z)
print("z in P_BH:", ok, "number of tight BH (w0,w):", len(info) if ok else info)
if ok:
    for w in info: print("   tight", w)

sigma = [-2, -1, -1, 1, 1, 1]
for a, delta in [(11, [-1.0, -1.0, -1.0, -1.0, -0.4995, -0.4995, -0.4995]),
                 (8, [-1.0, 0.998, 0.4985, 0.4985, 0.4995, 0.4995, 0.4995])]:
    # rational point near sqrt(a) * (1, sigma) + eps * delta
    rho = Fr(math.isqrt(a * 10 ** 24), 10 ** 12)          # floor(sqrt(a)*1e12)/1e12 (rational)
    eps = Fr(1, 10 ** 5)
    vh = [rho * t + eps * Fr(d).limit_denominator(10 ** 6) for t, d in zip([1] + sigma, delta)]
    v0, v = vh[0], vh[1:]
    A, C = ecg_exact_rational(v0, v)
    print("\na =", a, " v0 =", float(v0), " v =", [float(t) for t in v])
    print(" E-CG coefficients x:", A[:n], " X:", dict(zip(pairs(n), A[n:])), " const:", C)
    print(" min over binaries:", valid_on_binaries(n, A, C))
    print(" value at z:", value(A, C, z))
