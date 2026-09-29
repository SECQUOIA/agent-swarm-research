"""Scratch library for the s-free-intersection-cuts scouting report.

S = {s in R^k : s^T Q s + b^T s + c <= 0}, a point sbar with q(sbar) > 0,
and n rays p_1..p_n in R^k (projections of the simplicial-cone rays onto the
variables of q).  Nonbasic costs w_j > 0.

* ms_set: the constant-Gamma maximal quadratic-free set used in SCIP
  (Munoz-Serrano 2022; Chmiela-Munoz-Serrano 2023, Section 3, Cases 1-4).
* ic_coeffs: intersection-cut coefficients a_j = 1/alpha_j for a set C.
* corner_bound: z_K(w) = min{w^T lam : lam >= 0, q(sbar + P lam) <= 0},
  computed exactly by enumerating supports of size <= rank(P) and solving
  the face KKT system (Lemma: optimal lam has support <= rank(P)).
"""
import itertools
import numpy as np

TOL = 1e-10


def qval(Q, b, c, s):
    return s @ Q @ s + b @ s + c


def ms_set(Q, b, c, sbar, lam=None):
    """Return G with C = {s : G(s) <= 0} maximal S-free and G(sbar) < 0.

    lam optionally overrides the default Gamma == lam choice (unit vector in
    the space of the 'x' (positive) coordinates of the relevant case)."""
    k = len(sbar)
    th, V = np.linalg.eigh(Q)
    bb = V.T @ b
    Ip = [i for i in range(k) if th[i] > 1e-9]
    Im = [i for i in range(k) if th[i] < -1e-9]
    I0 = [i for i in range(k) if abs(th[i]) <= 1e-9]
    kappa = c - 0.25 * sum(bb[i] ** 2 / th[i] for i in Ip + Im)
    bI0 = np.array([bb[i] for i in I0])

    def xyz(s):
        psi = V.T @ s
        x = np.array([np.sqrt(th[i]) * (psi[i] + bb[i] / (2 * th[i])) for i in Ip])
        y = np.array([np.sqrt(-th[i]) * (psi[i] + bb[i] / (2 * th[i])) for i in Im])
        z = np.array([psi[i] for i in I0])
        return x, y, z

    if len(Im) == 0 and (len(I0) == 0 or np.linalg.norm(bI0) < 1e-12):
        raise ValueError("convex quadratic: maximal S-free sets are halfspaces")
    if len(I0) == 0 or np.linalg.norm(bI0) < 1e-12:
        if len(Ip) == 0:
            # reverse convex with no linear part: closure of complement
            return lambda s: -qval(Q, b, c, s), 'revconvex'
        if abs(kappa) < 1e-12:  # Case 1
            xb, yb, _ = xyz(sbar)
            L = xb / np.linalg.norm(xb) if lam is None else lam
            return (lambda s: np.linalg.norm(xyz(s)[1]) - L @ xyz(s)[0]), 'case1'
        if kappa > 0:  # Case 2
            xb, yb, _ = xyz(sbar)
            v = np.append(xb, np.sqrt(kappa))
            L = v / np.linalg.norm(v) if lam is None else lam
            return (lambda s: np.linalg.norm(xyz(s)[1])
                    - L @ np.append(xyz(s)[0], np.sqrt(kappa))), 'case2'
        # Case 3
        xb, yb, _ = xyz(sbar)
        L = xb / np.linalg.norm(xb) if lam is None else lam
        if len(Ip) == 0:
            return lambda s: -qval(Q, b, c, s), 'revconvex'
        return (lambda s: np.linalg.norm(np.append(xyz(s)[1], np.sqrt(-kappa)))
                - L @ xyz(s)[0]), 'case3'
    # Case 4: linear part in zero-eigenvalue directions
    r = np.sqrt(1 + kappa ** 2)
    f = r ** 0.5

    def hat(s):
        x, y, z = xyz(s)
        wv = bI0 @ z
        xh = np.append(x / f, (wv + (kappa + r)) / (2 * f))
        yh = np.append(y / f, (wv + (kappa - r)) / (2 * f))
        return xh, yh

    xhb, _ = hat(sbar)
    L = xhb / np.linalg.norm(xhb) if lam is None else lam
    lt = L[-1]  # lambda_{p+ + 1}; a = -e_last so lambda^T a = -lt, d = e_last

    def phi(y):
        ny = np.linalg.norm(y)
        if -lt * ny + y[-1] <= 0:
            return ny
        return np.sqrt(max(0.0, (1 - lt ** 2) * (ny ** 2 - y[-1] ** 2))) + lt * y[-1]

    def G(s):
        xh, yh = hat(s)
        return phi(yh) - L @ xh
    return G, 'case4'


