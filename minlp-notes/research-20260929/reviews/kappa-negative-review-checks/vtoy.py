"""Independent re-implementation (reviewer) of the scalar toys of kappa-negative.md.

Written from the problem statement only (it does not import the author's ktoy.py / lifted.py):
    min  h sum_t [ (x_t - a_t)^2 / 2 + k_t x_t u_t ] + phi1 x_N + phi2 x_N^2 / 2,
    x_{t+1} = x_t + h u_t,  x_0 = x0,  |u_t| <= 1,  h = T / N,
a_t = a(t h), k_t = k(t h) piecewise constant (a(t) = a_i on [t_i, t_{i+1})).
Everything is exact (fractions.Fraction) unless a function name ends in _f.

Calibration family: S_t(x) = p_t x + P_t (x - xa_t)^2 / 2 with the anchor's costates p_t as slopes.
Stage residual rho_t(x, u) = h[(x - a_t)^2/2 + k_t x u] + S_{t+1}(x + h u) - S_t(x).
loss_t = rho_t(anchor) - min over (x, u) in [-R, R] x [lo_t, hi_t] of rho_t.
The minimum is computed by `stage_min_direct` (2-variable box QP by face enumeration, used on small N
to validate) and by the closed form `stage_loss` (valid when beta_t = P_{t+1} + k_t = 0 and
K_t = h + P_{t+1} - P_t >= 0, which is asserted).
"""
from fractions import Fraction as Fr
import itertools

import numpy as np


class Toy:
    def __init__(self, a_pts, k_pts, phi1, phi2, R, T=2, x0=0):
        self.a_pts = [(Fr(t), Fr(v)) for t, v in a_pts]
        self.k_pts = [(Fr(t), Fr(v)) for t, v in k_pts]
        self.phi1, self.phi2, self.R, self.T, self.x0 = Fr(phi1), Fr(phi2), Fr(R), Fr(T), Fr(x0)

    def piece(self, pts, t, N):
        th = Fr(t) * self.T / N
        v = pts[0][1]
        for ti, vi in pts:
            if th >= ti:
                v = vi
        return v

    def data(self, N):
        a = [self.piece(self.a_pts, t, N) for t in range(N)]
        k = [self.piece(self.k_pts, t, N) for t in range(N)]
        return a, k


def traj(toy, N, u):
    """Exact states, cost, costates, switching values."""
    h = toy.T / N
    a, k = toy.data(N)
    x = [toy.x0]
    for t in range(N):
        x.append(x[t] + h * u[t])
    J = sum(h * ((x[t] - a[t]) ** 2 / 2 + k[t] * x[t] * u[t]) for t in range(N))
    J += toy.phi1 * x[N] + toy.phi2 * x[N] ** 2 / 2
    p = [None] * (N + 1)
    p[N] = toy.phi1 + toy.phi2 * x[N]
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + k[t] * u[t])
    sig = [k[t] * x[t] + p[t + 1] for t in range(N)]
    return dict(N=N, h=h, a=a, k=k, u=list(u), x=x, J=J, p=p, sig=sig)


def H_entry(toy, N, k, i, j):
    h = toy.T / N
    m = max(i, j)
    return h * h * (h * (N - 1 - m) + toy.phi2 + (k[m] if i != j else 0))


# ------------------------------------------------------------------ float helpers (search only)
def traj_f(toy, N, u):
    h = float(toy.T) / N
    a, k = toy.data(N)
    a = np.array([float(v) for v in a])
    k = np.array([float(v) for v in k])
    x = float(toy.x0) + np.concatenate([[0.0], np.cumsum(h * u)])
    J = h * np.sum((x[:N] - a) ** 2 / 2 + k * x[:N] * u) + float(toy.phi1) * x[N] + float(toy.phi2) * x[N] ** 2 / 2
    return J


def one_switch(N, m, v, first=1):
    u = [Fr(first)] * m + [Fr(v)] + [Fr(-first)] * (N - m - 1)
    return u


