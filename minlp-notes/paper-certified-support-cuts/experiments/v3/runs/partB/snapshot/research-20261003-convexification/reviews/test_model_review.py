"""Independent checks at the original-model admission boundary."""
from copy import deepcopy
from fractions import Fraction as Q
import itertools
import math
import random
from types import SimpleNamespace

import pytest

from solver.bounds import propagate_bounds, replay_bounds


def row(lin=None, *, nl=None, lower=-math.inf, upper=math.inf):
    return {"lin": lin or {}, "quad": [], "nl": nl,
            "lb": lower, "ub": upper}


def instance(lower, upper, rows=(), *, objective=None, types=None):
    return SimpleNamespace(name="independent_model_review", var_lb=list(lower),
                           var_ub=list(upper), var_type=types or ["C"]*len(lower),
                           var_names=[f"original_{i}" for i in range(len(lower))],
                           obj_sense="min", obj_const=0.0,
                           rows=[objective or row(), *rows])


def test_equality_implications_round_both_sides_outward():
    inst = instance([-math.inf], [math.inf], [row({0: 3.0}, lower=1.0, upper=1.0)])
    result = propagate_bounds(inst)
    assert result.lower == result.upper == (Q(1, 3),)
    assert Q(result.float_lower[0]) <= Q(1, 3) <= Q(result.float_upper[0])
    assert result.float_lower[0] != result.float_upper[0]
    assert replay_bounds(inst, result.certificate)


def test_negative_unbounded_implication_and_chained_integer_rounding():
    inst = instance([-math.inf, -math.inf], [math.inf, math.inf],
                    [row({0: 3.0}, upper=-1.0),
                     row({1: 1.0, 0: -1.0}, upper=0.0)], types=["C", "I"])
    result = propagate_bounds(inst)
    assert result.upper == (Q(-1, 3), Q(-1))
    assert all(x == -math.inf for x in result.lower)
    assert replay_bounds(inst, result.certificate)


def test_budget_prefix_never_invents_unfinished_deductions():
    inst = instance([-math.inf]*3, [math.inf]*3,
                    [row({0: 1.0}, lower=1.0),
                     row({1: 1.0, 0: -1.0}, lower=0.0),
                     row({2: 1.0, 1: -1.0}, lower=0.0)])
    for steps in range(4):
        result = propagate_bounds(inst, max_steps=steps)
        assert len(result.certificate["steps"]) <= steps
        assert replay_bounds(inst, result.certificate)
        assert result.lower == tuple(Q(1) if j < steps else -math.inf for j in range(3))


def test_nonlinear_and_objective_rows_are_not_bound_premises():
    inst = instance([-math.inf], [math.inf],
                    [row({0: 1.0}, nl=("times", ("num", 0.0),
                                               ("log", ("var", 0))), lower=2.0)],
                    objective=row({0: 1.0}, lower=3.0))
    result = propagate_bounds(inst)
    assert result.lower == (-math.inf,) and result.upper == (math.inf,)
    assert not result.certificate["binding"]["rows"]


def _vertices_2d(inst):
    """Separate exact intersection enumeration; no propagation code is used."""
    sides = [(Q(1), Q(0), Q(inst.var_ub[0])),
             (Q(-1), Q(0), -Q(inst.var_lb[0])),
             (Q(0), Q(1), Q(inst.var_ub[1])),
             (Q(0), Q(-1), -Q(inst.var_lb[1]))]
    for r in inst.rows[1:]:
        a, b = Q(r["lin"].get(0, 0)), Q(r["lin"].get(1, 0))
        if math.isfinite(r["ub"]):
            sides.append((a, b, Q(r["ub"])))
        if math.isfinite(r["lb"]):
            sides.append((-a, -b, -Q(r["lb"])))
    vertices = set()
    for (a, b, c), (d, e, f) in itertools.combinations(sides, 2):
        determinant = a*e-b*d
        if not determinant:
            continue
        x, y = (c*e-b*f)/determinant, (a*f-c*d)/determinant
        if all(g*x+h*y <= k for g, h, k in sides):
            vertices.add((x, y))
    return vertices


