"""Independent re-implementation of algorithm GR (adaptive-matching.md, Section 3.1) on the path
family of Theorem 4.1 of decomposition-certificates.md, written for the review without importing
the authors' code (ls_lib.py, gr_lib.py, dp_certificate.py).

F(x) = sum_i (x_i^2 - kappa x_i^4 + c_i x_i) + b sum_i x_i x_{i+1} on [-1,1]^n.
Bags t = 0..n-2, V_t = {t, t+1}, root bag 0, separator S_t = {t} (t >= 1).
Bag t holds phi(x_t) + c_t x_t + b x_t x_{t+1}; the last bag also phi(x_{n-1}) + c_{n-1} x_{n-1}.
Relaxation: alphaBB on the bilinear term with alpha = |b|/2 (unary terms exact, convex on [-1,1]).

Differences from the authors' code, on purpose:
  * convex subproblems: golden-section search on z1 (function values only), z2 in closed form
    (non-last bags) or by an inner golden-section search (last bag); no derivative bisection;
  * leaf-cell pairs: brute-force closed-interval intersection (broadcast), no sorting;
  * the minimizing configuration is re-evaluated from scratch (Phi(c) of Lemma 1.5) and its
    configuration constraints are checked.
Floating point; illustrations only.
"""
import sys
import time
import numpy as np

GOLD = (np.sqrt(5.0) - 1.0) / 2.0
NIT = 90


def phi(t, kappa):
    return t * t - kappa * t ** 4


def Fval(x, b, kappa, c):
    return float(np.sum(phi(x, kappa) + c * x) + b * np.sum(x[:-1] * x[1:]))


def relaxed_bag(z1, z2, l1, u1, l2, u2, b, kappa, c1, last, c2):
    ab = abs(b)
    v = phi(z1, kappa) + c1 * z1 + b * z1 * z2 - 0.5 * ab * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2))
    if last:
        v = v + phi(z2, kappa) + c2 * z2
    return v


def golden_min(fun, lo, hi):
    """vectorized golden-section minimization of convex fun on [lo, hi]; returns argmin."""
    a, d = lo.copy(), hi.copy()
    x1 = d - GOLD * (d - a)
    x2 = a + GOLD * (d - a)
    f1, f2 = fun(x1), fun(x2)
    for _ in range(NIT):
        left = f1 <= f2
        d = np.where(left, x2, d)
        a = np.where(left, a, x1)
        nx1 = d - GOLD * (d - a)
        nx2 = a + GOLD * (d - a)
        x2n = np.where(left, x1, nx2)
        x1n = np.where(left, nx1, x2)
        f2n = np.where(left, f1, np.nan)
        f1n = np.where(left, np.nan, f2)
        # evaluate only the new points (cheap enough to evaluate both)
        fx1, fx2 = fun(x1n), fun(x2n)
        x1, x2, f1, f2 = x1n, x2n, fx1, fx2
    xs = np.stack([lo, hi, 0.5 * (a + d)])
    vals = np.stack([fun(lo), fun(hi), fun(0.5 * (a + d))])
    k = np.argmin(vals, axis=0)
    return xs[k, np.arange(len(lo))]


def bag_min(l1, u1, l2, u2, L1, U1, a1, a2, b, kappa, c1, last, c2):
    """min over z1 in [L1,U1], z2 in [l2,u2] of relaxed bag + a1 z1 + a2 z2."""
    ab = abs(b)

    def z2opt(z1):
        if not last:
            # d/dz2: b z1 + ab (z2 - (l2+u2)/2) + a2 = 0
            return np.clip(0.5 * (l2 + u2) - (b * z1 + a2) / ab, l2, u2)
        # inner convex 1D problem in z2: projected Newton on the monotone derivative
        # d(z2) = b z1 + ab (z2 - (l2+u2)/2) + 2 z2 - 4 kappa z2^3 + c2 + a2, with
        # d' in [ab + 2 - 12 kappa, ab + 2] (ratio < 1.5 for kappa = 0.1), so the iteration contracts.
        z2 = 0.5 * (l2 + u2)
        for _ in range(40):
            d = b * z1 + ab * (z2 - 0.5 * (l2 + u2)) + 2 * z2 - 4 * kappa * z2 ** 3 + c2 + a2
            dd = ab + 2 - 12 * kappa * z2 ** 2
            z2 = np.clip(z2 - d / dd, l2, u2)
        return z2

    def h(z1):
        z2 = z2opt(z1)
        return relaxed_bag(z1, z2, l1, u1, l2, u2, b, kappa, c1, last, c2) + a1 * z1 + a2 * z2

    z1 = golden_min(h, L1, U1)
    z2 = z2opt(z1)
    return h(z1), z1, z2


