"""Independent re-implementation (reviewer) of the scalar toys of window-exactness.md, Section 7.

Written without importing or copying theory-bangbang/window/*.py.  Everything is built from the
problem definition by direct simulation:

  min  sum_{t<N} h [ (x_t - a_t)^2 / 2 + k x_t u_t ] + phi1 x_N + phi2 x_N^2 / 2,
  x_{t+1} = x_t + h u_t, x_0 = 0, |u_t| <= 1, a_t = 2 if t h < 1 else a2, h = 2 / N.

Quadratic coefficients of stage residuals and window objectives are extracted by exact polarization
(evaluating the function itself at a few points), not from closed-form coefficient formulas.
Box-QP minima are computed by enumerating faces (a face is used only if its free Hessian block is
positive definite; otherwise a minimizer also lies on a smaller face).
"""
from fractions import Fraction as Fr
import itertools
import math

import numpy as np


class Toy:
    def __init__(self, name, k, a2, phi1, phi2):
        self.name, self.k, self.a2, self.phi1, self.phi2 = name, k, a2, phi1, phi2
        self.T, self.a1, self.tj, self.x0, self.R = 2, 2, 1, 0, 2

    def a_list(self, N):
        # t h < 1  <=>  2 t < N  (exact integer test)
        return [self.a1 if 2 * t < N else self.a2 for t in range(N + 1)]


VER = Toy("verifier", k=-0.5, a2=-2, phi1=0, phi2=0)
PLUS = Toy("plus", k=0.5, a2=-1, phi1=1, phi2=0)
ZERO = Toy("zero", k=0, a2=-1, phi1=1, phi2=0.5)


# ----------------------------------------------------------------------------- continuous switch
def tau_of(toy):
    """sigma(tau) = 0 for the one-switch extremal (+1 on [0,tau), -1 after), tau < 1.
    sigma(tau) = k tau + psi(T) + int_tau^T (x - a + k u) dt with x(t) = 2 tau - t after tau."""
    import sympy as sp
    t = sp.symbols("t", real=True)
    k, a1, a2, p1, p2, T = [sp.nsimplify(v) for v in (toy.k, toy.a1, toy.a2, toy.phi1, toy.phi2, toy.T)]
    xT = 2 * t - T
    s = sp.symbols("s", real=True)
    expr = k * t + p1 + p2 * xT + sp.integrate(2 * t - s, (s, t, T)) - a1 * (1 - t) - a2 * (T - 1) - k * (T - t)
    sols = [s for s in sp.solve(sp.expand(expr), t) if s.is_real and 0 < s < 1]
    return [float(s) for s in sols], sp.expand(expr)


def pmp_check(toy, tau, n=20001):
    """Sign of sigma(t) along the one-switch extremal (sigma <= 0 before tau, >= 0 after)."""
    T = toy.T
    ts = np.linspace(0, T, n)
    xT = 2 * tau - T
    psiT = toy.phi1 + toy.phi2 * xT

    def x(s):
        return np.where(s <= tau, s, 2 * tau - s)

    def a(s):
        return np.where(s < 1, toy.a1, toy.a2)

    def u(s):
        return np.where(s <= tau, 1.0, -1.0)
    # psi(t) = psiT + int_t^T (x - a + k u) ds, by fine trapezoid on a dense grid (screening)
    fine = np.linspace(0, T, 400001)
    f = x(fine) - a(fine) + toy.k * u(fine)
    cum = np.concatenate([[0], np.cumsum((f[1:] + f[:-1]) / 2 * np.diff(fine))])
    I_tT = cum[-1] - np.interp(ts, fine, cum)
    sig = toy.k * x(ts) + psiT + I_tT
    viol = max(np.max(np.maximum(0, sig[ts < tau - 1e-3])), np.max(np.maximum(0, -sig[ts > tau + 1e-3])))
    mask = np.abs(ts - tau) > 1e-3
    return float(viol), float(np.min(np.abs(sig[mask]) / np.abs(ts - tau)[mask]))


