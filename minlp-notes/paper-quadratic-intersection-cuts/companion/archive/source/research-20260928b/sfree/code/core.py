"""Core routines for the optimal-intersection-cut workstream.

Notation (see ../optimal-intersection-cuts.md):
  S = {s in R^k : q(s) = s^T Q s + b^T s + c <= 0}, sbar with q(sbar) > 0,
  projected rays P in R^{k x N}, reduced costs w in R^N_{>0}.
  X = {lam >= 0 : sbar + P lam in S},   z_K(w) = min{w^T lam : lam in X}.
  For a closed convex S-free C with sbar in int C, alpha_j = sup{t : sbar + t p_j in C}
  and the one-cut bound is z_C(w) = min_{alpha_j < inf} w_j alpha_j.
"""
import itertools
import numpy as np

TOL = 1e-12


def qval(Q, b, c, s):
    return float(s @ Q @ s + b @ s + c)


# ---------------------------------------------------------------------------
# Corner bound z_K by support enumeration (Lemma 2 / Theorem 3 of the note)
# ---------------------------------------------------------------------------

def _face_data(Q, b, c, sbar, P, J):
    PJ = P[:, list(J)]
    G = PJ.T @ Q @ PJ
    m = PJ.T @ (Q @ sbar + b / 2.0)
    g0 = qval(Q, b, c, sbar)
    return PJ, G, m, g0


def one_ray(Q, b, c, sbar, p):
    """Smallest t > 0 with q(sbar + t p) <= 0 (inf if none)."""
    g0 = qval(Q, b, c, sbar)
    A = float(p @ Q @ p)
    B = float(2 * p @ (Q @ sbar + b / 2.0))
    # A t^2 + B t + g0 <= 0, g0 > 0
    if abs(A) <= 1e-15 * max(1.0, abs(B), g0):
        return -g0 / B if B < 0 else np.inf
    disc = B * B - 4 * A * g0
    if disc < 0:
        if disc > -1e-12 * (B * B + abs(4 * A * g0)):
            disc = 0.0          # grazing ray (double root): the ray touches dS
        else:
            return np.inf
    r = np.sqrt(disc)
    qq = -0.5 * (B + np.copysign(r, B)) if B != 0 else -0.5 * r
    roots = sorted([qq / A, g0 / qq] if qq != 0 else [(-B - r) / (2 * A), (-B + r) / (2 * A)])
    pos = [t for t in roots if t > 0]
    if not pos:
        return np.inf
    if A > 0:
        return pos[0]            # feasible between the roots; both roots >0 iff B<0
    # A < 0: feasible outside the roots; g0>0 means 0 lies between roots
    return roots[1] if roots[1] > 0 else np.inf


