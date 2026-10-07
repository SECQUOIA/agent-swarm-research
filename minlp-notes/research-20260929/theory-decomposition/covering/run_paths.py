"""Theorem 3 on grid path instances: cell counts of four refinement rules,
gaps, and covering numbers.

Rules (per edge e, dyadic cells, tolerance eps/n per edge):
  thm   : the explicit rule of Theorem 3 (interior / near-boundary bounds);
  bd    : refine while the Theorem 1 cell bracket for the sliver
          [psi_e - w_e/2n, psi_e + w_e/2n] exceeds eps/n;
  naive : refine while the one-edge band bracket for [L_e, U_e] exceeds
          eps/n (Proposition B.4 applied edge by edge with original bands);
  sup   : refine while 2 x the sup-norm error of the best affine
          approximation of U_e on the cell exceeds eps/n (the upper end of
          Theorem 3.1 of the consistency note with the DP split).
For each rule: cells per edge, max cell bracket, and the gap of the explicit
split built from the cell brackets (direct evaluation on the fine grid).
On a coarse grid (same instance) the LP optimum gap(PA) over all PA splits
on the cells of the rules bd and naive.  Floating point; exact minima over
finite grids; G is a grid estimate of the Lipschitz constant.

usage: python3 run_paths.py [fine_m] [coarse_m]
"""
import sys
import time
import numpy as np
from path_cells import (PathFast, path_unaries, tree_from_unaries,
                        cell_bracket, refine, pa_from_brackets, lp_gap,
                        sup_cover)
from tree_lib import graded_split

KINKS3 = {0: [(0.65, 0.5, 1)], 1: [(-0.7, 0.5, -1)], 2: [(0.6, 0.5, 1)]}
KINKS6 = {0: [(0.65, 0.5, 1)], 1: [(-0.7, 0.5, -1)], 2: [(0.6, 0.5, 1)],
          4: [(-0.8, 0.5, -1)], 5: [(0.75, 0.5, 1)]}
CONFIGS = [
    # name, n, kappa, A, v, tilt, kinks, centers
    ("D1 flat valley, tilt, kinks", 3, 10.0, 1.0, 0.3, (0.3, 3.0), KINKS3,
     (0.0,)),
    ("D2 same, n = 6", 6, 10.0, 1.0, 0.3, (0.3, 3.0), KINKS6, (0.0,)),
    ("D3 two flat valleys", 3, 10.0, 1.0, 0.15, (0.3, 3.0), KINKS3,
     (-0.4, 0.4)),
    ("D4 QG (v = 0)", 3, 10.0, 1.0, 0.0, (0.3, 3.0), KINKS3, (0.0,)),
]


def edge_data(path):
    U, V, fstar = path.value_functions()
    n = path.n_edges
    E = {}
    for e in range(1, n + 1):
        L = fstar - V[e]
        w = U[e] - L
        th = 1 - (2 * e - 1) / (2 * n)
        psi = (1 - th) * U[e] + th * L
        E[e] = dict(U=U[e], L=L, w=w, psi=psi,
                    up=psi + w / (2 * n), lo=psi - w / (2 * n))
    return E, fstar


def make_test(rule, s, d, n, eps, M, G):
    if rule == "thm":
        def test(i0, i1, lev):
            r = (s[i1] - s[i0]) / 2
            wmin = d["w"][i0:i1 + 1].min()
            interior = (s[i0] + 1 >= 8 * n * r) and (1 - s[i1] >= 8 * n * r)
            if interior:
                B = (32 * n + 0.5) * M * r ** 2 - wmin / (2 * n)
            else:
                B = 2 * G * r + 2.5 * M * r ** 2 - wmin / n
            return B > eps / n
        return test, d["up"], d["lo"]
    up, lo = {"bd": (d["up"], d["lo"]), "naive": (d["U"], d["L"]),
              "sup": (d["U"], d["U"])}[rule]

    def test(i0, i1, lev):
        g, _, _ = cell_bracket(s[i0:i1 + 1], up[i0:i1 + 1], lo[i0:i1 + 1])
        return g > eps / n
    return test, up, lo


