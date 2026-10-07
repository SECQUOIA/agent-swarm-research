"""Independent float screening of Corollary 2.4 / Theorem 2.3 on a toy problem with w != 0.

Continuous problem: min int_0^2 [(x - a(t))^2/2 + k x u] dt (k < 0; for k > 0 the equivalent terminal
cost k x(T)^2/2 forces a second switch near T), xdot = u, |u| <= 1, x(0) = 0,
a = 2 on [0,1), -2 on [1,2]. sigma_0 = k x + psi, so w = -d sigma_0/dx = -k != 0 (non-tangential
costate calibration). The one-switch bang-bang solution never reaches a, so there are no singular arcs.
Since k x u = d/dt (k x^2/2), S = p x - (k/2)(x - xbar)^2 has P b = -k = w: tangential.
Euler transcription with N stages; discrete KKT point by 1-D search over the fractional switch.
Families: A affine S_t = p_t x;  B tangential S_t = p_t x - (k/2)(x - xbar_t)^2.
Stage domain: x in [-t h, t h] (exact reachable set; argv[2] = reach) or [-2, 2] (argv[2] = box), u in [-1, 1]; each stage minimum is exact
(rho is a convex quadratic in x and affine/concave in u). A stage fails if its loss > 1e-12.
Prediction (Lemma 2.2 with Lambda = 1, M_s = 0, Delta = 2, |g| = k): A fails where |sigma| < k^2,
i.e. on a window of duration about 2 k^2 / |sigma_dot(tau)|, sigma_dot = a - x.
"""
import json
import sys

import numpy as np


def solve(N, k, T=2.0):
    h = T / N
    tt = h * np.arange(N + 1)
    a = np.where(tt < 1.0, 2.0, -2.0)

    def traj(s):
        m = int(np.floor(s)); f = s - m
        u = np.where(np.arange(N) < m, 1.0, -1.0)
        if m < N:
            u[m] = f * 1.0 + (1 - f) * (-1.0)
        x = np.concatenate([[0.0], np.cumsum(h * u)])
        J = h * np.sum((x[:N] - a[:N]) ** 2 / 2 + k * x[:N] * u)
        return J, u, x
    ms = np.arange(1, N - 1)
    Jm = [traj(float(m))[0] for m in ms]
    m0 = int(ms[int(np.argmin(Jm))])
    lo, hi = m0 - 1.0, m0 + 1.0
    g = (np.sqrt(5) - 1) / 2
    for _ in range(200):
        c1, c2 = hi - g * (hi - lo), lo + g * (hi - lo)
        if traj(c1)[0] < traj(c2)[0]:
            hi = c2
        else:
            lo = c1
    s = 0.5 * (lo + hi)
    J, u, x = traj(s)
    p = np.zeros(N + 1)
    for t in range(N - 1, -1, -1):
        p[t] = h * ((x[t] - a[t]) + k * u[t]) + p[t + 1]
    return h, tt, a, u, x, p, s, J


def stage_losses(h, tt, a, u, x, p, k, fam, dom):
    N = len(u)
    loss = np.zeros(N)
    for t in range(1, N):
        def rho(X, U):
            val = h * ((X - a[t]) ** 2 / 2 + k * X * U) + p[t + 1] * (X + h * U) - p[t] * X
            if fam == "B":
                val = val - k / 2 * ((X + h * U - x[t + 1]) ** 2 - (X - x[t]) ** 2)
            return val
        best = np.inf
        for U in (-1.0, 1.0):
            # rho is quadratic in X with leading coefficient h/2 (both families)
            c0 = rho(0.0, U); c1 = rho(1.0, U); cm = rho(-1.0, U)
            A2 = (c1 + cm - 2 * c0) / 2; B1 = (c1 - cm) / 2
            R = t * h if dom == "reach" else 2.0
            Xs = np.clip(-B1 / (2 * A2), -R, R)
            best = min(best, rho(Xs, U), rho(-R, U), rho(R, U))
        loss[t] = rho(x[t], u[t]) - best
    return loss


def main():
    k = float(sys.argv[1]) if len(sys.argv) > 1 else -0.5
    dom = sys.argv[2] if len(sys.argv) > 2 else "reach"     # "reach": [-th, th]; "box": [-2, 2]
    out = []
    for N in (500, 1000, 2000, 4000, 8000):
        h, tt, a, u, x, p, s, J = solve(N, k)
        m = int(s)
        sig = k * x[:N] + p[1:]
        tau = h * s
        gam = 2 - x[m]
        sgn_ok = bool(np.all(sig[:m] <= 1e-12) and np.all(sig[m + 1:] >= -1e-12))
        rec = dict(N=N, tau=tau, J=J, kkt_frac=float(sig[m]), kkt_signs_ok=sgn_ok,
                   min_abs_sigma_after_window=float(np.min(np.abs(sig[m + int(0.5 / h):]))),
                   predicted_duration_A=2 * k * k / gam)
        for fam in ("A", "B"):
            L = stage_losses(h, tt, a, u, x, p, k, fam, dom)
            f = np.where(L > 1e-12)[0]
            rec[fam] = dict(fail=int(len(f)), duration=float(len(f) * h),
                            range=[int(f.min() - m), int(f.max() - m)] if len(f) else None,
                            loss=float(L.sum()), min_loss=float(L.min()))
        out.append(rec)
        print(json.dumps(rec), flush=True)
    json.dump(out, open(f"logs/window_toy_k{k}_{dom}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
