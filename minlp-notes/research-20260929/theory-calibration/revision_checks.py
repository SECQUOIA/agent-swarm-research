"""Independent checks of the review's main claims (floating point, not certified).

Written by the note's author, separately from the reviewer's scripts in
reviews/calibration-review-checks/.  Parts:

A. Compactness counterexample (review F11): U = R, S = -x^4/4 strict, but the
   Euler transcription is unbounded below for every h.
B. Transfer example (review Part B, re-implemented): nonconvex strict exact
   calibration S = sin(2x+t) + 0.3x^3; compare transferred, uncorrected and
   costate-affine families, stage residuals minimized on a dense grid plus
   bounded local polish.
C. Theorem 3.5 = convexity of the condensed problem (review F8): critical a at
   which the unperturbed comparison Riccati recursion fails versus the critical a
   at which the reduced-Hessian lower bound loses definiteness (double well, N=50).
"""

import json

import numpy as np
from scipy.optimize import brentq, minimize

out = {}

# ------------------------------------------------------------------ Part A
rowsA = []
for h in (0.1, 0.01, 0.001):
    # x_0 = ... = x_{N-1} = 0 (u = 0), last step jumps to X: cost h*(u^2/2) + Phi(X),
    # running terms x^6 + x^2 are evaluated at x_{N-1} = 0 (explicit Euler).
    X = 1000.0
    cost = h * (X / h) ** 2 / 2 + X**2 / 2 - X**4 / 4
    rowsA.append({"h": h, "objective_of_jump_point": cost})
# strictness of r = (u - x^3)^2/2 + x^6/2 + x^2 against (x^2+u^2)/4 on a grid
xs = np.linspace(-3, 3, 1201)
us = np.linspace(-30, 30, 1201)
XX, UU = np.meshgrid(xs, us)
r = (UU - XX**3) ** 2 / 2 + XX**6 / 2 + XX**2
ratio = np.min(np.where(XX**2 + UU**2 > 0, r / np.maximum(XX**2 + UU**2, 1e-300), np.inf))
out["A"] = {"rows": rowsA, "min_r_over_norm2_on_grid": float(ratio)}
print("A", json.dumps(out["A"]))

# ------------------------------------------------------------------ Part B
XI, T, UMAX = 0.2, 1.0, 2.0
DLO, DHI = XI - UMAX * T, XI + UMAX * T  # state enclosure


def xst(t):
    return XI + 0.4 * np.sin(2 * t)


def ust(t):
    return 0.8 * np.cos(2 * t)


def S(t, x):
    return np.sin(2 * x + t) + 0.3 * x**3


def Sx(t, x):
    return 2 * np.cos(2 * x + t) + 0.9 * x**2


def St(t, x):
    return np.cos(2 * x + t)


def r(t, x, u):
    d, v = x - xst(t), u - ust(t)
    return v**2 * (1 + 0.5 * np.sin(5 * x)) + d**2 * (1.2 + np.sin(4 * d))


def ell(t, x, u):
    return r(t, x, u) - St(t, x) - Sx(t, x) * u


def Phi(x):
    return S(T, x) + (x - xst(T)) ** 2 * (1 + 0.3 * np.sin(7 * x))


def num_dx(f, x, eps=1e-6):
    return (f(x + eps) - f(x - eps)) / (2 * eps)


def solve_discrete(N):
    h = T / N
    tt = h * np.arange(N)

    def J_and_grad(u):
        x = np.empty(N + 1)
        x[0] = XI
        for k in range(N):
            x[k + 1] = x[k] + h * u[k]
        J = h * np.sum(ell(tt, x[:-1], u)) + Phi(x[-1])
        # adjoint: p_N = Phi'(x_N), p_k = p_{k+1} + h ell_x(t_k, x_k, u_k)
        p = np.empty(N + 1)
        p[N] = num_dx(Phi, x[N])
        lx = num_dx(lambda z: ell(tt, z, u), x[:-1])
        for k in range(N - 1, 0, -1):
            p[k] = p[k + 1] + h * lx[k]
        p[0] = p[1] + h * lx[0]
        lu = num_dx(lambda w: ell(tt, x[:-1], w), u)
        g = h * lu + h * p[1:]
        return J, g, x, p

    res = minimize(lambda u: J_and_grad(u)[:2], ust(tt), jac=True, method="L-BFGS-B",
                   bounds=[(-UMAX, UMAX)] * N,
                   options={"ftol": 1e-16, "gtol": 1e-13, "maxiter": 20000})
    J, g, x, p = J_and_grad(res.x)
    return res.x, x, p, J, float(np.max(np.abs(g)))


