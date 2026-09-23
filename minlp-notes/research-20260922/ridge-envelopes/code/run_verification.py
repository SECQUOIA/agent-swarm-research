"""Numerical verification of Theorem 1 and Corollary 3 in ../theory.md.

Usage: python run_verification.py [box|simplex|gain|grid|sshape|all]
Writes JSON records to results/ and prints summaries.
"""
import itertools
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from activations import SIGMAS, negated  # noqa: E402
from bruteforce import (box_as_simplices, certified_bounds, exact_cut_violation_box,  # noqa: E402
                        exact_cut_violation_simplices, grid_upper_box)
from ridge_envelope import (chain_law, envelope_box, envelope_simplices_merge,  # noqa: E402
                            envelope_simplices_tailsum, normalize, solve_D, vex_interval_hull)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
GRID_N = {1: 401, 2: 61, 3: 21, 4: 11, 5: 7}


def functions():
    fs = []
    for name, sig in SIGMAS.items():
        fs.append((name, "vex"))
        fs.append((name, "cave"))  # concave envelope = -vex(-sigma)
    return fs


def get_sigma(name, side):
    return SIGMAS[name] if side == "vex" else negated(SIGMAS[name])


def random_box(rng, n):
    if rng.random() < 0.5:
        l, u = -rng.uniform(0.1, 2, n), rng.uniform(0.1, 2, n)  # boxes crossing zero
    else:
        l = rng.uniform(-3, 3, n)
        u = l + rng.uniform(0.2, 3, n)
    a = rng.uniform(-1, 1, n)
    if n > 1 and rng.random() < 0.15:
        a[rng.integers(n)] = 0.0
    lo = np.sum(np.minimum(a * l, a * u))
    hi = np.sum(np.maximum(a * l, a * u))
    W, center = rng.uniform(0.5, 8.0), rng.uniform(-3.0, 3.0)
    a = a * W / (hi - lo)
    b = center - W * (lo + hi) / (2 * (hi - lo))
    return l, u, a, b


def random_point(rng, l, u, a, kind):
    n = len(l)
    xi = rng.uniform(0, 1, n)
    if kind == "ties" and n > 1:
        # ties in the normalized coordinates (after the sign flips)
        nd_sgn = np.where(a >= 0, 1.0, -1.0)
        xn = rng.uniform(0, 1, n)
        i, j = rng.choice(n, 2, replace=False)
        xn[j] = xn[i]
        if n > 3:
            k = [q for q in range(n) if q not in (i, j)][0]
            xn[k] = xn[i]
        xi = np.where(nd_sgn > 0, xn, 1 - xn)
    elif kind == "boundary":
        mask = rng.random(n) < 0.5
        xi[mask] = rng.integers(0, 2, mask.sum())
    elif kind == "vertex":
        xi = rng.integers(0, 2, n).astype(float)
    return l + (u - l) * xi


def f_range(sig, lo, hi):
    v = sig(np.linspace(lo, hi, 20001))
    return float(max(v.max() - v.min(), 1e-12)), v


def curvature(v):
    d2 = v[2:] - 2 * v[1:-1] + v[:-2]
    tol = 1e-12 * max(1.0, np.abs(v).max())
    if np.all(d2 >= -tol):
        return "convex"
    if np.all(d2 <= tol):
        return "concave"
    return "mixed"


