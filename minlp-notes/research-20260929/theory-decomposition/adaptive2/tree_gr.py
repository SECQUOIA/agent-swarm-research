"""Algorithm GR on a branching tree decomposition (adaptive-matching.md, Section 5.4).

Instance: complete binary tree graph on vertices 0..m-1 (children of v are 2v+1, 2v+2),

    F(x) = sum_v [phi(x_v) + c_v x_v] + b sum_{v >= 1} x_{p(v)} x_v,   phi(t) = t^2 - kappa t^4,   x in [-1,1]^m.

Tree decomposition: one bag per non-root vertex v (v = 1..m-1) with coordinates (z1, z2) = (x_{p(v)}, x_v).
Bag 1 is the root of the decomposition; bag 2 is a child of bag 1 (separator {x_0}); for v >= 3 the
parent of bag v is bag p(v) (separator {x_{p(v)}}). Width 1, one-dimensional separators; x_v lies in
bag v and the bags of the children of v, so k = 3, and bags have up to 2 children (bag 1 has 3).
Factors: bag v holds b z1 z2 + phi(z2) + c_v z2; bag 1 also phi(z1) + c_0 z1. Unary factors exact
(convex for kappa <= 1/6), bilinear factor relaxed by alphaBB with alpha = |b|/2.
Slopes (Lemma 3.2 of the decomposition note): lam_v(x) = b x_v for bags v >= 2.
For c = 0, x* = 0 and (QG) holds with c_g >= 1 - kappa - |b| rho(A)/2 > 1 - kappa - sqrt(2)|b|.
Floating point (nested bisection): illustrations, not certified values.
"""
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "adaptive"))
from ls_lib import interval_pairs, group_min  # noqa: E402

NB = 50


def phi(t, kappa):
    t2 = t * t
    return t2 - kappa * t2 * t2


def dphi(t, kappa):
    return t * (2 - 4 * kappa * t * t)


def F(x, b, kappa, c):
    m = len(x)
    p = (np.arange(1, m) - 1) // 2
    return float(np.sum(phi(x, kappa)) + np.dot(c, x) + b * np.sum(x[p] * x[1:]))


def grad(x, b, kappa, c):
    m = len(x)
    p = (np.arange(1, m) - 1) // 2
    g = dphi(x, kappa) + c
    np.add.at(g, p, b * x[1:])
    g[1:] += b * x[p]
    return g


def solve(l1, u1, l2, u2, L1, U1, lin1, lin2, b, kappa, root):
    """min over z1 in [L1,U1], z2 in [l2,u2] of
    [phi(z1) if root] + lin1 z1 + b z1 z2 - (|b|/2)[(z1-l1)(u1-z1) + (z2-l2)(u2-z2)] + phi(z2) + lin2 z2.
    Jointly convex; nested bisection on monotone derivatives. Returns (value, z1, z2)."""
    ab = abs(b)
    p1 = 1.0 if root else 0.0

    def z2star(z1):
        a, c_ = l2.copy(), u2.copy()

        def d(z2):
            return dphi(z2, kappa) + lin2 + b * z1 + (ab / 2) * (2 * z2 - l2 - u2)
        da, dc = d(a), d(c_)
        for _ in range(NB):
            mid = 0.5 * (a + c_)
            pos = d(mid) > 0
            c_ = np.where(pos, mid, c_)
            a = np.where(pos, a, mid)
        z = 0.5 * (a + c_)
        z = np.where(da >= 0, l2, z)
        z = np.where(dc <= 0, u2, z)
        return z

    def hprime(z1):
        z2 = z2star(z1)
        return p1 * dphi(z1, kappa) + lin1 + b * z2 + (ab / 2) * (2 * z1 - l1 - u1)

    a, c_ = L1.copy(), U1.copy()
    ha, hc = hprime(a), hprime(c_)
    for _ in range(NB):
        mid = 0.5 * (a + c_)
        pos = hprime(mid) > 0
        c_ = np.where(pos, mid, c_)
        a = np.where(pos, a, mid)
    z1 = 0.5 * (a + c_)
    z1 = np.where(ha >= 0, L1, z1)
    z1 = np.where(hc <= 0, U1, z1)
    z1 = np.where(U1 - L1 <= 0, L1, z1)
    z2 = z2star(z1)
    v = (p1 * phi(z1, kappa) + lin1 * z1 + b * z1 * z2
         - (ab / 2) * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2)) + phi(z2, kappa) + lin2 * z2)
    return v, z1, z2


