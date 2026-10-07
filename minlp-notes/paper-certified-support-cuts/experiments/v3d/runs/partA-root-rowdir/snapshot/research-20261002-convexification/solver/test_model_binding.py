"""Regressions for exact certificate binding to constructed native models."""
import math

import pytest
import sympy as sp

from solver.model_binding import (assert_source_domains, native_expression, normalize_constant_trees,
                                  same_expression, source_expression)


x, y = sp.symbols("x y", real=True)


def test_constant_cancellation_is_folded_before_rounding():
    tree = ("sum", ("sum", ("num", 1e16), ("num", 1.0)),
            ("num", -1e16))
    assert normalize_constant_trees(tree) == ("num", 1.0)
    assert source_expression(tree, ()) == 1


@pytest.mark.parametrize("tree", [
    ("times", ("num", 0.1), ("num", 0.1)),
    ("divide", ("num", 1.0), ("num", 3.0)),
    ("power", ("num", 2.0), ("num", 0.5)),
    ("times", ("num", 1e308), ("num", 1e308)),
])
def test_nonrepresentable_constant_arithmetic_remains_native(tree):
    assert normalize_constant_trees(tree) == tree


def test_variable_domain_operations_are_preserved():
    tree = ("power", ("sqrt", ("var", 0)), ("num", 4.0))
    assert normalize_constant_trees(tree) == tree
    # Algebraic equality alone must not replace the original domain-bearing
    # native definition. Here the source domain still requires x >= 0.
    assert source_expression(tree, (x,)) == x*x
    invalid = ("power", ("divide", ("num", 1.0), ("num", 0.0)),
               ("num", 0.0))
    assert normalize_constant_trees(invalid) == invalid


def test_constant_subtrees_inside_elementary_functions_are_folded():
    tree = ("log", ("sum", ("num", 1e16), ("num", 1.0),
                     ("num", -1e16)))
    assert normalize_constant_trees(tree) == ("log", ("num", 1.0))


def test_polynomial_native_coefficients_expose_rounding():
    ps = pytest.importorskip("pyscipopt")
    model = ps.Model()
    vx = model.addVar("vx")
    mapping = {"vx": x}
    original = ("times", ("num", 0.1),
                ("times", ("num", 0.1), ("square", ("var", 0))))
    native = native_expression(0.1 * (0.1 * vx**2), mapping)
    assert native == sp.Rational(0.1 * 0.1) * x*x
    assert not same_expression(source_expression(original, (x,)), native)
    assert same_expression(source_expression(("square", ("var", 0)), (x,)),
                           native_expression(vx**2, mapping))


def test_all_native_generic_nodes_and_binary_exponents():
    ps = pytest.importorskip("pyscipopt")
    model = ps.Model()
    vx, vy = model.addVar("vx"), model.addVar("vy")
    mapping = {"vx": x, "vy": y}
    native = (0.25 * ps.exp(vx) + ps.log(vy) + ps.sqrt(vy)
              + ps.sin(vx) + ps.cos(vx) + abs(vx) + vx**0.3 + vx/vy + 2)
    expected = (sp.exp(x)/4 + sp.log(y) + sp.sqrt(y) + sp.sin(x)
                + sp.cos(x) + sp.Abs(x) + x**sp.Rational(0.3) + x/y + 2)
    assert same_expression(native_expression(native, mapping), expected)
    assert native_expression(ps.scip.Constant(0.1), mapping) == sp.Rational(0.1)


def test_native_generic_coefficient_rounding_is_also_detected():
    ps = pytest.importorskip("pyscipopt")
    model = ps.Model()
    vx = model.addVar("vx")
    native = native_expression(0.1 * (0.1 * ps.exp(vx)), {"vx": x})
    assert native == sp.Rational(0.1 * 0.1) * sp.exp(x)
    assert not same_expression(sp.Rational(0.1)**2 * sp.exp(x), native)


def test_native_unknown_variable_and_nonfinite_numbers_fail_closed():
    ps = pytest.importorskip("pyscipopt")
    model = ps.Model()
    vx = model.addVar("vx")
    with pytest.raises(ValueError, match="unbound"):
        native_expression(vx, {})
    for bad in (math.inf, -math.inf, math.nan):
        with pytest.raises(ValueError, match="nonfinite"):
            native_expression(bad, {})


def test_native_sum_uses_explicit_coefficients():
    ps = pytest.importorskip("pyscipopt")
    model = ps.Model()
    vx = model.addVar("vx")
    expression = ps.scip.SumExpr()
    expression.children = [ps.scip.VarExpr(vx)]
    expression.coefs = [0.1]
    expression.constant = 0.3
    assert native_expression(expression, {"vx": x}) == (
        sp.Rational(0.1)*x + sp.Rational(0.3))


@pytest.mark.parametrize("tree", [
    ("times", ("num", 0.0), ("sqrt", ("var", 0))),
    ("times", ("num", 0.0), ("log", ("var", 0))),
    ("sum", ("divide", ("num", 1.0), ("var", 0)),
     ("negate", ("divide", ("num", 1.0), ("var", 0)))),
    ("power", ("log", ("var", 0)), ("num", 0.0)),
    ("power", ("var", 0), ("num", -2.0)),
    ("power", ("var", 0), ("num", 0.5)),
])
def test_source_domains_survive_zero_factors_and_cancellation(tree):
    with pytest.raises(ValueError, match="source .* domain"):
        assert_source_domains(tree, ((-1.0, 1.0),))


def test_source_domains_accept_valid_bounds_and_unrestricted_unbounded_nodes():
    assert_source_domains(("log", ("var", 0)), ((0.25, 2.0),))
    assert_source_domains(("sqrt", ("var", 0)), ((0.0, 2.0),))
    assert_source_domains(("power", ("var", 0), ("num", -2.0)), ((-2.0, -0.25),))
    assert_source_domains(("exp", ("var", 0)), ((-math.inf, math.inf),))
    with pytest.raises(ValueError, match="strictly positive"):
        assert_source_domains(("log", ("var", 0)), ((0.0, 2.0),))
    with pytest.raises(ValueError, match="domain"):
        assert_source_domains(("sqrt", ("var", 0)), ((0.0, math.inf),))


def test_source_domain_checks_use_exact_arithmetic_and_elementary_bounds():
    # Exact cancellation is safe before log; binary64 sequential sums lose it.
    tree = ("log", ("sum", ("num", 1e16), ("num", 1.0), ("num", -1e16)))
    assert_source_domains(tree, ())
    pytest.importorskip("flint")
    assert_source_domains(("log", ("exp", ("var", 0))), ((-1.0, 1.0),))
    with pytest.raises(ValueError, match="log"):
        assert_source_domains(("log", ("sin", ("var", 0))), ((-1.0, 1.0),))