# ----------------------------------------------------------------------------- discrete problem
def simulate(toy, N, u, exact=False):
    """States, cost, costates (p_t = dJ/dx_t along the dynamics) and switching values sig_t = dJ/du_t / h."""
    num = Fr if exact else float
    h = num(toy.T) / N if exact else toy.T / N
    a = [num(v) for v in toy.a_list(N)]
    k, p1, p2 = num(toy.k), num(toy.phi1), num(toy.phi2)
    u = [num(v) for v in u]
    x = [num(toy.x0)]
    for t in range(N):
        x.append(x[-1] + h * u[t])
    J = sum(h * ((x[t] - a[t]) ** 2 / 2 + k * x[t] * u[t]) for t in range(N)) + p1 * x[N] + p2 * x[N] ** 2 / 2
    p = [None] * (N + 1)
    p[N] = p1 + p2 * x[N]
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + k * u[t])
    sig = [k * x[t] + p[t + 1] for t in range(N)]
    return dict(N=N, h=h, a=a, u=u, x=x, J=J, p=p, sig=sig, exact=exact)


def simulate_np(toy, N, u):
    h = toy.T / N
    a = np.array(toy.a_list(N), dtype=float)
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    J = h * np.sum((x[:N] - a[:N]) ** 2 / 2 + toy.k * x[:N] * u) + toy.phi1 * x[N] + toy.phi2 * x[N] ** 2 / 2
    inc = h * (x[:N] - a[:N] + toy.k * u)
    pN = toy.phi1 + toy.phi2 * x[N]
    p = np.concatenate([pN + np.cumsum(inc[::-1])[::-1], [pN]])
    sig = toy.k * x[:N] + p[1:]
    return x, J, p, sig


def kkt(toy, N, span=40):
    """Reviewer's KKT search: controls +1 on [0, m), v at m, -1 after; J is quadratic in v, fitted
    exactly from three evaluations; best (m, v) over a range of m around tau / h.  Then the KKT sign
    conditions are checked at every stage (no refinement: a violation is reported, not repaired)."""
    h = toy.T / N
    tau = tau_of(toy)[0][0]
    m0 = int(tau / h)
    best = None
    for m in range(max(1, m0 - span), min(N - 1, m0 + span)):
        base = np.where(np.arange(N) < m, 1.0, -1.0)
        vals = []
        for v in (-1.0, 0.0, 1.0):
            uu = base.copy()
            uu[m] = v
            vals.append(simulate_np(toy, N, uu)[1])
        c2 = (vals[0] + vals[2]) / 2 - vals[1]
        c1 = (vals[2] - vals[0]) / 2
        cands = [-1.0, 1.0] + ([-c1 / (2 * c2)] if c2 > 0 and abs(c1 / (2 * c2)) < 1 else [])
        for v in cands:
            uu = base.copy()
            uu[m] = v
            J = simulate_np(toy, N, uu)[1]
            if best is None or J < best[0]:
                best = (J, m, uu)
    J, m, u = best
    x, J, p, sig = simulate_np(toy, N, u)
    tol = 1e-12
    viol = float(np.max(np.where(u >= 1 - tol, np.maximum(0, sig), np.where(u <= -1 + tol, np.maximum(0, -sig), np.abs(sig)))))
    inter = [int(t) for t in np.where(np.abs(u) < 1 - tol)[0]]
    s = inter[0] if inter else int(np.where(u < 0)[0][0])
    return dict(N=N, h=h, u=u, x=x, J=J, p=p, sig=sig, s=s, inter=inter, viol=viol, m_edge=(m in (m0 - span, m0 + span - 1)))