class Part:
    def __init__(self, n):
        self.n = n
        one = lambda: np.array([-1.0])
        two = lambda: np.array([1.0])
        self.L = [dict(l1=one(), u1=two(), l2=one(), u2=two()) for _ in range(n - 1)]
        self.C = [None] + [dict(lo=one(), hi=two()) for _ in range(1, n - 1)]

    def size(self):
        return sum(len(L["l1"]) for L in self.L), sum(len(C["lo"]) for C in self.C[1:])


def pairs(lo, hi, l, u):
    """indices (i, k) with closed intervals [l_i,u_i] and [lo_k,hi_k] intersecting."""
    M = (l[:, None] <= hi[None, :]) & (lo[None, :] <= u[:, None])
    return np.nonzero(M)


def dp(P, lam, b, kappa, c):
    n = P.n
    info = [None] * (n - 1)
    for t in range(n - 2, -1, -1):
        L = P.L[t]
        last = t == n - 2
        nl = len(L["l1"])
        a2 = 0.0 if last else lam[t + 1]
        if not last:
            Cc = P.C[t + 1]
            i, k = pairs(Cc["lo"], Cc["hi"], L["l2"], L["u2"])
            beta = info[t + 1]["beta"]
            mc = np.full(nl, np.inf)
            np.minimum.at(mc, i, beta[k])
            # argmin cell per leaf
            marg = np.full(nl, -1)
            order = np.lexsort((beta[k], i))
            first = np.ones(len(order), bool)
            first[1:] = i[order][1:] != i[order][:-1]
            marg[i[order][first]] = k[order][first]
        else:
            mc = np.zeros(nl)
            marg = np.full(nl, -1)
        if t == 0:
            val, z1, z2 = bag_min(L["l1"], L["u1"], L["l2"], L["u2"], L["l1"], L["u1"],
                                  np.zeros(nl), np.full(nl, a2), b, kappa, c[0], last, c[n - 1])
            info[0] = dict(tot=val + mc, z1=z1, z2=z2, marg=marg)
            continue
        S = P.C[t]
        bi, di = pairs(S["lo"], S["hi"], L["l1"], L["u1"])
        L1 = np.maximum(L["l1"][bi], S["lo"][di])
        U1 = np.minimum(L["u1"][bi], S["hi"][di])
        val, z1, z2 = bag_min(L["l1"][bi], L["u1"][bi], L["l2"][bi], L["u2"][bi], L1, U1,
                              np.full(len(bi), -lam[t]), np.full(len(bi), a2), b, kappa, c[t], last, c[n - 1])
        tot = val + mc[bi]
        nc = len(S["lo"])
        beta = np.full(nc, np.inf)
        np.minimum.at(beta, di, tot)
        order = np.lexsort((tot, di))
        first = np.ones(len(order), bool)
        first[1:] = di[order][1:] != di[order][:-1]
        parg = np.full(nc, -1)
        parg[di[order][first]] = order[first]
        info[t] = dict(beta=beta, parg=parg, bi=bi, z1=z1, z2=z2, marg=marg, npairs=len(bi))
    k0 = int(np.argmin(info[0]["tot"]))
    lr = float(info[0]["tot"][k0])
    z = np.zeros((n - 1, 2))
    leaf = np.zeros(n - 1, int)
    cell = np.full(n - 1, -1)
    z[0] = info[0]["z1"][k0], info[0]["z2"][k0]
    leaf[0] = k0
    d = info[0]["marg"][k0]
    for t in range(1, n - 1):
        q = info[t]["parg"][d]
        cell[t] = d
        leaf[t] = info[t]["bi"][q]
        z[t] = info[t]["z1"][q], info[t]["z2"][q]
        d = info[t]["marg"][leaf[t]]
    x = np.concatenate([[z[0, 0]], z[:, 1]])
    npairs = sum(info[t]["npairs"] for t in range(1, n - 1)) + len(P.L[0]["l1"])
    return lr, z, leaf, cell, x, npairs


