"""Scalar bang-bang toy for window-exactness.md.

Continuous problem:  min int_0^T [ (x - a(t))^2 / 2 + k x u ] dt + Phi(x(T)),
                     x' = u, |u| <= 1, x(0) = x0,  a = a1 on [0, tj), a2 on [tj, T],
                     Phi(x) = phi1 x + phi2 x^2 / 2.
sigma_0 = k x + psi, so w = -k, b = 1 and the switch self-curvature is kappa_tau = b w = -k.

Euler transcription (N stages, h = T/N):
    min h sum_t [ (x_t - a_t)^2 / 2 + k x_t u_t ] + Phi(x_N),  x_{t+1} = x_t + h u_t,  a_t = a(t h).
Quadratic calibration families S_t(x) = p_t x + P_t (x - xbar_t)^2 / 2 (p_t discrete costates).
In d = x - xbar_t, om = u - ubar_t the stage residual is exactly
    rho_t - rho_t(zbar) = g_t d + h sig_t om + K_t d^2 / 2 + h beta_t d om + h^2 kap_t om^2 / 2,
    K_t = h + P_{t+1} - P_t,  beta_t = P_{t+1} + k,  kap_t = P_{t+1},  g_t = 0 (discrete adjoint).
Everything here works for float or fractions.Fraction data (exact mode).
"""
from dataclasses import dataclass
from fractions import Fraction as Fr
import functools
import itertools

import numpy as np


@dataclass(frozen=True)
class Toy:
    k: float
    x0: float = 0.0
    T: float = 2.0
    a1: float = 2.0
    a2: float = -2.0
    tj: float = 1.0
    phi1: float = 0.0
    phi2: float = 0.0
    R: float = 2.0          # state box |x| <= R used as the stage domain D_t

    def a_of(self, N):
        return _a_of(self, N).copy()


@functools.lru_cache(maxsize=64)
def _a_of(toy, N):
    # a_t = a(t h), decided exactly: t h < tj  <=>  t T < tj N (T, tj are dyadic floats)
    tj, T = Fr(toy.tj), Fr(toy.T)
    return np.array([toy.a1 if Fr(t) * T < tj * N else toy.a2 for t in range(N + 1)])


VERIFIER = Toy(k=-0.5)                                   # reviews/bangbang-verification toy, kappa_tau = +0.5
TOYPLUS = Toy(k=0.5, a2=-1.0, phi1=1.0)                  # kappa_tau = -0.5 (counterexample)
TOYZERO = Toy(k=0.0, a2=-1.0, phi1=1.0, phi2=0.5)        # kappa_tau = 0 (degenerate case)


def simulate(toy, N, u):
    h = toy.T / N
    a = toy.a_of(N)
    x = toy.x0 + np.concatenate([[0.0], np.cumsum(h * u)])
    J = h * np.sum((x[:N] - a[:N]) ** 2 / 2 + toy.k * x[:N] * u) + toy.phi1 * x[N] + toy.phi2 * x[N] ** 2 / 2
    return x, J


def adjoint(toy, N, x, u):
    h = toy.T / N
    a = toy.a_of(N)
    pN = toy.phi1 + toy.phi2 * x[N]
    inc = h * (x[:N] - a[:N] + toy.k * u)
    p = np.empty(N + 1)
    p[N] = pN
    p[:N] = pN + np.cumsum(inc[::-1])[::-1]
    sig = toy.k * x[:N] + p[1:]
    return p, sig


def hessian(toy, N, idx):
    """Exact Hessian block d^2 J / du_i du_j, i, j in idx (J is an exact quadratic in u):
    H_ij = h^2 [ h (N - 1 - max(i, j)) + phi2 + k (1 - delta_ij) ]."""
    h = toy.T / N
    idx = np.asarray(idx)
    mx = np.maximum.outer(idx, idx)
    return h * h * (h * (N - 1 - mx) + toy.phi2 + toy.k * (1 - np.eye(len(idx))))


def kkt(toy, N, maxit=60):
    """One-switch KKT point (+1 then -1): best switch stage m with the 1-D optimal control at m,
    then an active-set Newton refinement with the exact Hessian (handles two adjacent interior
    controls).  Returns a dict; kkt_viol is the largest sign violation."""
    h = toy.T / N
    best = None
    for m in range(1, N - 1):
        u = np.where(np.arange(N) < m, 1.0, -1.0)
        x, _ = simulate(toy, N, u)
        _, sig = adjoint(toy, N, x, u)
        # J restricted to u_m is quadratic: slope h sig_m at u_m = -1, curvature H_mm
        Hmm = hessian(toy, N, [m])[0, 0]
        um = -1.0 - h * sig[m] / Hmm if Hmm > 0 else -1.0
        um = min(1.0, max(-1.0, um))
        u[m] = um
        _, J = simulate(toy, N, u)
        if best is None or J < best[0]:
            best = (J, m, u.copy())
    u = best[2]
    for it in range(maxit):
        x, J = simulate(toy, N, u)
        p, sig = adjoint(toy, N, x, u)
        inter = np.where(np.abs(u) < 1 - 1e-15)[0]
        viol = np.where(((u >= 1 - 1e-15) & (sig > 1e-15)) | ((u <= -1 + 1e-15) & (sig < -1e-15)))[0]
        F = np.union1d(inter, viol)
        if len(viol) == 0 and (len(inter) == 0 or np.abs(sig[inter]).max() < 1e-15):
            break
        step = np.linalg.solve(hessian(toy, N, F), -h * sig[F])
        u[F] = np.clip(u[F] + step, -1.0, 1.0)
    x, J = simulate(toy, N, u)
    p, sig = adjoint(toy, N, x, u)
    inter = [int(t) for t in np.where(np.abs(u) < 1 - 1e-12)[0]]
    sgn = np.where(u > 1 - 1e-12, np.maximum(0, sig), np.where(u < -1 + 1e-12, np.maximum(0, -sig), np.abs(sig)))
    s = inter[0] if inter else int(np.where(u < 0)[0][0])
    return dict(N=N, h=h, u=u, x=x, p=p, sig=sig, J=J, s=s, frac=inter, kkt_viol=float(sgn.max()), iters=it)


