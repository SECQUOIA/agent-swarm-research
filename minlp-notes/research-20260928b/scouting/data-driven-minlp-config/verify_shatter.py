# Exact-rational re-verification of the shattering found by shatter.py (clean model).
import numpy as np, subprocess
from fractions import Fraction as F
LO, HI, N = 0.40, 0.60, 4_000_001
chosen = [(0.3141592653589793, 10**-1.5, 7), (0.2718281828459045, 10**-2, 9), (0.2718281828459045, 10**-2.5, 13),
          (0.3141592653589793, 10**-4.5, 25), (0.6180339887498949, 10**-6, 33), (0.4142135623730951, 10**-7, 39),
          (0.6180339887498949, 10**-8.5, 47)]
def dual(xs, eps):
    out = subprocess.run(['./quadmodel_bin', repr(xs), '2.0', repr(eps), repr(LO), repr(HI), str(N)], capture_output=True).stdout
    return np.frombuffer(out, dtype=np.int32)
V = [dual(xs, e) for xs, e, _ in chosen]
codes = sum(((v >= r).astype(np.int64) << k) for k, (v, (_, _, r)) in enumerate(zip(V, chosen)))
rho = F(2)
def cnt(l, u, a, xs, eps):
    m, r = (l + u)/2, (u - l)/2; d = m - xs
    if not (r*r - d*d/(1 + rho) > eps/rho): return 1
    p = l + a*(u - l)
    return 1 + cnt(l, p, a, xs, eps) + cnt(p, u, a, xs, eps)
ok = 0
for c in range(2**len(chosen)):
    i = int(np.nonzero(codes == c)[0][len(np.nonzero(codes == c)[0])//2])
    a = F(LO) + (F(HI) - F(LO))*F(i, N - 1)
    bits = [int(cnt(F(0), F(1), a, F(xs), F(eps)) >= r) for xs, eps, r in chosen]
    ok += (sum(b << k for k, b in enumerate(bits)) == c)
print('patterns verified exactly:', ok, 'of', 2**len(chosen))
