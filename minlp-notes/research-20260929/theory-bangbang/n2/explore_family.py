"""Scan the k2-family (a=1, rho=0.5, k1=0.5, q=0.3, c=0.2, T=2, x0=0) for the sign of eta_L and F''.
Also: brute-force global check over bang-bang controls with <= 3 switches (continuous, closed form
via fine Euler-free polynomial evaluation is overkill; we use RK-exact piecewise polynomials)."""
import itertools
import sys
import numpy as np
from model import Par, with_, find_switch, solve_arcs, switch_quantities, Fpp_fd, pmp_check

base = Par(T=2.0, a=1.0, rho=0.5, k1=0.5, q=0.3, c=0.2)


def cost_bb(p, sw, u0):
    """Cost of a bang-bang control starting with u0 and switching at times sw (exact, piecewise poly)."""
    from numpy.polynomial import Polynomial as Poly
    t = Poly([0.0, 1.0])
    x1, x2, J, tprev, u = p.x10, p.x20, 0.0, 0.0, u0
    for tn in list(sw) + [p.T]:
        X2 = x2 + u * (t - tprev)
        X1 = x1 + x2 * (t - tprev) + 0.5 * u * (t - tprev) ** 2
        run = (p.e * X2 + 0.5 * p.q * X1 ** 2 - 0.5 * p.c * X2 ** 2 + (p.k1 * X1 + p.k2 * X2) * u).integ()
        J += run(tn) - run(tprev)
        x1, x2, tprev, u = X1(tn), X2(tn), tn, -u
    return J + p.Phi(x1, x2)


def global_bb(p, n=81):
    grid = np.linspace(0, p.T, n)
    best = (np.inf, None)
    for u0 in (1.0, -1.0):
        for m in range(0, 4):
            for sw in itertools.combinations(grid[1:-1], m):
                J = cost_bb(p, sw, u0)
                if J < best[0]:
                    best = (J, (u0, sw))
    return best


if __name__ == "__main__":
    for k2 in [0.2, 0.0, -0.2, -0.4, -0.6, -0.8, -1.0]:
        p = with_(base, k2=k2)
        roots = find_switch(p)
        for th in roots:
            sol = solve_arcs(p, th)
            sq = switch_quantities(p, sol)
            _, fdr = Fpp_fd(p, th)
            gb = global_bb(p, n=41 if k2 not in (0.2, -0.8) else 81)
            print("k2=%5.2f th=%.5f J=%.6f pmp=%.1e eta_L=%+.4f D=%.4f F''=%.4f (fd %.4f) | bb-grid best %.6f %s"
                  % (k2, th, sol["J"], pmp_check(p, sol), sq["eta_L"], sq["D"], sq["Fpp_formula"], fdr,
                     gb[0], (gb[1][0], np.round(gb[1][1], 3))), flush=True)
