"""Part 5S star family of campaign-v5-protocol.md, as exact case data.

Instance (k, n, s), k in {4, 8, 16} leaves per star, n in {10, 20} stars, s in 0..4, with one
``random.Random(100000*k + 1000*n + s)``. For star i = 1..n and, within it, leaf j = 1..k:

    m1, m2 = rng.sample(range(49), 2)          # two distinct m in 0..48, in random order
    (a1, a2) = (m1/64, m2/64)
    d = rng.choice((1/8, 1/4, 1/2, 1))

Variables, star by star: y_i, then x_ij, t_ij for j = 1..k (indices (2k+1)(i-1), then
(2k+1)(i-1) + 2j - 1 and + 2j). Bounds: y, x in [0, 1], t in [-10, 10].
Row 0 is the objective sum_ij t_ij. Rows 1..nk (star by star) are Phi_ij(x_ij, y_i) - t_ij <= 0,
expanded exactly with the constant a1^2 moved to the right-hand side:

    Phi(x, y) = (y - a1 - p x)^2 + x (1 - x)
              = y^2 + (p^2 - 1) x^2 - 2 p x y + (2 a1 p + 1) x - 2 a1 y + a1^2,   p = a2 - a1.

Rows nk+1..2nk are the center-leaf rows x_ij - y_i <= d_ij (same order); row 2nk+1 is the
coupling row sum_i y_i <= 0.8 n. Every coefficient is dyadic and exact in binary64.

Exact optimum. Phi is concave in x (p^2 - 1 < 0), so for fixed y its minimum over the leaf
interval [0, U(y)], U(y) = min(1, y + d), is attained at an endpoint, and
Phi(U, y) - Phi(0, y) = U g(y) with g(y) = (p^2 - 1) U(y) - 2 p y + 2 a1 p + 1, affine in y on
each regime of U (y <= 1 - d: U = y + d; y >= 1 - d: U = 1). The star optimum is
min_{y in [0, 1]} sum_j phi_j(y), phi_j(y) = min{Phi_j(0, y), Phi_j(U_j(y), y)}. Piece enumeration
(``star_optimum``): all breakpoints (1 - d_j and the zero of g_j in each regime) are rational; on
each piece every leaf's endpoint choice is fixed (decided at the midpoint) and the sum is one
quadratic in y; its minimum over the closed piece is at an endpoint or at an interior stationary
point (leading coefficient positive). The least candidate value, with F evaluated directly from
its definition, is the exact star optimum; the least candidate attaining it is the smallest
minimizer (a minimizing interval is a whole piece with a constant quadratic). The value is
cross-checked against the independent sweep ``sweep_star`` of ``verification/M3_star_sweep.py``
(loaded read-only from its file). The generator requires the sum of the smallest minimizers to
be at most 0.8 n, so the coupling row does not bind and the instance optimum is the sum of the
star optima.

Known witness: per star the smallest minimizer y*, each leaf at the endpoint that is optimal at
y* (0 if Phi(0, y*) <= Phi(U(y*), y*)); y rounded down to binary64, a leaf at U recomputed as
min(1, y_b + d) rounded down (so x - y <= d holds exactly), t = Phi(x, y) at the binary64 point
rounded up. ``exact_check`` verifies all bounds and rows of the case model in rational
arithmetic; make_jobs also runs the archived primal check.
"""
from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import math
from pathlib import Path
import random

KS = (4, 8, 16)
NS = (10, 20)
SEEDS = (0, 1, 2, 3, 4)
SLACKS = (Q(1, 8), Q(1, 4), Q(1, 2), Q(1))
COUPLING = Q(4, 5)
SWEEP = Path(__file__).resolve().parents[2] / "verification/M3_star_sweep.py"


def case_name(k, n, seed):
    return f"constrained_star_k{k}_n{n}_s{seed}"


def rng_seed(k, n, seed):
    return 100000 * k + 1000 * n + seed


def draw(k, n, seed):
    """Per star a list of k leaves (a1, a2, d), exact."""
    rng = random.Random(rng_seed(k, n, seed))
    stars = []
    for _ in range(n):
        leaves = []
        for _ in range(k):
            m1, m2 = rng.sample(range(49), 2)
            leaves.append((Q(m1, 64), Q(m2, 64), rng.choice(SLACKS)))
        stars.append(leaves)
    return stars


def coefficients(a1, a2):
    """Exact coefficients of Phi - a1^2: linear (x, y), quadratic (yy, xx, xy)."""
    p = a2 - a1
    return {"x": 2 * a1 * p + 1, "y": -2 * a1, "yy": Q(1), "xx": p * p - 1, "xy": -2 * p}


def phi(leaf, x, y):
    a1, a2, _ = leaf
    return (y - a1 - (a2 - a1) * x) ** 2 + x * (1 - x)


def upper(leaf, y):
    return min(Q(1), y + leaf[2])


def regime(leaf, y):
    """U(y) = u0 + u1 y on the regime containing y (y + d below 1 - d, 1 above)."""
    return (leaf[2], Q(1)) if y + leaf[2] < 1 else (Q(1), Q(0))