def exact_kkt(toy, N, u):
    """Rational KKT point: float controls as rationals, the (single) interior control solved so that
    sigma_n = 0 exactly (sigma_n is affine in u_n: two exact evaluations).  Asserts all KKT signs."""
    uf = [Fr(float(v)) for v in u]
    inter = [t for t in range(N) if -1 < uf[t] < 1]
    assert len(inter) <= 1
    if inter:
        n = inter[0]
        s0 = simulate(toy, N, uf, exact=True)["sig"][n]
        u1 = list(uf)
        u1[n] = uf[n] + 1
        s1 = simulate(toy, N, u1, exact=True)["sig"][n]
        uf[n] = uf[n] - s0 / (s1 - s0)
        assert -1 < uf[n] < 1
    E = simulate(toy, N, uf, exact=True)
    for t in range(N):
        if uf[t] == 1:
            assert E["sig"][t] <= 0, t
        elif uf[t] == -1:
            assert E["sig"][t] >= 0, t
        else:
            assert E["sig"][t] == 0, t
    E["inter"] = inter
    return E


# ----------------------------------------------------------------------------- box QP
def _ldl_pd_solve(A, b, exact):
    """Solve A z = b if A is positive definite (Gaussian elimination without pivoting; all pivots > 0);
    return None otherwise."""
    n = len(b)
    M = [list(map(lambda v: v, A[i])) + [b[i]] for i in range(n)]
    eps = 0 if exact else 1e-300
    for c in range(n):
        piv = M[c][c]
        if not piv > eps:
            return None
        for r in range(c + 1, n):
            f = M[r][c] / piv
            if f != 0:
                for j in range(c, n + 1):
                    M[r][j] -= f * M[c][j]
    z = [None] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n] - sum((M[i][j] * z[j] for j in range(i + 1, n)), Fr(0) if exact else 0.0)
        z[i] = s / M[i][i]
    return z


def boxqp_min(g, H, lo, hi, exact=False):
    """min g.v + v^T H v / 2 over lo <= v <= hi.  Enumerates all faces; on a face with free set F the
    relative-interior stationary point is used only if H_FF is positive definite."""
    n = len(g)
    zero = Fr(0) if exact else 0.0
    var = [i for i in range(n) if lo[i] != hi[i]]
    best, bv = None, None
    for pat in itertools.product((0, 1, 2), repeat=len(var)):
        v = list(lo)
        free = []
        for i, c in zip(var, pat):
            if c == 1:
                v[i] = hi[i]
            elif c == 2:
                free.append(i)
        if free:
            fixed = [i for i in range(n) if i not in free]
            A = [[H[i][j] for j in free] for i in free]
            b = [-(g[i] + sum((H[i][j] * v[j] for j in fixed), zero)) for i in free]
            z = _ldl_pd_solve(A, b, exact)
            if z is None:
                continue
            if any(not (lo[i] <= zi <= hi[i]) for i, zi in zip(free, z)):
                continue
            for i, zi in zip(free, z):
                v[i] = zi
        val = sum((g[i] * v[i] for i in range(n)), zero) + sum((H[i][j] * v[i] * v[j] for i in range(n) for j in range(n)), zero) / 2
        if best is None or val < best:
            best, bv = val, v
    return best, bv


def boxqp_min_np(g, H, lo, hi):
    """Float version of boxqp_min (numpy linear algebra)."""
    g, H, lo, hi = map(lambda a: np.asarray(a, float), (g, H, lo, hi))
    n = len(g)
    var = [i for i in range(n) if lo[i] != hi[i]]
    best, bv = np.inf, None
    for pat in itertools.product((0, 1, 2), repeat=len(var)):
        v = lo.copy()
        pat = np.array(pat)
        vv = np.array(var, dtype=int)
        v[vv[pat == 1]] = hi[vv[pat == 1]]
        free = vv[pat == 2]
        if len(free):
            fixed = np.setdiff1d(np.arange(n), free)
            Hf = H[np.ix_(free, free)]
            try:
                np.linalg.cholesky(Hf)
            except np.linalg.LinAlgError:
                continue
            z = np.linalg.solve(Hf, -(g[free] + H[np.ix_(free, fixed)] @ v[fixed]))
            if np.any(z < lo[free]) or np.any(z > hi[free]):
                continue
            v[free] = z
        val = g @ v + 0.5 * v @ H @ v
        if val < best:
            best, bv = val, v
    return best, bv