def test_random_continuous_polygons_retain_every_exact_vertex():
    rng = random.Random(813048)
    for _ in range(120):
        rows = [row({0: rng.randrange(-3, 4), 1: rng.randrange(-3, 4)},
                    upper=rng.randrange(-4, 8)) for _ in range(4)]
        inst = instance([-3.0, -3.0], [3.0, 3.0], rows)
        vertices = _vertices_2d(inst)
        result = propagate_bounds(inst)
        assert replay_bounds(inst, result.certificate)
        if vertices:
            assert not result.infeasible
            for point in vertices:
                assert all(lo <= value <= hi for value, lo, hi in
                           zip(point, result.lower, result.upper))


def test_proof_edits_and_changed_original_premises_are_rejected():
    inst = instance([-math.inf, -math.inf], [math.inf, math.inf],
                    [row({0: 3.0}, lower=1.0),
                     row({1: 1.0, 0: -1.0}, lower=0.0)])
    certificate = propagate_bounds(inst).certificate
    assert len(certificate["steps"]) == 2
    for field, value in [("row", 1), ("side", "upper"), ("variable", 1),
                         ("new", "1"), ("old", "0"), ("bound", "upper"),
                         ("kind", "integer")]:
        altered = deepcopy(certificate)
        altered["steps"][0][field] = value
        assert not replay_bounds(inst, altered), (field, value)
    altered = deepcopy(certificate)
    altered["steps"].reverse()
    assert not replay_bounds(inst, altered)
    altered = deepcopy(certificate)
    altered["result"]["float_lower"][0] = float(Q(1, 3)).hex()
    # The nearest float is already the valid lower rounding of 1/3; move inward.
    altered["result"]["float_lower"][0] = math.nextafter(float(Q(1, 3)), math.inf).hex()
    assert not replay_bounds(inst, altered)
    for index, field, value in [(1, "lb", 0.0), (1, "lin", {0: 2.0}),
                                (2, "nl", ("num", 0.0))]:
        altered_inst = deepcopy(inst)
        altered_inst.rows[index][field] = value
        assert not replay_bounds(altered_inst, certificate)


@pytest.mark.parametrize("bad", [None, [], {}, True, {"schema": "bogus"}])
def test_malformed_proofs_return_false(bad):
    assert not replay_bounds(instance([0.0], [1.0]), bad)


def _build(inst):
    from solver.model import build_model
    built = build_model(inst)
    built.model.hideOutput()
    built.model.setIntParam("parallel/maxnthreads", 1)
    built.model.setRealParam("limits/time", 3.0)
    return built


def _solve(built):
    built.model.optimize()
    assert built.model.getNSols() > 0
    solution = built.model.getBestSol()
    return tuple(built.model.getSolVal(solution, x) for x in built.xs)


def test_original_unbounded_affine_equality_proves_log_domain():
    built = _build(instance([-math.inf], [math.inf],
                            [row({0: 3.0}, lower=1.0, upper=1.0)],
                            objective=row(nl=("log", ("var", 0)))))
    assert built.exact_bounds == ((Q(1, 3), Q(1, 3)),)
    assert not built.metadata["domain_guards"]
    point = _solve(built)
    assert point[0] == pytest.approx(1/3, abs=1e-7)
    built.model.freeProb()


def test_unbounded_difference_equality_proves_direct_affine_argument():
    argument = ("sum", ("var", 0), ("negate", ("var", 1)))
    built = _build(instance([-math.inf]*2, [math.inf]*2,
                            [row({0: 1.0, 1: -1.0}, lower=1.0, upper=1.0)],
                            objective=row(nl=("log", argument))))
    assert not built.metadata["domain_guards"]
    point = _solve(built)
    assert point[0]-point[1] == pytest.approx(1.0, abs=1e-7)
    built.model.freeProb()


def test_canceled_sqrt_domain_guard_retains_original_feasible_set():
    canceled = ("times", ("num", 0.0), ("sqrt", ("var", 0)))
    built = _build(instance([-1.0], [1.0], objective=row({0: 1.0}, nl=canceled)))
    assert [g["kind"] for g in built.metadata["domain_guards"]] == ["nonnegative"]
    point = _solve(built)
    assert point[0] >= -1e-7
    built.model.freeProb()


