"""Per-edge refinement with the original bands is not enough on paths.

Instances of type D (run_paths.py): tight coupling kappa = 10, flat valley
[-0.3, 0.3], tilt +-0.3 sin(3 s) at the two ends, concave kinks.  For each
n and eps, cells are refined edge by edge until the one-edge band bracket
for [L_e, U_e] is <= tol (rule naive with tol = eps/n, and with tol = eps/n^2),
or until the Theorem 1 sliver bracket is <= eps/n (rule bd).  For each cell
set, the LP optimum gap(PA) over ALL cellwise-affine splits on those cells
is computed (HiGHS).  Rule B.4: Proposition B.4 of extension-adaptive.md
edge by edge with tolerance eps/n (split while M r^2 - min_D w_e > eps/n).
Each rule makes every one-edge problem accurate to its tolerance; only bd
carries a guarantee for the path.

usage: python3 check_naive_failure.py [m ...]
"""
import sys
import numpy as np
from path_cells import (PathFast, path_unaries, tree_from_unaries,
                        cell_bracket, refine, lp_gap)
from run_paths import edge_data, KINKS6


def cells_for(s, E, n, tol, kind, M=None):
    out = {}
    for e in range(1, n + 1):
        d = E[e]
        if kind == "pb4":
            def test(i0, i1, lev, w=d["w"]):
                r = (s[i1] - s[i0]) / 2
                return M * r ** 2 - w[i0:i1 + 1].min() > tol
            out[e], _ = refine(s, test)
            continue
        up, lo = (d["U"], d["L"]) if kind == "band" else (d["up"], d["lo"])

        def test(i0, i1, lev, up=up, lo=lo):
            g, _, _ = cell_bracket(s[i0:i1 + 1], up[i0:i1 + 1], lo[i0:i1 + 1])
            return g > tol
        out[e], _ = refine(s, test)
    return out


def main():
    ms = [int(a) for a in sys.argv[1:]] or [129, 257]
    kappa, A, v, tilt = 10.0, 1.0, 0.3, (0.3, 3.0)
    M = 2 * kappa + 2 * A + tilt[0] * tilt[1] ** 2
    fails = 0
    for m in ms:
        s = np.linspace(-1, 1, m)
        for n in [2, 3, 4, 6, 8]:
            kinks = {k: val for k, val in KINKS6.items() if k <= n}
            un = path_unaries(n, s, A, v, kinks, tilt)
            path = PathFast(s, kappa, un)
            tree = tree_from_unaries(s, kappa, un)
            E, fstar = edge_data(path)
            for eps in [1e-2, 1e-3]:
                row = f"m={m:4d} n={n} eps={eps:g}:"
                for name, tol, kind in [("naive", eps / n, "band"),
                                        ("naive/n", eps / n ** 2, "band"),
                                        ("B.4", eps / n, "pb4"),
                                        ("bd", eps / n, "sliver")]:
                    cells = cells_for(s, E, n, tol, kind, M)
                    g = lp_gap(s, tree, cells, fstar)
                    tot = sum(len(c) for c in cells.values())
                    mark = " >eps" if g > eps * (1 + 1e-9) else ""
                    if name == "bd" and g > eps * (1 + 1e-9):
                        fails += 1
                    row += f"  {name}: {tot:3d} cells, gap(PA) {g:.2e}{mark};"
                print(row)
                sys.stdout.flush()
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
