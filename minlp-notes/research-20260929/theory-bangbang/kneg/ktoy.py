"""Scalar toys for kappa-negative.md (one or several switches, optional terminal row).

Continuous problem:  min int_0^T [ (x - a(t))^2 / 2 + k(t) x u ] dt + Phi(x(T)),  x' = u, |u| <= 1, x(0) = x0,
with a(t), k(t) piecewise constant and Phi(x) = phi1 x + phi2 x^2 / 2, or the terminal row x(T) = xT.
b = 1 and w_t = -k(t), so the switch self-curvature at a switch tau is kappa_tau = -k(tau).

Euler transcription (N stages, h = T / N):
    J(u) = h sum_t [ (x_t - a_t)^2 / 2 + k_t x_t u_t ] + Phi(x_N),  x_{t+1} = x_t + h u_t,
a_t = a(t h), k_t = k(t h) (piece containing t h, decided exactly).  J is an exact quadratic in u with
    dJ/du_t = h sigma_t,  sigma_t = k_t x_t + p_{t+1},  p_t = p_{t+1} + h (x_t - a_t + k_t u_t),
    p_N = phi1 + phi2 x_N (+ nu for the terminal row),
    H_ij = h^2 [ h (N - 1 - max(i, j)) + phi2 + k_{max(i, j)} (1 - delta_ij) ].
Quadratic families S_t(x) = p_t x + P_t (x - xbar_t)^2 / 2; in d = x - xbar_t, om = u - ubar_t the stage
residual minus its value at zbar_t is exactly
    h sig_t om + K_t d^2 / 2 + h beta_t d om + h^2 kap_t om^2 / 2,
    K_t = h + P_{t+1} - P_t,  beta_t = P_{t+1} + k_t,  kap_t = P_{t+1}.
All routines accept float or fractions.Fraction data.
"""
from dataclasses import dataclass
from fractions import Fraction as Fr
import functools
import itertools

import numpy as np


@dataclass(frozen=True)
class KToy:
    a_pts: tuple                 # ((t_0 = 0, a_0), (t_1, a_1), ...): a(t) = a_i on [t_i, t_{i+1})
    k_pts: tuple                 # same for k(t)
    T: float = 2.0
    x0: float = 0.0
    phi1: float = 0.0
    phi2: float = 0.0
    xT: object = None            # terminal row x_N = xT (then Phi is ignored), or None (free endpoint)
    R: float = 4.0               # state box |x| <= R (the stage domain D_t)

    def fixed_end(self):
        return self.xT is not None


def _exact_time(ti):
    """Jump time as the rational it denotes: a float is read as its shortest decimal repr (0.65 -> 13/20),
    not as its binary value (Fraction(0.65) > 13/20).  Revision after review (finding F2): the earlier
    version used Fraction(ti), so a stage with t h = t_i exactly kept the old value whenever
    fl(t_i) > t_i (t_i = 0.45, 0.55, 0.65, 1.3, 1.35, 1.55)."""
    return Fr(repr(ti)) if isinstance(ti, float) else Fr(ti)


def _piece(pts, N, T):
    T = Fr(T)
    out = []
    for t in range(N + 1):
        v = pts[0][1]
        for (ti, vi) in pts:
            if _exact_time(ti) * N <= Fr(t) * T:     # t h >= t_i, decided exactly
                v = vi
        out.append(v)
    return out


@functools.lru_cache(maxsize=256)
def _ak(toy, N):
    return tuple(_piece(toy.a_pts, N, toy.T)), tuple(_piece(toy.k_pts, N, toy.T))


def data(toy, N, exact=False):
    a, k = _ak(toy, N)
    if exact:
        return [Fr(v) for v in a], [Fr(v) for v in k]
    return np.array(a, float), np.array(k, float)


# ---------------------------------------------------------------- float objective, adjoint, Hessian
def simulate(toy, N, u):
    h = toy.T / N
    a, k = data(toy, N)
    x = toy.x0 + np.concatenate([[0.0], np.cumsum(h * u)])
    J = h * np.sum((x[:N] - a[:N]) ** 2 / 2 + k[:N] * x[:N] * u)
    if not toy.fixed_end():
        J += toy.phi1 * x[N] + toy.phi2 * x[N] ** 2 / 2
    return x, J


