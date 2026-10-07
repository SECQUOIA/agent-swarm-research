"""Independent exact boundary checks for the adaptive OBBT theory review.

This script checks mathematical scope failures as well as accepted certificates.
It is not a solver-performance experiment or a proof of uniform contraction.
Run with standard-library Python from any working directory.
"""

from dataclasses import replace
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys


MODULE = Path(__file__).resolve().parents[1] / "theory" / "certificates.py"
SPEC = importlib.util.spec_from_file_location("review_certificates", MODULE)
cert = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cert
SPEC.loader.exec_module(cert)


def must_reject(function, *args):
    try:
        function(*args)
    except (ValueError, TypeError):
        return
    raise AssertionError("An invalid certificate was accepted")


def check_scope_boundaries():
    model = cert.Model(1, ((0, 0),), (), (0, 1))
    outer = cert.Box((-1,), (1,))
    half = cert.Box((F(-1, 2),), (F(1, 2),))
    frozen_witnesses = ((F(-1, 2), 0), (F(1, 2), 0))

    # Endpoint points from the first round are valid on the old LP only.
    assert cert.current_round_ceilings(model, outer, 0, frozen_witnesses) == (
        (F(1, 2),), (F(1, 2),)
    )
    must_reject(cert.verify_protected_box, model, outer, half, 0, frozen_witnesses)
    must_reject(cert.ProtectedBox, model, half, frozen_witnesses)
    # Indeed, the finite square LP with zero cutoff halves [-h,h] each round.
    h = F(1)
    for _ in range(12):
        box = cert.Box((-h,), (h,))
        assert model.feasible(box, (h / 2, 0), 0)
        assert not model.feasible(box, (h / 2 + h / 100, 0), 0)
        h /= 2

    # On cutoff 1/4, actual endpoints protect the half interval. An additional
    # nongraph point at its center certifies a relaxation ceiling of -1/4.
    witnesses = ((F(-1, 2), F(1, 4)), (F(1, 2), F(1, 4)), (0, F(-1, 4)))
    protected = cert.verify_protected_box(model, outer, half, F(1, 4), witnesses)
    assert protected.objective_ceiling == F(-1, 4)
    assert protected.required_cutoff == F(1, 4)
    assert protected.reusable(model, half, F(1, 4))
    assert protected.reusable(model, outer, 1)
    assert not protected.reusable(model, outer, 0)
    assert not protected.reusable(model, cert.Box((0,), (1,)), 1)
    strengthened = replace(model, rows=(cert.Row((0, -1), 0),))
    assert not protected.reusable(strengthened, outer, 1)
    assert not strengthened.feasible(half, (0, F(-1, 4)))

    # An original-feasibility statement would be false: x^2 >= 0, whereas the
    # LP admits w=-1/4. Integer rounding also removes the fractional faces.
    assert witnesses[2][1] < witnesses[2][0] ** 2
    rounded = cert.Box((0,), (0,))
    assert not rounded.contains(half)

    # Mixing after an incumbent improvement preserves the frozen outer LP,
    # but it does not repair a permanent certificate on the smaller hull.
    mixed = tuple(
        cert.mix_for_cutoff(model, outer, (s, 1), (0, -1), 0)
        for s in (-1, 1)
    )
    assert mixed == frozen_witnesses
    must_reject(cert.verify_protected_box, model, outer, half, 0, mixed)
    return 7


def check_nested_mccormick():
    checks = 0
    # Independently form feasible nongraph lifted values from envelope bounds.
    # Testing repeated indices catches the special square coefficient case.
    for diagonal in (False, True):
        products = ((0, 0),) if diagonal else ((0, 1),)
        dimension = 1 if diagonal else 2
        model = cert.Model(dimension, products, (), (0,) * (dimension + 1))
        outer = cert.Box((-3,) * dimension, (4,) * dimension)
        for left in range(-3, 4):
            for right in range(left, 5):
                inner = cert.Box((left,) * dimension, (right,) * dimension)
                for r in (F(0), F(1, 3), F(1, 2), F(1)):
                    x = left + r * (right - left)
                    for s in (F(0), F(1, 3), F(1, 2), F(1)):
                        y = x if diagonal else left + s * (right - left)
                        lower = max(left * (x + y) - left * left,
                                    right * (x + y) - right * right)
                        upper = min(right * x + left * y - left * right,
                                    left * x + right * y - left * right)
                        assert lower <= upper
                        for w in (lower, (lower + upper) / 2, upper):
                            point = (x, w) if diagonal else (x, y, w)
                            assert model.feasible(inner, point)
                            assert model.feasible(outer, point)
                            checks += 1
    return checks


