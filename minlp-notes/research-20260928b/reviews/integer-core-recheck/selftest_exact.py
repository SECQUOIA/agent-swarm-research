"""Self-test of exact.py against independent floating-point solvers (SciPy):
hull_min vs. NNLS-on-the-simplex (penalty form), box_min vs. lsq_linear, halfspace_min
vs. SLSQP.  Guards the exact tools that all other scripts use."""
import random
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import lsq_linear, minimize, nnls

from exact import hull_min, box_min, halfspace_min, phi

rng = random.Random(11)
worst = {'hull': 0.0, 'box': 0.0, 'half': 0.0}
for t in range(300):
    d = rng.choice([2, 3])
    A = [[Fr(rng.randint(-3, 3)) for _ in range(d)] for _ in range(d)]
    if abs(np.linalg.det(np.array(A, float))) < 0.5:
        continue
    y = [Fr(rng.randint(-20, 20), 7) for _ in range(d)]
    Af, yf = np.array(A, float), np.array(y, float)
    pts = [[Fr(rng.randint(-2, 3)) for _ in range(d)] for _ in range(rng.randint(1, 7))]
    ex = float(hull_min(A, y, pts)[0])
    # float: min ||A X lam - y||^2, lam >= 0, sum lam = 1 (big-weight penalty row + NNLS)
    X = np.array(pts, float).T
    M = np.vstack([Af @ X, 1e6 * np.ones((1, X.shape[1]))])
    rhs = np.concatenate([yf, [1e6]])
    lam, _ = nnls(M, rhs)
    fl = float(np.sum((Af @ X @ lam - yf) ** 2))
    worst['hull'] = max(worst['hull'], abs(ex - fl) / (1 + abs(ex)))
    lo = [rng.randint(-2, 1) for _ in range(d)]
    hi = [l + rng.randint(0, 2) for l in lo]
    exb = float(box_min(A, y, lo, hi))
    r = lsq_linear(Af, yf, bounds=(np.array(lo, float) - 1e-15, np.array(hi, float) + 1e-15))
    worst['box'] = max(worst['box'], abs(exb - 2 * r.cost) / (1 + abs(exb)))
    g = [Fr(rng.randint(-3, 3)) for _ in range(d)]
    if all(v == 0 for v in g):
        continue
    c = Fr(rng.randint(-10, 10), 3)
    exh = float(halfspace_min(A, y, g, c))
    gf = np.array(g, float)
    res = minimize(lambda x: np.sum((Af @ x - yf) ** 2), np.zeros(d), method='SLSQP',
                   constraints=[{'type': 'ineq', 'fun': lambda x: gf @ x - float(c)}], options={'ftol': 1e-14, 'maxiter': 500})
    worst['half'] = max(worst['half'], abs(exh - res.fun) / (1 + abs(exh)))
print("max relative deviation exact vs float:", {k: f"{v:.1e}" for k, v in worst.items()})
