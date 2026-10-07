"""The bound-driven rule bd refines a coarsening of rule R3 (added after
review).

The validity part of the proof of Theorem 3 shows g_{e,D} <= B(D) for every
dyadic cell D, where g_{e,D} is the sliver bracket of Theorem 1(c) and B(D)
is the R3 quantity.  Hence bd (split while g > eps/n) splits only cells that
R3 (split while B > eps/n) also splits, and bd's partition is a coarsening
of R3's.  On the grid path instances D1-D4 of run_paths.py this script
  (1) evaluates g and B on every dyadic cell that R3 tests and reports the
      largest value of g - B;
  (2) checks that every R3 cell lies inside one bd cell.
Grid problems (exact minima on the grid), floating point; M is the analytic
bound of run_paths.py and G a grid estimate, as there.

usage: python3 check_bd_coarsening.py [fine_m]
"""
import sys
import numpy as np
from path_cells import PathFast, path_unaries, cell_bracket, refine
from run_paths import CONFIGS, edge_data, make_test


def main():
    fine_m = int(sys.argv[1]) if len(sys.argv) > 1 else 16385
    s = np.linspace(-1, 1, fine_m)
    ok = True
    for (name, n, kappa, A, v, tilt, kinks, centers) in CONFIGS:
        M = 2 * kappa + 2 * A + tilt[0] * tilt[1] ** 2
        un = path_unaries(n, s, A, v, kinks, tilt, centers)
        path = PathFast(s, kappa, un)
        E, fstar = edge_data(path)
        ds = s[1] - s[0]
        G = max(max(np.max(np.abs(np.diff(E[e]["U"]))),
                    np.max(np.abs(np.diff(E[e]["L"])))) / ds for e in E)
        for eps in [1e-2, 1e-3]:
            worst, tested, nested, counts = -np.inf, 0, True, []
            for e in range(1, n + 1):
                d = E[e]
                thm_test, up, lo = make_test("thm", s, d, n, eps, M, G)
                bd_test, _, _ = make_test("bd", s, d, n, eps, M, G)
                rec = []

                def wrapped(i0, i1, lev):
                    r = (s[i1] - s[i0]) / 2
                    wmin = d["w"][i0:i1 + 1].min()
                    interior = ((s[i0] + 1 >= 8 * n * r)
                                and (1 - s[i1] >= 8 * n * r))
                    if interior:
                        B = (32 * n + 0.5) * M * r ** 2 - wmin / (2 * n)
                    else:
                        B = 2 * G * r + 2.5 * M * r ** 2 - wmin / n
                    g, _, _ = cell_bracket(s[i0:i1 + 1], up[i0:i1 + 1],
                                           lo[i0:i1 + 1])
                    rec.append(g - B)
                    return thm_test(i0, i1, lev)

                c_thm, _ = refine(s, wrapped)
                c_bd, _ = refine(s, bd_test)
                worst = max(worst, max(rec))
                tested += len(rec)
                # every R3 cell inside one bd cell
                j = 0
                for (a, b) in c_thm:
                    while c_bd[j][1] < b:
                        j += 1
                    if not (c_bd[j][0] <= a and b <= c_bd[j][1]):
                        nested = False
                counts.append((len(c_bd), len(c_thm)))
            ok = ok and worst <= 1e-9 and nested
            print(f"{name.split()[0]}, eps={eps:g}: {tested} dyadic cells "
                  f"tested by R3, max (g - B) = {worst:.2e}; bd partition "
                  f"coarsens R3: {nested}; cells per edge (bd, R3): {counts}")
            sys.stdout.flush()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
