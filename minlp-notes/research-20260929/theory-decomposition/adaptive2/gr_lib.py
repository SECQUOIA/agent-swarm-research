"""Algorithm GR (graded refinement around the minimizing configuration) on the path family

    F(x) = sum_i phi(x_i) + b sum_i x_i x_{i+1} + sum_i c_i x_i,   phi(t) = t^2 - kappa t^4,   x in [-1,1]^n.

Path decomposition, relaxation, dyadic leaves and cells as in ../adaptive/ls_lib.py: bags
t = 0..n-2 with V_t = {t, t+1}, root bag 0, separator S_t = {t} (t >= 1); unary factors exact,
bilinear factor relaxed by alphaBB with alpha = |b|/2.

GR (adaptive-matching.md, Section 2):
  stage j = 0, 1, 2, ...  (core width W_j = 2 * 2^-j):
    1. slopes lam = lam(x_{j-1}) at the consistent point of the previous stage (x_{-1} = x0);
    2. one bottom-up DP (Lemma 1.5 of the decomposition note) on the current partition:
       root bound l_r and a minimizing configuration with copies z^t in every bag;
    3. incumbent UBD := min(UBD, F(x_j)) at its consistent point x_j; stop if l_r >= UBD - eps;
    4. refine, in every bag t, every leaf B with  w(B) > max(W_{j+1}, theta (dist_inf(B, z^t) - R W_j)_+),
       and every cell D of S_t with  w(D) > max(W_{j+1}, theta (dist_inf(D, z^t_{S_t}) - R W_j)_+),
       until no box qualifies.
No pruning, no min-marginals, no knowledge of x*, no local solver; one DP per stage.
Floating point throughout (nested bisection, 60 steps): illustrations, not certified values.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "adaptive"))
sys.path.insert(0, os.path.join(HERE, ".."))
from ls_lib import solve, slopes, Partition, interval_pairs, group_min  # noqa: E402
from dp_certificate import F, global_min  # noqa: E402


def dp_min(P, lam, b, kappa, c, tol=0.0):
    """Bottom-up DP of Lemma 1.5 and one minimizing configuration.
    Returns lr, the copies z (n-1, 2) of the minimizing configuration (z[t] = copy of
    (x_t, x_{t+1}) in bag t), its leaf index per bag, its cell index per separator,
    the consistent point x (x_0 from bag 0, x_{t+1} from bag t), and the number of pairs."""
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
            mc = np.zeros(nl)
            mcarg = np.full(nl, -1)
        if t == 0:
            val, z1, z2 = solve(l1, u1, l2, u2, l1.copy(), u1.copy(), np.full(nl, c[0]),
                                np.full(nl, lin2), b, kappa, last, cz2)
            info[0] = dict(g=val, z1=z1, z2=z2, mc=mc, mcarg=mcarg)
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
        info[t] = dict(g=val, z1=z1, z2=z2, bi=bi, di=di, mc=mc, mcarg=mcarg,
                       beta=beta, argpair=argpair)
        del tot
    root_tot = info[0]["g"] + info[0]["mc"]
    lr = float(root_tot.min())
    k = int(root_tot.argmin())
    z = np.zeros((n - 1, 2))
    leaf = np.zeros(n - 1, int)
    cell = np.full(n - 1, -1)
    z[0] = info[0]["z1"][k], info[0]["z2"][k]
    leaf[0] = k
    d = info[0]["mcarg"][k]
    for t in range(1, n - 1):
        q = info[t]["argpair"][d]
        cell[t] = d
        leaf[t] = int(info[t]["bi"][q])
        z[t] = info[t]["z1"][q], info[t]["z2"][q]
        d = info[t]["mcarg"][leaf[t]]
    x = np.concatenate([[z[0, 0]], z[:, 1]])
    return dict(lr=lr, z=z, leaf=leaf, cell=cell, x=x, npairs=npairs)


def dist_inf_box(lo, hi, p):
    """sup-norm distance of the boxes [lo, hi] (arrays (N, d)) to the point p (d,)."""
    return np.max(np.maximum(np.maximum(lo - p[None, :], p[None, :] - hi), 0.0), axis=1)


def refine(P, z, W_next, W_cur, theta, R):
    """Step 4 of GR. Returns (leaves split, cells split) per bag (arrays) and the number of
    splits of boxes wider than W_cur."""
    n = P.n
    nsl = np.zeros(n - 1, int)
    nsc = np.zeros(n - 1, int)
    nwide = 0            # splits of boxes wider than W_cur (the proof of Theorem 2 predicts none)
    for t in range(n - 1):
        while True:
            L = P.leaves[t]
            lo = np.stack([L["l1"], L["l2"]], 1)
            hi = np.stack([L["u1"], L["u2"]], 1)
            w = L["u1"] - L["l1"]
            target = np.maximum(W_next, theta * np.maximum(dist_inf_box(lo, hi, z[t]) - R * W_cur, 0.0))
            lm = w > target * (1 + 1e-12)
            cm = None
            if t >= 1:
                C = P.cells[t]
                wc = C["hi"] - C["lo"]
                dc = np.maximum(np.maximum(C["lo"] - z[t, 0], z[t, 0] - C["hi"]), 0.0)
                tc = np.maximum(W_next, theta * np.maximum(dc - R * W_cur, 0.0))
                cm = wc > tc * (1 + 1e-12)
            if not lm.any() and (cm is None or not cm.any()):
                break
            nsl[t] += int(lm.sum())
            nwide += int(np.sum(w[lm] > W_cur * (1 + 1e-12)))
            if cm is not None:
                nsc[t] += int(cm.sum())
                nwide += int(np.sum(wc[cm] > W_cur * (1 + 1e-12)))
            P.split(t, lm, cm)
    return nsl, nsc, nwide


def graded_violations(P, xstar, W, theta):
    """Number of leaves and cells violating w <= max(W, theta * dist_inf(box, x*)) (invariant G)."""
    n = P.n
    v = 0
    for t in range(n - 1):
        L = P.leaves[t]
        lo = np.stack([L["l1"], L["l2"]], 1)
        hi = np.stack([L["u1"], L["u2"]], 1)
        w = L["u1"] - L["l1"]
        v += int(np.sum(w > np.maximum(W, theta * dist_inf_box(lo, hi, xstar[t:t + 2])) * (1 + 1e-12)))
        if t >= 1:
            C = P.cells[t]
            wc = C["hi"] - C["lo"]
            dc = np.maximum(np.maximum(C["lo"] - xstar[t], xstar[t] - C["hi"]), 0.0)
            v += int(np.sum(wc > np.maximum(W, theta * dc) * (1 + 1e-12)))
    return v


def run_gr(n, b, kappa, c, eps, x0, theta, R, jmax=40, xstar=None, fstar=None, log=None,
           s0=2.0):
    UBD = F(x0, b, kappa, c)
    xprev = x0.copy()
    P = Partition(n)
    recs = []
    created = 0          # boxes created by splits (the initial 2n-3 boxes not included)
    processed = 0        # sum of partition sizes over all DP runs
    for j in range(jmax + 1):
        W = s0 * 2.0 ** (-j)
        lam = slopes(xprev, b, kappa, c)
        nl, nc = P.size()
        processed += nl + nc
        D = dp_min(P, lam, b, kappa, c)
        fx = F(D["x"], b, kappa, c)
        UBD = min(UBD, fx)
        rec = dict(j=j, W=W, leaves=nl, cells=nc, lr=D["lr"], UBD=UBD, npairs=D["npairs"],
                   created=created)
        if xstar is not None:
            zs = np.stack([xstar[:-1], xstar[1:]], 1)
            rec["zloc"] = float(np.abs(D["z"] - zs).max()) / W          # max_t |z^t - x*_{V_t}|_inf / W_j
            rec["xloc"] = float(np.abs(D["x"] - xstar).max()) / W
            rec["x2"] = float(np.linalg.norm(D["x"] - xstar)) / W
            lam_star = slopes(xstar, b, kappa, c)
            rec["nu_inf"] = float(np.abs(lam - lam_star).max())
            rec["graded_viol"] = graded_violations(P, xstar, W, theta)
        if fstar is not None:
            rec["gap"] = fstar - D["lr"]
            rec["inc"] = UBD - fstar
        done = D["lr"] >= UBD - eps
        if not done and j < jmax:
            nsl, nsc, nwide = refine(P, D["z"], W / 2, W, theta, R)
            rec["wide_splits"] = nwide
            created += 4 * int(nsl.sum()) + 2 * int(nsc.sum())
            rec["split_leaf_max"] = int(nsl.max())
            rec["split_leaf_mean"] = float(nsl.mean())
            rec["split_cell_max"] = int(nsc.max())
        recs.append(rec)
        if log:
            log(rec)
        if done:
            return dict(done=True, j=j, size=nl + nc, leaves=nl, cells=nc, lr=D["lr"], UBD=UBD,
                        created=created, processed=processed), recs
        xprev = D["x"]
    return dict(done=False, created=created, processed=processed), recs
