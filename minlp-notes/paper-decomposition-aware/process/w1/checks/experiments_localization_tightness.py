"""Exact check of the localization lower bound (separable quadratic, uniform grid).

F(x) = g * sum_i (x_i - c_i)^2 on [-1,1]^n, curvature bound L >= 2g, kappa = L/g.
Grid: G_i = (c_i + hZ) cap [-1,1] plus the endpoints. For U = F* = 0 the
filter retains every interval with an endpoint v satisfying
g (v - c_i)^2 - (L/8) w_i(v)^2 + sum_{k != i} min q_k <= 0.
Claim: every node v with |v - c_i| <= h*sqrt(n*kappa/8) whose adjacent
intervals have length h passes, so the retained hull has radius >= that.
Part 2 runs the unchanged solver from the optimizer with uniform filtered
grids and compares the measured retained radius with h*sqrt(n*kappa/8).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import math
import sys
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver'))


def grid(c, h):
    k_lo = math.ceil((-1 - c) / h)
    k_hi = math.floor((1 - c) / h)
    nodes = sorted({F(-1), F(1)} | {c + k * h for k in range(k_lo, k_hi + 1)})
    w = []
    for k, v in enumerate(nodes):
        adj = ([v - nodes[k - 1]] if k else []) + ([nodes[k + 1] - v] if k + 1 < len(nodes) else [])
        w.append(max(adj))
    return nodes, w


def retained_radius(n, g, L, h, c=F(0)):
    nodes, w = grid(c, h)
    q = [g * (v - c) ** 2 - L * wi ** 2 / 8 for v, wi in zip(nodes, w)]
    qmin = min(q)
    others = (n - 1) * qmin
    m = [qi + others for qi in q]
    keep = [k for k in range(len(nodes) - 1) if min(m[k], m[k + 1]) <= 0]
    lo, hi = nodes[keep[0]], nodes[keep[-1] + 1]
    return max(c - lo, hi - c)


ok = True
for n, g, L, h in product((1, 2, 4, 8, 16, 64, 256, 1024), (F(1), F(1, 3)), (F(2), F(8), F(50)),
                          (F(1, 64), F(1, 512))):
    if L < 2 * g:
        continue
    kappa = L / g
    r = retained_radius(n, g, L, h)
    bound = h * math.sqrt(float(n * kappa) / 8)
    # The proposition claims r >= the largest multiple of h not exceeding the bound,
    # unless the retained hull reaches the box boundary.
    claim = min(h * math.floor(bound / float(h) + 1e-12), F(1))
    if r < claim:
        ok = False
        print('VIOLATION', n, g, L, h, float(r), bound)
print('separable exact check:', 'PASS' if ok else 'FAIL')

# Part 2: the unchanged solver, uniform filtered grids, warm start at the optimizer.
# A purely separable model is certified by the exact initial interval bound before
# any grid stage, so a weak path coupling 1/256 is added (kappa then slightly above 2).
from certified_grid import BoxQP, solve
for n in (4, 16, 64):
    c = F(1, 3)
    A = [[F(2) if i == j else (F(1, 256) if abs(i - j) == 1 else F(0)) for j in range(n)] for i in range(n)]
    b = [-sum(A[i][j] * c for j in range(n)) for i in range(n)]
    const = sum(A[i][j] * c * c for i in range(n) for j in range(n)) / 2
    p = BoxQP(A=A, b=b, bounds=[(-1, 1)] * n, integers=[], constant=const,
              bags=[(i, i + 1) for i in range(n - 1)], edges=[(i, i + 1) for i in range(n - 2)])
    cert = solve(p, epsilon=F(1, 2**60), max_stages=10, time_limit=60, max_table_states=10**6,
                 pruning=True, grid_mode='uniform', schedule='adaptive', slope_decay_period=0,
                 convex_presolve=False, warm_start=[c] * n)
    for st in cert['stages'][-3:]:
        h = F(st['h'])
        y = [F(v) for v in st['grid_point']]
        rad = max(max(abs(F(lo) - yi), abs(F(hi) - yi)) for (lo, hi), yi in zip(st['next_bounds'], y))
        print(f'solver n={n:3d} stage {st["stage"]:2d}: retained radius/h = {float(rad / h):5.2f}, '
              f'sqrt(n*kappa/8) with kappa=2: {math.sqrt(n * 2 / 8):5.2f}, nodes = {len(st["grids"][0])}')


# Part 3: exact-curvature pair construction. n = 2m, F = sum_k (L/2)(u_k^2+v_k^2) + beta u_k v_k
# on [-1,1]^n, uniform grid through 0 with spacing h. Claim: every node a with
# a^2 <= (n-1) kappa h^2 / 16 (kappa = 2L/(L-beta)) has m_{u_1}(a) <= 0 <= U.
def pair_check(m, L, beta, h):
    nodes, w = grid(F(0), h)
    idx = {v: k for k, v in enumerate(nodes)}
    def q(a, b):
        return L * (a * a + b * b) / 2 + beta * a * b - L * (w[idx[a]] ** 2 + w[idx[b]] ** 2) / 8
    qmin = min(q(a, b) for a in nodes for b in nodes)
    rows = {a: min(q(a, b) for b in nodes) + (m - 1) * qmin for a in nodes}
    kappa = 2 * L / (L - beta)
    n = 2 * m
    bad = [a for a in nodes if a * a <= (n - 1) * kappa * h * h / 16 and rows[a] > 0]
    retained = max(abs(a) for a in nodes if rows[a] <= 0)
    return bad, float(retained / h), math.sqrt(float((n - 1) * kappa) / 16)

ok = True
for m in (1, 2, 8, 32, 128):
    for L, beta in ((F(2), F(0)), (F(2), F(1)), (F(2), F(15, 8)), (F(4), F(63, 16))):
        bad, rad, pred = pair_check(m, L, beta, F(1, 128))
        if bad:
            ok = False
        print(f'pairs m={m:3d} kappa={float(2*L/(L-beta)):6.1f}: retained node radius/h={rad:6.1f} >= sqrt((n-1)kappa/16)={pred:6.2f}', 'OK' if not bad else f'VIOLATION {bad[:3]}')
print('pair exact-curvature check:', 'PASS' if ok else 'FAIL')
