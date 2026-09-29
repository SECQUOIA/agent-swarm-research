"""Numerical (not exact) check that family (B) of the note (upward closures cl(C_F cap H + R_+ e_w)) also
misses T* in Proposition 16.  T* is in the (B) set of F iff for each vertex v some tau_v in [0, q(v)] has
sym(F^T (M(v) - tau_v E)) >= 0, E = e1 e1^T (tau = 0 at t* since q(t*) = 0).
For fixed tau, no nonzero F exists if there is a PD certificate Y_v with sum_v (M(v) - tau_v E) Y_v = 0
(same argument as Proposition 16(2)).  h(tau) = max{t : Y_v >= t I, sum_v A_v Y_v = 0, sum tr Y_v = 1};
h(0) is the margin of the (A) certificate.  We minimize h over the tau-box (grid + Nelder-Mead):
min h > 0 means that for every lowering no nonzero F works (numerically).
(An earlier primal version, max_F min_v lambda_min, is vacuous: F = 0 gives 0 and the rank-one vertex t*
caps it at 0.)"""
import numpy as np, cvxpy as cp, itertools
from scipy.optimize import minimize
sb = np.array([-2, 3, 2.]); v1 = np.zeros(3); v2 = np.array([6, -2, .25]); v3 = np.array([1, -2.5, .5])
q = lambda s: s[2] - s[0] * s[1]
M = lambda s: np.array([[s[2], s[0]], [s[1], 1.]])
E = np.array([[1., 0], [0, 0]])
qs = np.array([q(sb), q(v2), q(v3)])
def h(tau):
    tau = np.clip(tau, 0, qs)
    A = [M(sb) - tau[0] * E, M(v1), M(v2) - tau[1] * E, M(v3) - tau[2] * E]
    Y = [cp.Variable((2, 2), symmetric=True) for _ in range(4)]; t = cp.Variable()
    cons = [Y[i] - t * np.eye(2) >> 0 for i in range(4)]
    cons += [sum(A[i] @ Y[i] for i in range(4)) == 0, sum(cp.trace(Y[i]) for i in range(4)) == 1]
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    return t.value
print('h(0) (family A margin) = %.4e' % h(np.zeros(3)), flush=True)
grid = [np.linspace(0, qq, 9) for qq in qs]
vals = sorted(((h(np.array(tau)), tau) for tau in itertools.product(*grid)), key=lambda z: z[0])
print('grid 9^3 over [0,%g]x[0,%g]x[0,%g]: min h = %.4e at tau = %s' % (*qs, vals[0][0], np.round(vals[0][1], 3)), flush=True)
best = vals[0]
for val, tau in vals[:6]:
    r = minimize(lambda x: h(x), np.array(tau), method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-12, maxiter=600))
    x = np.clip(r.x, 0, qs)
    print('  refine from %s: h = %.4e at tau = %s' % (np.round(tau, 3), r.fun, np.round(x, 5)), flush=True)
    if r.fun < best[0]:
        best = (r.fun, x)
print('min over the tau-box of h = %.4e at tau = %s (positive: no (B) set contains T*, numerically)' % (best[0], np.round(best[1], 5)))