def family_bound(N, u, x, p, kind):
    h = T / N
    tt = h * np.arange(N + 1)
    if kind == "transferred":
        a = p - Sx(tt, x)
        Sh = lambda k, y: S(tt[k], y) + a[k] * y
    elif kind == "uncorrected":
        Sh = lambda k, y: S(tt[k], y)
    else:  # costate affine
        Sh = lambda k, y: p[k] * y
    xg = np.linspace(DLO, DHI, 1601)
    ug = np.linspace(-UMAX, UMAX, 801)
    X, Uu = np.meshgrid(xg, ug, indexing="ij")
    total = Sh(0, XI)
    worst = 0.0
    for k in range(N):
        def rho(z, k=k):
            y, w = (XI, z[0]) if k == 0 else (z[0], z[1])
            return h * ell(tt[k], y, w) + Sh(k + 1, y + h * w) - Sh(k, y)
        traj = rho([u[0]]) if k == 0 else rho([x[k], u[k]])
        if k == 0:
            vals = rho([ug])
            starts = [[ug[i]] for i in np.argsort(vals)[:5]]
            bnds = [(-UMAX, UMAX)]
        else:
            vals = h * ell(tt[k], X, Uu) + Sh(k + 1, X + h * Uu) - Sh(k, X)
            idx = np.argsort(vals, axis=None)[:5]
            starts = [[X.flat[i], Uu.flat[i]] for i in idx]
            bnds = [(DLO, DHI), (-UMAX, UMAX)]
        best = min(np.min(vals), traj)
        for z0 in starts:
            rr = minimize(rho, z0, method="L-BFGS-B", bounds=bnds, options={"ftol": 1e-15, "gtol": 1e-12})
            best = min(best, rr.fun)
        total += best
        worst = min(worst, best - traj)
    # terminal residual Phi - S_N over D
    rhoN = lambda y: Phi(y) - Sh(N, y)
    vals = rhoN(xg)
    best = min(np.min(vals), rhoN(x[N]))
    for i in np.argsort(vals)[:5]:
        rr = minimize(lambda z: rhoN(z[0]), [xg[i]], method="L-BFGS-B", bounds=[(DLO, DHI)])
        best = min(best, rr.fun)
    worst = min(worst, best - rhoN(x[N]))
    total += best
    return total, worst


rowsB = []
for N in (10, 20, 40, 80):
    u, x, p, J, kkt = solve_discrete(N)
    row = {"N": N, "J": J, "proj_grad_inf": kkt,
           "controls_interior": bool(np.all(np.abs(u) < UMAX - 1e-9)),
           "max_state_err": float(np.max(np.abs(x - xst(T / N * np.arange(N + 1)))))}
    for kind in ("transferred", "uncorrected", "costate"):
        B, worst = family_bound(N, u, x, p, kind)
        row[kind + "_gap"] = J - B
        row[kind + "_worst_stage_defect"] = worst
    rowsB.append(row)
    print("B", json.dumps(row))
out["B"] = rowsB

# ------------------------------------------------------------------ Part C
N, b = 50, 1.0
h = 1.0 / N


def riccati_ok(a):
    P = 0.0  # P_N = 0
    for t in range(N - 1, -1, -1):
        piv = 2 * h + h * h * P
        if piv <= 0:
            return -1.0
        P = -2 * a * h + P - (h * P) ** 2 / piv
    return 1.0


def reduced_min_eig(a):
    # controls u_0..u_{N-1}; x_t = x_0 + h sum_{s<t} u_s, t = 1..N-1 carry curvature -2a h
    L = h * np.tril(np.ones((N - 1, N)), 0)  # x_t (t=1..N-1) as function of u
    Hm = 2 * h * np.eye(N) + L.T @ (-2 * a * h * np.eye(N - 1)) @ L
    return np.linalg.eigvalsh(Hm)[0]


lo, hi = 2.0, 3.0
for _ in range(60):
    mid = (lo + hi) / 2
    if riccati_ok(mid) > 0:
        lo = mid
    else:
        hi = mid
a_ric = lo
a_hess = brentq(reduced_min_eig, 2.0, 3.0, xtol=1e-13)
out["C"] = {"N": N, "critical_a_riccati": a_ric, "critical_a_reduced_hessian": a_hess,
            "pi2_over_4": np.pi**2 / 4}
print("C", json.dumps(out["C"]))

with open("logs/revision_checks.json", "w") as fh:
    json.dump(out, fh, indent=1)
