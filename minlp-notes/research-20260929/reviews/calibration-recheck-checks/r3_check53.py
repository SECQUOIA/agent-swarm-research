"""Third implementation of Check 5.3 (nonconvex transfer example), floating point only.

Differences from the review's c2 (Part B) and the author's revision_checks.py (Part B):
  * the discrete KKT point is found by solving the full KKT system in (u, x, p) with
    scipy.optimize.root (Powell hybrid), started from the sampled continuous solution;
  * stage residuals are minimized on a finer grid (2001 x 1001 on D x U), then polished
    with bounded Powell from the 10 best grid points; the terminal residual on a 400001
    grid plus polish;
  * all derivatives are analytic.
Reports gaps J - B for the transferred family (Theorem 5.2), the uncorrected sampled
family and the costate-affine family, plus max|a_{t+1} - a_t|/h^2 and the (T3) error.
"""
import json
import sys

import numpy as np
from scipy.optimize import minimize, root

XI, T, UMAX = 0.2, 1.0, 2.0
DLO, DHI = XI - UMAX * T, XI + UMAX * T

xst = lambda t: XI + 0.4 * np.sin(2 * t)
ust = lambda t: 0.8 * np.cos(2 * t)
S = lambda t, x: np.sin(2 * x + t) + 0.3 * x**3
S_t = lambda t, x: np.cos(2 * x + t)
S_x = lambda t, x: 2 * np.cos(2 * x + t) + 0.9 * x**2
S_xt = lambda t, x: -2 * np.sin(2 * x + t)
S_xx = lambda t, x: -4 * np.sin(2 * x + t) + 1.8 * x


def r(t, x, u):
    d, v = x - xst(t), u - ust(t)
    return v**2 * (1 + 0.5 * np.sin(5 * x)) + d**2 * (1.2 + np.sin(4 * d))


def r_x(t, x, u):
    d, v = x - xst(t), u - ust(t)
    return 2.5 * v**2 * np.cos(5 * x) + 2 * d * (1.2 + np.sin(4 * d)) + 4 * d**2 * np.cos(4 * d)


def r_u(t, x, u):
    return 2 * (u - ust(t)) * (1 + 0.5 * np.sin(5 * x))


ell = lambda t, x, u: r(t, x, u) - S_t(t, x) - S_x(t, x) * u
ell_x = lambda t, x, u: r_x(t, x, u) - S_xt(t, x) - S_xx(t, x) * u
ell_u = lambda t, x, u: r_u(t, x, u) - S_x(t, x)
XT = xst(T)
Phi = lambda x: S(T, x) + (x - XT) ** 2 * (1 + 0.3 * np.sin(7 * x))
dPhi = lambda x: S_x(T, x) + 2 * (x - XT) * (1 + 0.3 * np.sin(7 * x)) + 2.1 * (x - XT) ** 2 * np.cos(7 * x)


def kkt(N):
    h = T / N
    tt = h * np.arange(N + 1)

    def F(z):
        u, x1, p1 = z[:N], z[N:2 * N], z[2 * N:]
        x = np.concatenate([[XI], x1])
        p = np.concatenate([[np.nan], p1])  # p_1..p_N
        e1 = x[1:] - x[:-1] - h * u                                   # dynamics
        e2 = np.empty(N)
        e2[:-1] = p[1:N] - p[2:] - h * ell_x(tt[1:N], x[1:N], u[1:])   # adjoint t = 1..N-1
        e2[-1] = p[N] - dPhi(x[N])                                     # terminal
        e3 = ell_u(tt[:N], x[:N], u) + p[1:]                           # stationarity in u
        return np.concatenate([e1, e2, e3])

    z0 = np.concatenate([ust(tt[:N]), xst(tt[1:]), S_x(tt[1:], xst(tt[1:]))])
    sol = root(F, z0, method="hybr", options={"xtol": 1e-14})
    u, x1, p1 = sol.x[:N], sol.x[N:2 * N], sol.x[2 * N:]
    x = np.concatenate([[XI], x1])
    p = np.empty(N + 1)
    p[1:] = p1
    p[0] = p[1] + h * ell_x(0.0, XI, u[0])  # adjoint formula continued to t = 0
    J = h * np.sum(ell(tt[:N], x[:N], u)) + Phi(x[N])
    return u, x, p, J, float(np.max(np.abs(F(sol.x)))), bool(sol.success)


