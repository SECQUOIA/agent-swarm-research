"""Observable source-domain, exact-row, and model-construction regressions."""
from fractions import Fraction
import math

import pytest
import sympy as sp

from solver.model import (Instance, ModelAdmissionError, build_model,
                          expression, generic_expression, native_expression)


def row(nl=None, lin=None, *, lb=-math.inf, ub=math.inf):
    return {"lin": lin or {}, "quad": [], "nl": nl, "lb": lb, "ub": ub}


def instance(bounds, objective=None, constraints=(), types=None):
    return Instance("model_contract", [b[0] for b in bounds], [b[1] for b in bounds],
                    types or ["C"]*len(bounds), "min", 0.0,
                    [objective or row(), *constraints])


def test_one_sided_unbounded_log_and_reciprocal_need_no_witness():
    for op, bounds in [("log", (0.001, math.inf)), ("divide", (-math.inf, -0.001))]:
        tree = (op, ("var", 0)) if op == "log" else (op, ("num", 1.0), ("var", 0))
        built = build_model(instance([bounds], row(tree)))
        assert built.metadata["proved_domain_requirements"] == 1
        assert built.metadata["domain_guards"] == []
        built.model.freeProb()


def test_exact_affine_deduction_proves_strict_log_domain_and_rounds_outward():
    built = build_model(instance([(-math.inf, math.inf)], row(("log", ("var", 0))),
                                 [row(lin={0: 3.0}, lb=1.0)]))
    assert built.exact_bounds[0][0] == Fraction(1, 3)
    assert Fraction(built.bounds[0][0]) <= Fraction(1, 3)
    assert not built.metadata["domain_guards"]
    built.model.freeProb()


def test_affine_argument_domain_from_unbounded_equality():
    difference = ("sum", ("var", 0), ("negate", ("var", 1)))
    built = build_model(instance([(-math.inf, math.inf)]*2, row(("log", difference)),
                                 [row(lin={0: 1.0, 1: -1.0}, lb=1.0, ub=1.0)]))
    assert all(math.isinf(b) for pair in built.bounds for b in pair)
    assert not built.metadata["domain_guards"]
    built.model.freeProb()


@pytest.mark.parametrize("tree,kind", [
    (("times", ("num", 0.0), ("log", ("var", 0))), "positive"),
    (("power", ("log", ("var", 0)), ("num", 0.0)), "positive"),
    (("square", ("sqrt", ("var", 0))), "nonnegative"),
    (("divide", ("var", 0), ("var", 0)), "nonzero"),
])
def test_cancellation_cannot_remove_original_domains(tree, kind):
    built = build_model(instance([(-1.0, 1.0)], row(tree)))
    assert [g["kind"] for g in built.metadata["domain_guards"]] == [kind]
    if kind != "nonnegative":
        witness = next(v for v in built.model.getVars() if v.name.startswith("source_domain_witness"))
        assert (witness.getLbOriginal() == 0) == (kind == "positive")
    built.model.freeProb()


def test_variable_exponents_retain_log_node_without_irrational_float_coefficient():
    built = build_model(instance([(0, 1), (-2, 2)], row(("power", ("num", 2.0),
                                                        ("sum", ("var", 0), ("var", 1))))))
    expected = sp.exp((built.source_symbols[0]+built.source_symbols[1])*sp.log(2))
    assert built.source_rows[0] == expected
    assert built.metadata["generic_fallback_rows"] == [0]
    assert not built.metadata["domain_guards"]
    built.model.freeProb()


def test_positive_variable_base_and_exponent_are_supported():
    tree = ("power", ("var", 0), ("var", 1))
    built = build_model(instance([(0.5, 2), (-2, 2)], row(tree)))
    assert built.source_rows[0] == sp.exp(built.source_symbols[1]*sp.log(built.source_symbols[0]))
    built.model.freeProb()


@pytest.mark.parametrize("bounds,types", [([(-2, -1), (2, 3)], ["C", "I"]),
                                         ([(0, 1), (1, 2)], ["C", "C"])])
def test_positive_power_rewrite_must_not_discard_valid_nonpositive_bases(bounds, types):
    with pytest.raises(ModelAdmissionError) as error:
        build_model(instance(bounds, row(("power", ("var", 0), ("var", 1))), types=types))
    assert error.value.status == "unsupported_variable_power_domain"


def test_generic_dag_avoids_product_constant_rounding():
    tree = ("square", ("times", ("num", 0.1), ("var", 0)))
    built = build_model(instance([(1, 2)], row(tree)))
    assert built.metadata["generic_fallback_rows"] == [0]
    assert built.source_rows[0].coeff(built.source_symbols[0], 2) == sp.Rational(0.1)**2
    built.model.freeProb()


def test_constant_arithmetic_cancellation_is_exact_before_compilation():
    tree = ("square", ("sum", ("var", 0), ("sum", ("num", 1e16), ("num", 1), ("num", -1e16))))
    built = build_model(instance([(0, 1)], row(tree)))
    assert sp.expand(built.source_rows[0]-(built.source_symbols[0]+1)**2) == 0
    built.model.freeProb()


def test_row_constant_side_shift_is_not_rounded_in_python():
    constraint = row(("sum", ("var", 0), ("num", 0.1)), ub=0.3)
    built = build_model(instance([(0, 1)], row(lin={0: -1}), [constraint]))
    assert built.metadata["generic_fallback_rows"] == [1]
    assert built.source_rows[1] == built.source_symbols[0]+sp.Rational(0.1)
    built.model.hideOutput(); built.model.optimize()
    assert abs(built.model.getVal(built.xs[0])-0.2) < 1e-7
    built.model.freeProb()


def test_ranged_equalities_and_integer_semantics_survive():
    built = build_model(instance([(0, 5)], row(lin={0: -1}),
                                 [row(lin={0: 3}, lb=6, ub=6)], types=["I"]))
    built.model.hideOutput(); built.model.optimize()
    assert built.model.getStatus() == "optimal"
    assert built.model.getVal(built.xs[0]) == 2
    built.model.freeProb()


@pytest.mark.parametrize("constraint", [row(lb=0, ub=0), row(("num", 1.0), lb=1, ub=1)])
def test_feasible_constant_rows_build(constraint):
    built = build_model(instance([(0, 1)], constraints=[constraint]))
    built.model.hideOutput(); built.model.optimize()
    assert built.model.getStatus() == "optimal"
    built.model.freeProb()


def test_unsupported_operator_has_structured_status():
    with pytest.raises(ModelAdmissionError) as error:
        build_model(instance([(0, 1)], row(("unknown", ("var", 0)))))
    assert error.value.status == "unsupported_operator"