class TreeDecomp:
    def __init__(self, m):
        self.m = m
        self.bags = list(range(1, m))
        self.parent = {v: (1 if v == 2 else (v - 1) // 2) for v in range(2, m)}
        # children bags of bag v, with the coordinate (0 = z1, 1 = z2) of bag v carrying the separator
        self.children = {v: [] for v in self.bags}
        for u in range(2, m):
            pv = self.parent[u]
            self.children[pv].append((u, 0 if u == 2 else 1))
        order = [1]
        k = 0
        while k < len(order):
            order += [u for (u, _) in self.children[order[k]]]
            k += 1
        self.topdown = order


class TreePartition:
    def __init__(self, m):
        self.m = m
        self.leaves = {v: dict(l1=np.array([-1.0]), u1=np.array([1.0]), l2=np.array([-1.0]),
                               u2=np.array([1.0])) for v in range(1, m)}
        self.cells = {v: dict(lo=np.array([-1.0]), hi=np.array([1.0])) for v in range(2, m)}

    def size(self):
        return (sum(len(L["l1"]) for L in self.leaves.values()),
                sum(len(C["lo"]) for C in self.cells.values()))

    def split(self, v, lm, cm):
        L = self.leaves[v]
        if lm.any():
            keep = ~lm
            l1, u1, l2, u2 = (L[k][lm] for k in ("l1", "u1", "l2", "u2"))
            m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
            new = {k: [L[k][keep]] for k in L}
            for (a1, b1) in ((l1, m1), (m1, u1)):
                for (a2, b2) in ((l2, m2), (m2, u2)):
                    new["l1"].append(a1); new["u1"].append(b1)
                    new["l2"].append(a2); new["u2"].append(b2)
            self.leaves[v] = {k: np.concatenate(w) for k, w in new.items()}
        if cm is not None and cm.any():
            C = self.cells[v]
            keep = ~cm
            lo, hi = C["lo"][cm], C["hi"][cm]
            mid = 0.5 * (lo + hi)
            self.cells[v] = dict(lo=np.concatenate([C["lo"][keep], lo, mid]),
                                 hi=np.concatenate([C["hi"][keep], mid, hi]))


def slopes(x, b):
    lam = np.zeros(len(x))
    lam[2:] = b * x[2:]          # lam for bag v >= 2 (index v)
    return lam


def dp_min(T, P, lam, b, kappa, c):
    info = {}
    npairs = 0
    for v in reversed(T.topdown):
        L = P.leaves[v]
        l1, u1, l2, u2 = L["l1"], L["u1"], L["l2"], L["u2"]
        nl = len(l1)
        mc = np.zeros(nl)
        marg = {}
        lin_z1, lin_z2 = (c[0] if v == 1 else 0.0), c[v]
        for (u, coord) in T.children[v]:
            C = P.cells[u]
            lo_, hi_ = (l1, u1) if coord == 0 else (l2, u2)
            ck, cD = interval_pairs(C["lo"], C["hi"], lo_, hi_)
            mu, a = group_min(info[u]["beta"][cD], ck, nl)
            mc += mu
            marg[u] = cD[a]
            if coord == 0:
                lin_z1 += lam[u]
            else:
                lin_z2 += lam[u]
        if v == 1:
            val, z1, z2 = solve(l1, u1, l2, u2, l1.copy(), u1.copy(), np.full(nl, lin_z1),
                                np.full(nl, lin_z2), b, kappa, True)
            info[v] = dict(z1=z1, z2=z2, tot=val + mc, marg=marg)
            npairs += nl
            continue
        S = P.cells[v]
        bi, di = interval_pairs(S["lo"], S["hi"], l1, u1)
        npairs += len(bi)
        L1 = np.maximum(l1[bi], S["lo"][di])
        U1 = np.minimum(u1[bi], S["hi"][di])
        val, z1, z2 = solve(l1[bi], u1[bi], l2[bi], u2[bi], L1, U1,
                            np.full(len(bi), lin_z1 - lam[v]), np.full(len(bi), lin_z2),
                            b, kappa, False)
        beta, argpair = group_min(val + mc[bi], di, len(S["lo"]))
        info[v] = dict(z1=z1, z2=z2, bi=bi, beta=beta, argpair=argpair, marg=marg)
    tot = info[1]["tot"]
    lr = float(tot.min())
    k = int(tot.argmin())
    z = np.zeros((T.m, 2))
    leaf = {1: k}
    cell = {}
    z[1] = info[1]["z1"][k], info[1]["z2"][k]
    for v in T.topdown:
        if v == 1:
            continue
        pv = T.parent[v]
        d = info[pv]["marg"][v][leaf[pv]]
        cell[v] = int(d)
        q = info[v]["argpair"][d]
        leaf[v] = int(info[v]["bi"][q])
        z[v] = info[v]["z1"][q], info[v]["z2"][q]
    x = np.zeros(T.m)
    x[0] = z[1, 0]
    x[1:] = z[1:, 1]
    return dict(lr=lr, z=z, x=x, npairs=npairs, leaf=leaf, cell=cell)


def refine(T, P, z, W_next, W_cur, theta, R):
    nsl, nwide = {}, 0
    for v in T.bags:
        nsl[v] = 0
        while True:
            L = P.leaves[v]
            d1 = np.maximum(np.maximum(L["l1"] - z[v, 0], z[v, 0] - L["u1"]), 0.0)
            d2 = np.maximum(np.maximum(L["l2"] - z[v, 1], z[v, 1] - L["u2"]), 0.0)
            w = L["u1"] - L["l1"]
            lm = w > np.maximum(W_next, theta * np.maximum(np.maximum(d1, d2) - R * W_cur, 0.0)) * (1 + 1e-12)
            cm = None
            if v >= 2:
                C = P.cells[v]
                wc = C["hi"] - C["lo"]
                dc = np.maximum(np.maximum(C["lo"] - z[v, 0], z[v, 0] - C["hi"]), 0.0)
                cm = wc > np.maximum(W_next, theta * np.maximum(dc - R * W_cur, 0.0)) * (1 + 1e-12)
            if not lm.any() and (cm is None or not cm.any()):
                break
            nsl[v] += int(lm.sum())
            nwide += int(np.sum(w[lm] > W_cur * (1 + 1e-12)))
            if cm is not None:
                nwide += int(np.sum(wc[cm] > W_cur * (1 + 1e-12)))
            P.split(v, lm, cm)
    return nsl, nwide


def global_min_tree(m, b, kappa, c, G=2001):
    """Grid DP on the tree, then L-BFGS-B."""
    from scipy.optimize import minimize
    y = np.linspace(-1, 1, G)
    msg = {}
    arg = {}
    for v in range(m - 1, -1, -1):
        val = phi(y, kappa) + c[v] * y
        for u in (2 * v + 1, 2 * v + 2):
            if u < m:
                val = val + msg[u]
        if v == 0:
            root_val = val
            break
        M = b * y[:, None] * y[None, :] + val[None, :]   # rows: x_{p(v)}, cols: x_v
        arg[v] = np.argmin(M, axis=1)
        msg[v] = M[np.arange(G), arg[v]]
    idx = np.zeros(m, int)
    idx[0] = int(np.argmin(root_val))
    for v in range(1, m):
        idx[v] = arg[v][idx[(v - 1) // 2]]
    x0 = y[idx]
    r = minimize(lambda x: F(x, b, kappa, c), x0, jac=lambda x: grad(x, b, kappa, c),
                 bounds=[(-1, 1)] * m, method="L-BFGS-B",
                 options={"ftol": 1e-16, "gtol": 1e-13, "maxiter": 20000})
    return r.x, r.fun


def run_gr_tree(m, b, kappa, c, eps, x0, theta, R, jmax=40, xstar=None, fstar=None, log=None):
    T = TreeDecomp(m)
    P = TreePartition(m)
    UBD = F(x0, b, kappa, c)
    xprev = x0.copy()
    created = processed = 0
    recs = []
    for j in range(jmax + 1):
        W = 2.0 * 2.0 ** (-j)
        lam = slopes(xprev, b)
        nl, nc = P.size()
        processed += nl + nc
        D = dp_min(T, P, lam, b, kappa, c)
        UBD = min(UBD, F(D["x"], b, kappa, c))
        rec = dict(j=j, W=W, leaves=nl, cells=nc, npairs=D["npairs"], lr=D["lr"], UBD=UBD)
        if xstar is not None:
            p = (np.arange(1, m) - 1) // 2          # parent vertex of v (bag v holds (x_{p(v)}, x_v))
            zs = np.stack([xstar[p], xstar[1:]], 1)
            rec["zloc"] = float(np.abs(D["z"][1:] - zs).max()) / W
            rec["xloc"] = float(np.abs(D["x"] - xstar).max()) / W
            rec["x2"] = float(np.linalg.norm(D["x"] - xstar)) / W
            rec["nu_inf"] = float(np.abs(lam - slopes(xstar, b)).max())
        if fstar is not None:
            rec["gap"] = fstar - D["lr"]
        done = D["lr"] >= UBD - eps
        if not done and j < jmax:
            nsl, nwide = refine(T, P, D["z"], W / 2, W, theta, R)
            created += 4 * sum(nsl.values())
            rec["split_leaf_max"] = max(nsl.values())
            rec["split_leaf_mean"] = float(np.mean(list(nsl.values())))
            rec["wide"] = nwide
        recs.append(rec)
        if log:
            log(rec)
        if done:
            return dict(done=True, j=j, size=nl + nc, leaves=nl, cells=nc, lr=D["lr"], UBD=UBD,
                        created=created, processed=processed), recs
        xprev = D["x"]
    return dict(done=False, created=created, processed=processed), recs


def fmt(r):
    s = "j=%2d W=%.3e leaves=%8d cells=%6d pairs=%8d lr=% .5e UBD=% .5e" % (
        r["j"], r["W"], r["leaves"], r["cells"], r["npairs"], r["lr"], r["UBD"])
    if "zloc" in r:
        s += " zloc=%.3f xloc=%.3f x2=%.2f nu_inf/W=%.2f" % (r["zloc"], r["xloc"], r["x2"], r["nu_inf"] / r["W"])
    if "gap" in r:
        s += " gap=%.3e gap/(m-1)W^2=%.3g" % (r["gap"], r["gap"] / (r["m"] - 1) / r["W"] ** 2)
    if "split_leaf_max" in r:
        s += " split=%d/%.1f wide=%d" % (r["split_leaf_max"], r["split_leaf_mean"], r["wide"])
    return s


def main():
    """python3 tree_gr.py MODE MMIN MMAX EPS THETA R B   (MODE = zero: c = 0; random: c ~ U(-0.2,0.2), seed 0)
    m = MMIN, 2 MMIN + 1, ... <= MMAX (complete binary trees)."""
    mode = sys.argv[1]
    mmin, mmax, eps = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    theta, R, b = 1.0 / float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])
    kappa = 0.1
    m = mmin
    while m <= mmax:
        if mode == "zero":
            c = np.zeros(m)
            xs, fs = np.zeros(m), 0.0
            x0 = np.full(m, 0.5)
        else:
            c = np.random.default_rng(0).uniform(-0.2, 0.2, m)
            xs, fs = global_min_tree(m, b, kappa, c)
            x0 = np.zeros(m)
            print("m=%d: f* = %.10f |x*|_inf = %.3f |grad|_inf = %.1e" % (
                m, fs, np.abs(xs).max(), np.abs(grad(xs, b, kappa, c)).max()), flush=True)
        t0 = time.time()

        def log(r):
            r["m"] = m
            print(fmt(r), flush=True)
        res, recs = run_gr_tree(m, b, kappa, c, eps, x0, theta, R, xstar=xs, fstar=fs, log=log)
        print("SUMMARY tree-%s m=%d b=%.2f eps=%.0e theta=1/%d R=%g done=%s stages=%s size=%s "
              "size_per_bag=%.0f created=%d processed=%d max_split=%d max_zloc=%.3f wide=%d time=%.1fs" % (
                  mode, m, b, eps, round(1 / theta), R, res["done"], res.get("j"), res.get("size"),
                  (res.get("size") or 0) / (m - 1), res["created"], res["processed"],
                  max(r.get("split_leaf_max", 0) for r in recs), max(r["zloc"] for r in recs),
                  sum(r.get("wide", 0) for r in recs), time.time() - t0), flush=True)
        m = 2 * m + 1


if __name__ == "__main__":
    main()
