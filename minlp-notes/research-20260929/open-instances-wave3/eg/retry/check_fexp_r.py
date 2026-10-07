"""Exact check of the argument reduction in egfast.fexp (review item on the docstring bound).

For float arguments x it repeats the float steps of fexp,
    m = rint(x / (ln2/64)),  s = fl(x - m L1),  r~ = fl(s - fl(m L2)),
and checks in exact rational arithmetic (ln2/64 to 75 digits) that
  (a) m L1 is exact and s = x - m L1 exactly (Sterbenz's lemma, since 0 < L1 < ln2/64), and
  (b) |r~ - r| with r = x - m ln2/64, against the docstring bound.
Arguments: both float neighbours (3 ulps each side) of every reduction boundary
(m + 1/2) ln2/64 for |m| <= 300 and near |m| = 64640, of 2% of the other boundaries,
and 100,000 uniform arguments in [-700, 700].  Evidence for the hand argument, not a proof.

    python3 check_fexp_r.py
"""
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

import egfast as ef

with mp.workdps(80):
    L = Fr(mp.nstr(mp.log(2) / 64, 75, strip_zeros=False))
L1, L2 = ef._L1, ef._L2
print(f"L1 < ln2/64: {Fr(L1) < L}; (ln2/64 - L1)/L1 = {float((L - Fr(L1)) / Fr(L1)):.3e}")

rng = np.random.default_rng(11)
ms = set(range(-300, 301)) | set(range(-64640, -64340)) | set(range(64340, 64641))
others = [m for m in range(-64640, 64641) if m not in ms]
ms |= set(rng.choice(others, size=len(others) // 50, replace=False).tolist())
xs = []
for m in sorted(ms):
    for h in (Fr(1, 2), Fr(-1, 2)):
        b = float((m + h) * L)
        v = b
        for _ in range(3):
            v = np.nextafter(v, -np.inf)
        for _ in range(7):
            xs.append(v)
            v = np.nextafter(v, np.inf)
xs = np.array(xs)
xs = xs[(xs >= -700.0) & (xs <= 700.0)]
xs = np.concatenate([xs, rng.uniform(-700.0, 700.0, 100_000)])

m = np.rint(xs * ef._INV_L)
mL1 = m * L1
s = xs - mL1
mL2 = m * L2
rt = s - mL2
assert np.all(np.abs(rt) <= 0.0055)
inexact_mL1 = inexact_s = 0
worst = Fr(0)
worst_rel = 0.0
for x, mi, a, b, r in zip(xs.tolist(), m.tolist(), mL1.tolist(), s.tolist(), rt.tolist()):
    X, M = Fr(x), int(mi)
    if Fr(a) != M * Fr(L1):
        inexact_mL1 += 1
    if Fr(b) != X - Fr(a):
        inexact_s += 1
    e = abs(Fr(r) - (X - M * L))
    if e > worst:
        worst = e
    if r != 0.0:
        worst_rel = max(worst_rel, float(e) / abs(r))
print(f"{len(xs)} arguments ({len(xs) - 100_000} at reduction boundaries): m L1 inexact {inexact_mL1}, "
      f"x - m L1 inexact {inexact_s}")
print(f"max |r~ - r| = {float(worst):.3e} (docstring bound 1e-18; u * 0.0055 = {0.0055 * 2.0**-53:.3e}); "
      f"max |r~ - r|/|r~| = {worst_rel:.3e}")
