"""Corner bound z_K for dumped SCIP corners.

Reduction.  In the space SCIP uses, q(s) = s^T Q s + b^T s + c.  With Q = V diag(th) V^T, the
nonzero-eigenvalue coordinates u = V_r^T s and the single linear coordinate l = b0^T s
(b0 = projection of b on ker Q) describe q completely:
  q = sum_i th_i u_i^2 + (V_r^T b)^T u + l + c        (l absent if b0 = 0).
So z_K is computed in dimension k' = rank Q + [b0 != 0] with projected rays.  By Theorem 4 of
the earlier note some minimizer uses at most rho = n_+ + n_0' + 1 - [b0 != 0] rays, where n_0' =
[b0 != 0] in the reduced space; i.e. rho = n_+ + 1 in all cases.

zK_upto2 : exact minimum over supports of size <= 2, vectorized over all pairs (closed form of
           core.two_ray: candidates are theta in {0, 1}, zeros of D, roots of D'^2 = 4 b'^2 D
           and of D' = 0), plus a 9-point grid in theta as a safety net (feasible points, so
           including them keeps the value an upper bound on z_K).
Every candidate point is verified independently (q recomputed at the point must be ~0, see
           _on_boundary); this removes values produced by cancellation in the closed form.
For rho <= 2 this is z_K (exact up to floating point).  For rho >= 3 it is an upper bound;
core.corner_bound (generic KKT for supports of size >= 3) or a global solve is then used.
"""
import os, sys
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)


def reduce_space(Q, b, c, sbar, P, eigtol=1e-9):
    th, V = np.linalg.eigh(Q)
    nz = np.abs(th) > eigtol
    Vr = V[:, nz]
    b0 = V[:, ~nz] @ (V[:, ~nz].T @ b)
    has_l = np.linalg.norm(b0) > 1e-12
    Qr = np.diag(th[nz])
    br = Vr.T @ b
    sr = Vr.T @ sbar
    Pr = Vr.T @ P
    if has_l:
        Qr = np.pad(Qr, ((0, 1), (0, 1)))
        br = np.append(br, 1.0)
        sr = np.append(sr, b0 @ sbar)
        Pr = np.vstack([Pr, b0 @ P])
    npos = int(np.sum(th > eigtol))
    return Qr, br, c, sr, Pr, npos + 1, npos


def one_ray_vec(Q, b, c, sbar, P):
    g0 = float(sbar @ Q @ sbar + b @ sbar + c)
    A = np.einsum('ij,ik,kj->j', P, Q, P)
    B = 2 * P.T @ (Q @ sbar + b / 2)
    t = np.full(P.shape[1], np.inf)
    lin = np.abs(A) <= 1e-15 * np.maximum(1.0, np.maximum(np.abs(B), g0))
    m = lin & (B < 0)
    t[m] = -g0 / B[m]
    q = ~lin
    disc = B * B - 4 * A * g0
    graze = q & (disc < 0) & (disc > -1e-12 * (B * B + np.abs(4 * A * g0)))
    disc = np.where(graze, 0.0, disc)
    ok = q & (disc >= 0)
    r = np.sqrt(np.where(ok, disc, 0.0))
    with np.errstate(divide='ignore', invalid='ignore'):
        qq = -0.5 * (B + np.copysign(r, B))
        r1 = qq / A
        r2 = g0 / qq
    lo = np.minimum(r1, r2); hi = np.maximum(r1, r2)
    # A > 0: feasible between the roots (both positive iff B < 0); A < 0: t >= larger root
    pos_case = ok & (A > 0) & (lo > 0)
    t[pos_case] = lo[pos_case]
    neg_case = ok & (A < 0) & (hi > 0)
    t[neg_case] = hi[neg_case]
    return t, g0


def _on_boundary(Q, b, c, sbar, D, tau, g0):
    """Independent check of candidate points x = sbar + tau D (columns): q(x) recomputed from
    scratch must be ~0.  Rejects candidates produced by cancellation in the closed form (a and bb
    both at rounding level, e.g. null directions of q or antiparallel scaled rays), where
    q(x) stays close to q(sbar) = g0 > 0."""
    X = sbar[:, None] + D * tau[None, :]
    QX = Q @ X
    quad = np.einsum('ij,ij->j', X, QX)
    lin = b @ X
    qv = quad + lin + c
    scale = np.abs(quad) + np.abs(lin) + abs(c)
    return qv <= 1e-3 * g0 + 1e-10 * scale


