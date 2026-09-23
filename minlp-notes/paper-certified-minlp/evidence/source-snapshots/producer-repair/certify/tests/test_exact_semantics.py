"""Regressions for the exact expression contract and original domains."""
from fractions import Fraction as F
from types import SimpleNamespace

import pyomo.environ as pe
from pyomo.core.expr import numeric_expr as NE
import pytest
import sympy as sp

from certify.convexity import certify, validate_expression_domain, CONCAVE, UNKNOWN
from certify.exact_model import (ExactModelError, exact_constant,
    exact_constraint_rows, exact_repn, exact_sympy, rational)
from certify.safecut import SafeCutter, mpf_to_frac_down
from lbesh.structure import NLRow


def test_quadratic_cancellation_uses_exact_binary_leaves():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(-1, 1))
    expr = .1*m.x*m.x + .2*m.x*m.x - .30000000000000004*m.x*m.x
    coefficient = F(.1) + F(.2) - F(.30000000000000004)
    assert coefficient == -F(1, 2**55)
    assert exact_repn(expr, quadratic=True).quadratic_coefs == (coefficient,)
    assert certify(expr).curv == CONCAVE
    symbols, se = exact_sympy(expr)
    assert sp.diff(se, symbols[0], 2) == 2*coefficient


def test_affine_rows_and_mutable_parameter_arithmetic_remain_exact():
    m = pe.ConcreteModel()
    m.x = pe.Var()
    m.a = pe.Param(initialize=.1, mutable=True)
    m.b = pe.Param(initialize=.2, mutable=True)
    expr = (m.a + m.b)*m.x + m.a + m.b
    repn = exact_repn(expr)
    assert repn.linear_coefs == (F(.1)+F(.2),)
    assert repn.constant == F(.1)+F(.2)
    assert exact_constant(m.a+m.b) != F(.1+.2)
    # Changing the loaded parameter must change the certified model.
    m.a.set_value(.25)
    assert exact_repn(expr).linear_coefs == (F(.25)+F(.2),)


def test_large_integer_and_fixed_rational_are_not_cast_to_float():
    m = pe.ConcreteModel()
    m.x = pe.Var(initialize=2**60+1)
    m.x.fix()
    assert rational(2**60+1) == 2**60+1
    assert exact_constant(m.x) == 2**60+1
    # Pyomo rewrites x/3 to (binary float 1/3)*x at construction.
    assert exact_repn(m.x/3).constant == F(1/3)*(2**60+1)
    assert exact_repn(NE.DivisionExpression((m.x, 3))).constant == F(2**60+1, 3)


def test_nonlinear_row_split_keeps_exact_constant_and_linear_part():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 1), initialize=.5)
    m.y = pe.Var(bounds=(0, 1))
    m.a = pe.Param(initialize=.1, mutable=True)
    m.b = pe.Param(initialize=.2, mutable=True)
    m.c = pe.Constraint(expr=pe.exp(m.x)+(m.a+m.b)*m.y+m.a >= m.b)
    row, = exact_constraint_rows(m.c)
    assert row.name == 'c_lb'
    assert row.lin_coefs == [-(F(.1)+F(.2))]
    assert row.const == F(.2)-F(.1)


def test_transcendental_constant_stays_in_nonlinear_expression():
    m = pe.ConcreteModel()
    m.a = pe.Param(initialize=.1, mutable=True)
    expr = pe.exp(m.a)
    assert exact_repn(expr).nonlinear_expr is not None
    with pytest.raises(ExactModelError, match='exactly rational'):
        exact_constant(expr)
    _, se = exact_sympy(expr)
    assert se == sp.exp(sp.Rational(F(.1).numerator, F(.1).denominator), evaluate=False)


