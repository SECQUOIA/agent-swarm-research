"""Euler transcription of the model.py family, its bang-bang KKT point, and quadratic calibrations
    S_t(x) = p_t . x + 1/2 (x - xbar_t)^T P_t (x - xbar_t),   p_t = discrete costates.

Stage residual rho_t = L_t + S_{t+1} o f_t - S_t is jointly quadratic in (x, u).  In the
coordinates d = x - xbar_t, om = u - ubar_t:
    rho_t - rho_t(zbar) = g_t.d + h sig_t om + 1/2 d^T K_t d + h om beta_t.d + 1/2 h^2 kap_t om^2,
    K_t = h Hxx + Fx^T P_{t+1} Fx - P_t,  beta_t = Fx^T P_{t+1} b - w,  kap_t = b^T P_{t+1} b,
with g_t = 0 up to rounding (discrete adjoint).  Exactness of stage t over the reachable box is
checked by exact minimization of this quadratic over the box (enumeration of faces).
"""
import itertools

import numpy as np

from model import A, B

bvec = B


def fx(h):
    return np.array([[1.0, h], [0.0, 1.0]])


def reach_box(p, N, h):
    """Exact bounds on all feasible Euler states: x2_t in x20 +- t h, x1_t in x10 + t h x20 +- h^2 t(t-1)/2."""
    t = np.arange(N + 1, dtype=float)
    x2lo, x2hi = p.x20 - t * h, p.x20 + t * h
    x1lo = p.x10 + t * h * p.x20 - h * h * t * (t - 1) / 2
    x1hi = p.x10 + t * h * p.x20 + h * h * t * (t - 1) / 2
    return np.stack([x1lo, x2lo], 1), np.stack([x1hi, x2hi], 1)


def simulate(p, N, u):
    h = p.T / N
    x = np.empty((N + 1, 2))
    x[0] = (p.x10, p.x20)
    J = 0.0
    for t in range(N):
        x1, x2 = x[t]
        J += h * (p.e * x2 + 0.5 * p.q * x1 ** 2 - 0.5 * p.c * x2 ** 2 + (p.k1 * x1 + p.k2 * x2) * u[t])
        x[t + 1] = (x1 + h * x2, x2 + h * u[t])
    J += p.Phi(*x[N])
    return x, J


def adjoint(p, N, x, u):
    h = p.T / N
    P = np.empty((N + 1, 2))
    P[N] = p.dPhi(*x[N])
    for t in range(N - 1, -1, -1):
        p1, p2 = P[t + 1]
        P[t] = (p1 + h * (p.q * x[t, 0] + p.k1 * u[t]),
                p2 + h * p1 + h * (p.e - p.c * x[t, 1] + p.k2 * u[t]))
    sig = p.k1 * x[:N, 0] + p.k2 * x[:N, 1] + P[1:, 1]
    return P, sig


def controls(p, N, th):
    m = int(np.floor(th))
    f = th - m
    u = np.full(N, p.ub)
    u[:m] = p.ua
    if m < N:
        u[m] = f * p.ua + (1 - f) * p.ub
    return u, m


def _sig_of(p, N, u):
    x, _ = simulate(p, N, u)
    _, sig = adjoint(p, N, x, u)
    return sig


def refine_kkt(p, N, u, maxit=50):
    """Active-set Newton for the box QP min J(u), u in [-1,1]^N (J is an exact quadratic in u here):
    free set = interior controls plus sign violators; Hessian block of the free set by exact
    differencing of sigma (sigma is affine in u)."""
    h = p.T / N
    lo, hi = min(p.ua, p.ub), max(p.ua, p.ub)
    u = u.copy()
    for it in range(maxit):
        sig = _sig_of(p, N, u)
        interior = np.where((u > lo + 1e-15) & (u < hi - 1e-15))[0]
        viol = np.where(((u >= hi - 1e-15) & (sig > 1e-15)) | ((u <= lo + 1e-15) & (sig < -1e-15)))[0]
        F = np.union1d(interior, viol)
        if len(viol) == 0 and (len(interior) == 0 or np.abs(sig[interior]).max() < 1e-14):
            return u, it
        # Hessian block H_FF = d(h sig_F)/du_F by unit differencing
        Hff = np.empty((len(F), len(F)))
        for j, t in enumerate(F):
            du = np.zeros(N); du[t] = 1e-3
            Hff[:, j] = h * (_sig_of(p, N, u + du)[F] - sig[F]) / 1e-3
        step = np.linalg.solve(Hff, -h * sig[F])
        u[F] = np.clip(u[F] + step, lo, hi)
    raise RuntimeError("refine_kkt did not converge")


