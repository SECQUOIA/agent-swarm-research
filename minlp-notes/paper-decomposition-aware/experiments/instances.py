"""Exact rational instance families for the computational illustration.

The solver directory is located relative to this file
(../../research-20261002-decomposition/solver).

Planted family (continuous box [-1,1]^n, Hessian H = 2I + C sparse):
  * the interaction graph is a path, a random recursive tree, or a band;
  * a set A of about n/4 coordinates is active at x* (x*_i = +-1), the
    remaining set S is free (x*_i strictly inside);
  * H_SS = 2I + c W_SS has a controlled smallest eigenvalue, while entries
    touching A are large, so H is indefinite (the problem is nonconvex);
  * b is chosen so that grad F(x*) = l with l_S = 0, l_A = -mu x*_A, and the
    constant makes F* = F(x*) = 0.

For d = x - x*, F(x) - F* = mu sum_A |d_i| + d'Hd/2 >= d'(H + mu I_A)d/2,
because |d_i| <= 2 on [-1,1]. Hence g >= g_lb := lambda_min(H + mu I_A)/2;
g_lb is certified by an exact LDL' test. Moving along a rational vector v
supported on S gives the certified upper bound g <= g_ub := v'H_SS v/(2 v'v).
With L = 2 (every diagonal entry is 2), kappa = L/g lies in [2/g_ub, 2/g_lb].
"""
from __future__ import annotations

from fractions import Fraction as F
from random import Random
import sys
from pathlib import Path

import numpy as np

SOLVER = (Path(__file__).resolve().parents[2] / 'research-20261002-decomposition' / 'solver')
if str(SOLVER) not in sys.path:
    sys.path.insert(0, str(SOLVER))
from certified_grid import BoxQP  # noqa: E402


def graph_edges(kind: str, n: int, rng: Random):
    if kind == 'path':
        return [(i, i + 1) for i in range(n - 1)]
    if kind == 'tree':  # random recursive tree
        return [(rng.randrange(i), i) for i in range(1, n)]
    if kind.startswith('band'):
        w = int(kind[4:])
        return [(i, i + k) for k in range(1, w + 1) for i in range(n - k)]
    raise ValueError(kind)


