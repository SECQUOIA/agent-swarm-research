"""Confirm-recheck C3: Proposition 5.8(b) of the note (unaligned breakpoint,
dyadic bisection), for the note's test function

    psi(s) = -|s - c0| + 0.3 sin(3 s) + 0.2 s^2,   c0 = 1/sqrt 7,   [a, b] = [-1, 1].

(a) Inclusion E_rho(D) in E_rho(I) for subintervals D of I: random test.
(b) The inequality  gap <= max(4 M rho^-p/(rho - 1), G (b - a) 2^-m)  with
    p = ceil(m log 2/log rho), and gap <= C' exp(-b sqrt N) with
    C' = max(4M/(rho-1), G(b-a)) * rho * exp(b sqrt 2), b = sqrt(log 2 log rho),
    for rho = 2, 4, 8.  M = max |psi_piece| on the ellipse of each piece (max
    modulus on the boundary), G = max |psi'|.  The actual gap is max_D 2E_{p_D}
    over the cells, from a grid LP re-evaluated on a 10x finer grid (upper
    estimate of each 2E_p).
(c) Per-cell errors 2E_p, p = 1..4, on [0.25, 0.375] (next to c0) and
    [0.125, 0.25], for psi and for psi_alg = -|s - c0|^{4/3} + 0.3 sin 3s + 0.2 s^2,
    by a Remez exchange (independent of the note's grid LP).
"""
import math
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog, minimize_scalar

out = None
c0 = 1 / math.sqrt(7)


def log(m):
    print(m)
    if out is not None:
        out.write(m + "\n")
        out.flush()


def psi(s):
    return -np.abs(s - c0) + 0.3 * np.sin(3 * s) + 0.2 * s ** 2


def psi_alg(s):
    return -np.abs(s - c0) ** (4.0 / 3.0) + 0.3 * np.sin(3 * s) + 0.2 * s ** 2


def ellipse(lo, hi, rho, npts=4000):
    th = np.linspace(0, 2 * np.pi, npts, endpoint=False)
    w = rho * np.exp(1j * th)
    return 0.5 * (lo + hi) + 0.25 * (hi - lo) * (w + 1 / w)


def cell_err_upper(f, lo, hi, p, m=2001, mf=20001):
    """Grid-LP best approximation of degree p on [lo, hi]; returns 2 * (max error of
    the LP polynomial on a 10x finer grid) = upper estimate of 2 E_p."""
    def pts(k):
        u = np.linspace(lo, hi, k)
        ch = 0.5 * (lo + hi) + 0.5 * (hi - lo) * np.cos(np.pi * (np.arange(k) + 0.5) / k)
        return np.unique(np.concatenate([u, ch]))
    s = pts(m)
    t = (2 * s - lo - hi) / (hi - lo)
    B = C.chebvander(t, p)
    v = f(s)
    d = p + 1
    cost = np.zeros(d + 1); cost[d] = 1
    A = np.vstack([np.hstack([B, -np.ones((len(s), 1))]), np.hstack([-B, -np.ones((len(s), 1))])])
    res = linprog(cost, A_ub=A, b_ub=np.concatenate([v, -v]), bounds=[(None, None)] * (d + 1),
                  method="highs", options={"primal_feasibility_tolerance": 1e-10,
                                            "dual_feasibility_tolerance": 1e-10})
    assert res.status == 0
    sf = pts(mf)
    tf = (2 * sf - lo - hi) / (hi - lo)
    e = np.max(np.abs(f(sf) - C.chebval(tf, res.x[:d])))
    return 2 * e


def remez(f, lo, hi, n, iters=80):
    """Best uniform approximation error E_n of f on [lo, hi] (float64 Remez with refinement)."""
    tm = lambda s: (2 * s - lo - hi) / (hi - lo)
    ref = 0.5 * (lo + hi) - 0.5 * (hi - lo) * np.cos(np.pi * np.arange(n + 2) / (n + 1))
    k = 40001
    grid = np.unique(np.concatenate([np.linspace(lo, hi, k),
                                     0.5 * (lo + hi) - 0.5 * (hi - lo) * np.cos(np.pi * np.arange(k) / (k - 1))]))
    E = None
    for _ in range(iters):
        A = np.hstack([C.chebvander(tm(ref), n), ((-1.0) ** np.arange(n + 2))[:, None]])
        sol = np.linalg.solve(A, f(ref))
        c, E = sol[:n + 1], sol[n + 1]
        err = lambda s: f(s) - C.chebval(tm(s), c)
        e = err(grid)
        idx = [0] + [i for i in range(1, len(grid) - 1) if (e[i] - e[i - 1]) * (e[i + 1] - e[i]) <= 0] + [len(grid) - 1]
        pts = []
        for i in idx:
            if pts and np.sign(e[i]) == np.sign(e[pts[-1]]):
                if abs(e[i]) > abs(e[pts[-1]]):
                    pts[-1] = i
            else:
                pts.append(i)
        while len(pts) > n + 2:
            if abs(e[pts[0]]) < abs(e[pts[-1]]):
                pts.pop(0)
            else:
                pts.pop()
        if len(pts) < n + 2:
            raise RuntimeError("alternation lost")
        new = []
        for i in pts:
            if i in (0, len(grid) - 1):
                new.append(grid[i]); continue
            sg = np.sign(e[i])
            r = minimize_scalar(lambda s: -sg * err(s), bounds=(grid[i - 1], grid[i + 1]), method="bounded",
                                options={"xatol": 1e-16})
            new.append(r.x)
        ref = np.array(new)
        emax = np.max(np.abs(err(ref)))
        if emax - abs(E) <= 1e-12 * abs(E):
            break
    return abs(E), emax