def adjoint(toy, N, x, u, nu=0.0):
    h = toy.T / N
    a, k = data(toy, N)
    pN = (0.0 if toy.fixed_end() else toy.phi1 + toy.phi2 * x[N]) + nu
    inc = h * (x[:N] - a[:N] + k[:N] * u)
    p = np.empty(N + 1)
    p[N] = pN
    p[:N] = pN + np.cumsum(inc[::-1])[::-1]
    sig = k[:N] * x[:N] + p[1:]
    return p, sig


def hess(toy, N, idx):
    h = toy.T / N
    _, k = data(toy, N)
    idx = np.asarray(idx, int)
    mx = np.maximum.outer(idx, idx)
    phi2 = 0.0 if toy.fixed_end() else toy.phi2
    return h * h * (h * (N - 1 - mx) + phi2 + k[mx] * (1 - np.eye(len(idx))))


# ---------------------------------------------------------------- KKT points (active-set Newton)
def kkt_refine(toy, N, u, fixed=(), maxit=200, tol=1e-13, bnds=None):
    """Active-set Newton on the exact quadratic J (nonconvex in general).  `fixed` lists stages whose
    control is held (parameters); bnds = {t: (lo, hi)} narrows the control range of stage t (a branch
    and bound node).  Returns dict with u, nu, sigma, frac, kkt violation."""
    h = toy.T / N
    lo = np.full(N, -1.0)
    hi = np.full(N, 1.0)
    for t, (l_, r_) in (bnds or {}).items():
        lo[t], hi[t] = float(l_), float(r_)
    u = np.clip(np.array(u, float), lo, hi)
    fixed = set(int(i) for i in fixed)
    nu = 0.0
    m = None if not toy.fixed_end() else (toy.xT - toy.x0) / h
    if m is not None:
        # start the row multiplier where the interior stages are stationary
        x, _ = simulate(toy, N, u)
        _, sig0 = adjoint(toy, N, x, u, 0.0)
        inter0 = [t for t in range(N) if lo[t] + 1e-15 < u[t] < hi[t] - 1e-15 and t not in fixed]
        if inter0:
            nu = -float(np.mean(sig0[inter0]))
    for it in range(maxit):
        x, J = simulate(toy, N, u)
        p, sig = adjoint(toy, N, x, u, nu)
        inter = [t for t in range(N) if lo[t] + 1e-15 < u[t] < hi[t] - 1e-15 and t not in fixed]
        viol = [t for t in range(N) if t not in fixed and
                ((u[t] >= hi[t] - 1e-15 and sig[t] > tol) or (u[t] <= lo[t] + 1e-15 and sig[t] < -tol))]
        F = sorted(set(inter) | set(viol))
        res_end = 0.0 if m is None else (np.sum(u) - m)
        if not viol and (not inter or np.abs(sig[inter]).max() < tol) and abs(res_end) < 1e-12:
            break
        if not F:
            break
        HF = hess(toy, N, F)
        if m is None:
            step = np.linalg.solve(HF, -h * sig[F])
            dnu = 0.0
        else:
            nF = len(F)
            A = np.zeros((nF + 1, nF + 1))
            A[:nF, :nF] = HF
            A[:nF, nF] = h
            A[nF, :nF] = h
            rhs = np.concatenate([-h * sig[F], [-h * res_end]])
            sol = np.linalg.lstsq(A, rhs, rcond=None)[0]
            step, dnu = sol[:nF], sol[nF]
        u[F] = np.clip(u[F] + step, lo[F], hi[F])
        nu += dnu
    x, J = simulate(toy, N, u)
    p, sig = adjoint(toy, N, x, u, nu)
    frac = [t for t in range(N) if lo[t] + 1e-12 < u[t] < hi[t] - 1e-12 and t not in fixed]
    for t in range(N):       # snap to bounds
        if t not in fixed and t not in frac:
            u[t] = hi[t] if abs(u[t] - hi[t]) <= 1e-12 else lo[t]
    x, J = simulate(toy, N, u)
    p, sig = adjoint(toy, N, x, u, nu)
    v = np.where(u >= hi, np.maximum(0, sig), np.where(u <= lo, np.maximum(0, -sig), np.abs(sig)))
    v[list(fixed)] = 0.0
    viol = float(v.max())
    if m is not None and abs(np.sum(u) - m) > 1e-9:
        viol = float("inf")                       # terminal row not satisfied
    return dict(N=N, h=h, u=u, x=x, p=p, sig=sig, nu=nu, J=J, frac=frac, kkt_viol=viol, iters=it,
                fixed=sorted(fixed), bnds=dict(bnds or {}))