def solve_kkt(p, N):
    """Bang-bang KKT point: bisection on the switching parameter, then active-set refinement."""
    def g(th):
        u, m = controls(p, N, th)
        x, _ = simulate(p, N, u)
        _, sig = adjoint(p, N, x, u)
        return sig[min(m, N - 1)]
    # sign convention: ua = +1 needs sigma <= 0 before the switch
    lo, hi = 0.0, float(N) - 1e-9
    glo, ghi = g(lo), g(hi)
    assert glo * ghi < 0, (glo, ghi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        gm = g(mid)
        if gm * glo > 0:
            lo, glo = mid, gm
        else:
            hi = mid
        if hi - lo < 1e-13 * N:
            break
    th = 0.5 * (lo + hi)
    u, m = controls(p, N, th)
    u, nit = refine_kkt(p, N, u)
    inter = np.where(np.abs(np.abs(u) - 1.0) > 1e-12)[0]
    if len(inter):
        m = int(inter[0])
    x, J = simulate(p, N, u)
    P, sig = adjoint(p, N, x, u)
    # KKT sign violations away from the fractional stage
    sgn = np.where(u > 0.5, np.maximum(0, sig), np.where(u < -0.5, np.maximum(0, -sig), 0.0))
    frac = bool(abs(abs(u[m]) - 1.0) > 1e-12)
    fracset = set(int(t) for t in inter)
    return dict(th=th, m=m, u=u, x=x, J=J, p=P, sig=sig, kkt_viol=float(sgn.max()), frac=frac, fracset=fracset,
                sig_m=float(sig[m]), N=N, h=p.T / N)


# ------------------------------------------------------------------ calibration families
def fam_affine(p, kk):
    return np.zeros((kk["N"] + 1, 2, 2))


def fam_lyap(p, kk, eps):
    """Discrete Lyapunov with margin: K_t = 2 h eps I at every stage (non-tangential at the switch)."""
    N, h, x = kk["N"], kk["h"], kk["x"]
    F = fx(h)
    Ps = np.empty((N + 1, 2, 2))
    Ps[N] = p.Phixx(*x[N]) - 2 * eps * np.eye(2)
    for t in range(N - 1, -1, -1):
        Ps[t] = h * p.Hxx + F.T @ Ps[t + 1] @ F - 2 * h * eps * np.eye(2)
    return Ps


def fam_rmax(p, kk, eps, P_N=None, t_stop=0):
    """Discrete maximal singular Riccati recursion (the discrete P-hat):
        P_t = h Hxx + Fx^T P_{t+1} Fx - 2 h eps I - beta_t beta_t^T / m_t,
        m_t = 2 |sig_t| / (h Delta) + kap_t   (> 0 required; the stage cannot be exact otherwise).
    Returns P and the first (largest) t at which m_t <= 0 (None if the recursion never breaks)."""
    N, h, x, sig = kk["N"], kk["h"], kk["x"], kk["sig"]
    Delta = abs(p.ub - p.ua)
    F = fx(h)
    Ps = np.full((N + 1, 2, 2), np.nan)
    Ps[N] = p.Phixx(*x[N]) - 2 * eps * np.eye(2) if P_N is None else P_N
    brk = None
    ms = np.full(N, np.nan)
    for t in range(N - 1, t_stop - 1, -1):
        X = Ps[t + 1]
        beta = F.T @ X @ bvec - p.w
        kap = bvec @ X @ bvec
        s = 0.0 if t in kk["fracset"] else abs(sig[t])
        m = 2 * s / (h * Delta) + kap
        ms[t] = m
        if m <= 0:
            brk = t
            break
        Ps[t] = h * p.Hxx + F.T @ X @ F - 2 * h * eps * np.eye(2) - np.outer(beta, beta) / m
    return Ps, brk, ms


# ------------------------------------------------------------------ stage checks (float)
def stage_quadratics(p, kk, Ps):
    """Coefficients of rho_t - rho_t(zbar) in (d, om), t = 0..N-1, plus the terminal quadratic."""
    N, h, x, u, pc = kk["N"], kk["h"], kk["x"], kk["u"], kk["p"]
    F = fx(h)
    out = []
    for t in range(N):
        X = Ps[t + 1]
        g = h * np.array([p.q * x[t, 0] + p.k1 * u[t], p.e - p.c * x[t, 1] + p.k2 * u[t]]) + F.T @ pc[t + 1] - pc[t]
        K = h * p.Hxx + F.T @ X @ F - Ps[t]
        beta = F.T @ X @ bvec - p.w
        kap = bvec @ X @ bvec
        out.append((g, h * kk["sig"][t], K, h * beta, h * h * kap))
    return out


def box_min_quadratic(c0, g, Hm, lo, hi):
    """Exact (float) minimum of c0 + g.z + 1/2 z^T Hm z over the box lo <= z <= hi (face enumeration)."""
    n = len(g)
    best = np.inf
    for pat in itertools.product((0, 1, 2), repeat=n):  # 0 lo, 1 hi, 2 free
        z = np.where(np.array(pat) == 0, lo, hi).astype(float)
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fixed = [i for i in range(n) if pat[i] != 2]
            Hff = Hm[np.ix_(free, free)]
            rhs = -(g[free] + Hm[np.ix_(free, fixed)] @ z[fixed]) if fixed else -g[free]
            if abs(np.linalg.det(Hff)) < 1e-300:
                continue
            zf = np.linalg.solve(Hff, rhs)
            if np.any(zf < lo[free] - 1e-15) or np.any(zf > hi[free] + 1e-15):
                continue
            z[free] = np.clip(zf, lo[free], hi[free])
        val = c0 + g @ z + 0.5 * z @ Hm @ z
        best = min(best, val)
    return best


def stage_losses(p, kk, Ps, box=None):
    """Loss_t = rho_t(zbar) - min over (D_t x U) of rho_t  (>= 0 up to rounding)."""
    N, h, x, u = kk["N"], kk["h"], kk["x"], kk["u"]
    lo_b, hi_b = reach_box(p, N, h) if box is None else box
    quads = stage_quadratics(p, kk, Ps)
    loss = np.empty(N)
    for t, (g, hs, K, hb, hk) in enumerate(quads):
        gg = np.array([g[0], g[1], hs])
        Hm = np.zeros((3, 3))
        Hm[:2, :2] = K
        Hm[:2, 2] = Hm[2, :2] = hb
        Hm[2, 2] = hk
        if t == 0:  # x_0 is fixed: minimize over om only
            lo = np.array([0.0, 0.0, p.ub - u[0] if p.ub < p.ua else p.ua - u[0]])
            lo = np.array([0.0, 0.0, min(p.ua, p.ub) - u[0]])
            hi = np.array([0.0, 0.0, max(p.ua, p.ub) - u[0]])
        else:
            lo = np.array([lo_b[t, 0] - x[t, 0], lo_b[t, 1] - x[t, 1], min(p.ua, p.ub) - u[t]])
            hi = np.array([hi_b[t, 0] - x[t, 0], hi_b[t, 1] - x[t, 1], max(p.ua, p.ub) - u[t]])
        loss[t] = -box_min_quadratic(0.0, gg, Hm, lo, hi)
    # terminal: Phi - S_N (quadratic when nu = 0) minus its value at xbar_N
    assert p.nu == 0.0
    gN = p.dPhi(*x[N]) - kk["p"][N]
    HN = p.Phixx(*x[N]) - Ps[N]
    loN = lo_b[N] - x[N]
    hiN = hi_b[N] - x[N]
    lossN = -box_min_quadratic(0.0, gN, HN, loN, hiN)
    return loss, lossN


def fam_tlayer(p, kk, eps, delta1, pre="rmax", shift=0, delta_pre=None):
    """Discrete analogue of the local-version tangential construction (extension-n2.md, Thm 2):
    - stages t > s + L (L = round(delta1 / h)): discrete Lyapunov with margin 2 h eps;
    - layer s < t <= s + L: R^2-maximal Schur push for stage t, plus a rank-one PSD push Z_t chosen so
      that beta_{t-1} decreases linearly to 0 at stage s + shift (shift != 0 gives an O(h) defect);
    - stage s and earlier: pre = "rmax" (R^2-maximal recursion) for t >= s - Lpre (Lpre = delta_pre/h,
      all stages if delta_pre is None), discrete Lyapunov before that.
    Returns P (N+1, 2, 2) and a dict of diagnostics."""
    N, h, x, sig, s = kk["N"], kk["h"], kk["x"], kk["sig"], kk["m"]
    Delta = abs(p.ub - p.ua)
    F = fx(h)
    FinvT = np.linalg.inv(F).T
    L = max(1, int(round(delta1 / h)))
    s0 = s + shift
    Ps = np.full((N + 1, 2, 2), np.nan)
    Ps[N] = p.Phixx(*x[N]) - 2 * eps * np.eye(2)
    I2 = np.eye(2)
    diag = dict(L=L, ybad=0, brk=None)
    for t in range(N - 1, s0, -1):
        X = Ps[t + 1]
        Pl = h * p.Hxx + F.T @ X @ F - 2 * h * eps * I2
        if t > s0 + L:
            Ps[t] = Pl
            if t == s0 + L + 1:
                diag["beta_start"] = F.T @ Pl @ bvec - p.w
            continue
        beta = F.T @ X @ bvec - p.w
        m = 2 * abs(sig[t]) / (h * Delta) + bvec @ X @ bvec
        Pt = Pl - np.outer(beta, beta) / m if m > 0 else Pl
        target = diag["beta_start"] * (t - 1 - s0) / L
        z = F.T @ Pt @ bvec - p.w - target
        y = FinvT @ z
        if bvec @ y <= 0:
            diag["ybad"] += 1
            Ps[t] = Pt
        else:
            Ps[t] = Pt - np.outer(y, y) / (bvec @ y)
    Lpre = N if delta_pre is None else int(round(delta_pre / h))
    for t in range(s0, -1, -1):
        X = Ps[t + 1]
        Pl = h * p.Hxx + F.T @ X @ F - 2 * h * eps * I2
        beta = F.T @ X @ bvec - p.w
        frac = t in kk["fracset"]
        m = (0.0 if frac else 2 * abs(sig[t]) / (h * Delta)) + bvec @ X @ bvec
        if pre == "rmax" and t >= s0 - Lpre:
            if m <= 0:
                diag["brk"] = t
                Ps[t] = Pl
            else:
                Ps[t] = Pl - np.outer(beta, beta) / m
        else:
            Ps[t] = Pl
    return Ps, diag