def best_single_switch(toy, N, first=1, mrange=None):
    """Scan switch stage m (u = first before m, u_m = v, -first after), optimize v exactly (1-D quadratic,
    clipped).  Float scan to locate, exact on a neighbourhood.  Returns exact traj of the best."""
    h = float(toy.T) / N
    _, k = toy.data(N)
    best = None
    ms = range(1, N - 1) if mrange is None else mrange
    for m in ms:
        u0 = np.array([float(first)] * m + [0.0] + [-float(first)] * (N - m - 1))
        J0 = traj_f(toy, N, u0)
        u1 = u0.copy(); u1[m] = 1.0
        um = u0.copy(); um[m] = -1.0
        J1, Jm = traj_f(toy, N, u1), traj_f(toy, N, um)
        g = (J1 - Jm) / 2
        Hmm = J1 + Jm - 2 * J0
        cands = [-1.0, 1.0]
        if Hmm > 0:
            cands.append(min(1.0, max(-1.0, -g / Hmm)))
        for v in cands:
            Jv = J0 + g * v + Hmm * v * v / 2
            if best is None or Jv < best[0]:
                best = (Jv, m, v)
    m0 = best[1]
    bestx = None
    for m in range(max(1, m0 - 2), min(N - 1, m0 + 3)):
        E0 = traj(toy, N, one_switch(N, m, 0, first))
        Hmm = H_entry(toy, N, E0["k"], m, m)
        g = E0["h"] * E0["sig"][m]
        cands = [Fr(-1), Fr(1)]
        if Hmm > 0:
            vs = -g / Hmm
            cands.append(min(Fr(1), max(Fr(-1), vs)))
        for v in cands:
            Jv = E0["J"] + g * v + Hmm * v * v / 2
            if bestx is None or Jv < bestx[0]:
                bestx = (Jv, m, v)
    E = traj(toy, N, one_switch(N, bestx[1], bestx[2], first))
    assert E["J"] == bestx[0]
    return E


def kkt_check(E, lo=None, hi=None, fixed=()):
    """Exact KKT sign check; returns (ok, list of fractional stages)."""
    N = E["N"]
    frac = []
    for t in range(N):
        if t in fixed:
            continue
        l = Fr(-1) if lo is None else lo[t]
        r = Fr(1) if hi is None else hi[t]
        u, s = E["u"][t], E["sig"][t]
        if u == r:
            if s > 0:
                return False, t
        elif u == l:
            if s < 0:
                return False, t
        else:
            if not (l < u < r and s == 0):
                return False, t
            frac.append(t)
    return True, frac


# ------------------------------------------------------------------ stage minima
def qmin_interval(c1, c2, lo, hi):
    """min over w in [lo, hi] of c1 w + c2 w^2 (exact)."""
    vals = [c1 * lo + c2 * lo * lo, c1 * hi + c2 * hi * hi]
    if c2 > 0:
        w = -c1 / (2 * c2)
        if lo <= w <= hi:
            vals.append(c1 * w + c2 * w * w)
    return min(vals)


def stage_loss(E, P, t, lo_t, hi_t, R):
    """Closed form, needs beta_t = 0 and K_t >= 0 (asserted) and |x_t| <= R."""
    h, k = E["h"], E["k"]
    assert P[t + 1] + k[t] == 0, "beta != 0"
    K = h + P[t + 1] - P[t]
    assert K >= 0
    assert abs(E["x"][t]) <= R
    s, u = E["sig"][t], E["u"][t]
    m = qmin_interval(h * s, h * h * P[t + 1] / 2, lo_t - u, hi_t - u)
    return -m          # >= 0 since w = 0 is in the interval


