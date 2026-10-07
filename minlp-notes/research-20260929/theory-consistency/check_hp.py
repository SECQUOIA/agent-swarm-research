"""h, p and hp classes on one separator with a piecewise-analytic, kinked
zero-width band U = L = psi (note, Section 5.5; results in Section 7.5):

    psi(s) = -|s - c0| + 0.3 sin(3 s) + 0.2 s^2,   c0 = 1/sqrt(7) (not dyadic).

For a discontinuous cellwise class the gap is max_D g_D with
g_D = 2 E_{p_D}(psi|_D) (Proposition 2.3).  N = sum_D (p_D + 1) is the number
of degrees of freedom (split coefficients); #cells is the number of bag
subproblems per incident bag; max p fixes the moment order per subproblem.
"""
import numpy as np
from numpy.polynomial import chebyshev as C
from consistency_lib import grid, cheb_basis, band_gap

c0 = 1 / np.sqrt(7)


def psi(s):
    return -np.abs(s - c0) + 0.3 * np.sin(3 * s) + 0.2 * s ** 2


_cache = {}


def g_cell(lo, hi, p):
    key = (round(lo, 15), round(hi, 15), p)
    if key not in _cache:
        s = grid(lo, hi, 401, (c0,))
        v = psi(s)
        g, _, _, _ = band_gap(cheb_basis(s, p, lo, hi), v, v, tight=True)
        _cache[key] = max(g, 0.0)
    return _cache[key]


def mesh_gap(cells, degs):
    return max(g_cell(a, b, p) for (a, b), p in zip(cells, degs))


def dyadic_geometric(m):
    """Bisect the cell containing c0 m times, starting from [-1, 1]."""
    cells = []
    a, b = -1.0, 1.0
    for _ in range(m):
        mid = 0.5 * (a + b)
        if c0 < mid:
            cells.append((mid, b)); b = mid
        else:
            cells.append((a, mid)); a = mid
    kink = (a, b)
    return cells, kink


def decay_ratio(lo, hi, K=48):
    """Per-degree decay factor of the Chebyshev coefficients of psi on [lo, hi]
    (interpolation at 4K points).  Coefficients below 1e-13 * max are treated
    as round-off; if they reach round-off before degree 16 the cell counts as
    analytic (factor 0).  Otherwise the factor is exp(slope) of a least-squares
    fit of log|a_k| for 8 <= k <= last coefficient above round-off."""
    k = np.arange(4 * K)
    t = np.cos(np.pi * (k + 0.5) / (4 * K))
    s = 0.5 * (lo + hi) + 0.5 * (hi - lo) * t
    a = np.abs(C.chebfit(t, psi(s), K))
    scale = a[1:].max() + 1e-300
    above = np.nonzero(a > 1e-13 * scale)[0]
    kmax = above.max() if len(above) else 0
    if kmax < 16:
        return 0.0
    kk = np.arange(8, kmax + 1)
    # upper envelope: running max from the right removes zeros of odd/even parity
    env = np.maximum.accumulate(a[kk][::-1])[::-1]
    slope = np.polyfit(kk, np.log(env), 1)[0]
    return float(np.exp(slope))


def kink_estimate(lo, hi):
    """Location of the largest second difference of psi on a sample (a solver
    would use the active-set change of the private minimizer instead)."""
    s = np.linspace(lo, hi, 2001)
    d2 = np.abs(np.diff(psi(s), 2))
    j = int(np.argmax(d2)) + 1
    return s[j]


out = None  # opened under __main__ only, so importing this module leaves its log alone


def log(m):
    print(m)
    if out is not None:
        out.write(m + "\n")
        out.flush()


def main():
    log("[p only] one cell, degree p")
    for p in [1, 2, 4, 8, 16, 32]:
        log(f"  p={p:2d} N={p + 1:3d}: gap = {g_cell(-1, 1, p):.3e}")
    log("[h only] uniform cells, degree 1 (PA)")
    for J in [4, 16, 64, 256]:
        e = np.linspace(-1, 1, J + 1)
        cells = list(zip(e[:-1], e[1:]))
        log(f"  J={J:4d} N={2 * J:4d}: gap = {mesh_gap(cells, [1] * J):.3e}")
    log("[hp aligned] cells [-1, c0], [c0, 1], degree p")
    for p in [1, 2, 4, 6, 8, 10, 12, 14]:
        log(f"  p={p:2d} N={2 * (p + 1):3d}: gap = {mesh_gap([(-1, c0), (c0, 1)], [p, p]):.3e}")
    log("[hp geometric, dyadic, not aligned] m bisections toward c0; degree p on non-kink cells, 1 on the kink cell")
    for m in [2, 4, 6, 8, 10, 12, 14]:
        cells, kink = dyadic_geometric(m)
        best = None
        for p in range(1, 16):
            degs = [p] * len(cells) + [1]
            g = mesh_gap(cells + [kink], degs)
            N = sum(d + 1 for d in degs)
            if best is None or g < best[0] * 0.999:
                best = (g, p, N)
        g, p, N = best
        log(f"  m={m:2d} cells={m + 1:2d} best p={p:2d} N={N:4d}: gap = {g:.3e}, "
            f"log(gap)/sqrt(N) = {np.log(g) / np.sqrt(N):.3f}")
    for variant in ["midpoint", "kink-split"]:
        log(f"[adaptive hp, {variant}] refine the worst cell; raise p if the coefficient decay factor < 0.8, else split")
        cells, degs = [(-1.0, 1.0)], [1]
        targets = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
        ti = 0
        it = 0
        while ti < len(targets) and it < 300:
            gs = [g_cell(a, b, p) for (a, b), p in zip(cells, degs)]
            G = max(gs)
            while ti < len(targets) and G <= targets[ti]:
                N = sum(d + 1 for d in degs)
                log(f"  tol={targets[ti]:.0e}: gap={G:.2e} N={N:4d} cells={len(cells):2d} max p={max(degs):2d} "
                    f"smallest cell={min(b - a for a, b in cells):.1e}")
                ti += 1
            j = int(np.argmax(gs))
            a, b = cells[j]
            if decay_ratio(a, b) < 0.8:
                degs[j] += 1
            else:
                mid = 0.5 * (a + b) if variant == "midpoint" else kink_estimate(a, b)
                cells[j:j + 1] = [(a, mid), (mid, b)]
                degs[j:j + 1] = [degs[j], degs[j]]
            it += 1
        log(f"  iterations: {it}")


if __name__ == "__main__":
    out = open("logs/check_hp.log", "w")
    main()