def gaps(N, u, x, p, J):
    h = T / N
    tt = h * np.arange(N + 1)
    fam = {"transferred": (True, p - S_x(tt, x)), "uncorrected": (True, np.zeros(N + 1)),
           "costate": (False, p)}
    xg = np.linspace(DLO, DHI, 2001)
    ug = np.linspace(-UMAX, UMAX, 1001)
    Xg, Ug = np.meshgrid(xg, ug, indexing="ij")
    res = {}
    for name, (base, a) in fam.items():
        Sh = lambda k, y: (S(tt[k], y) if base else 0.0) + a[k] * y
        loss = 0.0
        for k in range(N):
            rho = lambda y, w: h * ell(tt[k], y, w) + Sh(k + 1, y + h * w) - Sh(k, y)
            at = rho(x[k], u[k])
            if k == 0:
                vals = rho(XI, ug)
                best = min(vals.min(), at)
                for i in np.argsort(vals)[:10]:
                    rr = minimize(lambda z: rho(XI, z[0]), [ug[i]], method="Powell",
                                  bounds=[(-UMAX, UMAX)], options={"xtol": 1e-12, "ftol": 1e-15})
                    best = min(best, rr.fun)
            else:
                vals = rho(Xg, Ug)
                best = min(vals.min(), at)
                for i in np.argsort(vals, axis=None)[:10]:
                    rr = minimize(lambda z: rho(z[0], z[1]), [Xg.flat[i], Ug.flat[i]], method="Powell",
                                  bounds=[(DLO, DHI), (-UMAX, UMAX)], options={"xtol": 1e-12, "ftol": 1e-15})
                    best = min(best, rr.fun)
            loss += at - best
        rhoN = lambda y: Phi(y) - Sh(N, y)
        yg = np.linspace(DLO, DHI, 400001)
        vals = rhoN(yg)
        atN = rhoN(x[N])
        best = min(vals.min(), atN)
        for i in np.argsort(vals)[:5]:
            rr = minimize(lambda z: rhoN(z[0]), [yg[i]], method="Powell", bounds=[(DLO, DHI)],
                          options={"xtol": 1e-12, "ftol": 1e-15})
            best = min(best, rr.fun)
        loss += atN - best
        res[name] = loss
    a = p - S_x(tt, x)
    return res, float(np.max(np.abs(np.diff(a[1:]))) / h**2)


rows = []
for N in (10, 20, 40, 80):
    u, x, p, J, kres, ok = kkt(N)
    h = T / N
    tt = h * np.arange(N + 1)
    e_h = float(np.max(np.abs(x - xst(tt))) + np.max(np.abs(u - ust(tt[:N])))
                + np.max(np.abs(p[1:] - S_x(tt[1:], xst(tt[1:])))))
    g, da = gaps(N, u, x, p, J)
    rec = {"N": N, "J": J, "kkt_residual": kres, "root_success": ok,
           "controls_interior": bool(np.max(np.abs(u)) < UMAX), "T3_error_over_h": e_h / h,
           "max_a_increment_over_h2_t>=1": da, "gap_transferred": g["transferred"],
           "gap_uncorrected": g["uncorrected"], "gap_costate": g["costate"]}
    rows.append(rec)
    print(json.dumps(rec))
    sys.stdout.flush()
with open("logs/r3_check53.json", "w") as fh:
    json.dump(rows, fh, indent=1)