# ---------------------------------------------------------------- box (tasks 2, 3, 6)
def box_job(args):
    name, side, seed = args
    sig = get_sigma(name, side)
    rng = np.random.default_rng(seed)
    recs = []
    kinds = ["interior", "interior", "ties", "boundary", "vertex"]
    for n in range(1, 6):
        for inst in range(6):
            l, u, a, b = random_box(rng, n)
            lo = b + np.sum(np.minimum(a * l, a * u))
            hi = b + np.sum(np.maximum(a * l, a * u))
            R, vals = f_range(sig, lo, hi)
            curv = curvature(vals)
            Zs = rng.uniform(l, u, size=(100000, n))
            fZs = sig(Zs @ a + b)
            V = np.array(list(itertools.product(*[[l[i], u[i]] for i in range(n)])))
            fV = sig(V @ a + b)
            for q in range(2):
                kind = kinds[(inst * 2 + q) % len(kinds)]
                x = random_point(rng, l, u, a, kind)
                E = envelope_box(sig, l, u, a, b, x)
                C, X = box_as_simplices(l, u, a, x)
                B = certified_bounds(sig, C, b, X)
                grid = grid_upper_box(sig, l, u, a, b, x, GRID_N[n]) if q == 0 else None
                h = lambda Z: E["c0"] + Z @ E["g"]
                viol_sample = float(np.max(h(Zs) - fZs))
                viol_vert = float(np.max(h(V) - fV))
                viol_exact = float(exact_cut_violation_box(sig, l, u, a, b, E["c0"], E["g"]))
                fx = float(sig(np.array([a @ x + b]))[0])
                lovasz = float(E["p"] @ sig(E["t"]))
                recs.append(dict(
                    sigma=name, side=side, n=n, inst=inst, kind=kind, R=R, curv=curv,
                    thm_low=E["value"], thm_up=E["value_up"], thm_viol=E["viol"],
                    bf_low=B["low"], bf_up=B["up"], bf_iters=B["iters"], grid=grid,
                    cut_at_x=float(h(x)), viol_sample=viol_sample, viol_vert=viol_vert,
                    viol_exact=viol_exact, fx=fx, lovasz=lovasz,
                ))
    return recs


def summarize_box(recs, tol=1e-7):
    print("\n=== Box: Theorem 1 vs certified brute force (values / R, R = range of f over B) ===")
    print(f"{'sigma':16s}{'side':5s}{'cases':>6s}{'max|thm-bf|':>13s}{'max bf gap':>12s}"
          f"{'max sep':>10s}{'thm>grid':>10s}{'cut viol smp':>14s}{'cut viol ex':>13s}")
    worst = dict(dis=0, sep=0, grid=-np.inf, vs=-np.inf, ve=-np.inf, gap=0)
    flagged = []
    for (name, side) in functions():
        rs = [r for r in recs if r["sigma"] == name and r["side"] == side]
        if not rs:
            continue
        dis = max(abs(0.5 * (r["thm_low"] + r["thm_up"]) - 0.5 * (r["bf_low"] + r["bf_up"])) / r["R"] for r in rs)
        gap = max((r["bf_up"] - r["bf_low"]) / r["R"] for r in rs)
        sep = max(max(r["thm_low"] - r["bf_up"], r["bf_low"] - r["thm_up"], 0) / r["R"] for r in rs)
        gr = max(((r["thm_low"] - r["grid"]) / r["R"]) for r in rs if r["grid"] is not None)
        vs = max(max(r["viol_sample"], r["viol_vert"]) / r["R"] for r in rs)
        ve = max(r["viol_exact"] / r["R"] for r in rs)
        print(f"{name:16s}{side:5s}{len(rs):6d}{dis:13.2e}{gap:12.2e}{sep:10.2e}{gr:10.2e}{vs:14.2e}{ve:13.2e}")
        worst = dict(dis=max(worst["dis"], dis), sep=max(worst["sep"], sep), grid=max(worst["grid"], gr),
                     vs=max(worst["vs"], vs), ve=max(worst["ve"], ve), gap=max(worst["gap"], gap))
        for r in rs:
            s = max(r["thm_low"] - r["bf_up"], r["bf_low"] - r["thm_up"], 0) / r["R"]
            if s > tol or r["viol_exact"] / r["R"] > tol or max(r["viol_sample"], r["viol_vert"]) / r["R"] > tol:
                flagged.append(r)
    print("overall worst:", {k: f"{v:.2e}" for k, v in worst.items()})
    print(f"flagged cases (> {tol:g} R):", len(flagged))
    for r in flagged[:20]:
        print("  ", r)
    tight = max(abs(r["cut_at_x"] - r["thm_low"]) / r["R"] for r in recs)
    print(f"max |h(x) - value| / R: {tight:.2e}")
    # special cases claimed in theory.md
    cx = [r for r in recs if r["curv"] == "convex"]
    cc = [r for r in recs if r["curv"] == "concave"]
    if cx:
        print(f"sigma convex on I ({len(cx)} cases): max |vex - f(x)|/R = "
              f"{max(abs(r['thm_low'] - r['fx']) / r['R'] for r in cx):.2e}")
    if cc:
        print(f"sigma concave on I ({len(cc)} cases): max |vex - sum p sigma(t)|/R = "
              f"{max(abs(r['thm_low'] - r['lovasz']) / r['R'] for r in cc):.2e}")
    kinds = sorted(set(r["kind"] for r in recs))
    for k in kinds:
        rk = [r for r in recs if r["kind"] == k]
        print(f"  point kind {k:9s}: {len(rk):5d} cases, max |thm-bf|/R = "
              f"{max(abs(r['thm_low'] - r['bf_low']) / r['R'] for r in rk):.2e}")
    return flagged