def is_psd(matrix) -> bool:
    """Exact rational PSD test by symmetric elimination without pivoting."""
    m = [list(row) for row in matrix]
    n = len(m)
    for k in range(n):
        p = m[k][k]
        if p < 0:
            return False
        if p == 0:
            if any(m[i][k] != 0 for i in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            if m[i][k]:
                f = m[i][k] / p
                for j in range(k + 1, i + 1):
                    m[i][j] -= f * m[j][k]
                    m[j][i] = m[i][j]
    return True


def lam_min(matrix) -> float:
    a = np.array([[float(v) for v in row] for row in matrix])
    return float(np.linalg.eigvalsh(a)[0]) if len(a) else float('inf')


def planted(kind: str, n: int, kappa_target: float, seed: int,
            active_fraction: float = 0.25, growth_ratio: float = 0.9):
    """Return (BoxQP, info) for the planted nonconvex family described above."""
    rng = Random(seed)
    edges = graph_edges(kind, n, rng)
    n_active = max(1, round(active_fraction * n)) if n >= 2 else 0
    active = sorted(rng.sample(range(n), n_active))
    act = set(active)
    free = [i for i in range(n) if i not in act]
    xstar = [F(0)] * n
    for i in range(n):
        xstar[i] = F(rng.choice((-1, 1))) if i in act else F(rng.randint(-10, 10), 21)
    # Coupling pattern: W_SS entries in +-[1/2,1]; entries touching A in +-[2,4].
    w = {}
    for (i, j) in edges:
        sign = rng.choice((-1, 1))
        if i in act or j in act:
            w[i, j] = F(sign * rng.randint(8, 16), 4)
        else:
            w[i, j] = F(sign * rng.randint(4, 8), 8)
    pos = {i: k for k, i in enumerate(free)}
    wss = [[F(0)] * len(free) for _ in free]
    for (i, j), v in w.items():
        if i in pos and j in pos:
            wss[pos[i]][pos[j]] = wss[pos[j]][pos[i]] = v
    target_lmin = F(4) / F(kappa_target).limit_denominator(10**6)  # lambda_min(H_SS)
    lw = lam_min(wss) if free else 0.0
    if lw < -1e-12 and target_lmin < 2:
        c = F(int((2 - float(target_lmin)) / (-lw) * 4096), 4096)
    else:
        c = F(0)
    H = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = F(2)
    for (i, j), v in w.items():
        val = c * v if (i in pos and j in pos) else v
        H[i][j] = H[j][i] = val
    hss = [[H[i][j] for j in free] for i in free]
    # Certified upper bound on g from a rational approximate eigenvector of H_SS.
    if free:
        vals, vecs = np.linalg.eigh(np.array([[float(x) for x in r] for r in hss]))
        v = [F(float(x)).limit_denominator(10**6) for x in vecs[:, 0]]
        num = sum(v[a] * hss[a][b] * v[b] for a in range(len(free)) for b in range(len(free)))
        g_ub = num / (2 * sum(x * x for x in v))
    else:
        g_ub = None
    # Smallest half-integer mu with lambda_min(H + mu I_A)/2 >= growth_ratio * g_ub.
    target = growth_ratio * float(g_ub) if g_ub is not None else 0.5
    mu = F(1, 2)
    while True:
        Hm = [row[:] for row in H]
        for i in active:
            Hm[i][i] += mu
        if lam_min(Hm) / 2 >= target or mu > 10**4:
            break
        mu += F(1, 2)
    g_num = lam_min(Hm) / 2
    g_lb = F(int(g_num * 0.999 * 2**20), 2**20)
    shifted = [[Hm[i][j] - (2 * g_lb if i == j else 0) for j in range(n)] for i in range(n)]
    if g_lb <= 0 or not is_psd(shifted):
        raise ArithmeticError('growth certificate failed')
    ell = [F(0)] * n
    for i in active:
        ell[i] = -mu * xstar[i]
    b = [ell[i] - sum(H[i][j] * xstar[j] for j in range(n)) for i in range(n)]
    const = -(sum(b[i] * xstar[i] for i in range(n))
              + sum(H[i][j] * xstar[i] * xstar[j] for i in range(n) for j in range(n)) / 2)
    problem = BoxQP(A=H, b=b, bounds=[(F(-1), F(1))] * n, integers=[], constant=const,
                    name=f'planted_{kind}_n{n}_k{kappa_target}_s{seed}')
    if problem.value(tuple(xstar)) != 0:
        raise ArithmeticError('planted value is not zero')
    L = F(2)
    info = {'kind': kind, 'n': n, 'seed': seed, 'kappa_target': kappa_target,
            'active': active, 'xstar': [str(x) for x in xstar], 'fstar': '0',
            'mu': str(mu), 'coupling_scale': str(c), 'L': str(L),
            'g_lb': str(g_lb), 'g_ub': str(g_ub),
            'kappa_lb': float(L / g_ub), 'kappa_ub': float(L / g_lb),
            'nu': max(0.0, -lam_min(H)), 'lambda_min_H': lam_min(H),
            'max_bag_size': max(map(len, problem.bags)), 'edges': edges}
    return problem, info


def random_small(n: int, kind: str, n_int: int, seed: int):
    """Unplanted random mixed-integer nonconvex box QP for exact-output checks."""
    rng = Random(seed)
    edges = graph_edges(kind, n, rng)
    H = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = F(rng.randint(-8, 8), rng.choice((2, 3, 4)))
    for (i, j) in edges:
        H[i][j] = H[j][i] = F(rng.choice((-1, 1)) * rng.randint(1, 8), rng.choice((2, 3, 4)))
    b = [F(rng.randint(-6, 6), rng.choice((1, 2, 3, 5))) for _ in range(n)]
    ints = sorted(rng.sample(range(n), n_int))
    bounds = []
    for i in range(n):
        if i in ints:
            lo = rng.randint(-2, 0)
            bounds.append((F(lo), F(lo + rng.randint(1, 3))))
        else:
            lo = F(rng.randint(-3, 0), rng.choice((1, 2, 3)))
            bounds.append((lo, lo + F(rng.randint(1, 4), rng.choice((1, 2)))))
    return BoxQP(A=H, b=b, bounds=bounds, integers=ints, name=f'random_{kind}_n{n}_s{seed}')


def tied_isolated(seed: int):
    """Two isolated global minimizers (an integer sign tie); growth holds toward the set."""
    a = F(1 + seed % 3)
    # F = a(x0-1/3)^2 + (x1-x0/2)^2 - x2^2/2 + (x3-1/5)^2 + (x3-x4)^2/4,
    # x2 integer in [-1,1]: minimizers (1/3,1/6,+-1,1/5,1/5), value -1/2.
    H = [[2 * a + F(1, 2), F(-1), 0, 0, 0], [F(-1), F(2), 0, 0, 0], [0, 0, F(-1), 0, 0],
         [0, 0, 0, F(5, 2), F(-1, 2)], [0, 0, 0, F(-1, 2), F(1, 2)]]
    b = [-2 * a / 3, F(0), F(0), F(-2, 5), F(0)]
    const = a / 9 + F(1, 25)
    return BoxQP(A=H, b=b, bounds=[(0, 1), (-1, 1), (-1, 1), (-1, 1), (-1, 1)], integers=[2],
                 constant=const, name=f'tied_isolated_s{seed}')


def flat_segment(seed: int):
    """A continuous segment of global minimizers: no growth toward any single point."""
    a = F(1 + seed % 3)
    # F = a(x0 - x1)^2 + (x2 - 1/3)^2 - x3^2/2, x3 integer in [-1,1]:
    # minimizers x0 = x1 in [0,1], x2 = 1/3, x3 = +-1; value -1/2.
    H = [[2 * a, -2 * a, 0, 0], [-2 * a, 2 * a, 0, 0], [0, 0, 2, 0], [0, 0, 0, F(-1)]]
    b = [F(0), F(0), F(-2, 3), F(0)]
    return BoxQP(A=H, b=b, bounds=[(0, 1), (0, 1), (-1, 1), (-1, 1)], integers=[3],
                 constant=F(1, 9), name=f'flat_segment_s{seed}')


def random_continuous(kind: str, n: int, seed: int):
    """Unplanted random continuous box QP on [-1,1]^n (E6).

    Diagonal entries k/2 with k uniform in {-4,...,8}, interaction entries
    +-k/4 with k uniform in {1,...,6} on the edges of a path or band, linear
    entries k/4 with k uniform in {-8,...,8}. Nothing about the minimizer or
    the growth constant is prescribed.
    """
    rng = Random(seed)
    edges = graph_edges(kind, n, rng)
    H = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = F(rng.randint(-4, 8), 2)
    for (i, j) in edges:
        H[i][j] = H[j][i] = F(rng.choice((-1, 1)) * rng.randint(1, 6), 4)
    b = [F(rng.randint(-8, 8), 4) for _ in range(n)]
    return BoxQP(A=H, b=b, bounds=[(F(-1), F(1))] * n, integers=[],
                 name=f'random_continuous_{kind}_n{n}_s{seed}')
