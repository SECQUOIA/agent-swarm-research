"""Affine versus quadratic discrete calibrations on a double-well control problem.

Floating-point illustration (not a certified computation) for
scouting.md, Example 3.6.

Discrete problem (explicit Euler, T = 1, h = T/N):
    min  J = h * sum_{t=0}^{N-1} (u_t^2 + w(x_t)),   w(x) = -a x^2 + b x^4,
    s.t. x_{t+1} = x_t + h u_t,  x_0 = xi,  x_N free, all variables free.

Reported per (a, N):
  * J at the KKT point found by Newton on the reduced problem;
  * affine (Lagrangian) bound with the discrete costates, d(p*);
  * best affine bound, max_p d(p), computed two ways: by maximizing the
    concave dual function (L-BFGS) and as the convexified primal
    (w replaced by its convex envelope); the two must agree;
  * quadratic calibration: Riccati recursion of the comparison LQ problem
    with the global Hessian lower bound w'' >= -2a (perturbed by eps), the
    smallest eigenvalue of the stage Hessian lower bounds (>= eps*h expected),
    and the bound obtained by numerically minimizing every stage residual
    from far-away starting points.
"""

import json
import sys

import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import minimize


def w(x, a, b):
    return -a * x**2 + b * x**4


def dw(x, a, b):
    return -2 * a * x + 4 * b * x**3


def d2w(x, a, b):
    return -2 * a + 12 * b * x**2


def solve_primal(N, a, b, xi, T=1.0, x_init=None):
    """Newton with backtracking on the reduced problem in x_1..x_N."""
    h = T / N
    x = np.full(N + 1, xi) if x_init is None else x_init.copy()
    x[0] = xi

    def J(xx):
        return np.sum((xx[1:] - xx[:-1]) ** 2) / h + h * np.sum(w(xx[:-1], a, b))

    for it in range(200):
        d = x[1:] - x[:-1]
        g = np.zeros(N + 1)
        g[1:] += 2 * d / h
        g[:-1] -= 2 * d / h
        g[:-1] += h * dw(x[:-1], a, b)
        g = g[1:]
        diag = np.full(N, 4.0 / h)
        diag[-1] = 2.0 / h
        diag[:-1] += h * d2w(x[1:-1], a, b)
        off = np.full(N - 1, -2.0 / h)
        # regularize if not positive definite (saddle avoidance)
        shift = 0.0
        while True:
            ab = np.zeros((3, N))
            ab[0, 1:] = off
            ab[1, :] = diag + shift
            ab[2, :-1] = off
            try:
                step = solve_banded((1, 1), ab, -g)
            except np.linalg.LinAlgError:
                shift = max(2 * shift, 1e-6)
                continue
            if g @ step < 0:
                break
            shift = max(2 * shift, 1e-6 / h)
        f0 = J(x)
        s = 1.0
        while True:
            xn = x.copy()
            xn[1:] += s * step
            if J(xn) <= f0 + 1e-4 * s * (g @ step) or s < 1e-12:
                break
            s *= 0.5
        x = xn
        if np.max(np.abs(g)) < 1e-13 and shift == 0.0:
            break
    u = (x[1:] - x[:-1]) / h
    # costates: p_N = 0, p_t = p_{t+1} + h w'(x_t), t = N-1..1
    p = np.zeros(N + 1)
    for t in range(N - 1, 0, -1):
        p[t] = p[t + 1] + h * dw(x[t], a, b)
    kkt_u = np.max(np.abs(u + p[1:] / 2))  # u_t = -p_{t+1}/2
    return x, u, p, J(x), kkt_u


def stage_min_quartic(c, h, a, b):
    """Global min over x of h*w(x) + c*x (vectorized over c) via cubic roots."""
    c = np.atleast_1d(c)
    # derivative: 4 h b x^3 - 2 h a x + c = 0
    comp = np.zeros((c.size, 3, 3))
    comp[:, 1, 0] = 1.0
    comp[:, 2, 1] = 1.0
    # monic: x^3 + 0 x^2 + (-a/(2b)) x + c/(4 h b)
    comp[:, 0, 2] = -c / (4 * h * b)
    comp[:, 1, 2] = a / (2 * b)
    roots = np.linalg.eigvals(comp)
    xr = np.where(np.abs(roots.imag) < 1e-7 * (1 + np.abs(roots.real)), roots.real, np.nan)
    vals = h * w(xr, a, b) + c[:, None] * xr
    vals = np.where(np.isnan(vals), np.inf, vals)
    k = np.argmin(vals, axis=1)
    return vals[np.arange(c.size), k], xr[np.arange(c.size), k]


def dual_value(pint, N, h, a, b, xi):
    """d(p) with p_1..p_{N-1} = pint and p_N = 0. Returns value and gradient."""
    p = np.zeros(N + 1)
    p[1:N] = pint
    c = p[2:] - p[1:-1]  # stages t = 1..N-1: c_t = p_{t+1} - p_t
    m, xs = stage_min_quartic(c, h, a, b)
    val = h * w(xi, a, b) + p[1] * xi + np.sum(m) - h * np.sum(p[1:] ** 2) / 4
    xstar = np.concatenate([[xi], xs])  # x*_0 = xi, x*_1..x*_{N-1}
    grad = xstar[:-1] - xstar[1:] - h * pint / 2
    return val, grad


