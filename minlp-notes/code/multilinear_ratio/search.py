"""Search for x maximizing tbtgap(x)/chgap(x).

Theory used (see README): with tbt_l(x) = min{sum_t a_t y_t : y_t >= 0, y_t >= sum_{j in t} x_j - |t| + 1},
K*chgap - tbtgap = (K-1) cav - K vex + tbt_l is a concave function minimized over the polytope
P = {(x,y): 0<=x<=1, y_t >= 0, y_t >= sum_{j in t} x_j - |t| + 1}, so sup ratio is attained at the
x-projection of a vertex of P, i.e. at a point x uniquely determined by tight constraints
x_j in {0,1} and sum_{j in t} x_j = |t| - 1.  `arrangement_vertices` enumerates these exactly for
small instances; `multistart` is the heuristic used for larger ones.
"""
from __future__ import annotations

from fractions import Fraction
import itertools
import math

import numpy as np
from scipy.optimize import minimize


def grid_search(f, values, rng, max_points=20000):
    """Evaluate ratio on x with coordinates in `values` (all, or a random sample)."""
    vals = np.array(values, float)
    total = len(vals) ** f.n
    best = (-1.0, None)
    if total <= max_points:
        it = (np.array(p) for p in itertools.product(vals, repeat=f.n))
    else:
        it = (vals[rng.integers(0, len(vals), f.n)] for _ in range(max_points))
    for x in it:
        r = f.ratio(x)
        if r > best[0]:
            best = (r, x.copy())
    return best


def snap(f, x, max_den=12):
    """Round coordinates to fractions with denominator <= max_den; keep if ratio not worse."""
    xr = np.array([float(Fraction(v).limit_denominator(max_den)) for v in x])
    return (f.ratio(xr), xr) if f.ratio(xr) >= f.ratio(x) - 1e-9 else (f.ratio(x), x)


def local_refine(f, x0, iters=400):
    def obj(z):
        x = np.clip(z, 0.0, 1.0)
        r = f.ratio(x)
        return -r if np.isfinite(r) else 0.0

    res = minimize(obj, x0, method="Nelder-Mead",
                   options={"maxfev": iters * f.n, "xatol": 1e-7, "fatol": 1e-10, "initial_simplex": None})
    x = np.clip(res.x, 0, 1)
    return f.ratio(x), x


def multistart(f, rng, n_starts=30, grid_values=(0, 1/3, 1/2, 2/3, 3/4, 1), grid_points=3000, verbose=False):
    """Grid seeds + random seeds, Nelder-Mead refinement, rational snapping. Returns (ratio, x)."""
    seeds = []
    r, x = grid_search(f, grid_values, rng, max_points=grid_points)
    seeds.append(x)
    for _ in range(n_starts):
        kind = rng.integers(0, 3)
        if kind == 0:
            seeds.append(rng.random(f.n))
        elif kind == 1:
            seeds.append(np.array(grid_values)[rng.integers(0, len(grid_values), f.n)])
        else:  # perturbation of the best grid point
            seeds.append(np.clip(x + 0.15 * rng.standard_normal(f.n), 0, 1))
    best = (r, x)
    for s in seeds:
        r, x = local_refine(f, s)
        r, x = snap(f, x)
        if r > best[0] + 1e-12:
            best = (r, x)
            if verbose:
                print(f"  new best {r:.6f} at {np.round(x, 4)}")
    return best