def bang(N, T, switches, first=1.0):
    """Bang-bang control starting at `first` and switching at the given times."""
    u = np.full(N, first)
    h = T / N
    for j, ts in enumerate(switches):
        m = int(round(ts / h))
        u[m:] = first * (-1) ** (j + 1)
    return u


def best_bang(toy, N0, nsw, first=1.0):
    """Brute force over integer switch stages (nsw = 1 or 2) at a coarse N0; returns switch times."""
    best = None
    h = toy.T / N0
    if nsw == 1:
        cands = [(m,) for m in range(1, N0)]
    else:
        cands = [(m1, m2) for m1 in range(1, N0) for m2 in range(m1 + 1, N0)]
    for c in cands:
        u = np.full(N0, first)
        for j, m in enumerate(c):
            u[m:] = first * (-1) ** (j + 1)
        if toy.fixed_end():
            kk = kkt_refine(toy, N0, u, maxit=50)
            J = kk["J"] if kk["kkt_viol"] < 1e-9 else np.inf
        else:
            _, J = simulate(toy, N0, u)
        if best is None or J < best[0]:
            best = (J, c)
    return [m * h for m in best[1]]


def _pattern(N, ms, first):
    u = np.full(N, first)
    for j, m in enumerate(ms):
        u[m:] = first * (-1) ** (j + 1)
    return u


def _best_frac(toy, N, u, m):
    """Optimize the single control u_m (1-D quadratic, clipped)."""
    h = toy.T / N
    x, _ = simulate(toy, N, u)
    _, sig = adjoint(toy, N, x, u)
    Hmm = hess(toy, N, [m])[0, 0]
    v = u[m] - h * sig[m] / Hmm if Hmm > 0 else (u[m] if sig[m] * u[m] <= 0 else -u[m])
    u = u.copy()
    u[m] = min(1.0, max(-1.0, v))
    return u


def _fixed_end_fill(toy, N, ms, first):
    """Pattern with switch stages ms[:-1] and the last switch placed (with one fractional stage) so that
    the terminal row sum(u) = (xT - x0)/h holds.  Returns None if impossible."""
    h = toy.T / N
    target = (toy.xT - toy.x0) / h
    best = None
    for m in range(1, N):
        u = _pattern(N, list(ms[:-1]) + [m], first)
        # one fractional stage at m - 1 or m absorbs the defect
        for f in (m - 1, m):
            if f < 0 or f >= N:
                continue
            uu = u.copy()
            uu[f] = 0.0
            need = target - uu.sum()
            if -1 <= need <= 1:
                uu[f] = need
                return uu
    return best


def kkt(toy, N, switches, first=1.0, W=None, rounds=3):
    """KKT point near the given switch times.  Phase scan: for each switch in turn, scan its stage over
    +-W stages, optimizing the switching stage's control (1-D, exact quadratic); for the terminal row the
    last switch is placed by the row.  Then active-set Newton (kkt_refine) from the best scanned point."""
    h = toy.T / N
    ms = [int(round(ts / h)) for ts in switches]
    W = max(4, int(0.02 * N)) if W is None else W
    nsc = len(ms) - (1 if toy.fixed_end() else 0)

    def evalp(ms_):
        if toy.fixed_end():
            u = _fixed_end_fill(toy, N, ms_, first)
            if u is None:
                return np.inf, None
        else:
            u = _pattern(N, ms_, first)
            for m in ms_:
                u = _best_frac(toy, N, u, m)
                u = _best_frac(toy, N, u, m - 1)
        return simulate(toy, N, u)[1], u
    bestJ, bestu = evalp(ms)
    for _ in range(rounds):
        changed = False
        for j in range(nsc):
            lo = (ms[j - 1] + 1) if j > 0 else 1
            hi = (ms[j + 1] - 1) if j + 1 < len(ms) else N - 1
            for m in range(max(lo, ms[j] - W), min(hi, ms[j] + W) + 1):
                trial = list(ms)
                trial[j] = m
                J, u = evalp(trial)
                if J < bestJ - 1e-16:
                    bestJ, bestu, ms, changed = J, u, trial, True
        if not changed:
            break
    kk = kkt_refine(toy, N, bestu)
    return kk if kk["kkt_viol"] < 1e-10 else None


