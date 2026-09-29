"""omega / deficit / OPT_min on anisotropic quadratics m = (x-a)^2 + g (z-b)^2 (exact knot instances)."""
import sys
from fractions import Fraction as Fr
from sepexact import run, opt_min
import fam
A, B = Fr(1, 3), Fr(29, 70)
if __name__ == "__main__":
    g = Fr(sys.argv[1])
    for k in range(3, 11):
        eps = Fr(1, 10 ** k)
        c1 = fam.quad(A, 1, rmin=Fr(1, 10 ** 7), ratio=Fr(9, 8))
        c2 = fam.quad(B, g, rmin=Fr(1, 10 ** 7), ratio=Fr(9, 8))
        ro, rd = run([c1, c2], eps, "omega"), run([c1, c2], eps, "deficit")
        om = opt_min(c1, c2, eps, cap=2000000)
        print(f"g={g} eps=1e-{k} omega={ro['leaves']} deficit={rd['leaves']} optmin={om} "
              f"omega/optmin={ro['leaves']/om:.3f} deficit/optmin={rd['leaves']/om:.3f}", flush=True)