def stage_min_direct(toy, E, P, t, lo_t, hi_t):
    """Direct: residual rho_t(x, u) - rho_t(anchor) minimized over the box by face enumeration of the
    2-variable quadratic (computed by evaluating rho_t, no residual formula).  Returns -min (the loss)."""
    h, a, k = E["h"], E["a"], E["k"]
    xb, ub, p = E["x"], E["u"], E["p"]
    R = toy.R

    def S(s, x):
        return p[s] * x + P[s] * (x - xb[s]) ** 2 / 2

    def rho(x, u):
        return h * ((x - a[t]) ** 2 / 2 + k[t] * x * u) + S(t + 1, x + h * u) - S(t, x)
    r0 = rho(xb[t], ub[t])
    # quadratic in (x, u): recover coefficients by exact evaluation
    f = lambda x, u: rho(x, u) - r0
    X0, U0 = xb[t], ub[t]
    c00 = f(X0, U0)
    fx1, fxm = f(X0 + 1, U0), f(X0 - 1, U0)
    fu1, fum = f(X0, U0 + 1), f(X0, U0 - 1)
    gx, gu = (fx1 - fxm) / 2, (fu1 - fum) / 2
    Hxx, Huu = fx1 + fxm - 2 * c00, fu1 + fum - 2 * c00
    Hxu = f(X0 + 1, U0 + 1) - c00 - gx - gu - Hxx / 2 - Huu / 2
    if t == 0:
        lo = [Fr(0), lo_t - U0]; hi = [Fr(0), hi_t - U0]
    else:
        lo = [-R - X0, lo_t - U0]; hi = [R - X0, hi_t - U0]
    g = [gx, gu]
    H = [[Hxx, Hxu], [Hxu, Huu]]
    best = None
    for pat in itertools.product((0, 1, 2), repeat=2):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(2)]
        free = [i for i in range(2) if pat[i] == 2]
        if len(free) == 1:
            i = free[0]; j = 1 - i
            if H[i][i] == 0:
                continue
            z[i] = -(g[i] + H[i][j] * z[j]) / H[i][i]
            if not lo[i] <= z[i] <= hi[i]:
                continue
        elif len(free) == 2:
            det = H[0][0] * H[1][1] - H[0][1] ** 2
            if det == 0:
                continue
            z = [(-g[0] * H[1][1] + H[0][1] * g[1]) / det, (H[0][1] * g[0] - H[0][0] * g[1]) / det]
            if not all(lo[i] <= z[i] <= hi[i] for i in range(2)):
                continue
        val = g[0] * z[0] + g[1] * z[1] + (H[0][0] * z[0] ** 2 + 2 * H[0][1] * z[0] * z[1] + H[1][1] * z[1] ** 2) / 2
        if best is None or val < best:
            best = val
    return -best


def terminal_loss(toy, E, P):
    c = toy.phi2 - P[E["N"]]
    if c >= 0:
        return Fr(0)
    xN = E["x"][E["N"]]
    d = max(abs(-toy.R - xN), abs(toy.R - xN))
    return -c * d * d / 2


def node_bound(toy, E, P, lo, hi):
    """Calibration bound of the node {u_t in [lo_t, hi_t]} with the family anchored at E."""
    N = E["N"]
    losses = [stage_loss(E, P, t, lo[t], hi[t], toy.R) for t in range(N)]
    LN = terminal_loss(toy, E, P)
    return E["J"] - sum(losses) - LN, losses, LN


def coord_refine(toy, E, lo, hi, stages, passes=6):
    """Exact coordinate descent on the given stages (1-D exact quadratic minimization, clipped)."""
    N = E["N"]
    u = list(E["u"])
    for _ in range(passes):
        changed = False
        for j in stages:
            Ej = traj(toy, N, u)
            Hjj = H_entry(toy, N, Ej["k"], j, j)
            g = Ej["h"] * Ej["sig"][j]
            cands = [lo[j], hi[j]]
            if Hjj > 0:
                vs = u[j] - g / Hjj
                cands.append(min(hi[j], max(lo[j], vs)))
            vals = [(g * (c - u[j]) + Hjj * (c - u[j]) ** 2 / 2, c) for c in cands]
            dv, c = min(vals, key=lambda q: q[0])
            if dv < 0:
                u[j] = c
                changed = True
        if not changed:
            break
    return traj(toy, N, u)