def two_ray(Q, b, c, sbar, P, i, j, w):
    """Exact min{w_i mu_i + w_j mu_j : mu >= 0, q(sbar + mu_i p_i + mu_j p_j) <= 0}.

    Parametrize the level-tau segment mu = tau * nu(theta), nu = (theta/w_i, (1-theta)/w_j).
    q(sbar + tau P nu) = a(theta) tau^2 + bb(theta) tau + g0.  With u = 1/tau the feasible
    u form [u-, u+] and the best tau is 1/max_theta u+(theta).  u+ is maximized at
    theta in {0, 1}, at zeros of the discriminant D, or at roots of D'^2 = 4 bb'^2 D.
    Returns (value, lam_i, lam_j)."""
    g0 = qval(Q, b, c, sbar)
    pi, pj = P[:, i], P[:, j]
    gi = float(2 * pi @ (Q @ sbar + b / 2.0)); gj = float(2 * pj @ (Q @ sbar + b / 2.0))
    Qii, Qjj, Qij = float(pi @ Q @ pi), float(pj @ Q @ pj), float(pi @ Q @ pj)
    wi, wj = w[i], w[j]
    # nu = (theta/wi, (1-theta)/wj) ; a(theta) = nu^T G nu ; bb(theta) = g^T nu
    # write nu = e0 + theta*e1 with e0 = (0, 1/wj), e1 = (1/wi, -1/wj)
    e0 = np.array([0.0, 1.0 / wj]); e1 = np.array([1.0 / wi, -1.0 / wj])
    G = np.array([[Qii, Qij], [Qij, Qjj]]); g = np.array([gi, gj])
    A0, A1, A2 = e0 @ G @ e0, 2 * e0 @ G @ e1, e1 @ G @ e1
    B0, B1 = g @ e0, g @ e1
    # D = bb^2 - 4 g0 a
    D2 = B1 * B1 - 4 * g0 * A2; D1 = 2 * B0 * B1 - 4 * g0 * A1; D0 = B0 * B0 - 4 * g0 * A0
    cands = [0.0, 1.0]
    for coeffs in ([D2, D1, D0],
                   # stationarity D' = 2 bb' sqrt(D), squared: (D1 + 2 D2 th)^2 - 4 B1^2 (D2 th^2 + D1 th + D0) = 0
                   [4 * D2 * D2 - 4 * B1 * B1 * D2, 4 * D1 * D2 - 4 * B1 * B1 * D1, D1 * D1 - 4 * B1 * B1 * D0],
                   # D' = 0 (exact stationarity when B1 = 0)
                   [0.0, 2 * D2, D1]):
        cands.extend(real_roots_quadratic(*coeffs))
    cands = [min(1.0, max(0.0, t)) for t in cands if -1e-9 <= t <= 1 + 1e-9]

    def uplus(th):
        bb = B0 + B1 * th
        a_th = A0 + A1 * th + A2 * th * th
        D = D0 + D1 * th + D2 * th * th
        if D < 0:
            if D > -1e-12 * max(1.0, bb * bb):
                D = 0.0                       # tangential contact
            else:
                return -np.inf
        sq = np.sqrt(D)
        # numerically stable larger root of g0 u^2 + bb u + a = 0
        return (-bb + sq) / (2 * g0) if bb <= 0 else -2 * a_th / (bb + sq)

    best_u, best_th = -np.inf, None
    for th in cands:
        u = uplus(th)
        if u > best_u:
            best_u, best_th = u, th
    # safety net: grid + golden-section refinement (detects missed stationary points)
    grid = np.linspace(0.0, 1.0, 257)
    gv = np.array([uplus(t) for t in grid])
    kmax = int(np.argmax(gv))
    if np.isfinite(gv[kmax]):
        lo, hi = grid[max(0, kmax - 1)], grid[min(len(grid) - 1, kmax + 1)]
        gr = (np.sqrt(5) - 1) / 2
        for _ in range(80):
            m1 = hi - gr * (hi - lo); m2 = lo + gr * (hi - lo)
            if uplus(m1) >= uplus(m2):
                hi = m2
            else:
                lo = m1
        tg = 0.5 * (lo + hi); ug = uplus(tg)
        if ug > best_u + 1e-9 * max(1.0, abs(best_u)):
            TWO_RAY_WARN[0] += 1
            best_u, best_th = ug, tg
    if best_u <= 1e-300:
        return np.inf, None, None
    tau = 1.0 / best_u
    return tau, tau * best_th / wi, tau * (1 - best_th) / wj


TWO_RAY_WARN = [0]


def real_roots_quadratic(a2, a1, a0):
    """Real roots of a2 t^2 + a1 t + a0 (tolerant to tiny negative discriminants)."""
    scale = max(abs(a2), abs(a1), abs(a0))
    if scale == 0:
        return []
    a2, a1, a0 = a2 / scale, a1 / scale, a0 / scale
    if abs(a2) < 1e-13:
        return [] if abs(a1) < 1e-13 else [-a0 / a1]
    disc = a1 * a1 - 4 * a2 * a0
    if disc < 0:
        if disc > -1e-10 * (a1 * a1 + abs(4 * a2 * a0)):
            disc = 0.0
        else:
            return []
    r = np.sqrt(disc)
    qq = -0.5 * (a1 + np.copysign(r, a1)) if a1 != 0 else -0.5 * r
    if qq == 0:
        return [0.0, 0.0] if a0 == 0 else [np.sqrt(-a0 / a2)] * 2 if -a0 / a2 >= 0 else []
    return [qq / a2, a0 / qq]


def corner_bound(Q, b, c, sbar, P, w, max_support=None, return_point=False):
    """z_K(w) for w > 0 by support enumeration.  Supports of size 1 and 2 are solved
    exactly (closed form); supports of size >= 3 use the generic face-KKT formula
    (nonsingular face Hessian), which is exact for generic data."""
    k, N = P.shape
    r = np.linalg.matrix_rank(P)
    if max_support is None:
        max_support = r
    g0 = qval(Q, b, c, sbar)
    assert g0 > 0
    best, arg = np.inf, None
    for j in range(N):
        t = one_ray(Q, b, c, sbar, P[:, j])
        if w[j] * t < best:
            best = w[j] * t; arg = np.zeros(N); arg[j] = t
    if max_support >= 2:
        for i, j in itertools.combinations(range(N), 2):
            v, li, lj = two_ray(Q, b, c, sbar, P, i, j, w)
            if v < best:
                best = v; arg = np.zeros(N); arg[i] = li; arg[j] = lj
    # generic KKT for supports of size >= 3
    for size in range(3, max_support + 1):
        for J in itertools.combinations(range(N), size):
            PJ, G, m, _ = _face_data(Q, b, c, sbar, P, J)
            if np.linalg.matrix_rank(PJ) < size:
                continue
            try:
                Gi = np.linalg.inv(G)
            except np.linalg.LinAlgError:
                continue
            wJ = w[list(J)]
            # g(mu) = mu^T G mu + 2 m^T mu + g0 ; KKT: w = -sigma (2 G mu + 2 m) -> mu = -Gi (m + t w), t = 1/(2 sigma)
            den = wJ @ Gi @ wJ
            num = m @ Gi @ m - g0
            if abs(den) < 1e-14:
                continue
            t2 = num / den
            if t2 <= 0:
                continue
            t = np.sqrt(t2)
            mu = -Gi @ (m + t * wJ)
            if np.all(mu > -1e-12):
                lam = np.zeros(N); lam[list(J)] = np.maximum(mu, 0)
                if qval(Q, b, c, sbar + P @ lam) <= 1e-8 * (1 + g0):
                    v = w @ lam
                    if v < best:
                        best, arg = v, lam
    return (best, arg) if return_point else best


