"""Adversarial tests for certify.convexity written during the 2026-09-12 review.

Each test builds a small Pyomo expression whose curvature is known (checked
numerically on a grid) and asserts that certify() does not claim a stronger
curvature than the truth. Failing tests document unsound rules.
"""
import itertools, math
from fractions import Fraction

import pyomo.environ as pe
import pytest

from certify.convexity import certify, CONVEX, CONCAVE, AFFINE, UNKNOWN


def _grid(bounds, n=7):
    axes = [[lo + (hi - lo) * k / (n - 1) for k in range(n)] for lo, hi in bounds]
    return list(itertools.product(*axes))


def numeric_curvature(expr, vars_, n=7):
    """Return (is_convex, is_concave) by midpoint tests on a grid within bounds."""
    bounds = [(v.lb, v.ub) for v in vars_]
    pts = _grid(bounds, n)
    def f(p):
        for v, x in zip(vars_, p):
            v.set_value(x, skip_validation=True)
        return pe.value(expr)
    vals = {p: f(p) for p in pts}
    convex = concave = True
    tol = 1e-9
    for p in pts:
        for q in pts:
            mid = tuple((a + b) / 2 for a, b in zip(p, q))
            fm = f(mid)
            avg = (vals[p] + vals[q]) / 2
            if fm > avg + tol * (1 + abs(avg)):
                convex = False
            if fm < avg - tol * (1 + abs(avg)):
                concave = False
    return convex, concave


def assert_sound(expr, vars_):
    c = certify(expr)
    conv, conc = numeric_curvature(expr, vars_)
    if c.curv == CONVEX:
        assert conv, f"certified convex but not convex: {c.why}"
    elif c.curv == CONCAVE:
        assert conc, f"certified concave but not concave: {c.why}"
    elif c.curv == AFFINE:
        assert conv and conc, f"certified affine but not: {c.why}"
    return c


def model(**bounds):
    m = pe.ConcreteModel()
    for name, (lo, hi) in bounds.items():
        m.add_component(name, pe.Var(bounds=(lo, hi), initialize=(lo + hi) / 2))
    return m


# --- perspective rule -------------------------------------------------------

def test_perspective_t_outside_division():
    # t * ((x/t)**2 + exp(-t)) = x^2/t + t exp(-t): not convex for t < 2
    m = model(x=(-1, 1), t=(0.5, 1.5))
    assert_sound(m.t * ((m.x / m.t) ** 2 + pe.exp(-m.t)), [m.x, m.t])


def test_perspective_x_outside_division():
    # t * (exp(x/t) + x) = t exp(x/t) + t x : bilinear term, not convex
    m = model(x=(-1, 1), t=(0.5, 1.5))
    assert_sound(m.t * (pe.exp(m.x / m.t) + m.x), [m.x, m.t])


def test_perspective_affine_claim():
    # t * (x/t + t) = x + t^2 is convex, not affine
    m = model(x=(-1, 1), t=(0.5, 1.5))
    c = assert_sound(m.t * (m.x / m.t + m.t), [m.x, m.t])
    assert c.curv != AFFINE


# --- division rules ----------------------------------------------------------

def test_negative_const_over_positive_convex():
    # -1/(exp(x)+exp(-x)) = -sech(x): convex near 0, so not concave
    m = model(x=(-1, 1))
    assert_sound(-1 / (pe.exp(m.x) + pe.exp(-m.x)), [m.x])


def test_positive_const_over_positive_concave_ok():
    m = model(x=(1, 2))
    c = assert_sound(1 / pe.log(m.x + 1), [m.x])
    assert c.curv == CONVEX


# --- monomial rule -----------------------------------------------------------

def test_monomial_zero_exponent_variable_order():
    # y/y*x is x (for y != 0): affine, range should be that of x, not y
    m = model(x=(-5, 5), y=(1, 2))
    c = certify(m.y / m.y * m.x)
    assert c.curv == AFFINE
    assert (c.lo, c.hi) == (Fraction(-5), Fraction(5)), (c.lo, c.hi, c.why)


def test_monomial_negative_exponent_needs_positive():
    m = model(x=(-1, 1))
    c = certify(1 / (m.x * m.x))  # 1/x^2 not convex on [-1,1] (undefined at 0)
    assert c.curv == UNKNOWN


