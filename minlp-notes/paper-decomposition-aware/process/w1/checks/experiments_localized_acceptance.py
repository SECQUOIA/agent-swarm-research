"""Localized exact acceptance: a filtering history plus a local first/second-order test.

Rule (proved in experiments-proofs.tex): let the verified filtering history of
the last trial end with retained box B and incumbent value U; let xhat in B be
feasible with F(xhat) <= U; l = grad F(xhat); W = {i : beta_i < gamma_i}.
If, for i in W, (xhat_i interior to B_i and l_i = 0) or (xhat_i = beta_i and
l_i >= 0) or (xhat_i = gamma_i and l_i <= 0), and H_WW + 2 diag(|l_i|/w_i)
is PSD, then F(xhat) = F*. This script computes the first stage at which the
rule accepts on planted instances, versus the stages used by the height rule.
The candidate xhat is the exact stationary point of the face given by the
incumbent's original-bound coordinates (an untrusted proposal; all checks exact).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import json
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))
from instances import planted  # noqa: E402
from certified_grid import solve  # noqa: E402
from verify_certificate import verify_certificate  # noqa: E402


def is_psd(m):
    m = [list(r) for r in m]
    n = len(m)
    for k in range(n):
        p = m[k][k]
        if p < 0:
            return False
        if p == 0:
            if any(m[i][k] for i in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            if m[i][k]:
                f = m[i][k] / p
                for j in range(k + 1, i + 1):
                    m[i][j] -= f * m[j][k]
                    m[j][i] = m[i][j]
    return True


def solve_linear(M, r):
    n = len(M)
    rows = [list(M[i]) + [r[i]] for i in range(n)]
    for c in range(n):
        piv = next((k for k in range(c, n) if rows[k][c]), None)
        if piv is None:
            return None
        rows[c], rows[piv] = rows[piv], rows[c]
        p = rows[c][c]
        rows[c] = [v / p for v in rows[c]]
        for k in range(n):
            if k != c and rows[k][c]:
                f = rows[k][c]
                rows[k] = [a - f * b for a, b in zip(rows[k], rows[c])]
    return [rows[i][n] for i in range(n)]


def candidate(problem, point):
    n = len(point)
    H, b = problem.A, problem.b
    active = [i for i in range(n) if point[i] in problem.bounds[i] or i in problem.integers]
    free = [i for i in range(n) if i not in active]
    x = list(point)
    if free:
        sol = solve_linear([[H[i][j] for j in free] for i in free],
                           [-b[i] - sum(H[i][j] * x[j] for j in active) for i in free])
        if sol is None:
            return None
        for i, v in zip(free, sol):
            x[i] = v
    return tuple(x) if problem.feasible(x) else None


def local_accept(problem, xhat, box, upper):
    if xhat is None or not all(lo <= v <= hi for v, (lo, hi) in zip(xhat, box)):
        return False
    if problem.value(xhat) > upper:
        return False
    n = len(xhat)
    H, b = problem.A, problem.b
    grad = [b[i] + sum(H[i][j] * xhat[j] for j in range(n)) for i in range(n)]
    W = [i for i in range(n) if box[i][0] < box[i][1]]
    mu = {}
    for i in W:
        lo, hi = box[i]
        if lo < xhat[i] < hi:
            if i in problem.integers:
                # integer step: l_i d_i >= -|l_i| |d_i| >= -|l_i| d_i^2
                mu[i] = -abs(grad[i])
                continue
            if grad[i] != 0:
                return False
            mu[i] = F(0)
        elif xhat[i] == lo and grad[i] >= 0:
            mu[i] = grad[i] / (hi - lo)
        elif xhat[i] == hi and grad[i] <= 0:
            mu[i] = -grad[i] / (hi - lo)
        elif i in problem.integers:
            mu[i] = -abs(grad[i])
        else:
            return False
    M = [[H[i][j] + (2 * mu[i] if i == j else 0) for j in W] for i in W]
    return is_psd(M)


from instances import random_small  # noqa: E402
from exact_output import solve_exact  # noqa: E402


def tightened_box(problem, st):
    """Hull of next_bounds, with integer labels v removed when m_i(v) > U.

    Valid because the grid rounding keeps Y_i = v for every point with x_i = v,
    so m_i(v) <= F(x) on that slice (conditional bound with a = b = v).
    """
    upper = F(st['upper'])
    box = []
    for i, (lo, hi) in enumerate(st['next_bounds']):
        lo, hi = F(lo), F(hi)
        if i in problem.integers:
            grid = [F(v) for v in st['grids'][i]]
            marg = [F(v) for v in st['min_marginals'][i]]
            # integers strictly between two grid nodes stay unless the interval is removed
            keep = []
            for k, v in enumerate(grid):
                if lo <= v <= hi and marg[k] <= upper:
                    keep.append(v)
            for k in range(len(grid) - 1):
                a, b = grid[k], grid[k + 1]
                if b - a >= 2 and lo <= a and b <= hi and min(marg[k], marg[k + 1]) <= upper:
                    keep.extend([a + 1, b - 1])
            if keep:
                lo, hi = min(keep), max(keep)
        elif problem.A[i][i] <= 0 and len(st['grids'][i]) == 2:
            # Coordinatewise concave: endpoint replacement does not increase F.
            # If one endpoint's node marginal exceeds U, every point of B is either
            # worse than U or dominated by a point with x_i at the other endpoint.
            (a, b), (ma, mb) = map(F, st['grids'][i]), map(F, st['min_marginals'][i])
            if ma > upper and mb <= upper:
                lo = hi = b
            elif mb > upper and ma <= upper:
                lo = hi = a
        box.append((lo, hi))
    return tuple(box)


def first_local_acceptance(problem, max_stages=60, tighten=True):
    cert = solve(problem, epsilon=F(1, 2**60), max_stages=max_stages, time_limit=60,
                 max_table_states=300000, convex_presolve=False)
    assert verify_certificate(cert, max_table_states=10**7)['valid']
    # stages whose history starts at the original box: those after the last restart
    for st in cert['stages']:
        box = (tightened_box(problem, st) if tighten else
               tuple((F(lo), F(hi)) for lo, hi in st['next_bounds']))
        inc = tuple(F(v) for v in st['incumbent'])
        xhat = candidate(problem, inc)
        if local_accept(problem, xhat, box, F(st['upper'])):
            full = tuple(problem.bounds)
            at_full_box = local_accept(problem, xhat, full, F(st['upper']))
            return st['stage'], xhat, at_full_box
    return None, None, None


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'random'
    rows = []
    if mode == 'planted':
        cases = [('path', 6, 4, 4100), ('tree', 6, 4, 4100), ('band2', 6, 4, 4100),
                 ('path', 16, 4, 101), ('path', 16, 256, 101)]
        for kind, n, kt, seed in cases:
            problem, info = planted(kind, n, kt, seed)
            stage, xhat, full = first_local_acceptance(problem, 12)
            print(json.dumps({'kind': kind, 'n': n, 'kappa': kt, 'first_stage': stage,
                              'planted': list(map(str, xhat)) == info['xstar'] if xhat else None,
                              'accepted_on_full_box': full}))
    else:
        seed = 7000
        for n in (4, 6, 8, 12, 16):
            for kind in ('path', 'tree', 'band2'):
                for rep in range(2):
                    seed += 1
                    problem = random_small(n, kind, 1 + (n >= 8), seed)
                    t0 = time.perf_counter()
                    stage0, _, _ = first_local_acceptance(problem, tighten=False)
                    stage, xhat, full = first_local_acceptance(problem)
                    t_local = time.perf_counter() - t0
                    t0 = time.perf_counter()
                    ex = solve_exact(problem, time_limit=30, max_rounds=12, max_stages=3000,
                                     max_table_states=300000)
                    t_exact = time.perf_counter() - t0
                    agree = (ex['status'] == 'exact' and xhat is not None
                             and problem.value(xhat) == F(ex['upper']))
                    row = {'kind': kind, 'n': n, 'seed': seed, 'n_int': len(problem.integers),
                           'local_first_stage_interval_filter_only': stage0,
                           'local_first_stage': stage,
                           'local_accepted_on_full_box': full,
                           'height_rule_status': ex['status'],
                           'height_rule_stages': ex['stats']['completed_stages'],
                           'height_rule_rounds': ex['stats']['rounds'],
                           'values_agree': agree if stage is not None else None,
                           't_local_60_stages_s': round(t_local, 2), 't_exact_s': round(t_exact, 2)}
                    rows.append(row)
                    print(json.dumps(row), flush=True)
        acc = [r for r in rows if r['local_first_stage'] is not None]
        print('accepted', len(acc), 'of', len(rows), '; disagreements',
              sum(1 for r in acc if r['values_agree'] is False))


def diagnose(problem, max_stages=60):
    cert = solve(problem, epsilon=F(1, 2**60), max_stages=max_stages, time_limit=60,
                 max_table_states=300000, convex_presolve=False)
    st = cert['stages'][-1]
    box = tightened_box(problem, st)
    inc = tuple(F(v) for v in st['incumbent'])
    xhat = candidate(problem, inc)
    n = len(inc)
    H, b = problem.A, problem.b
    out = {'gap': float(F(cert['gap'])), 'xhat_is_none': xhat is None}
    if xhat is None:
        return out
    grad = [b[i] + sum(H[i][j] * xhat[j] for j in range(n)) for i in range(n)]
    out['coords'] = [(i, 'int' if i in problem.integers else 'cont', float(xhat[i]),
                      [float(box[i][0]), float(box[i][1])], float(grad[i]),
                      str(problem.bounds[i])) for i in range(n) if box[i][0] < box[i][1]]
    out['value_minus_upper'] = float(problem.value(xhat) - F(st['upper']))
    return out
