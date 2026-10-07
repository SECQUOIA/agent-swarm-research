"""Bounded exact-certificate OBBT workflow for the rational model in certificates.

SciPy proposes LP optima; rational primal/dual replay authorizes each complete
round. A protected-box check after rebuilding authorizes finite termination.
Failure to reconstruct a proof is inconclusive, not a numerical certificate.
This standalone reference driver does not certify native SCIP rows or claim
that its LP and exact-arithmetic costs improve solving time.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from math import isfinite
from time import perf_counter
from typing import Callable

from certificates import Box, dot, rational, vector, verify_protected_box


@dataclass(frozen=True)
class LPProposal:
    primal: tuple
    dual: tuple


@dataclass(frozen=True)
class LPOptimum:
    objective: tuple
    primal: tuple
    dual: tuple
    value: Q


@dataclass(frozen=True)
class CertifiedRound:
    input_box: Box
    output_box: Box
    optima: tuple


@dataclass(frozen=True)
class ClosureResult:
    status: str
    box: Box
    certificate: object
    rounds: tuple
    lp_calls: int
    seconds_including_exact_checks: float
    reason: str
    objective_lp_accepted: bool


def scipy_lp_proposal(rows, objective):
    """All variable bounds belong to rows; HiGHS variables are unrestricted."""
    from scipy.optimize import linprog

    result = linprog(
        [float(v) for v in objective],
        A_ub=[[float(v) for v in row.coefficients] for row in rows],
        b_ub=[float(row.rhs) for row in rows],
        bounds=[(None, None)] * len(objective),
        method="highs",
    )
    if not result.success:
        return None
    return LPProposal(tuple(result.x), tuple(result.ineqlin.marginals))


def recover_rationals(values, max_denominator):
    """Reconstruction proposes exact values; subsequent row replay proves them."""
    recovered = []
    for value in values:
        if isinstance(value, (int, Q, str)):
            recovered.append(rational(value))
        else:
            value = float(value)
            if not isfinite(value):
                raise ValueError("Nonfinite LP proposal")
            recovered.append(Q(str(value)).limit_denominator(max_denominator))
    return tuple(recovered)


def verify_lp_optimum(rows, objective, primal, dual):
    """Check min c*z over A*z<=b using lambda<=0 and A^T*lambda=c.

    Feasible primal and dual points with equal objectives prove optimality.
    No floating tolerance, solver status, or implicit variable bound is used.
    """
    objective, primal, dual = map(vector, (objective, primal, dual))
    n = len(objective)
    if (
        not n or len(primal) != n or len(dual) != len(rows)
        or any(len(row.coefficients) != n for row in rows)
    ):
        raise ValueError("LP certificate dimension mismatch")
    if not all(row.holds(primal) for row in rows):
        raise ValueError("LP primal violates an exact row")
    if any(multiplier > 0 for multiplier in dual):
        raise ValueError("LP dual has a positive inequality multiplier")
    if any(
        sum((row.coefficients[i] * multiplier for row, multiplier in zip(rows, dual)), Q(0))
        != objective[i]
        for i in range(n)
    ):
        raise ValueError("LP dual does not reproduce the objective")
    primal_value = dot(objective, primal)
    if primal_value != dot(tuple(row.rhs for row in rows), dual):
        raise ValueError("LP primal and dual objectives differ")
    return LPOptimum(objective, primal, dual, primal_value)


def certified_closure(
    model, initial_box, cutoff, max_rounds=10,
    proposal_solver: Callable = scipy_lp_proposal,
    max_denominator=10**9, improve_objective=False,
):
    """Run simultaneous OBBT rounds, then replay witnesses on each rebuilt box.

    Status ``fixed`` means a protected-box certificate proves no coordinate can
    improve in any further round of this fixed LP family and cutoff. Status
    ``unfinished`` means the round budget was exhausted. Status ``inconclusive``
    means a proposed LP optimum failed exact reconstruction; the incomplete
    round is discarded, while previous certified rounds remain valid.

    Exact termination need not occur in finite time. Failed protected-box checks
    are expected on contracting instances and do not invalidate an OBBT round.
    An optional final objective LP needs only exact primal feasibility: it can
    lower the ceiling on future relaxation lower bounds, not certify nonlinear
    feasibility or a globally optimal nonlinear objective.
    """
    started = perf_counter()
    if isinstance(max_rounds, bool) or not isinstance(max_rounds, int) or max_rounds < 0:
        raise ValueError("max_rounds must be a nonnegative integer")
    if isinstance(max_denominator, bool) or not isinstance(max_denominator, int) or max_denominator < 1:
        raise ValueError("max_denominator must be a positive integer")
    cutoff = rational(cutoff)
    # Check dimensions even when no round is requested.
    model.relaxation_rows(initial_box, cutoff)
    box, rounds, calls = initial_box, [], 0

    def finish(status, reason, certificate=None, objective_lp_accepted=False):
        return ClosureResult(
            status, box, certificate, tuple(rounds), calls,
            perf_counter() - started, reason, objective_lp_accepted,
        )

    def propose(rows, objective):
        nonlocal calls
        calls += 1
        return proposal_solver(rows, objective)

    for _ in range(max_rounds):
        rows = model.relaxation_rows(box, cutoff)
        optima = []
        for coordinate in range(model.n):
            for sign in (1, -1):
                objective = tuple(Q(sign if i == coordinate else 0) for i in range(model.dimension))
                try:
                    proposal = propose(rows, objective)
                    if proposal is None:
                        return finish("inconclusive", "The LP solver did not propose an optimum")
                    optima.append(verify_lp_optimum(
                        rows, objective,
                        recover_rationals(proposal.primal, max_denominator),
                        recover_rationals(proposal.dual, max_denominator),
                    ))
                except (ValueError, TypeError, ArithmeticError) as error:
                    return finish("inconclusive", str(error))
        candidate = Box(
            tuple(optima[2 * i].primal[i] for i in range(model.n)),
            tuple(optima[2 * i + 1].primal[i] for i in range(model.n)),
        )
        if not box.contains(candidate):
            raise AssertionError("Certified endpoint optima escaped their bound rows")
        previous = box
        rounds.append(CertifiedRound(previous, candidate, tuple(optima)))
        box = candidate
        witnesses = tuple(optimum.primal for optimum in optima)
        try:
            certificate = verify_protected_box(model, previous, candidate, cutoff, witnesses)
        except ValueError:
            continue
        accepted = False
        if improve_objective:
            try:
                proposal = propose(model.relaxation_rows(candidate, cutoff), model.objective)
                if proposal is not None:
                    point = recover_rationals(proposal.primal, max_denominator)
                    if model.feasible(candidate, point, cutoff):
                        certificate = verify_protected_box(
                            model, previous, candidate, cutoff, (*witnesses, point),
                        )
                        accepted = True
            except (ValueError, TypeError, ArithmeticError):
                # Optional objective work cannot invalidate an existing proof.
                pass
        return finish("fixed", "Rebuilt endpoint witnesses certify a fixed box", certificate, accepted)
    return finish("unfinished", "The round budget was exhausted without a fixed-box certificate")
