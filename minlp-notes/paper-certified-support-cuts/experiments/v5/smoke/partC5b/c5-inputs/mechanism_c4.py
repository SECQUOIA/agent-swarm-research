"""Part C4 (campaign-v4-protocol.md, Amendment 1): the path family with a binding coupling row.

Instances. C4 instance (n, seed), n in {10, 20, 40, 80}, seed in 5..9, is the C3 instance
``mechanism.instance(n, seed)`` with one change: the coupling row sum_i y_i <= 0.8 n becomes
sum_i y_i <= c, c = floor(64 * 0.5 * sum_i y_i*) / 64, where y_i* is the smallest minimizer in y
of copy i alone, i.e. the smallest midpoint (s + t) / 2 over the closest pairs s in A_i, t in C_i.
The instance is named interleaved_path_coupled_n{n}_s{seed}; all other data are unchanged.

Copy i and phi_i. For fixed y, D_i is separable in x and z and concave in each (coefficients
p^2 - 1 < 0 of x^2 and q^2 - 1 < 0 of z^2, no x z term), so its minimum over [0, 1]^2 is at a
vertex, where D_i(x, y, z) = (y - s)^2 + (y - t)^2 with s = A_i[x], t = C_i[z]. Hence
    phi_i(y) = min_{x, z} D_i = min_{(s, t) in A_i x C_i} q_st(y),
    q_st(y) = 2 (y - m)^2 + e,  m = (s + t) / 2,  e = (s - t)^2 / 2.
``identity_check`` verifies this from the case row: the concavity coefficients, the polynomial
identity D_i(vertex, y) = q_st(y) in exact arithmetic, and a numerical grid in (x, y, z).

Reference (i), the optimum of min sum_i phi_i(y_i) s.t. sum_i y_i <= c, 0 <= y <= 1. Convex
MIQP reformulation (perspective formulation of the disjunction, one binary per pair (s, t)):
    y_i = sum_k w_ik, 0 <= w_ik <= b_ik, sum_k b_ik = 1, w_ik^2 <= r_ik b_ik, r_ik >= 0,
    minimize sum_ik 2 r_ik - 2 (s_k + t_k) w_ik + (s_k^2 + t_k^2) b_ik,
solved with Gurobi (GUROBI_ATTEMPTS: one thread, MIPGap 1e-9, MIPGapAbs 1e-12, first with
tightened tolerances, then with default tolerances if Gurobi does not return OPTIMAL). Gurobi's
binary assignment is solved exactly in rational arithmetic (fixed pairs: a separable convex QP
with one row, water-filling). Gurobi's own objective and bound carry its feasibility tolerances,
so the optimum is certified separately by an exact branch and bound on the Lagrangian bound of
reference (ii) (``certify``: branching on the pair choice of the copy that lies on a segment of
its envelope); the certified exact value is the reference optimum. Witness of the original C4
model: x_i, z_i the vertices of the chosen pair, y_i the exact solution rounded down to binary64
(bounds and coupling row hold exactly), t_i = D_i(x_i, y_i, z_i) rounded up to binary64 (rows
1..n hold exactly). It is checked with the archived independent primal check (snapshot
``cases.check_primal``).

Reference (ii), the best root bound of aggregated cuts on the blocks:
min sum_i conv(phi_i)(y_i) s.t. sum_i y_i <= c, 0 <= y <= 1. Its Lagrangian dual is
h(mu) = sum_i min_{y in [0,1]} (phi_i(y) + mu y) - mu c, because the minimum of a linear
function plus conv(phi_i) over [0, 1] equals that of phi_i; h is concave, exact rational for
rational mu, and strong duality holds (convex problem, Slater point). Bisection on mu in [0, 4]
by the sign of (sum of the smallest minimizers - c) keeps a maximizer in [lo, hi]; h(mid) is a
lower bound and h(mid) + n (hi - lo) / 2 an upper bound (every supergradient lies in [-c, n - c]).
The convex envelope of each phi_i is built explicitly (``envelope``, slope sweep of the conjugate,
mpmath at 60 digits; checked to touch phi_i, to be convex, and to be supported by affine
minorants of phi_i); it gives a primal point with sum_i y_i = c and value sum_i env_i(y_i), which
must agree with h(mid). Cross-check: lower convex hull of phi_i on the grid j / 2^14 (exact
integer arithmetic), compared with the envelope on the grid, and the bound recomputed with these
hulls (greedy by slope).

    mechanism_c4.py references --output c4-references.json [--only 10:5 ...] [--time-limit S]
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
import time

from mpmath import mp, mpf
import numpy as np

import mechanism

NS = mechanism.NS
SEEDS = (5, 6, 7, 8, 9)  # the 20 C3 instances
GRID = 2 ** 14
BISECTION_STEPS = 100
mp.dps = 60
TOL = mpf(10) ** -45
GUROBI_BASE = {"Threads": 1, "MIPGap": 1e-9, "MIPGapAbs": 1e-12, "Seed": 0, "OutputFlag": 0}
GUROBI_ATTEMPTS = ({**GUROBI_BASE, "FeasibilityTol": 1e-9, "OptimalityTol": 1e-9, "IntFeasTol": 1e-9,
                    "BarQCPConvTol": 1e-12, "NumericFocus": 3},
                   GUROBI_BASE)
CERTIFICATE_TOLERANCE = Q(1, 10 ** 20)
MAX_CERTIFICATE_NODES = 10000


def case_name(n, seed):
    return f"interleaved_path_coupled_n{n}_s{seed}"


# ---------------------------------------------------------------- instance data

def blocks(n, seed):
    """Per copy: (A, C, pairs) with pairs (s, t, x, z, m, e) in the order x, z = 00, 01, 10, 11."""
    out = []
    for a, c in mechanism.draw_triples(n, seed):
        pairs = [(s, t, x, z, (s + t) / 2, (s - t) ** 2 / 2) for x, s in enumerate(a) for z, t in enumerate(c)]
        out.append((a, c, pairs))
    return out


def smallest_minimizer(pairs):
    delta = min(abs(s - t) for s, t, *_ in pairs)
    return min(m for s, t, x, z, m, e in pairs if abs(s - t) == delta)


def coupling(data):
    """(y*, sum y*, c) with c = floor(64 * 0.5 * sum y*) / 64; the row must bind."""
    ystar = [smallest_minimizer(pairs) for _, _, pairs in data]
    total = sum(ystar, Q(0))
    capacity = Q(math.floor(64 * total / 2), 64)
    if not 0 <= capacity < total:
        raise AssertionError("coupling row does not bind")
    return ystar, total, capacity


def q(pair, y):
    *_, m, e = pair
    return 2 * (y - m) ** 2 + e


def phi(pairs, y):
    return min(q(p, y) for p in pairs)


def coupled_model(n, seed):
    """The C3 model with the coupling row bound replaced and the C4 name; plus the C3 records."""
    model, optimum, witness, records = mechanism.instance(n, seed)
    ystar, total, capacity = coupling(blocks(n, seed))
    row = model["rows"][-1]
    if row["lin"] != {4 * i + 1: 1.0 for i in range(n)} or row["ub"] != mechanism.binary64(Q(4 * n, 5)):
        raise AssertionError("last row is not the C3 coupling row")
    row["ub"] = mechanism.binary64(capacity)
    model["name"] = case_name(n, seed)
    return model, records, ystar, total, capacity


# ---------------------------------------------------------------- identity phi_i = min_{x,z} D_i

def row_polynomial(row, i):
    """Exact coefficients of D_i from case row i + 1 (decoded floats): lin, quad, constant."""
    index = {4 * i + k: v for k, v in enumerate("xyzt")}
    lin = {index[int(j)]: Q(c) for j, c in row["lin"].items()}
    quad = {}
    for j, k, c in row["quad"]:
        quad[(index[j], index[k])] = quad.get((index[j], index[k]), Q(0)) + Q(c)
    if lin.pop("t") != -1 or math.isfinite(row["lb"]) or set(lin) - set("xyz") or any("t" in key for key in quad):
        raise AssertionError(f"row {i + 1} is not D_i - t_i <= -constant")
    return lin, quad, -Q(row["ub"])


def evaluate_row(poly, x, y, z):
    lin, quad, constant = poly
    value = {"x": x, "y": y, "z": z}
    return (constant + sum(c * value[v] for v, c in lin.items())
            + sum(c * value[u] * value[v] for (u, v), c in quad.items()))


def identity_check(model, data):
    """phi_i(y) = min_{x,z in [0,1]} D_i(x, y, z) for every copy, from the case rows."""
    worst_grid, worst_vertex = 0.0, 0.0
    ys = np.linspace(0.0, 1.0, 65)
    xs = np.linspace(0.0, 1.0, 17)
    for i, (a, c, pairs) in enumerate(data):
        lin, quad, constant = poly = row_polynomial(model["rows"][i + 1], i)
        if not (quad.get(("x", "x"), 0) < 0 and quad.get(("z", "z"), 0) < 0
                and set(quad) <= {("x", "x"), ("y", "y"), ("z", "z"), ("x", "y"), ("y", "z")}):
            raise AssertionError(f"copy {i}: D_i is not concave in x and z separately")
        for s, t, x, z, m, e in pairs:  # polynomial identity in y at each vertex
            coefficients = [evaluate_row(poly, Q(x), Q(0), Q(z))]
            coefficients.append(evaluate_row(poly, Q(x), Q(1), Q(z)) - evaluate_row(poly, Q(x), Q(-1), Q(z)))
            coefficients[1] /= 2
            coefficients.append(evaluate_row(poly, Q(x), Q(1), Q(z)) - coefficients[0] - coefficients[1])
            if coefficients != [s * s + t * t, -2 * (s + t), Q(2)]:
                raise AssertionError(f"copy {i}: D_i at vertex ({x}, {z}) is not (y - s)^2 + (y - t)^2")
        f = lambda X, Y, Z: (float(constant) + float(lin.get("x", 0)) * X + float(lin.get("y", 0)) * Y
                             + float(lin.get("z", 0)) * Z + sum(float(cf) * {"x": X, "y": Y, "z": Z}[u]
                                                                * {"x": X, "y": Y, "z": Z}[v]
                                                                for (u, v), cf in quad.items()))
        X, Y, Z = np.meshgrid(xs, ys, xs, indexing="ij")
        values = f(X, Y, Z)
        reference = np.array([float(phi(pairs, Q(y))) for y in ys])
        grid_min = values.min(axis=(0, 2))
        vertex_min = np.minimum.reduce([f(float(x), ys, float(z)) for _, _, x, z, _, _ in pairs])
        worst_grid = max(worst_grid, float(np.max(reference - grid_min)))  # > 0 would contradict
        worst_vertex = max(worst_vertex, float(np.max(np.abs(vertex_min - reference))))
    if worst_grid > 1e-12 or worst_vertex > 1e-12:
        raise AssertionError(f"identity fails numerically: grid {worst_grid}, vertex {worst_vertex}")
    return {"passed": True, "copies": len(data),
            "exact": "x^2, z^2 coefficients negative, no x z term; D_i(vertex, y) = (y - s)^2 + (y - t)^2 as polynomials",
            "grid": "y in 65 points, (x, z) in 17 x 17 points of [0,1]^2",
            "max_phi_minus_grid_min": worst_grid, "max_abs_vertex_min_minus_phi": worst_vertex}


# ---------------------------------------------------------------- reference (ii)

def block_dual(pairs, mu):
    """min over y in [0,1] of phi(y) + mu y; value and smallest and largest minimizer (exact)."""
    best, points = None, []
    for p in pairs:
        y = min(max(p[4] - mu / 4, Q(0)), Q(1))
        value = q(p, y) + mu * y
        if best is None or value < best:
            best, points = value, [y]
        elif value == best:
            points.append(y)
    return best, min(points), max(points)


def dual_value(data, capacity, mu):
    return sum((block_dual(pairs, mu)[0] for _, _, pairs in data), Q(0)) - mu * capacity


def smallest_minimizers(data, mu):
    return [block_dual(pairs, mu)[1] for _, _, pairs in data]


def to_mpf(value):
    return mpf(value.numerator) / value.denominator


def envelope(pairs):
    """Convex envelope of phi = min_k q_k on [0, 1] as ordered pieces covering [0, 1].

    Slope sweep: psi_k(sigma) = min_{y in [0,1]} q_k(y) - sigma y and Psi = min_k psi_k
    (Psi(sigma) = -phi*(sigma)). Between consecutive candidate slopes (regime boundaries of each
    psi_k and all pairwise crossings of psi_k, psi_l, regime by regime) the minimizing k is
    constant; there the contact point clip(m_k + sigma / 4, 0, 1) moves along q_k (arc), and at
    a candidate slope where the contact point jumps the envelope is the segment of that slope.
    Pieces: ("arc", y0, y1, k) or ("segment", y0, y1, slope, value at y0).
    """
    par = [(to_mpf(p[4]), to_mpf(p[5])) for p in pairs]

    def regimes(m, e):
        lo, hi = -4 * m, 4 * (1 - m)
        return [(mpf("-inf"), lo, (2 * m * m + e, mpf(0), mpf(0))), (lo, hi, (e, -m, mpf(-1) / 8)),
                (hi, mpf("inf"), (2 * (1 - m) ** 2 + e, mpf(-1), mpf(0)))]

    def contact(k, sigma):
        if sigma == mpf("-inf"):
            return mpf(0)
        if sigma == mpf("inf"):
            return mpf(1)
        return min(max(par[k][0] + sigma / 4, mpf(0)), mpf(1))

    def psi(k, sigma):
        y = contact(k, sigma)
        return 2 * (y - par[k][0]) ** 2 + par[k][1] - sigma * y

    candidates = []
    for k, (m, e) in enumerate(par):
        candidates += [-4 * m, 4 * (1 - m)]
        for l in range(k + 1, len(par)):
            for lo_k, hi_k, ck in regimes(m, e):
                for lo_l, hi_l, cl in regimes(*par[l]):
                    lo, hi = max(lo_k, lo_l), min(hi_k, hi_l)
                    if lo >= hi:
                        continue
                    d0, d1, d2 = (u - v for u, v in zip(ck, cl))
                    if d2 == 0:
                        roots = [] if d1 == 0 else [-d0 / d1]
                    else:
                        disc = d1 * d1 - 4 * d2 * d0
                        roots = [] if disc < 0 else [(-d1 + r) / (2 * d2) for r in {mp.sqrt(disc), -mp.sqrt(disc)}]
                    candidates += [r for r in roots if lo - TOL <= r <= hi + TOL]
    candidates.sort()
    slopes = []
    for s in candidates:
        if not slopes or s - slopes[-1] > TOL:
            slopes.append(s)
    bounds = [mpf("-inf")] + slopes + [mpf("inf")]
    active = []
    for left, right in zip(bounds[:-1], bounds[1:]):
        probe = (left + right) / 2 if math.isfinite(left) and math.isfinite(right) else (
            right - 1 if math.isfinite(right) else left + 1)
        values = [psi(k, probe) for k in range(len(par))]
        best = min(values)
        tied = [k for k, v in enumerate(values) if v - best <= TOL]
        if max(contact(k, probe) for k in tied) - min(contact(k, probe) for k in tied) > TOL:
            raise AssertionError("tie with distinct contact points inside a slope interval")
        active.append(tied[0])
    pieces = []
    for j, k in enumerate(active):
        y0, y1 = contact(k, bounds[j]), contact(k, bounds[j + 1])
        if y1 - y0 > TOL:
            pieces.append(("arc", y0, y1, k))
        if j + 1 < len(active):
            sigma, nxt = bounds[j + 1], active[j + 1]
            ya, yb = contact(k, sigma), contact(nxt, sigma)
            if yb - ya > TOL:
                pieces.append(("segment", ya, yb, sigma, 2 * (ya - par[k][0]) ** 2 + par[k][1]))
    merged = []
    for piece in pieces:  # adjacent arcs of the same parabola
        if merged and piece[0] == "arc" and merged[-1][0] == "arc" and merged[-1][3] == piece[3]:
            merged[-1] = ("arc", merged[-1][1], piece[2], piece[3])
        else:
            merged.append(piece)
    return {"pieces": merged, "parabolas": par, "Psi": lambda sigma: min(psi(k, sigma) for k in range(len(par)))}


def env_value(env, y):
    for piece in env["pieces"]:
        if piece[1] - TOL <= y <= piece[2] + TOL:
            if piece[0] == "arc":
                m, e = env["parabolas"][piece[3]]
                return 2 * (y - m) ** 2 + e
            return piece[4] + piece[3] * (y - piece[1])
    raise ValueError(f"{y} outside [0, 1]")


def envelope_check(env, pairs):
    """Pieces cover [0, 1] contiguously; env is continuous and convex; env = phi on arcs and at
    segment ends; the supporting line of every segment and at every arc point checked is an
    affine minorant of phi (intercept <= Psi(slope))."""
    pieces, par, Psi = env["pieces"], env["parabolas"], env["Psi"]
    phi_mp = lambda y: min(2 * (y - m) ** 2 + e for m, e in par)
    worst = mpf(0)
    if abs(pieces[0][1]) > TOL or abs(pieces[-1][2] - 1) > TOL:
        raise AssertionError("envelope does not cover [0, 1]")
    slopes = []
    for a, b in zip(pieces[:-1], pieces[1:]):
        worst = max(worst, abs(a[2] - b[1]))
    for piece in pieces:
        y0, y1 = piece[1], piece[2]
        if piece[0] == "arc":
            m, e = par[piece[3]]
            for y in (y0, (y0 + y1) / 2, y1):
                slope = 4 * (y - m)
                worst = max(worst, abs(phi_mp(y) - env_value(env, y)),
                            max(mpf(0), (env_value(env, y) - slope * y) - Psi(slope)))
            slopes += [4 * (y0 - m), 4 * (y1 - m)]
        else:
            slope, v0 = piece[3], piece[4]
            worst = max(worst, abs(phi_mp(y0) - v0), abs(phi_mp(y1) - (v0 + slope * (y1 - y0))),
                        max(mpf(0), (v0 - slope * y0) - Psi(slope)))
            slopes += [slope, slope]
    for a, b in zip(pieces[:-1], pieces[1:]):  # continuity at the joints
        left = env_value({"pieces": [a], "parabolas": par}, a[2])
        right = env_value({"pieces": [b], "parabolas": par}, b[1])
        worst = max(worst, abs(left - right))
    convex = all(s2 - s1 >= -TOL for s1, s2 in zip(slopes[:-1], slopes[1:]))
    if worst > mpf(10) ** -40 or not convex:
        raise AssertionError(f"envelope check failed: worst {worst}, convex {convex}")
    return float(worst)


def env_numpy(env, ys):
    out = np.full(ys.shape, np.nan)
    for piece in env["pieces"]:
        y0, y1 = float(piece[1]), float(piece[2])
        mask = (ys >= y0 - 1e-15) & (ys <= y1 + 1e-15)
        if piece[0] == "arc":
            m, e = (float(v) for v in env["parabolas"][piece[3]])
            out[mask] = 2 * (ys[mask] - m) ** 2 + e
        else:
            out[mask] = float(piece[4]) + float(piece[3]) * (ys[mask] - y0)
    return out


def grid_hull(pairs, grid=GRID):
    """Lower convex hull of (j/grid, phi(j/grid)) for grid = 2^14, in exact integers.

    With m = M/128 and e = E/8192 (s, t multiples of 1/64), phi(j/2^14) * 2^27 equals
    min_k (j - 128 M_k)^2 + 16384 E_k."""
    if grid != 2 ** 14:
        raise ValueError("the integer scaling assumes grid = 2^14")
    scale = 2 ** 27
    coefficients = []
    for *_, m, e in pairs:
        if (m * 128).denominator != 1 or (e * 8192).denominator != 1:
            raise AssertionError("pair data are not multiples of 1/128 and 1/8192")
        coefficients.append((int(m * 128), int(e * 8192)))
    xs = range(grid + 1)
    fs = [min((j - 128 * M) ** 2 + 16384 * E for M, E in coefficients) for j in xs]
    for j in (0, 1, grid // 3, grid):
        if Q(fs[j], scale) != phi(pairs, Q(j, grid)):
            raise AssertionError("integer grid values differ from phi")
    hull = []
    for p in zip(xs, fs):
        while len(hull) >= 2 and ((hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1])
                                  - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0])) <= 0:
            hull.pop()
        hull.append(p)
    return [(Q(x, grid), Q(f, scale)) for x, f in hull]


def grid_bound(hulls, capacity):
    """min sum_i hull_i(y_i) s.t. sum y_i <= c: greedy over hull segments by slope (convex PL)."""
    value = sum(h[0][1] for h in hulls)
    segments = sorted(((h[k + 1][1] - h[k][1]) / (h[k + 1][0] - h[k][0]), h[k + 1][0] - h[k][0])
                      for h in hulls for k in range(len(h) - 1))
    budget = capacity
    for slope, length in segments:
        if slope >= 0 or budget <= 0:
            break
        step = min(length, budget)
        value += slope * step
        budget -= step
    return value


def bisect_multiplier(data, capacity):
    """Bracket [lo, hi] of a maximizer of h; lower = h(mid), upper = lower + n (hi - lo) / 2; and a
    point with sum = c between the smallest minimizers for hi (sum <= c) and for lo (sum > c)."""
    lo, hi = Q(0), Q(4)
    if sum(smallest_minimizers(data, lo)) <= capacity:  # the row does not bind the relaxation
        hi = lo
    elif capacity < sum(smallest_minimizers(data, hi)):
        raise AssertionError("bisection interval does not bracket the multiplier")
    for _ in range(BISECTION_STEPS if hi > lo else 0):
        mid = (lo + hi) / 2
        if sum(smallest_minimizers(data, mid)) > capacity:
            lo = mid
        else:
            hi = mid
    mid = (lo + hi) / 2
    lower = dual_value(data, capacity, mid)
    y_hi, y_lo = smallest_minimizers(data, hi), smallest_minimizers(data, lo)
    deficit, point = capacity - sum(y_hi), []
    if hi == lo:  # mu = 0: the smallest minimizers are feasible
        deficit, y_lo = Q(0), y_hi
    for a, b in zip(y_hi, y_lo):
        step = min(deficit, b - a)
        point.append(a + step)
        deficit -= step
    if deficit != 0 or sum(point) > capacity or any(not 0 <= v <= 1 for v in point):
        raise AssertionError("primal point of the envelope problem not found")
    return {"lo": lo, "hi": hi, "mid": mid, "lower": lower, "upper": lower + len(data) * (hi - lo) / 2,
            "point": point}


def bound_ii(data, capacity, envelopes):
    result = bisect_multiplier(data, capacity)
    lo, hi, mid, lower, upper, point = (result[k] for k in ("lo", "hi", "mid", "lower", "upper", "point"))
    if sum(point) != capacity:
        raise AssertionError("the coupling row does not bind the envelope problem")
    primal = sum(env_value(env, to_mpf(v)) for env, v in zip(envelopes, point))
    if not (to_mpf(lower) - mpf(10) ** -40 <= primal <= to_mpf(upper) + mpf(10) ** -40):
        raise AssertionError("envelope primal value outside the dual enclosure")
    return {"value": float(lower), "lower_exact": str(lower), "upper_minus_lower": float(upper - lower),
            "mu": float(mid), "mu_bracket_width": float(hi - lo), "bisection_steps": BISECTION_STEPS,
            "envelope_primal_value": mp.nstr(primal, 40),
            "envelope_primal_minus_dual": float(primal - to_mpf(lower)),
            "fractional_copies": sum(any(p[0] == "segment" and p[1] + TOL < to_mpf(v) < p[2] - TOL
                                         for p in env["pieces"]) for env, v in zip(envelopes, point))}


# ---------------------------------------------------------------- reference (i)

def solve_miqp(data, capacity, time_limit):
    """Gurobi on the perspective MISOCP: the tightened settings first, the default tolerances if
    Gurobi does not return OPTIMAL (e.g. status 13, tolerances not met). Every attempt is kept."""
    attempts = []
    for params in GUROBI_ATTEMPTS:
        assignment, info = solve_miqp_once(data, capacity, time_limit, params)
        attempts.append({k: v for k, v in info.items() if k != "y"})
        if assignment is not None:
            return assignment, {**info, "attempts": attempts}
    raise RuntimeError(f"Gurobi did not return OPTIMAL: {attempts}")


def solve_miqp_once(data, capacity, time_limit, settings):
    import gurobipy as gp
    from gurobipy import GRB
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    try:
        g = gp.Model("c4_perspective", env=env)
        y = [g.addVar(lb=0.0, ub=1.0, name=f"y{i}") for i in range(len(data))]
        binaries, objective = [], gp.LinExpr()
        for i, (_, _, pairs) in enumerate(data):
            b = [g.addVar(vtype=GRB.BINARY, name=f"b{i}_{k}") for k in range(len(pairs))]
            w = [g.addVar(lb=0.0, ub=1.0, name=f"w{i}_{k}") for k in range(len(pairs))]
            r = [g.addVar(lb=0.0, ub=1.0, name=f"r{i}_{k}") for k in range(len(pairs))]
            g.addConstr(gp.quicksum(b) == 1)
            g.addConstr(y[i] == gp.quicksum(w))
            for k, (s, t, *_) in enumerate(pairs):
                g.addConstr(w[k] <= b[k])
                g.addQConstr(w[k] * w[k] <= r[k] * b[k])  # rotated cone: perspective of w^2
                objective += 2 * r[k] - float(2 * (s + t)) * w[k] + float(s * s + t * t) * b[k]
            binaries.append(b)
        g.addConstr(gp.quicksum(y) <= float(capacity))
        g.setObjective(objective, GRB.MINIMIZE)
        params = {**settings, "TimeLimit": float(time_limit)}
        for key, value in params.items():
            g.setParam(key, value)
        g.optimize()
        if g.Status != GRB.OPTIMAL:
            return None, {"status": g.Status, "runtime_seconds": g.Runtime, "nodes": g.NodeCount,
                          "objective": g.ObjVal if g.SolCount else None, "bound": g.ObjBound, "params": params}
        assignment = []
        for b in binaries:
            values = [v.X for v in b]
            k = max(range(len(values)), key=values.__getitem__)
            if values[k] < 0.5:
                raise RuntimeError("no binary at 1")
            assignment.append(k)
        return assignment, {
            "formulation": "perspective MISOCP (binary per pair (s, t); w^2 <= r b)",
            "status": "OPTIMAL", "objective": g.ObjVal, "bound": g.ObjBound, "mip_gap": g.MIPGap,
            "absolute_gap": g.ObjVal - g.ObjBound, "runtime_seconds": g.Runtime, "work": g.Work,
            "nodes": g.NodeCount, "params": params, "version": ".".join(map(str, gp.gurobi.version())),
            "y": [v.X for v in y]}
    finally:
        try:
            g.dispose()
        except NameError:
            pass
        env.dispose()


def exact_assignment_optimum(data, assignment, capacity):
    """For fixed pairs: min sum_i 2 (y_i - m_i)^2 + e_i s.t. sum y_i <= c, 0 <= y <= 1, exactly.

    y_i(lam) = max(m_i - lam / 4, 0) (m_i <= 3/4, so y_i < 1); lam = 0 if sum m_i <= c, else
    sum_i y_i(lam) = c on the segment of breakpoints 4 m_i that contains lam."""
    ms = [data[i][2][k][4] for i, k in enumerate(assignment)]
    lam = Q(0)
    if sum(ms) > capacity:
        order = sorted(ms, reverse=True)
        for j in range(1, len(order) + 1):
            lam = 4 * (sum(order[:j]) - capacity) / j
            if lam <= 4 * order[j - 1] and (j == len(order) or lam >= 4 * order[j]):
                break
        else:
            raise AssertionError("water-filling failed")
    ys = [max(m - lam / 4, Q(0)) for m in ms]
    if sum(ys) > capacity or any(y > 1 for y in ys):
        raise AssertionError("water-filling point infeasible")
    value = sum((q(data[i][2][k], y) for i, (k, y) in enumerate(zip(assignment, ys))), Q(0))
    return value, ys, lam


def improve(data, assignment, capacity):
    """Re-select the best pair at each y_i and re-solve until no pair changes (local check)."""
    switches = 0
    while True:
        value, ys, lam = exact_assignment_optimum(data, assignment, capacity)
        better = [min(range(4), key=lambda k: (q(data[i][2][k], y), k)) for i, y in enumerate(ys)]
        changed = [i for i, (k, b) in enumerate(zip(assignment, better)) if q(data[i][2][b], ys[i]) < q(data[i][2][k], ys[i])]
        if not changed:
            return value, ys, lam, assignment, switches
        assignment = [better[i] if i in changed else k for i, k in enumerate(assignment)]
        switches += len(changed)


def certify(data, capacity, value, assignment):
    """Exact branch and bound on the Lagrangian bound, independent of Gurobi's tolerances.

    A node allows a subset of the pairs of each copy; its lower bound is h(mid) of the restricted
    problem (``bisect_multiplier``), a valid bound for every assignment in the node. The point of
    the restricted envelope problem gives an incumbent (exact re-solve of its pairs). A node is
    closed when its bound is within CERTIFICATE_TOLERANCE of the incumbent or no copy is on a
    segment of its envelope (gap phi_i(y_i) + mu y_i - H_i(mu) at most the tolerance); otherwise
    it is split into one child per allowed pair of the copy with the largest gap. Returns the best
    value and assignment, the smallest bound over closed nodes and the node count."""
    best_value, best_assignment = value, assignment
    stack, closed_lower, nodes = [[list(range(4)) for _ in data]], None, 0
    while stack:
        allowed = stack.pop()
        nodes += 1
        if nodes > MAX_CERTIFICATE_NODES:
            raise RuntimeError("certificate node limit reached")
        restricted = [(a, c, [pairs[k] for k in allowed[i]]) for i, (a, c, pairs) in enumerate(data)]
        relaxation = bisect_multiplier(restricted, capacity)
        lower, mu, point = relaxation["lower"], relaxation["mid"], relaxation["point"]
        start = [min(allowed[i], key=lambda k: (q(data[i][2][k], y), k)) for i, y in enumerate(point)]
        candidate, _, _, candidate_assignment, _ = improve(data, start, capacity)
        if candidate < best_value:
            best_value, best_assignment = candidate, candidate_assignment
        gaps = [phi(r[2], y) + mu * y - block_dual(r[2], mu)[0] for r, y in zip(restricted, point)]
        if lower >= best_value - CERTIFICATE_TOLERANCE or max(gaps) <= CERTIFICATE_TOLERANCE:
            closed_lower = lower if closed_lower is None else min(closed_lower, lower)
            continue
        j = max(range(len(gaps)), key=gaps.__getitem__)
        for k in allowed[j]:
            stack.append([[k] if i == j else list(v) for i, v in enumerate(allowed)])
    return best_value, best_assignment, closed_lower, nodes


def round_down(value):
    f = float(value)
    return f if Q(f) <= value else math.nextafter(f, -math.inf)


def round_up(value):
    f = float(value)
    return f if Q(f) >= value else math.nextafter(f, math.inf)


def witness(model, data, assignment, ys):
    """Feasible point of the original C4 model: exact rows, binary64 values."""
    values = []
    for i, (k, y) in enumerate(zip(assignment, ys)):
        s, t, x, z, m, e = data[i][2][k]
        yf = round_down(y)
        d = evaluate_row(row_polynomial(model["rows"][i + 1], i), Q(x), Q(yf), Q(z))
        values += [float(x), yf, float(z), round_up(d)]
    if sum(Q(values[4 * i + 1]) for i in range(len(data))) > Q(model["rows"][-1]["ub"]):
        raise AssertionError("witness violates the coupling row")
    return values, sum((Q(values[4 * i + 3]) for i in range(len(data))), Q(0))


# ---------------------------------------------------------------- references and case

def snapshot_modules():
    import make_jobs
    make_jobs.snapshot_module_path()
    from run_campaign import exact_json
    from worker import load_model
    from cases import check_primal
    return exact_json, load_model, check_primal


def reference(n, seed, time_limit):
    exact_json, load_model, check_primal = snapshot_modules()
    started = time.perf_counter()
    data = blocks(n, seed)
    model, records, ystar, total, capacity = coupled_model(n, seed)
    decoded = load_model({"model": exact_json(model)})
    identity = identity_check({"rows": decoded.rows}, data)
    envelopes = [envelope(pairs) for _, _, pairs in data]
    envelope_residual = max(envelope_check(env, pairs) for env, (_, _, pairs) in zip(envelopes, data))
    ii = bound_ii(data, capacity, envelopes)
    hulls = [grid_hull(pairs) for _, _, pairs in data]
    ys_grid = np.arange(GRID + 1) / GRID
    hull_minus_env = []
    for hull, env, (_, _, pairs) in zip(hulls, envelopes, data):
        hx, hf = np.array([float(x) for x, _ in hull]), np.array([float(f) for _, f in hull])
        hull_minus_env.append(np.interp(ys_grid, hx, hf) - env_numpy(env, ys_grid))
    hull_minus_env = np.concatenate(hull_minus_env)
    gb = grid_bound(hulls, capacity)
    ii.update(envelope_pieces=[{"arcs": sum(p[0] == "arc" for p in env["pieces"]),
                                "segments": sum(p[0] == "segment" for p in env["pieces"])} for env in envelopes],
              envelope_check_max_residual=envelope_residual,
              grid_cross_check={"grid": f"j/{GRID}", "min_hull_minus_envelope": float(hull_minus_env.min()),
                                "max_hull_minus_envelope": float(hull_minus_env.max()),
                                "grid_bound": float(gb), "grid_bound_minus_bound": float(gb - Q(ii["lower_exact"]))})
    if not (-1e-12 <= ii["grid_cross_check"]["min_hull_minus_envelope"]
            and ii["grid_cross_check"]["max_hull_minus_envelope"] <= 1e-8
            and -1e-12 <= ii["grid_cross_check"]["grid_bound_minus_bound"] <= 1e-6):
        raise AssertionError(f"grid cross-check failed: {ii['grid_cross_check']}")
    reference_seconds = time.perf_counter() - started
    assignment, gurobi = solve_miqp(data, capacity, time_limit)
    gurobi_value, _, _, gurobi_assignment, switches = improve(data, assignment, capacity)
    certificate_started = time.perf_counter()
    optimum, final, certified_lower, nodes = certify(data, capacity, gurobi_value, gurobi_assignment)
    certificate = {"method": "exact branch and bound on the Lagrangian bound (certify)",
                   "lower_exact": str(certified_lower), "optimum_minus_lower": float(optimum - certified_lower),
                   "certified": optimum - certified_lower <= n * CERTIFICATE_TOLERANCE, "nodes": nodes,
                   "tolerance": str(CERTIFICATE_TOLERANCE),
                   "gurobi_assignment_value_minus_optimum": float(gurobi_value - optimum),
                   "seconds": time.perf_counter() - certificate_started}
    if not certificate["certified"]:
        raise AssertionError(f"optimum not certified: {certificate}")
    optimum, ys, lam = exact_assignment_optimum(data, final, capacity)
    values, witness_objective = witness(model, data, final, ys)
    instance = load_model({"model": exact_json(model)})
    check = check_primal(instance, values, float(optimum))
    if not check["passed"]:
        raise AssertionError(f"witness fails the primal check: {check}")
    lower = Q(ii["lower_exact"])
    return {
        "name": case_name(n, seed), "n": n, "seed": seed, "c3_name": mechanism.case_name(n, seed),
        "coupling": {"c": str(capacity), "c_binary64": float(capacity), "sum_y_star": str(total),
                     "y_star": [str(v) for v in ystar], "binds": capacity < total,
                     "replaced_ub": str(Q(4 * n, 5))},
        "identity_check": identity,
        "optimum": float(optimum), "optimum_exact": str(optimum),
        "optimum_source": "Gurobi assignment re-solved exactly, certified by exact branch and bound",
        "optimum_certificate": certificate,
        "gurobi": gurobi,
        "gurobi_objective_minus_exact": gurobi["objective"] - float(optimum),
        "exact_minus_gurobi_bound": float(optimum) - gurobi["bound"],
        "assignment": [{"s": str(data[i][2][k][0]), "t": str(data[i][2][k][1]), "x": data[i][2][k][2],
                        "z": data[i][2][k][3]} for i, k in enumerate(final)],
        "assignment_switches_after_gurobi": switches,
        "multiplier_exact": str(lam), "y_exact": [str(v) for v in ys],
        "witness": values, "witness_exact": [str(Q(v)) for v in values],
        "witness_objective_exact": str(witness_objective),
        "witness_objective_minus_optimum": float(witness_objective - optimum),
        "witness_primal_check": check,
        "bound_ii": ii, "optimum_minus_bound_ii": float(optimum - lower),
        "optimum_minus_bound_ii_exact": str(optimum - lower),
        "envelope_and_check_seconds": reference_seconds,
    }


def case(n, seed, exact_json, ref):
    """C4 case descriptor (campaign-v2 synthetic format) from the stored reference entry."""
    model, records, ystar, total, capacity = coupled_model(n, seed)
    if (ref["name"] != case_name(n, seed) or ref["coupling"]["c"] != str(capacity)
            or ref["coupling"]["y_star"] != [str(v) for v in ystar]):
        raise SystemExit(f"stored reference does not match instance {case_name(n, seed)}")
    return {"name": model["name"], "suite": "mechanism",
            "stratum": "interleaved path family with a binding coupling row (campaign-v4-protocol.md, Amendment 1, C4)",
            "known_optimum": ref["optimum"], "known_optimum_exact": ref["optimum_exact"],
            "known_optimum_source": ref["optimum_source"] + f"; Gurobi gap {ref['gurobi']['mip_gap']:.3g}",
            "known_witness": ref["witness"], "known_witness_exact": ref["witness_exact"],
            "reference_bound_ii": ref["bound_ii"]["value"],
            "reference_bound_ii_exact_lower": ref["bound_ii"]["lower_exact"],
            "mechanism": {"n": n, "seed": seed, "rng": f"random.Random({1000 * n + seed})",
                          "triples": records, "c3_name": mechanism.case_name(n, seed),
                          "coupling": ref["coupling"]},
            "model": exact_json(model)}


def main(args):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from common import write_new
    targets = [(n, s) for n in NS for s in SEEDS]
    if args.only:
        targets = [tuple(int(v) for v in item.split(":")) for item in args.only]
    entries = []
    for n, seed in targets:
        entry = reference(n, seed, args.time_limit)
        entries.append(entry)
        print(json.dumps({k: entry[k] for k in ("name", "optimum", "optimum_minus_bound_ii")}
                         | {"bound_ii": entry["bound_ii"]["value"], "gurobi_seconds": entry["gurobi"]["runtime_seconds"],
                            "gurobi_gap": entry["gurobi"]["mip_gap"], "nodes": entry["gurobi"]["nodes"],
                            "fractional": entry["bound_ii"]["fractional_copies"],
                            "certificate_nodes": entry["optimum_certificate"]["nodes"],
                            "gurobi_assignment_minus_optimum":
                                entry["optimum_certificate"]["gurobi_assignment_value_minus_optimum"]}), flush=True)
    import gurobipy
    write_new(args.output, {"schema": "campaign-v4-c4-references-1",
                            "generator_sha256": __import__("hashlib").sha256(Path(__file__).read_bytes()).hexdigest(),
                            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "gurobi_version": ".".join(map(str, gurobipy.gurobi.version())),
                            "instances": entries})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    refs = sub.add_parser("references")
    refs.add_argument("--output", type=Path, required=True)
    refs.add_argument("--only", nargs="*")
    refs.add_argument("--time-limit", type=float, default=3600.0)
    main(parser.parse_args())
