"""Two-term fits of the integrals I(eps) against the predicted leading terms.

cusp:  I = a eps^(-7/12) + b eps^(-1/2) + c; prediction a = A_cusp Gamma(17/12) Gamma(7/12)
       (b comes from the next pole, 1/2, of the smooth part of the zero curve).
xy2:   I sqrt(eps) = a log(1/eps) + b;         prediction a = pi  (theta = 2)
xy2z4: I eps^(3/4) = a log(1/eps) + b;         prediction a = c_V Gamma(7/4) Gamma(3/4)/Gamma(3/2)
Usage: python3 fit_constants.py > logs/fit_constants.log
"""
import math

import numpy as np

import integrals as it


def lsq(A, y):
    return np.linalg.lstsq(A, y, rcond=None)[0]


E = np.array([10.0 ** (-k / 2) for k in range(10, 15)])
I = np.array([it.I_cusp(e) for e in E])
a, b, c = lsq(np.vstack([E ** (-7 / 12), E ** (-0.5), np.ones_like(E)]).T, I)
print(f"cusp : fit a = {a:.5f}, b = {b:.4f}, c = {c:.3f};  predicted a = "
      f"{it.A_cusp * math.gamma(17 / 12) * math.gamma(7 / 12):.5f}  (eps in [1e-7, 1e-5])")

E = np.array([10.0 ** (-k / 2) for k in range(10, 17)])
y = np.array([it.I_xy2(e) * math.sqrt(e) for e in E])
a, b = lsq(np.vstack([np.log(1 / E), np.ones_like(E)]).T, y)
print(f"xy2  : fit a = {a:.5f}, b = {b:.4f};  predicted a = pi = {math.pi:.5f}  (eps in [1e-8, 1e-5])")

E = np.array([10.0 ** (-k / 2) for k in range(8, 13)])
y = np.array([it.I_xy2z4(e) * e ** 0.75 for e in E])
a, b = lsq(np.vstack([np.log(1 / E), np.ones_like(E)]).T, y)
pred = 2 * it.K4 * math.gamma(1.75) * math.gamma(0.75) / math.gamma(1.5)
print(f"xy2z4: fit a = {a:.5f}, b = {b:.4f};  predicted a = {pred:.5f}  (eps in [1e-6, 1e-4])")