def test_monomial_lundell_westerlund_convex():
    m = model(x=(0.5, 2), y=(0.5, 2))
    # x^2/y is convex (LW conditions); the DivisionExpression path does not
    # call _monomial, so the current answer is 'unknown' (completeness gap)
    c = assert_sound(m.x ** 2 / m.y, [m.x, m.y])
    c = assert_sound(m.x * m.x / m.y, [m.x, m.y])
    c = assert_sound(m.x ** 2 * (1 / m.y), [m.x, m.y])
    c = assert_sound(m.x ** 2 / m.y ** 2, [m.x, m.y])
    assert c.curv == UNKNOWN


# --- power rules -------------------------------------------------------------

@pytest.mark.parametrize("p", [3, 1.5, 0.5, -1, -2, 2, 4, 2.5])
def test_pow_on_positive_box(p):
    m = model(x=(0.5, 2))
    assert_sound(m.x ** p, [m.x])


@pytest.mark.parametrize("p", [3, 1.5, 0.5, 2, 4])
def test_pow_on_mixed_box(p):
    m = model(x=(-1, 2))
    c = certify(m.x ** p)
    if p in (2, 4):
        assert c.curv == CONVEX
    else:
        assert c.curv == UNKNOWN, c.why


def test_even_power_of_nonneg_convex():
    m = model(x=(-1, 1))
    assert_sound((pe.exp(m.x)) ** 2, [m.x])
    assert_sound((pe.exp(m.x) - 3) ** 2, [m.x])  # base not nonneg -> must not be convex-certified? (it is convex? no: (e^x-3)^2 has negative curvature where e^x < 1.5)


def test_const_pow_expr():
    m = model(x=(-1, 1))
    c = assert_sound(2 ** (m.x ** 2), [m.x])
    c = assert_sound(0.5 ** (-(m.x ** 2)), [m.x])
    # 0.5 ** convex is not convex in general
    c = assert_sound(0.5 ** (m.x ** 2), [m.x])
    assert c.curv == UNKNOWN


# --- quadratic / PSD ---------------------------------------------------------

def test_psd_zero_pivot():
    m = model(x=(-1, 1), y=(-1, 1), z=(-1, 1))
    # x*y has zero diagonal -> indefinite
    assert certify(m.x * m.y).curv == UNKNOWN
    # (x - y)^2 + 0*z^2 is PSD with a zero pivot after elimination
    c = assert_sound((m.x - m.y) ** 2, [m.x, m.y])
    assert c.curv == CONVEX
    # x^2 + 2xy + y^2 + y*z : after eliminating x the (y,y) pivot is 0 but (y,z) != 0
    assert certify(m.x ** 2 + 2 * m.x * m.y + m.y ** 2 + m.y * m.z).curv == UNKNOWN


def test_sqrt_quadratic():
    m = model(x=(-1, 1), y=(-1, 1))
    c = assert_sound(pe.sqrt(m.x ** 2 + m.y ** 2 + 1), [m.x, m.y])
    assert c.curv == CONVEX
    c = assert_sound(pe.sqrt(m.x ** 2 + 2 * m.x + 2), [m.x])  # (x+1)^2 + 1
    assert c.curv == CONVEX
    c = certify(pe.sqrt(m.x ** 2 + 2 * m.x))  # (x+1)^2 - 1, not PSD-homogenized
    assert c.curv == UNKNOWN


# --- fixed variables and log/exp ranges --------------------------------------

def test_fixed_variable_as_constant():
    m = model(x=(0.5, 2), y=(-10, 10))
    m.y.fix(-3.0)
    # y * log(x) with y fixed negative -> convex
    c = assert_sound(m.y * pe.log(m.x), [m.x])
    assert c.curv == CONVEX


def test_log_of_exp_minus_const():
    # log(exp(x) - 1): argument is convex, so DCP cannot certify (unknown is
    # the expected answer); the argument's positivity comes from _exp_range.
    m = model(x=(1, 2))
    assert_sound(pe.log(pe.exp(m.x) - 1), [m.x])
    m2 = model(x=(0, 2))
    assert certify(pe.log(pe.exp(m2.x) - 1)).curv == UNKNOWN
    # 1/(exp(x) - 1) needs the argument positive: x in [1, 2] ok, x in [0, 2] must be refused
    assert certify(1 / (pe.exp(m2.x) - 1)).curv == UNKNOWN


def test_linear_fractional():
    m = model(x=(0, 1))
    c = assert_sound((m.x + 1) / (m.x + 2), [m.x])
    assert c.curv == CONCAVE
    c = assert_sound((2 * m.x + 1) / (m.x + 0.25), [m.x])
    assert c.curv == CONVEX
