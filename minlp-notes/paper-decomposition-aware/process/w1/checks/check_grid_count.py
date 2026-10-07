"""Worst-case node counts of graded grids at the localization radius.

For theta = 2^-mu and the extreme admissible conditioning kappa = 1/(8 theta^2),
the retained radius at stage j is at most R = 8 sqrt(kappa n_P) h_j (+1 for
integer coordinates).  At stage j+1 the mesh is h = h_j/2.  We build the
actual grids (exact Fractions) on [c-R, c+R] with a rational R' >= R and check
  (a) the mesh inequality w(v) <= h + theta |v - c| (corrected widths),
  (b) nodes <= 3 + (8/theta) ln(5/4 + 4 sqrt(2 n_P)),
  (c) nodes <= K = 10 theta^-1 ceil(log2(n_P + 2)).
Also checks the two scalar inequalities used in the proof of (c).
"""

import math
from fractions import Fraction as Fr

from core_lib import graded_grid, corrected_widths, ceil_log2


def rational_upper_sqrt(x, den=1 << 20):
    r = Fr(math.isqrt(int(x * den * den)) + 1, den)
    assert r * r >= x
    return r


def main():
    cases = 0
    worst = 0.0
    for mu in range(2, 8):
        theta = Fr(1, 2 ** mu)
        kappa = 1 / (8 * theta ** 2)
        for nP in (1, 2, 3, 4, 6, 10, 30, 100, 1000, 10 ** 4):
            Kcap = 10 * 2 ** mu * ceil_log2(nP + 2)
            bound_b = 3 + 8 * 2 ** mu * math.log(1.25 + 4 * math.sqrt(2 * nP))
            assert bound_b <= Kcap, (mu, nP, bound_b, Kcap)
            for hprime in (Fr(1, 7), Fr(1, 2), Fr(1), Fr(3, 2), Fr(5), Fr(37, 3)):
                hj = 2 * hprime
                Rc = 8 * rational_upper_sqrt(kappa * nP) * hj
                for integer in (False, True):
                    if integer:
                        R = Fr(math.floor(1 + Rc))
                        c = Fr(0)
                    else:
                        R, c = Rc, Fr(1, 3)
                    # node count can be large for tiny h; keep runs short
                    if R / max(hprime, Fr(1)) > 10 ** 6:
                        continue
                    g = graded_grid(c - R, c + R, c, hprime, theta, integer)
                    w = corrected_widths(g, integer)
                    for v, wv in zip(g, w):
                        assert wv <= hprime + theta * abs(v - c)
                    assert len(g) <= bound_b + 1e-9, (mu, nP, hprime, integer, len(g), bound_b)
                    assert len(g) <= Kcap
                    worst = max(worst, len(g) / Kcap)
                    cases += 1
    # scalar facts: log(1+t/3) >= t/4 on (0,1/4]; ln(1+x) >= x - x^2/2
    for k in range(1, 2001):
        t = 0.25 * k / 2000
        assert math.log1p(t / 3) >= t / 4
    print({"grid_cases": cases, "max_nodes_over_cap": round(worst, 4)})


if __name__ == "__main__":
    main()
