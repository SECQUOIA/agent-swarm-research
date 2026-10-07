"""Shared routines for the multiround stream.

Reuses (read-only, via sys.path) the code of research-20260928b/sfree/code:
  exp_mccormick  instance generator and LP helpers (HiGHS),
  core           bilinear_quadratic, Mmat, corner_bound (reference implementation),
  scout_sfree    ms_set / step_length (Python model of SCIP's Case-4 set),
  bilinear       step_B (completion (B)).
New here:
  zk_vec         vectorized exact corner bound for one bilinear term (supports <= 2,
                 sufficient by Theorem 4 of the sfree note, rho = 2), checked against
                 core.corner_bound by check_zk.py;
  conedepth      distance from the vertex to K cap {cut}, and pointedness of the cone.
"""
import os
import sys
import numpy as np
import scipy.sparse as sp
import clarabel

HERE = os.path.dirname(os.path.abspath(__file__))
SFREE = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'research-20260928b', 'sfree', 'code'))
if SFREE not in sys.path:
    sys.path.insert(0, SFREE)
import exp_mccormick as E          # noqa: E402
from core import bilinear_quadratic, Mmat   # noqa: E402
from scout_sfree import ms_set, step_length  # noqa: E402
import fastorbit as FO              # noqa: E402

_SET = clarabel.DefaultSettings(); _SET.verbose = False


# ----------------------------------------------------------------------------- z_K
def _uplus(th, B0, B1, A0, A1, A2, D0, D1, D2, g0):
    bb = B0 + B1 * th
    a = A0 + A1 * th + A2 * th * th
    D = D0 + D1 * th + D2 * th * th
    tang = (D < 0) & (D > -1e-12 * np.maximum(1.0, bb * bb))
    D = np.where(tang, 0.0, D)
    bad = D < 0
    sq = np.sqrt(np.where(bad, 0.0, D))
    with np.errstate(divide='ignore', invalid='ignore'):
        u = np.where(bb <= 0, (-bb + sq) / (2 * g0), -2 * a / (bb + sq))
    return np.where(bad, -np.inf, u)


def _roots(a2, a1, a0):
    """Real roots of a2 t^2 + a1 t + a0 (vectorized, same tolerances as core)."""
    sc = np.maximum(np.maximum(np.abs(a2), np.abs(a1)), np.abs(a0))
    sc = np.where(sc == 0, 1.0, sc)
    a2, a1, a0 = a2 / sc, a1 / sc, a0 / sc
    lin = np.abs(a2) < 1e-13
    disc = a1 * a1 - 4 * a2 * a0
    disc = np.where((disc < 0) & (disc > -1e-10 * (a1 * a1 + np.abs(4 * a2 * a0))), 0.0, disc)
    ok = (disc >= 0) & ~lin
    r = np.sqrt(np.where(ok, disc, 0.0))
    qq = -0.5 * (a1 + np.copysign(r, a1))
    qq = np.where(a1 == 0, -0.5 * r, qq)
    with np.errstate(divide='ignore', invalid='ignore'):
        r1 = np.where(ok, qq / a2, np.nan)
        r2 = np.where(ok & (qq != 0), a0 / qq, np.nan)
        rl = np.where(lin & (np.abs(a1) >= 1e-13), -a0 / a1, np.nan)
    return [r1, r2, rl]