def step_length(G, sbar, p, amax=1e7):
    """sup{alpha >= 0 : G(sbar + alpha p) <= 0} (C convex, sbar in int C)."""
    if np.linalg.norm(p) < 1e-14:
        return np.inf
    if G(sbar + amax * p) <= 0:
        return np.inf
    lo, hi = 0.0, 1.0
    while G(sbar + hi * p) <= 0:
        lo, hi = hi, hi * 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if G(sbar + mid * p) <= 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-13 * max(1, hi):
            break
    return lo


def ic_bound(G, sbar, P, w):
    """Bound min{w^T lam : lam >= 0, sum a_j lam_j >= 1} of the intersection cut."""
    al = np.array([step_length(G, sbar, P[:, j]) for j in range(P.shape[1])])
    vals = [w[j] * al[j] for j in range(len(w)) if np.isfinite(al[j])]
    return (min(vals) if vals else np.inf), al


def corner_bound(Q, b, c, sbar, P, w, return_point=False):
    """Exact z_K = min{w^T lam : lam >= 0, q(sbar + P lam) <= 0}, w > 0."""
    k, n = P.shape
    rk = np.linalg.matrix_rank(P)
    mu0 = qval(Q, b, c, sbar)
    assert mu0 > 0
    best, arg = np.inf, None
    g = Q @ sbar + b / 2
    for size in range(1, rk + 1):
        for F in itertools.combinations(range(n), size):
            PF = P[:, F]
            if np.linalg.matrix_rank(PF) < size:
                continue
            M = PF.T @ Q @ PF
            m = PF.T @ g
            wF = w[list(F)]
            cands = []
            if size == 1:
                A_, B_, C_ = M[0, 0], 2 * m[0], mu0
                if abs(A_) < 1e-14:
                    if B_ < 0:
                        cands.append(np.array([-C_ / B_]))
                else:
                    disc = B_ ** 2 - 4 * A_ * C_
                    if disc >= 0:
                        for t in ((-B_ - np.sqrt(disc)) / (2 * A_), (-B_ + np.sqrt(disc)) / (2 * A_)):
                            if t > 0:
                                cands.append(np.array([t]))
            else:
                try:
                    Mi = np.linalg.inv(M)
                except np.linalg.LinAlgError:
                    continue
                den = wF @ Mi @ wF
                num = m @ Mi @ m - mu0
                if abs(den) < 1e-14:
                    continue
                s2 = num / den
                if s2 > 0:
                    for s in (np.sqrt(s2), -np.sqrt(s2)):
                        if s <= 0:
                            continue
                        mu = -Mi @ (m + s * wF)
                        cands.append(mu)
            for mu in cands:
                if np.all(mu > -1e-12):
                    lamv = np.zeros(n)
                    lamv[list(F)] = mu
                    if qval(Q, b, c, sbar + P @ lamv) <= 1e-7 * (1 + mu0):
                        v = w @ lamv
                        if v < best:
                            best, arg = v, lamv
    if return_point:
        return best, arg
    return best


def corner_bound_scip(Q, b, c, sbar, P, w, box=None, timelimit=60):
    """Same bound computed with SCIP (optionally with box l <= sbar+P lam <= u)."""
    import pyscipopt as ps
    k, n = P.shape
    m = ps.Model()
    m.hideOutput()
    m.setParam('limits/time', timelimit)
    lam = [m.addVar(lb=0, ub=1e4) for _ in range(n)]
    s = [sbar[i] + ps.quicksum(P[i, j] * lam[j] for j in range(n)) for i in range(k)]
    sv = [m.addVar(lb=None) for _ in range(k)]
    for i in range(k):
        m.addCons(sv[i] == s[i])
        if box is not None:
            sv[i].chgLb(box[0][i]) if False else None
    if box is not None:
        for i in range(k):
            m.chgVarLb(sv[i], box[0][i])
            m.chgVarUb(sv[i], box[1][i])
    expr = ps.quicksum(Q[i, j] * sv[i] * sv[j] for i in range(k) for j in range(k)) \
        + ps.quicksum(b[i] * sv[i] for i in range(k)) + c
    m.addCons(expr <= 0)
    m.setObjective(ps.quicksum(w[j] * lam[j] for j in range(n)), 'minimize')
    m.optimize()
    st = m.getStatus()
    if st == 'infeasible':
        return np.inf
    return m.getDualbound()