# ---------------------------------------------------------------------------
# Bilinear constraints: det representation and the sliced orbit family
# ---------------------------------------------------------------------------

def bilinear_quadratic(side):
    """side '+' : S = {w <= x y}  (q = w - x y);   side '-' : S = {w >= x y} (q = x y - w).
    Variables s = (x, y, w)."""
    Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = -0.5
    b = np.array([0.0, 0.0, 1.0])
    if side == '-':
        Q, b = -Q, -b
    return Q, b, 0.0


def Mmat(side, s, h=1.0):
    """2x2 matrix with det M(s,1) = q(s).  Linear in (s, h)."""
    x, y, w = s
    if side == '+':
        return np.array([[w, x], [y, h]])
    return np.array([[x, w], [h, y]])


def in_CF(F, side, s, tol=0.0):
    X = F.T @ Mmat(side, s)
    X = (X + X.T) / 2
    return np.linalg.eigvalsh(X)[0] >= -tol


def step_CF(F, side, sbar, p):
    """sup{alpha >= 0 : sym(F^T M(sbar + alpha p)) >= 0}; requires sym(F^T M(sbar)) > 0."""
    A = F.T @ Mmat(side, sbar); A = (A + A.T) / 2
    lmin = np.linalg.eigvalsh(A)[0]; floor = 1e-9 * max(1.0, np.abs(A).max())
    if lmin <= floor:
        F = F + (floor - lmin) * np.linalg.inv(Mmat(side, sbar)).T
        A = F.T @ Mmat(side, sbar); A = (A + A.T) / 2
    B = F.T @ Mmat(side, p, h=0.0); B = (B + B.T) / 2
    L = np.linalg.cholesky(A)
    Li = np.linalg.inv(L)
    ev = np.linalg.eigvalsh(Li @ B @ Li.T)
    mn = ev[0]
    return np.inf if mn >= 0 else -1.0 / mn


def orbit_bound_of(F, side, sbar, P, w):
    al = np.array([step_CF(F, side, sbar, P[:, j]) for j in range(P.shape[1])])
    vals = [w[j] * al[j] for j in range(len(w)) if np.isfinite(al[j])]
    return (min(vals) if vals else np.inf), al


def orbit_feasible(side, pts_strict, pts, solver='CLARABEL'):
    """Find F with sym(F^T M(t)) >= I at pts_strict and >= 0 at pts (None if infeasible)."""
    import cvxpy as cp
    F = cp.Variable((2, 2))
    cons = []
    for t in pts_strict:
        M = Mmat(side, t)
        X = F.T @ M
        cons.append((X + X.T) / 2 >> np.eye(2))
    for t in pts:
        M = Mmat(side, t)
        X = F.T @ M
        cons.append((X + X.T) / 2 >> 0)
    prob = cp.Problem(cp.Minimize(cp.norm(F, 'fro')), cons)
    try:
        prob.solve(solver=solver)
    except Exception:
        return None
    if prob.status not in ('optimal', 'optimal_inaccurate'):
        return None
    return F.value


def best_orbit_bound(side, sbar, P, w, zhi, iters=40):
    """Best one-cut bound over the sliced orbit family {C_F : det F > 0} by bisection
    (quasi-convexity: {F : C_F contains T_z} is a convex cone).  Returns a certified
    lower bound (bound of an explicit F) and the bisection upper value."""
    lo, hi = 0.0, 1.0                       # bisection on z / zhi (better scaling)
    bestF = orbit_feasible(side, [sbar], [])
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        pts = [sbar + (mid * zhi / w[j]) * P[:, j] for j in range(P.shape[1])]
        F = orbit_feasible(side, [sbar], pts)
        if F is not None:
            lo, bestF = mid, F
        else:
            hi = mid
    try:
        cert = orbit_bound_of(bestF, side, sbar, P, w)[0] if bestF is not None else 0.0
    except np.linalg.LinAlgError:          # solver returned sym(F^T M(sbar)) only PSD
        cert = 0.0
    return cert, hi * zhi, bestF