# ---------------------------------------------------------------- families (arrays P_0..P_N)
def fam_const(N, val):
    return np.full(N + 1, float(val))


def fam_fun(toy, N, Pfun):
    h = toy.T / N
    return np.array([Pfun(t * h) for t in range(N + 1)])


def fam_rmax(toy, kk, eps=0.0, PN=None):
    """Discrete maximal recursion (extension-n2.md, Lemma 10), scalar case, Delta = 2:
    P_t = h + P_{t+1} - 2 h eps - beta_t^2 / m_t, m_t = |sig_t| / h + P_{t+1}, beta_t = P_{t+1} + k
    (sig_t := 0 at interior stages).  Returns P and the break stage (m_t <= 0) or None."""
    N, h, sig = kk["N"], kk["h"], kk["sig"]
    P = np.full(N + 1, np.nan)
    P[N] = toy.phi2 - 2 * eps if PN is None else PN
    for t in range(N - 1, -1, -1):
        beta = P[t + 1] + toy.k
        s = 0.0 if t in kk["frac"] else abs(sig[t])
        m = s / h + P[t + 1]
        if m <= 0:
            return P, t
        P[t] = h + P[t + 1] - 2 * h * eps - beta * beta / m
    return P, None


# ---------------------------------------------------------------- exact data
def exact_traj(toy, N, u):
    h = Fr(toy.T) / N
    a = [Fr(float(v)) for v in toy.a_of(N)]
    uf = [v if isinstance(v, Fr) else Fr(float(v)) for v in u]
    x = [Fr(toy.x0)]
    for t in range(N):
        x.append(x[-1] + h * uf[t])
    k = Fr(toy.k)
    J = sum(h * ((x[t] - a[t]) ** 2 / 2 + k * x[t] * uf[t]) for t in range(N)) \
        + Fr(toy.phi1) * x[N] + Fr(toy.phi2) * x[N] ** 2 / 2
    p = [None] * (N + 1)
    p[N] = Fr(toy.phi1) + Fr(toy.phi2) * x[N]
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + k * uf[t])
    sig = [k * x[t] + p[t + 1] for t in range(N)]
    return dict(h=h, a=a, u=uf, x=x, p=p, sig=sig, J=J, N=N)