def leaf_value(leaf, y):
    return min(phi(leaf, Q(0), y), phi(leaf, upper(leaf, y), y))


def leaf_breakpoints(leaf):
    """Rational points of (0, 1) where U changes regime or the preferred endpoint can change."""
    a1, a2, d = leaf
    p = a2 - a1
    points = set()
    if 0 < 1 - d < 1:
        points.add(1 - d)
    for lo, hi, (u0, u1) in ((Q(0), min(Q(1), 1 - d), (d, Q(1))), (max(Q(0), 1 - d), Q(1), (Q(1), Q(0)))):
        slope = (p * p - 1) * u1 - 2 * p
        if lo < hi and slope:
            root = -((p * p - 1) * u0 + 2 * a1 * p + 1) / slope
            if lo < root < hi:
                points.add(root)
    return points


def total(star, y):
    return sum((leaf_value(leaf, y) for leaf in star), Q(0))


def quadratic_in_y(leaf, rule):
    """Coefficients (c0, c1, c2) of Phi(x0 + x1 y, y) for the affine leaf rule (x0, x1)."""
    x0, x1 = rule
    f = lambda y: phi(leaf, x0 + x1 * y, y)
    c0 = f(Q(0))
    c1 = (f(Q(1)) - f(Q(-1))) / 2
    c2 = (f(Q(1)) + f(Q(-1))) / 2 - c0
    return c0, c1, c2


def star_optimum(star):
    """Exact minimum of sum_j phi_j over y in [0, 1], the smallest minimizer and the piece count."""
    points = sorted({Q(0), Q(1)}.union(*(leaf_breakpoints(leaf) for leaf in star)))
    candidates = []
    for left, right in zip(points, points[1:]):
        middle = (left + right) / 2
        polynomial = [Q(0), Q(0), Q(0)]
        for leaf in star:
            at_zero, at_upper = phi(leaf, Q(0), middle), phi(leaf, upper(leaf, middle), middle)
            rule = (Q(0), Q(0)) if at_zero <= at_upper else regime(leaf, middle)
            polynomial = [a + b for a, b in zip(polynomial, quadratic_in_y(leaf, rule))]
        c0, c1, c2 = polynomial
        local = [left, right]
        if c2 > 0 and left < -c1 / (2 * c2) < right:
            local.append(-c1 / (2 * c2))
        for y in local:
            value = total(star, y)
            if value != c0 + c1 * y + c2 * y * y:  # the piece quadratic agrees on the closed piece
                raise AssertionError("piece quadratic differs from the star function")
            candidates.append((value, y))
    value = min(v for v, _ in candidates)
    return value, min(y for v, y in candidates if v == value), len(points) - 1


def load_sweep():
    spec = importlib.util.spec_from_file_location("m3_star_sweep_readonly", SWEEP)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sweep_value(star, sweep):
    """The star optimum by the independent sweep of verification/M3_star_sweep.py."""
    center = {"ly": Q(0), "uy": Q(1), "rows": [],
              "a0": sum((a1 * a1 for a1, _, _ in star), Q(0)),
              "a1": sum((-2 * a1 for a1, _, _ in star), Q(0)), "a2": Q(len(star))}
    leaves = []
    for a1, a2, d in star:
        c = coefficients(a1, a2)
        # x - y <= d is p*y + b*x <= c with p = -1, b = 1.
        leaves.append({"l": Q(0), "u": Q(1), "d": c["xx"], "e": c["xy"], "f": c["x"],
                       "rows": [(Q(-1), Q(1), d)]})
    result = sweep.sweep_star(center, leaves)
    if result is None:
        raise AssertionError("the sweep reports an empty star")
    return result["value"]


def binary64(value):
    result = float(value)
    if Q(result) != value:
        raise ValueError(f"{value} is not exactly representable in binary64")
    return result


def round_down(value):
    f = float(value)
    return f if Q(f) <= value else math.nextafter(f, -math.inf)


def round_up(value):
    f = float(value)
    return f if Q(f) >= value else math.nextafter(f, math.inf)


def indices(k, i, j=None):
    """Indices of y_i (j None) or of (x_ij, t_ij), zero-based i and j."""
    base = (2 * k + 1) * i
    return base if j is None else (base + 2 * j + 1, base + 2 * j + 2)


