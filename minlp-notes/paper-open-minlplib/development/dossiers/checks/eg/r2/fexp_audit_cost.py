"""Speed and width of egfast.fexp's enclosure (code copied verbatim below) as an auditor for np.exp:
check (1 - eps) hi <= np.exp(x) <= (1 + eps) lo, which implies |np.exp(x) - e^x| <= eps e^x."""
import time, numpy as np, mpmath as mp
from fractions import Fraction as Fr
import kan_iv as K
with mp.workdps(60):
    _L = mp.log(2) / 64
    _Lq = Fr(mp.nstr(_L, 58, strip_zeros=False))
_L1 = float(np.ldexp(np.floor(np.ldexp(float(_Lq), 38)), -38))
_L2 = float(_Lq - Fr(_L1))
_INV_L = float(64 / mp.log(2))
_C = [1.0, 1.0, 0.5, 1.0 / 6, 1.0 / 24, 1.0 / 120, 1.0 / 720]
_TLO, _THI = K._TLO, K._THI
def fexp(x):
    x = np.asarray(x, dtype=np.float64)
    small = x < -700.0
    xs = np.where(small, 0.0, x)
    m = np.rint(xs * _INV_L)
    r = (xs - m * _L1) - m * _L2
    assert np.all(np.abs(r) <= 0.0055)
    p = _C[6]
    for j in range(5, -1, -1):
        p = _C[j] + r * p
    mi = m.astype(np.int64); k = np.floor_divide(mi, 64); j = mi - 64 * k
    lo = np.ldexp((_TLO[j] * p) * (1.0 - 4e-15), k); hi = np.ldexp((_THI[j] * p) * (1.0 + 4e-15), k)
    return np.where(small, 0.0, lo), np.where(small, 1e-300, hi)
rng = np.random.default_rng(5)
x = rng.uniform(-700, 17, 4_000_000)
t0 = time.perf_counter(); lo, hi = fexp(x); t = time.perf_counter() - t0
e = np.exp(x)
print(f"fexp: {1e9 * t / x.size:.0f} ns/argument; max relative width {float(np.max((hi - lo) / lo)):.2e}")
for eps in (1e-14, 9.9e-14):
    ok = ((1 - eps) * hi <= e) & (e <= (1 + eps) * lo)
    print(f"audit with eps = {eps:g}: passes on {int(ok.sum())}/{x.size} (float test; a final version would use directed rounding or a 1% safety factor)")