# ------------------------------------------------------- grid convergence illustration
def grid_job(args):
    name, seed = args
    sig = SIGMAS[name]
    rng = np.random.default_rng(seed)
    out = []
    for n in (2, 3):
        l, u, a, b = random_box(rng, n)
        x = random_point(rng, l, u, a, "interior")
        lo = b + np.sum(np.minimum(a * l, a * u))
        hi = b + np.sum(np.maximum(a * l, a * u))
        R, _ = f_range(sig, lo, hi)
        E = envelope_box(sig, l, u, a, b, x)
        Ns = (6, 11, 21, 41, 81, 161) if n == 2 else (6, 11, 21, 31, 41)
        out.append(dict(sigma=name, n=n, gaps=[(N, (grid_upper_box(sig, l, u, a, b, x, N) - E["value"]) / R) for N in Ns]))
    return out


# ---------------------------------------------------------- products of simplices (task 4)
def random_blocks(rng):
    m = int(rng.integers(2, 4))
    C, X = [], []
    for _ in range(m):
        r = int(rng.integers(2, 5))
        c = rng.uniform(-1.5, 1.5, r)
        if rng.random() < 0.3:
            c[0] = 0.0  # a "none" option
        x = rng.dirichlet(np.ones(r))
        if r > 2 and rng.random() < 0.3:
            x[rng.integers(r)] = 0.0
            x /= x.sum()
        C.append(c)
        X.append(x)
    lo = sum(c.min() for c in C)
    hi = sum(c.max() for c in C)
    W, center = rng.uniform(0.5, 8.0), rng.uniform(-3.0, 3.0)
    C = [c * W / (hi - lo) for c in C]
    b = center - W * (lo + hi) / (2 * (hi - lo))
    return C, X, b


def simplex_points(rng, C, N):
    """N random points of the product of simplices (Dirichlet with small concentration mixes faces)."""
    return [[rng.dirichlet(np.full(len(c), alpha)) for c in C] for alpha in rng.choice([0.2, 1.0], N)]


def simplex_grid_upper(sig, C, b, X, total=30000):
    import gurobipy as gp
    from common import gurobi_model
    from gurobipy import GRB

    def comps(r, N):
        for bars in itertools.combinations(range(N + r - 1), r - 1):
            prev, out = -1, []
            for q in bars + (N + r - 1,):
                out.append(q - prev - 1)
                prev = q
            yield np.array(out) / N
    N = 1
    while True:
        cnt = np.prod([len(list(comps(len(c), N + 1))) for c in C])
        if cnt > total:
            break
        N += 1
    blocks = [list(comps(len(c), N)) for c in C]
    pts = list(itertools.product(*blocks))
    cflat = np.concatenate(C)
    L = np.array([np.concatenate(p) for p in pts])
    fz = sig(b + L @ cflat)
    xflat = np.concatenate(X)
    m = gurobi_model()
    lam = [m.addVar(lb=0.0) for _ in range(len(L))]
    for i in range(L.shape[1]):
        m.addConstr(gp.LinExpr(L[:, i].tolist(), lam) == float(xflat[i]))
    m.setObjective(gp.LinExpr(fz.tolist(), lam), GRB.MINIMIZE)
    m.optimize()
    return m.ObjVal, N


def simplex_job(args):
    name, side, seed = args
    sig = get_sigma(name, side)
    rng = np.random.default_rng(seed)
    recs = []
    for inst in range(10):
        C, X, b = random_blocks(rng)
        lo = b + sum(c.min() for c in C)
        hi = b + sum(c.max() for c in C)
        R, _ = f_range(sig, lo, hi)
        Em = envelope_simplices_merge(sig, C, b, X)
        Et = envelope_simplices_tailsum(sig, C, b, X)
        B = certified_bounds(sig, C, b, X)
        grid, N = simplex_grid_upper(sig, C, b, X) if inst < 3 else (None, None)
        P = simplex_points(rng, C, 20000)
        cflat = np.concatenate(C)
        Gf = np.concatenate(Et["G"])
        Lp = np.array([np.concatenate(p) for p in P])
        verts = np.array([np.concatenate([np.eye(len(c))[i] for c, i in zip(C, v)])
                          for v in itertools.product(*[range(len(c)) for c in C])])
        allp = np.vstack([Lp, verts])
        viol_sample = float(np.max(Et["c0"] + allp @ Gf - sig(b + allp @ cflat)))
        viol_exact = float(exact_cut_violation_simplices(sig, C, b, Et["c0"], Et["G"]))
        cut_at_x = float(Et["c0"] + np.concatenate(X) @ Gf)
        recs.append(dict(sigma=name, side=side, inst=inst, blocks=[len(c) for c in C], R=R,
                         merge_low=Em["low"], merge_up=Em["up"], tail_low=Et["value"], tail_up=Et["value_up"],
                         bf_low=B["low"], bf_up=B["up"], grid=grid, gridN=N, cut_at_x=cut_at_x,
                         viol_sample=viol_sample, viol_exact=viol_exact))
    return recs


