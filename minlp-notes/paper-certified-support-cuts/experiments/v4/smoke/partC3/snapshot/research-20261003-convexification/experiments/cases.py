"""Frozen mechanism cases and independent original-model primal checks.

This module intentionally evaluates expression trees without the model builder.
Checks are floating-point residual checks, not feasible-point certificates.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "code/univariate_envelopes"))
from uenv.osil import Instance


def v(i):
    return ("var", i)


def num(a):
    return ("num", float(a))


def add(*terms):
    return ("sum", *terms)


def mul(*terms):
    return ("times", *terms)


def pow_(term, exponent):
    return ("power", term, num(exponent))


def row(nl=None, lin=None, quad=None, lb=-math.inf, ub=math.inf):
    return {"nl": nl, "lin": lin or {}, "quad": quad or [], "lb": lb, "ub": ub}


def instance(name, bounds, objective, constraints=(), types=None):
    return Instance(name, [b[0] for b in bounds], [b[1] for b in bounds],
                    types or ["C"] * len(bounds), "min", 0.0,
                    [objective, *constraints], [f"x{i}" for i in range(len(bounds))])


def synthetic_cases():
    """Return model, explanatory stratum, and optional exact optimum/witness."""
    cases = []

    def save(model, stratum, optimum=None, witness=None):
        cases.append({"instance": model, "stratum": stratum,
                      "known_optimum": optimum, "known_witness": witness})

    for n in (4, 8):
        f = add(*(add(pow_(v(i), 4), mul(num(-1), pow_(v(i), 2))) for i in range(n)))
        save(instance(f"quartic_balance_{n}", [(-1, 1)] * n, row(nl=f),
                      [row(lin={i: 1 for i in range(n)}, lb=0, ub=0)]),
             "composite polynomial mechanism", -n / 4,
             [(-1 if i % 2 else 1) / math.sqrt(2) for i in range(n)])

    save(instance("cubic_moment", [(0, 1)], row(nl=pow_(v(0), 3)),
                  [row(nl=pow_(v(0), 2), lb=0.25)]),
         "shared polynomial curve", 0.125, [0.5])

    exps = add(("exp", v(0)), ("exp", mul(num(-1), v(0))))
    save(instance("exp_pair", [(-2, 2)], row(nl=exps), [row(nl=exps, lb=3)]),
         "general exp curve", 3.0, [math.acosh(1.5)])

    logs = add(("log", v(0)), mul(num(-0.5), ("log", add(num(1), mul(num(2), v(0))))))
    save(instance("log_pair", [(0.25, 2)], row(nl=logs)),
         "general log curve", math.log(0.25) - 0.5 * math.log(1.5), [0.25])

    save(instance("trig_pair", [(-math.pi, math.pi)],
                  row(nl=add(("sin", v(0)), ("cos", v(0))))),
         "general trigonometric curve", -math.sqrt(2), [-3 * math.pi / 4])

    # min -xy on a simplex is -1/4. McCormick over its enclosing square gives -1/2.
    save(instance("simplex_product", [(0, 1), (0, 1)], row(quad=[(0, 1, -1)]),
                  [row(lin={0: 1, 1: 1}, ub=1)]),
         "coupled two-variable domain", -0.25, [0.5, 0.5])

    # Adding the square features gives a genuine vector block on the same domain.
    save(instance("simplex_quadratic_vector", [(0, 1), (0, 1)],
                  row(quad=[(0, 0, 1), (1, 1, 1), (0, 1, -4)]),
                  [row(lin={0: 1, 1: 1}, ub=1)]),
         "coupled quadratic vector", -0.5, [0.5, 0.5])

    # -y(x+z), x+y<=1, y+z<=1 has minimum -1/2 at all variables 1/2.
    save(instance("overlapping_products", [(0, 1)] * 3,
                  row(quad=[(0, 1, -1), (1, 2, -1)]),
                  [row(lin={0: 1, 1: 1}, ub=1), row(lin={1: 1, 2: 1}, ub=1)]),
         "overlapping coupled blocks", -0.5, [0.5, 0.5, 0.5])

    # Pair quadratic hulls admit incompatible laws of the central variable.
    # The assembled quadratic-star minimum is 1/128; each pair alone admits 0.
    star = instance("star_marginal_inconsistency", [(0, 1)] * 3,
                    row(lin={0: 1.25, 1: -0.5, 2: 1.0},
                        quad=[(0, 0, -0.75), (1, 1, 2.0), (2, 2, -0.609375),
                              (0, 1, -1.0), (1, 2, -1.25)]))
    star.obj_const = 0.0625
    save(star, "pair marginals versus merged quadratic star", 1 / 128,
         [1.0, 11 / 16, 1.0])

    save(instance("affine_control", [(0, 1)] * 8,
                  row(lin={i: i + 1 for i in range(8)}),
                  [row(lin={i: 1 for i in range(8)}, lb=1)]),
         "neutral no nonlinear structure", 1.0, [1.0] + [0.0] * 7)

    save(instance("convex_redundant_control", [(-1, 1)] * 8,
                  row(nl=add(*(add(pow_(v(i), 2), pow_(v(i), 4)) for i in range(8))))),
         "adverse unnecessary convexification", 0.0, [0.0] * 8)

    save(instance("binary_product_control", [(0, 1)] * 4,
                  row(quad=[(0, 1, -1), (2, 3, -1)]),
                  [row(lin={i: 1 for i in range(4)}, ub=2)], types=["B"] * 4),
         "neutral native integer products", -1.0, [1, 1, 0, 0])
    return cases


def evaluate_tree(tree, values):
    tag = tree[0]
    if tag == "num":
        return float(tree[1])
    if tag == "var":
        return float(values[tree[1]])
    a = [evaluate_tree(t, values) for t in tree[1:]]
    if tag == "sum":
        return math.fsum(a)
    if tag == "times":
        return math.prod(a)
    if tag == "negate":
        return -a[0]
    if tag == "divide":
        return a[0] / a[1]
    if tag == "power":
        return a[0] ** a[1]
    if tag == "square":
        return a[0] ** 2
    return {"log": math.log, "exp": math.exp, "sin": math.sin,
            "cos": math.cos, "sqrt": math.sqrt, "abs": abs}[tag](a[0])


def row_value(r, values):
    terms = [c * values[int(i)] for i, c in r["lin"].items()]
    terms.extend(c * values[i] * values[j] for i, j, c in r["quad"])
    if r["nl"] is not None:
        terms.append(evaluate_tree(r["nl"], values))
    return math.fsum(terms), math.fsum(abs(t) for t in terms)


def check_primal(model, values, reported_objective=None, tolerance=1e-5):
    if values is None:
        return {"checked": False, "reason": "no incumbent"}
    if len(values) != len(model.var_lb):
        return {"checked": True, "passed": False, "reason": "wrong original variable count"}
    if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in values):
        return {"checked": True, "passed": False, "reason": "nonfinite original value"}
    violations = []
    for i, (x, lo, hi, kind) in enumerate(zip(values, model.var_lb, model.var_ub, model.var_type)):
        if kind == "B":
            lo, hi = max(0.0, lo), min(1.0, hi)
        if math.isfinite(lo):
            violations.append((max(0.0, lo - x) / max(1.0, abs(lo)), f"lower bound {i}"))
        if math.isfinite(hi):
            violations.append((max(0.0, x - hi) / max(1.0, abs(hi)), f"upper bound {i}"))
        if kind in ("B", "I"):
            violations.append((abs(x - round(x)), f"integrality {i}"))
    try:
        objective, _ = row_value(model.rows[0], values)
        objective += model.obj_const
        if not math.isfinite(objective):
            raise ValueError("nonfinite original objective")
        if reported_objective is not None and not math.isfinite(reported_objective):
            raise ValueError("nonfinite reported objective")
        for i, r in enumerate(model.rows[1:]):
            y, magnitude = row_value(r, values)
            if not math.isfinite(y):
                raise ValueError("nonfinite row")
            for bound, residual, side in ((r["lb"], r["lb"] - y, "lower"),
                                          (r["ub"], y - r["ub"], "upper")):
                if math.isfinite(bound):
                    violations.append((max(0.0, residual) / max(1.0, magnitude, abs(bound)),
                                       f"row {i} {side}"))
    except (ArithmeticError, ValueError, TypeError, OverflowError) as exc:
        return {"checked": True, "passed": False, "reason": str(exc)}
    discrepancy = (abs(objective - reported_objective) / max(1.0, abs(objective))
                   if reported_objective is not None else 0.0)
    worst, where = max(violations, default=(0.0, "none"))
    return {"checked": True, "passed": worst <= tolerance and discrepancy <= tolerance,
            "objective": objective, "max_scaled_violation": worst, "worst_location": where,
            "relative_objective_discrepancy": discrepancy, "tolerance": tolerance,
            "certificate": False}
