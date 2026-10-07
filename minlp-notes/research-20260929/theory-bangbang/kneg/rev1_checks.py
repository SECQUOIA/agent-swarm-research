"""Targeted checks for the revision of kappa-negative.md after review round 1.

usage: OMP_NUM_THREADS=1 python3 rev1_checks.py PART [PART ...]    PART in: spectraG convexity qneg epscover cascade
  spectraG   (F5.1)  toy plus, kappa = -0.5: lambda_min(G) / h^2 against h / 4, G = H - h^2 diag(kappa_t)
                     (Hessian of Jt), 40-digit eigenvalues (mpmath) at N = 10, 40, 100; float at N = 800.
  convexity  (F3)    two-switch toys of Sections 9.1 and 9.3 (exact jump times): float eigenvalues of the
                     reduced Hessian H of J at N = 1000 (smallest / h^2, number of negative ones).
  qneg       (F5.5)  q < 0 toy (k = 3, Phi = x - x^2) and kappa = -1 toy: exact vertex margins |sigma_t| / h
                     below Delta |kappa| / 2 at N = 200, 400, and the exact bound of the outer node
                     {u_n in [r, 1]} at N = 2000 for both toys (r = right end of the lifted interval).
  epscover   (F5.6)  the two exactly re-checked epsilon-partitions (N = 1000, kappa = -0.5): do the
                     rationalized node ends cover [-1, 1] without gaps?
  cascade    (7.2)   kappa 1 -> 0 close-switch toys: lifting cascade of the maximal-recursion break (float).
Each part prints JSON lines and writes logs/rev1_<part>.json.
"""
import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ktoy import KToy, kkt, best_bang, exact_kkt, hess, fam_const  # noqa: E402
from lifted import node_kkt, fixed_bound, lifted_interval, greedy_partition  # noqa: E402

LOG = os.path.join(HERE, "logs")


def out(name, recs):
    for r in recs:
        print(json.dumps(r, default=float), flush=True)
    with open(os.path.join(LOG, f"rev1_{name}.json"), "w") as f:
        json.dump(recs, f, indent=1, default=float)


def part_spectraG():
    import mpmath as mp
    mp.mp.dps = 40
    recs = []
    for N in (10, 40, 100):
        h = mp.mpf(2) / N
        G = mp.matrix(N, N)
        for i in range(N):
            for j in range(N):
                G[i, j] = h * (N - 1 - max(i, j)) + mp.mpf(1) / 2      # G / h^2 (toy plus: phi2 = 0, k = 1/2)
        ev = mp.eigsy(G, eigvals_only=True)
        lam = min(ev)
        recs.append(dict(N=N, digits=40, lam_min_G_over_h2=mp.nstr(lam, 15), h_over_4=mp.nstr(h / 4, 15),
                         relative_excess=mp.nstr(lam / (h / 4) - 1, 6)))
    N = 800
    h = 2.0 / N
    idx = np.arange(N)
    G = h * (N - 1 - np.maximum.outer(idx, idx)) + 0.5
    lam = np.linalg.eigvalsh(G)[0]
    recs.append(dict(N=N, digits="float", lam_min_G_over_h2=lam, h_over_4=h / 4, relative_excess=lam / (h / 4) - 1))
    out("spectraG", recs)


def _two_toys():
    from run_multi import toy2, structure, CASES
    toys = []
    for (k, t1, t2) in CASES:
        toys.append(("9.1", dict(kappa=-k, t1=t1, t2=t2), toy2(((0.0, k),), t1, t2)))
    pairs = ((-0.5, 0.0), (0.0, -0.5), (-0.5, -0.3), (-0.3, -0.5), (-1.0, 0.0), (0.0, -1.0))
    for (k1, k2) in pairs:
        cfgs = ((0.5, 1.5), (0.55, 1.45), (0.45, 1.55)) if -1.0 in (k1, k2) else ((0.5, 1.5), (0.6, 1.4), (0.65, 1.35))
        for (t1, t2) in cfgs:
            base = toy2(((0.0, k1),), t1, t2)
            sw0 = structure(base)
            if len(sw0) != 2:
                continue
            tk = round((sw0[0] + sw0[1]) / 2 * 64) / 64
            toys.append(("9.3", dict(kappa1=-k1, kappa2=-k2, t1=t1, t2=t2, tk=tk), toy2(((0.0, k1), (tk, k2)), t1, t2)))
    return toys


def part_convexity():
    recs = []
    N = 1000
    for sec, desc, toy in _two_toys():
        h = toy.T / N
        H = hess(toy, N, list(range(N)))
        ev = np.linalg.eigvalsh(H)
        tol = 1e-12 * np.abs(ev).max()
        recs.append(dict(section=sec, **desc, N=N, lam_min_over_h2=ev[0] / h ** 2, lam_2_over_h2=ev[1] / h ** 2,
                         n_negative=int(np.sum(ev < -tol))))
    out("convexity", recs)