# ---------------------------------------------------------------- exact data
def exact_traj(toy, N, u, nu=Fr(0)):
    h = Fr(toy.T) / N
    a, k = data(toy, N, exact=True)
    u = [v if isinstance(v, Fr) else Fr(float(v)) for v in u]
    x = [Fr(toy.x0)]
    for t in range(N):
        x.append(x[-1] + h * u[t])
    J = sum(h * ((x[t] - a[t]) ** 2 / 2 + k[t] * x[t] * u[t]) for t in range(N))
    if not toy.fixed_end():
        J += Fr(toy.phi1) * x[N] + Fr(toy.phi2) * x[N] ** 2 / 2
    p = [None] * (N + 1)
    p[N] = (Fr(0) if toy.fixed_end() else Fr(toy.phi1) + Fr(toy.phi2) * x[N]) + nu
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + k[t] * u[t])
    sig = [k[t] * x[t] + p[t + 1] for t in range(N)]
    return dict(N=N, h=h, a=a, k=k, u=u, x=x, p=p, sig=sig, J=J, nu=nu)


def hess_exact(toy, N, idx):
    h = Fr(toy.T) / N
    _, k = data(toy, N, exact=True)
    phi2 = Fr(0) if toy.fixed_end() else Fr(toy.phi2)
    return [[h * h * (h * (N - 1 - max(i, j)) + phi2 + (k[max(i, j)] if i != j else 0)) for j in idx] for i in idx]


def solve_lin(A, b):
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def exact_kkt(toy, kk, check=True):
    """Rational KKT point: float controls as rationals; the fractional controls (and nu for the terminal
    row) corrected by one exact Newton step (J is quadratic, so the step is exact).  Asserts the exact
    KKT sign conditions (stages in kk['fixed'] are parameters and are not checked)."""
    N = kk["N"]
    bn = {t: (Fr(l_), Fr(r_)) for t, (l_, r_) in kk.get("bnds", {}).items()}
    lo = [bn[t][0] if t in bn else Fr(-1) for t in range(N)]
    hi = [bn[t][1] if t in bn else Fr(1) for t in range(N)]
    u = [Fr(float(v)) for v in kk["u"]]
    for t in range(N):
        if t not in kk["frac"] and t not in kk.get("fixed", []):
            u[t] = hi[t] if abs(float(u[t]) - float(hi[t])) <= 1e-12 else lo[t]
    F = list(kk["frac"])
    nu = Fr(float(kk["nu"])) if toy.fixed_end() else Fr(0)
    E = exact_traj(toy, N, u, nu)
    if toy.fixed_end() and not F:
        # bang-bang point satisfying the row exactly: the multiplier nu is any value in the interval
        # where all sign conditions hold (sigma_t(nu) = sigma_t(0) + nu); take its midpoint
        E0 = exact_traj(toy, N, u, Fr(0))
        lo_nu = max((-E0["sig"][t] for t in range(N) if u[t] == lo[t]), default=None)
        hi_nu = min((-E0["sig"][t] for t in range(N) if u[t] == hi[t]), default=None)
        if lo_nu is not None and hi_nu is not None and lo_nu <= hi_nu:
            nu = (lo_nu + hi_nu) / 2
        E = exact_traj(toy, N, u, nu)
    if F:
        h = E["h"]
        HF = hess_exact(toy, N, F)
        if toy.fixed_end():
            m = (Fr(toy.xT) - Fr(toy.x0)) / h
            A = [row + [h] for row in HF] + [[h] * len(F) + [Fr(0)]]
            b = [-h * E["sig"][t] for t in F] + [-h * (sum(u) - m)]
            sol = solve_lin(A, b)
            for i, t in enumerate(F):
                u[t] += sol[i]
            nu += sol[-1]
        else:
            sol = solve_lin(HF, [-h * E["sig"][t] for t in F])
            for i, t in enumerate(F):
                u[t] += sol[i]
        E = exact_traj(toy, N, u, nu)
    if check:
        fixed = set(kk.get("fixed", []))
        for t in range(N):
            if t in fixed:
                continue
            if u[t] == hi[t]:
                assert E["sig"][t] <= 0, ("sign", t)
            elif u[t] == lo[t]:
                assert E["sig"][t] >= 0, ("sign", t)
            else:
                assert lo[t] < u[t] < hi[t] and E["sig"][t] == 0, ("interior", t)
        if toy.fixed_end():
            assert E["x"][N] == Fr(toy.xT)
    E["frac"] = F
    E["fixed"] = list(kk.get("fixed", []))
    E["lo"], E["hi"] = lo, hi
    return E


