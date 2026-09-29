"""Sharp x quadratic drift family with strip-adapted grids (revision after the review; the grid
recipe is the review's).  x = 2|t-1/3| - (t-1/3)^2, z = knot interpolant of (t - 29/70)^2.
x-grid: 1/3 +- d with d geometric of ratio 4 from eps/4;  z-grid: omega's z-cuts plus the left
and right greedy breakpoints of z at every strip budget eps + m_x(1/3 +- d) (and at eps), thinned
to at most GZ points.  Exact-verified guillotine optimum (upper bound on N_guill), omega, slice.
usage: python3 drift_grid.py GZ"""
import sys
from fractions import Fraction as Fr
from sepexact import Coord, run, guill_grid
import fam
from exp1 import family

GZ = int(sys.argv[1]) if len(sys.argv) > 1 else 200
A = Fr(1, 3)
for k in range(3, 12):
    eps = Fr(1, 10 ** k)
    cx, cz = family("sharp_quad", eps)
    ro = run([cx, cz], eps, "omega", record=True)
    cuts = fam.cut_positions(ro)
    gx = {Fr(0), Fr(1), A}
    d = eps / 4
    while d < 1:
        for p in (A - d, A + d):
            if 0 < p < 1:
                gx.add(p)
        d *= 4
    gx = sorted(gx)
    budgets = {eps} | {eps + cx.m(p) for p in gx}
    rz = Coord([-x for x in reversed(cz.x)], [h for h in reversed(cz.H)], shift=False)
    gz = set(cuts[1]) | {cz.L, cz.U}
    for b in budgets:
        gz |= set(cz.greedy(b))
        gz |= {-p for p in rz.greedy(b)}
    gz = fam.thin(sorted(gz), GZ)
    N, cert = guill_grid(cx, cz, gx, gz, eps)
    slice_ = len(cz.greedy(eps)) - 1
    print(f"eps=1e-{k}: grid {len(gx)}x{len(gz)}, exact-verified grid optimum {N}, omega leaves {ro['leaves']}, "
          f"omega/grid {ro['leaves'] / N:.3f}, slice N_z(eps) {slice_}, omega/slice {ro['leaves'] / slice_:.2f}", flush=True)