# ---------------------------------------------------------------- box QP minimum (face enumeration)
def _solve(A, b):
    """Gaussian elimination (works for Fraction or float); returns None if singular."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = None
        for r in range(c, n):
            if M[r][c] != 0:
                if piv is None or abs(M[r][c]) > abs(M[piv][c]):
                    piv = r
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def box_qp_min(g, H, lo, hi, exact=False):
    """min g.z + z^T H z / 2 over lo <= z <= hi by enumerating faces (relative-interior
    stationary points of every face; the global minimum of a quadratic over a box is attained at
    such a point, possibly of a smaller face when the free block is singular).  Returns (value, z)."""
    n = len(g)
    zero = Fr(0) if exact else 0.0
    best, bz = None, None
    for pat in itertools.product((0, 1, 2), repeat=n):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(n)]
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fixed = [i for i in range(n) if pat[i] != 2]
            A = [[H[i][j] for j in free] for i in free]
            b = [-(g[i] + sum((H[i][j] * z[j] for j in fixed), zero)) for i in free]
            sol = _solve(A, b)
            if sol is None:
                continue
            ok = all(lo[i] <= v <= hi[i] for i, v in zip(free, sol))
            if not ok:
                continue
            for i, v in zip(free, sol):
                z[i] = v
        val = sum((g[i] * z[i] for i in range(n)), zero) + sum((H[i][j] * z[i] * z[j] for i in range(n) for j in range(n)), zero) / 2
        if best is None or val < best:
            best, bz = val, z
    return best, bz


# ---------------------------------------------------------------- stage and window problems
def stage_quad(toy, D, P, t, exact=False):
    """(g, H, lo, hi) of rho_t - rho_t(zbar) in z = (d, om) over D_t x U, D_t = [-R, R]."""
    F = Fr if exact else float
    h, x, u, p, sig, a = D["h"], D["x"], D["u"], D["p"], D["sig"], D["a"]
    k = F(toy.k)
    Pt, Pn = F(P[t]), F(P[t + 1])
    gd = h * (x[t] - a[t] + k * u[t]) + p[t + 1] - p[t]
    g = [gd, h * sig[t]]
    H = [[h + Pn - Pt, h * (Pn + k)], [h * (Pn + k), h * h * Pn]]
    R = F(toy.R)
    if t == 0:
        lo, hi = [F(0), -1 - u[0]], [F(0), 1 - u[0]]
    else:
        lo, hi = [-R - x[t], -1 - u[t]], [R - x[t], 1 - u[t]]
    return g, H, lo, hi


def stage_losses(toy, D, P, exact=False, stages=None):
    N = D["N"]
    out = {}
    for t in (range(N) if stages is None else stages):
        g, H, lo, hi = stage_quad(toy, D, P, t, exact)
        v, _ = box_qp_min(g, H, lo, hi, exact)
        out[t] = -v
    return out


def terminal_loss(toy, D, P, exact=False):
    F = Fr if exact else float
    N, x, p = D["N"], D["x"], D["p"]
    R = F(toy.R)
    g = [F(toy.phi1) + F(toy.phi2) * x[N] - p[N]]
    H = [[F(toy.phi2) - F(P[N])]]
    v, _ = box_qp_min(g, H, [-R - x[N]], [R - x[N]], exact)
    return -v


def window_quad(toy, D, P, a, b, exact=False):
    """Window objective J_W(x_a, u_a..u_{b-1}) - J_W(zbar) = g.v + v^T H v / 2 in
    v = (d_a, om_a, ..., om_{b-1}); entry domain D_a = [-R, R] (the whole state box), controls in U.
    J_W = sum_{t=a}^{b-1} h[(x_t - a_t)^2/2 + k x_t u_t] + S_b(x_b) - S_a(x_a)."""
    F = Fr if exact else float
    h, x, u, p, at = D["h"], D["x"], D["u"], D["p"], D["a"]
    k = F(toy.k)
    K = b - a
    n = 1 + K
    zero = F(0)
    g = [zero] * n
    H = [[zero] * n for _ in range(n)]

    def e(t):  # x_t = xbar_t + e(t).v
        v = [zero] * n
        v[0] = F(1)
        for j in range(a, t):
            v[1 + j - a] = h
        return v

    def addg(vec, c):
        for i in range(n):
            if vec[i] != 0:
                g[i] += c * vec[i]

    def addH(v1, v2, c):
        for i in range(n):
            if v1[i] == 0:
                continue
            for j in range(n):
                if v2[j] != 0:
                    H[i][j] += c * v1[i] * v2[j]
    for t in range(a, b):
        et = e(t)
        ft = [zero] * n
        ft[1 + t - a] = F(1)
        addg(et, h * (x[t] - at[t]))
        addH(et, et, h)
        addg(et, h * k * u[t])
        addg(ft, h * k * x[t])
        addH(et, ft, h * k)
        addH(ft, et, h * k)
    eb = e(b)
    addg(eb, p[b])
    addH(eb, eb, F(P[b]))
    ea = e(a)
    addg(ea, -p[a])
    addH(ea, ea, -F(P[a]))
    R = F(toy.R)
    lo = [(-R - x[a]) if a > 0 else zero] + [-1 - u[t] for t in range(a, b)]
    hi = [(R - x[a]) if a > 0 else zero] + [1 - u[t] for t in range(a, b)]
    return g, H, lo, hi


def window_value(toy, D, P, a, b, exact=False):
    g, H, lo, hi = window_quad(toy, D, P, a, b, exact)
    v, z = box_qp_min(g, H, lo, hi, exact)
    return v, z


def float_data(toy, kk):
    return dict(N=kk["N"], h=kk["h"], x=kk["x"], u=kk["u"], p=kk["p"], sig=kk["sig"], a=toy.a_of(kk["N"]))


def exact_kkt_traj(toy, N, u):
    """Rational KKT point: the float controls as rationals, with the single interior control (if any)
    corrected by one exact Newton step so that sigma_n = 0 exactly (sigma_n is affine in u_n with slope
    h (h (N - 1 - n) + phi2)).  Asserts the exact KKT sign conditions."""
    uf = [Fr(float(v)) for v in u]
    E = exact_traj(toy, N, uf)
    inter = [t for t in range(N) if -1 < uf[t] < 1]
    assert len(inter) <= 1, inter
    if inter:
        n = inter[0]
        h = E["h"]
        uf[n] -= E["sig"][n] / (h * (h * (N - 1 - n) + Fr(toy.phi2)))
        assert -1 < uf[n] < 1
        E = exact_traj(toy, N, uf)
        assert E["sig"][n] == 0
    for t in range(N):
        if uf[t] == 1:
            assert E["sig"][t] <= 0, t
        elif uf[t] == -1:
            assert E["sig"][t] >= 0, t
    E["interior"] = inter
    return E