def check_config(P, lam, b, kappa, c, z, leaf, cell, lr):
    """Re-evaluate Phi(c) of Lemma 1.5 and check the configuration constraints."""
    n = P.n
    val = 0.0
    ok = True
    tol = 1e-12
    for t in range(n - 1):
        L = P.L[t]
        B = (L["l1"][leaf[t]], L["u1"][leaf[t]], L["l2"][leaf[t]], L["u2"][leaf[t]])
        ok &= B[0] - tol <= z[t, 0] <= B[1] + tol and B[2] - tol <= z[t, 1] <= B[3] + tol
        val += float(relaxed_bag(z[t, 0], z[t, 1], *B, b, kappa, c[t], t == n - 2, c[n - 1]))
        if t >= 1:
            S = P.C[t]
            lo, hi = S["lo"][cell[t]], S["hi"][cell[t]]
            ok &= lo - tol <= z[t, 0] <= hi + tol
            Lp = P.L[t - 1]
            ok &= Lp["l2"][leaf[t - 1]] <= hi and lo <= Lp["u2"][leaf[t - 1]]
            val += lam[t] * (z[t - 1, 1] - z[t, 0])
    return bool(ok), val - lr


def slopes(x, b, kappa, c):
    lam = np.zeros(len(x))
    for t in range(1, len(x) - 1):
        lam[t] = 2 * x[t] - 4 * kappa * x[t] ** 3 + c[t] + b * x[t + 1]
    return lam


def refine(P, z, Wn, W, theta, R):
    n = P.n
    split_leaf = np.zeros(n - 1, int)
    wide = 0
    for t in range(n - 1):
        while True:
            L = P.L[t]
            dist = np.maximum.reduce([L["l1"] - z[t, 0], z[t, 0] - L["u1"], L["l2"] - z[t, 1], z[t, 1] - L["u2"],
                                      np.zeros(len(L["l1"]))])
            w = L["u1"] - L["l1"]
            lm = w > np.maximum(Wn, theta * np.maximum(dist - R * W, 0.0)) * (1 + 1e-12)
            cm = np.zeros(0, bool)
            if t >= 1:
                S = P.C[t]
                dc = np.maximum.reduce([S["lo"] - z[t, 0], z[t, 0] - S["hi"], np.zeros(len(S["lo"]))])
                wc = S["hi"] - S["lo"]
                cm = wc > np.maximum(Wn, theta * np.maximum(dc - R * W, 0.0)) * (1 + 1e-12)
            if not lm.any() and not cm.any():
                break
            split_leaf[t] += int(lm.sum())
            wide += int(np.sum(w[lm] > W * (1 + 1e-12)))
            if lm.any():
                keep = ~lm
                l1, u1, l2, u2 = (L[k][lm] for k in ("l1", "u1", "l2", "u2"))
                m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
                new = {k: [L[k][keep]] for k in L}
                for a1, b1 in ((l1, m1), (m1, u1)):
                    for a2, b2 in ((l2, m2), (m2, u2)):
                        new["l1"].append(a1); new["u1"].append(b1); new["l2"].append(a2); new["u2"].append(b2)
                P.L[t] = {k: np.concatenate(v) for k, v in new.items()}
            if cm.any():
                S = P.C[t]
                wide += int(np.sum(wc[cm] > W * (1 + 1e-12)))
                keep = ~cm
                lo, hi = S["lo"][cm], S["hi"][cm]
                mid = 0.5 * (lo + hi)
                P.C[t] = dict(lo=np.concatenate([S["lo"][keep], lo, mid]), hi=np.concatenate([S["hi"][keep], mid, hi]))
    return split_leaf, wide


