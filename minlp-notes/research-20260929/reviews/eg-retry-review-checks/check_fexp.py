"""Review check of egfast.fexp: (1) the table [TLO_j, THI_j] encloses 2^(j/64) (exact
comparison at 80 digits); (2) lo <= e^x <= hi at 80 digits for adversarial and random float
arguments (near the reduction boundaries m ln2/64 +- ln2/128, near -700, near 0, tiny,
integers, and uniform samples); reports the largest relative widths."""
import os, sys, random
from fractions import Fraction as Fr
import numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "open-instances-wave3", "eg", "retry"))
import egfast
mp.mp.dps = 80
bad = 0
for j in range(64):
    T = mp.mpf(2) ** (mp.mpf(j) / 64)
    if not (mp.mpf(egfast._TLO[j]) <= T <= mp.mpf(egfast._THI[j])):
        bad += 1
print("table enclosure failures:", bad)
rng = random.Random(7)
L = mp.log(2) / 64
xs = []
for m in range(-64640, 50, 1):        # boundaries x = (m + 1/2) ln2/64, both sides
    if rng.random() < 0.08 or m > -200 or m < -64400:
        b = float((m + mp.mpf(1) / 2) * L)
        xs += [b, float(np.nextafter(b, -np.inf)), float(np.nextafter(b, np.inf)), float(m * L)]
xs += [rng.uniform(-700, 0) for _ in range(20000)] + [rng.uniform(-1, 1) * 10 ** rng.uniform(-300, 0) for _ in range(3000)]
xs += [float(k) for k in range(-700, 60)] + [-700.0, float(np.nextafter(-700.0, 0)), 0.0, -0.0, 5e-324, -5e-324]
xs += [rng.uniform(0, 600) for _ in range(3000)]
xs = np.array([x for x in xs if -700 <= x <= 700])
lo, hi = egfast.fexp(xs)
fails, wmax = 0, 0.0
for x, a, b in zip(xs, lo, hi):
    e = mp.exp(mp.mpf(x))
    if not (mp.mpf(a) <= e <= mp.mpf(b)):
        fails += 1
        print("FAIL", repr(x), a, b, e)
    wmax = max(wmax, float((mp.mpf(b) - mp.mpf(a)) / e))
print(f"fexp: {len(xs)} arguments, enclosure failures {fails}, max relative width {wmax:.2e}")
# x < -700 branch
lo, hi = egfast.fexp(np.array([-700.0000001, -1e4, -745.2]))
print("x < -700 branch:", lo, hi, "e^-700 =", mp.nstr(mp.exp(-700), 5))
