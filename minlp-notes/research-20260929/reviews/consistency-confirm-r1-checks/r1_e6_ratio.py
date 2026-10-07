"""Independent check of the Proposition 5.6 ratio 30 (3 + c) n gap(P_n) for
E6(c): U = -|s|, L = -|s| - c s^2 on [-1, 1], c = 0.5, 2, 8.

Own LP (Legendre basis, own graded grid; no code shared with the note):
    gap = min_p [ max(p - U) + max(L - p) ]  over p in P_n.
Grid value = lower estimate; the same p re-evaluated on a 10x finer grid gives
an upper estimate.  Closed forms for n = 1, 2, 3 (derived in the report):
    gap(P_1) = 1,  gap(P_2) = gap(P_3) = 1 / (4 (1 + c)).
Floating point (HiGHS via scipy); not certified.
"""
import numpy as np
from numpy.polynomial import legendre as Lg
from scipy.optimize import linprog

out = open("logs/r1_e6_ratio.log", "w")


def log(m):
    print(m)
    out.write(m + "\n")
    out.flush()


def mkgrid(m):
    u = np.linspace(-1, 1, m)
    g = np.logspace(-9, 0, m // 2)
    return np.unique(np.concatenate([u, g, -g, [0.0]]))


def gap(n, c, m=6001):
    s = mkgrid(m)
    U = -np.abs(s)
    L = U - c * s ** 2
    B = Lg.legvander(s, n)
    d = n + 1
    A = np.vstack([np.hstack([B, -np.ones((len(s), 1)), np.zeros((len(s), 1))]),
                   np.hstack([-B, np.zeros((len(s), 1)), -np.ones((len(s), 1))])])
    b = np.concatenate([U, -L])
    cost = np.zeros(d + 2)
    cost[d:] = 1
    res = None
    for tol in [1e-10, 1e-9, None]:     # retry with looser tolerances if HiGHS stops early
        opts = {} if tol is None else {"primal_feasibility_tolerance": tol, "dual_feasibility_tolerance": tol}
        res = linprog(cost, A_ub=A, b_ub=b, bounds=[(None, None)] * (d + 2), method="highs", options=opts)
        if res.status == 0:
            break
    assert res.status == 0, res.message
    coef = res.x[:d]
    sf = mkgrid(10 * m)
    pf = Lg.legval(sf, coef)
    Uf = -np.abs(sf)
    up = np.max(pf - Uf) + np.max(Uf - c * sf ** 2 - pf)
    return res.fun, up


log("Ratio 30 (3 + c) n gap for E6(c); lower/upper estimate; closed form where known")
table = {}
for n in [1, 2, 3, 4, 8, 16, 32]:
    row = []
    for c in [0.5, 2.0, 8.0]:
        lo, up = gap(n, c)
        f = 30 * (3 + c) * n
        closed = 1.0 if n == 1 else (1 / (4 * (1 + c)) if n in (2, 3) else None)
        cs = f"; closed form {f * closed:.3f}" if closed is not None else ""
        row.append((f * lo, f * up))
        log(f"  n={n:3d} c={c:3.1f}: gap {lo:.6e}/{up:.6e}  ratio {f * lo:.2f}/{f * up:.2f}{cs}")
    los = [r[0] for r in row]
    ups = [r[1] for r in row]
    inc = all(ups[i] < los[i + 1] for i in range(2))
    dec = all(los[i] > ups[i + 1] for i in range(2))
    kind = "increasing" if inc else "decreasing" if dec else "not monotone (or brackets overlap)"
    log(f"  n={n:3d}: ratios {', '.join(f'{x:.1f}' for x in los)} -> {kind} in c (bracket-safe)")

log("n = 64, 128 from the note's logs/check_pinch_rates.log (n gap lower/upper), converted to ratios:")
E6 = {0.5: {64: (0.4629, 0.4644), 128: (0.4855, 0.5022)},
      2.0: {64: (0.3816, 0.3888), 128: (0.4209, 0.4754)},
      8.0: {64: (0.2722, 0.2926), 128: (0.3257, 0.5330)}}
for n in [64, 128]:
    br = [(30 * (3 + c) * E6[c][n][0], 30 * (3 + c) * E6[c][n][1]) for c in [0.5, 2.0, 8.0]]
    inc = all(br[i][1] < br[i + 1][0] for i in range(2))
    log(f"  n={n}: " + ", ".join(f"[{a:.1f}, {b:.1f}]" for a, b in br) + f" -> brackets disjoint and increasing: {inc}")