def run_rule(rule, s, path, E, fstar, eps, M, G):
    n = path.n_edges
    t0 = time.time()
    cells, phis, gmax, lim = {}, [None], 0.0, False
    for e in range(1, n + 1):
        test, up, lo = make_test(rule, s, E[e], n, eps, M, G)
        c, l = refine(s, test)
        lim = lim or l
        phi, gs = pa_from_brackets(s, c, up, lo)
        cells[e] = c
        phis.append(phi)
        gmax = max(gmax, gs.max())
    gap_phi = fstar - path.rho(phis)
    return dict(cells=cells, counts=[len(cells[e]) for e in range(1, n + 1)],
                gmax=gmax, gap_phi=gap_phi, lim=lim, time=time.time() - t0)


def main():
    fine_m = int(sys.argv[1]) if len(sys.argv) > 1 else 16385
    coarse_m = int(sys.argv[2]) if len(sys.argv) > 2 else 257
    print(f"grids on [-1,1]: fine m = {fine_m}, coarse m = {coarse_m}")
    for (name, n, kappa, A, v, tilt, kinks, centers) in CONFIGS:
        H = tilt[0] * tilt[1] ** 2
        M = 2 * kappa + 2 * A + H
        print("=" * 78)
        print(f"{name}: n = {n} edges, kappa = {kappa}, A = {A}, v = {v}, "
              f"centers = {centers}, tilt = {tilt}, M = {M:.2f}")
        for eps in [1e-2, 1e-3]:
            s = np.linspace(-1, 1, fine_m)
            un = path_unaries(n, s, A, v, kinks, tilt, centers)
            path = PathFast(s, kappa, un)
            E, fstar = edge_data(path)
            ds = s[1] - s[0]
            G = max(max(np.max(np.abs(np.diff(E[e]["U"]))),
                        np.max(np.abs(np.diff(E[e]["L"])))) / ds for e in E)
            emp = max(max(np.max(np.diff(E[e]["U"], 2)),
                          np.max(-np.diff(E[e]["L"], 2))) / ds ** 2 for e in E)
            covs = [sup_cover(s, E[e]["w"], eps, M) for e in E]
            Jint = max(0, int(np.ceil(np.log2(2 * np.sqrt(
                (64 * n * n + n) * M / (8 * eps))))))
            print(f"-- eps = {eps:g}: f* = {fstar:.6f}, G ~ {G:.2f}, grid "
                  f"max(U'', -L'') = {emp:.2f} (<= M), J_int = {Jint}")
            print(f"   covering sup_eta N(pi_e E(eta), 2 sqrt((eps+eta)/M)) "
                  f"per edge: {covs}")
            res = {}
            for rule in ["thm", "bd", "naive", "sup"]:
                rr = run_rule(rule, s, path, E, fstar, eps, M, G)
                res[rule] = rr
                flag = "  [grid-limited]" if rr["lim"] else ""
                print(f"   {rule:5s}: cells/edge {rr['counts']} (total "
                      f"{sum(rr['counts'])}), max bracket {rr['gmax']:.2e} "
                      f"(eps/n {eps / n:.2e}), gap(phi) {rr['gap_phi']:.3e}"
                      f"{flag} ({rr['time']:.0f}s)")
                if rule in ("thm", "bd"):
                    q = [c / cv for c, cv in zip(rr["counts"], covs)]
                    print(f"          cells/cover per edge "
                          f"{np.round(q, 2).tolist()}; "
                          f"total/(n J_int sum cover) = "
                          f"{sum(rr['counts']) / (n * Jint * sum(covs)):.3f}")
                sys.stdout.flush()
            # LP optimum on the coarse grid, cells of rules bd and naive
            # rebuilt on the coarse grid
            sc = np.linspace(-1, 1, coarse_m)
            unc = path_unaries(n, sc, A, v, kinks, tilt, centers)
            tree = tree_from_unaries(sc, kappa, unc)
            pc = PathFast(sc, kappa, unc)
            Ec, fc = edge_data(pc)
            line = f"   coarse m = {coarse_m}:"
            for rule in ["bd", "naive"]:
                rr = run_rule(rule, sc, pc, Ec, fc, eps, M, G)
                glp = lp_gap(sc, tree, rr["cells"], fc)
                line += (f" {rule}: cells {sum(rr['counts'])}, gap(phi) "
                         f"{rr['gap_phi']:.2e}, LP gap(PA) {glp:.2e};")
            print(line)
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
