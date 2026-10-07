"""Decomposition-aware branch and bound for chain (path) problems.

    F(x) = sum_i phi_i(x_i) + sum_e psi_e(x_e, x_{e+1}),   x in prod_i [lo_i, hi_i].

Each variable's interval is partitioned into cells. Every iteration:
  1. A rigorous constant lower bound is computed for every unary piece on every
     surviving cell and for every pair piece on every product of adjacent
     surviving cells (problem-supplied bounding routines).
  2. Forward and backward min-sum dynamic programming over the path gives the
     global DP lower bound and, for every cell, the min-marginal: the smallest
     DP path sum through that cell (a valid lower bound on F over
     {x : x_i in cell}).
  3. The upper bound comes from local optimization started at the midpoints of
     the cells on the DP argmin path.
  4. Cells whose min-marginal is >= UB - eps are pruned (their marginal is kept
     as a certified bound on the removed region); every other cell is bisected.

Reparametrization ("transfers"). For every edge e and each endpoint, a
univariate function tau(x) = rho x^2 - alpha x is added to psi_e and subtracted
from the unary piece of that endpoint. The sum of all pieces is unchanged
(exact identity), so bounds stay valid for any transfer parameters. Modes:
  plain  : no transfers (constant bounds; first-order copy error),
  affine : linear transfers only (Lagrangian multipliers from the incumbent),
  quad   : rho = |d2 psi/dx dy| / 2 on both sides plus linear terms that make
           every pair piece stationary at the incumbent.

Problem interface (vectorized over cells):
  n, lo, hi, F(x), local_opt(x0) -> (x, f),
  pair_grad(x) -> (dpsi/dx_e, dpsi/dx_{e+1}) per edge,
  pair_cross() -> |d2 psi_e / dx dy| (used only by mode quad),
  unary_lb(i, p, q, Qt, Lt) -> LB of phi_i(x) - Qt x^2 + Lt x on [p, q],
  pair_lb(e, p, q, s, t, rhoL, alpha, rhoR, beta)
      -> LB of psi_e(x, y) + rhoL x^2 - alpha x + rhoR y^2 - beta y on [p,q]x[s,t].
Optional: hessian_is_pd_on_box(lo, hi) for the localization certificate.
"""
import time
import numpy as np

FP_REL = 1e-13  # safety margin factor for floating-point rounding in piece bounds


def quad_box_min(A, B, C, D, E, p, q, s, t):
    """Exact minimum of A x^2 + B x y + C y^2 + D x + E y over [p,q] x [s,t]
    (vectorized), minus a floating-point safety margin.

    The minimum of a continuous function on a compact box is attained. If it is
    attained in the interior, the gradient vanishes there; if the Hessian is
    positive definite that point is the unique stationary point; if the Hessian
    is singular or indefinite an interior minimizer (if any) lies on a line or
    is impossible, so a boundary minimizer also exists. On each edge the
    function is a univariate quadratic whose minimum is at an endpoint or at
    the clipped vertex. Hence the candidate set {corners, edge minimizers,
    interior stationary point if Hessian PD} contains a global minimizer.
    """
    def val(x, y):
        return A * x * x + B * x * y + C * y * y + D * x + E * y

    best = np.minimum(np.minimum(val(p, s), val(p, t)), np.minimum(val(q, s), val(q, t)))
    # edges x = const: minimize C y^2 + (B x + E) y over [s, t]
    with np.errstate(divide="ignore", invalid="ignore"):
        for xe in (p, q):
            yv = np.where(C > 0, np.clip(-(B * xe + E) / (2 * C), s, t), s)
            best = np.minimum(best, val(xe, yv))
        for ye in (s, t):
            xv = np.where(A > 0, np.clip(-(B * ye + D) / (2 * A), p, q), p)
            best = np.minimum(best, val(xv, ye))
        det = 4 * A * C - B * B
        pd = (A > 0) & (det > 0)
        xs = np.where(pd, (B * E - 2 * C * D) / det, p)
        ys = np.where(pd, (B * D - 2 * A * E) / det, s)
        inside = pd & (xs >= p) & (xs <= q) & (ys >= s) & (ys <= t)
        best = np.where(inside, np.minimum(best, val(xs, ys)), best)
    mx = np.maximum(np.maximum(np.abs(p), np.abs(q)), np.maximum(np.abs(s), np.abs(t)))
    scale = (np.abs(A) + np.abs(B) + np.abs(C)) * mx * mx + (np.abs(D) + np.abs(E)) * mx
    return best - FP_REL * (1 + scale + np.abs(best))


