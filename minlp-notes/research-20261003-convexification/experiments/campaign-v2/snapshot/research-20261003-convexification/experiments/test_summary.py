"""Guard against favorable counts from incomplete or inconsistent records."""
from summarize import compare, good, solved


def record(**changes):
    result = {"name": "case", "suite": "holdout", "phase": "full", "mode": "baseline",
              "status": "optimal", "sense": "min", "primal": 1.0, "dual": 1.0,
              "total_seconds": 1.0, "cuts": [],
              "reference_check": {"checked": False, "reason": "no finite reference"},
              "primal_check": {"checked": True, "passed": True}}
    result.update(changes)
    return result


def test_numerical_solve_requires_checked_incumbent_and_clean_worker():
    assert solved(record())
    for changes in ({"primal_check": {"checked": False}},
                    {"primal_check": {"checked": True, "passed": False}},
                    {"returncode": -9}, {"primal": None},
                    {"primal": float("nan")}, {"status": "process_timeout"},
                    {"reference_check": {"checked": True, "root_dual_consistent": False}},
                    {"reference_check": None}, {"primal_check": None}):
        assert not solved(record(**changes))


def test_failed_records_cannot_contribute_favorable_dual_comparisons():
    baseline = record()
    bad = record(mode="auto", dual=2.0, primal_check={"checked": True, "passed": False})
    assert not good(bad)
    comparison = compare([baseline, bad], "holdout", "full", "auto")
    assert comparison["outcomes"] == {"unavailable_or_flagged": 1}
    assert comparison["both_solved_count"] == 0


def test_bound_comparison_is_objective_sense_and_phase_aware():
    baseline = record(sense="max", dual=5.0, status="timelimit")
    strengthened = record(mode="auto", sense="max", dual=4.0, status="timelimit")
    unrelated_repeat = record(mode="auto", phase="repeat", sense="max", dual=100.0)
    comparison = compare([baseline, strengthened, unrelated_repeat], "holdout", "full", "auto")
    assert comparison["outcomes"] == {"better": 1}
    assert compare([baseline, record(mode="auto", dual=float("inf"))],
                   "holdout", "full", "auto")["outcomes"] == {"unavailable_or_flagged": 1}
