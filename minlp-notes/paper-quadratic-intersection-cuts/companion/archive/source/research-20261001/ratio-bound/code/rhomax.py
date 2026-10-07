"""Theorem B family in the normalized frame: rho_max(H) = sup{rho : some X with sym(X) > 0 has
sym(X M(P_i)) >= 0 at P1 = (rho, -rho, 1), P2 = (rho, -2 rho, 1), P3 = (rho, rho, 1 + H)}
(SDP bisection, Clarabel), so that z_A / z_K = rho_max(H) sqrt(eps) / z_K with H = rho_max / sqrt(eps).
Also the H = infinity limit: X upper triangular (X21 = 0), only P1 and P2."""
import numpy as np
import cvxpy as cp
import warnings

warnings.filterwarnings('ignore')


def feas(rho, H, k=2.0, limit=False):
    Ms = [np.array([[1, rho], [-rho, 1.0]]), np.array([[1, rho], [-k * rho, 1.0]])]
    if not limit:
        Ms.append(np.array([[1 + H, rho], [rho, 1.0]]))
    X = cp.Variable((2, 2))
    cons = [(X + X.T) / 2 >> np.eye(2)] + [((X @ M) + (X @ M).T) / 2 >> 0 for M in Ms]
    if limit:
        cons.append(X[1, 0] == 0)
    pr = cp.Problem(cp.Minimize(cp.norm(X, 'fro')), cons)
    try:
        pr.solve(solver='CLARABEL')
    except Exception:
        return False
    return pr.status in ('optimal', 'optimal_inaccurate')


def rhomax(H, limit=False):
    lo, hi = 1.0, 4000.0
    for _ in range(45):
        mid = np.sqrt(lo * hi)
        if feas(mid, H, limit=limit):
            lo = mid
        else:
            hi = mid
    return lo


for H in [1e3, 3e3, 1e4, 3e4, 1e5, 3e5, 1e6, 1e7, 1e8, 1e9, 1e10]:
    rm = rhomax(H)
    print('H = %.0e  rho_max = %.4f  (eps = (rho_max/H)^2 = %.3e; sqrt(H) = %.2f)' % (H, rm, (rm / H) ** 2, np.sqrt(H)), flush=True)
print('H = infinity (X21 = 0, P1 and P2 only): rho_max = %.4f' % rhomax(None, limit=True))