def interpolate(knots, x):
    for (a, fa), (b, fb) in zip(knots, knots[1:]):
        if a <= x <= b:
            return fa + (x - a) * (fb - fa) / (b - a)
    raise ValueError("Point outside interpolation interval")


def check_observed_ratio_failure():
    fast = tuple((F(x), F(y)) for x, y in
                 ((0, 0), ("1/10", 0), ("899/1000", "1/10"),
                  ("9/10", "899/1000"), (1, "9/10")))
    stall = tuple((F(x), F(y)) for x, y in
                  ((0, 0), ("899/1000", "899/1000"),
                   ("9/10", "899/1000"), (1, "9/10")))
    for knots in (fast, stall):
        assert all(y <= x for x, y in knots)
        assert all(fa <= fb for (_, fa), (_, fb) in zip(knots, knots[1:]))
    paths = []
    for knots in (fast, stall):
        widths = [F(1)]
        for _ in range(4):
            widths.append(interpolate(knots, widths[-1]))
        paths.append(widths)
    assert paths[0][:3] == paths[1][:3] == [F(1), F(9, 10), F(899, 1000)]
    assert paths[0][-1] == 0 and paths[1][-1] == F(899, 1000)
    observed_ratio = (paths[0][1] - paths[0][2]) / (paths[0][0] - paths[0][1])
    predicted_tail_after_first = (paths[0][1] - paths[0][2]) / (1 - observed_ratio)
    assert paths[0][1] - paths[0][-1] > 800 * predicted_tail_after_first
    return {
        "common_width_prefix": [str(v) for v in paths[0][:3]],
        "observed_decrement_ratio": str(observed_ratio),
        "actual_remaining_after_first": str(paths[0][1]),
        "unjustified_geometric_prediction": str(predicted_tail_after_first),
    }


def check_tail_majorant_boundary():
    # rho(M)=1 is allowed when residual has no component in that eigenspace.
    matrix = ((1, 0), (0, F(1, 2)))
    residual, majorant = (0, 1), (5, 2)
    assert cert.check_tail_majorant(matrix, residual, majorant)
    increment = tuple(F(v) for v in residual)
    total = (F(0), F(0))
    for _ in range(50):
        total = tuple(a + b for a, b in zip(total, increment))
        assert all(a <= b for a, b in zip(total, majorant))
        increment = tuple(sum(F(a) * b for a, b in zip(row, increment)) for row in matrix)
    assert not cert.check_tail_majorant(matrix, (1, 1), majorant)
    assert not cert.check_tail_majorant(((1, -1), (0, 1)), residual, majorant)
    return 50


def check_constrained_supports():
    # Independent vertex enumeration, without the author's basis solver.
    from itertools import combinations

    rows = ((-1, 0), (0, -1), (1, 0), (0, 1), (1, -1), (4, -1), (1, 0), (0, 1))
    count = 0
    for numerator in range(65):
        cutoff = F(numerator, 16)
        rhs = (F(0), F(0), F(3), F(4), F(1), F(7), F(5, 2), cutoff)
        vertices = []
        for i, j in combinations(range(len(rows)), 2):
            a, b = rows[i]
            c, d = rows[j]
            determinant = a * d - b * c
            if determinant == 0:
                continue
            x = (rhs[i] * d - b * rhs[j]) / determinant
            y = (a * rhs[j] - rhs[i] * c) / determinant
            if all(a * x + b * y <= value for (a, b), value in zip(rows, rhs)):
                vertices.append((x, y))
        expected = min(1 + cutoff, F(7, 4) + cutoff / 4, F(5, 2))
        assert vertices and max(x for x, _ in vertices) == expected
        count += 1

    # Check the uniform slope across both basis cells, including cross-cell
    # pairs, rather than inferring it from consecutive iterate ratios.
    points = [F(i, 4) for i in range(33)]
    for a in points:
        for b in points:
            fa = min(a / 4, a / 16 + F(3, 8))
            fb = min(b / 4, b / 16 + F(3, 8))
            assert abs(fa - fb) <= abs(a - b) / 4
    return {"independent_cutoff_LPs": count, "cross_cell_pairs": len(points) ** 2}


