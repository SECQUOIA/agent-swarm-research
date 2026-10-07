"""lukvle10: Lagrangian decomposition into 500 independent pair problems.
Numerical (non-rigorous) exploration helpers: KKT multipliers and grid estimates."""
import numpy as np
from osil_eval import load

n = 1000

def fpair(a, b):
    return (a * a) ** (b * b + 1) + (b * b) ** (a * a + 1)

def grad_pair(a, b):
    A = a * a; B = b * b
    t1 = A ** (B + 1); t2 = B ** (A + 1)
    da = (B + 1) * 2 * a * A ** B + t2 * np.log(np.maximum(B, 1e-300)) * 2 * a
    db = (A + 1) * 2 * b * B ** A + t1 * np.log(np.maximum(A, 1e-300)) * 2 * b
    return da, db

def load_sol(fname):
    I = load("lukvle10"); idx = {nm: j for j, nm in enumerate(I["names"])}
    x = np.zeros(n)
    for line in open(fname):
        p = line.split()
        if len(p) >= 2 and p[0] in idx:
            x[idx[p[0]]] = float(p[1])
    return x

def objective(x):
    return sum(fpair(x[2 * i], x[2 * i + 1]) for i in range(500))

def kkt_multipliers(x):
    g = np.zeros(n)
    for i in range(500):
        g[2 * i], g[2 * i + 1] = grad_pair(x[2 * i], x[2 * i + 1])
    J = np.zeros((998, n))
    for j in range(998):
        J[j, j] = -1; J[j, j + 1] = 3 - 4 * x[j + 1]; J[j, j + 2] = -2
    lam = np.linalg.lstsq(J.T, -g, rcond=None)[0]
    return lam, np.abs(J.T @ lam + g).max()

def pair_coeffs(lam):
    """L = sum_i [f(a_i,b_i) + beta_a a + quad_a a^2 + beta_b b + quad_b b^2] + sum(lam);
    constraint j (0-based): -x_j + 3x_{j+1} - 2x_{j+2} - 2x_{j+1}^2 + 1 = 0."""
    beta = np.zeros(n); quad = np.zeros(n)
    for j in range(998):
        beta[j] += -lam[j]; beta[j + 1] += 3 * lam[j]; beta[j + 2] += -2 * lam[j]; quad[j + 1] += -2 * lam[j]
    return beta, quad, lam.sum()

def grid_dual(lam, grid, x=None):
    beta, quad, const = pair_coeffs(lam)
    A, B = np.meshgrid(grid, grid, indexing="ij")
    F = fpair(A, B)
    tot = const; mins = []; argm = []
    for i in range(500):
        val = F + beta[2 * i] * A + quad[2 * i] * A * A + beta[2 * i + 1] * B + quad[2 * i + 1] * B * B
        k = np.unravel_index(np.argmin(val), val.shape)
        mins.append(val[k]); argm.append((grid[k[0]], grid[k[1]]))
    return const + sum(mins), np.array(mins), np.array(argm)
