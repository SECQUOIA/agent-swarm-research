"""Interval branch-and-bound for E-CG separation at a fixed point z with M(z) positive definite.

F(v0,v) = floor(v0^2) + sum_i x_i ceil(p_i) + sum_{i<j} X_ij ceil(q_ij),
p_i = v_i^2 + 2 v_i v0,  q_ij = 2 v_i v_j.  We look for F < 0.

Identity: q_M(v) := (v0,v)^T M (v0,v) = v0^2 + sum x_i p_i + sum X_ij q_ij, hence
   F = q_M(v) + sum x_i rho(p_i) + sum X_ij rho(q_ij) - frac(v0^2),   rho(t) = ceil(t) - t in [0,1).
Consequences: F < 0 needs q_M < 1 (ellipsoid), and (v0,v) ~ -(v0,v) lets us take v0 >= 0.
Lower bounds on a box (exact ranges of each p_i, q_ij, v0^2 over the box are computed):
   LB1 = floor(min v0^2) + sum x_i ceil(min p_i) + sum X_ij ceil(min q_ij)      (monotonicity)
   LB3 = min q_M + sum x_i min rho(p_i) + sum X_ij min rho(q_ij) - max frac(v0^2)
where min q_M over the box is bounded below by q(c) - 2 sum_k |(Mc)_k| h_k (c centre, h half-widths).
Boxes are pruned when max(LB1, LB3) >= 0.  If no p_i, q_ij (with positive weight) or v0^2 crosses
an integer on the box, F is constant there and LB1 is exact.  Boxes narrower than minw with a
negative bound are reported as 'candidates' (they sit on integer surfaces; check them exactly).
Depth-first in batches to bound memory.
"""
import numpy as np
from bh import pairs, moment_matrix


def _rho_min(lo, hi):
    """min over [lo,hi] of ceil(t)-t: 0 if the interval contains an integer, else ceil(lo)-hi."""
    cl = np.ceil(lo)
    return np.where(cl <= hi, 0.0, cl - hi)


def box_bounds(n, z, lo, hi, M, P):
    x = z[:n]
    X = z[n:]
    l0, h0 = lo[:, 0], hi[:, 0]
    s_lo, s_hi = l0 ** 2, h0 ** 2           # v0 >= 0
    LB1 = np.floor(s_lo)
    const = (np.floor(s_lo) == np.floor(s_hi)) & (np.floor(s_hi) != s_hi)
    rsum = np.zeros(lo.shape[0])
    for i in range(n):
        li, ui = lo[:, i + 1], hi[:, i + 1]
        corners = np.stack([li * li + 2 * li * l0, li * li + 2 * li * h0,
                            ui * ui + 2 * ui * l0, ui * ui + 2 * ui * h0], 1)
        pmin = corners.min(1)
        pmax = corners.max(1)
        for vv0 in (l0, h0):
            inside = (-vv0 >= li) & (-vv0 <= ui)
            pmin = np.where(inside, np.minimum(pmin, -vv0 ** 2), pmin)
        if x[i] != 0:
            LB1 = LB1 + x[i] * np.ceil(pmin)
            rsum = rsum + x[i] * _rho_min(pmin, pmax)
            const &= (np.ceil(pmin) == np.ceil(pmax))
    for k, (i, j) in enumerate(P):
        if X[k] == 0:
            continue
        a1, b1, a2, b2 = lo[:, i + 1], hi[:, i + 1], lo[:, j + 1], hi[:, j + 1]
        c = np.stack([a1 * a2, a1 * b2, b1 * a2, b1 * b2], 1) * 2
        qmin, qmax = c.min(1), c.max(1)
        LB1 = LB1 + X[k] * np.ceil(qmin)
        rsum = rsum + X[k] * _rho_min(qmin, qmax)
        const &= (np.ceil(qmin) == np.ceil(qmax))
    cen = (lo + hi) / 2
    h = (hi - lo) / 2
    Mc = cen @ M
    qlb = np.einsum('ij,ij->i', cen, Mc) - 2 * np.sum(np.abs(Mc) * h, 1)
    fracmax = np.where(np.floor(s_lo) == np.floor(s_hi), s_hi - np.floor(s_hi), 1.0)
    LB3 = qlb + rsum - fracmax
    return LB1, np.maximum(LB1, LB3), const, qlb


def bnb(n, z, minw=1e-7, maxboxes=10 ** 8, tol=1e-9, batch=200000, verbose=False):
    P = pairs(n)
    M = moment_matrix(n, z)
    Minv = np.linalg.inv(M)
    r = np.sqrt(np.diag(Minv)) * (1 + 1e-9)
    stack_lo = [np.array([[0.0] + list(-r[1:])])]
    stack_hi = [np.array([list(r)])]
    processed = 0
    best_exact = (np.inf, None)
    candidates = []
    while stack_lo:
        lo, hi = stack_lo.pop(), stack_hi.pop()
        if lo.shape[0] > batch:
            stack_lo.append(lo[batch:]); stack_hi.append(hi[batch:])
            lo, hi = lo[:batch], hi[:batch]
        LB1, LB, const, qlb = box_bounds(n, z, lo, hi, M, P)
        processed += lo.shape[0]
        keep = (LB < -tol) & (qlb < 1)
        ex = keep & const
        if ex.any():
            k = np.argmin(np.where(ex, LB1, np.inf))
            if LB1[k] < best_exact[0]:
                best_exact = (LB1[k], (lo[k] + hi[k]) / 2)
        keep &= ~const
        lo, hi, LBk = lo[keep], hi[keep], LB[keep]
        w = hi - lo
        small = w.max(1) < minw
        if small.any():
            candidates += list(zip(LBk[small], lo[small], hi[small]))
            lo, hi, w = lo[~small], hi[~small], w[~small]
        if processed > maxboxes:
            return dict(status="limit", best=best_exact, cand=candidates, processed=processed)
        if lo.shape[0] == 0:
            continue
        d = np.argmax(w, 1)
        idx = np.arange(len(d))
        mid = (lo[idx, d] + hi[idx, d]) / 2
        lo2, hi2 = lo.copy(), hi.copy()
        hi[idx, d] = mid
        lo2[idx, d] = mid
        stack_lo.append(np.vstack([lo, lo2]))
        stack_hi.append(np.vstack([hi, hi2]))
        if verbose and processed % (50 * batch) < batch:
            print(processed, sum(s.shape[0] for s in stack_lo), best_exact[0], len(candidates), flush=True)
    return dict(status="done", best=best_exact, cand=candidates, processed=processed)
