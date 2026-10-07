"""Referee check R3: kink rates, Bernstein constant, curvature-jump constant, hp aligned.

Best uniform approximation errors are computed with a Remez exchange (not an LP),
in a symmetry-reduced basis:
  E_{2m}(|x|)      : f(x) = x on [0,1], basis T_0, T_2, ..., T_{2m}  (even polys);
  E_{2m+1}(x|x|)   : f(x) = x^2 on (0,1], basis T_1, T_3, ..., T_{2m+1} (odd polys);
Positive-width bands (E6(c): U = -|s|, L = U - c s^2) are not best-approximation
problems; they use an LP on a graded grid plus a fine-grid re-evaluation.
"""
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog


def remez(f, basis, a, b, grid, iters=60, tol=1e-13, ref=None):
    """Minimax approximation of f on the grid (subset of [a, b]) by span(basis).
    basis(x) -> matrix (len(x), d).  Returns (E_lower, E_upper): the levelled
    error |h| (de la Vallee Poussin lower bound when the signs alternate) and the
    max error on the grid."""
    fx = f(grid)
    Bg = basis(grid)
    d = Bg.shape[1]
    npts = d + 1
    if ref is None:
        # Chebyshev extrema of degree npts-1 mapped to [grid[0], grid[-1]]
        tt = np.cos(np.pi * np.arange(npts) / (npts - 1))[::-1]
        pts = grid[0] + (tt + 1) / 2 * (grid[-1] - grid[0])
        idx = np.searchsorted(grid, pts).clip(0, len(grid) - 1)
    else:
        pts = ref
        idx = np.searchsorted(grid, pts).clip(0, len(grid) - 1)
    idx = np.unique(idx)
    assert len(idx) == npts
    for it in range(iters):
        A = np.hstack([Bg[idx], ((-1.0) ** np.arange(npts))[:, None]])
        sol = np.linalg.solve(A, fx[idx])
        c, h = sol[:d], sol[d]
        e = fx - Bg @ c
        # local extrema of e on the grid (including endpoints)
        de = np.diff(e)
        inner = np.nonzero(de[:-1] * de[1:] <= 0)[0] + 1
        ext = np.unique(np.concatenate([[0], inner, [len(e) - 1]]))
        # group consecutive extrema with the same sign, keep the largest |e|
        groups = []
        for i in ext:
            if abs(e[i]) == 0:
                continue
            if groups and np.sign(e[groups[-1]]) == np.sign(e[i]):
                if abs(e[i]) > abs(e[groups[-1]]):
                    groups[-1] = i
            else:
                groups.append(i)
        # trim to npts points keeping the global maximum
        while len(groups) > npts:
            if abs(e[groups[0]]) < abs(e[groups[-1]]):
                groups.pop(0)
            else:
                groups.pop()
        if len(groups) < npts:
            break
        new = np.array(groups)
        Emax = np.max(np.abs(e))
        lev = np.min(np.abs(e[new]))
        idx = new
        if Emax - lev <= tol * max(Emax, 1e-300) + 1e-16:
            break
    # final levelled bound: min |e| over an alternating reference is a lower bound
    return lev, Emax


def E_abs(n, M=400001):
    m = n // 2
    x = np.linspace(0, 1, M)
    basis = lambda t: C.chebvander(t, 2 * m)[:, ::2]
    ref = np.sort(np.cos(np.pi * np.arange(m + 2) / (2 * m + 2)))
    return remez(lambda t: t, basis, 0, 1, x, ref=ref)


def E_xabsx(n, M=400001):
    # odd polynomials of degree <= n: T_1, T_3, ..., T_{2m+1} with 2m+1 <= n
    m = (n - 1) // 2
    x = np.linspace(0, 1, M)[1:]
    basis = lambda t: C.chebvander(t, 2 * m + 1)[:, 1::2]
    ref = np.sort(np.cos(np.pi * np.arange(m + 2) / (2 * m + 3)))
    return remez(lambda t: t ** 2, basis, 0, 1, x, ref=ref)


def band_lp(U, L, s, n):
    B = C.chebvander(s, n)
    k, d = B.shape
    A1 = np.hstack([B, -np.ones((k, 1)), np.zeros((k, 1))])
    A2 = np.hstack([-B, np.zeros((k, 1)), -np.ones((k, 1))])
    cost = np.zeros(d + 2); cost[d:] = 1
    r = linprog(cost, A_ub=np.vstack([A1, A2]), b_ub=np.concatenate([U, -L]),
                bounds=[(None, None)] * (d + 2), method="highs",
                options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})
    return r.fun, r.x[:d]


def graded(M):
    # uniform + Chebyshev + dense near the kink at 0
    u = np.linspace(-1, 1, M)
    ch = np.cos(np.pi * (np.arange(M) + 0.5) / M)
    g = np.sign(u) * u ** 2
    return np.unique(np.concatenate([u, ch, g, [0.0]]))


