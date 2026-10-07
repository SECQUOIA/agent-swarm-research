"""Checks for the second revision (after the recheck; Section 12.2 of the note).

(1) T1 (Section 3, Remarks): with phi_1 = phi_2 = -p, p a near-best degree-n
    approximant of |s|, and r = |s| - p, the three bag bounds give
        gap <= osc(r) + Lip(r)^2 / (4K),
    so gap -> 2 E_n as K -> inf.  Evaluates this upper bound (continuum
    quantities evaluated on a fine grid) against 2 E_n.
(2) Unaligned hp (Proposition 5.8(b)): relative distance of the kink c0 to the
    cells left behind by dyadic bisection, and per-cell errors 2 E_p on the
    level-4 cell [0.25, 0.375] (next to c0) against the same-width cell
    [0.125, 0.25], for the note's psi (each piece extends to an entire
    function) and for an algebraic variant with |s - c0|^{4/3} (branch point
    at c0); and, for the dyadic meshes of check_hp.py, the kink cell against
    the other cells.
(3) Proposition 5.6: ratio of the computed E6(c) gap to the bound
    1/(30 (3 + c) n) for n = 1..32 (graded-grid LP, as check_pinch_rates.py);
    n = 64, 128 are read from logs/check_pinch_rates.log.
"""
import re
import numpy as np
from numpy.polynomial import chebyshev as C
from consistency_lib import grid, cheb_basis, band_gap, eval_gap
import check_hp as HP

out = None


def log(m):
    print(m)
    if out is not None:
        out.write(m + "\n")
        out.flush()


def t1_bound():
    log("(1) T1 upper bound gap <= osc(r) + Lip(r)^2/(4K), r = |s| - p (continuum), against 2E_n")
    s = grid(-1, 1, 20001, (0.0,))
    sf = grid(-1, 1, 200001, (0.0,))
    for n in [4, 8]:
        U = -np.abs(s)
        g, c, _, _ = band_gap(cheb_basis(s, n), U, U, tight=True)   # g = 2 E_n on the grid; B c ~ -|s|
        p_f = -(cheb_basis(sf, n) @ c)                               # p ~ |s|
        r = np.abs(sf) - p_f
        osc = r.max() - r.min()
        dp = C.chebval(sf, C.chebder(-c))
        lip = np.max(np.abs(np.sign(sf) - dp))
        log(f"  n={n}: 2E_n (grid LP) = {g:.6f}, osc(r) on fine grid = {osc:.6f}, Lip(r) = {lip:.4f}")
        for K in [10.0, 100.0, 1000.0, 10000.0]:
            ub = osc + lip ** 2 / (4 * K)
            log(f"    K={K:7.0f}: bound on gap/2E_n <= {ub / g:.4f}")


def hp_checks():
    c0 = HP.c0
    log("(2a) dyadic bisection toward c0 = 1/sqrt 7: relative distance t = dist(c0, cell)/half-width of the cells left behind")
    cells, kink = HP.dyadic_geometric(15)
    for j, (a, b) in enumerate(cells, 1):
        t = min(abs(c0 - a), abs(c0 - b)) / ((b - a) / 2)
        rho = 1 + t + np.sqrt(t * (t + 2))
        log(f"  level {j:2d}: cell [{a:.6f}, {b:.6f}]  t = {t:.4f}  (ellipse avoiding c0: rho = {rho:.3f})")
    log(f"  kink cell after 15 levels: [{kink[0]:.7f}, {kink[1]:.7f}]")

    psi = HP.psi
    psi_alg = lambda s: -np.abs(s - c0) ** (4.0 / 3.0) + 0.3 * np.sin(3 * s) + 0.2 * s ** 2
    log("(2b) per-cell error 2E_p: level-4 cell [0.25, 0.375] (t = 0.047) against the same-width cell [0.125, 0.25] (t = 2.05)")
    for name, f in [("psi (pieces entire)", psi), ("psi_alg (|s - c0|^(4/3))", psi_alg)]:
        row = []
        for p in [1, 2, 3, 4]:
            vals = []
            for lo, hi in [(0.25, 0.375), (0.125, 0.25)]:
                s = grid(lo, hi, 2001)
                v = f(s)
                g, cc, _, _ = band_gap(cheb_basis(s, p, lo, hi), v, v, tight=True)
                vals.append(g)
            row.append(f"p={p}: {vals[0]:.3e} vs {vals[1]:.3e} (ratio {vals[0] / vals[1]:.2f})")
        log(f"  {name}: " + "; ".join(row))
    log("(2c) dyadic meshes of check_hp.py with its best uniform p: kink cell (degree 1) against the other cells")
    for m, p in [(2, 2), (4, 4), (6, 4), (8, 4), (10, 4), (12, 6), (14, 6)]:
        cells, kink = HP.dyadic_geometric(m)
        gk = HP.g_cell(kink[0], kink[1], 1)
        go = max(HP.g_cell(a, b, p) for a, b in cells)
        log(f"  m={m:2d} p={p}: kink cell g_D = {gk:.3e}, largest other g_D = {go:.3e}")


def prop56_ratios():
    log("(3) Proposition 5.6: ratio gap / (1/(30 (3+c) n)) = 30 (3+c) n gap for E6(c): U = -|s|, L = U - c s^2")
    geo = np.concatenate([10.0 ** -np.arange(1, 7, 0.05), -10.0 ** -np.arange(1, 7, 0.05), [0.0]])
    s = np.unique(np.concatenate([grid(-1, 1, 8001), geo]))
    sf = np.unique(np.concatenate([grid(-1, 1, 80001), geo]))
    logged = {}
    try:
        txt = open("logs/check_pinch_rates.log").read().split("E6(c)")[1]
        for line in txt.splitlines():
            m = re.match(r"\s*c=\s*([\d.]+):", line)
            if m:
                for n, lo, up in re.findall(r"n=(\d+): ([\d.]+)/([\d.]+)", line):
                    logged[(float(m.group(1)), int(n))] = (float(lo), float(up))
    except (OSError, IndexError):
        pass
    for c in [0.5, 2.0, 8.0]:
        U = -np.abs(s)
        L = U - c * s ** 2
        row = []
        for n in [1, 2, 3, 4, 8, 16, 32]:
            g, cc, _, _ = band_gap(cheb_basis(s, n), U, L, tight=True)
            gu = eval_gap(cheb_basis(sf, n) @ cc, -np.abs(sf), -np.abs(sf) - c * sf ** 2)
            row.append(f"n={n}: {30 * (3 + c) * n * g:.1f}/{30 * (3 + c) * n * gu:.1f}")
        for n in [64, 128]:
            if (c, n) in logged:
                lo, up = logged[(c, n)]
                row.append(f"n={n} (log): {30 * (3 + c) * lo:.1f}/{30 * (3 + c) * up:.1f}")
        log(f"  c={c}: " + "; ".join(row) + "   (lower/upper estimate)")


if __name__ == "__main__":
    out = open("logs/check_revision2.log", "w")
    t1_bound()
    hp_checks()
    prop56_ratios()
