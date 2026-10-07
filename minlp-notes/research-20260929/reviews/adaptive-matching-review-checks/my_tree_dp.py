"""Independent dynamic program for the binary-tree decomposition of adaptive-matching.md Section 8.4,
used to drive GR and compare with the authors' logs (tree_zero_eps1e-4.log, tree_random_eps1e-4.log).

Reused from the authors' tree_gr.py: TreeDecomp (bag tree), TreePartition (box storage), refine (step 4),
F. Written here: the bag solver (golden section on z1, projected Newton on z2), the bottom-up DP, the
reconstruction of the minimizing configuration with its leaves and cells, the exact re-evaluation of
the relaxed value Phi(c) of Lemma 1.5 (must equal l_r) with the configuration constraints, x* by
multistart L-BFGS-B, and zloc with the parent vertex computed from the bag structure.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys
import time
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-decomposition/adaptive2'))
import tree_gr as TG  # noqa: E402

GOLD = (np.sqrt(5.0) - 1.0) / 2.0


def phi(t, kappa):
    return t * t - kappa * t ** 4


def bag_rel(z1, z2, B, b, kappa, root, c0, cv):
    l1, u1, l2, u2 = B
    v = b * z1 * z2 - 0.5 * abs(b) * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2)) + phi(z2, kappa) + cv * z2
    if root:
        v = v + phi(z1, kappa) + c0 * z1
    return v


def solve(B, L1, U1, a1, a2, b, kappa, root, c0, cv):
    l1, u1, l2, u2 = B
    ab = abs(b)

    def z2opt(z1):
        z2 = 0.5 * (l2 + u2)
        for _ in range(40):
            d = b * z1 + ab * (z2 - 0.5 * (l2 + u2)) + 2 * z2 - 4 * kappa * z2 ** 3 + cv + a2
            z2 = np.clip(z2 - d / (ab + 2 - 12 * kappa * z2 ** 2), l2, u2)
        return z2

    def h(z1):
        z2 = z2opt(z1)
        return bag_rel(z1, z2, B, b, kappa, root, c0, cv) + a1 * z1 + a2 * z2

    a, d = L1.copy(), U1.copy()
    for _ in range(90):
        x1 = d - GOLD * (d - a)
        x2 = a + GOLD * (d - a)
        left = h(x1) <= h(x2)
        d = np.where(left, x2, d)
        a = np.where(left, a, x1)
    cand = np.stack([L1, U1, 0.5 * (a + d)])
    vals = np.stack([h(L1), h(U1), h(0.5 * (a + d))])
    k = np.argmin(vals, axis=0)
    z1 = cand[k, np.arange(len(L1))]
    return h(z1), z1, z2opt(z1)


def meet(lo, hi, l, u):
    return np.nonzero((l[:, None] <= hi[None, :]) & (lo[None, :] <= u[:, None]))


def dp(T, P, lam, b, kappa, c):
    info = {}
    for v in reversed(T.topdown):
        L = P.leaves[v]
        Bx = (L["l1"], L["u1"], L["l2"], L["u2"])
        nl = len(L["l1"])
        mc = np.zeros(nl)
        a1 = np.zeros(nl)
        a2 = np.zeros(nl)
        marg = {}
        for (u, coord) in T.children[v]:
            C = P.cells[u]
            lo_, hi_ = (L["l1"], L["u1"]) if coord == 0 else (L["l2"], L["u2"])
            i, k = meet(C["lo"], C["hi"], lo_, hi_)
            beta = info[u]["beta"]
            m = np.full(nl, np.inf)
            np.minimum.at(m, i, beta[k])
            order = np.lexsort((beta[k], i))
            first = np.ones(len(order), bool)
            first[1:] = i[order][1:] != i[order][:-1]
            ag = np.full(nl, -1)
            ag[i[order][first]] = k[order][first]
            mc += m
            marg[u] = ag
            if coord == 0:
                a1 += lam[u]
            else:
                a2 += lam[u]
        root = v == 1
        if root:
            val, z1, z2 = solve(Bx, L["l1"], L["u1"], a1, a2, b, kappa, True, c[0], c[v])
            info[v] = dict(tot=val + mc, z1=z1, z2=z2, marg=marg)
            continue
        S = P.cells[v]
        bi, di = meet(S["lo"], S["hi"], L["l1"], L["u1"])
        Bp = tuple(x[bi] for x in Bx)
        L1 = np.maximum(L["l1"][bi], S["lo"][di])
        U1 = np.minimum(L["u1"][bi], S["hi"][di])
        val, z1, z2 = solve(Bp, L1, U1, a1[bi] - lam[v], a2[bi], b, kappa, False, 0.0, c[v])
        tot = val + mc[bi]
        nc = len(S["lo"])
        beta = np.full(nc, np.inf)
        np.minimum.at(beta, di, tot)
        order = np.lexsort((tot, di))
        first = np.ones(len(order), bool)
        first[1:] = di[order][1:] != di[order][:-1]
        parg = np.full(nc, -1)
        parg[di[order][first]] = order[first]
        info[v] = dict(beta=beta, parg=parg, bi=bi, z1=z1, z2=z2, marg=marg)
    k0 = int(np.argmin(info[1]["tot"]))
    lr = float(info[1]["tot"][k0])
    z = np.zeros((T.m, 2))
    leaf, cell = {1: k0}, {}
    z[1] = info[1]["z1"][k0], info[1]["z2"][k0]
    for v in T.topdown[1:]:
        pv = T.parent[v]
        d = info[pv]["marg"][v][leaf[pv]]
        q = info[v]["parg"][d]
        cell[v] = d
        leaf[v] = int(info[v]["bi"][q])
        z[v] = info[v]["z1"][q], info[v]["z2"][q]
    return lr, z, leaf, cell


def phi_config(T, P, lam, b, kappa, c, z, leaf, cell):
    """Relaxed value of the configuration (Lemma 1.5) and constraint check."""
    val, ok = 0.0, True
    for v in T.bags:
        L = P.leaves[v]
        B = tuple(L[k][leaf[v]] for k in ("l1", "u1", "l2", "u2"))
        ok &= B[0] - 1e-12 <= z[v, 0] <= B[1] + 1e-12 and B[2] - 1e-12 <= z[v, 1] <= B[3] + 1e-12
        val += float(bag_rel(z[v, 0], z[v, 1], B, b, kappa, v == 1, c[0], c[v]))
        if v >= 2:
            pv = T.parent[v]
            coord = 0 if v == 2 else 1          # coordinate of the parent bag carrying x_{p(v)}
            Lp = P.leaves[pv]
            plo = Lp["l1" if coord == 0 else "l2"][leaf[pv]]
            phi_ = Lp["u1" if coord == 0 else "u2"][leaf[pv]]
            C = P.cells[v]
            lo, hi = C["lo"][cell[v]], C["hi"][cell[v]]
            ok &= lo - 1e-12 <= z[v, 0] <= hi + 1e-12 and plo <= hi and lo <= phi_
            val += lam[v] * (z[pv, coord] - z[v, 0])
    return val, bool(ok)


def xstar_multistart(m, b, kappa, c, starts=40, seed=5):
    rng = np.random.default_rng(seed)
    best = None
    for s in range(starts):
        x0 = rng.uniform(-1, 1, m) if s else np.zeros(m)
        r = minimize(lambda x: TG.F(x, b, kappa, c), x0, jac=lambda x: TG.grad(x, b, kappa, c),
                     bounds=[(-1, 1)] * m, method="L-BFGS-B", options={"ftol": 1e-16, "gtol": 1e-13, "maxiter": 20000})
        if best is None or r.fun < best.fun:
            best = r
    return best.x, best.fun


def main():
    mode, m, eps, thinv, R, b, jmax = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), \
        float(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
    kappa = 0.1
    theta = 1.0 / thinv
    if mode == "zero":
        c, xs, fs, x0 = np.zeros(m), np.zeros(m), 0.0, np.full(m, 0.5)
    else:
        c = np.random.default_rng(0).uniform(-0.2, 0.2, m)
        xs, fs = xstar_multistart(m, b, kappa, c)
        xa, fa = TG.global_min_tree(m, b, kappa, c)
        print("x* multistart f*=%.10f; authors' grid+LBFGS f*=%.10f; |x*-x*_auth|_inf=%.1e" % (fs, fa, np.abs(xs - xa).max()))
        x0 = np.zeros(m)
    T, P = TG.TreeDecomp(m), TG.TreePartition(m)
    # parent vertex of the first coordinate of bag v, from the bag structure: bag v = (x_{p(v)}, x_v)
    pvert = {v: (v - 1) // 2 for v in T.bags}
    UBD = TG.F(x0, b, kappa, c)
    xprev = x0.copy()
    t0 = time.time()
    for j in range(jmax + 1):
        W = 2.0 * 2.0 ** (-j)
        lam = TG.slopes(xprev, b)
        nl, nc = P.size()
        lr, z, leaf, cell = dp(T, P, lam, b, kappa, c)
        val, ok = phi_config(T, P, lam, b, kappa, c, z, leaf, cell)
        x = np.zeros(m)
        x[0] = z[1, 0]
        x[1:] = z[1:, 1]
        UBD = min(UBD, TG.F(x, b, kappa, c))
        zloc = max(max(abs(z[v, 0] - xs[pvert[v]]), abs(z[v, 1] - xs[v])) for v in T.bags) / W
        done = lr >= UBD - eps
        print("j=%2d leaves=%8d cells=%6d lr=% .6e UBD=% .6e zloc=%.3f cfg_ok=%s Phi(c)-lr=%.1e lr<=f*:%s" % (
            j, nl, nc, lr, UBD, zloc, ok, val - lr, lr <= fs + 1e-12), flush=True)
        if done:
            break
        TG.refine(T, P, z, W / 2, W, theta, R)
        xprev = x
    print("MYTREE m=%d mode=%s done=%s stage=%d size=%d time=%.1fs" % (m, mode, done, j, nl + nc, time.time() - t0))


if __name__ == "__main__":
    main()
