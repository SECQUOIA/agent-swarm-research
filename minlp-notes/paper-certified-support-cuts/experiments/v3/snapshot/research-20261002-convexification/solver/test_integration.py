"""Focused observable contracts of native SCIP model strengthening."""
from copy import deepcopy
from fractions import Fraction
import json

import numpy as np
import sympy as sp
import pytest

from solver.integration import (Block, Config, Instance, _sample, discover,
                                exact_expression, propose_direction, run_instance)
from solver.certified import certify_support, replay_support


def row(*, linear=None, quadratic=(), nonlinear=None, lower=-float("inf"), upper=float("inf")):
    return {"lin": linear or {}, "quad": list(quadratic), "nl": nonlinear,
            "lb": lower, "ub": upper}


def test_coupled_cut_is_valid_for_actual_exported_coefficients_and_separates():
    x, y = sp.symbols("x y", real=True)
    block = Block((0, 1), (), (x, y, x*x, x*y, y*y), (x, y), ((0, 1), (0, 1)),
                  (((1., 1.), 1.),))
    point = (.5, .5, .5, .5, .5)
    coefficients, activity, _ = propose_direction(block, point)
    supported = certify_support(block.features, block.symbols, block.box, coefficients,
                                rows=block.rows)
    assert supported.cut.rhs - activity > .5
    assert replay_support(block.features, block.symbols, block.box,
                          coefficients, block.rows, supported.witness)
    assert not replay_support(block.features, block.symbols, block.box,
                              tuple(c + .1 for c in coefficients), block.rows, supported.witness)
    assert max(Fraction(float(s)) * abs(Fraction(c)) for s, c in zip(block.scale, coefficients)) <= 1


def test_thin_non_dyadic_equality_has_exact_feasible_samples():
    x, y = sp.symbols("x y", real=True)
    block = Block((0, 1), (), (x, y, x*y), (x, y), ((0, 1), (0, 1)),
                  (((3., 0.), 1.), ((-3., 0.), -1.)))
    _sample(block, Config())
    assert any(p[0] == Fraction(1, 3) for p in block.sample_points)
    assert np.isfinite(block.sample).all()


def test_source_domains_are_not_lost_by_symbolic_deduplication():
    t = ("var", 0)
    square = ("square", t)
    root_square = ("power", ("sqrt", t), ("num", 4.))
    inst = Instance("source_domains", [-1.], [1.], ["C"], "min", 0.,
                    [row(nonlinear=("sum", square, root_square))])
    detected = discover(inst)
    assert len(detected.atoms) == 2
    assert detected.atoms[0].expr == detected.atoms[1].expr
    assert detected.atoms[0].tree != detected.atoms[1].tree
    for mode in ("baseline", "control", "all", "auto"):
        result = run_instance(inst, mode, time_limit=2)
        assert result["status"] == "source_model_mismatch"
        assert "domain" in result["diagnostic"]
        assert result["original_values"] is None


def test_exact_source_constants_do_not_round_during_symbolic_analysis():
    x = sp.Symbol("x", real=True)
    tree = ("times", ("num", .1), ("num", .1), ("var", 0))
    assert exact_expression(tree, (x,)) == sp.Rational(.1)**2*x
    assert exact_expression(tree, (x,)) != sp.Rational(.1*.1)*x


def test_native_modes_retain_constant_infeasibility_and_input_instance():
    inst = Instance("constant_infeasible", [0.], [1.], ["C"], "min", 0.,
                    [row(linear={0: 1.}), row(lower=1.)])
    original = deepcopy(inst)
    for mode in ("baseline", "control", "all", "auto"):
        result = run_instance(inst, mode, time_limit=2)
        assert result["status"] == "infeasible"
        assert result["primal"] is None
    assert inst == original