def summarize_simplex(recs, tol=1e-7):
    print("\n=== Products of simplices: Corollary 3 vs certified brute force (values / R) ===")
    d1 = max(abs(r["merge_low"] - r["tail_low"]) / r["R"] for r in recs)
    d2 = max(abs(0.5 * (r["merge_low"] + r["merge_up"]) - 0.5 * (r["bf_low"] + r["bf_up"])) / r["R"] for r in recs)
    sep = max(max(r["merge_low"] - r["bf_up"], r["bf_low"] - r["merge_up"], 0) / r["R"] for r in recs)
    gap = max((r["bf_up"] - r["bf_low"]) / r["R"] for r in recs)
    gr = [r for r in recs if r["grid"] is not None]
    grd = max((r["merge_low"] - r["grid"]) / r["R"] for r in gr)
    grm = np.median([(r["grid"] - r["merge_low"]) / r["R"] for r in gr])
    vs = max(r["viol_sample"] / r["R"] for r in recs)
    ve = max(r["viol_exact"] / r["R"] for r in recs)
    tight = max(abs(r["cut_at_x"] - r["tail_low"]) / r["R"] for r in recs)
    print(f"cases: {len(recs)}; block sizes seen: {sorted(set(tuple(r['blocks']) for r in recs))[:6]} ...")
    print(f"max |merge - tailsum|/R = {d1:.2e}; max |merge - bf|/R = {d2:.2e}; max separation = {sep:.2e}; "
          f"max bf gap = {gap:.2e}")
    print(f"grid LP ({len(gr)} cases): max (thm - grid)/R = {grd:.2e} (must be <= 0); median grid excess = {grm:.2e}")
    print(f"tail-sum cut: max violation/R sample+vertices = {vs:.2e}, exact 1-D = {ve:.2e}; max |h(x)-value|/R = {tight:.2e}")
    flagged = [r for r in recs if max(r["merge_low"] - r["bf_up"], r["bf_low"] - r["merge_up"], 0) / r["R"] > tol
               or r["viol_exact"] / r["R"] > tol]
    print("flagged:", len(flagged))
    for r in flagged[:10]:
        print("  ", r)


# -------------------------------------------------------------- strength gain (task 5)
def gain_job(args):
    name, side, seed = args
    sig = get_sigma(name, side)
    rng = np.random.default_rng(seed)
    recs = []
    for n in (2, 3, 5):
        for inst in range(4):
            l, u, a, b = random_box(rng, n)
            lo = b + np.sum(np.minimum(a * l, a * u))
            hi = b + np.sum(np.maximum(a * l, a * u))
            R, _ = f_range(sig, lo, hi)
            hs, hv = vex_interval_hull(sig, lo, hi)

            def gain(x):
                x = np.clip(x, l, u)
                return (envelope_box(sig, l, u, a, b, x, ngrid=201)["value"] - float(np.interp(a @ x + b, hs, hv))) / R

            X = rng.uniform(l, u, size=(150, n))
            G = np.array([gain(x) for x in X])
            # pattern search from the 3 best random points
            best = -np.inf
            for i0 in np.argsort(-G)[:3]:
                x, gx, step = X[i0].copy(), G[i0], 0.25 * (u - l)
                while np.max(step / (u - l)) > 1e-3:
                    moved = False
                    for i in range(n):
                        for sgn in (1, -1):
                            y = x.copy()
                            y[i] = np.clip(y[i] + sgn * step[i], l[i], u[i])
                            gy = gain(y)
                            if gy > gx:
                                x, gx, moved = y, gy, True
                    if not moved:
                        step = step / 2
                best = max(best, gx)
            recs.append(dict(sigma=name, side=side, n=n, inst=inst, mean=float(G.mean()),
                             maxrand=float(G.max()), worst=float(best), minrand=float(G.min())))
    return recs