def part_qneg():
    recs = []
    qtoy = KToy(a_pts=((0.0, 2.0), (1.0, -1.0)), k_pts=((0.0, 3.0),), phi1=1.0, phi2=-2.0, R=3.0)
    ktoy1 = KToy(a_pts=((0.0, 2.0), (1.0, -1.0)), k_pts=((0.0, 1.0),), phi1=1.0, phi2=0.0, R=3.0)
    for name, toy, kap in (("q<0 (k=3)", qtoy, 3), ("kappa=-1 (k=1)", ktoy1, 1)):
        sw = best_bang(toy, 200, 1)
        for N in (200, 400):
            Z = exact_kkt(toy, kkt(toy, N, sw))
            h = Z["h"]
            small = sorted((abs(Z["sig"][t]) / h, t) for t in range(N) if t not in Z["frac"])
            small = [(t, float(m)) for (m, t) in small if m < kap]           # Delta |kappa| / 2 = kap
            recs.append(dict(toy=name, N=N, frac=Z["frac"], small_margin_vertex_stages=small, threshold=kap))
        N = 2000
        Z = exact_kkt(toy, kkt(toy, N, sw))
        h = Z["h"]
        n = min(range(N), key=lambda s: abs(Z["sig"][s]))
        P = fam_const(N, Fr(-kap))
        Z["lo"], Z["hi"] = [Fr(-1)] * N, [Fr(1)] * N
        V = lifted_interval(toy, Z, P, n)
        r = V[1] if V[1] < 1 else V[0]
        l, rr = (r, Fr(1)) if V[1] < 1 else (Fr(-1), r)
        A = node_kkt(toy, N, [float(v) for v in Z["u"]], n, l, rr)
        B, worst = fixed_bound(toy, A, P, n)
        recs.append(dict(toy=name, N=N, n=n, V=[float(V[0]), float(V[1])], outer_node=[float(l), float(rr)],
                         outer_anchor_u_n=float(A["u"][n]), outer_anchor_minus_J_over_h2=float((A["J"] - Z["J"]) / h ** 2),
                         outer_bound_minus_J_over_h2=float((B - Z["J"]) / h ** 2), outer_losses=len(worst)))
    out("qneg", recs)


def part_epscover():
    from run_kneg import plus
    toy = plus(0.5)
    N = 1000
    kk = kkt(toy, N, best_bang(toy, 200, 1))
    n = kk["frac"][0]
    h = toy.T / N
    recs = []
    for er in (1e-4, 1e-8):
        nodes = greedy_partition(toy, N, kk["u"], n, kk["J"], er * h * h, 0.5, h * h, safety=0.9)
        ends = sorted((Fr(a).limit_denominator(10 ** 12), Fr(b).limit_denominator(10 ** 12)) for (a, b, _) in nodes)
        gaps = [float(ends[i + 1][0] - ends[i][1]) for i in range(len(ends) - 1) if ends[i + 1][0] > ends[i][1]]
        recs.append(dict(N=N, eps_over_h2=er, n_nodes=len(nodes), first=float(ends[0][0]), last=float(ends[-1][1]),
                         n_gaps=len(gaps), max_gap=max(gaps) if gaps else 0.0))
    out("epscover", recs)


def part_cascade():
    """Section 7.2 lifting cascade (float), logged: kappa 1 -> 0 configurations; when the maximal
    recursion breaks at stage t_b, treat u_{t_b} as a parameter (no control: P_t = h + P_{t+1}) and rerun;
    six iterations.  Reports the break stages relative to the first switching stage s1."""
    from run_multi import toy2, structure
    from ktoy import fam_rmax, float_data
    recs = []
    for (t1, t2) in ((0.5, 1.5), (0.55, 1.45), (0.45, 1.55)):
        base = toy2(((0.0, -1.0),), t1, t2)
        sw0 = structure(base)
        tk = round((sw0[0] + sw0[1]) / 2 * 64) / 64
        toy = toy2(((0.0, -1.0), (tk, 0.0)), t1, t2)
        sw = structure(toy)
        for N in (1000, 2000, 4000, 8000):
            kk = kkt(toy, N, sw)
            D = float_data(toy, kk)
            s1 = [t for t in range(1, N) if kk["u"][t] != kk["u"][t - 1]][0]
            fixed, breaks = [], []
            for _ in range(7):
                _, br = fam_rmax(toy, D, eps=0.0, fixed_stages=set(fixed))
                breaks.append(None if br is None else br - s1)
                if br is None:
                    break
                fixed.append(br)
            recs.append(dict(t1=t1, t2=t2, tk=tk, N=N, s1=s1, frac=kk["frac"], breaks_minus_s1=breaks))
    out("cascade", recs)


if __name__ == "__main__":
    for part in sys.argv[1:]:
        dict(spectraG=part_spectraG, convexity=part_convexity, qneg=part_qneg, epscover=part_epscover,
             cascade=part_cascade)[part]()