def test_real_scip_inserted_rows_replay_and_costs_are_not_double_counted():
    inst = Instance("dev_bilinear", [0., 0.], [1., 1.], ["C", "C"], "min", 0.,
                    [row(quadratic=[(0, 1, -1.)]), row(linear={0: 1., 1: 1.}, upper=1.)])
    result = run_instance(inst, "all", time_limit=3)
    assert abs(result["primal"] + .25) < 1e-5
    assert result["cuts"]
    detected = discover(inst)
    for cut in result["cuts"]:
        block = detected.blocks[cut["block"]]
        assert replay_support(block.features, block.symbols, block.box, cut["coefficients"],
                              block.rows, cut["certificate"])
        assert not cut["local"] and not cut["actual_row"]["local"]
        assert cut["actual_row"]["lhs"] - cut["actual_row"]["constant"] == cut["rhs"]
    assert result["total_seconds"] >= result["solve_wall_seconds"]
    assert result["solve_wall_seconds"] >= result["separation"]["callback_seconds"]
    json.dumps(result, allow_nan=False)


def test_overlap_discovery_merges_supported_stars_only():
    inst = Instance("dev_star", [0.] * 3, [1.] * 3, ["C"] * 3, "min", 0.,
                    [row(quadratic=[(0, 1, 1.), (0, 2, 1.), (0, 0, 1.),
                                    (1, 1, 1.), (2, 2, 1.)])])
    assert any(len(b.variables) == 3 and b.exact_quadratic for b in discover(inst).blocks)
    assert all(len(b.variables) <= 2 for b in discover(inst, Config(merge_stars=False)).blocks)
    inst.rows[0]["quad"].append((1, 2, 1.))
    assert all(len(b.variables) <= 2 for b in discover(inst).blocks)


def test_constant_cancellation_is_folded_exactly_in_every_mode():
    constant = ("sum", ("num", 1e16), ("num", 1.), ("num", -1e16))
    tree = ("square", ("sum", ("var", 0), constant))
    inst = Instance("constant_cancellation", [-1.], [1.], ["C"], "min", 0.,
                    [row(nonlinear=tree), row(linear={0: 1.}, lower=1., upper=1.)])
    for mode in ("baseline", "control", "all", "auto"):
        result = run_instance(inst, mode, time_limit=2)
        assert abs(result["primal"] - 4) < 1e-7


def test_rounded_native_source_row_is_refused_and_never_certified():
    tree = ("square", ("times", ("num", .1), ("num", .1), ("var", 0)))
    inst = Instance("rounded_native_atom", [-1.], [1.], ["C"], "min", 0.,
                    [row(nonlinear=tree)])
    for mode in ("control", "all", "auto"):
        result = run_instance(inst, mode, time_limit=2)
        assert result["status"] == "source_model_mismatch"
        assert result["cuts"] == [] and result["primal"] is None


def test_whole_row_native_coefficient_loss_is_rejected_in_every_mode():
    square = ("square", ("var", 0))
    product = ("times", ("var", 0), ("var", 0))
    tree = ("sum", ("times", ("num", 1e16), square), product,
            ("times", ("num", -1e16), square))
    inst = Instance("whole_row_loss", [-1.], [1.], ["C"], "min", 0., [row(nonlinear=tree)])
    for mode in ("baseline", "control", "all", "auto"):
        result = run_instance(inst, mode, time_limit=2)
        assert result["status"] == "source_model_mismatch"
        assert result["cuts"] == [] and result["primal"] is None


def test_finite_source_domains_cannot_become_scip_infinity():
    inst = Instance("finite_not_infinity", [-1.], [1e20], ["C"], "min", 0., [row(linear={0: 1.})])
    for mode in ("baseline", "control", "all", "auto"):
        result = run_instance(inst, mode, time_limit=2)
        assert result["status"] == "source_model_mismatch"
        assert "infinity" in result["diagnostic"]


def test_invalid_declared_domains_are_never_made_unbounded():
    for lo, hi in ((float("inf"), float("inf")), (-float("inf"), -float("inf")),
                   (float("nan"), 1.), (2., 1.)):
        for kind in ("variable", "row"):
            inst = Instance("invalid_domain", [0.], [1.], ["C"], "min", 0., [row(linear={0: 1.})])
            if kind == "variable":
                inst.var_lb, inst.var_ub = [lo], [hi]
            else:
                inst.rows.append(row(linear={0: 1.}, lower=lo, upper=hi))
            for mode in ("baseline", "control", "all", "auto"):
                result = run_instance(inst, mode, time_limit=2)
                assert result["status"] == "source_model_mismatch"
                assert result["primal"] is None