@pytest.mark.parametrize("domain_tree,kind", [
    (("log", ("var", 0)), "positive"),
    (("divide", ("num", 1.0), ("var", 0)), "nonzero"),
])
def test_canceled_open_domains_use_exact_witness_guards(domain_tree, kind):
    canceled = ("power", domain_tree, ("num", 0.0))
    built = _build(instance([-1.0], [1.0], objective=row(nl=canceled)))
    guards = built.metadata["domain_guards"]
    assert len(guards) == 1 and guards[0]["kind"] == kind
    assert guards[0]["witness"] is not None
    variables = {v.name: v for v in built.model.getVars()}
    witness = variables[guards[0]["witness"]]
    assert witness.getUbOriginal() >= built.model.infinity()
    if kind == "positive":
        assert witness.getLbOriginal() == 0
    else:
        assert witness.getLbOriginal() <= -built.model.infinity()
    point = _solve(built)
    assert point[0] > 0 if kind == "positive" else point[0] != 0
    built.model.freeProb()


@pytest.mark.parametrize("types,exponent_bounds,rows", [
    (["C", "I"], (2.0, 3.0), ()),
    (["C", "C"], (-math.inf, math.inf), (row({1: 1.0}, lower=2.0, upper=2.0),)),
])
def test_negative_base_variable_power_is_not_silently_restricted(types, exponent_bounds, rows):
    from solver.model import ModelAdmissionError
    with pytest.raises(ModelAdmissionError) as caught:
        _build(instance([-2.0, exponent_bounds[0]], [-1.0, exponent_bounds[1]], rows,
                        types=types, objective=row(nl=("power", ("var", 0), ("var", 1)))))
    assert caught.value.status == "unsupported_variable_power_domain"


def test_positive_base_variable_power_preserves_analytic_optimum():
    built = _build(instance([0.5, -2.0], [2.0, 2.0],
                            objective=row(nl=("power", ("var", 0), ("var", 1)))))
    point = _solve(built)
    assert point[0]**point[1] == pytest.approx(0.25, abs=1e-6)
    assert not built.metadata["domain_guards"]
    built.model.freeProb()


def test_full_row_fallback_keeps_exact_source_coefficient_sum():
    # Fast polynomial assembly merges 1e16 + 1 - 1e16 to zero.
    tree = ("sum", ("times", ("num", 1e16), ("var", 0)),
            ("var", 0), ("times", ("num", -1e16), ("var", 0)))
    built = _build(instance([1.0], [2.0], objective=row(nl=tree)))
    assert built.source_rows[0] == built.source_symbols[0]
    assert built.metadata["generic_fallback_rows"] == [0]
    # Native SCIP's later numerical folding is outside the checked boundary;
    # this test asserts admitted DAG binding, not exact numerical optimization.
    built.model.freeProb()


@pytest.mark.parametrize("constant_row", [row(lower=0.0, upper=0.0),
                                           row(nl=("num", 1.0), lower=1.0, upper=1.0)])
def test_feasible_constant_rows_do_not_become_python_boolean_constraints(constant_row):
    built = _build(instance([0.0], [1.0], [constant_row], objective=row({0: 1.0})))
    assert _solve(built)[0] == pytest.approx(0.0, abs=1e-7)
    built.model.freeProb()


def test_negative_fixed_integer_power_on_negative_unbounded_base():
    built = _build(instance([-math.inf], [-1.0],
                            [row({0: 1.0}, lower=-2.0)],
                            objective=row(nl=("power", ("var", 0), ("num", -2.0)))))
    assert not built.metadata["domain_guards"]
    point = _solve(built)
    assert point[0]**-2 == pytest.approx(0.25, abs=1e-6)
    built.model.freeProb()


@pytest.mark.parametrize("invalid", [
    ("times", ("num", 0.0), ("log", ("num", -1.0))),
    ("power", ("divide", ("num", 1.0), ("num", 0.0)), ("num", 0.0)),
    ("times", ("num", 0.0), ("sqrt", ("num", -1.0))),
])
def test_cancellation_never_makes_undefined_constant_source_defined(invalid):
    from solver.model import ModelAdmissionError
    with pytest.raises(ModelAdmissionError) as caught:
        _build(instance([0.0], [1.0], objective=row(nl=invalid)))
    assert caught.value.status == "source_domain_infeasible"