def float_data(toy, kk):
    a, k = data(toy, kk["N"])
    return dict(N=kk["N"], h=kk["h"], u=kk["u"], x=kk["x"], p=kk["p"], sig=kk["sig"], J=kk["J"], a=a, k=k,
                frac=kk["frac"], nu=kk["nu"])


# ---------------------------------------------------------------- two-variable box QP (exact or float)
def qp2_min(g, H, lo, hi):
    """min g.z + z^T H z / 2 over a box in R^1 or R^2 by enumerating faces."""
    n = len(g)
    best = None
    zero = g[0] * 0
    for pat in itertools.product((0, 1, 2), repeat=n):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(n)]
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fx = [i for i in range(n) if pat[i] != 2]
            A = [[H[i][j] for j in free] for i in free]
            b = [-(g[i] + sum((H[i][j] * z[j] for j in fx), zero)) for i in free]
            if len(free) == 1:
                if A[0][0] == 0:
                    continue
                sol = [b[0] / A[0][0]]
            else:
                det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
                if det == 0:
                    continue
                sol = [(b[0] * A[1][1] - A[0][1] * b[1]) / det, (A[0][0] * b[1] - A[1][0] * b[0]) / det]
            if not all(lo[i] <= v <= hi[i] for i, v in zip(free, sol)):
                continue
            for i, v in zip(free, sol):
                z[i] = v
        val = sum((g[i] * z[i] for i in range(n)), zero) + sum((H[i][j] * z[i] * z[j] for i in range(n) for j in range(n)), zero) / 2
        if best is None or val < best:
            best = val
    return best


# ---------------------------------------------------------------- calibration bound of a quadratic family
def stage_loss(toy, D, P, t, om_lo=None, om_hi=None, sig=None):
    """Loss rho_t(zbar_t) - inf rho_t over D_t x U_t for the family with curvatures P (slopes = costates of D).
    om range defaults to U - ubar_t; sig overrides sigma_t (lifted certificate)."""
    h, x, u, k = D["h"], D["x"], D["u"], D["k"]
    s = D["sig"][t] if sig is None else sig
    Pt, Pn = P[t], P[t + 1]
    K = h + Pn - Pt
    beta = Pn + k[t]
    g = [0 * h, h * s]
    H = [[K, h * beta], [h * beta, h * h * Pn]]
    R = type(h)(toy.R) if not isinstance(h, Fr) else Fr(toy.R)
    lo_om = (-1 - u[t]) if om_lo is None else om_lo
    hi_om = (1 - u[t]) if om_hi is None else om_hi
    if t == 0:
        v = qp2_min([g[1]], [[H[1][1]]], [lo_om], [hi_om])
    else:
        v = qp2_min(g, H, [-R - x[t], lo_om], [R - x[t], hi_om])
    return -v


def terminal_loss(toy, D, P):
    if toy.fixed_end():
        return 0 * D["h"]
    N, x = D["N"], D["x"]
    R = Fr(toy.R) if isinstance(D["h"], Fr) else float(toy.R)
    phi2 = Fr(toy.phi2) if isinstance(D["h"], Fr) else float(toy.phi2)
    return -qp2_min([0 * D["h"]], [[phi2 - P[N]]], [-R - x[N]], [R - x[N]])


def bound(toy, D, P, skip=()):
    """Calibration bound B = J(zbar) - sum of stage losses - terminal loss (no windows)."""
    L = {t: stage_loss(toy, D, P, t) for t in range(D["N"]) if t not in skip}
    LN = terminal_loss(toy, D, P)
    return D["J"] - sum(L.values()) - LN, L, LN


def fam_const(N, val):
    return [val] * (N + 1)