def quad_band_min(A, B, C, D, E, p, q, s, t, dlo, dhi):
    """Exact minimum of A x^2 + B x y + C y^2 + D x + E y over the convex polygon
    [p,q] x [s,t] intersected with {dlo <= y - x <= dhi} (vectorized), minus a
    floating-point margin; +inf where the polygon is empty.

    A minimizer exists on a compact polygon. It is either the interior
    stationary point (Hessian PD), or lies on an edge; restricted to an edge the
    function is a univariate quadratic, minimized at an edge endpoint (a vertex)
    or at the clipped vertex of the parabola. Candidates: all vertices (box
    corners, band-line/box-edge intersections), the minimizer along each of the
    6 edge lines clipped to the polygon, and the interior stationary point.
    """
    tol = 1e-12 * (1 + np.abs(p) + np.abs(q) + np.abs(s) + np.abs(t))

    def val(x, y):
        return A * x * x + B * x * y + C * y * y + D * x + E * y

    def feas(x, y):
        return ((x >= p - tol) & (x <= q + tol) & (y >= s - tol) & (y <= t + tol)
                & (y - x >= dlo - tol) & (y - x <= dhi + tol))

    best = np.full(np.shape(p), np.inf)

    def take(x, y, ok=True):
        nonlocal best
        best = np.where(ok & feas(x, y), np.minimum(best, val(x, y)), best)

    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        for x in (p, q):
            for y in (s, t):
                take(x, y)
        for c in (dlo, dhi):
            take(p, p + c); take(q, q + c); take(s - c, s); take(t - c, t)
            # along the band line y = x + c, x in [max(p, s - c), min(q, t - c)]
            a2 = A + B + C
            a1 = B * c + 2 * C * c + D + E
            xl, xh = np.maximum(p, s - c), np.minimum(q, t - c)
            xv = np.clip(np.where(a2 > 0, -a1 / (2 * a2), xl), xl, xh)
            take(xv, xv + c, xl <= xh)
        # box edges x = const (y in [s,t] and in [x+dlo, x+dhi]) and y = const
        for x in (p, q):
            yl, yh = np.maximum(s, x + dlo), np.minimum(t, x + dhi)
            yv = np.clip(np.where(C > 0, -(B * x + E) / (2 * C), yl), yl, yh)
            take(x, yv, yl <= yh)
        for y in (s, t):
            xl, xh = np.maximum(p, y - dhi), np.minimum(q, y - dlo)
            xv = np.clip(np.where(A > 0, -(B * y + D) / (2 * A), xl), xl, xh)
            take(xv, y, xl <= xh)
        det = 4 * A * C - B * B
        pd = (A > 0) & (det > 0)
        xs = np.where(pd, (B * E - 2 * C * D) / det, p)
        ys = np.where(pd, (B * D - 2 * A * E) / det, s)
        take(xs, ys, pd)
    mx = np.maximum(np.maximum(np.abs(p), np.abs(q)), np.maximum(np.abs(s), np.abs(t)))
    scale = (np.abs(A) + np.abs(B) + np.abs(C)) * mx * mx + (np.abs(D) + np.abs(E)) * mx
    return best - 1e-11 * (1 + scale + np.where(np.isfinite(best), np.abs(best), 0))


def taylor2_lb(val, g, Hlo, r):
    """Lower bound of phi(m + d), |d| <= r, given phi(m) = val, phi'(m) = g and
    phi'' >= Hlo on the interval (Taylor with Lagrange remainder), minus margin."""
    with np.errstate(divide="ignore", invalid="ignore"):
        interior = (Hlo > 0) & (np.abs(g) < Hlo * r)
        m = np.where(interior, -g * g / (2 * Hlo), -np.abs(g) * r + 0.5 * Hlo * r * r)
    return val + m - FP_REL * (1 + np.abs(val) + np.abs(g) * r + np.abs(Hlo) * r * r)


def unary_lb_sub(prob, vidx, p, q, Qt, Lt, sub):
    """Unary bound as the minimum of prob.unary_lb over `sub` equal sub-intervals
    of each cell (valid: the sub-intervals cover the cell)."""
    if sub == 1:
        return prob.unary_lb(vidx, p, q, Qt, Lt)
    k = np.arange(sub)
    w = (q - p) / sub
    ps = (p[:, None] + k[None, :] * w[:, None]).ravel()
    qs = np.minimum((p[:, None] + (k[None, :] + 1) * w[:, None]).ravel(), np.repeat(q, sub))
    rep = lambda a: np.repeat(a, sub)
    return prob.unary_lb(rep(vidx), ps, qs, rep(Qt), rep(Lt)).reshape(-1, sub).min(axis=1)


