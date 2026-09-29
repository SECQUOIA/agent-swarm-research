"""Example 5.3 constants (linediag expanded): D0 on t in [0.2,1.1], K0 over
coordinate segments |s| <= 1 (max over y, i, s of |d_ii t_j|), rho*, alpha_F,
theta, and the covering bound 2^-n ceil(0.9/delta)."""
import math
import numpy as np
import sympy as sp
import inst as I
from loss_check import DL
d = I.make('linediag'); x, y = d['syms']
poly = sp.Poly(sp.expand(d['f']), x, y)
terms = [float(c) * x ** a * y ** b for (a, b), c in poly.terms() if a + b > 0]
H = [[sp.lambdify((x, y), sp.diff(t, v, 2)) for v in (x, y)] for t in terms]
ts = np.linspace(0.2, 1.1, 91)
D0 = min(DL(d['f'], d['syms'], [t + 1, t])[0].min() for t in ts[::10])
Hmax = np.zeros(len(terms))
for t in ts:
    for i in range(2):
        for s in np.linspace(-1, 1, 41):
            p = [t + 1.0, t]; p[i] += s
            Hmax = np.maximum(Hmax, [abs(H[j][i](*p)) for j in range(len(terms))])
K0 = Hmax.sum() / 2 + Hmax.max()
rho = min(1.0, D0 / (2 * K0)); aF = D0 / (2 * 2 * 4.2); theta = D0 * rho / 2
print(f'D0={D0:.4f} K0={K0:.1f} rho*={rho:.5f} alpha_F={aF:.4f} theta={theta:.2e}')
for eps in (1e-3, 1e-4, 1e-5, 1e-6):
    delta = 2 * math.sqrt(eps / aF)
    print(f'  eps={eps:.0e}: |P| >= {math.ceil(0.9 / delta) / 4}')
