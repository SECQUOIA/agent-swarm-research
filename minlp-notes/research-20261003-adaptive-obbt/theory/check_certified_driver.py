#!/usr/bin/env python3
"""Targeted LP proposal, exact replay, stopping, and failure-path checks."""

import json
from fractions import Fraction as Q

from certificates import Box, Model, Row, verify_protected_box
from certified_driver import LPProposal, certified_closure, scipy_lp_proposal, verify_lp_optimum
from check_remaining_benefit import quadratic_stall, squares


def replay(model, initial, cutoff, result):
    box = initial
    for step in result.rounds:
        assert step.input_box == box
        rows = model.relaxation_rows(box, cutoff)
        assert len(step.optima) == 2 * model.n
        for i, optimum in enumerate(step.optima):
            objective = tuple(Q((1 if i % 2 == 0 else -1) if j == i // 2 else 0) for j in range(model.dimension))
            assert optimum.objective == objective
            assert verify_lp_optimum(rows, objective, optimum.primal, optimum.dual) == optimum
        box = Box(
            tuple(step.optima[2 * i].primal[i] for i in range(model.n)),
            tuple(step.optima[2 * i + 1].primal[i] for i in range(model.n)),
        )
        assert box == step.output_box
    assert result.box == box
    if result.certificate is not None:
        cert = result.certificate
        assert verify_protected_box(model, initial, box, cutoff, cert.witnesses) == cert
        assert cert.ceilings(model, box, cutoff) == ((Q(0),) * model.n,) * 2


def main():
    outcomes = []

    def record(name, model, box, cutoff, **kwargs):
        result = certified_closure(model, box, cutoff, **kwargs)
        replay(model, box, cutoff, result)
        assert result.seconds_including_exact_checks >= 0
        outcomes.append({
            "fixture": name, "status": result.status,
            "certified_rounds": len(result.rounds), "lp_calls": result.lp_calls,
            "seconds_including_exact_checks": result.seconds_including_exact_checks,
            "lower": [str(v) for v in result.box.lower],
            "upper": [str(v) for v in result.box.upper],
            "objective_ceiling": str(result.certificate.objective_ceiling) if result.certificate else None,
            "reason": result.reason,
        })
        return result

    stall = record("quadratic_stall", quadratic_stall(), Box((-1,) * 3, (1,) * 3), 0, improve_objective=True)
    assert stall.status == "fixed" and len(stall.rounds) == 1 and stall.lp_calls == 7
    assert stall.objective_lp_accepted and stall.certificate.objective_ceiling == -3

    linear_rows = (Row((-1, -1), -1), Row((1, -1), 0), Row((-1, 1), 0))
    linear = Model(2, (), linear_rows, (0, 0))
    coupled = record("linear_coupled", linear, Box((0, 0), (2, 2)), 0)
    assert coupled.status == "fixed" and coupled.lp_calls == 4
    assert coupled.box == Box((Q(1, 2), Q(1, 2)), (2, 2))

    # Free LP variables are essential: default nonnegative solver bounds would
    # silently remove feasible negative endpoints before proof replay.
    negative = record("negative_linear_box", Model(1, (), (), (0,)), Box((-3,), (-1,)), 0)
    assert negative.status == "fixed" and negative.box == Box((-3,), (-1,))

    square = squares(1)
    zero = record("zero_cutoff_geometric_contraction", square, Box((0,), (1,)), 0, max_rounds=5)
    assert zero.status == "unfinished" and len(zero.rounds) == 5 and zero.lp_calls == 10
    assert zero.box == Box((0,), (Q(1, 32),)) and zero.certificate is None

    positive = record("positive_cutoff_newton_contraction", square, Box((0,), (2,)), 1, max_rounds=3)
    assert positive.status == "unfinished" and positive.lp_calls == 6
    assert positive.box == Box((0,), (Q(3281, 3280),)) and positive.certificate is None
    upper = Q(2)
    for step in positive.rounds:
        upper = (upper * upper + 1) / (2 * upper)
        assert step.output_box.upper == (upper,) and upper > 1

    # With finite reconstruction precision the driver may become inconclusive;
    # it must not round the positive limiting floor into an exact fixed point.
    long_run = record("positive_cutoff_precision_limit", square, Box((0,), (2,)), 1, max_rounds=12)
    assert long_run.status in ("inconclusive", "unfinished") and long_run.box.upper[0] > 1
    assert long_run.certificate is None

    skipped = record("zero_round_budget", square, Box((0,), (1,)), 0, max_rounds=0)
    assert skipped.status == "unfinished" and not skipped.rounds and skipped.lp_calls == 0

    # Reject a feasible but nonoptimal point; discard the entire incomplete
    # round, including the preceding correctly certified coordinate endpoint.
    calls = 0

    def faulty_second(rows, objective):
        nonlocal calls
        calls += 1
        if calls == 2:
            return LPProposal((Q(1, 4), Q(0)), tuple(Q(0) for _ in rows))
        return scipy_lp_proposal(rows, objective)

    bad = record("invalid_dual_discards_round", square, Box((0,), (1,)), 0, proposal_solver=faulty_second)
    assert bad.status == "inconclusive" and bad.lp_calls == 2 and bad.box == Box((0,), (1,)) and not bad.rounds

    # Failure during a later round preserves, and accounts for, earlier proof.
    calls = 0

    def faulty_third(rows, objective):
        nonlocal calls
        calls += 1
        return None if calls == 3 else scipy_lp_proposal(rows, objective)

    late = record("failed_proposal_preserves_prior_round", square, Box((0,), (1,)), 0, proposal_solver=faulty_third)
    assert late.status == "inconclusive" and late.lp_calls == 3 and len(late.rounds) == 1
    assert late.box == Box((0,), (Q(1, 2),))

    calls = 0

    def faulty_objective(rows, objective):
        nonlocal calls
        calls += 1
        if calls == 3:
            return LPProposal((float("nan"),), ())
        return scipy_lp_proposal(rows, objective)

    optional = record("invalid_optional_objective_keeps_certificate", Model(1, (), (), (0,)), Box((0,), (1,)), 0,
                      proposal_solver=faulty_objective, improve_objective=True)
    assert optional.status == "fixed" and optional.lp_calls == 3 and not optional.objective_lp_accepted

    # Each exact LP contract is checked separately, including dual sign and
    # zero duality gap; these failures can occur despite plausible primal data.
    rows = (Row((-1,), 0), Row((1,), 1))
    invalid = (
        ((-1,), (-1, 0)),      # primal infeasible
        ((0,), (0, 1)),        # wrong dual sign, although A^T*dual=1
        ((0,), (0, 0)),        # incorrect stationarity
        ((Q(1, 2),), (-1, 0)), # nonzero duality gap
        ((0,), (-1,)),         # wrong row count
    )
    for primal, dual in invalid:
        try:
            verify_lp_optimum(rows, (1,), primal, dual)
        except ValueError:
            continue
        raise AssertionError("Invalid LP proof accepted")
    assert verify_lp_optimum(rows, (1,), (0,), (-1, 0)).value == 0
    print(json.dumps({"driver_checks": outcomes, "invalid_lp_certificates_rejected": len(invalid)}, indent=2))


if __name__ == "__main__":
    main()