def summarize_gain(recs):
    print("\n=== Strength gain: (vex_B f - vex_I sigma)(x) / range(f) ; cave side uses -sigma ===")
    print(f"{'sigma':16s}{'side':5s}{'mean':>9s}{'max-mean-inst':>15s}{'worst pt':>10s}{'min(>=0?)':>11s}")
    for (name, side) in functions():
        rs = [r for r in recs if r["sigma"] == name and r["side"] == side]
        if not rs:
            continue
        print(f"{name:16s}{side:5s}{np.mean([r['mean'] for r in rs]):9.4f}{max(r['mean'] for r in rs):15.4f}"
              f"{max(r['worst'] for r in rs):10.4f}{min(r['minrand'] for r in rs):11.1e}")
    for n in (2, 3, 5):
        rn = [r for r in recs if r["n"] == n]
        print(f"n={n}: mean gain {np.mean([r['mean'] for r in rn]):.4f}, max worst-point gain {max(r['worst'] for r in rn):.4f}")


# ------------------------------------------------ S-shape structure claim (theory.md)
def sshape_job(args):
    name, seed = args
    sig = SIGMAS[name]
    rng = np.random.default_rng(seed)
    recs = []
    for n in (2, 3, 4, 5):
        for _ in range(25):
            l, u, a, b = random_box(rng, n)
            x = random_point(rng, l, u, a, "interior")
            nd = normalize(l, u, a, b)
            xn = nd["sgn"] * (x[nd["keep"]] - nd["base"]) / nd["w"]
            _, t, p = __import__("ridge_envelope").staircase(xn, nd["an"])
            sg = lambda s: sig(np.asarray(s, float) + nd["b0"])
            full = solve_D(t, p, sg)
            best = -np.inf
            for ks in range(-1, len(t)):
                r = solve_D(t, p, sg, kstar=ks)
                if r is not None:
                    best = max(best, r["low"])
            recs.append(dict(sigma=name, n=n, full=full["low"], full_up=full["up"], structured=best))
    return recs


def summarize_sshape(recs):
    print("\n=== S-shape structure claim: (D) optimum vs best 'sigma on right nodes + one line on left' ===")
    for name in sorted(set(r["sigma"] for r in recs)):
        rs = [r for r in recs if r["sigma"] == name]
        d = [(r["full_up"] - r["structured"]) for r in rs]
        print(f"{name}: {len(rs)} cases, max (D - structured) = {max(d):.2e}, cases > 1e-7: {sum(v > 1e-7 for v in d)}")


def run(job, tasks, tag):
    t0 = time.time()
    with mp.get_context("fork").Pool(min(32, len(tasks))) as pool:
        res = pool.map(job, tasks, chunksize=1)
    recs = [r for rs in res for r in rs]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{tag}.json"), "w") as fh:
        json.dump(recs, fh)
    print(f"[{tag}] {len(recs)} records in {time.time() - t0:.0f}s")
    return recs


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    fs = functions()
    if what in ("box", "all"):
        summarize_box(run(box_job, [(nm, sd, 1000 + i) for i, (nm, sd) in enumerate(fs)], "box"))
    if what in ("grid", "all"):
        out = run(grid_job, [(nm, 2000 + i) for i, nm in enumerate(SIGMAS)], "grid")
        print("\n=== Grid-LP upper bound minus Theorem 1, divided by R (must be >= 0 and shrink) ===")
        for r in out:
            print(f"{r['sigma']:16s} n={r['n']}: " + "  ".join(f"N={N}:{g:.1e}" for N, g in r["gaps"]))
    if what in ("simplex", "all"):
        summarize_simplex(run(simplex_job, [(nm, sd, 3000 + i) for i, (nm, sd) in enumerate(fs)], "simplex"))
    if what in ("gain", "all"):
        summarize_gain(run(gain_job, [(nm, sd, 4000 + i) for i, (nm, sd) in enumerate(fs)], "gain"))
    if what in ("sshape", "all"):
        summarize_sshape(run(sshape_job, [("sigmoid", 5000), ("tanh", 5001)], "sshape"))


if __name__ == "__main__":
    main()