def test_generic_nested_coefficient_product_preserves_exact_binary_leaves():
    tree = ("times", ("num", 0.1),
            ("times", ("num", 0.1), ("square", ("var", 0))))
    built = _build(instance([1.0], [2.0], objective=row(nl=tree)))
    import sympy as sp
    assert built.source_rows[0] == sp.Rational(0.1)**2*built.source_symbols[0]**2
    assert built.metadata["generic_fallback_rows"] == [0]
    built.model.freeProb()


def test_row_constant_is_not_rounded_into_a_different_side():
    constraint = row(nl=("sum", ("var", 0), ("num", 0.01)), lower=0.1, upper=0.1)
    built = _build(instance([0.0], [1.0], [constraint], objective=row({0: 1.0})))
    assert built.metadata["generic_fallback_rows"] == [1]
    cons = next(c for c in built.model.getConss() if c.name == "source_row_1")
    assert built.model.getLhs(cons) == 0.1
    assert built.model.getRhs(cons) == 0.1
    assert Q(0.1)-Q(0.01) != Q(0.1-0.01)
    built.model.freeProb()


def _guarded_review_instance():
    tree = ("sum", ("times", ("num", 0.0), ("log", ("var", 0))),
            ("times", ("num", 0.0), ("divide", ("num", 1.0), ("var", 1))),
            ("times", ("num", 0.0), ("sqrt", ("var", 2))))
    return instance([-1.0]*3, [1.0]*3, objective=row(nl=tree))


def test_saved_model_metadata_replays_all_guard_kinds_and_json_paths():
    import json
    from model_binding_audit import replay_model_metadata
    original = _guarded_review_instance()
    built = _build(original)
    metadata = json.loads(json.dumps(built.metadata))
    assert [g["kind"] for g in metadata["domain_guards"]] == ["positive", "nonzero", "nonnegative"]
    assert replay_model_metadata(original, metadata)
    built.model.freeProb()


def test_metadata_replay_rejects_guard_equations_sides_scope_and_changed_source():
    from model_binding_audit import replay_model_metadata
    original = _guarded_review_instance()
    built = _build(original)
    metadata = deepcopy(built.metadata)
    built.model.freeProb()
    for field, value in [("kind", "nonzero"), ("row", 2), ("path", (0,)),
                         ("witness", "wrong_witness"), ("argument", "Integer(1)"),
                         ("constraint", "wrong_constraint"),
                         ("submitted_expression", "Integer(1)"),
                         ("submitted_lhs", 0.0), ("submitted_rhs", None),
                         ("stored_lhs", 0.0), ("stored_rhs", 2.0),
                         ("witness_bounds", [-1e20, 1e20]),
                         ("scip_infinity", 1e30)]:
        bad = deepcopy(metadata)
        bad["domain_guards"][0][field] = value
        assert not replay_model_metadata(original, bad), field
    for field, value in [("source_variables", ["v1", "v0", "v2"]),
                         ("objective_variable", None), ("domain_requirements", 0),
                         ("proved_domain_requirements", 3),
                         ("generic_fallback_rows", [0]),
                         ("binding_boundary", "exact SCIP solve")]:
        bad = deepcopy(metadata)
        bad[field] = value
        assert not replay_model_metadata(original, bad), field
    bad = deepcopy(metadata)
    bad["domain_guards"].pop()
    assert not replay_model_metadata(original, bad)
    changed_original = deepcopy(original)
    changed_original.rows[0]["nl"] = ("num", 0.0)
    assert not replay_model_metadata(changed_original, metadata)


def test_metadata_replay_checks_proved_domains_against_original_affine_rows():
    from model_binding_audit import replay_model_metadata
    original = instance([-math.inf], [math.inf],
                        [row({0: 3.0}, lower=1.0, upper=1.0)],
                        objective=row(nl=("log", ("var", 0))))
    built = _build(original)
    metadata = deepcopy(built.metadata)
    built.model.freeProb()
    assert not metadata["domain_guards"]
    assert replay_model_metadata(original, metadata)
    changed_original = deepcopy(original)
    changed_original.rows[1]["lb"] = -1.0
    assert not replay_model_metadata(changed_original, metadata)