def check_basis_float_rejection():
    path = MODULE.parent / "check_constrained_obbt.py"
    spec = importlib.util.spec_from_file_location("review_constrained", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # On the initially reviewed version this was falsely accepted because the
    # nonbasis row's floating dot product rounded 10^16+1 down to 10^16.
    args = ([[1, 0], [0, 1], [1e16, 1]], [1, 1, 10**16],
            [[0], [0], [0]], [1, 0], [0, 1], [[0]])
    must_reject(module.verify_basis_cell, *args)
    # The integer-data version must also reject the infeasible proposed point.
    exact_args = ([[1, 0], [0, 1], [10**16, 1]], *args[1:])
    must_reject(module.verify_basis_cell, *exact_args)
    return 2


def check_atomic_driver():
    # Independent exact proposal oracle: no SciPy or production LP checker is
    # used to construct the negative-domain optimum and its support proof.
    sys.modules["certificates"] = cert
    path = MODULE.parent / "certified_driver.py"
    spec = importlib.util.spec_from_file_location("review_driver", path)
    driver = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = driver
    spec.loader.exec_module(driver)
    model = cert.Model(1, (), (), (0,), 7)
    initial = cert.Box((-2,), (3,))

    def oracle(rows, objective):
        assert len(rows) == 3
        if objective == (F(1),):
            return driver.LPProposal((-2,), (-1, 0, 0))
        assert objective == (F(-1),)
        return driver.LPProposal((3,), (0, -1, 0))

    result = driver.certified_closure(model, initial, 7, proposal_solver=oracle)
    assert result.status == "fixed" and result.lp_calls == 2
    assert result.box == initial and len(result.rounds) == 1
    for step in result.rounds:
        rows = model.relaxation_rows(step.input_box, 7)
        for direction, optimum in enumerate(step.optima):
            expected_objective = (F(1 if direction == 0 else -1),)
            assert optimum.objective == expected_objective
            assert all(value <= 0 for value in optimum.dual)
            assert all(sum(a * x for a, x in zip(row.coefficients, optimum.primal)) <= row.rhs
                       for row in rows)
            column_sum = sum(row.coefficients[0] * y for row, y in zip(rows, optimum.dual))
            assert column_sum == expected_objective[0]
            assert sum(row.rhs * y for row, y in zip(rows, optimum.dual)) == (
                expected_objective[0] * optimum.primal[0]
            ) == optimum.value

    def wrong_direction(rows, objective):
        # A valid proof for the lower objective is not a valid upper proof.
        return oracle(rows, (F(1),))

    failed = driver.certified_closure(model, initial, 7, proposal_solver=wrong_direction)
    assert failed.status == "inconclusive" and failed.lp_calls == 2
    assert failed.box == initial and not failed.rounds and failed.certificate is None

    infeasible_model = cert.Model(1, (), (cert.Row((-1,), -2),), (0,))
    empty_proposal = driver.certified_closure(
        infeasible_model, cert.Box((0,), (1,)), 0,
        proposal_solver=lambda rows, objective: None,
    )
    assert empty_proposal.status == "inconclusive"
    assert not empty_proposal.rounds and empty_proposal.certificate is None
    return 3


def check_unbudgeted_rejections():
    native, enhancement, credit, rate, cap = map(F, (1, 1, 1, 0, 1))
    rejected_entry_work = 100 * F(1, 10)
    assert enhancement <= credit + rate * native + cap
    assert enhancement + rejected_entry_work > credit + rate * native + cap
    return str(rejected_entry_work)


if __name__ == "__main__":
    print(json.dumps({
        "scope_boundary_cases": check_scope_boundaries(),
        "nested_mccormick_points": check_nested_mccormick(),
        "observed_ratio_counterexample": check_observed_ratio_failure(),
        "tail_majorant_partial_sums": check_tail_majorant_boundary(),
        "constrained_supports": check_constrained_supports(),
        "basis_arithmetic_rejections": check_basis_float_rejection(),
        "atomic_driver_cases": check_atomic_driver(),
        "unbudgeted_rejected_entry_cost": check_unbudgeted_rejections(),
        "result": "passed",
    }, indent=2))
