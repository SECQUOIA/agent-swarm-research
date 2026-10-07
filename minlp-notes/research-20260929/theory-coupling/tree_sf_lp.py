"""Check of Theorem 2.2 (tree Shapley-Folkman) on finite-domain path problems.

Path x_1..x_n, each x_i in a grid of d values, bags {x_i, x_{i+1}} (width 1),
random pairwise bag costs, k random dense linear rows sum_i A_ji x_i = b_j
with b = A (average of two random configurations) so that the relaxation is
feasible. The coupling dual equals the LP over locally consistent bag
marginals plus the k moment rows (Theorem 2.1). HiGHS dual simplex returns a
basic (extreme) optimal solution. We count fractional components and compare
with k, and compute OPT by brute force for the gap.

Usage: python3 tree_sf_lp.py
"""
import itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix


def solve(n, d, k, rng, penalty=0.0, mode='mid'):
    grid = np.linspace(0, 1, d)
    nb = n - 1
    cost = rng.normal(size=(nb, d, d))
    if penalty:
        cost += penalty * (grid[:, None] - grid[None, :]) ** 2
    A = rng.normal(size=(k, n))
    z1 = rng.integers(0, d, n)
    z2 = rng.integers(0, d, n)
    b = A @ ((grid[z1] + grid[z2]) / 2) if mode == 'mid' else A @ grid[z1]
    nv = nb * d * d
    idx = lambda t, a, c: t * d * d + a * d + c
    rows, rhs = [], []
    M = lil_matrix((nb + (nb - 1) * d + k, nv))
    r = 0
    for t in range(nb):  # normalization
        for a in range(d):
            for c in range(d):
                M[r, idx(t, a, c)] = 1
        rhs.append(1); r += 1
    for t in range(nb - 1):  # marginal of x_{t+1} agrees between bags t, t+1
        for v in range(d):
            for a in range(d):
                M[r, idx(t, a, v)] += 1
            for c in range(d):
                M[r, idx(t + 1, v, c)] -= 1
            rhs.append(0); r += 1
    for j in range(k):  # moment rows; coefficient of x_i assigned to one bag
        for t in range(nb):
            for a in range(d):
                for c in range(d):
                    val = A[j, t] * grid[a]
                    if t == nb - 1:
                        val += A[j, t + 1] * grid[c]
                    M[r, idx(t, a, c)] = val
        rhs.append(b[j]); r += 1
    res = linprog(cost.reshape(-1), A_eq=M.tocsr(), b_eq=np.array(rhs),
                  bounds=(0, None), method="highs-ds")
    mu = res.x.reshape(nb, d, d)
    frac = [np.max(mu[t]) < 1 - 1e-7 for t in range(nb)]
    # separator between bag t and t+1 is x_{t+1}; its marginal from bag t
    comps, cur, sizes = 0, False, []
    for t in range(nb):
        if not frac[t]:
            cur = False
            continue
        if cur and t > 0:
            marg = mu[t - 1].sum(axis=0)
            if np.max(marg) < 1 - 1e-7:
                sizes[-1] += 1
                continue  # same component
        comps += 1
        sizes.append(1)
        cur = True
    # OPT by brute force
    best = np.inf
    for z in itertools.product(range(d), repeat=n):
        x = grid[list(z)]
        if np.max(np.abs(A @ x - b)) < 1e-9:
            best = min(best, sum(cost[t, z[t], z[t + 1]] for t in range(nb)))
    return res.fun, best, comps, max(sizes, default=0)


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    print("mode n d k penalty | trials | max components | viol(comps>k) | mean largest component (bags) | mean gap over finite")
    for mode in ["mid", "feas"]:
     for (n, d, k, pen) in [(8, 3, 1, 0.0), (8, 3, 2, 0.0), (8, 3, 3, 0.0), (7, 4, 2, 0.0),
                           (8, 3, 1, 20.0), (8, 3, 2, 20.0)]:
        comps, fracs, gaps, viol = [], [], [], 0
        for trial in range(30):
            D, opt, q, nf = solve(n, d, k, rng, pen, mode)
            comps.append(q); fracs.append(nf); gaps.append(opt - D)
            viol += q > k
        fin = [g for g in gaps if np.isfinite(g)]
        print(f"{mode} {n} {d} {k} {pen:5.1f} | 30 | {max(comps)} | {viol} | {np.mean(fracs):.2f} | "
              f"{np.mean(fin) if fin else float('nan'):.3f} ({len(fin)} finite)")
