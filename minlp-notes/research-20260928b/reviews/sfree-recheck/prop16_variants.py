"""Exploratory (numerical): which feature of the Proposition 16 instance drives z_A < 1?  Vary v2 and report
the edge slope grad q(t*).(v2 - t*) = w2 (transversality at t*), min of q over the far face conv{sbar, v2, v3}
(near-contact away from t*; must be > 0 for z_K = 1 with unique support-one minimizer, by the radial argument
of prop16_exact.py), and z_A (bisection, Clarabel; dual certificate margin at z = 1 also reported)."""
import numpy as np, cvxpy as cp
from scipy.optimize import minimize_scalar
sb = np.array([-2, 3, 2.]); v1 = np.zeros(3); v3 = np.array([1, -2.5, .5])
q = lambda s: s[2] - s[0] * s[1]
M = lambda s: np.array([[s[2], s[0]], [s[1], 1.]])
def face_min(v2):
    best = np.inf
    for a in np.linspace(0, 1, 401):
        bs = np.linspace(0, 1 - a, max(2, int(401 * (1 - a))))
        pts = sb[None] + a * (v2 - sb)[None] + bs[:, None] * (v3 - sb)[None]
        best = min(best, np.min(pts[:, 2] - pts[:, 0] * pts[:, 1]))
    return best
def feasible(z, v2):
    V = [sb] + [sb + z * (v - sb) for v in (v1, v2, v3)]
    F = cp.Variable((2, 2)); t = cp.Variable()
    cons = [(F.T @ M(v) + M(v).T @ F) / 2 - t * np.eye(2) >> 0 for v in V] + [cp.norm(F, 'fro') <= 1]
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    return t.value > 1e-8          # F = 0 always gives t = 0, so feasibility needs a strictly positive margin
def margin(v2):
    Y = [cp.Variable((2, 2), symmetric=True) for _ in range(4)]; t = cp.Variable()
    Ms = [M(v) for v in (sb, v1, v2, v3)]
    cons = [Y[i] - t * np.eye(2) >> 0 for i in range(4)] + [sum(Ms[i] @ Y[i] for i in range(4)) == 0, sum(cp.trace(y) for y in Y) == 1]
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL'); return t.value
def zA(v2):
    lo, hi = 0.5, 1.0
    if not feasible(lo, v2): return float('nan')
    for _ in range(26):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if feasible(mid, v2) else (lo, mid)
    return lo
rows = [('Prop 16', np.array([6, -2, .25]))]
for w2 in (0.5, 1.0, 2.0):
    rows.append(('w2 = %g' % w2, np.array([6, -2, w2])))
for (x2, y2) in ((6, -3), (6, -4), (4, -3), (8, -3)):
    rows.append(('(x2,y2) = (%g,%g), w2 = 1/4' % (x2, y2), np.array([x2, y2, .25])))
for name, v2 in rows:
    fm = face_min(v2)
    cosang = v2[2] / np.linalg.norm(v2)
    print('%-28s edge cosine at t* %.4f | min q on far face %.4f | %s' % (name, cosang, fm,
          ('certificate margin at z=1 %.2e | z_A = %.5f' % (margin(v2), zA(v2))) if fm > 0 else 'far face meets S: z_K < 1, skipped'), flush=True)