def _roots_quad_vec(a2, a1, a0):
    """Real roots (two arrays, nan where absent) of a2 t^2 + a1 t + a0, elementwise."""
    scale = np.maximum(np.maximum(np.abs(a2), np.abs(a1)), np.abs(a0))
    scale = np.where(scale == 0, 1.0, scale)
    a2, a1, a0 = a2 / scale, a1 / scale, a0 / scale
    r1 = np.full(a2.shape, np.nan); r2 = np.full(a2.shape, np.nan)
    lin = np.abs(a2) < 1e-13
    with np.errstate(divide='ignore', invalid='ignore'):
        lr = -a0 / a1
    m = lin & (np.abs(a1) >= 1e-13)
    r1[m] = lr[m]
    disc = a1 * a1 - 4 * a2 * a0
    disc = np.where((disc < 0) & (disc > -1e-10 * (a1 * a1 + np.abs(4 * a2 * a0))), 0.0, disc)
    q = (~lin) & (disc >= 0)
    r = np.sqrt(np.where(q, disc, 0.0))
    with np.errstate(divide='ignore', invalid='ignore'):
        qq = -0.5 * (a1 + np.copysign(r, a1))
        x1 = qq / a2
        x2 = a0 / qq
    x2 = np.where(qq == 0, x1, x2)
    r1[q] = x1[q]; r2[q] = x2[q]
    return r1, r2


def zK_upto2(Q, b, c, sbar, P, w, chunk=200000, grid=9):
    """Exact min over supports of size <= 2 (w > 0).  Returns (value, argmin support)."""
    N = P.shape[1]
    t1, g0 = one_ray_vec(Q, b, c, sbar, P)
    fin = np.isfinite(t1)
    if fin.any():
        ok = np.zeros(N, bool)
        ok[fin] = _on_boundary(Q, b, c, sbar, P[:, fin], t1[fin], g0)
        t1 = np.where(ok, t1, np.inf)
    v1 = w * t1
    j1 = int(np.argmin(v1)) if N else -1
    best = float(v1[j1]) if N else np.inf
    arg = (j1,)
    if N < 2:
        return best, arg
    g = 2 * P.T @ (Q @ sbar + b / 2)
    QP = Q @ P
    I, J = np.triu_indices(N, 1)
    thg = np.linspace(0, 1, grid)
    for s in range(0, len(I), chunk):
        ii, jj = I[s:s + chunk], J[s:s + chunk]
        Qii = np.einsum('ij,ij->j', P[:, ii], QP[:, ii])
        Qjj = np.einsum('ij,ij->j', P[:, jj], QP[:, jj])
        Qij = np.einsum('ij,ij->j', P[:, ii], QP[:, jj])
        wi, wj = w[ii], w[jj]
        gi, gj = g[ii], g[jj]
        Gii = np.einsum('ij,ij->j', P[:, ii], P[:, ii]) / wi ** 2       # Gram entries of p/w
        Gjj = np.einsum('ij,ij->j', P[:, jj], P[:, jj]) / wj ** 2
        Gij = np.einsum('ij,ij->j', P[:, ii], P[:, jj]) / (wi * wj)
        A0 = Qjj / wj ** 2
        A1 = 2 * (Qij / (wi * wj) - Qjj / wj ** 2)
        A2 = Qii / wi ** 2 - 2 * Qij / (wi * wj) + Qjj / wj ** 2
        B0 = gj / wj
        B1 = gi / wi - gj / wj
        D2 = B1 * B1 - 4 * g0 * A2
        D1 = 2 * B0 * B1 - 4 * g0 * A1
        D0 = B0 * B0 - 4 * g0 * A0
        cands = [np.zeros_like(A0), np.ones_like(A0)]
        cands += list(_roots_quad_vec(D2, D1, D0))
        cands += list(_roots_quad_vec(4 * D2 * D2 - 4 * B1 * B1 * D2, 4 * D1 * D2 - 4 * B1 * B1 * D1,
                                      D1 * D1 - 4 * B1 * B1 * D0))
        with np.errstate(divide='ignore', invalid='ignore'):
            cands.append(-D1 / (2 * D2))
        C = np.stack(cands, 1)                                  # (m, 7)
        C = np.where((C >= -1e-9) & (C <= 1 + 1e-9), np.clip(C, 0, 1), np.nan)
        C = np.concatenate([C, np.broadcast_to(thg, (len(ii), grid))], 1)

        def uplus(th):
            bb = B0[:, None] + B1[:, None] * th
            a = A0[:, None] + A1[:, None] * th + A2[:, None] * th * th
            D = D0[:, None] + D1[:, None] * th + D2[:, None] * th * th
            D = np.where((D < 0) & (D > -1e-12 * np.maximum(1.0, bb * bb)), 0.0, D)
            sq = np.sqrt(np.where(D >= 0, D, 0.0))
            with np.errstate(divide='ignore', invalid='ignore'):
                u = np.where(bb <= 0, (-bb + sq) / (2 * g0), -2 * a / (bb + sq))
                # guard: if bb and sqrt(D) are both at rounding level (P nu ~ 0, e.g. two
                # antiparallel projected rays), -2a/(bb + sq) is 0/0 noise; the true u+ is ~0
                tiny = (bb + sq) <= 1e-9 * (np.abs(B0) + np.abs(B1))[:, None]
                u = np.where(tiny, (-bb + sq) / (2 * g0), u)
                # direction P nu(theta) of relative length <= 1e-6 (antiparallel rays): treated as
                # no root; such directions cost >= 1e6 times more than the endpoint rays
                nrm2 = (th * th * Gii[:, None] + 2 * th * (1 - th) * Gij[:, None] + (1 - th) ** 2 * Gjj[:, None])
                zero = nrm2 <= 1e-12 * (Gii + Gjj)[:, None]
                u = np.where(zero, 0.0, u)
            u = np.where((D >= 0) & np.isfinite(th), u, -np.inf)
            return u
        U = uplus(C)
        good = U > 1e-300
        if not good.any():
            continue
        V = np.where(good, 1.0 / np.where(good, U, 1.0), np.inf)       # (m, ncand) candidate values
        flat = V.ravel()
        cand = np.where(flat < best)[0]
        if cand.size == 0:
            continue
        cand = cand[np.argsort(flat[cand])]
        ncols = V.shape[1]
        for s0 in range(0, cand.size, 256):                       # verify in increasing order
            cc = cand[s0:s0 + 256]
            pr, cl = cc // ncols, cc % ncols
            th = C[pr, cl]
            Dm = P[:, ii[pr]] * (th / wi[pr])[None, :] + P[:, jj[pr]] * ((1 - th) / wj[pr])[None, :]
            okv = _on_boundary(Q, b, c, sbar, Dm, flat[cc], g0)
            if okv.any():
                f = int(np.argmax(okv))
                best = float(flat[cc[f]]); arg = (int(ii[pr[f]]), int(jj[pr[f]]))
                break
    return best, arg


