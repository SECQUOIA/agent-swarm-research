"""Algorithm LS of extension-adaptive.md on the path family

    F(x) = sum_i phi(x_i) + b sum_i x_i x_{i+1} + sum_i c_i x_i,   phi(t) = t^2 - kappa t^4,   x in [-1,1]^n.

Path decomposition as in ../dp_certificate.py: bags t = 0..n-2 with V_t = {t, t+1}, root bag 0,
separator S_t = {t} for t >= 1. Unary factors exact (convex for kappa <= 1/6), bilinear factor
relaxed by alphaBB with alpha = |b|/2 on every box (monotone under refinement).

LS = level-synchronous separator branching:
  * leaves and cells are dyadic boxes of [-1,1]^2 and [-1,1];
  * a pass p uses fixed slopes lam (gradients of the subtree factors at the previous
    pass's consistent point) and runs sublevels i = 0..p from the root partition;
  * at each sublevel: bottom-up DP (Lemma 1.5 of the decomposition note), top-down pass
    for min-marginals, incumbent update at the consistent point of the minimizing
    configuration, stop test l_r >= UBD - eps, then split every level-i leaf and cell
    whose min-marginal is < UBD - eps.
Floating point throughout (nested bisection, 60 steps): illustrations, not certified values.
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dp_certificate import phi, dphi, F, global_min  # noqa: E402

NB = 60


def solve(l1, u1, l2, u2, L1, U1, lin1, lin2, b, kappa, last, cz2):
    """min over z1 in [L1,U1], z2 in [l2,u2] of
    phi(z1) + lin1 z1 + b z1 z2 - (|b|/2)[(z1-l1)(u1-z1) + (z2-l2)(u2-z2)] + lin2 z2
    (+ phi(z2) + cz2 z2 if last). Convex; nested bisection. Returns (value, z1, z2)."""
    ab = abs(b)

    def z2star(z1):
        if not last:
            return np.clip(((ab / 2) * (l2 + u2) - b * z1 - lin2) / ab, l2, u2)
        a, c_ = l2.copy(), u2.copy()

        def d(z2):
            return dphi(z2, kappa) + cz2 + b * z1 + (ab / 2) * (2 * z2 - l2 - u2) + lin2
        da, dc = d(a), d(c_)
        for _ in range(NB):
            m = 0.5 * (a + c_)
            pos = d(m) > 0
            c_ = np.where(pos, m, c_)
            a = np.where(pos, a, m)
        z = 0.5 * (a + c_)
        z = np.where(da >= 0, l2, z)
        z = np.where(dc <= 0, u2, z)
        return z

    def g(z1, z2):
        v = (phi(z1, kappa) + lin1 * z1 + b * z1 * z2
             - (ab / 2) * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2)) + lin2 * z2)
        if last:
            v = v + phi(z2, kappa) + cz2 * z2
        return v

    def hprime(z1):
        z2 = z2star(z1)
        return dphi(z1, kappa) + lin1 + b * z2 + (ab / 2) * (2 * z1 - l1 - u1)

    a, c_ = L1.copy(), U1.copy()
    ha, hc = hprime(a), hprime(c_)
    for _ in range(NB):
        m = 0.5 * (a + c_)
        pos = hprime(m) > 0
        c_ = np.where(pos, m, c_)
        a = np.where(pos, a, m)
    z1 = 0.5 * (a + c_)
    z1 = np.where(ha >= 0, L1, z1)
    z1 = np.where(hc <= 0, U1, z1)
    z1 = np.where(U1 - L1 <= 0, L1, z1)
    z2 = z2star(z1)
    return g(z1, z2), z1, z2


def slopes(x, b, kappa, c):
    """lam_t(x) = d/dx_t of the factors of bag t (Lemma 3.2 of the note), t = 1..n-2."""
    n = len(x)
    lam = np.zeros(n)
    for t in range(1, n - 1):
        lam[t] = dphi(x[t], kappa) + c[t] + b * x[t + 1]
    return lam


class Partition:
    """Leaves of each bag (arrays l1,u1,l2,u2,lev) and cells of each separator (lo,hi,lev)."""

    def __init__(self, n):
        self.n = n
        self.leaves = [dict(l1=np.array([-1.0]), u1=np.array([1.0]), l2=np.array([-1.0]),
                            u2=np.array([1.0]), lev=np.array([0])) for _ in range(n - 1)]
        self.cells = [None] + [dict(lo=np.array([-1.0]), hi=np.array([1.0]), lev=np.array([0]))
                               for _ in range(1, n - 1)]

    def size(self):
        nl = sum(len(L["l1"]) for L in self.leaves)
        nc = sum(len(C["lo"]) for C in self.cells[1:])
        return nl, nc

    def split(self, t, leaf_mask, cell_mask):
        L = self.leaves[t]
        keep = ~leaf_mask
        new = {k: [L[k][keep]] for k in L}
        if leaf_mask.any():
            l1, u1, l2, u2 = (L[k][leaf_mask] for k in ("l1", "u1", "l2", "u2"))
            m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
            lev = L["lev"][leaf_mask] + 1
            for (a1, b1) in ((l1, m1), (m1, u1)):
                for (a2, b2) in ((l2, m2), (m2, u2)):
                    new["l1"].append(a1); new["u1"].append(b1)
                    new["l2"].append(a2); new["u2"].append(b2)
                    new["lev"].append(lev)
        self.leaves[t] = {k: np.concatenate(v) for k, v in new.items()}
        if t >= 1 and cell_mask is not None:
            C = self.cells[t]
            keep = ~cell_mask
            lo, hi, lev = C["lo"][cell_mask], C["hi"][cell_mask], C["lev"][cell_mask] + 1
            mid = 0.5 * (lo + hi)
            self.cells[t] = dict(lo=np.concatenate([C["lo"][keep], lo, mid]),
                                 hi=np.concatenate([C["hi"][keep], mid, hi]),
                                 lev=np.concatenate([C["lev"][keep], lev, lev]))


def interval_pairs(lo, hi, l, u, tol=0.0):
    """All (k, D) with [l_k,u_k] and cell [lo_D,hi_D] intersecting (closed), after widening
    [l_k,u_k] by tol. Cells are intervals with disjoint interiors covering the axis. Returns (k, D)
    index arrays (D in original order). tol > 0 keeps pairs that touch in exact arithmetic but are
    1 ulp apart after rounding (non-dyadic box edges, as in rc_lib); dyadic LS boxes are exact."""
    l, u = l - tol, u + tol
    order = np.argsort(lo)
    los, his = lo[order], hi[order]
    a = np.searchsorted(his, l, side="left")          # first cell with hi >= l
    bnd = np.searchsorted(los, u, side="right") - 1   # last cell with lo <= u
    cnt = np.maximum(bnd - a + 1, 0)
    k = np.repeat(np.arange(len(l)), cnt)
    offs = np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    D = order[np.repeat(a, cnt) + offs]
    return k, D


def group_min(vals, groups, ngroups):
    """min and argmin (index into vals) of vals per group."""
    m = np.full(ngroups, np.inf)
    np.minimum.at(m, groups, vals)
    order = np.lexsort((vals, groups))
    first = np.ones(len(order), bool)
    first[1:] = groups[order][1:] != groups[order][:-1]
    arg = np.full(ngroups, -1)
    arg[groups[order][first]] = order[first]
    return m, arg


def dp(P, lam, b, kappa, c, tol=0.0):
    """Bottom-up DP (beta), top-down min-marginals, minimizing configuration.
    Returns dict with root bound, MM of leaves and cells, consistent point, config value, pairs.
    tol: widening of the leaf-cell intersection test (see interval_pairs)."""
    n = P.n
    cz2 = c[n - 1]
    info = [None] * (n - 1)
    npairs = 0
    for t in range(n - 2, -1, -1):
        L = P.leaves[t]
        last = (t == n - 2)
        l1, u1, l2, u2 = L["l1"], L["u1"], L["l2"], L["u2"]
        nl = len(l1)
        lin2 = lam[t + 1] if not last else 0.0
        if not last:
            C = P.cells[t + 1]
            ck, cD = interval_pairs(C["lo"], C["hi"], l2, u2, tol)
            mc, a = group_min(info[t + 1]["beta"][cD], ck, nl)
            mcarg = cD[a]
        else:
            ck = cD = None
            mc = np.zeros(nl)
            mcarg = np.full(nl, -1)
        if t == 0:
            val, z1, z2 = solve(l1, u1, l2, u2, l1.copy(), u1.copy(), np.full(nl, c[0]),
                                np.full(nl, lin2), b, kappa, last, cz2)
            info[0] = dict(g=val, z1=z1, z2=z2, mc=mc, mcarg=mcarg, ck=ck, cD=cD)
            npairs += nl
            continue
        S = P.cells[t]
        bi, di = interval_pairs(S["lo"], S["hi"], l1, u1, tol)
        npairs += len(bi)
        L1 = np.maximum(l1[bi], S["lo"][di])
        U1 = np.minimum(u1[bi], S["hi"][di])
        val, z1, z2 = solve(l1[bi], u1[bi], l2[bi], u2[bi], L1, U1,
                            np.full(len(bi), c[t] - lam[t]), np.full(len(bi), lin2),
                            b, kappa, last, cz2)
        tot = val + mc[bi]
        beta, argpair = group_min(tot, di, len(S["lo"]))
        info[t] = dict(g=val, z1=z1, z2=z2, bi=bi, di=di, mc=mc, mcarg=mcarg, ck=ck, cD=cD,
                       beta=beta, argpair=argpair)
    root_tot = info[0]["g"] + info[0]["mc"]
    lr = float(root_tot.min())
    # top-down: o(B) and min-marginals
    MMleaf = [None] * (n - 1)
    MMcell = [None] * (n - 1)
    o = info[0]["g"]
    MMleaf[0] = o + info[0]["mc"]
    for t in range(1, n - 1):
        ck, cD = info[t - 1]["ck"], info[t - 1]["cD"]  # (leaf of bag t-1, cell of S_t) pairs
        out, _ = group_min(o[ck], cD, len(P.cells[t]["lo"]))
        MMcell[t] = out + info[t]["beta"]
        bi, di = info[t]["bi"], info[t]["di"]
        ot = np.full(len(P.leaves[t]["l1"]), np.inf)
        np.minimum.at(ot, bi, out[di] + info[t]["g"])
        o = ot
        MMleaf[t] = o + info[t]["mc"]
    # minimizing configuration and its consistent point
    k = int(root_tot.argmin())
    conf_leaves = [k]          # leaf index of the minimizing configuration in each bag
    x = np.zeros(n)
    x[0], x[1] = info[0]["z1"][k], info[0]["z2"][k]
    d = info[0]["mcarg"][k]
    conf_val = info[0]["g"][k]
    maxdrift = 0.0
    prev_copy = x[1]
    for t in range(1, n - 1):
        q = info[t]["argpair"][d]
        leaf = info[t]["bi"][q]
        conf_leaves.append(int(leaf))
        conf_val += info[t]["g"][q]
        maxdrift = max(maxdrift, abs(info[t]["z1"][q] - prev_copy))
        x[t + 1] = info[t]["z2"][q]
        prev_copy = x[t + 1]
        d = info[t]["mcarg"][leaf]
    return dict(lr=lr, MMleaf=MMleaf, MMcell=MMcell, x=x, conf_val=float(conf_val),
                maxdrift=maxdrift, npairs=npairs, conf_leaves=conf_leaves)


def run_ls(n, b, kappa, c, eps, x0, pmax=40, xstar=None, fstar=None, fixed_lam=None, log=None):
    """Algorithm LS with restarts. If fixed_lam is given, a single pass with these slopes and
    no restarts (comparison run). Returns summary dict and per-sublevel records."""
    UBD = F(x0, b, kappa, c)
    xbest = x0.copy()          # point attaining the incumbent UBD
    xprev = x0.copy()
    recs = []
    total_boxes = 0
    passes = [None] if fixed_lam is not None else range(pmax + 1)
    for p in passes:
        lam = fixed_lam if fixed_lam is not None else slopes(xprev, b, kappa, c)
        nu = None
        if xstar is not None:
            nu = float(np.linalg.norm(lam - slopes(xstar, b, kappa, c)))
        start = dict(lam=np.array(lam, float), UBD=UBD, xbest=xbest.copy())  # state at pass start
        P = Partition(n)
        imax = pmax if fixed_lam is not None else p
        for i in range(imax + 1):
            nl, nc = P.size()
            total_boxes += nl + nc
            R = dp(P, lam, b, kappa, c)
            fx = F(R["x"], b, kappa, c)
            if fx < UBD:
                UBD, xbest = fx, R["x"].copy()
            thr = UBD - eps
            # permanence check (Lemma A.2): frozen boxes (level < i) must have MM >= thr
            viol = 0
            nnew_leaf = []
            for t in range(n - 1):
                lev = P.leaves[t]["lev"]
                viol += int(np.sum((lev < i) & (R["MMleaf"][t] < thr - 1e-12)))
                nnew_leaf.append(int(np.sum(lev == i)))
                if t >= 1:
                    viol += int(np.sum((P.cells[t]["lev"] < i) & (R["MMcell"][t] < thr - 1e-12)))
            live = [int(np.sum((P.leaves[t]["lev"] == i) & (R["MMleaf"][t] < thr))) for t in range(n - 1)]
            rec = dict(p=p, i=i, leaves=nl, cells=nc, lr=R["lr"], UBD=UBD, viol=viol,
                       new_max=max(nnew_leaf), new_mean=float(np.mean(nnew_leaf)),
                       live_max=max(live), live_mean=float(np.mean(live)),
                       conf_err=abs(R["conf_val"] - R["lr"]), nu=nu,
                       conf_lev=[int(P.leaves[t]["lev"][R["conf_leaves"][t]]) for t in range(n - 1)])
            if xstar is not None:
                rec["dx2"] = float(np.linalg.norm(R["x"] - xstar))
                rec["dxinf"] = float(np.abs(R["x"] - xstar).max())
            if fstar is not None:
                rec["gap"] = fstar - R["lr"]
            recs.append(rec)
            if log:
                log(rec)
            if R["lr"] >= thr:
                return dict(done=True, p=p, i=i, size=nl + nc, leaves=nl, cells=nc,
                            lr=R["lr"], UBD=UBD, total_boxes=total_boxes, start=start), recs
            if i < imax:
                for t in range(n - 1):
                    lm = (P.leaves[t]["lev"] == i) & (R["MMleaf"][t] < thr)
                    cm = None
                    if t >= 1:
                        cm = (P.cells[t]["lev"] == i) & (R["MMcell"][t] < thr)
                    P.split(t, lm, cm)
        xprev = R["x"]
    return dict(done=False, total_boxes=total_boxes), recs
