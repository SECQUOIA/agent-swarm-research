"""OPT_min (best offline minimizer rule) vs omega vs grid optimum on families.
usage: python3 exp2.py FAMILY [G]"""
import sys
from fractions import Fraction as Fr
from sepexact import run, guill_grid, opt_min
import fam
from exp1 import family

if __name__ == "__main__":
    name = sys.argv[1]
    G = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    for k in (3, 4, 5, 6, 7, 8):
        eps = Fr(1, 10 ** k)
        c1, c2 = family(name, eps)
        ro = run([c1, c2], eps, "omega", record=True)
        om = opt_min(c1, c2, eps)
        cuts = fam.cut_positions(ro)
        g = []
        for c, cu in zip((c1, c2), cuts):
            pts = {c.L, c.U} | cu
            extra = fam.greedy_multi(c, eps, K=10)
            pts = set(fam.thin(sorted(pts), G // 2)) | set(fam.thin(sorted(extra), G - G // 2))
            g.append(fam.thin(sorted(pts), G))
        N, cert = guill_grid(c1, c2, g[0], g[1], eps, certificate=False)
        print(f"{name} eps=1e-{k} Ngrid={N} optmin={om} omega={ro['leaves']} omega/optmin={ro['leaves']/om:.2f} optmin/Ngrid={om/N:.2f}", flush=True)