def zK_kkt3(Q, b, c, sbar, P, w, maxtriples=3_000_000):
    """Generic KKT minimum over supports of size 3 (as core.corner_bound); None if too many."""
    import itertools
    N = P.shape[1]
    from math import comb
    if comb(N, 3) > maxtriples:
        return None
    g0 = float(sbar @ Q @ sbar + b @ sbar + c)
    m_all = P.T @ (Q @ sbar + b / 2)
    G_all = P.T @ Q @ P
    best = np.inf
    T = np.array(list(itertools.combinations(range(N), 3)), int)
    for s in range(0, len(T), 200000):
        J = T[s:s + 200000]
        G = G_all[J[:, :, None], J[:, None, :]]
        det = np.linalg.det(G)
        ok = np.abs(det) > 1e-12 * np.maximum(1.0, np.abs(G).max(axis=(1, 2)) ** 3)
        if not ok.any():
            continue
        J, G = J[ok], G[ok]
        Gi = np.linalg.inv(G)
        wJ = w[J]; mJ = m_all[J]
        den = np.einsum('ni,nij,nj->n', wJ, Gi, wJ)
        num = np.einsum('ni,nij,nj->n', mJ, Gi, mJ) - g0
        with np.errstate(divide='ignore', invalid='ignore'):
            t2 = num / den
        okk = (np.abs(den) > 1e-14) & (t2 > 0)
        t = np.sqrt(np.where(okk, t2, 0.0))
        mu = -np.einsum('nij,nj->ni', Gi, mJ + t[:, None] * wJ)
        okk &= np.all(mu > -1e-12, 1)
        if not okk.any():
            continue
        mu = np.maximum(mu, 0)
        vals = np.einsum('ni,ni->n', wJ, mu)
        for idx in np.where(okk)[0][np.argsort(vals[okk])][:50]:
            pt = sbar + P[:, J[idx]] @ mu[idx]
            if pt @ Q @ pt + b @ pt + c <= 1e-8 * (1 + g0) and vals[idx] < best:
                best = float(vals[idx])
                break
    return best
