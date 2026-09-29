"""Guillotine overhead on candidate grids: exact guillotine optimum (DP) versus exact
unrestricted optimum (MILP), both with boxes on the same grid.
With the optional argument "knots", the grid also contains the kinks (knots of the
separable components; triple-point coordinates of polyhedral instances).
Usage: python3 overhead_search.py NSEP NPOLY SEED [knots]"""
import sys
import ctypes
import numpy as np
from nd_sep import Ftable, TOL, _lib
from search_sep2d import build, rand_params
from poly2d import Poly2, valid_table, opt_ilp


def dp(V):
    out = ctypes.c_int(0)
    _lib.guillotine_dp(V.shape[0], V.shape[2], np.ascontiguousarray(V).ctypes.data, ctypes.byref(out))
    return out.value


if __name__ == "__main__":
    nsep, npoly, seed = map(int, sys.argv[1:4])
    KNOTS = len(sys.argv) > 4 and sys.argv[4] == "knots"
    rng = np.random.default_rng(seed)
    best = (1.0, None)
    hist = {}
    for t in range(nsep + npoly):
        G = int(rng.integers(8, 13))
        g = np.linspace(0, 1, G)
        if t < nsep:
            Is = build(rand_params(rng, int(rng.integers(3, 8))), 10 ** rng.uniform(-6, -2))
            if KNOTS:
                g1 = np.array(sorted(set(g) | set(float(x) for x in Is[0].x)))
                g2 = np.array(sorted(set(g) | set(float(x) for x in Is[1].x)))
            else:
                g1 = g2 = g
            F1, F2 = Ftable(Is[0], g1), Ftable(Is[1], g2)
            V = (F1[:, :, None, None] + F2[None, None, :, :] >= -TOL).astype(np.uint8)
            kind = "sep"
        else:
            K = int(rng.integers(4, 9))
            P = rng.uniform(0, 1, (K, 2)); mu = np.exp(rng.uniform(np.log(1e-3), np.log(0.3), K))
            inst = Poly2(2 * P, -(P ** 2).sum(1) + mu, 10 ** rng.uniform(-5, -2))
            if KNOTS:
                T = inst.tri[(inst.tri >= 0).all(1) & (inst.tri <= 1).all(1)]
                g1 = np.array(sorted(set(g) | set(T[:, 0].tolist())))
                g2 = np.array(sorted(set(g) | set(T[:, 1].tolist())))
                if len(g1) > 22 or len(g2) > 22:
                    continue
            else:
                g1 = g2 = g
            V = valid_table(inst, g1, g2)
            kind = "poly"
        ng = dp(V)
        if ng <= 0:
            continue
        no, st = opt_ilp(V, time_limit=60)
        if no is None or st != 0:
            continue
        r = ng / no
        hist[(ng - no)] = hist.get(ng - no, 0) + 1
        if r > best[0]:
            best = (r, (kind, t, G, ng, no))
            print("new best overhead", best, flush=True)
    print("histogram of N_guill_grid - N_grid_opt:", sorted(hist.items()))
    print("BEST", best)