def graded_viol(P, xs, W, theta):
    v = 0
    for t in range(P.n - 1):
        L = P.L[t]
        d = np.maximum.reduce([L["l1"] - xs[t], xs[t] - L["u1"], L["l2"] - xs[t + 1], xs[t + 1] - L["u2"],
                               np.zeros(len(L["l1"]))])
        v += int(np.sum(L["u1"] - L["l1"] > np.maximum(W, theta * d) * (1 + 1e-12)))
        if t >= 1:
            S = P.C[t]
            dc = np.maximum.reduce([S["lo"] - xs[t], xs[t] - S["hi"], np.zeros(len(S["lo"]))])
            v += int(np.sum(S["hi"] - S["lo"] > np.maximum(W, theta * dc) * (1 + 1e-12)))
    return v


def run(n, b, kappa, c, eps, x0, theta, R, xs, fs, jmax=30, verbose=True):
    P = Part(n)
    UBD = Fval(x0, b, kappa, c)
    xprev = x0.copy()
    created = processed = 0
    t0 = time.time()
    maxsplit = 0
    maxz = 0.0
    tot_wide = 0
    for j in range(jmax + 1):
        W = 2.0 * 2.0 ** (-j)
        lam = slopes(xprev, b, kappa, c)
        nl, nc = P.size()
        processed += nl + nc
        lr, z, leaf, cell, x, npairs = dp(P, lam, b, kappa, c)
        ok, dval = check_config(P, lam, b, kappa, c, z, leaf, cell, lr)
        UBD = min(UBD, Fval(x, b, kappa, c))
        zs = np.stack([xs[:-1], xs[1:]], 1)
        zloc = float(np.abs(z - zs).max()) / W
        maxz = max(maxz, zloc)
        gv = graded_viol(P, xs, W, theta)
        done = lr >= UBD - eps
        line = ("j=%2d W=%.3e leaves=%8d cells=%6d pairs=%8d lr=% .6e UBD=% .6e gap=%.3e zloc=%.3f gviol=%d "
                "cfg_ok=%s cfg_val-lr=%.1e lr<=f*:%s" % (j, W, nl, nc, npairs, lr, UBD, fs - lr, zloc, gv, ok, dval,
                                                       lr <= fs + 1e-12))
        if not done and j < jmax:
            sl, wide = refine(P, z, W / 2, W, theta, R)
            created += 4 * int(sl.sum())
            for t in range(1, n - 1):
                pass
            maxsplit = max(maxsplit, int(sl.max()))
            tot_wide += wide
            line += " split=%d wide=%d" % (sl.max(), wide)
        if verbose:
            print(line, flush=True)
        if done:
            break
        xprev = x
    nl, nc = P.size()
    print("MYSUMMARY n=%d b=%.2f eps=%.0e theta=1/%d R=%g done=%s stage=%d size=%d (per bag %.0f) leaves=%d cells=%d "
          "processed=%d max_split=%d max_zloc=%.3f wide=%d time=%.1fs" % (
              n, b, eps, round(1 / theta), R, done, j, nl + nc, (nl + nc) / (n - 1), nl, nc, processed, maxsplit, maxz,
              tot_wide, time.time() - t0), flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    b, kappa = 0.8, 0.1
    if mode == "zero":
        n, eps, th, R = int(sys.argv[2]), float(sys.argv[3]), 1.0 / float(sys.argv[4]), float(sys.argv[5])
        if len(sys.argv) > 6:
            b = float(sys.argv[6])
        jmax = int(sys.argv[7]) if len(sys.argv) > 7 else 30
        run(n, b, kappa, np.zeros(n), eps, np.full(n, 0.5), th, R, np.zeros(n), 0.0, jmax=jmax)
