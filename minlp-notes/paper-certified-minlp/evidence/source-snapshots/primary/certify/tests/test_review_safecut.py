"""Adversarial tests for the safe-cut lemma implementation (safecut.py and
driver._verify_given_cut), written during the 2026-09-12 review.

Validity is brute-forced: b_safe must not exceed min over a grid of
phi(x) = g(x) + l^T x + c - a^T x on the box."""
import itertools
from fractions import Fraction

import pyomo.environ as pe
import pytest

from certify.driver import _verify_given_cut
from certify.safecut import SafeCutter
from lbesh.structure import _classify_constraint


def make_row(build, bounds):
    m = pe.ConcreteModel()
    for name, (lo, hi) in bounds.items():
        m.add_component(name, pe.Var(bounds=(lo, hi), initialize=0.0 if lo is None else lo))
    m.c = pe.Constraint(expr=build(m))
    kind, rows = _classify_constraint(m.c, "c")
    assert kind == "nl" and len(rows) == 1
    row = rows[0]
    vars_by_name = {v.name: v for v in m.component_data_objects(pe.Var)}
    boxid = {id(v): (None if v.lb is None else Fraction(v.lb), None if v.ub is None else Fraction(v.ub)) for v in vars_by_name.values()}
    return m, row, vars_by_name, boxid


def phi_min_grid(row, vars_by_name, a, n=41):
    vs = row.all_vars()
    axes = []
    for v in vs:
        lo, hi = v.lb, v.ub
        # unbounded side: sample a wide range on that side only
        lo = -50.0 if lo is None else lo
        hi = 50.0 if hi is None else hi
        axes.append([lo + (hi - lo) * k / (n - 1) for k in range(n)])
    best = float("inf")
    for p in itertools.product(*axes):
        xv = {id(v): x for v, x in zip(vs, p)}
        val = row.violation(xv) - sum(float(a.get(v.name, 0)) * xv[id(v)] for v in vs)
        best = min(best, val)
    return best


def check(build, bounds, z, a, expect_none=False):
    m, row, vbn, boxid = make_row(build, bounds)
    sc = SafeCutter(row, boxid)
    zid = {id(vbn[k]): v for k, v in z.items()}
    a = {k: Fraction(v) for k, v in a.items()}
    b_safe = _verify_given_cut(sc, row, zid, a, vbn)
    if expect_none:
        assert b_safe is None
        return None
    assert b_safe is not None
    gmin = phi_min_grid(row, vbn, a)
    assert float(b_safe) <= gmin + 1e-9, (float(b_safe), gmin)
    return b_safe, gmin


def test_interior_point_exact_slope():
    check(lambda m: pe.exp(m.x) - m.y <= 0, dict(x=(-1, 1), y=(0, 10)), dict(x=0.5, y=1.0), dict(x="1.6487212707", y="-1"))


def test_corner_points_and_bad_slopes():
    for zx in (-1.0, 1.0, 0.0):
        for ax in ("0", "5", "-3"):
            check(lambda m: pe.exp(m.x) + 0.1 * m.y - 0.3 <= 0, dict(x=(-1, 1), y=(-2, 2)), dict(x=zx, y=0.0), dict(x=ax, y="0.1"))


def test_negative_coefficients_and_ge_row():
    # concave row body >= : -g convex
    check(lambda m: pe.log(m.x) - 2 * m.y >= -1, dict(x=(0.5, 3), y=(-1, 1)), dict(x=2.0, y=0.5), dict(x="-0.5", y="2"))


def test_unbounded_coordinate_requires_zero_slope():
    # y unbounded: slope must match exactly, else None
    check(lambda m: m.x ** 2 - m.y <= 0, dict(x=(-2, 2), y=(None, None)), dict(x=1.0, y=1.0), dict(x="2", y="-1"))
    check(lambda m: m.x ** 2 - m.y <= 0, dict(x=(-2, 2), y=(None, None)), dict(x=1.0, y=1.0), dict(x="2", y="-0.999999999999"), expect_none=True)


def test_tight_bound_at_minimizer_with_non_dyadic_values():
    # z at the lower corner with d >= 0: bound is tight; phi(z) has > 53 bits
    check(lambda m: m.x ** 2 + m.y ** 2 - 1 <= 0, dict(x=(0.1, 1), y=(0.3, 1)), dict(x=0.1, y=0.3), dict(x="0.1", y="0.5"))


def test_fractional_power_and_sqrt():
    check(lambda m: m.x ** 1.5 - pe.sqrt(m.y) - 3 <= 0, dict(x=(0.5, 2), y=(0.25, 4)), dict(x=1.0, y=1.0), dict(x="1.5", y="-0.5"))


def test_linearization_point_outside_box_is_rejected():
    # x^3 is convex only for x >= 0; a tangent taken at x = -1 is not a valid
    # underestimator on the box [0, 10]. The checker must reject z outside B.
    m, row, vbn, boxid = make_row(lambda m: m.x ** 3 - m.y <= 0, dict(x=(0, 10), y=(0, 1000)))
    sc = SafeCutter(row, boxid)
    zid = {id(vbn["x"]): -1.0, id(vbn["y"]): 0.0}
    b_safe = _verify_given_cut(sc, row, zid, {"x": Fraction(3), "y": Fraction(-1)}, vbn)
    gmin = phi_min_grid(row, vbn, {"x": 3, "y": -1})
    assert b_safe is None or float(b_safe) <= gmin + 1e-9, (b_safe, gmin)


def test_half_line_rule_one_sided_bounds():
    # y has only a lower bound: accepted iff d_y >= 0, i.e. a_y <= l_y + grad_y
    check(lambda m: pe.exp(m.x) - m.y <= 0, dict(x=(-1, 1), y=(0, None)), dict(x=0.0, y=1.0), dict(x="1", y="-1"))
    check(lambda m: pe.exp(m.x) - m.y <= 0, dict(x=(-1, 1), y=(0, None)), dict(x=0.0, y=1.0), dict(x="1", y="-1.5"))
    check(lambda m: pe.exp(m.x) - m.y <= 0, dict(x=(-1, 1), y=(0, None)), dict(x=0.0, y=1.0), dict(x="1", y="-0.5"), expect_none=True)
    # y has only an upper bound: accepted iff d_y <= 0
    check(lambda m: pe.exp(m.x) + m.y <= 5, dict(x=(-1, 1), y=(None, 3)), dict(x=0.0, y=1.0), dict(x="1", y="1"))
    check(lambda m: pe.exp(m.x) + m.y <= 5, dict(x=(-1, 1), y=(None, 3)), dict(x=0.0, y=1.0), dict(x="1", y="1.5"))
    check(lambda m: pe.exp(m.x) + m.y <= 5, dict(x=(-1, 1), y=(None, 3)), dict(x=0.0, y=1.0), dict(x="1", y="0.5"), expect_none=True)
    # nonlinear variable with a one-sided bound: x >= 0.5 only, x**2 row
    check(lambda m: m.x ** 2 - m.y <= 0, dict(x=(0.5, None), y=(0, 100)), dict(x=1.0, y=1.0), dict(x="1.9", y="-1"))
    check(lambda m: m.x ** 2 - m.y <= 0, dict(x=(0.5, None), y=(0, 100)), dict(x=1.0, y=1.0), dict(x="2.1", y="-1"), expect_none=True)
