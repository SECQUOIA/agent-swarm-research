"""Round-3 confirmation, refusal check (optional): [V]'s toy with a smooth target.

a(t) = -2 tanh((t - 1)/w), w = 0.05 (C-infinity; a ~ 2 on [0, 0.8], ~ -2 on [1.2, 2]).
Continuous problem: min int_0^2 (x - a)^2/2 + k x u dt, x' = u, |u| <= 1, x(0) = 0, k = -1/2, Phi = 0.
Candidate: u = +1 on [0, tau), -1 on (tau, 2].  Costate psi' = -(x - a + k u), psi(2) = 0,
switching function sigma = k x + psi (u = +1 where sigma < 0).  Checks: one sign change, slope.
Discrete (N = 1000, 4000): own one-switch KKT scan (as in c1), KKT sign violation, and family B's
terminal loss (2 + |xbar_N|)^2 / 4 (stage exactness of family B is algebraic, independent of a).
Float screening only; f* is not certified here.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

K, T, W = -0.5, 2.0, 0.05
a = lambda t: -2.0 * np.tanh((t - 1.0) / W)


def sigma(t, tau):
    x = lambda s: s if s < tau else 2 * tau - s
    u = lambda s: 1.0 if s < tau else -1.0
    # psi(t) = int_t^T (x - a + k u) ds  (psi' = -(x - a + k u), psi(T) = 0)
    pts = [p for p in (tau, 1.0) if t < p < T]
    psi = quad(lambda s: x(s) - a(s) + K * u(s), t, T, points=pts or None, limit=400, epsabs=1e-13)[0]
    return K * x(t) + psi


def switch_eq(tau):
    return sigma(tau, tau)


taus = np.linspace(0.01, 1.99, 199)
vals = [switch_eq(tt) for tt in taus]
roots = [brentq(switch_eq, taus[i], taus[i + 1], xtol=1e-14) for i in range(len(taus) - 1) if vals[i] * vals[i + 1] < 0]
print("candidate switch times:", roots)
for tau in roots:
    ts = np.linspace(0, T, 2001)
    s = np.array([sigma(t, tau) for t in ts])
    pre, post = s[ts < tau - 1e-9], s[ts > tau + 1e-9]
    viol = max(np.maximum(0, pre).max(), np.maximum(0, -post).max())
    ratio = np.min(np.abs(s[np.abs(ts - tau) > 1e-6]) / np.abs(ts[np.abs(ts - tau) > 1e-6] - tau))
    d = 1e-6
    print(f"tau={tau:.6f}  PMP sign violation={viol:.2e}  min |sigma|/|t-tau|={ratio:.3f}  "
          f"sigma_dot(tau)~{(sigma(tau + d, tau) - sigma(tau - d, tau)) / (2 * d):.4f}  x(T)={2 * tau - 2:.5f}")


def disc(N):
    h = T / N
    at = a(np.arange(N + 1) * h)
    best = None
    for m in range(1, N - 1):
        base = np.where(np.arange(N) < m, 1.0, -1.0)
        vals = []
        for v in (-1.0, 0.0, 1.0):
            u = base.copy(); u[m] = v
            x = np.concatenate([[0.0], np.cumsum(h * u)])
            vals.append(h * np.sum((x[:N] - at[:N]) ** 2 / 2 + K * x[:N] * u))
        c2, c1 = (vals[2] + vals[0] - 2 * vals[1]) / 2, (vals[2] - vals[0]) / 2
        v = min(1.0, max(-1.0, -c1 / (2 * c2))) if c2 > 0 else (-1.0 if vals[0] < vals[2] else 1.0)
        u = base.copy(); u[m] = v
        x = np.concatenate([[0.0], np.cumsum(h * u)])
        J = h * np.sum((x[:N] - at[:N]) ** 2 / 2 + K * x[:N] * u)
        if best is None or J < best[0]:
            best = (J, m, v, u, x)
    J, m, v, u, x = best
    p = np.empty(N + 1); p[N] = 0.0
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - at[t] + K * u[t])
    sig = K * x[:N] + p[1:]
    viol = np.where(u > 1 - 1e-12, np.maximum(0, sig), np.where(u < -1 + 1e-12, np.maximum(0, -sig), np.abs(sig)))
    print(f"N={N}: switch stage {m}, u_m={v:.4f}, J={J:.6f}, KKT sign violation={viol.max():.1e}, "
          f"x_N={x[N]:.5f}, family-B terminal loss={(2 + abs(x[N])) ** 2 / 4:.5f}")


for N in (1000, 4000):
    disc(N)