def dyadic(m):
    cells, a, b = [], -1.0, 1.0
    for _ in range(m):
        mid = 0.5 * (a + b)
        if c0 < mid:
            cells.append((mid, b)); b = mid
        else:
            cells.append((a, mid)); a = mid
    return cells, (a, b)


def main():
    rng = np.random.default_rng(1)
    worst = -np.inf
    for _ in range(2000):
        aI, bI = np.sort(rng.uniform(-3, 3, 2))
        aD, bD = np.sort(rng.uniform(aI, bI, 2))
        rho = 1 + rng.exponential(1.0)
        R = (rho + 1 / rho) / 2
        z = ellipse(aD, bD, rho, 200)
        # points on the boundary of E_rho(D) must lie in the closure of E_rho(I)
        worst = max(worst, np.max((np.abs(z - aI) + np.abs(z - bI)) / ((bI - aI) * R)))
    log(f"(a) E_rho(D) in E_rho(I): largest (|z-a_I| + |z-b_I|)/(|I| R) over boundary points of E_rho(D): {worst:.6f} (must be <= 1)")

    sgrid = np.linspace(-1, 1, 400001)
    dpsi = np.where(sgrid < c0, 1.0, -1.0) + 0.9 * np.cos(3 * sgrid) + 0.4 * sgrid
    G = np.max(np.abs(dpsi))
    left = lambda z: (z - c0) + 0.3 * np.sin(3 * z) + 0.2 * z ** 2
    right = lambda z: -(z - c0) + 0.3 * np.sin(3 * z) + 0.2 * z ** 2
    log(f"(b) G = max|psi'| = {G:.4f}")
    for rho in [2.0, 4.0, 8.0]:
        M = max(np.max(np.abs(left(ellipse(-1, c0, rho)))), np.max(np.abs(right(ellipse(c0, 1, rho)))))
        bb = math.sqrt(math.log(2) * math.log(rho))
        Cp = max(4 * M / (rho - 1), G * 2) * rho * math.exp(bb * math.sqrt(2))
        log(f"  rho = {rho}: M = {M:.3f}, b = {bb:.4f}, C' = {Cp:.3e}")
        ok = True
        for m in [2, 4, 6, 8, 10, 12, 14]:
            p = math.ceil(m * math.log(2) / math.log(rho))
            cells, kink = dyadic(m)
            g_other = max(cell_err_upper(psi, lo, hi, p) for lo, hi in cells)
            g_kink = cell_err_upper(psi, kink[0], kink[1], 1)
            gap = max(g_other, g_kink)
            N = m * (p + 1) + 2
            bound = max(4 * M * rho ** (-p) / (rho - 1), G * 2 * 2.0 ** (-m))
            bound2 = Cp * math.exp(-bb * math.sqrt(N))
            ok &= gap <= bound and bound <= bound2 * (1 + 1e-12)
            log(f"    m={m:2d} p={p:2d} N={N:3d}: gap (upper est.) = {gap:.3e} [other cells {g_other:.2e}, kink cell {g_kink:.2e}]"
                f" <= bound {bound:.3e} <= C' exp(-b sqrt N) = {bound2:.3e}")
        log(f"  rho = {rho}: all inequalities hold: {ok}")

    log("(c) Remez 2E_p on [0.25, 0.375] (t = 0.047) and [0.125, 0.25] (t = 2.05)")
    for name, f in [("psi", psi), ("psi_alg", psi_alg)]:
        parts = []
        for p in [1, 2, 3, 4]:
            e1, u1 = remez(f, 0.25, 0.375, p)
            e2, u2 = remez(f, 0.125, 0.25, p)
            parts.append(f"p={p}: {2 * e1:.4e} vs {2 * e2:.4e} (ratio {e1 / e2:.2f}; "
                         f"rel. check {max(u1 / e1, u2 / e2) - 1:.0e})")
        log(f"  {name}: " + "; ".join(parts))


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    out = open("logs/c3_prop58b.log", "w")
    main()
