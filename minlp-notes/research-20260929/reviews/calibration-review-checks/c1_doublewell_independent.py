"""Independent recomputation of Example 3.6 (double well) of theory-calibration/scouting.md.

Written without reusing doublewell_calibration.py. Differences in method:
  * KKT point: L-BFGS on the reduced problem from a linear ramp, then Newton with a
    sparse (scipy.sparse) Hessian; KKT residual reported.
  * Global optimality check that does not use calibrations at all: the reduced
    objective J(x_1..x_N) has Hessian >= Hlb = (2/h) D^T D - 2 a h E, where E selects
    x_1..x_{N-1}. If lambda_min(Hlb) > 0 the reduced problem is convex and the KKT
    point is the global minimizer ("hidden convexity").
  * Costate-affine bound: stage minimizations over x by a dense grid plus Newton polish
    (no cubic-root formula); u-part in closed form.
  * Best affine bound: closed form h w(xi) - (1-h) a^2/(4b); checked as B(0), and
    B(p) <= closed form checked at the costates and at random p.
  * Quadratic (Riccati) calibration: unperturbed and eps-perturbed recursions; the
    stage residual Hessians are bounded below by constant matrices, whose minimum
    eigenvalue is reported; the bound is then sum of residuals at the trajectory.
  * Critical a for the unperturbed discrete Riccati recursion vs lambda_min(Hlb) = 0,
    vs the continuous focal value pi^2/4.
  * SGM sanity case: xi = 1.3 (trajectory outside the concave region of w).
"""
import json
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.linalg import eigvalsh_tridiagonal
from scipy.optimize import minimize, brentq

B = 1.0
XI = 0.3


def w(x, a):
    return -a * x**2 + B * x**4


def dw(x, a):
    return -2 * a * x + 4 * B * x**3


def d2w(x, a):
    return -2 * a + 12 * B * x**2


def reduced(y, N, a, xi):
    h = 1.0 / N
    x = np.concatenate([[xi], y])
    d = np.diff(x)
    J = np.sum(d**2) / h + h * np.sum(w(x[:-1], a))
    g = np.zeros(N + 1)
    g[1:] += 2 * d / h
    g[:-1] -= 2 * d / h
    g[:-1] += h * dw(x[:-1], a)
    return J, g[1:]


def hess(y, N, a, xi):
    h = 1.0 / N
    main = np.full(N, 4.0 / h)
    main[-1] = 2.0 / h
    main[:-1] += h * d2w(y[:-1], a)
    off = np.full(N - 1, -2.0 / h)
    return sp.diags([off, main, off], [-1, 0, 1], format="csc")


def kkt_point(N, a, xi, sign=+1.0):
    h = 1.0 / N
    target = sign * np.sqrt(a / (2 * B))
    y0 = xi + (target - xi) * np.linspace(0, 1, N + 1)[1:]
    r = minimize(reduced, y0, args=(N, a, xi), jac=True, method="L-BFGS-B",
                 options={"maxiter": 100000, "gtol": 1e-10, "ftol": 1e-16})
    y = r.x
    for _ in range(50):
        J, g = reduced(y, N, a, xi)
        if np.max(np.abs(g)) < 1e-13:
            break
        step = spla.spsolve(hess(y, N, a, xi), -g)
        y = y + step
    J, g = reduced(y, N, a, xi)
    x = np.concatenate([[xi], y])
    u = np.diff(x) / h
    p = np.zeros(N + 1)
    for t in range(N - 1, 0, -1):
        p[t] = p[t + 1] + h * dw(x[t], a)
    return x, u, p, J, float(np.max(np.abs(g))), float(np.max(np.abs(u + p[1:] / 2)))


def lam_min_Hlb(N, a):
    """Smallest eigenvalue of (2/h)D^T D - 2ah E (reduced-Hessian lower bound), times 1/h."""
    h = 1.0 / N
    main = np.full(N, 4.0 / h)
    main[-1] = 2.0 / h
    main[:-1] -= 2 * a * h
    off = np.full(N - 1, -2.0 / h)
    return eigvalsh_tridiagonal(main, off, select="i", select_range=(0, 0))[0]


def stage_xmin(c, h, a):
    """min_x h w(x) + c x : dense grid then Newton polish (vectorized over c)."""
    grid = np.linspace(-3, 3, 6001)
    vals = h * w(grid[None, :], a) + c[:, None] * grid[None, :]
    k = np.argmin(vals, axis=1)
    x = grid[k].copy()
    for _ in range(40):
        g = h * dw(x, a) + c
        H = h * d2w(x, a)
        H = np.where(H > 1e-14, H, 1e-14)
        x = x - g / H
    return h * w(x, a) + c * x


def affine_bound(p, N, a, xi):
    h = 1.0 / N
    c = p[2:] - p[1:-1]  # stages t = 1..N-1
    m = stage_xmin(c, h, a)
    return h * w(xi, a) + p[1] * xi + np.sum(m) - h * np.sum(p[1:] ** 2) / 4