def transfers(prob, xhat, mode):
    n = prob.n
    z = np.zeros(n - 1)
    if mode == "plain" or xhat is None:
        return z, z.copy(), z.copy(), z.copy()
    gx, gy = prob.pair_grad(xhat)
    if hasattr(prob, "pair_multipliers"):
        # KKT multipliers of pairwise constraints active at xhat: shifting them
        # into the pair pieces makes every unary piece stationary at xhat.
        mu = prob.pair_multipliers(xhat)
        gx, gy = gx + mu, gy - mu
    if mode == "affine":
        return z, gx, z.copy(), gy
    if mode == "quad":
        rho = 0.5 * prob.pair_cross()
        return rho, gx + 2 * rho * xhat[:-1], rho.copy(), gy + 2 * rho * xhat[1:]
    if mode == "split":
        rhoL, rhoR = hessian_split(prob, xhat)
        return rhoL, gx + 2 * rhoL * xhat[:-1], rhoR, gy + 2 * rhoR * xhat[1:]
    raise ValueError(mode)


def hessian_split(prob, xhat, theta=0.3):
    """Quadratic transfers from a chordal (edge-wise) PSD splitting of the
    tridiagonal Hessian H of F at xhat. Pair block e gets [[u_e, b_e], [b_e, v_e]]
    with u_e = (1 - theta) rem_e and v_e = b_e^2 / u_e (PSD, singular), the unary
    of variable e keeps theta rem_e, and rem_{e+1} = H_{e+1,e+1} - v_e (the LDL^T
    pivots when theta = 0). If H is positive definite and theta is small enough,
    every piece is convex at xhat. rho may be negative; validity never depends
    on the choice of rho (the pieces always sum to F)."""
    hxx, hxy, hyy = prob.pair_hess(xhat)
    a = prob.unary_hess(xhat).astype(float).copy()
    a[:-1] += hxx
    a[1:] += hyy
    # a fixed variable (zero-width domain) can absorb any curvature exactly
    a = np.where(prob.hi <= prob.lo, 1e3, a)
    n = prob.n
    u = np.empty(n - 1); v = np.empty(n - 1)
    rem = a[0]
    for e in range(n - 1):
        ok = rem > 1e-3 * max(1.0, abs(a[e]))
        if ok:
            u[e] = (1 - theta) * rem
            v[e] = hxy[e] ** 2 / u[e]
            ok = a[e + 1] - v[e] > 1e-3 * max(1.0, abs(a[e + 1]))
        if not ok:
            # H is not positive definite along the recursion: no quadratic
            # transfer on this edge (the pair keeps its own Hessian)
            u[e], v[e] = hxx[e], hyy[e]
        rem = a[e + 1] - v[e]
    return 0.5 * (u - hxx), 0.5 * (v - hyy)


