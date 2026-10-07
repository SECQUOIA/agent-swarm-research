"""Confirm-recheck C2: the T1 limit argument of the note (Section 3, Remarks):

    2 E_n <= gap(P_n) <= osc(r) + Lip(r)^2/(4K) = 2 E_n + Lip(r)^2/(4K),   r = |s| - p*,

for T1: bags -|s1|,  |s1| - |s2| + K (s1 - s2)^2,  |s2| on [-1, 1], P_n on both edges.

(1) E_n(|s|) and the best approximant p* by a Remez exchange for sqrt(t) on
    [0, 1] (E_n(|s|) = E_{n/2}(sqrt t) for even n, p*(s) = q*(s^2)), with
    golden-section refinement of the extrema.  Lip(r) = max_{0<s<=1} |1 - p*'(s)|.
(2) The bound on gap/2E_n for K = 10, 100, 1000, 10000.
(3) 2E_4 on the 161- and 321-point grids against the Remez value.
(4) n = 4, K = 100: grid LPs of the split relaxation on 161 ... 2561 points
    (constraints of the middle bag restricted to |s1 - s2| <= w; the solution
    is then checked against *all* grid constraints, so the value is the
    full-grid LP value).  Grid gaps are lower estimates of the continuum gap
    (f* = 0 is attained on the grid), so gap_grid / (Remez 2E_4) is a lower
    estimate of the continuum ratio.
(5) n = 4, K = 100: the gap of the fixed split phi_1 = phi_2 = -p* evaluated
    directly (an upper estimate of the continuum gap, tighter than the bound).
"""
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog, minimize_scalar, minimize

out = None


def log(m):
    print(m)
    if out is not None:
        out.write(m + "\n")
        out.flush()


def remez_sqrt(m, iters=60):
    """Best uniform approximation of sqrt(t) on [0,1] by degree m. Returns (E, coeffs in t-Chebyshev on [0,1])."""
    f = np.sqrt
    tmap = lambda t: 2 * t - 1
    ref = 0.5 * (1 - np.cos(np.pi * np.arange(m + 2) / (m + 1)))   # m+2 points incl. 0 and 1
    grid = np.unique(np.concatenate([np.linspace(0, 1, 200001), 0.5 * (1 - np.cos(np.pi * np.arange(20001) / 20000)),
                                     np.geomspace(1e-14, 1e-3, 2000)]))
    for _ in range(iters):
        A = np.hstack([C.chebvander(tmap(ref), m), ((-1.0) ** np.arange(m + 2))[:, None]])
        sol = np.linalg.solve(A, f(ref))
        c, E = sol[:m + 1], sol[m + 1]
        err = lambda t: f(t) - C.chebval(tmap(t), c)
        e = err(grid)
        # local extrema of e on the grid (including endpoints)
        idx = [0] + [i for i in range(1, len(grid) - 1)
                     if (e[i] - e[i - 1]) * (e[i + 1] - e[i]) <= 0 and abs(e[i]) > 0.5 * abs(E)] + [len(grid) - 1]
        # group by sign, keep the largest |e| in each run
        pts = []
        for i in idx:
            if pts and np.sign(e[i]) == np.sign(e[pts[-1]]):
                if abs(e[i]) > abs(e[pts[-1]]):
                    pts[-1] = i
            else:
                pts.append(i)
        while len(pts) > m + 2:   # drop the smaller end
            if abs(e[pts[0]]) < abs(e[pts[-1]]):
                pts.pop(0)
            else:
                pts.pop()
        new = []
        for i in pts:
            if i == 0 or i == len(grid) - 1:
                new.append(grid[i]); continue
            lo, hi = grid[i - 1], grid[i + 1]
            sgn = np.sign(e[i])
            r = minimize_scalar(lambda t: -sgn * err(t), bounds=(lo, hi), method="bounded",
                                options={"xatol": 1e-15})
            new.append(r.x)
        new = np.array(new)
        if len(new) != m + 2:
            raise RuntimeError("alternation set lost")
        emax = np.max(np.abs(err(new)))
        ref = new
        if emax - abs(E) < 1e-14 * max(1, abs(E)):
            break
    return abs(E), c, emax


def p_star(s, c):
    return C.chebval(2 * s ** 2 - 1, c)


def dp_star(s, c):
    return C.chebval(2 * s ** 2 - 1, C.chebder(c)) * 2 * (2 * s)   # d/ds q(s^2) with t-map 2t-1


def grid_E(n, npts):
    s = np.unique(np.concatenate([np.linspace(-1, 1, npts), [0.0]]))
    B = C.chebvander(s, n)
    d = n + 1
    cost = np.zeros(d + 1); cost[d] = 1
    A = np.vstack([np.hstack([B, -np.ones((len(s), 1))]), np.hstack([-B, -np.ones((len(s), 1))])])
    rhs = np.concatenate([np.abs(s), -np.abs(s)])
    res = linprog(cost, A_ub=A, b_ub=rhs, bounds=[(None, None)] * (d + 1), method="highs",
                  options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})
    return res.fun


