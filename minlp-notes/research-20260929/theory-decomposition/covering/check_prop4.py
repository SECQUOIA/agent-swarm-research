"""Proposition 4: each band contains the constant 0, yet gap(Aff) = beta.

Path with two edges: root 2 beta s1^2, middle kappa (s1 - s2)^2 - beta s2^2,
leaf 2 beta s2^2 on [-1, 1]^2 (kappa >= 2 beta).  Checks on a grid:
  - U_e >= 0 >= L_e on both edges (0 lies in both bands);
  - LP gap of the affine class (one cell per edge) and of the constants;
  - per-edge refinement with original bands stops at one cell per edge for
    every tolerance, so its gap stays beta;
  - the rule of Proposition B.4 applied edge by edge with tolerance eps/n
    (split while M r^2 - min w_e > eps/n) and its LP gap(PA);
  - the Theorem 1 rule (sliver brackets, eps/n) and its LP gap(PA), and the
    number of cells as eps decreases (quadratic growth: O(log(1/eps))).
Floating point, HiGHS.
"""
import numpy as np
from path_cells import (PathFast, tree_from_unaries, cell_bracket, refine,
                        lp_gap)
from run_paths import edge_data


def main():
    m = 257
    s = np.linspace(-1, 1, m)
    ok = True
    for beta, kappa in [(1.0, 10.0), (1.0, 2.0), (0.1, 10.0)]:
        # PathFast convention: middle table kappa (s1 - s2)^2 + u_1(s2)
        un = [2 * beta * s ** 2, -beta * s ** 2, 2 * beta * s ** 2]
        path = PathFast(s, kappa, un)
        tree = tree_from_unaries(s, kappa, un)
        E, fstar = edge_data(path)
        n = 2
        inband = min(min(E[e]["U"].min(), -E[e]["L"].max()) for e in E)
        one = {e: [(0, m - 1)] for e in (1, 2)}
        gap_aff = lp_gap(s, tree, one, fstar)
        # constants: gap with phi = 0
        gap0 = fstar - path.rho([None, np.zeros(m), np.zeros(m)])
        print(f"beta={beta}, kappa={kappa}: f*={fstar:.3e}, "
              f"min over edges of min(U_e, -L_e) = {inband:.3e} (>= 0: 0 in "
              f"both bands); gap(Aff) = {gap_aff:.6f}, gap(phi=0) = {gap0:.6f}")
        ok = ok and inband >= -1e-12 and abs(gap_aff - beta) < 1e-6
        for tol in [1e-2, 1e-4, 1e-6]:
            cells = {}
            for e in (1, 2):
                U, L = E[e]["U"], E[e]["L"]

                def test(i0, i1, lev, U=U, L=L):
                    g, _, _ = cell_bracket(s[i0:i1 + 1], U[i0:i1 + 1],
                                           L[i0:i1 + 1])
                    return g > tol
                cells[e], _ = refine(s, test)
            g = lp_gap(s, tree, cells, fstar)
            print(f"   per-edge band rule, tol {tol:g}: cells "
                  f"{[len(cells[e]) for e in (1, 2)]}, LP gap(PA) = {g:.6f}")
        M = max(2 * kappa, 4 * beta)
        for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
            cells = {}
            for e in (1, 2):
                w = E[e]["w"]

                def test(i0, i1, lev, w=w):
                    r = (s[i1] - s[i0]) / 2
                    return M * r ** 2 - w[i0:i1 + 1].min() > eps / n
                cells[e], lim = refine(s, test)
            g = lp_gap(s, tree, cells, fstar)
            print(f"   Prop. B.4 rule edge by edge (M = {M:g}), eps {eps:g}: "
                  f"cells {[len(cells[e]) for e in (1, 2)]}, LP gap(PA) = "
                  f"{g:.2e}{' > eps' if g > eps else ''}")
            cells = {}
            for e in (1, 2):
                up, lo = E[e]["up"], E[e]["lo"]

                def test(i0, i1, lev, up=up, lo=lo):
                    g, _, _ = cell_bracket(s[i0:i1 + 1], up[i0:i1 + 1],
                                           lo[i0:i1 + 1])
                    return g > eps / n
                cells[e], lim = refine(s, test)
            g = lp_gap(s, tree, cells, fstar)
            flag = " [grid-limited]" if lim else ""
            print(f"   Theorem 1 rule, eps {eps:g}: cells "
                  f"{[len(cells[e]) for e in (1, 2)]}, LP gap(PA) = {g:.2e}"
                  f"{flag}")
            ok = ok and g <= eps + 1e-9
    # Added after review (R5): the reduced band of edge 1 after phi_2 = 0.
    # U'_1(s1) = min_{s2} [kappa (s1 - s2)^2 - beta s2^2], L_1 = -2 beta s1^2.
    # Closed form: -kappa beta/(kappa - beta) s1^2 for |s1| <= 1 - beta/kappa
    # (concave), kappa (|s1| - 1)^2 - beta beyond (convex).  Width near 0:
    # beta (kappa - 2 beta)/(kappa - beta) s1^2, zero for kappa = 2 beta.
    print("Reduced band of edge 1 after phi_2 = 0 (added after review):")
    sf = np.linspace(-1, 1, 2001)
    hf = sf[1] - sf[0]
    for beta, kappa in [(1.0, 10.0), (1.0, 2.0), (0.1, 10.0)]:
        Ur = (kappa * (sf[:, None] - sf[None, :]) ** 2
              - beta * sf[None, :] ** 2).min(axis=1)
        a0 = 1 - beta / kappa
        cf = np.where(np.abs(sf) <= a0,
                      -kappa * beta / (kappa - beta) * sf ** 2,
                      kappa * (np.abs(sf) - 1) ** 2 - beta)
        L1 = -2 * beta * sf ** 2
        d2 = np.diff(Ur, 2) / hf ** 2
        conc = sf[1:-1][d2 <= 1e-6]
        near = np.abs(sf) <= 0.2
        width = (Ur - L1)[near].max()
        width_cf = (beta * (kappa - 2 * beta) / (kappa - beta)
                    * sf[near] ** 2).max()
        g, _, _ = cell_bracket(sf, Ur, L1)
        print(f"  beta={beta}, kappa={kappa}: max|U'_1 - closed form| = "
              f"{np.max(np.abs(Ur - cf)):.1e}; U'_1 concave (grid) on "
              f"[{conc.min():.3f}, {conc.max():.3f}] (1 - beta/kappa = "
              f"{a0:.3f}); max width on |s| <= 0.2: {width:.2e} (closed form "
              f"{width_cf:.2e}); one-cell affine bracket of [L_1, U'_1] = "
              f"{g:.6f} (beta = {beta})")
        ok = ok and abs(g - beta) < 1e-6
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
