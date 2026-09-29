"""T2: Corollaries B and C (aperture bounds) on random layered DAGs of balls.

(a) Euclidean lengths: OPT <= E[round] <= sum_e kappa_e * ltilde_e <= kappa_max * REL_H,
    kappa_e = sec(theta_e), sin(theta_e) = (r_u + r_v)/|c_v - c_u|.
(b) Squared lengths: same chain with kappa^sq_e = sec^2(theta_e) (exact for balls);
    also reports the weaker product bound sec^2 * (M+m)^2/(4Mm) = sec^4 for balls.
(c) l1 lengths with sign-monotone boxes: REL_H = OPT (kappa = 1).
Usage: python3 t2_kappa.py [seed] [n]
"""
import sys
import numpy as np
from gcslib import *

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30


def layered_balls(d, L, k, D, spread, rmax, skip):
    sets = {"s": point(np.zeros(d))}
    layers = []
    for i in range(1, L + 1):
        lay = []
        for j in range(k):
            c = np.r_[i * D, rng.uniform(-spread, spread, d - 1)]
            sets[f"{i}_{j}"] = ball(c, rng.uniform(0.2, 1.0) * rmax)
            lay.append(f"{i}_{j}")
        layers.append(lay)
    sets["t"] = point(np.r_[(L + 1) * D, rng.uniform(-spread, spread, d - 1)])
    E = [("s", v) for v in layers[0]] + [(v, "t") for v in layers[-1]]
    for a, b in zip(layers, layers[1:]):
        E += [(u, v) for u in a for v in b]
    for a, b in zip(layers, layers[2:]):
        E += [(u, v) for u in a for v in b if rng.random() < skip]
    return sets, E


def check(norm, n):
    viol, rows = 0, []
    cnt = 0
    while cnt < n:
        d = int(rng.choice([2, 3]))
        sets, E = layered_balls(d, int(rng.integers(2, 4)), int(rng.integers(2, 4)), 3.0,
                                float(rng.choice([0.5, 1.0, 2.0])), float(rng.choice([0.6, 1.0, 1.4])), 0.3)
        kap = {e: (kappa_l2 if norm == "l2" else kappa_sq)(sets[e[0]], sets[e[1]]) for e in E}
        if not all(np.isfinite(list(kap.values()))):
            continue
        cnt += 1
        g = GCS(sets, E, "s", "t", L2 if norm == "l2" else SQ)
        r = relax(g)
        rh, sol = relax(g, hull=True, return_sol=True)
        o = opt(g)
        Er = expected_round(g, sol)
        y = sol["y"]
        kb = sum(kap[e] * y[e] * g.cost[e].val(sol["z"][e] / y[e], sol["zp"][e] / y[e]) for e in E if y[e] > 1e-7)
        km = max(kap.values())
        chain = [rh, o, Er, kb, km * rh]
        ok = all(chain[i] <= chain[i + 1] + 1e-5 * max(1, abs(chain[i + 1])) for i in range(len(chain) - 1))
        viol += not ok
        rows.append((o / r, o / rh, km))
        extra = ""
        if norm == "sq":
            extra = f" sec^4 bound={km**2:.4f}"
        print(f"{norm} d={d} |E|={len(E):3d} kmax={km:.4f} OPT/REL={o/r:.5f} OPT/REL_H={o/rh:.5f} "
              f"E/REL_H={Er/rh:.5f} sum(k*l)/REL_H={kb/rh:.5f}{extra} {'' if ok else 'VIOLATION'}", flush=True)
    rows = np.array(rows)
    ex = (rows[:, 1] - 1) / (rows[:, 2] - 1)
    print(f"[{norm}] n={len(rows)} violations={viol} max OPT/REL_H={rows[:,1].max():.5f} "
          f"max (OPT/REL_H-1)/(kmax-1)={ex.max():.4f} #gap(REL_H)>1e-5: {np.sum(rows[:,1]>1+1e-5)} "
          f"#gap(REL)>1e-5: {np.sum(rows[:,0]>1+1e-5)}")


def l1_monotone(n):
    """boxes placed so that every edge displacement set lies in the closed positive orthant."""
    bad = 0
    for trial in range(n):
        d = int(rng.choice([2, 3]))
        L, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        sets = {"s": point(np.zeros(d))}
        layers = []
        for i in range(1, L + 1):
            lay = []
            for j in range(k):
                lo = np.full(d, 2.0 * i) + rng.uniform(0, 0.3, d)
                hi = lo + rng.uniform(0.1, 1.5, d)
                sets[f"{i}_{j}"] = box(lo, hi)
                lay.append(f"{i}_{j}")
            layers.append(lay)
        sets["t"] = point(np.full(d, 2.0 * (L + 1)))
        E = [("s", v) for v in layers[0]] + [(v, "t") for v in layers[-1]]
        for a, b in zip(layers, layers[1:]):
            E += [(u, v) for u in a for v in b]
        g = GCS(sets, E, "s", "t", L1)
        rh = relax(g, hull=True)
        o = opt(g)
        bad += abs(o - rh) > 1e-5 * max(1, abs(o))
    print(f"[l1 sign-monotone boxes] n={n} #(|OPT-REL_H|>1e-5)={bad}")


check("l2", N)
check("sq", N)
l1_monotone(max(10, N // 2))