if __name__ == "__main__":
    beta = 0.2801694990238691
    print("[Bernstein] gap = 2 E_n(|s|) for the zero-width kinked band U = L = -|s| (E1)")
    for n in [2, 4, 8, 16, 32, 64, 128, 256]:
        lo, hi = E_abs(n)
        print(f"  n={n:4d}: 2E_n in [{2 * lo:.8e}, {2 * hi:.8e}], n*gap = {2 * n * lo:.6f}  (2 beta = {2 * beta:.6f})")

    print("\n[Curvature jump] gap = 2 E_n((s_+)^2) = E_n(s|s|) (E2 = quadratic example of [S])")
    rows = []
    for n in [4, 8, 16, 32, 64, 128, 256, 512]:
        lo, hi = E_xabsx(n)
        rows.append((n, lo))
        print(f"  n={n:4d}: E_n(s|s|) in [{lo:.8e}, {hi:.8e}], n^2 * gap = {n * n * lo:.6f}")
    # Richardson in 1/n^2? use the last three values assuming K + a/n + b/n^2
    n_arr = np.array([r[0] for r in rows[-3:]], float)
    v = np.array([r[0] ** 2 * r[1] for r in rows[-3:]])
    A = np.column_stack([np.ones(3), 1 / n_arr, 1 / n_arr ** 2])
    K, a1, a2 = np.linalg.solve(A, v)
    print(f"  extrapolated lim n^2 E_n(s|s|) (fit K + a/n + b/n^2 on n = 128, 256, 512): {K:.5f}")
    print(f"  in sparse-order terms (n = 2R): ideal gap ~ {K / 4:.5f}/R^2; [S] bound 2/(27 pi (2R+2)^2) ~ "
          f"{2 / (27 * np.pi * 4):.6f}/R^2; ratio -> {K / 4 / (2 / (27 * np.pi * 4)):.2f}")
    print(f"  affine recourse: ideal gap 2E_2R(|y|) ~ beta/R = {beta:.5f}/R; [S] bound 1/(9 pi (R+1)) ~ "
          f"{1 / (9 * np.pi):.5f}/R; ratio -> {beta * 9 * np.pi:.3f}")
    # finite-R ratios (R = 2..32) using the Remez values
    print("  finite-R ratios ideal/[S]-bound:")
    for R in [2, 4, 8, 16, 32]:
        n = 2 * R
        lo_abs, _ = E_abs(n)
        lo_q, _ = E_xabsx(n)
        print(f"    R={R:3d}: affine recourse 2E_2R(|y|)*9pi(R+1) = {2 * lo_abs * 9 * np.pi * (R + 1):.3f};"
              f"  quadratic E_2R(y|y|)*27pi(2R+2)^2/2 = {lo_q * 27 * np.pi * (2 * R + 2) ** 2 / 2:.3f}")

    print("\n[Prop 5.6] E6(c): U = -|s|, L = -|s| - c s^2; LP on graded grid / fine re-evaluation")
    s = graded(3001)
    sf = graded(40001)
    for c in [0.5, 2.0, 8.0]:
        out = []
        for n in [1, 2, 3, 4, 6, 8, 16, 32]:
            g, coef = band_lp(-np.abs(s), -np.abs(s) - c * s ** 2, s, n)
            phif = C.chebvander(sf, n) @ coef
            gu = np.max(phif + np.abs(sf)) + np.max(-np.abs(sf) - c * sf ** 2 - phif)
            lb = 1 / (30 * (3 + c) * n)
            ok = "ok" if g >= lb else "FAIL"
            out.append(f"n={n}: {g:.5f}/{gu:.5f} (n*gap={n * g:.4f}; LB {lb:.5f} {ok})")
        print(f"  c={c}: " + "; ".join(out))

    print("\n[hp aligned] psi = -|s - c0| + 0.3 sin(3s) + 0.2 s^2, cells [-1,c0], [c0,1]; gap = max_D 2 E_p(psi|D)")
    c0 = 1 / np.sqrt(7)
    for p in [4, 8, 12]:
        vals = []
        for (lo, hi) in [(-1, c0), (c0, 1)]:
            x = np.linspace(lo, hi, 200001)
            f = lambda t: -np.abs(t - c0) + 0.3 * np.sin(3 * t) + 0.2 * t ** 2
            basis = lambda t, lo=lo, hi=hi: C.chebvander((2 * t - lo - hi) / (hi - lo), p)
            l, u = remez(f, basis, lo, hi, x)
            vals.append((l, u))
        gl = max(2 * v[0] for v in vals); gu = max(2 * v[1] for v in vals)
        print(f"  p={p:2d} N={2 * (p + 1)}: gap in [{gl:.3e}, {gu:.3e}]")