@pytest.mark.parametrize('kind', ['division', 'zero_product', 'zero_power', 'log'])
def test_original_domain_survives_algebraic_cancellation(kind):
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(-1, 1))
    quotient = NE.DivisionExpression((m.x, m.x))
    expr = {'division': quotient,
            'zero_product': NE.ProductExpression((0, quotient)),
            'zero_power': NE.PowExpression((quotient, 0)),
            'log': NE.SumExpression([pe.log(m.x), -pe.log(m.x)])}[kind]
    assert exact_repn(expr).nonlinear_expr is not None
    with pytest.raises(ExactModelError):
        validate_expression_domain(expr)
    assert certify(expr).curv == UNKNOWN


def test_fractional_monomial_identity_does_not_replace_abs_x_by_x():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(-1, 1))
    # sqrt(x^2)*x = |x|x is neither convex nor concave on this box.
    assert certify(pe.sqrt(m.x**2)*m.x).curv == UNKNOWN


def test_perspective_does_not_reuse_numerator_bounds_for_ratios():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(2, 3))
    m.t = pe.Var(bounds=(10, 20))
    # (exp(x)-3)^2 is convex for x>=2. For x/t in [.1,.3], its
    # second derivative 2 exp(x/t)*(2 exp(x/t)-3) is negative.
    assert certify(m.t*(pe.exp(m.x/m.t)-3)**2).curv == UNKNOWN


def test_cut_encloses_exact_function_and_exact_derivative():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(-1, 1))
    # Deliberate cancellation used to disappear inside sympyify_expression.
    expr = .30000000000000004*m.x**2 - .1*m.x**2 - .2*m.x**2
    row = NLRow('tiny', SimpleNamespace(expr=expr, vars=[m.x]), [], [], F(0))
    cutter = SafeCutter(row, {id(m.x): (F(-1), F(1))})
    f, gradient = cutter.enclose([F(1, 3)])
    coefficient = F(.30000000000000004)-F(.1)-F(.2)
    for enclosure, expected in [(f, coefficient/9), (gradient[0], 2*coefficient/3)]:
        assert mpf_to_frac_down(enclosure.a) <= expected <= mpf_to_frac_down(enclosure.b)
    a, b, _ = cutter.safe_cut({id(m.x): F(1, 3)}, {id(m.x): 0.0}, 0.0)
    assert b <= 0  # minimum of the exact convex quadratic is zero


def test_singular_gradient_and_unsupported_function_fail_closed():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 1))
    row = NLRow('root', SimpleNamespace(expr=-pe.sqrt(m.x), vars=[m.x]))
    cutter = SafeCutter(row, {id(m.x): (F(0), F(1))})
    with pytest.raises(ValueError):
        cutter.enclose([F(0)])
    with pytest.raises(ExactModelError, match='unsupported'):
        validate_expression_domain(pe.sin(m.x))


def test_rational_rounding_handles_extreme_magnitudes_without_float_cast():
    cutter = object.__new__(SafeCutter)
    cutter.sig = 12
    for q in [F(1, 10**500), -F(1, 10**500), F(10**500), F(1, 3)]:
        assert cutter._round_dir(q, -1) <= q <= cutter._round_dir(q, 1)


def test_variable_domain_intersection_bounds_are_exact():
    m = pe.ConcreteModel()
    m.a = pe.Param(initialize=.1, mutable=True)
    m.b = pe.Param(initialize=.2, mutable=True)
    m.x = pe.Var(domain=pe.NonNegativeReals, bounds=(m.a+m.b, 1))
    m.y = pe.Var(domain=pe.Binary, bounds=(0, 1))
    assert exact_constant(m.x.lower) == F(.1)+F(.2)
    assert exact_constant(m.y.lower) == 0
    assert exact_constant(m.y.upper) == 1


@pytest.mark.parametrize('upper', [None, 3])
def test_geometric_mean_preserves_nonnegative_product_domain(upper):
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, upper))
    m.y = pe.Var(bounds=(0, upper))
    validate_expression_domain(pe.sqrt(m.x*m.y))
    assert certify(pe.sqrt(m.x*m.y)).curv == CONCAVE