def optimize_coefs(f, rng, n_rounds=3, n_starts=10):
    """Alternate: maximize over x (multistart), then jointly over (x, log a) with Nelder-Mead."""
    from families import with_coefs

    g = f
    best_r, best_x = multistart(g, rng, n_starts=n_starts)
    m = len(g.terms)
    for _ in range(n_rounds):
        z0 = np.concatenate([best_x, np.log([a for a, _ in g.terms])])

        def obj(z):
            x = np.clip(z[:g.n], 0, 1)
            h = with_coefs(g, np.exp(np.clip(z[g.n:], -6, 6)))
            r = h.ratio(x)
            return -r if np.isfinite(r) else 0.0

        res = minimize(obj, z0, method="Nelder-Mead", options={"maxfev": 300 * (g.n + m), "xatol": 1e-7, "fatol": 1e-10})
        x = np.clip(res.x[:g.n], 0, 1)
        h = with_coefs(g, np.exp(np.clip(res.x[g.n:], -6, 6)))
        r = h.ratio(x)
        if r > best_r + 1e-9:
            best_r, best_x, g = r, x, h
        r2, x2 = multistart(g, rng, n_starts=n_starts)
        if r2 > best_r + 1e-9:
            best_r, best_x = r2, x2
    return best_r, best_x, g


def arrangement_vertices(f, budget=5_000_000, tol=1e-9):
    """Exact candidate set: all x in [0,1]^n determined by tight constraints x_j in {0,1},
    sum_{j in t} x_j = |t|-1.  Returns list of x (numpy) or None if the enumeration exceeds `budget`."""
    n = f.n
    terms = [t for _, t in f.terms]
    pts = {}
    work = 0
    for m in range(0, n + 1):
        for F in itertools.combinations(range(n), m):
            Fs = set(F)
            outside = [j for j in range(n) if j not in Fs]
            # distinct patterns S = t cap F with |S| >= 2, and the outside parts realizing each pattern
            patt = {}
            for t in terms:
                S = tuple(j for j in t if j in Fs)
                if len(S) >= 2:
                    patt.setdefault(S, []).append(frozenset(t) - Fs)
            pat_list = list(patt)
            if m == 0:
                for bits in itertools.product((0.0, 1.0), repeat=n):
                    pts[bits] = np.array(bits)
                continue
            if len(pat_list) < m:
                continue
            cnt = math.comb(len(pat_list), m)
            work += cnt
            if work > budget:
                return None
            idx = {j: i for i, j in enumerate(F)}
            rows = np.zeros((len(pat_list), m))
            rhs = np.array([len(S) - 1.0 for S in pat_list])
            for i, S in enumerate(pat_list):
                rows[i, [idx[j] for j in S]] = 1.0
            sols = set()
            combs = np.array(list(itertools.combinations(range(len(pat_list)), m)), dtype=np.int32)
            for beg in range(0, len(combs), 200_000):
                C = combs[beg:beg + 200_000]
                A = rows[C]  # batch x m x m
                b = rhs[C]
                det = np.linalg.det(A)
                ok = np.abs(det) > 1e-9
                if not ok.any():
                    continue
                X = np.linalg.solve(A[ok], b[ok][..., None])[..., 0]
                inside = np.all((X > tol) & (X < 1 - tol), axis=1)
                for xF in X[inside]:
                    sols.add(tuple(np.round(xF, 10)))
            # each F-solution: choose B_0 among outside coordinates (rest -> 1) such that the tight
            # patterns realised by a term avoiding B_0 still determine x_F uniquely
            for xF in sols:
                xF = np.array(xF)
                tight = [i for i, S in enumerate(pat_list) if abs(rows[i] @ xF - rhs[i]) < 1e-7]
                for r0 in range(len(outside) + 1):
                    for B0 in itertools.combinations(outside, r0):
                        B0s = frozenset(B0)
                        ok_rows = [rows[i] for i in tight if any(not (o & B0s) for o in patt[pat_list[i]])]
                        if len(ok_rows) >= m and np.linalg.matrix_rank(np.array(ok_rows)) == m:
                            x = np.ones(n)
                            x[list(B0)] = 0.0
                            x[list(F)] = xF
                            pts[tuple(np.round(x, 10))] = x
    return list(pts.values())


def exact_max(f, budget=5_000_000):
    """Max ratio over the exact candidate set (None if enumeration too large)."""
    cands = arrangement_vertices(f, budget=budget)
    if cands is None:
        return None
    best = (-1.0, None)
    for x in cands:
        r = f.ratio(x)
        if r > best[0]:
            best = (r, x)
    return best[0], best[1], len(cands)
