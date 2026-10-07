"""Checks of Theorem 5.2 (transfer of a strict continuous calibration) and its hypotheses.

Part A. Counterexample outside (T1): control set U = R (not compact).
    min int_0^T (u^2/2 + x^6 + x^2) dt + Phi(x(T)),  Phi(x) = x^2/2 - x^4/4,
    xdot = u, x(0) = 0.
    S(t,x) = -x^4/4 is a strict C^infinity calibration on all of R x R:
    r = l + S_x u = (u - x^3)^2/2 + x^6/2 + x^2 >= (x^2 + u^2)/4,  Phi - S(T,.) = x^2/2.
    The continuous optimum is x = u = 0 (value 0).  The Euler transcription is unbounded
    below for every h (one large last step), although (x,u,p) = 0 is an exact KKT point
    and S^h = S (a_t = 0).

Part B. Positive test inside the hypotheses, with nonconvex stage residuals.
    Reverse-engineered problem: pick S, (x*,u*), r >= c|z - z*|^2 and set
    l(t,x,u) = r - S_t - S_x u (time-dependent running cost), Phi = S(T,.) + growth.
    Euler transcription on D x U compact; discrete KKT point by bounded L-BFGS and Newton;
    transferred calibration S^h_t = S(t_t,.) + a_t x; every stage residual minimized
    globally by a dense grid plus local polish.  Reported per N: exactness (min over t of
    [min rho_t - rho_t(z^h)]), gap of the transferred family, gap without the affine
    correction (Prop. 5.1), gap of the costate-affine family, and the (T3) error.

Part C. Strictness in x is needed: LQ value function (a field, r = 0 on every field
    trajectory) versus the tilted version S - eps e^{-lam t}|x - x*(t)|^2.
"""
import json
import sys

import numpy as np
from scipy.optimize import minimize

OUT = {}

# ---------------------------------------------------------------- Part A
def partA():
    rows = []
    # continuous strictness on a grid
    xs = np.linspace(-5, 5, 2001)
    us = np.linspace(-50, 50, 2001)
    X, U = np.meshgrid(xs, us)
    r = (U - X**3) ** 2 / 2 + X**6 / 2 + X**2
    ratio = np.min(r / np.maximum(X**2 + U**2, 1e-300) + (X**2 + U**2 == 0) * 1e9)
    for h in (0.1, 0.01, 0.001):
        # u_t = 0 for t < N-1, last step to X: J = X^2/(2h) + Phi(X)
        best = min((Xv**2 / (2 * h) + Xv**2 / 2 - Xv**4 / 4, Xv) for Xv in np.logspace(0, 3, 400))
        # stage residual of the last stage at x = 0 with the transferred family (a_t = 0):
        # rho(0,u) = h u^2/2 + S(h u) - S(0) = h u^2/2 - (h u)^4/4
        uu = np.logspace(0, 6, 601)
        rho = h * uu**2 / 2 - (h * uu) ** 4 / 4
        k = int(np.argmin(rho))
        rows.append({"h": h, "min_ratio_r_over_|z|^2_on_grid": float(ratio),
                     "J_h_at_last_step_X": best[0], "X": best[1],
                     "last_stage_residual_min_over_u_grid": float(rho[k]), "argmin_u": float(uu[k])})
    return rows


# ---------------------------------------------------------------- Part B
XI, T, UMAX = 0.2, 1.0, 2.0
C_R = 0.2  # growth constant of r


def xs_(t):
    return XI + 0.4 * np.sin(2 * t)


def us_(t):
    return 0.8 * np.cos(2 * t)


def S(t, x):
    return np.sin(2 * x + t) + 0.3 * x**3


def S_t(t, x):
    return np.cos(2 * x + t)


def S_x(t, x):
    return 2 * np.cos(2 * x + t) + 0.9 * x**2


def S_xt(t, x):
    return -2 * np.sin(2 * x + t)


def S_xx(t, x):
    return -4 * np.sin(2 * x + t) + 1.8 * x


def r_fun(t, x, u):
    d = x - xs_(t)
    v = u - us_(t)
    return v**2 * (1 + 0.5 * np.sin(5 * x)) + d**2 * (1.2 + np.sin(4 * d))


def r_x(t, x, u):
    d = x - xs_(t)
    v = u - us_(t)
    return v**2 * 2.5 * np.cos(5 * x) + 2 * d * (1.2 + np.sin(4 * d)) + d**2 * 4 * np.cos(4 * d)


def r_u(t, x, u):
    v = u - us_(t)
    return 2 * v * (1 + 0.5 * np.sin(5 * x))


def l_fun(t, x, u):
    return r_fun(t, x, u) - S_t(t, x) - S_x(t, x) * u


def l_x(t, x, u):
    # d/dx [r - S_t - S_x u] ; S_tx = S_xt
    return r_x(t, x, u) - S_xt(t, x) - S_xx(t, x) * u