def zk_vec(side, sbar, P, w, return_point=False):
    """Exact z_K(w) = min{w^T lam : lam >= 0, q(sbar + P lam) <= 0} for a bilinear term,
    w > 0, by enumerating supports of size 1 and 2 (closed forms of core.one_ray /
    core.two_ray, vectorized over all rays and pairs)."""
    Q, b, c = bilinear_quadratic(side)
    g0 = float(sbar @ Q @ sbar + b @ sbar + c)
    assert g0 > 0
    N = P.shape[1]
    hvec = Q @ sbar + b / 2.0
    g = 2 * (P.T @ hvec)                  # linear coefficients per ray
    G = P.T @ Q @ P
    # one ray: A t^2 + B t + g0 <= 0
    A = np.diag(G).copy(); B = g.copy()
    t1 = np.full(N, np.inf)
    for j in range(N):                    # cheap, keep the exact scalar logic
        Aj, Bj = A[j], B[j]
        if abs(Aj) <= 1e-15 * max(1.0, abs(Bj), g0):
            t1[j] = -g0 / Bj if Bj < 0 else np.inf
            continue
        disc = Bj * Bj - 4 * Aj * g0
        if disc < 0:
            if disc > -1e-12 * (Bj * Bj + abs(4 * Aj * g0)):
                disc = 0.0
            else:
                continue
        r = np.sqrt(disc)
        qq = -0.5 * (Bj + np.copysign(r, Bj)) if Bj != 0 else -0.5 * r
        roots = sorted([qq / Aj, g0 / qq] if qq != 0 else [(-Bj - r) / (2 * Aj), (-Bj + r) / (2 * Aj)])
        pos = [t for t in roots if t > 0]
        if not pos:
            continue
        t1[j] = pos[0] if Aj > 0 else (roots[1] if roots[1] > 0 else np.inf)
    v1 = w * t1
    jb = int(np.argmin(v1)); best = v1[jb]
    arg = np.zeros(N)
    if np.isfinite(best):
        arg[jb] = t1[jb]
    if N >= 2:
        I, J = np.triu_indices(N, 1)
        wi, wj = w[I], w[J]
        Qii, Qjj, Qij = G[I, I], G[J, J], G[I, J]
        gi, gj = g[I], g[J]
        A0 = Qjj / wj ** 2
        A1 = 2 * (Qij / (wi * wj) - Qjj / wj ** 2)
        A2 = Qii / wi ** 2 - 2 * Qij / (wi * wj) + Qjj / wj ** 2
        B0 = gj / wj; B1 = gi / wi - gj / wj
        D2 = B1 * B1 - 4 * g0 * A2; D1 = 2 * B0 * B1 - 4 * g0 * A1; D0 = B0 * B0 - 4 * g0 * A0
        args = (B0, B1, A0, A1, A2, D0, D1, D2, g0)
        cands = [np.zeros_like(A0), np.ones_like(A0)]
        for co in ([D2, D1, D0],
                   [4 * D2 * D2 - 4 * B1 * B1 * D2, 4 * D1 * D2 - 4 * B1 * B1 * D1, D1 * D1 - 4 * B1 * B1 * D0],
                   [np.zeros_like(D2), 2 * D2, D1]):
            cands += _roots(*co)
        best_u = np.full(A0.shape, -np.inf); best_th = np.zeros(A0.shape)
        for th in cands:
            okc = np.isfinite(th) & (th >= -1e-9) & (th <= 1 + 1e-9)
            thc = np.clip(np.where(okc, th, 0.0), 0.0, 1.0)
            u = np.where(okc, _uplus(thc, *args), -np.inf)
            upd = u > best_u
            best_u = np.where(upd, u, best_u); best_th = np.where(upd, thc, best_th)
        # grid + golden-section safety net (as in core.two_ray)
        grid = np.linspace(0.0, 1.0, 257)
        GV = _uplus(grid[None, :], *[a[:, None] if np.ndim(a) else a for a in args])
        km = np.argmax(GV, axis=1)
        fin = np.isfinite(GV[np.arange(len(km)), km])
        lo = grid[np.maximum(0, km - 1)]; hi = grid[np.minimum(256, km + 1)]
        gr = (np.sqrt(5) - 1) / 2
        for _ in range(80):
            m1 = hi - gr * (hi - lo); m2 = lo + gr * (hi - lo)
            left = _uplus(m1, *args) >= _uplus(m2, *args)
            hi = np.where(left, m2, hi); lo = np.where(left, lo, m1)
        tg = 0.5 * (lo + hi); ug = _uplus(tg, *args)
        upd = fin & (ug > best_u + 1e-9 * np.maximum(1.0, np.abs(best_u)))
        best_u = np.where(upd, ug, best_u); best_th = np.where(upd, tg, best_th)
        with np.errstate(divide='ignore'):
            tau = np.where(best_u > 1e-300, 1.0 / np.where(best_u > 1e-300, best_u, 1.0), np.inf)
        # collinear projected rays span a ray or a line: the pair adds nothing to the one-ray
        # values, and its closed form is 0/0-unstable (spurious values, see check_zk.py)
        nI = np.linalg.norm(P[:, I], axis=0); nJ = np.linalg.norm(P[:, J], axis=0)
        cr = np.linalg.norm(np.cross(P[:, I].T, P[:, J].T), axis=1)
        tau = np.where(cr <= 1e-9 * nI * nJ, np.inf, tau)
        # safety net: accept the best pair whose point is feasible (q <= 1e-9 q(sbar))
        for kb in np.argsort(tau):
            if not tau[kb] < best:
                break
            lam = np.zeros(N)
            lam[I[kb]] = tau[kb] * best_th[kb] / wi[kb]; lam[J[kb]] = tau[kb] * (1 - best_th[kb]) / wj[kb]
            s = sbar + P @ lam
            if float(s @ Q @ s + b @ s + c) <= 1e-9 * g0:
                best, arg = tau[kb], lam
                break
            ZK_REJECT[0] += 1
    return (best, arg) if return_point else best


