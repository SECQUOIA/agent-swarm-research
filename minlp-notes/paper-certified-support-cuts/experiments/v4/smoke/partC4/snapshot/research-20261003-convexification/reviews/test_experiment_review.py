"""Distinct checks for the independent record/primal audit, without solving."""
from dataclasses import asdict
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
from cases import instance, row, synthetic_cases
from audit_experiments import independent_primal, trusted_record


def test_known_witnesses_pass_independent_rational_evaluator():
    for case in synthetic_cases():
        check = independent_primal(asdict(case["instance"]), case["known_witness"], case["known_optimum"])
        assert check["passed"], (case["instance"].name, check)


def test_implicit_binary_domain_is_checked_without_declared_unit_bounds():
    model = asdict(instance("binary_semantics", [(-10, 10)], row(lin={0: 1}), types=["B"]))
    assert not independent_primal(model, [2.0], 2.0)["passed"]
    assert independent_primal(model, [1.0], 1.0)["passed"]


def test_exact_source_constants_and_uncancelled_domain_are_evaluated():
    # Exact binary inputs sum to one, despite the left-to-right float sum being zero.
    tree = ("sum", ("num", 1e16), ("num", 1.0), ("num", -1e16))
    model = asdict(instance("constant_arithmetic", [(0, 1)], row(nl=tree)))
    assert independent_primal(model, [0.0], 1.0)["passed"]
    assert not independent_primal(model, [0.0], 0.0)["passed"]
    # Multiplication by zero must not suppress an undefined source subexpression.
    model["rows"][0]["nl"] = ("times", ("num", 0.0), ("log", ("var", 0)))
    assert not independent_primal(model, [0.0], 0.0)["passed"]


def test_missing_checks_and_failed_reference_cannot_be_favorable():
    record = {"status": "optimal", "primal": 1.0,
              "primal_check": {"checked": True, "passed": True},
              "reference_check": {"checked": True, "dual_consistent": True, "root_dual_consistent": True}}
    assert trusted_record(record)
    for field in ("primal_check", "reference_check"):
        altered = dict(record)
        del altered[field]
        assert not trusted_record(altered)
    altered = {**record, "reference_check": {"checked": True, "dual_consistent": False, "root_dual_consistent": True}}
    assert not trusted_record(altered)
    assert not trusted_record({**record, "status": "invented_status"})