def polarize(f, n, num):
    """g, H of the quadratic f (f(0) = 0 assumed subtracted) from exact evaluations."""
    e = lambda i, s=1: [num(s) if j == i else num(0) for j in range(n)]
    fp = [f(e(i)) for i in range(n)]
    fm = [f(e(i, -1)) for i in range(n)]
    g = [(fp[i] - fm[i]) / 2 for i in range(n)]
    H = [[None] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = fp[i] + fm[i]
    for i in range(n):
        for j in range(i + 1, n):
            v = [num(1) if q in (i, j) else num(0) for q in range(n)]
            H[i][j] = H[j][i] = f(v) - g[i] - g[j] - H[i][i] / 2 - H[j][j] / 2
    return g, H


# ----------------------------------------------------------------------------- calibration families
def S_val(E, P, t, x):
    return E["p"][t] * x + P[t] * (x - E["x"][t]) ** 2 / 2


def fam(E, Pfun):
    """P_t = P(t h) as exact rationals of the float values (any family gives a valid bound)."""
    N = E["N"]
    h = float(E["h"])
    return [Fr(float(Pfun(t * h))) if E["exact"] else float(Pfun(t * h)) for t in range(N + 1)]


def stage_loss(toy, E, P, t):
    """rho_t(zbar_t) - min over D_t x U of rho_t (>= 0; 0 means stage t is exact)."""
    num = Fr if E["exact"] else float
    h, k, a = E["h"], num(toy.k), E["a"]
    xb, ub = E["x"][t], E["u"][t]

    def rho(x, u):
        return h * ((x - a[t]) ** 2 / 2 + k * x * u) + S_val(E, P, t + 1, x + h * u) - S_val(E, P, t, x)
    r0 = rho(xb, ub)
    g, H = polarize(lambda v: rho(xb + v[0], ub + v[1]) - r0, 2, num)
    R = num(toy.R)
    lo = [num(0) if t == 0 else -R - xb, -1 - ub]
    hi = [num(0) if t == 0 else R - xb, 1 - ub]
    val, _ = boxqp_min(g, H, lo, hi, exact=E["exact"])
    return -val


def terminal_loss(toy, E, P):
    num = Fr if E["exact"] else float
    N = E["N"]
    xb = E["x"][N]
    p1, p2 = num(toy.phi1), num(toy.phi2)

    def F(x):
        return p1 * x + p2 * x ** 2 / 2 - S_val(E, P, N, x)
    f0 = F(xb)
    g, H = polarize(lambda v: F(xb + v[0]) - f0, 1, num)
    R = num(toy.R)
    val, _ = boxqp_min(g, H, [-R - xb], [R - xb], exact=E["exact"])
    return -val


def window_problem(toy, E, P, a, b):
    """f(v) = J_W(z) - J_W(zbar), v = (d_a, om_a, ..., om_{b-1}); J_W = sum_{a<=t<b} L_t + S_b(x_b) - S_a(x_a).
    Built by simulation; returns g, H, lo, hi (entry x_a in [-R, R], or fixed if a = 0; intermediate
    state bounds are dropped, which can only lower the window value) and a state map for checks."""
    num = Fr if E["exact"] else float
    h, k, at = E["h"], num(toy.k), E["a"]
    n = 1 + (b - a)

    def states(v):
        xs = [E["x"][a] + v[0]]
        for t in range(a, b):
            xs.append(xs[-1] + h * (E["u"][t] + v[1 + t - a]))
        return xs

    def JW(v):
        xs = states(v)
        tot = -S_val(E, P, a, xs[0])
        for t in range(a, b):
            u = E["u"][t] + v[1 + t - a]
            x = xs[t - a]
            tot += h * ((x - at[t]) ** 2 / 2 + k * x * u)
        return tot + S_val(E, P, b, xs[-1])
    J0 = JW([num(0)] * n)
    g, H = polarize(lambda v: JW(v) - J0, n, num)
    R = num(toy.R)
    lo = [num(0) if a == 0 else -R - E["x"][a]] + [-1 - E["u"][t] for t in range(a, b)]
    hi = [num(0) if a == 0 else R - E["x"][a]] + [1 - E["u"][t] for t in range(a, b)]
    return g, H, lo, hi, states