def t1_grid_gap(n, K, npts, w):
    """Split LP: max mA + mB + mC with -|s1| - phi1 >= mA, b + phi1 - phi2 >= mB, |s2| + phi2 >= mC."""
    s = np.unique(np.concatenate([np.linspace(-1, 1, npts), [0.0]]))
    k = len(s)
    B = C.chebvander(s, n)
    d = n + 1
    nv = 2 * d + 3
    iA, iB, iC = 2 * d, 2 * d + 1, 2 * d + 2
    I, J = np.nonzero(np.abs(s[:, None] - s[None, :]) <= w + 1e-12)
    bvals = np.abs(s[I]) - np.abs(s[J]) + K * (s[I] - s[J]) ** 2
    R1 = np.zeros((k, nv)); R1[:, :d] = B; R1[:, iA] = 1                       # phi1 + mA <= -|s|
    R3 = np.zeros((k, nv)); R3[:, d:2 * d] = -B; R3[:, iC] = 1                 # -phi2 + mC <= |s|
    R2 = np.zeros((len(I), nv)); R2[:, :d] = -B[I]; R2[:, d:2 * d] = B[J]; R2[:, iB] = 1
    A = np.vstack([R1, R3, R2])
    rhs = np.concatenate([-np.abs(s), np.abs(s), bvals])
    cost = np.zeros(nv); cost[[iA, iB, iC]] = -1
    res = linprog(cost, A_ub=A, b_ub=rhs, bounds=[(None, None)] * nv, method="highs")
    assert res.status == 0, res.message
    x = res.x
    phi1, phi2 = B @ x[:d], B @ x[d:2 * d]
    # check all middle-bag grid constraints (not just the band |s1 - s2| <= w)
    mid_min = np.inf
    for i in range(k):
        row = np.abs(s[i]) - np.abs(s) + K * (s[i] - s) ** 2 + phi1[i] - phi2
        mid_min = min(mid_min, row.min())
    viol = x[iB] - mid_min
    rho = -res.fun
    return -rho, viol, len(I)


def main():
    log("(1) Remez for E_n(|s|) = E_{n/2}(sqrt t, [0,1])")
    Ks = [10.0, 100.0, 1000.0, 10000.0]
    info = {}
    for n in [4, 8]:
        E, c, emax = remez_sqrt(n // 2)
        s = np.linspace(1e-9, 1, 2000001)
        lipvals = np.abs(1 - dp_star(s, c))
        j = int(np.argmax(lipvals))
        lip = lipvals[j]
        r = np.abs(s) - p_star(s, c)
        info[n] = (E, c, lip)
        log(f"  n={n}: 2E_n = {2 * E:.10f} (largest error on refined reference {2 * emax:.10f}); "
            f"osc(r) on [0,1] grid = {r.max() - r.min():.10f}; Lip(r) = {lip:.6f} at s = {s[j]:.6f}")
        log("(2) bound on gap/2E_n = 1 + Lip(r)^2/(4K 2E_n):  " +
            ", ".join(f"K={K:g}: {1 + lip ** 2 / (4 * K * 2 * E):.5f}" for K in Ks))
    E4 = info[4][0]
    log("(3) grid values of 2E_4 against Remez")
    for npts in [161, 321]:
        g = 2 * grid_E(4, npts)
        log(f"  {npts} points: 2E_4 = {g:.10f}; relative difference to Remez {(2 * E4 - g) / (2 * E4):.2e}")
    log("(4) n = 4, K = 100: grid LP gap / Remez 2E_4 (lower estimates of the continuum ratio)")
    for npts, w in [(161, 2.0), (321, 2.0), (641, 0.3), (1281, 0.2), (2561, 0.12)]:
        g, viol, nrows = t1_grid_gap(4, 100.0, npts, w)
        log(f"  {npts} points (middle-bag rows {nrows}, band w = {w}): gap = {g:.8f}, "
            f"ratio = {g / (2 * E4):.5f}; largest violation of dropped constraints {viol:.1e}")
    log("(5) n = 4, K = 100: gap of the fixed split phi_1 = phi_2 = -p* (upper estimate)")
    E, c, lip = info[4]
    K = 100.0
    rfun = lambda x: np.abs(x) - p_star(x, c)
    # min over (s1, s2) of r(s1) - r(s2) + K (s1 - s2)^2: dense near-diagonal search, then local refinement
    ss = np.linspace(-1, 1, 4001)
    best = (np.inf, None)
    for dd in np.linspace(-0.05, 0.05, 401):
        s2 = np.clip(ss + dd, -1, 1)
        v = rfun(ss) - rfun(s2) + K * (ss - s2) ** 2
        i = int(np.argmin(v))
        if v[i] < best[0]:
            best = (v[i], (ss[i], s2[i]))
    f2 = lambda z: rfun(np.clip(z[0], -1, 1)) - rfun(np.clip(z[1], -1, 1)) + K * (z[0] - z[1]) ** 2
    loc = minimize(f2, np.array(best[1]), method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-15})
    mid = min(best[0], loc.fun)
    sf = np.linspace(-1, 1, 2000001)
    rr = rfun(sf)
    gap_phi = (rr.max() - rr.min()) - mid
    log(f"  min of the middle bag = {mid:.8f} (Lipschitz bound {-lip ** 2 / (4 * K):.8f}) at {np.round(loc.x, 6)}; "
        f"gap(phi) = {gap_phi:.8f}; gap(phi)/2E_4 = {gap_phi / (2 * E):.5f}")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    out = open("logs/c2_t1_bound.log", "w")
    main()