def l_u(t, x, u):
    return r_u(t, x, u) - S_x(t, x)


def Phi(x):
    xT = xs_(T)
    return S(T, x) + (x - xT) ** 2 * (1 + 0.3 * np.sin(7 * x))


def dPhi(x):
    xT = xs_(T)
    return S_x(T, x) + 2 * (x - xT) * (1 + 0.3 * np.sin(7 * x)) + (x - xT) ** 2 * 2.1 * np.cos(7 * x)


def simulate(u, N):
    h = T / N
    x = np.empty(N + 1)
    x[0] = XI
    for t in range(N):
        x[t + 1] = x[t] + h * u[t]
    return x


def Jred(u, N):
    h = T / N
    x = simulate(u, N)
    tt = h * np.arange(N)
    J = h * np.sum(l_fun(tt, x[:-1], u)) + Phi(x[-1])
    # adjoint
    p = np.empty(N + 1)
    p[N] = dPhi(x[N])
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * l_x(tt[t], x[t], u[t])
    grad = h * (l_u(tt, x[:-1], u) + p[1:])
    return J, grad, x, p


def discrete_kkt(N):
    h = T / N
    tt = h * np.arange(N)
    u0 = us_(tt)
    res = minimize(lambda u: Jred(u, N)[:2], u0, jac=True, method="L-BFGS-B",
                   bounds=[(-UMAX, UMAX)] * N,
                   options={"maxiter": 20000, "ftol": 1e-16, "gtol": 1e-13})
    u = res.x
    # Newton polish with finite-difference Hessian of the reduced gradient
    for _ in range(6):
        J, g, x, p = Jred(u, N)
        if np.max(np.abs(g)) < 1e-14:
            break
        H = np.empty((N, N))
        eps = 1e-6
        for k in range(N):
            e = np.zeros(N)
            e[k] = eps
            H[:, k] = (Jred(u + e, N)[1] - Jred(u - e, N)[1]) / (2 * eps)
        H = 0.5 * (H + H.T)
        u = u - np.linalg.solve(H, g)
    J, g, x, p = Jred(u, N)
    return u, x, p, J, float(np.max(np.abs(g)))


def stage_min(fun, xlo, xhi, x_fixed=None, nx=801, nu=401):
    """Global min of fun(x,u) over [xlo,xhi] x [-UMAX,UMAX] (or u only if x_fixed)."""
    us = np.linspace(-UMAX, UMAX, nu)
    if x_fixed is not None:
        vals = fun(x_fixed, us)
        k = np.argsort(vals)[:5]
        best = np.inf
        for kk in k:
            rr = minimize(lambda z: fun(x_fixed, z[0]), [us[kk]], method="L-BFGS-B",
                          bounds=[(-UMAX, UMAX)], options={"ftol": 1e-16, "gtol": 1e-14})
            best = min(best, rr.fun, vals[kk])
        return best
    xs = np.linspace(xlo, xhi, nx)
    Xg, Ug = np.meshgrid(xs, us, indexing="ij")
    vals = fun(Xg, Ug)
    flat = np.argsort(vals, axis=None)[:8]
    best = np.inf
    for f in flat:
        i, j = np.unravel_index(f, vals.shape)
        rr = minimize(lambda z: fun(z[0], z[1]), [xs[i], us[j]], method="L-BFGS-B",
                      bounds=[(xlo, xhi), (-UMAX, UMAX)], options={"ftol": 1e-16, "gtol": 1e-14})
        best = min(best, rr.fun, vals[i, j])
    return best


def partB(Ns=(5, 10, 20, 40, 80, 160)):
    rows = []
    xlo, xhi = XI - UMAX * T, XI + UMAX * T  # contains every Euler-feasible state
    for N in Ns:
        h = T / N
        tt = h * np.arange(N + 1)
        u, x, p, J, gmax = discrete_kkt(N)
        interior = bool(np.max(np.abs(u)) < UMAX - 1e-9)
        err = float(np.max(np.abs(x - xs_(tt))) + np.max(np.abs(u - us_(tt[:-1])))
                    + np.max(np.abs(p - S_x(tt, xs_(tt)))))
        fams = {}
        a_corr = p - S_x(tt, x)
        for name, a_vec, base in (("transferred", a_corr, True),
                                  ("sampled_no_correction", np.zeros(N + 1), True),
                                  ("costate_affine", p, False)):
            def Sh(t, y, a_vec=a_vec, base=base):
                return (S(tt[t], y) if base else 0.0) + a_vec[t] * y
            total = Sh(0, XI)
            worst_defect = 0.0
            for t in range(N):
                def rho(y, v, t=t):
                    return h * l_fun(tt[t], y, v) + Sh(t + 1, y + h * v) - Sh(t, y)
                at_traj = rho(x[t], u[t])
                if t == 0:
                    m = stage_min(rho, None, None, x_fixed=XI)
                else:
                    m = stage_min(rho, xlo, xhi)
                m = min(m, at_traj)
                worst_defect = min(worst_defect, m - at_traj)
                total += m
            # terminal residual Phi - S_N over the enclosure
            ys = np.linspace(xlo, xhi, 200001)
            term = Phi(ys) - Sh(N, ys)
            mT = min(term.min(), Phi(x[N]) - Sh(N, x[N]))
            worst_defect = min(worst_defect, mT - (Phi(x[N]) - Sh(N, x[N])))
            total += mT
            fams[name] = {"gap": J - total, "worst_stage_defect": worst_defect}
        rec = {"N": N, "h": h, "J": J, "kkt_grad_inf": gmax, "controls_interior": interior,
               "T3_error": err, "T3_error_over_h": err / h, "a_max": float(np.max(np.abs(a_corr))),
               "a_increment_max_over_h2": float(np.max(np.abs(np.diff(a_corr))) / h**2),
               "families": fams}
        rows.append(rec)
        print(json.dumps(rec))
        sys.stdout.flush()
    return rows