def riccati(N, a, eps):
    h = 1.0 / N
    Q = -2 * a * h - eps * h
    R = 2 * h - eps * h
    P = np.zeros(N + 1)
    P[N] = -eps
    for t in range(N - 1, -1, -1):
        piv = R + h * h * P[t + 1]
        if piv <= 0:
            return None, t
        P[t] = Q + P[t + 1] - (h * P[t + 1]) ** 2 / piv
    return P, None


def quad_check(x, u, p, N, a, eps=1e-3):
    h = 1.0 / N
    P, fail = riccati(N, a, eps)
    if P is None:
        return {"riccati_ok": False, "fail_stage": fail, "fail_t_over_T": fail / N}
    # Constant lower bound of the stage Hessian of rho_t (w'' >= -2a everywhere).
    mineig = np.inf
    maxgrad = 0.0
    for t in range(1, N):
        K = np.array([[-2 * a * h + P[t + 1] - P[t], h * P[t + 1]],
                      [h * P[t + 1], 2 * h + h * h * P[t + 1]]])
        mineig = min(mineig, np.linalg.eigvalsh(K)[0] / h)
        # gradient of rho_t at the trajectory (should be 0 by KKT)
        gx = h * dw(x[t], a) + p[t + 1] - p[t]
        gu = 2 * h * u[t] + h * p[t + 1]
        maxgrad = max(maxgrad, abs(gx), abs(gu))
    Kuu0 = 2 * h + h * h * P[1]
    # rho_t convex with zero gradient at the trajectory => its minimum is its value there;
    # sum of those values = J (telescoping), so the bound equals J exactly.
    return {"riccati_ok": True, "min_stage_hess_lb_over_h": mineig, "stage0_uu": Kuu0,
            "max_residual_grad_at_traj": maxgrad}


def critical_a(N, eps=0.0):
    def f(a):
        P, fail = riccati(N, a, eps)
        return 1.0 if P is not None else -1.0
    lo, hi = 1.0, 3.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    a_ric = lo
    a_hess = brentq(lambda a: lam_min_Hlb(N, a), 1.0, 3.0, xtol=1e-14)
    return a_ric, a_hess


def main():
    out = []
    rng = np.random.default_rng(1)
    for a in (2.0, 2.4, 3.0):
        for N in (50, 200, 1000, 5000):
            h = 1.0 / N
            x, u, p, J, gmax, kkt_u = kkt_point(N, a, XI)
            d_cost = affine_bound(p, N, a, XI)
            closed = h * w(XI, a) - (1 - h) * a * a / (4 * B)
            B0 = affine_bound(np.zeros(N + 1), N, a, XI)
            rand_ok = True
            for _ in range(5):
                pr = np.zeros(N + 1)
                pr[1:N] = rng.normal(scale=0.5, size=N - 1)
                if affine_bound(pr, N, a, XI) > closed + 1e-12:
                    rand_ok = False
            # the other (negative-well) KKT point, for comparison
            xn, un, pn, Jn, gn, _ = kkt_point(N, a, XI, sign=-1.0)
            rec = {"a": a, "N": N, "J": J, "grad_inf": gmax, "kkt_u": kkt_u,
                   "x_N": x[-1],
                   "costate_affine_gap": J - d_cost,
                   "B0_minus_closed": B0 - closed,
                   "best_affine_gap_closed": J - closed,
                   "random_p_below_closed": rand_ok,
                   "lam_min_Hlb": lam_min_Hlb(N, a),
                   "J_negative_well_kkt": Jn, "negwell_grad_inf": gn,
                   "quad": quad_check(x, u, p, N, a)}
            out.append(rec)
            print(json.dumps(rec))
            sys.stdout.flush()
    for N in (50, 200, 1000, 5000):
        a_ric, a_hess = critical_a(N)
        rec = {"N": N, "a_crit_riccati_unperturbed": a_ric, "a_crit_hidden_convexity": a_hess,
               "pi2_over_4": np.pi**2 / 4}
        out.append(rec)
        print(json.dumps(rec))
    # SGM sanity case: trajectory stays outside the concave region |x| < sqrt(a/(6b))?
    # Tangent-below condition needs |x*(t)| >= sqrt(a/(2b)) (convex-envelope region).
    for N in (50, 200, 1000):
        a = 2.0
        xi = 1.3
        x, u, p, J, gmax, _ = kkt_point(N, a, xi)
        d_cost = affine_bound(p, N, a, xi)
        rec = {"SGM_case": True, "a": a, "xi": xi, "N": N, "J": J, "min_x": float(x.min()),
               "costate_affine_gap": J - d_cost}
        out.append(rec)
        print(json.dumps(rec))
    with open("logs/c1_doublewell_independent.json", "w") as fh:
        json.dump(out, fh, indent=1, default=float)


if __name__ == "__main__":
    main()