def model_dict(k, n, stars, name):
    width = 2 * k + 1
    rows = [{"nl": None, "lin": {indices(k, i, j)[1]: 1.0 for i in range(n) for j in range(k)}, "quad": [],
             "lb": -math.inf, "ub": math.inf}]
    for i, star in enumerate(stars):
        y = indices(k, i)
        for j, (a1, a2, d) in enumerate(star):
            x, t = indices(k, i, j)
            c = coefficients(a1, a2)
            lin = {y: c["y"], x: c["x"], t: Q(-1)}
            lin = {index: binary64(v) for index, v in sorted(lin.items()) if v}
            quad = [(y, y, binary64(c["yy"])), (x, x, binary64(c["xx"])), (y, x, binary64(c["xy"]))]
            rows.append({"nl": None, "lin": lin, "quad": [q for q in quad if q[2]],
                         "lb": -math.inf, "ub": binary64(-a1 * a1)})
    for i, star in enumerate(stars):
        y = indices(k, i)
        for j, (_, _, d) in enumerate(star):
            rows.append({"nl": None, "lin": {y: -1.0, indices(k, i, j)[0]: 1.0}, "quad": [],
                         "lb": -math.inf, "ub": binary64(d)})
    rows.append({"nl": None, "lin": {indices(k, i): 1.0 for i in range(n)}, "quad": [],
                 "lb": -math.inf, "ub": binary64(COUPLING * n)})
    names = []
    for i in range(n):
        names.append(f"y_{i + 1}")
        for j in range(k):
            names += [f"x_{i + 1}_{j + 1}", f"t_{i + 1}_{j + 1}"]
    return {"name": name, "var_lb": ([0.0] + [0.0, -10.0] * k) * n, "var_ub": ([1.0] + [1.0, 10.0] * k) * n,
            "var_type": ["C"] * (width * n), "obj_sense": "min", "obj_const": 0.0, "rows": rows,
            "var_names": names}


def row_value(row, values):
    value = sum((Q(c) * values[int(i)] for i, c in row["lin"].items()), Q(0))
    return value + sum((Q(c) * values[i] * values[j] for i, j, c in row["quad"]), Q(0))


def exact_check(model, values):
    """Bounds and rows of the model at the binary64 point, in rational arithmetic; objective."""
    point = [Q(v) for v in values]
    for v, lo, hi in zip(point, model["var_lb"], model["var_ub"]):
        if not Q(lo) <= v <= Q(hi):
            raise AssertionError("witness violates a variable bound")
    for row in model["rows"][1:]:
        value = row_value(row, point)
        if (math.isfinite(row["ub"]) and value > Q(row["ub"])) or (math.isfinite(row["lb"]) and value < Q(row["lb"])):
            raise AssertionError("witness violates a row")
    return row_value(model["rows"][0], point) + Q(model["obj_const"])


def witness(k, stars, minimizers):
    values = [0.0] * ((2 * k + 1) * len(stars))
    for i, (star, ystar) in enumerate(zip(stars, minimizers)):
        yb = round_down(ystar)
        values[indices(k, i)] = yb
        for j, leaf in enumerate(star):
            x, t = indices(k, i, j)
            at_upper = phi(leaf, Q(0), ystar) > phi(leaf, upper(leaf, ystar), ystar)
            xb = round_down(upper(leaf, Q(yb))) if at_upper else 0.0
            values[x] = xb
            values[t] = round_up(phi(leaf, Q(xb), Q(yb)))
    return values


def instance(k, n, seed, sweep=None):
    """Return (model dict, exact optimum, witness values, star records)."""
    sweep = sweep or load_sweep()
    stars = draw(k, n, seed)
    optima, minimizers, pieces = [], [], []
    for star in stars:
        value, ystar, count = star_optimum(star)
        if sweep_value(star, sweep) != value:
            raise AssertionError("piece enumeration and the independent sweep disagree")
        optima.append(value)
        minimizers.append(ystar)
        pieces.append(count)
    if sum(minimizers) > COUPLING * n:
        raise AssertionError("the coupling row binds at the smallest minimizers")
    optimum = sum(optima, Q(0))
    model = model_dict(k, n, stars, case_name(k, n, seed))
    values = witness(k, stars, minimizers)
    objective = exact_check(model, values)
    if not 0 <= objective - optimum <= Q(1, 10 ** 9):
        raise AssertionError("witness objective is not within 1e-9 above the optimum")
    records = {"leaves": [[[str(a1), str(a2), str(d)] for a1, a2, d in star] for star in stars],
               "star_optima": [str(v) for v in optima], "smallest_minimizers": [str(v) for v in minimizers],
               "sum_smallest_minimizers": str(sum(minimizers)), "coupling_rhs": str(COUPLING * n),
               "pieces": pieces, "witness_objective_exact": str(objective),
               "witness_objective_minus_optimum": float(objective - optimum)}
    return model, optimum, values, records


def case(k, n, seed, exact_json, sweep=None):
    """Case descriptor in the campaign-v2 synthetic format (see worker.load_model)."""
    model, optimum, values, records = instance(k, n, seed, sweep)
    return {"name": model["name"], "suite": "star",
            "stratum": "constrained quadratic stars with center-leaf rows (campaign-v5-protocol.md, Part 5S)",
            "known_optimum": float(optimum), "known_optimum_exact": str(optimum),
            "known_optimum_source": ("sum of the exact star optima (piece enumeration in rational arithmetic, "
                                     "equal to the sweep of verification/M3_star_sweep.py); the coupling row "
                                     "does not bind at the smallest minimizers"),
            "known_witness": values, "known_witness_exact": [str(Q(v)) for v in values],
            "star": {"k": k, "n": n, "seed": seed, "rng": f"random.Random({rng_seed(k, n, seed)})", **records},
            "model": exact_json(model)}