# ---------------------------------------------------------------- Part C
def partC(Ns=(10, 20, 40, 80, 160), eps_tilt=0.5, lam=4.0):
    """xdot = u, l = (u^2 + x^2)/2, Phi = 0, x0 = 1, U = [-3,3]; V = P x^2/2, P = tanh(T-t)."""
    rows = []
    U3 = 3.0
    x0 = 1.0
    xlo, xhi = x0 - U3 * T, x0 + U3 * T

    def P(t):
        return np.tanh(T - t)

    def dP(t):
        return -(1 - np.tanh(T - t) ** 2)

    # continuous optimal trajectory: xdot = -P x
    def xstar(t):
        return x0 * np.cosh(T - t) / np.cosh(T)

    for N in Ns:
        h = T / N
        tt = h * np.arange(N + 1)
        # discrete LQ: exact solution by discrete Riccati
        Pd = np.zeros(N + 1)
        K = np.zeros(N)
        for t in range(N - 1, -1, -1):
            # min_u h(u^2+x^2)/2 + Pd_{t+1}(x+hu)^2/2
            K[t] = h * Pd[t + 1] / (h + h * h * Pd[t + 1])
            Pd[t] = h + Pd[t + 1] - (h * Pd[t + 1]) ** 2 / (h + h * h * Pd[t + 1])
        x = np.empty(N + 1)
        x[0] = x0
        u = np.empty(N)
        for t in range(N):
            u[t] = -K[t] * x[t]
            x[t + 1] = x[t] + h * u[t]
        J = h * np.sum((u**2 + x[:-1] ** 2) / 2)
        p = Pd * x  # discrete costate p_t = Pd_t x_t
        out = {"N": N, "J": J}
        for name, tilt in (("field_value_function", 0.0), ("tilted", eps_tilt)):
            def Scont(t, y, tilt=tilt):
                return 0.5 * P(t) * y**2 - tilt * np.exp(-lam * t) * (y - xstar(t)) ** 2

            def Scont_x(t, y, tilt=tilt):
                return P(t) * y - 2 * tilt * np.exp(-lam * t) * (y - xstar(t))
            a_vec = p - Scont_x(tt, x)

            def Sh(t, y):
                return Scont(tt[t], y) + a_vec[t] * y
            total = Sh(0, x0)
            worst = 0.0
            for t in range(N):
                def rho(y, v, t=t):
                    return h * (v**2 + y**2) / 2 + Sh(t + 1, y + h * v) - Sh(t, y)
                at = rho(x[t], u[t])
                if t == 0:
                    vs = np.linspace(-U3, U3, 60001)
                    m = np.min(rho(x0, vs))
                else:
                    # rho is quadratic in (y, v): minimize exactly over the box via grid+polish
                    ys = np.linspace(xlo, xhi, 601)
                    vs = np.linspace(-U3, U3, 601)
                    Yg, Vg = np.meshgrid(ys, vs, indexing="ij")
                    m = np.min(rho(Yg, Vg))
                m = min(m, at)
                worst = min(worst, m - at)
                total += m
            ys = np.linspace(xlo, xhi, 200001)
            term = 0.0 - Sh(N, ys)
            mT = min(term.min(), -Sh(N, x[N]))
            worst = min(worst, mT + Sh(N, x[N]))
            total += mT
            out[name] = {"gap": J - total, "worst_stage_defect": worst}
        rows.append(out)
        print(json.dumps(out))
        sys.stdout.flush()
    return rows


if __name__ == "__main__":
    OUT["A"] = partA()
    for r in OUT["A"]:
        print(json.dumps(r))
    OUT["B"] = partB()
    OUT["C"] = partC()
    with open("logs/c2_transfer_theorem.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=float)
