"""End-to-end check: transferred field (non-strict) calibration vs tilted (strict) one.

Scalar LQ xdot = alpha x + u, l = (u^2 + q x^2)/2, Phi = phiT x^2/2, x0 = 1, T = 1,
U = [-Umax, Umax], D = enclosure of all Euler-feasible states.  Continuous value function
V = P(t) x^2/2 (field calibration, r = (u + P x)^2/2, not strict in x).  Tilted:
S = V - eps e^{-lam t} (x - x*(t))^2 (strict).  Transferred families
S^h_t = S(t_t,.) + a_t x with a_t = p^h_t - S_x(t_t, x^h_t).
Stage residuals are quadratics in (x,u); minimized exactly over the box by checking the
interior stationary point and the four edges (1-D quadratics) and corners.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp


def box_min_quadratic(f, xlo, xhi, ulo, uhi):
    # f is a quadratic in (x,u); recover coefficients by evaluation
    f00 = f(0.0, 0.0)
    fx = (f(1.0, 0.0) - f(-1.0, 0.0)) / 2
    fu = (f(0.0, 1.0) - f(0.0, -1.0)) / 2
    fxx = f(1.0, 0.0) + f(-1.0, 0.0) - 2 * f00
    fuu = f(0.0, 1.0) + f(0.0, -1.0) - 2 * f00
    fxu = (f(1.0, 1.0) - f(1.0, -1.0) - f(-1.0, 1.0) + f(-1.0, -1.0)) / 4
    cand = [f(x, u) for x in (xlo, xhi) for u in (ulo, uhi)]
    H = np.array([[fxx, fxu], [fxu, fuu]])
    g = np.array([fx, fu])
    if abs(np.linalg.det(H)) > 1e-300:
        z = np.linalg.solve(H, -g)
        if xlo <= z[0] <= xhi and ulo <= z[1] <= uhi:
            cand.append(f(z[0], z[1]))
    for x in (xlo, xhi):
        if fuu > 0:
            u = -(fu + fxu * x) / fuu
            if ulo <= u <= uhi:
                cand.append(f(x, u))
    for u in (ulo, uhi):
        if fxx > 0:
            x = -(fx + fxu * u) / fxx
            if xlo <= x <= xhi:
                cand.append(f(x, u))
    return min(cand)


def run(alpha, q, phiT, Umax=5.0, eps=0.5, lam=8.0, Ns=(10, 20, 40, 80, 160, 320)):
    T, x0 = 1.0, 1.0
    solP = solve_ivp(lambda t, P: -(q + 2 * alpha * P - P**2), [T, 0.0], [phiT],
                     rtol=1e-12, atol=1e-14, dense_output=True)
    P = lambda t: solP.sol(t)[0]
    solx = solve_ivp(lambda t, x: (alpha - P(t)) * x, [0.0, T], [x0], rtol=1e-12, atol=1e-14,
                     dense_output=True)
    xstar = lambda t: solx.sol(t)[0]
    out = []
    for N in Ns:
        h = T / N
        tt = h * np.arange(N + 1)
        A = 1 + h * alpha
        Pd = np.zeros(N + 1)
        Pd[N] = phiT
        K = np.zeros(N)
        for t in range(N - 1, -1, -1):
            den = h + h * h * Pd[t + 1]
            K[t] = h * A * Pd[t + 1] / den
            Pd[t] = h * q + A * A * Pd[t + 1] - (h * A * Pd[t + 1]) ** 2 / den
        x = np.empty(N + 1); x[0] = x0; u = np.empty(N)
        for t in range(N):
            u[t] = -K[t] * x[t]
            x[t + 1] = A * x[t] + h * u[t]
        assert np.max(np.abs(u)) < Umax
        J = h * np.sum((u**2 + q * x[:-1] ** 2) / 2) + phiT * x[N] ** 2 / 2
        p = Pd * x
        # enclosure of Euler-feasible states (interval propagation)
        lo = np.empty(N + 1); hi = np.empty(N + 1); lo[0] = hi[0] = x0
        for t in range(N):
            c = [A * lo[t], A * hi[t]]
            lo[t + 1] = min(c) - h * Umax; hi[t + 1] = max(c) + h * Umax
        rec = {"N": N, "J": J}
        for name, tilt in (("field", 0.0), ("tilted", eps)):
            S = lambda t, y, tilt=tilt: 0.5 * P(t) * y**2 - tilt * np.exp(-lam * t) * (y - xstar(t)) ** 2
            Sx = lambda t, y, tilt=tilt: P(t) * y - 2 * tilt * np.exp(-lam * t) * (y - xstar(t))
            a = p - np.array([Sx(tt[t], x[t]) for t in range(N + 1)])
            Sh = lambda t, y: S(tt[t], y) + a[t] * y
            total = Sh(0, x0); worst = 0.0
            for t in range(N):
                rho = lambda y, v, t=t: h * (v**2 + q * y**2) / 2 + Sh(t + 1, A * y + h * v) - Sh(t, y)
                at = rho(x[t], u[t])
                if t == 0:
                    m = box_min_quadratic(rho, x0, x0, -Umax, Umax)
                else:
                    m = box_min_quadratic(rho, lo[t], hi[t], -Umax, Umax)
                m = min(m, at); worst = min(worst, m - at); total += m
            term = lambda y, v: phiT * y**2 / 2 - Sh(N, y)
            mT = min(box_min_quadratic(term, lo[N], hi[N], 0.0, 0.0), term(x[N], 0))
            worst = min(worst, mT - term(x[N], 0)); total += mT
            rec[name + "_gap"] = J - total
            rec[name + "_worst_stage_defect"] = worst
        out.append(rec)
    return out


rows = []
for alpha, q, phiT in [(-2.0, 0.0, 1.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0)]:
    res = run(alpha, q, phiT)
    for r in res:
        r.update({"alpha": alpha, "q": q, "phiT": phiT})
        print(json.dumps(r))
    rows += res
json.dump(rows, open("logs/c4_nonstrict_lq_gap.json", "w"), indent=1)