def chain_bb(prob, eps, mode="quad", max_iter=80, time_limit=600.0, localize_delta=None,
             max_cells=2_000_000, max_pairs_iter=20_000_000, unary_sub=1, theta=1.0, verbose=False):
    """Returns a dict with LB, UB, incumbent and work statistics.

    theta: refinement rule. A surviving cell is bisected if its marginal is below
    LBdp + theta * (prune threshold - LBdp). theta = 1 bisects every surviving
    cell; theta = 0 bisects only cells whose marginal equals the DP bound (the
    cells on the lowest-bound paths). Unsplit cells stay in the partition.

    localize_delta: if given, cells are pruned only when their marginal exceeds
    UB + localize_delta, and the run also stops only once the hull of the
    surviving cells passes prob.hessian_is_pd_on_box (uniqueness certificate).
    """
    t0 = time.time()
    n = prob.n
    cells = [np.array([[prob.lo[i], prob.hi[i]]]) for i in range(n)]
    xhat, UB = prob.local_opt(0.5 * (prob.lo + prob.hi))
    nlocal = 1
    pruned_min = np.inf
    pairs = unary = 0
    hist = []
    status = "iter_limit"
    certified = None
    LB = -np.inf
    for it in range(max_iter):
        rhoL, alpha, rhoR, beta = transfers(prob, xhat, mode)
        Q = np.zeros(n); L = np.zeros(n)
        Q[:-1] += rhoL; Q[1:] += rhoR; L[:-1] += alpha; L[1:] += beta
        K = np.array([len(c) for c in cells])
        if int((K[:-1] * K[1:]).sum()) > max_pairs_iter:
            status = "pair_limit"
            break
        if K.min() == 0:
            LBdp = np.inf
        else:
            allc = np.concatenate(cells)
            vidx = np.repeat(np.arange(n), K)
            uflat = unary_lb_sub(prob, vidx, allc[:, 0], allc[:, 1], Q[vidx], L[vidx], unary_sub)
            unary += len(uflat)
            uoff = np.concatenate([[0], np.cumsum(K)])
            u = [uflat[uoff[i]:uoff[i + 1]] for i in range(n)]
            # pair bounds, computed in chunks of edges to bound memory use
            P = []
            e0 = 0
            while e0 < n - 1:
                eidx, P0, P1, S0, S1 = [], [], [], [], []
                tot, e = 0, e0
                while e < n - 1 and (tot == 0 or tot + K[e] * K[e + 1] <= 2_000_000):
                    ka, kb = K[e], K[e + 1]
                    ia = np.repeat(np.arange(ka), kb); ib = np.tile(np.arange(kb), ka)
                    P0.append(cells[e][ia, 0]); P1.append(cells[e][ia, 1])
                    S0.append(cells[e + 1][ib, 0]); S1.append(cells[e + 1][ib, 1])
                    eidx.append(np.full(ka * kb, e))
                    tot += ka * kb; e += 1
                eidx = np.concatenate(eidx)
                pflat = prob.pair_lb(eidx, np.concatenate(P0), np.concatenate(P1),
                                     np.concatenate(S0), np.concatenate(S1),
                                     rhoL[eidx], alpha[eidx], rhoR[eidx], beta[eidx])
                off = 0
                for ee in range(e0, e):
                    sz = K[ee] * K[ee + 1]
                    P.append(pflat[off:off + sz].reshape(K[ee], K[ee + 1])); off += sz
                e0 = e
            pairs += int((K[:-1] * K[1:]).sum())
            # forward / backward min-sum DP
            f = [u[0]]
            for e in range(n - 1):
                f.append((f[e][:, None] + P[e]).min(axis=0) + u[e + 1])
            g = [None] * n
            g[n - 1] = np.zeros(K[n - 1])
            for e in range(n - 2, -1, -1):
                g[e] = (P[e] + (u[e + 1] + g[e + 1])[None, :]).min(axis=1)
            marg = [f[i] + g[i] for i in range(n)]
            LBdp = float(f[n - 1].min())
            # upper bound from the DP argmin path
            path = np.empty(n, int)
            path[n - 1] = int(np.argmin(f[n - 1]))
            for e in range(n - 2, -1, -1):
                path[e] = int(np.argmin(f[e] + P[e][:, path[e + 1]]))
            x0 = np.array([cells[i][path[i]].mean() for i in range(n)])
            xl, fl = prob.local_opt(x0)
            nlocal += 1
            if fl < UB:
                UB, xhat = fl, xl
        LB = min(LBdp, pruned_min)
        wmax = max((float((c[:, 1] - c[:, 0]).max()) for c in cells if len(c)), default=0.0)
        hist.append(dict(it=it, LB=LB, UB=UB, cells=int(K.sum()), maxK=int(K.max()),
                         pairs=pairs, wmax=wmax, t=time.time() - t0))
        if verbose:
            print(hist[-1], flush=True)
        if K.min() == 0:
            status = "optimal"
            break
        thr = UB - eps if localize_delta is None else UB + localize_delta
        newcells, splitmask = [], []
        split_thr = LBdp + theta * (thr - LBdp) if theta < 1 else np.inf
        for i in range(n):
            keep = marg[i] < thr if localize_delta is None else marg[i] <= thr
            if (~keep).any():
                pruned_min = min(pruned_min, float(marg[i][~keep].min()))
            newcells.append(cells[i][keep])
            splitmask.append(marg[i][keep] <= max(split_thr, LBdp * (1 + 1e-15) + 1e-15))
        if LB >= UB - eps:
            if localize_delta is None:
                status = "optimal"
                break
            hlo = np.array([c[:, 0].min() if len(c) else np.nan for c in newcells])
            hhi = np.array([c[:, 1].max() if len(c) else np.nan for c in newcells])
            if not np.isnan(hlo).any() and prob.hessian_is_pd_on_box(hlo, hhi):
                certified = dict(hull_lo=hlo, hull_hi=hhi)
                status = "optimal"
                break
        if time.time() - t0 > time_limit:
            status = "time_limit"
            break
        cells = []
        for c, sm in zip(newcells, splitmask):
            flat = (c[:, 1] <= c[:, 0]) | ~sm  # zero-width cells (fixed variables) are not split
            c2 = c[~flat]
            m = 0.5 * (c2[:, 0] + c2[:, 1])
            cells.append(np.concatenate([c[flat], np.stack([np.concatenate([c2[:, 0], m]),
                                                            np.concatenate([m, c2[:, 1]])], 1)]))
        if sum(len(c) for c in cells) > max_cells:
            status = "cell_limit"
            break
    if not hist:
        LB = -np.inf
    return dict(status=status, LB=LB, UB=UB, x=xhat, iters=len(hist), pairs=int(pairs),
                unary=int(unary), nlocal=nlocal, time=time.time() - t0, hist=hist,
                final_cells=int(sum(len(c) for c in cells)), certified=certified, cell_list=cells)
