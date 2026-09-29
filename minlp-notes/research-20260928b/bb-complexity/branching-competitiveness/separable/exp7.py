"""sharp x quadratic at smaller eps: omega, OPT_min, exact-verified grid optimum (usage: python3 exp7.py G)."""
import sys
from fractions import Fraction as Fr
from sepexact import run, guill_grid, opt_min
import fam
from exp1 import family

if __name__ == "__main__":
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    for k in (9, 10, 11):
        eps = Fr(1, 10 ** k)
        c1, c2 = family("sharp_quad", eps)
        ro = run([c1, c2], eps, "omega", record=True)
        om = opt_min(c1, c2, eps)
        cuts = fam.cut_positions(ro)
        g = []
        for c, cu in zip((c1, c2), cuts):
            pts = {c.L, c.U} | cu
            extra = fam.greedy_multi(c, eps, K=10)
            pts = set(fam.thin(sorted(pts), G // 2)) | set(fam.thin(sorted(extra), G - G // 2))
            g.append(fam.thin(sorted(pts), G))
        N, _ = guill_grid(c1, c2, g[0], g[1], eps)
        print(f"sharp_quad eps=1e-{k} grid={len(g[0])}x{len(g[1])} Ngrid={N} optmin={om} omega={ro['leaves']} "
              f"ratio={ro['leaves']/N:.2f} slice={len(c2.greedy(eps)) - 1}", flush=True)
