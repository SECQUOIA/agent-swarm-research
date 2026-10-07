"""Re-centering algorithm RC of extension-adaptive.md (Section A.6; conjectural analysis).

Round j: center xhat_j (xhat_0 = x0), central width h_j = 2^{-j} * 2, shell partitions
Pi(xhat_{V_t}; h_j, theta) for leaves and Pi(xhat_{S_t}; h_j, theta) for cells (Lemma 3.1 of the
decomposition note), slopes lam(xhat_j), DP of Lemma 1.5 (ls_lib.dp). The consistent point of the
minimizing configuration becomes xhat_{j+1}. Stop when l_r >= UBD - eps.
Every round builds a new certificate; no knowledge of x* is used.

Leaf and cell edges around a non-dyadic centre are rounded, so boxes that touch in exact
arithmetic can miss each other by 1 ulp, and the closed intersection test then drops the pair
(which makes l_r too high). Since the revision after review, the DP uses the intersection test
widened by PAIR_TOL. Logs made before that (tol = 0) are the *_eps*.log files without "_tol".
"""
import os
import sys
import numpy as np
from ls_lib import dp, slopes, Partition, F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dp_certificate import shells  # noqa: E402


def shell_partition(n, xhat, h, mu):
    P = Partition(n)
    for t in range(n - 1):
        L, U = shells(xhat[t:t + 2], h, mu, 2)
        P.leaves[t] = dict(l1=L[:, 0].copy(), u1=U[:, 0].copy(), l2=L[:, 1].copy(), u2=U[:, 1].copy(),
                           lev=np.zeros(len(L), int))
        if t >= 1:
            Lc, Uc = shells(xhat[t:t + 1], h, mu, 1)
            P.cells[t] = dict(lo=Lc[:, 0].copy(), hi=Uc[:, 0].copy(), lev=np.zeros(len(Lc), int))
    return P


def local_solve(x, b, kappa, c):
    """L-BFGS-B from x on [-1,1]^n (the 'local solver' of Section 1.5 of the decomposition note)."""
    from scipy.optimize import minimize
    from ls_lib import dphi

    def grad(z):
        g = dphi(z, kappa) + c
        g[:-1] += b * z[1:]
        g[1:] += b * z[:-1]
        return g
    r = minimize(lambda z: F(z, b, kappa, c), x, jac=grad, bounds=[(-1, 1)] * len(x),
                 method="L-BFGS-B", options={"ftol": 1e-16, "gtol": 1e-12, "maxiter": 10000})
    return r.x


PAIR_TOL = 1e-12


def run_rc(n, b, kappa, c, eps, x0, mu=4, jmax=30, xstar=None, fstar=None, log=None, local=False,
           tol=PAIR_TOL):
    """local=True: the new center is a local minimizer found from the consistent point (RC+LS)."""
    UBD = F(x0, b, kappa, c)
    xhat = x0.copy()
    total = 0
    recs = []
    for j in range(jmax + 1):
        h = 2.0 * 2.0 ** -j
        lam = slopes(xhat, b, kappa, c)
        P = shell_partition(n, xhat, h, mu)
        nl, nc = P.size()
        total += nl + nc
        R = dp(P, lam, b, kappa, c, tol=tol)
        UBD = min(UBD, F(R["x"], b, kappa, c))
        rec = dict(j=j, h=h, leaves=nl, cells=nc, lr=R["lr"], UBD=UBD)
        if xstar is not None:
            rec["cen_inf"] = float(np.abs(xhat - xstar).max()) / h     # center error / h
            rec["x_inf"] = float(np.abs(R["x"] - xstar).max()) / h     # new consistent point error / h
            rec["x_2"] = float(np.linalg.norm(R["x"] - xstar)) / h
            rec["nu"] = float(np.linalg.norm(lam - slopes(xstar, b, kappa, c)))
        if fstar is not None:
            rec["gap"] = fstar - R["lr"]
        recs.append(rec)
        if log:
            log(rec)
        if R["lr"] >= UBD - eps:
            return dict(done=True, j=j, size=nl + nc, total=total, lr=R["lr"], UBD=UBD), recs
        xhat = R["x"]
        if local:
            xhat = local_solve(R["x"], b, kappa, c)
            UBD = min(UBD, F(xhat, b, kappa, c))
    return dict(done=False, total=total), recs