def fam_rmax(toy, D, eps=0.0, PN=None, fixed_stages=()):
    """Discrete maximal recursion (extension-n2.md Lemma 10), scalar, Delta = 2:
    P_t = h + P_{t+1} - 2 h eps - beta_t^2 / m_t,  m_t = |sig_t| / h + P_{t+1} (sig_t := 0 at interior
    stages),  beta_t = P_{t+1} + k_t.  PN = None: phi2 - 2 eps (free end); PN = 'inf' (terminal row): the
    first step from P_N = +infinity gives P_{N-1} = h + |sig_{N-1}|/h - 2 k_{N-1} - 2 h eps.
    Stages in fixed_stages have no control: P_t = h + P_{t+1} - 2 h eps.  Returns (P, break stage or None)."""
    N, h, sig, k = D["N"], D["h"], D["sig"], D["k"]
    frac = set(D["frac"])
    P = [None] * (N + 1)
    start = N - 1
    if PN == "inf":
        t = N - 1
        s = 0 * h if t in frac else abs(sig[t])
        P[N] = None
        P[N - 1] = h + s / h - 2 * k[t] - 2 * h * eps
        start = N - 2
    else:
        P[N] = (toy.phi2 - 2 * eps) if PN is None else PN
    for t in range(start, -1, -1):
        if t in fixed_stages:
            P[t] = h + P[t + 1] - 2 * h * eps
            continue
        beta = P[t + 1] + k[t]
        s = 0 * h if t in frac else abs(sig[t])
        m = s / h + P[t + 1]
        if m <= 0:
            return P, t
        P[t] = h + P[t + 1] - 2 * h * eps - beta * beta / m
    return P, None


# ---------------------------------------------------------------- window problems (box QP by faces)
def box_qp_min(g, H, lo, hi):
    """min g.z + z^T H z / 2 over a box (any dimension) by enumerating faces; exact for Fractions."""
    n = len(g)
    zero = g[0] * 0
    best = None
    for pat in itertools.product((0, 1, 2), repeat=n):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(n)]
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fx = [i for i in range(n) if pat[i] != 2]
            A = [[H[i][j] for j in free] for i in free]
            b = [-(g[i] + sum((H[i][j] * z[j] for j in fx), zero)) for i in free]
            sol = solve_lin(A, b)
            if sol is None or not all(lo[i] <= v <= hi[i] for i, v in zip(free, sol)):
                continue
            for i, v in zip(free, sol):
                z[i] = v
        val = sum((g[i] * z[i] for i in range(n)), zero) + sum((H[i][j] * z[i] * z[j] for i in range(n) for j in range(n)), zero) / 2
        if best is None or val < best:
            best = val
    return best


def window_value(toy, D, P, a, b):
    """min over the window relaxation of J_W - J_W(zbar), J_W = sum_{t=a}^{b-1} L_t + S_b(x_b) - S_a(x_a), in
    v = (d_a, om_a, ..., om_{b-1}); entry d_a over the state box (0 if a = 0), controls over U_t (node bounds)."""
    h, x, u, p, at, k = D["h"], D["x"], D["u"], D["p"], D["a"], D["k"]
    one = h / h
    zero = h * 0
    m = b - a
    n = 1 + m
    g = [zero] * n
    H = [[zero] * n for _ in range(n)]

    def e(t):
        v = [zero] * n
        v[0] = one
        for j in range(a, t):
            v[1 + j - a] = h
        return v

    def addH(v1, v2, c):
        for i in range(n):
            if v1[i] != 0:
                for j in range(n):
                    if v2[j] != 0:
                        H[i][j] += c * v1[i] * v2[j]
    for t in range(a, b):
        et = e(t)
        ft = [zero] * n
        ft[1 + t - a] = one
        for i in range(n):
            g[i] += et[i] * h * (x[t] - at[t] + k[t] * u[t]) + ft[i] * h * k[t] * x[t]
        addH(et, et, h)
        addH(et, ft, h * k[t])
        addH(ft, et, h * k[t])
    eb, ea = e(b), e(a)
    for i in range(n):
        g[i] += eb[i] * p[b] - ea[i] * p[a]
    addH(eb, eb, P[b])
    addH(ea, ea, -P[a])
    R = Fr(toy.R) if isinstance(h, Fr) else float(toy.R)
    lo_u = D.get("lo", [-one] * D["N"])
    hi_u = D.get("hi", [one] * D["N"])
    lo = [(-R - x[a]) if a > 0 else zero] + [lo_u[t] - u[t] for t in range(a, b)]
    hi = [(R - x[a]) if a > 0 else zero] + [hi_u[t] - u[t] for t in range(a, b)]
    return box_qp_min(g, H, lo, hi)