def best_affine_by_dual(N, a, b, xi, p0):
    h = 1.0 / N
    res = minimize(lambda q: tuple(-v for v in dual_value(q, N, h, a, b, xi)),
                   p0[1:N], jac=True, method="L-BFGS-B",
                   options={"maxiter": 20000, "maxcor": 50, "ftol": 1e-15, "gtol": 1e-11})
    return -res.fun


def best_affine_by_envelope(N, a, b, xi):
    """Convexified primal: w replaced by its convex envelope on stages t>=1."""
    h = 1.0 / N
    xm = np.sqrt(a / (2 * b))
    wmin = -a * a / (4 * b)

    def wh(x):
        return np.where(np.abs(x) >= xm, w(x, a, b), wmin)

    def dwh(x):
        return np.where(np.abs(x) >= xm, dw(x, a, b), 0.0)

    def f(y):
        x = np.concatenate([[xi], y])
        d = x[1:] - x[:-1]
        val = np.sum(d**2) / h + h * w(xi, a, b) + h * np.sum(wh(x[1:-1]))
        g = np.zeros(N + 1)
        g[1:] += 2 * d / h
        g[:-1] -= 2 * d / h
        g[1:-1] += h * dwh(x[1:-1])
        return val, g[1:]

    res = minimize(f, np.full(N, xi), jac=True, method="L-BFGS-B",
                   options={"maxiter": 50000, "maxcor": 50, "ftol": 1e-15, "gtol": 1e-12})
    return res.fun


def quadratic_certificate(x, u, p, N, a, b, xi, eps=1e-3):
    """Riccati of the comparison LQ problem; returns diagnostics and the bound."""
    h = 1.0 / N
    Q = -2 * a * h - eps * h  # Hessian lower bound of h*w, minus eps*h
    R = 2 * h - eps * h
    P = np.zeros(N + 1)
    P[N] = -eps  # terminal: Phi = 0, so P_N = 0 - eps
    ok = True
    minpiv = np.inf
    for t in range(N - 1, -1, -1):
        piv = R + h * h * P[t + 1]
        minpiv = min(minpiv, piv)
        if piv <= 0:
            ok = False
            break
        P[t] = Q + P[t + 1] - (h * P[t + 1]) ** 2 / piv
    if not ok:
        return {"riccati_ok": False, "failed_at_stage": t, "min_pivot_before_failure": minpiv}
    # stage Hessian lower bounds K_t (unperturbed data): should be >= eps*h*I
    mineig = np.inf
    for t in range(1, N):
        K = np.array([[-2 * a * h + P[t + 1] - P[t], h * P[t + 1]],
                      [h * P[t + 1], 2 * h + h * h * P[t + 1]]])
        mineig = min(mineig, np.linalg.eigvalsh(K)[0] / h)
    # cost-to-go along the trajectory
    stage = h * (u**2 + w(x[:-1], a, b))
    Vbar = np.concatenate([np.cumsum(stage[::-1])[::-1], [0.0]])

    def S(t, y):
        return Vbar[t] + p[t] * (y - x[t]) + 0.5 * P[t] * (y - x[t]) ** 2

    # numerically minimize each stage residual from far starting points
    rng = np.random.default_rng(0)
    total = S(0, xi)  # S_0(xi) = Vbar_0
    worst = 0.0
    # t = 0: only u varies
    for t in range(N):
        def rho(z, t=t):
            xx, uu = (xi, z[0]) if t == 0 else (z[0], z[1])
            return h * (uu**2 + w(xx, a, b)) + S(t + 1, xx + h * uu) - S(t, xx)
        best = np.inf
        for _ in range(3):
            z0 = rng.normal(scale=3.0, size=1 if t == 0 else 2)
            r = minimize(rho, z0, method="BFGS", options={"gtol": 1e-12})
            best = min(best, r.fun)
        worst = min(worst, best)
        total += min(best, 0.0)
    # terminal residual Phi - S_N is the constant -Vbar_N = 0 (p_N = 0, P_N = -eps <= 0 gives >= 0)
    return {"riccati_ok": True, "min_pivot_over_h": minpiv / h,
            "min_stage_hessian_eig_over_h": mineig,
            "most_negative_stage_residual_min": worst,
            "bound": total}


def run(a, N, b=1.0, xi=0.3, do_dual=True):
    h = 1.0 / N
    x0 = xi + (np.sqrt(a / (2 * b)) - xi) * np.linspace(0, 1, N + 1) ** 0.5
    x, u, p, J, kkt = solve_primal(N, a, b, xi, x_init=x0)
    d_star, _ = dual_value(p[1:N], N, h, a, b, xi)
    out = {"a": a, "N": N, "J": J, "kkt_u_residual": kkt,
           "affine_costate_bound": d_star, "affine_costate_gap": J - d_star}
    if do_dual:
        out["best_affine_by_dual"] = best_affine_by_dual(N, a, b, xi, p)
        out["best_affine_by_envelope"] = best_affine_by_envelope(N, a, b, xi)
        out["best_affine_gap"] = J - out["best_affine_by_envelope"]
    q = quadratic_certificate(x, u, p, N, a, b, xi)
    out["quadratic"] = q
    if q.get("riccati_ok"):
        out["quadratic_gap"] = J - q["bound"]
    out["x_end"] = x[-1]
    return out


if __name__ == "__main__":
    results = []
    for a in (2.0, 2.4, 3.0):
        for N in (50, 200, 1000, 5000):
            r = run(a, N, do_dual=(N <= 1000))
            results.append(r)
            print(json.dumps(r))
            sys.stdout.flush()
    with open("logs/doublewell_calibration.json", "w") as fh:
        json.dump(results, fh, indent=1)