ZK_REJECT = [0]   # number of rejected (infeasible) pair candidates, for the record


def first_hits(side, sbar, P):
    """t_j = first hit of ray j with S (inf if it misses)."""
    N = P.shape[1]
    return np.array([zk_vec(side, sbar, P[:, [j]], np.ones(1)) for j in range(N)])


# ----------------------------------------------------------------------------- sets
def scip_alpha(side, sbar, P):
    Q, b, c = bilinear_quadratic(side)
    G, _ = ms_set(Q, b, c, sbar)
    return np.array([step_length(G, sbar, P[:, j]) for j in range(P.shape[1])])


def floor_pos(u):
    return np.maximum(u, 1e-9 * max(1.0, float(np.max(u))))


def orbit_alpha(side, sbar, P, u, iters=25):
    """Best orbit set for weights u (floored as in exp_loop.py).  Returns (alpha, F, zK(u))."""
    u = floor_pos(u)
    zk = zk_vec(side, sbar, P, u)
    _, _, F = FO.best_orbit(side, sbar, P, u, min(zk, 1e6), iters=iters)
    if F is None:
        return None, None, zk
    return FO.steps_A(F, side, sbar, P), F, zk


def inv(al):
    return np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al])


# ----------------------------------------------------------------------------- geometry
def _qp_min_norm(R, a):
    """min ||R lam||^2 s.t. lam >= 0, a^T lam >= 1 (Clarabel).  Returns sqrt(value)."""
    N = R.shape[1]
    H = sp.csc_matrix(2 * (R.T @ R) + 1e-12 * np.eye(N))
    q = np.zeros(N)
    A = sp.csc_matrix(np.vstack([-np.eye(N), -a[None, :]]))
    bvec = np.concatenate([np.zeros(N), [-1.0]])
    sol = clarabel.DefaultSolver(H, q, A, bvec, [clarabel.NonnegativeConeT(N + 1)], _SET).solve()
    if str(sol.status) not in ('Solved', 'AlmostSolved'):
        return np.nan
    lam = np.maximum(np.array(sol.x), 0)
    return float(np.linalg.norm(R @ lam))


def conedepth(R, a):
    """dist(xbar, K cap {a^T lam >= 1}) in x-space (how far the cut pushes the LP locally)."""
    return _qp_min_norm(R, a)


def pointedness(R):
    """gamma = dist(0, conv{r_j/||r_j||}) (0 for a half-space-like flat cone)."""
    U = R / np.linalg.norm(R, axis=0)
    return _qp_min_norm(U, np.ones(U.shape[1]))
