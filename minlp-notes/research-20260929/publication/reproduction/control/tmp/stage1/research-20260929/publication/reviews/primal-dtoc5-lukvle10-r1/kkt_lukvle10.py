"""Reviewer's numerical (not rigorous) check of the track's KKT claims for lukvle10.

1. KKT residual of the track's stored KKT point (logs/lukvle10_kkt_x.txt, lukvle10_kkt_lam.txt):
   rows g_j(x) = -x_j + 3x_{j+1} - 2x_{j+2} - 2x_{j+1}^2 + 1 and stationarity grad f + sum lam_j grad g_j
   (both sign conventions tried).
2. Distance of the exactly feasible point x* (seeds propagated in 2400-digit floating point) from
   the stored KKT point, and the stationarity residual at x* with the stored multipliers.
Gradient formulas are written here by hand from the OSIL objective
   sum over pairs (a,b) of (x_a^2)^(x_b^2+1) + (x_b^2)^(x_a^2+1).
"""
import json, os, time
from fractions import Fraction
from mpmath import mp, mpf, log, exp

T0 = time.time()
mp.dps = 900
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
TRACK = _REPO + "/research-20260929/publication/primal/dtoc5-lukvle10"
n, m = 1000, 998


def load(path, nkey):
    d = {}
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        k, v = line.split()
        d[k] = mpf(v)
    return d


xd = load(TRACK + "/logs/lukvle10_kkt_x.txt", None)
xk = [xd[f"x{k + 1}"] for k in range(n)]
ld = load(TRACK + "/logs/lukvle10_kkt_lam.txt", None)
lam = [ld[str(j)] for j in range(m)]


def rows(x):
    return [-x[j] + 3 * x[j + 1] - 2 * x[j + 2] - 2 * x[j + 1] ** 2 + 1 for j in range(m)]


def fgrad(x):
    f = mpf(0)
    g = [mpf(0)] * n
    for i in range(500):
        a, b = 2 * i, 2 * i + 1
        A, B = x[a] ** 2, x[b] ** 2
        t1 = exp((B + 1) * log(A))
        t2 = exp((A + 1) * log(B))
        f += t1 + t2
        g[a] += t1 * (B + 1) * 2 / x[a] + t2 * log(B) * 2 * x[a]
        g[b] += t1 * log(A) * 2 * x[b] + t2 * (A + 1) * 2 / x[b]
    return f, g


def stat(x, lam, s):
    _, g = fgrad(x)
    r = list(g)
    for j in range(m):
        r[j] += s * lam[j] * (-1)
        r[j + 1] += s * lam[j] * (3 - 4 * x[j + 1])
        r[j + 2] += s * lam[j] * (-2)
    return max(abs(v) for v in r)


def lsq_res(x):
    """least-squares multipliers mu from J J^T mu = -J grad f (pentadiagonal SPD, banded elimination);
    returns (log10 max |grad f + J^T mu|, mu)"""
    _, g = fgrad(x)
    c = [3 - 4 * x[j + 1] for j in range(m)]  # J[j] = (-1 at j, c_j at j+1, -2 at j+2)
    A = [[mpf(0)] * 3 for _ in range(m)]  # A[j][d] = (J J^T)[j][j+d]
    for j in range(m):
        A[j][0] = 1 + c[j] ** 2 + 4
        if j + 1 < m:
            A[j][1] = -c[j] - 2 * c[j + 1]
        if j + 2 < m:
            A[j][2] = mpf(2)
    rhs = [-(-g[j] + c[j] * g[j + 1] - 2 * g[j + 2]) for j in range(m)]
    # symmetric banded Gaussian elimination (no pivoting; A is SPD)
    U = [row[:] for row in A]
    b = rhs[:]
    for j in range(m):
        for d in (1, 2):
            i = j + d
            if i >= m:
                continue
            f = U[j][d] / U[j][0]  # A[i][j] = A[j][i] by symmetry
            # row i -= f * row j  (row j has entries at j, j+1, j+2)
            for e in range(d, 3):
                k = j + e
                if k < m and k - i <= 2:
                    U[i][k - i] -= f * U[j][e]
            b[i] -= f * b[j]
    mu = [mpf(0)] * m
    for j in range(m - 1, -1, -1):
        sacc = b[j]
        for d in (1, 2):
            if j + d < m:
                sacc -= U[j][d] * mu[j + d]
        mu[j] = sacc / U[j][0]
    r = list(g)
    for j in range(m):
        r[j] += -mu[j]
        r[j + 1] += c[j] * mu[j]
        r[j + 2] += -2 * mu[j]
    return lg(max(abs(v) for v in r)), mu


def lg(v):
    return float(mp.log10(v)) if v != 0 else float("-inf")


out = {}
fk, _ = fgrad(xk)
out["kkt_point_objective_40"] = mp.nstr(fk, 40)
out["kkt_point_log10_max_row"] = lg(max(abs(v) for v in rows(xk)))
out["kkt_point_log10_stat_plus"] = lg(stat(xk, lam, 1))
out["kkt_point_log10_stat_minus"] = lg(stat(xk, lam, -1))

# exactly feasible point x*: seeds from the seed file, rows solved forward at 2400 digits
seeds = {}
for line in open(TRACK + "/points/lukvle10_seed.txt"):
    if line.startswith("#") or not line.strip():
        continue
    k, v = line.split()
    seeds[k] = mpf(v)  # 640 decimals, exact at 2400 digits
xs = [seeds["x1"], seeds["x2"]] + [None] * (n - 2)
for j in range(m):
    xs[j + 2] = (1 - xs[j] + 3 * xs[j + 1] - 2 * xs[j + 1] ** 2) / 2
dev = [abs(xs[k] - xk[k]) for k in range(n)]
out["xstar_log10_max_dev_from_kkt"] = lg(max(dev))
out["xstar_log10_dev_first_last"] = [lg(dev[2]) if dev[2] else None, lg(dev[-1])]
s = 1 if out["kkt_point_log10_stat_plus"] < out["kkt_point_log10_stat_minus"] else -1
out["xstar_log10_stat_with_stored_lam"] = lg(stat(xs, lam, s))
fs, _ = fgrad(xs)
out["xstar_objective_45"] = mp.nstr(fs, 45)
rk, muk = lsq_res(xk)
out["kkt_point_log10_stat_lsq"] = rk
out["kkt_point_lsq_mu_vs_stored_lam_log10_maxdiff"] = lg(max(abs(muk[j] - s * lam[j]) for j in range(m)))
rs, mus = lsq_res(xs)
out["xstar_log10_stat_lsq"] = rs
out["lam_min_max"] = [mp.nstr(min(lam), 8), mp.nstr(max(lam), 8)]
out["seconds"] = round(time.time() - T0, 1)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "kkt_lukvle10.json"), "w"), indent=1)
